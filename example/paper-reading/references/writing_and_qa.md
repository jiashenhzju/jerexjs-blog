# Writing Contract and Quality Assurance

This guide defines what each section owns and how to judge the finished note. Length guidance is elastic: complexity determines length, not a form.

## 1. Section ownership

### 一页读懂 | Executive Reading

Write 3–5 connected Chinese paragraphs, usually 450–800 Chinese characters for a substantial paper. Cover:

- the problem and the paper's narrow thesis;
- the decisive mechanism or design choice;
- the strongest evidence and its comparison basis;
- the cost, validity boundary, and practical meaning.

This is a researcher's explanation, not an abstract translation or contribution list. Use only numbers that carry the argument. Do not impose an arbitrary “one number per paragraph” rule, but prevent stat dumps by explaining what each included number establishes.

### 论证地图 | Argument Map

Expose the paper's logic at section level. A compact table usually works:

| Link | Content | Evidence / location | Reading |
|---|---|---|---|
| Problem | … | §1 | Why prior approaches are insufficient |
| Thesis | … | Abstract / §1 | The claim the paper must establish |
| Mechanism | … | §3 / Eq. N | How the design is supposed to work |
| Evidence | … | Table/Figure N | What is directly supported |
| Boundary | … | §Limitations / missing control | Where the inference stops |

Use 4–7 rows. Do not turn it into a table of contents.

### 关键证据 | Evidence & Tensions

Use two subsections when both are warranted:

- `值得吸收 | What Transfers`: reusable mechanisms, clean ablations, implementation details, or under-emphasized evidence.
- `值得推敲 | What Remains Unsettled`: measurement validity, baseline fairness, missing controls, confounds, efficiency, or generalization.

Each bullet starts with an anchor such as `§3.2`, `Table 4`, `Figure 2`, `Eq. (7)`, or `Appendix B`. One bullet carries one main observation and explains why it matters. Usually 2–5 bullets per subsection; do not force symmetry.

### 研究者评注 | Researcher Commentary

Write 2–4 insight-led subsections. Each should make an argument that emerges after reading across the paper, such as:

- claimed novelty versus actual reusable contribution;
- algorithm/data/system attribution;
- what the work changes in the research landscape;
- the central assumption or ceiling of the approach;
- one decisive next experiment.

This section may be longer than the old 450-character limit when the reasoning warrants it, but each subsection should still have one center of gravity. If a paragraph merely expands one evidence bullet, it belongs above.

### 原文精读 | Semantic-chunk Bilingual Reading

Preserve the paper's heading hierarchy. Under each heading, present source and Chinese in coherent semantic units. A unit may have a short descriptive label only when it helps navigation; never invent labels that distort the authors' structure.

Recommended shape:

```markdown
<!-- chunk: 3.02 | source: p5 ¶2–p6 ¶1 | role: mechanism -->

**Original**

<one coherent English unit>

**译文**

<one coherent Chinese unit, possibly split into 1–2 paragraphs for readability>

> **句读**：<optional, only when the passage warrants microscopic analysis>
```

The HTML comment is optional in the final article but useful while tracking full coverage. Consecutive one-sentence Original/译文 pairs are a failure unless the source genuinely consists of isolated definitions or equations.

### 术语与符号 | Terms & Notation

Include only paper-specific, ambiguous, or load-bearing terms and symbols. This is not a generic ML glossary. Prefer a compact table with source term, chosen rendering, and paper-specific meaning.

## 2. Researcher voice

- Lead with the paper's intellectual object, not “近年来” or a ceremonial “本文提出”. These phrases are allowed when they are genuinely the clearest wording; do not use a mechanical ban that creates strained prose.
- Explain why a design matters, not only what components exist.
- Keep names and jargon only where they carry field meaning. Translate ordinary connectors and concepts into natural Chinese.
- Use calibrated verbs: “支持、提示、与……一致、尚不足以区分、在该设置下成立”.
- Prefer direct but bounded judgments. “这一实验未隔离数据增益与目标函数增益” is better than “实验不充分”.
- Avoid promotional adjectives, vague praise, empty future-work endings, and form-filling transitions.

## 3. Avoid repetition across resolutions

The same evidence may appear at two resolutions only when its function changes:

- Summary: what the evidence means for the central claim.
- Argument map: where it sits in the claim chain.
- Evidence bullet: the exact anchored observation.
- Commentary: a cross-paper or counterfactual interpretation.
- Close reading: source coverage and wording.

Copying or lightly paraphrasing the same sentence across three sections is a failure. Delete the weakest occurrence.

## 4. Full-coverage ledger

For `deep` and `full-translation` modes, track every source block from abstract through conclusion, plus the promised appendix scope. Mark each as:

- translated in chunk `<id>`;
- excluded as bibliography;
- excluded as figure-internal text or duplicate caption;
- repaired and merged with neighboring blocks;
- intentionally omitted, with the reason visible to the user.

Before completion, there must be no unclassified source block. A polished subset is not a full translation.

## 5. Quality gates

### Coverage gate

- promised scope and actual scope match;
- all source blocks have a disposition;
- appendices after References were not accidentally skipped;
- headings, equations, figures, tables, and citations retain correct order and numbering.

### Translation gate

- every proposition, qualifier, negation, comparison, number, unit, and symbol is preserved;
- no English-syntax residue makes the Chinese hard to parse;
- terminology is stable and English annotations are purposeful;
- sentence boundaries serve Chinese logic;
- the translation can be read fluently without consulting the source.

### Evidence gate

- central claims have concrete anchors;
- the strongest result is compared under a fair or explicitly qualified protocol;
- author claim, observed fact, and analyst inference are distinguishable;
- causal language does not exceed the experiment;
- limitations include missing controls and resource costs, not only the authors' own section.

### Analysis gate

- macro summary is accurate after the full read;
- argument map captures logic rather than section order;
- commentary contains genuine synthesis and at least one falsifiable implication when appropriate;
- recent field-positioning claims are verified or carefully bounded;
- no invented paper, number, date, author, or result appears.

### Prose gate

- no stat-dump paragraph, contribution-list paraphrase, or dense bilingual noun chain;
- no arbitrary rule has made the Chinese stilted;
- paragraphs have a clear center and natural transitions;
- criticism is specific and proportionate;
- decorative emoji and marketing language are absent.

### Artifact gate

- frontmatter validates;
- every image exists and has the intended crop;
- local PDFs remain outside committed/public build artifacts;
- repository build and local PDF range serving pass when applicable.

## 6. Final read-through order

Review in this order because later checks depend on earlier ones:

1. coverage ledger against extracted source;
2. translation against source;
3. evidence ledger against summary and critique;
4. duplication across sections;
5. Chinese-only read for fluency;
6. rendered artifact for visual hierarchy and broken assets.

If a gate fails, fix the note before reporting completion. Do not hide uncertainty behind confident prose.
