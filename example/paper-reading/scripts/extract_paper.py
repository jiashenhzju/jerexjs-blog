#!/usr/bin/env python3
"""Extract structured content and figures from a scientific PDF.

Produces machine-readable JSON plus a raw English markdown preview that an
LLM agent can then translate / annotate. Figures are rendered as page-region
PNGs (not just embedded bitmaps) so vector art / composite figures survive.

Usage:
    python extract_paper.py <pdf_path> [--out <dir>] [--dpi 200]

Default <dir>: <cwd>/paper_reading/<pdf_stem>/
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from statistics import median
from typing import Iterable

try:
    import fitz  # PyMuPDF
except ImportError as e:  # pragma: no cover
    sys.stderr.write(
        "[extract_paper] PyMuPDF not installed. Run scripts/setup_env.sh first.\n"
    )
    raise

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

# Keep the label alternatives case-insensitive, but leave the caption-title
# lookahead case-sensitive. Many arXiv templates omit punctuation after the
# number ("Figure 1 Overview ..."). In that form we only accept an uppercase
# next word, which avoids treating prose such as "Figure 2a reports ..." as a
# caption.
CAPTION_RE = re.compile(
    r"^\s*((?i:Figure|Fig\.|Fig|Table|Tab\.|Tab|Algorithm|Alg\.))"
    r"\s*([0-9]+[a-zA-Z]?)\s*(?:[\.:\uff1a\u3002]\s*|(?=[A-Z]))"
)
HEADING_NUM_RE = re.compile(r"^\s*\d+(\.\d+){0,3}\.?\s+\S")
APPENDIX_HEAD_RE = re.compile(r"^\s*[A-Z]\.\s+[A-Z]")
REFERENCES_HEAD_RE = re.compile(
    r"^\s*(references|bibliography|\u53c2\u8003\u6587\u732e)\s*$", re.IGNORECASE
)
# Lines like "[12]" or "1." at start of reference entries.
REF_ENTRY_RE = re.compile(r"^\s*(\[\d+\]|\d+\.)\s+\S")


@dataclass
class Block:
    id: str
    type: str  # title | heading | paragraph | caption | list | equation | figure
    text: str = ""
    page: int = 0
    bbox: tuple[float, float, float, float] | None = None
    column: int = 0  # 0 = left / single, 1 = right
    # heading-only
    level: int | None = None
    # figure-only
    image_path: str | None = None
    caption: str | None = None
    figure_label: str | None = None  # e.g. "Figure 1"
    # font metadata (debug / classification)
    avg_size: float | None = None
    is_bold: bool = False

    def to_public(self) -> dict:
        d = asdict(self)
        # drop internal-only fields from public JSON
        for k in ("avg_size", "is_bold"):
            d.pop(k, None)
        if d.get("bbox") is not None:
            d["bbox"] = [round(v, 2) for v in d["bbox"]]
        # drop None values to keep JSON compact
        return {k: v for k, v in d.items() if v is not None and v != ""}


# ---------------------------------------------------------------------------
# Geometry / layout helpers
# ---------------------------------------------------------------------------


def detect_column_count(pages_blocks: list[list[dict]], page_width: float) -> int:
    """Return 1 or 2 based on distribution of text block centers."""
    xs: list[float] = []
    for pb in pages_blocks:
        for b in pb:
            if b.get("type") != 0:  # 0 == text block in PyMuPDF dict mode
                continue
            x0, _y0, x1, _y1 = b["bbox"]
            # ignore very wide blocks (likely full-width headers / captions)
            if (x1 - x0) > 0.75 * page_width:
                continue
            xs.append((x0 + x1) / 2.0)
    if len(xs) < 20:
        return 1
    mid = page_width / 2.0
    left = sum(1 for x in xs if x < mid)
    right = len(xs) - left
    # If one side holds >85% of blocks, it's single-column.
    if left / len(xs) > 0.85 or right / len(xs) > 0.85:
        return 1
    return 2


def column_of(bbox: tuple[float, float, float, float], page_width: float, col_cnt: int) -> int:
    if col_cnt == 1:
        return 0
    cx = (bbox[0] + bbox[2]) / 2.0
    return 0 if cx < page_width / 2.0 else 1


def is_full_width(bbox: tuple[float, float, float, float], page_width: float) -> bool:
    return (bbox[2] - bbox[0]) > 0.75 * page_width


# ---------------------------------------------------------------------------
# Text extraction / classification
# ---------------------------------------------------------------------------


def _block_text_and_font(block: dict) -> tuple[str, float, bool]:
    """Flatten a PyMuPDF dict block to (text, avg_font_size, is_mostly_bold)."""
    parts: list[str] = []
    sizes: list[float] = []
    bold_chars = 0
    total_chars = 0
    for line in block.get("lines", []):
        line_parts: list[str] = []
        for span in line.get("spans", []):
            text = span.get("text", "")
            if not text:
                continue
            line_parts.append(text)
            sizes.append(span.get("size", 0.0))
            font = (span.get("font") or "").lower()
            is_bold = "bold" in font or "black" in font or "heavy" in font
            total_chars += len(text)
            if is_bold:
                bold_chars += len(text)
        if line_parts:
            parts.append("".join(line_parts))
    text = "\n".join(parts).strip()
    avg_size = sum(sizes) / len(sizes) if sizes else 0.0
    is_bold = (bold_chars / total_chars) > 0.6 if total_chars else False
    return text, avg_size, is_bold


def classify_block(
    text: str, avg_size: float, is_bold: bool, body_size: float
) -> tuple[str, int | None]:
    """Return (block_type, heading_level_or_None)."""
    if not text:
        return "paragraph", None
    stripped = text.strip()
    single_line = "\n" not in stripped

    # Caption / figure-table reference
    if CAPTION_RE.match(stripped):
        return "caption", None

    # Heading heuristics
    # 1. Larger font than body AND short
    if avg_size > body_size * 1.1 and len(stripped) < 200 and single_line:
        # Guess level by how much larger.
        ratio = avg_size / body_size
        if ratio > 1.6:
            return "title", 0
        if ratio > 1.3:
            return "heading", 1
        return "heading", 2
    # 2. Numbered section like "3.1 Method"
    if HEADING_NUM_RE.match(stripped) and len(stripped) < 200 and single_line:
        depth = stripped.split()[0].count(".") + 1
        return "heading", min(depth, 3)
    # 2b. Appendix-style section like "A. Sim-to-Real Gap"
    if APPENDIX_HEAD_RE.match(stripped) and len(stripped) < 200 and single_line:
        return "heading", 1
    # 3. Bold short single-line -> likely subheading
    if is_bold and len(stripped) < 120 and single_line:
        return "heading", 3
    # 4. List item
    if re.match(r"^\s*([\u2022\-\*]|\(?\d+\)|[a-zA-Z]\))\s+\S", stripped):
        return "list", None

    return "paragraph", None


def estimate_body_font_size(blocks_with_font: list[tuple[dict, float]]) -> float:
    sizes = [sz for _, sz in blocks_with_font if sz > 0]
    return median(sizes) if sizes else 10.0


# ---------------------------------------------------------------------------
# Page processing
# ---------------------------------------------------------------------------


def detect_header_footer(pages_raw: list[list[dict]], n_pages: int) -> tuple[set[str], set[str]]:
    """Find repeated short texts in top/bottom 8% of pages -> headers/footers."""
    top_counts: dict[str, int] = {}
    bot_counts: dict[str, int] = {}
    for pb in pages_raw:
        if not pb:
            continue
        for b in pb:
            if b.get("type") != 0:
                continue
            text = b.get("_text", "").strip()
            if not text or len(text) > 120:
                continue
            y0 = b["bbox"][1]
            y1 = b["bbox"][3]
            page_h = b["_page_h"]
            if y1 < page_h * 0.08:
                top_counts[text] = top_counts.get(text, 0) + 1
            elif y0 > page_h * 0.92:
                bot_counts[text] = bot_counts.get(text, 0) + 1
    threshold = max(3, int(n_pages * 0.4))
    headers = {t for t, c in top_counts.items() if c >= threshold}
    footers = {t for t, c in bot_counts.items() if c >= threshold}
    # page numbers like "12" or "Page 12" at bottom -> always drop
    footers.update({t for t in bot_counts if re.fullmatch(r"\d{1,4}", t)})
    return headers, footers


def _collect_visual_rects(
    page: fitz.Page,
    col_left: float,
    col_right: float,
    y_min: float,
    y_max: float,
) -> list[fitz.Rect]:
    """Collect bboxes of bitmaps + non-trivial vector drawings within a region."""
    rects: list[fitz.Rect] = []

    # 1. Embedded bitmaps
    try:
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                for r in page.get_image_rects(xref):
                    if not (y_min <= r.y0 and r.y1 <= y_max):
                        continue
                    cx = (r.x0 + r.x1) / 2.0
                    if not (col_left - 5 <= cx <= col_right + 5):
                        continue
                    if r.width < 20 or r.height < 20:
                        continue
                    rects.append(fitz.Rect(r))
            except Exception:
                pass
    except Exception:
        pass

    # 2. Vector drawings (paths, rules, filled shapes)
    try:
        for d in page.get_drawings():
            r = d.get("rect")
            if r is None:
                continue
            if not (y_min <= r.y0 and r.y1 <= y_max):
                continue
            cx = (r.x0 + r.x1) / 2.0
            if not (col_left - 5 <= cx <= col_right + 5):
                continue
            # Skip hairline rulers and borders
            if r.width < 10 or r.height < 4:
                continue
            rects.append(fitz.Rect(r))
    except Exception:
        pass

    return rects


def _union(rects: list[fitz.Rect]) -> fitz.Rect:
    x0 = min(r.x0 for r in rects)
    y0 = min(r.y0 for r in rects)
    x1 = max(r.x1 for r in rects)
    y1 = max(r.y1 for r in rects)
    return fitz.Rect(x0, y0, x1, y1)


def _rect_area(r: fitz.Rect) -> float:
    return max(0.0, r.width) * max(0.0, r.height)


def _rects_overlap(a: fitz.Rect, b: fitz.Rect, tol: float = 2.0) -> bool:
    return not (
        a.x1 <= b.x0 + tol
        or a.x0 >= b.x1 - tol
        or a.y1 <= b.y0 + tol
        or a.y0 >= b.y1 - tol
    )


def _is_mostly_contained(
    rect: fitz.Rect, others: list[fitz.Rect], threshold: float = 0.7
) -> bool:
    """True if `rect` is mostly inside the union of `others`.

    Used during the walk to decide whether to skip a candidate that is already
    represented by an accepted item. We want to skip duplicates (a thin label
    that sits inside a bitmap) but NOT skip a tall bitmap that merely shares
    a thin overlap with an accepted separator line.
    """
    if not others:
        return False
    own = max(0.0, rect.width) * max(0.0, rect.height)
    if own <= 0:
        return True
    best_inter = 0.0
    for o in others:
        ix0 = max(rect.x0, o.x0)
        ix1 = min(rect.x1, o.x1)
        iy0 = max(rect.y0, o.y0)
        iy1 = min(rect.y1, o.y1)
        if ix0 < ix1 and iy0 < iy1:
            best_inter = max(best_inter, (ix1 - ix0) * (iy1 - iy0))
    return (best_inter / own) > threshold


def _looks_like_prose(text: str) -> bool:
    """Heuristic: body paragraphs have multiple sentence terminators.

    Table data and figure labels rarely contain ". " (period+space) patterns —
    they have isolated decimals (0.7390) or symbols (↑↓). Body paragraphs almost
    always have multiple sentences.
    """
    return text.count(". ") >= 2 or text.count("。") >= 2 or text.count(".\n") >= 2


def _caption_kind_of(text: str) -> str:
    """Classify a caption text as 'figure' | 'table' | 'algorithm'."""
    m = CAPTION_RE.match(text.strip())
    if not m:
        return "figure"
    label = m.group(1).lower().rstrip(".")
    if label in ("table", "tab"):
        return "table"
    if label in ("algorithm", "alg"):
        return "algorithm"
    return "figure"


def _walk_content_band(
    page_blocks: list[dict],
    visuals: list[fitz.Rect],
    direction: str,  # 'above' | 'below'
    caption_y0: float,
    caption_y1: float,
    bound_top: float,
    bound_bot: float,
    col_left: float,
    col_right: float,
    caption_full_width: bool,
    body_size: float,
    caption_kind: str,
    claimed_rects: list[fitz.Rect],
) -> fitz.Rect | None:
    """Walk content adjacent to caption in `direction` and return the union bbox.

    The walk starts from the caption edge, accepts content (visuals + text)
    within a maximum gap to the caption, and stops when it encounters a
    section heading, body paragraph, claimed region, or large vertical gap.

    Returns None if no acceptable content adjacent to the caption.
    """
    MAX_INITIAL_GAP = 80.0  # first item must be this close to caption
    MAX_CONT_GAP = 35.0  # subsequent items must be within this gap

    # ---- build unified candidate list (visuals + text blocks) ----
    items: list[tuple[float, float, fitz.Rect, str, dict | None]] = []
    for r in visuals:
        items.append((r.y0, r.y1, fitz.Rect(r), "visual", None))
    for b in page_blocks:
        if b.get("type") != 0:
            continue
        bx0, by0, bx1, by1 = b["bbox"]
        if by1 <= bound_top or by0 >= bound_bot:
            continue
        bcx = (bx0 + bx1) / 2.0
        if not caption_full_width:
            if not (col_left - 10 <= bcx <= col_right + 10):
                continue
        text = (b.get("_text") or "").strip()
        if not text:
            continue
        items.append((by0, by1, fitz.Rect(bx0, by0, bx1, by1), "text", b))

    if not items:
        return None

    # ---- restrict to the search direction & sort by closeness to caption ----
    if direction == "above":
        items = [it for it in items if it[1] <= caption_y0 - 0.5]
        items.sort(key=lambda it: -it[1])  # closest (largest y1) first
    else:
        items = [it for it in items if it[0] >= caption_y1 + 0.5]
        items.sort(key=lambda it: it[0])  # closest (smallest y0) first

    if not items:
        return None

    # ---- walk ----
    accepted: list[tuple[fitz.Rect, str]] = []  # (rect, kind)
    pos_close = caption_y0 if direction == "above" else caption_y1

    body_para_min_w = (col_right - col_left) * 0.45

    for y0, y1, rect, kind, blk in items:
        # Skip items that are mostly inside an already-accepted region (e.g.
        # the caption text inside a separator drawing) — but DO NOT skip an
        # item that merely shares a thin slice with an accepted thin rule.
        if accepted and _is_mostly_contained(rect, [a[0] for a in accepted]):
            continue

        # gap from frontier to next item.  Vertically-interleaved content
        # (e.g. a small label sitting between two bitmap rows) shows up as a
        # negative raw gap; clamp to zero so it counts as "tightly adjacent"
        # rather than getting rejected.
        if direction == "above":
            gap = max(0.0, pos_close - y1)
        else:
            gap = max(0.0, y0 - pos_close)

        if not accepted:
            if gap > MAX_INITIAL_GAP:
                return None
        else:
            if gap > MAX_CONT_GAP:
                break

        # claimed-region guard
        if any(_rects_overlap(rect, c) for c in claimed_rects):
            break

        text = (blk.get("_text") or "").strip() if blk else ""
        wc = len(text.split())
        width = rect.width

        if kind == "text":
            avg_size = (blk.get("_avg_size") or 0.0) if blk else 0.0
            is_bold = bool(blk.get("_is_bold")) if blk else False

            # Section heading or References → stop
            if HEADING_NUM_RE.match(text) and len(text) < 200 and "\n" not in text:
                break
            if (
                APPENDIX_HEAD_RE.match(text)
                and len(text) < 200
                and "\n" not in text
            ):
                break
            if REFERENCES_HEAD_RE.match(text):
                break
            # Bold short title-cased line → likely a heading.  Only trigger
            # when the font is clearly larger than body AND the line runs
            # across most of the column (real headings span the column;
            # in-figure labels are short snippets).
            if (
                is_bold
                and wc <= 8
                and avg_size > body_size * 1.25
                and width >= (col_right - col_left) * 0.35
                and accepted
            ):
                break
            # Body paragraph (multiple sentences)
            if _looks_like_prose(text):
                if accepted:
                    break
                return None

            # Caption-kind specific filtering
            if caption_kind in ("figure", "algorithm"):
                # Inside figures, in-text annotations / sub-captions can be a
                # full sentence (e.g. "Replace the plain sky with the dramatic
                # sunset."). Only stop on clearly body-sized prose: wide AND
                # long. The prose-pattern check above already catches multi-
                # sentence body paragraphs.
                if wc >= 30 and width >= body_para_min_w:
                    if accepted:
                        break
                    return None
            elif caption_kind == "table":
                # If we've already grabbed visuals, don't extend with text.
                if any(k == "visual" for _, k in accepted):
                    break
                # Tables are mostly text, but a short full-column body
                # paragraph can sit directly below them without satisfying
                # `_looks_like_prose` (for example, a single 20-word
                # sentence). Once table content has been accepted, treat a
                # body-sized, paragraph-width block as the boundary.
                digit_ratio = (
                    sum(bool(re.search(r"\d", token)) for token in text.split())
                    / max(1, wc)
                )
                if (
                    accepted
                    and wc >= 14
                    and width >= body_para_min_w
                    and avg_size >= body_size * 0.9
                    and digit_ratio < 0.25
                ):
                    break

        elif kind == "visual":
            if caption_kind == "table":
                # If we already grabbed table-text, don't extend with visuals.
                if any(k == "text" for _, k in accepted):
                    break

        accepted.append((rect, kind))
        if direction == "above":
            pos_close = min(pos_close, y0)
        else:
            pos_close = max(pos_close, y1)

    if not accepted:
        return None

    bbox = _union([a[0] for a in accepted])
    if bbox.height < 15 or bbox.width < 30:
        return None
    return bbox


def find_figure_bbox(
    caption_bbox: tuple[float, float, float, float],
    caption_kind: str,
    page_blocks: list[dict],
    page: fitz.Page,
    col_cnt: int,
    body_size: float,
    prev_caption_y1: float,
    next_caption_y0: float,
    claimed_rects: list[fitz.Rect],
) -> fitz.Rect | None:
    """Figure / table region adjacent to the given caption.

    Algorithm:
        - Determine the primary search direction by caption type:
            Figure / Algorithm → look ABOVE caption first.
            Table              → look BELOW caption first.
        - Inside the bounded region (by neighbour captions in the same column),
          walk content (visuals + text) outward from the caption edge, accepting
          tightly-adjacent items. Stop at a section heading, body paragraph,
          claimed region, or large vertical gap.
        - If visuals span beyond the caption's column, auto-expand to full-page
          width.
        - Fall back to the secondary direction if the primary returned nothing.
    """
    page_rect = page.rect
    page_w = page_rect.width
    page_h = page_rect.height

    cx = (caption_bbox[0] + caption_bbox[2]) / 2.0
    # A caption is treated as "full-width" if it's wide OR centered exactly
    # at the page midline (typical for tables centered across columns).
    caption_full_width = (
        is_full_width(caption_bbox, page_w) or abs(cx - page_w / 2.0) < 30.0
    )

    if col_cnt == 2 and not caption_full_width:
        if cx < page_w / 2.0:
            col_left, col_right = 0.0, page_w / 2.0
        else:
            col_left, col_right = page_w / 2.0, page_w
    else:
        col_left, col_right = 0.0, page_w

    bound_top = max(0.0, prev_caption_y1 + 1.0)
    bound_bot = min(page_h, next_caption_y0 - 1.0)

    def _collect_with_optional_expand(y0: float, y1: float) -> tuple[list[fitz.Rect], bool]:
        rects = _collect_visual_rects(page, col_left, col_right, y0, y1)
        wide_used = caption_full_width
        if rects and col_cnt == 2 and not caption_full_width:
            u = _union(rects)
            if u.x0 < col_left - 10 or u.x1 > col_right + 10:
                rects = _collect_visual_rects(page, 0.0, page_w, y0, y1)
                wide_used = True
        rects = [r for r in rects if not any(_rects_overlap(r, c) for c in claimed_rects)]
        return rects, wide_used

    above_y0, above_y1 = bound_top, caption_bbox[1] - 1.0
    below_y0, below_y1 = caption_bbox[3] + 1.0, bound_bot
    visuals_above, full_above = _collect_with_optional_expand(above_y0, above_y1)
    visuals_below, full_below = _collect_with_optional_expand(below_y0, below_y1)

    primary = "above" if caption_kind in ("figure", "algorithm") else "below"
    secondary = "below" if primary == "above" else "above"

    for direction in (primary, secondary):
        if direction == "above":
            visuals = visuals_above
            full = full_above
        else:
            visuals = visuals_below
            full = full_below
        eff_full = caption_full_width or full
        eff_left = 0.0 if eff_full else col_left
        eff_right = page_w if eff_full else col_right

        bbox = _walk_content_band(
            page_blocks,
            visuals,
            direction,
            caption_bbox[1],
            caption_bbox[3],
            bound_top,
            bound_bot,
            eff_left,
            eff_right,
            eff_full,
            body_size,
            caption_kind,
            claimed_rects,
        )
        if bbox is not None:
            return fitz.Rect(
                max(0.0, bbox.x0 - 4),
                max(bound_top, bbox.y0 - 4),
                min(page_w, bbox.x1 + 4),
                min(bound_bot, bbox.y1 + 4),
            )

    return None


def _same_caption_column(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
    page_w: float,
    col_cnt: int,
) -> bool:
    """Two captions are 'in the same column' if both centers are on the same
    side of the page midline, OR if either is full-width / page-mid centered."""
    if col_cnt == 1:
        return True

    def _full(bb):
        cx = (bb[0] + bb[2]) / 2.0
        return (
            (bb[2] - bb[0]) > 0.75 * page_w or abs(cx - page_w / 2.0) < 30.0
        )

    if _full(a) or _full(b):
        return True
    return ((a[0] + a[2]) / 2.0 < page_w / 2.0) == ((b[0] + b[2]) / 2.0 < page_w / 2.0)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def extract(pdf_path: Path, out_dir: Path, dpi: int = 200) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"
    images_dir.mkdir(exist_ok=True)
    # A second extraction may find fewer figures after a heuristic change.
    # Remove only our deterministic outputs so stale fig_NN files cannot be
    # mistaken for current results; leave any hand-authored assets untouched.
    for stale in images_dir.glob("fig_*.png"):
        stale.unlink()

    doc = fitz.open(pdf_path)
    n_pages = len(doc)

    # --- Pass 1: collect raw blocks with font info ---
    pages_raw: list[list[dict]] = []
    all_block_fonts: list[tuple[dict, float]] = []
    page_widths: list[float] = []
    page_heights: list[float] = []

    for page_idx, page in enumerate(doc):
        page_widths.append(page.rect.width)
        page_heights.append(page.rect.height)
        raw = page.get_text("dict")
        page_blocks = []
        for b in raw.get("blocks", []):
            if b.get("type") == 0:  # text block
                text, avg_size, is_bold = _block_text_and_font(b)
                b["_text"] = text
                b["_avg_size"] = avg_size
                b["_is_bold"] = is_bold
                b["_page_h"] = page.rect.height
                if text:
                    all_block_fonts.append((b, avg_size))
            page_blocks.append(b)
        pages_raw.append(page_blocks)

    body_size = estimate_body_font_size(all_block_fonts)

    # --- Pass 2: detect columns (use most common width) ---
    typical_w = median(page_widths) if page_widths else 0
    col_cnt = detect_column_count(pages_raw, typical_w)

    # --- Pass 3: headers / footers ---
    headers, footers = detect_header_footer(pages_raw, n_pages)

    # --- Pass 4: build ordered blocks ---
    blocks: list[Block] = []
    figure_counter = 0
    stop_at_references = False
    references_captured = False
    # Track caption blocks that were absorbed into figure blocks (remove later).
    captions_absorbed: set[str] = set()

    for page_idx, page_blocks in enumerate(pages_raw):
        if stop_at_references:
            break
        page_w = page_widths[page_idx]
        page_h = page_heights[page_idx]

        # filter out page-chrome
        kept = []
        for b in page_blocks:
            if b.get("type") != 0:
                continue
            text = b.get("_text", "").strip()
            if not text:
                continue
            if text in headers or text in footers:
                continue
            y0, y1 = b["bbox"][1], b["bbox"][3]
            if y1 < page_h * 0.05 and len(text) < 120:
                continue
            if y0 > page_h * 0.95 and len(text) < 120:
                continue
            kept.append(b)

        # sort by reading order
        def sort_key(b):
            col = column_of(b["bbox"], page_w, col_cnt)
            if is_full_width(b["bbox"], page_w):
                col = -1  # full-width banners come first within their vertical slot
            return (col, b["bbox"][1])

        kept.sort(key=sort_key)

        page = doc[page_idx]

        # Pre-scan for caption bboxes on this page (sorted by y) to provide
        # neighbour bounds and prevent overlap with adjacent figures/tables.
        page_caption_bboxes: list[tuple[float, float, float, float]] = sorted(
            [
                tuple(b["bbox"])
                for b in kept
                if CAPTION_RE.match((b.get("_text") or "").strip())
            ],
            key=lambda bb: (bb[1], bb[0]),
        )
        # Track figure/table regions already extracted on this page so a later
        # caption (e.g. a text-only Table near a Figure) doesn't reclaim the
        # same area.
        claimed_rects_this_page: list[fitz.Rect] = []

        # build Block objects
        for b in kept:
            text = b["_text"]
            avg_size = b["_avg_size"]
            is_bold = b["_is_bold"]
            btype, level = classify_block(text, avg_size, is_bold, body_size)

            # detect "References" heading -> we stop harvesting body after this
            if btype in ("heading", "title") and REFERENCES_HEAD_RE.match(text.strip()):
                references_captured = True
                blocks.append(
                    Block(
                        id=f"b{len(blocks)+1}",
                        type="heading",
                        text=text,
                        page=page_idx + 1,
                        bbox=tuple(b["bbox"]),
                        column=column_of(b["bbox"], page_w, col_cnt),
                        level=1,
                        avg_size=avg_size,
                        is_bold=is_bold,
                    )
                )
                continue

            # if in references zone, skip reference entries entirely
            if references_captured and REF_ENTRY_RE.match(text):
                continue

            block_obj = Block(
                id=f"b{len(blocks)+1}",
                type=btype,
                text=text,
                page=page_idx + 1,
                bbox=tuple(b["bbox"]),
                column=column_of(b["bbox"], page_w, col_cnt),
                level=level,
                avg_size=avg_size,
                is_bold=is_bold,
            )
            blocks.append(block_obj)

            # if it's a caption, emit a figure block immediately AFTER
            if btype == "caption":
                m = CAPTION_RE.match(text.strip())
                label_kind = m.group(1) if m else "Figure"
                label_num = m.group(2) if m else str(figure_counter + 1)
                fig_label = f"{label_kind.rstrip('.').capitalize()} {label_num}"
                cap_kind = _caption_kind_of(text)

                # Compute neighbour-caption vertical bounds — column-aware.
                cur_bbox = tuple(b["bbox"])
                prev_y1 = 0.0
                next_y0 = page_h
                for other in page_caption_bboxes:
                    if other == cur_bbox:
                        continue
                    if not _same_caption_column(cur_bbox, other, page_w, col_cnt):
                        continue
                    if other[3] <= cur_bbox[1]:
                        prev_y1 = max(prev_y1, other[3])
                    elif other[1] >= cur_bbox[3]:
                        next_y0 = min(next_y0, other[1])

                bbox = find_figure_bbox(
                    cur_bbox,
                    cap_kind,
                    page_blocks,
                    page,
                    col_cnt,
                    body_size,
                    prev_y1,
                    next_y0,
                    claimed_rects_this_page,
                )
                if bbox is not None:
                    figure_counter += 1
                    fname = f"fig_{figure_counter:02d}.png"
                    try:
                        pix = page.get_pixmap(clip=bbox, dpi=dpi, alpha=False)
                        pix.save(str(images_dir / fname))
                        blocks.append(
                            Block(
                                id=f"fig{figure_counter}",
                                type="figure",
                                page=page_idx + 1,
                                bbox=(bbox.x0, bbox.y0, bbox.x1, bbox.y1),
                                column=column_of(
                                    (bbox.x0, bbox.y0, bbox.x1, bbox.y1), page_w, col_cnt
                                ),
                                image_path=f"images/{fname}",
                                caption=text,
                                figure_label=fig_label,
                            )
                        )
                        # caption text is now carried by the figure block itself
                        captions_absorbed.add(block_obj.id)
                        # mark the region so later captions on the same page
                        # cannot reclaim the same area
                        claimed_rects_this_page.append(fitz.Rect(bbox))
                    except Exception as exc:  # pragma: no cover
                        sys.stderr.write(f"[extract_paper] render failed on page {page_idx+1}: {exc}\n")

    # --- Pass 5: merge consecutive paragraph blocks across pages/columns ---
    # Also drop caption blocks that were already absorbed into figure blocks.
    blocks = [b for b in blocks if b.id not in captions_absorbed]
    merged: list[Block] = []
    for b in blocks:
        if (
            merged
            and b.type == "paragraph"
            and merged[-1].type == "paragraph"
            and _should_merge(merged[-1].text, b.text)
        ):
            glue = "" if merged[-1].text.endswith("-") else " "
            if merged[-1].text.endswith("-"):
                merged[-1].text = merged[-1].text[:-1] + b.text.lstrip()
            else:
                merged[-1].text = merged[-1].text.rstrip() + glue + b.text.lstrip()
        else:
            merged.append(b)

    # --- Pass 6: reposition figures to appear right after their caption reference ---
    ordered = _reorder_figures_near_references(merged)

    meta = {
        "pdf_path": str(pdf_path),
        "pdf_name": pdf_path.name,
        "pdf_stem": pdf_path.stem,
        "num_pages": n_pages,
        "columns": col_cnt,
        "body_font_size": round(body_size, 2),
        "num_figures": figure_counter,
    }

    result = {
        "meta": meta,
        "blocks": [b.to_public() for b in ordered],
    }

    # write JSON + raw markdown preview
    (out_dir / "paper.raw.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "paper.raw.md").write_text(_render_raw_markdown(result), encoding="utf-8")

    return result


def _should_merge(prev: str, nxt: str) -> bool:
    if not prev or not nxt:
        return False
    # prev ends with hyphen (word broken across lines/pages)
    if prev.endswith("-") and nxt[:1].isalpha() and nxt[:1].islower():
        return True
    # prev ends without sentence terminator AND next starts with lowercase
    terminators = ".?!\u3002\uff1f\uff01:\uff1a)]\u201d\"'"
    if prev[-1] not in terminators and nxt[:1].isalpha() and nxt[:1].islower():
        return True
    return False


def _reorder_figures_near_references(blocks: list[Block]) -> list[Block]:
    """Place each figure block right after the FIRST paragraph that references it.

    Keeps original order as fallback. A paragraph is said to reference a figure
    if it contains tokens like "Figure 1", "Fig. 1(a)", "Table 2".
    """
    figures_by_label: dict[str, Block] = {}
    remaining: list[Block] = []
    for b in blocks:
        if b.type == "figure" and b.figure_label:
            # normalize "Figure" / "Fig" / "Table" + number
            m = re.match(r"(Figure|Fig|Table|Algorithm)\s+(\d+[a-zA-Z]?)", b.figure_label, re.I)
            if m:
                key = f"{m.group(1).lower()}_{m.group(2).lower()}"
                figures_by_label[key] = b
                continue
        remaining.append(b)

    ref_re = re.compile(
        r"\b(Figure|Fig\.|Fig|Table|Algorithm|Alg\.)\s*(\d+[a-zA-Z]?)", re.IGNORECASE
    )
    inserted: set[str] = set()
    out: list[Block] = []
    for b in remaining:
        out.append(b)
        if b.type in ("paragraph", "list") and figures_by_label:
            for m in ref_re.finditer(b.text):
                kind = m.group(1).lower().rstrip(".")
                if kind == "fig":
                    kind = "figure"
                if kind == "alg":
                    kind = "algorithm"
                key = f"{kind}_{m.group(2).lower()}"
                if key in figures_by_label and key not in inserted:
                    out.append(figures_by_label[key])
                    inserted.add(key)

    # append any figures that were never referenced
    for key, fig in figures_by_label.items():
        if key not in inserted:
            out.append(fig)
    return out


def _render_raw_markdown(result: dict) -> str:
    lines: list[str] = []
    lines.append(f"# {result['meta']['pdf_stem']}")
    lines.append("")
    lines.append(
        f"> Auto-extracted preview. {result['meta']['num_pages']} pages, "
        f"{result['meta']['columns']}-column, {result['meta']['num_figures']} figures."
    )
    lines.append("")
    for b in result["blocks"]:
        t = b["type"]
        if t == "title":
            lines.append(f"# {b['text']}")
        elif t == "heading":
            level = b.get("level", 2) or 2
            lines.append("#" * (level + 1) + " " + b["text"])
        elif t == "caption":
            lines.append(f"_{b['text']}_")
        elif t == "figure":
            label = b.get("figure_label", "Figure")
            lines.append(f"![{label}]({b['image_path']})")
        elif t == "equation":
            lines.append("```")
            lines.append(b["text"])
            lines.append("```")
        elif t == "list":
            for line in b["text"].splitlines():
                lines.append(f"- {line.strip()}")
        else:
            lines.append(b["text"])
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extract structured content + figures from a PDF.")
    ap.add_argument("pdf", type=Path, help="Path to the PDF file")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: ./paper_reading/<pdf_stem>/)",
    )
    ap.add_argument("--dpi", type=int, default=200, help="Figure render DPI (default: 200)")
    args = ap.parse_args(argv)

    pdf_path: Path = args.pdf.resolve()
    if not pdf_path.exists():
        sys.stderr.write(f"[extract_paper] File not found: {pdf_path}\n")
        return 2

    if args.out is None:
        out_dir = Path.cwd() / "paper_reading" / pdf_path.stem
    else:
        out_dir = args.out.resolve()

    result = extract(pdf_path, out_dir, dpi=args.dpi)
    print(
        f"[extract_paper] OK  pages={result['meta']['num_pages']}  "
        f"columns={result['meta']['columns']}  figures={result['meta']['num_figures']}\n"
        f"[extract_paper] Output: {out_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
