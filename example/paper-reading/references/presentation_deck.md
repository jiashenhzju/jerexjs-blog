# Minimal Research Paper Presentation

Use this guide only when the requested output includes a slide deck. It defines the paper-specific editorial and visual decisions; the available `Presentations` skill remains authoritative for PPTX authoring, runtime setup, speaker-note citations, rendering, and programmatic QA.

## 1. Communication contract

Before outlining, write one private sentence:

> By the end, **[audience]** should understand **[what this paper changes and how strongly the evidence supports it]** because **[central claim + decisive evidence]**.

Default assumptions when the user gives no presentation context:

- audience: researchers and technically fluent engineers in the adjacent field;
- setting: an internal paper-sharing session, not a conference pitch;
- duration: 15–20 minutes plus discussion;
- visible language: English-first;
- presenter notes: concise English, optionally bilingual when it improves delivery;
- deck length: normally 8–14 slides, plus only necessary appendix slides.

Do not ask for these details unless a different choice would materially change the deck. Infer them from the paper and the user's context, then state the assumption.

## 2. Build a slide evidence map

Create a scratch table before writing slide code:

| Slide | Narrative job | Takeaway title | Evidence anchor | Visual | Transition |
|---|---|---|---|---|---|
| 1 | Frame the paper | … | title / abstract | minimal title composition | Why does this matter? |

Every slide must have exactly one primary narrative job and one main claim. Its evidence anchor should point to the paper's page, section, figure, table, equation, or appendix. If no evidence supports the proposed title, weaken the title or remove the slide.

Use takeaway titles that a researcher could say aloud:

- Strong: `Long-horizon drift begins with a train–test history mismatch`
- Weak: `Motivation`
- Strong: `State redistribution moves memory outside the fixed video window`
- Weak: `Our Architecture`

The title states the conclusion; the body shows why it is warranted.

## 3. Default narrative arc

Treat this as a reasoning sequence, not a rigid template. Merge or split beats according to the paper.

1. **Paper and thesis** — title, authors/venue, and one plain-English sentence stating the paper's intellectual claim.
2. **Problem pressure** — the concrete failure mode or bottleneck; show why prior practice is insufficient.
3. **Core insight** — the smallest conceptual move that differentiates the work. Contrast old and new assumptions when useful.
4. **Method at a glance** — one system-level view anchored by the strongest original overview figure or a restrained native diagram.
5. **Load-bearing mechanism I** — explain the first component necessary for the thesis, not every module.
6. **Load-bearing mechanism II** — explain the second only if it carries distinct causal or operational weight.
7. **How the claim is tested** — task, data, baselines, budget, metric/evaluator, and the control that matters most.
8. **Decisive result** — the result that most directly bears on the thesis, with comparator and protocol visible.
9. **Why the gain happens** — ablation, scaling behavior, or qualitative evidence; label causal strength accurately.
10. **Cost and boundary** — compute, data, latency, memory, assumptions, missing controls, and untested regimes.
11. **What we should believe** — separate established findings, suggestive findings, and open questions.
12. **Takeaways and discussion** — 2–3 durable lessons plus 1–2 specific research questions; do not end on a generic `Thank you` slide.

For method-heavy papers, spend more slides on mechanism and fewer on broad context. For benchmark or empirical papers, spend more on protocol validity, baselines, uncertainty, and slice behavior. For theoretical papers, replace system slides with definitions, intuition, theorem dependencies, and the empirical or conceptual consequence.

## 4. Content discipline

### Visible copy

- Default to concise, idiomatic English. Preserve model, dataset, benchmark, metric, and algorithm names exactly.
- Use one short setup statement plus at most 2–4 evidence points when prose is necessary. If the slide needs paragraphs, the composition or story is wrong.
- State quantitative results with the comparator, metric direction, and protocol. `+4.2` is meaningless without what changed, against what, and under which budget.
- Do not paste abstract sentences or contribution lists. Rewrite for oral explanation without strengthening the claim.
- Avoid repeated labels such as `Problem`, `Method`, and `Results` when a takeaway title can carry the meaning.

### Speaker notes

Use notes for the explanation that should be spoken rather than displayed:

- the slide's one-sentence speaking intent;
- 2–4 compact talk-track points where useful;
- caveats, transitions, and optional detail;
- a `[Sources]` block required by the `Presentations` skill.

For the local paper, cite enough precision to re-find the evidence, for example:

```text
[Sources]
- /absolute/path/Paper.pdf, p. 5, Fig. 3, accessed 2026-08-20
- /absolute/path/Paper.pdf, p. 8, Table 2, accessed 2026-08-20
[/Sources]
```

Do not expose production notes, layout instructions, or internal confidence labels on the canvas.

## 5. Visual system: minimalist researcher

The deck should feel like a careful lab talk: quiet, precise, and editorial. It should not resemble a startup pitch, a UI dashboard, or a generic academic template.

### Canvas and color

- Use 16:9 widescreen.
- Default background: warm off-white (`#F5F2EA` or a close accessible equivalent).
- Default text: near-black (`#171717`), not pure black when the background is warm.
- Use one restrained accent, preferably deep research blue (`#315EFB`) or muted teal. Reserve it for the current mechanism, comparison, or conclusion.
- Use light neutral rules and fills only when they clarify grouping. No gradients, glass effects, heavy shadows, or decorative texture.

### Typography

- Use a restrained sans-serif family available in the authoring environment for body copy; use one compatible serif face only for the deck title or rare editorial emphasis.
- Follow the `Presentations` skill's minimum sizes. As a working target: 50–60 pt title slide, 35–42 pt slide titles, 20–28 pt body/callouts, and 12–14 pt source/footer text.
- Use sentence case. Avoid all-caps headings except tiny navigation labels.
- Never shrink type to rescue an overloaded slide; cut, split, or move detail to notes.

### Composition

- Use a consistent left edge, generous margins, and deliberate whitespace.
- Prefer one dominant composition per slide: figure + takeaway, diagram + mechanism, or result + interpretation.
- Vary silhouettes across the deck while preserving the same grid, type, color, line weight, footer, and slide-number system.
- Avoid card grids, pills, badges, fake windows, button-like elements, icon clouds, and dense two-column bullet layouts.
- Use a subtle running marker only when it helps orientation; do not turn the deck into a navigation UI.

### Figures, tables, equations, and diagrams

- Treat original paper figures as primary evidence. Crop to the relevant panel while retaining labels needed to interpret it; include the figure number in notes or a quiet caption.
- Verify every crop against a rendered PDF page. Never trust extraction order or caption association without visual inspection.
- Do not place a full PDF page on a slide. Recompose the figure, equation, caption takeaway, and source into a legible layout.
- For tables, foreground the 1–3 rows or metrics that support the claim. Preserve the original values and comparison direction; place the complete table in the appendix only if discussion needs it.
- For equations, show only the notation needed for the current mechanism. Pair the equation with plain-English operational meaning.
- Use native shapes only for a simple, truthful causal or data-flow diagram. Do not recreate a complex architecture when the original figure communicates it better.
- Avoid decorative AI-generated imagery by default. It competes with technical evidence and weakens the researcher aesthetic.

## 6. Evidence and epistemic language

Keep these three layers distinct:

- **Author claim** — what the paper says;
- **Observed evidence** — what the reported experiment or derivation directly shows;
- **Analyst inference** — what follows only after interpretation or outside context.

Use calibrated titles and callouts: `supports`, `is consistent with`, `suggests`, `does not isolate`, and `remains untested` are often more accurate than `proves` or `solves`. Do not let visual prominence strengthen a result beyond its design.

Include resource costs and limitations in the main narrative when they change the interpretation. A strong paper talk explains both why the work matters and where the inference stops.

## 7. Appendix policy

Appendix slides are optional and should answer predictable technical questions, not warehouse unused content. Good candidates include:

- complete benchmark tables or additional slices;
- training recipe and compute details;
- notation and derivation detail;
- extra ablations or failure cases;
- exact prompts, evaluator rubric, or data composition when central to validity.

Give each appendix slide a specific question-style title. Keep the same visual system and source discipline as the main deck.

## 8. Render and QA gates

Follow the `Presentations` skill's exact render and lint procedure, then add these paper-specific checks.

### Narrative gate

- the opening creates a concrete technical question and the close resolves it;
- slide order follows a claim-evidence-consequence chain rather than the paper's table of contents;
- each slide advances the story and has one takeaway title;
- the decisive result receives more visual weight than peripheral detail.

### Research gate

- central claims, figures, equations, and numbers match the paper;
- comparator, budget, metric, and evaluator are attached to each important result;
- author claim, observation, and inference are distinguishable;
- costs, missing controls, and validity boundaries are visible;
- current field-positioning claims are either verified from primary sources or deliberately narrowed.

### Visual gate

- inspect every rendered slide individually at full size;
- inspect a montage for pacing, alignment, repeated silhouettes, and abrupt density changes;
- no title wraps unexpectedly, no body text falls below the minimum, and every figure label is readable;
- no placeholder, clipping, overflow, unintended overlap, broken image, or orphaned caption remains;
- citations and slide numbers are present but visually quiet.

### Delivery gate

- the `.pptx` opens and remains editable;
- rendered previews correspond to the final file;
- every slide with external claims or assets has a valid `[Sources]` block in notes;
- report final deck path, slide count, visible language, source-note status, and render/QA result.
