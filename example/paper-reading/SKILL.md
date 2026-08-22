---
name: paper-reading
description: Deep-read a local research-paper PDF and produce a rigorous bilingual research note, an English-first minimalist paper-sharing PPT, or both. Use for 精读、论文翻译、paper summary、论文解读、方法与实验分析、论文分享、PPT、slides、paper presentation, especially for LLMs, multimodal models, agents, video/world models, and foundation models; require a readable local PDF before starting.
---

# Paper Reading

Read as a senior algorithm researcher, not as a translation engine. Reconstruct the paper's argument, preserve its epistemic force, and write Chinese that sounds native to a researcher in the field. The default note combines a fast macro view, a section-level argument map, selective microscopic close reading, and a complete semantic-chunk translation of the main body. When slides are requested, turn the same evidence model into an English-first, minimalist research presentation rather than compressing the abstract into a generic deck.

## Resolve the task

Identify the directory containing this file as `SKILL_DIR`. Require a readable local PDF; if the user gives only a URL, ask before downloading it.

Infer the mode from the request:

| Request | Mode | Deliverable |
|---|---|---|
| 精读、深度解读、完整阅读 | `deep` (default) | Macro summary + argument map + highlights + independent analysis + full main-body semantic-chunk translation + selected close-reading notes |
| 快速读懂、只看总结 | `overview` | Macro summary + argument map + strongest evidence and limitations; no claim of full translation |
| 全文翻译、逐段翻译 | `full-translation` | Complete source coverage except bibliography, grouped into semantic chunks; include appendices unless the user narrows scope |
| 精读某节、逐句推敲 | `close-read` | Requested section only, with semantic-chunk translation and dense sentence/term/notation notes |
| 翻译某节 | `translation` | Faithful semantic-chunk translation with minimal analysis |

Resolve the output form independently from reading depth:

| Request | Output |
|---|---|
| No explicit artifact request | `note` (default) |
| PPT、slides、deck、论文分享、paper presentation | `deck` |
| 精读/博客 + PPT、note and slides | `note+deck` |

For a deck-only request with no reading depth, use `overview` internally but still inspect the complete paper and build the evidence ledger before authoring slides. An explicit `deep` request still requires deep reading even when only the deck is delivered. Reuse trustworthy extraction artifacts and an existing evidence ledger when available; verify their scope instead of blindly rerunning extraction.

If the request is ambiguous, use `deep + note`. State the chosen reading mode, output form, local PDF, and output target before extraction. Never label a condensed walkthrough as a full translation.

## Resolve paths

Choose the output root in this order:

1. Current workspace containing `src/content.config.ts` and `src/content/papers/`.
2. A clearly identifiable nested or sibling JerexJs Blog workspace.
3. `<workspace>/paper_reading/` as a standalone fallback.

For a blog target, use:

- Final note: `src/content/papers/<stem>.md`
- Extraction artifacts: `src/content/papers/<stem>/paper.raw.{json,md}`
- Figures: `src/content/papers/<stem>/images/fig_NN.png`
- Final deck: `presentations/<stem>-paper-talk.pptx`

An explicit output path wins. For a standalone workspace, put the deck at `<workspace>/paper_reading/<stem>-paper-talk.pptx`. Keep temporary deck source, renders, and QA files under `<workspace>/paper_reading/decks/<stem>/`; do not put the PPTX in `public/` unless the user explicitly asks to publish it.

## Extract and reconstruct

Use the bundled scripts, not a handwritten replacement:

```bash
bash "$SKILL_DIR/scripts/setup_env.sh" "$WORKSPACE"
"$WORKSPACE/paper_reading/.venv/bin/python" \
  "$SKILL_DIR/scripts/extract_paper.py" \
  "$PDF" --out "$OUTPUT_DIR"
```

If setup fails, surface the error instead of silently switching extractors. Inspect every block in `paper.raw.json`, not only `paper.raw.md`. Repair obvious reading-order, de-hyphenation, heading, equation, caption, table, and figure-label errors without changing meaning. Check every extracted image visually.

Read the abstract, full body, limitations, and evidence-bearing appendices before writing the summary. Skip bibliography entries, but continue into appendices or supplementary material that appear after References. For long PDFs, work section by section and maintain a scratch coverage ledger; do not summarize from the first pages or rely on a single context window.

## Build an evidence model before writing

Create a scratch ledger for the paper's central claims. For each important claim record:

- exact claim and scope;
- mechanism or design choice claimed to produce it;
- strongest section/table/figure/equation anchor;
- baseline, denominator, data, compute, and evaluation protocol;
- uncertainty, missing control, and plausible alternative explanation;
- whether it is the authors' claim, a direct observation, or your inference.

Use [references/reading_framework.md](references/reading_framework.md) for macro, argument, and micro analysis. Do not draft the final judgment until the ledger covers the complete paper.

## Translate by semantic unit

For every translation mode, read [references/translation_style.md](references/translation_style.md).

The unit of translation is a coherent argumentative unit, not a PDF text box and not necessarily one sentence or one source paragraph. Usually combine 1–3 adjacent source paragraphs or roughly 120–300 English words when they share one rhetorical role. Split sooner at a heading, conceptual turn, displayed equation, algorithm, figure/table boundary, or transition from claim to evidence. Never merge unrelated claims merely to hit a target length.

For each unit:

1. Reconstruct clean source prose in original order.
2. Translate the unit as connected academic Chinese; sentence boundaries may change when Chinese logic benefits.
3. Preserve every proposition, qualifier, comparison scope, number, symbol, citation, negation, and uncertainty marker.
4. Add a compact `句读` note only for a load-bearing sentence, ambiguous term, hidden scope, notation choice, or unusually difficult construction. Do not annotate every sentence.

This is semantic-chunk translation, not sentence-by-sentence display. Full coverage and fluent Chinese are both required; neither excuses the other.

## Write at three reading resolutions

In `deep` mode, expose three distinct resolutions:

1. **宏观 | Paper-level** — the field problem, paper thesis, actual novelty, strongest evidence, practical meaning, and boundary.
2. **中观 | Argument-level** — how sections, method components, training/inference choices, and experiments form or fail to form a claim-evidence chain.
3. **微观 | Passage-level** — complete semantic-chunk translation plus selective scrutiny of decisive sentences, terms, equations, and rhetorical scope.

Use [references/writing_and_qa.md](references/writing_and_qa.md) for section ownership, researcher voice, and final checks. Use [templates/output_template.md](templates/output_template.md) for a publishable blog note, removing all comments and unused placeholders.

The default blog order is:

1. `一页读懂 | Executive Reading`
2. `论证地图 | Argument Map`
3. `关键证据 | Evidence & Tensions`
4. `研究者评注 | Researcher Commentary`
5. `原文精读 | Semantic-chunk Bilingual Reading`
6. `术语与符号 | Terms & Notation` only when it adds real value

Keep section functions separate. Summary explains the paper; the map reveals its structure; evidence notes point to anchors; commentary contributes independent synthesis; close reading supplies coverage. Do not repeat the same sentence at multiple levels.

## Create a paper-sharing deck

When the output includes `deck`, read [references/presentation_deck.md](references/presentation_deck.md), then invoke the available `Presentations` skill and follow its authoring, rendering, citation, and QA workflow completely. The presentation workflow is required: do not generate a PPTX with `python-pptx`, do not skip slide rendering, and do not treat a successful file write as visual verification.

Build the deck from the paper evidence model:

1. Define the communication job, inferred audience, talk duration, and one-sentence central takeaway. Unless the user says otherwise, assume a 15–20 minute technical sharing session for researchers familiar with the field.
2. Create a slide evidence map before layout: each slide gets one narrative job, one claim, one paper anchor, one visual role, and one transition to the next slide.
3. Use the paper's original figures, tables, equations, and qualitative examples as the primary visual evidence. Crop for the current claim and verify against the rendered PDF page; never use an unverified extraction or a full-page screenshot as a substitute for composition.
4. Make visible slide copy English-first. Keep it concise and idiomatic, preserve technical names exactly, and move presenter detail to speaker notes. Add Chinese visible text only when the user asks or a bilingual terminology gloss materially prevents ambiguity.
5. Separate author claim, observed evidence, and analyst inference. A slide title may state only what its evidence warrants; limitations and costs belong in the main story, not a perfunctory appendix.
6. Put a `[Sources]` block in speaker notes for every externally sourced claim or asset, including the local PDF page/figure/table anchors. Use outside context only when it materially helps positioning, and verify current claims from primary sources.
7. Render and inspect every slide at full size, review a montage for narrative rhythm and visual consistency, and run the presentation overflow/overlap checks. Fix every unintended warning before delivery.

The default deck is 8–14 slides, not a fixed template. Adapt length to the paper and requested duration; do not pad a simple paper or cram a complex one. Prefer a coherent claim-evidence-consequence story over reproducing the paper's section order.

## Domain-specific judgment

For LLM, multimodal, agent, video/world-model, and foundation-model papers, explicitly test the relevant axes:

- model/data/objective/inference contributions and which one actually drives the gain;
- training–inference alignment, scaling variable, compute budget, latency, and memory;
- representation, modality fusion/alignment, temporal or spatial causality, and grounding;
- benchmark validity, contamination or evaluator coupling, baseline fairness, and human-evaluation design;
- algorithmic gain versus system engineering gain;
- reproducibility under the disclosed data, compute, code, and checkpoint conditions.

Broader field positioning must distinguish paper-grounded facts from outside knowledge. If a claim depends on the current 2026 literature, verify it from primary sources when browsing is authorized; otherwise narrow the claim and state the boundary. Never invent concurrent work.

## Metadata, tags, and local PDF

Extract only metadata supported by the PDF. Omit absent optional fields. Preserve model, dataset, benchmark, metric, and algorithm names in English.

Choose 3–6 stable lowercase English tags spanning method, domain, modality, and system concern; prefer existing repository tags.

For a JerexJs Blog target, keep large PDFs out of Git:

1. Prefer a symlink `local-papers/<stem>.pdf` to the input PDF; copy only when the user explicitly wants a self-contained library.
2. Set `localPdf: "<stem>.pdf"` and keep `arxiv` as the production fallback when available.
3. Never place source PDFs under `public/` or commit them.

## Verify

Before reporting completion:

- run the coverage, translation, evidence, and prose checks in [references/writing_and_qa.md](references/writing_and_qa.md);
- verify every figure path and crop;
- verify frontmatter against `src/content.config.ts`;
- run `npm run build` for a blog target;
- when local PDF support is present, verify HEAD returns `200`, a range request returns `206`, and the article shows the local source;
- confirm no source PDF entered `public/`, `dist/`, or Git.

For a deck output, additionally confirm:

- the deck opens as an editable `.pptx` and the rendered slides match it;
- every slide has one clear job and an audience-facing takeaway title;
- English copy is fluent, figures and equations are legible, and quantitative claims retain their comparator and protocol;
- speaker-note sources are present and no placeholder, overflow, unintended overlap, or broken asset remains;
- a blog build is run only when the note/site changed or the user explicitly requested it; deck-only work uses the presentation render and QA checks instead.

Report the reading mode, output form, pages read, translated scope when applicable, figure count, and each final artifact path. For a note, include tags, build result, and local-PDF status. For a deck, include slide count, language, render/QA result, and source-note status.

Consult [reference.md](reference.md) only for the living glossary, extraction pitfalls, and update protocol. Propose reusable additions after a reading, but never mutate the installed skill's glossary without explicit approval unless the user is directly asking to improve the skill.

## Non-negotiable quality bar

- Write idiomatic, precise Chinese research prose, not translated English syntax.
- Preserve epistemic strength: “suggests” is not “proves”; correlation is not causation.
- Preserve content coverage in every output labeled full; do not silently abridge.
- Separate the authors' statements, observed evidence, and analyst inference.
- Anchor criticism to evidence or an explicitly missing control.
- In slides, prefer an evidence-bearing visual and one precise takeaway over a wall of text or decorative imagery.
- Prefer a qualified judgment over a confident invention.
- Avoid promotional prose, empty trend openings, form-filling, and decorative emoji.
