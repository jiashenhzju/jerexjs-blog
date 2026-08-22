---
title: "{{ENGLISH_TITLE}}"
titleZh: "{{CHINESE_TITLE}}"
authors: {{AUTHORS_YAML_LIST}}
affiliations: {{AFFILIATIONS_YAML_LIST}}
venue: "{{VENUE}}"
year: {{YEAR}}
arxiv: "{{ARXIV_ID_OR_URL}}"
projectPage: "{{PROJECT_PAGE_URL_OR_OMIT}}"
github: "{{GITHUB_URL_OR_OMIT}}"
huggingface: "{{HUGGINGFACE_URL_OR_OMIT}}"
localPdf: "{{LOCAL_PDF_FILENAME_OR_OMIT}}"
date: {{TODAY_YYYY_MM_DD}}
summary: "{{ONE_LINE_SUMMARY}}"
tags: {{TAGS_YAML_LIST}}
rating: {{RATING_0_TO_5_OR_OMIT}}
status: done
---

## 一页读懂 | Executive Reading

<!--
3–5 connected Chinese paragraphs. Explain the paper through:
problem and narrow thesis → decisive mechanism → strongest evidence → cost/boundary/meaning.
Do not translate the abstract, enumerate contributions, or dump metrics.
Use as many numbers as the argument needs, and explain what each number establishes.
-->

{{PROBLEM_AND_NARROW_THESIS}}

{{DECISIVE_MECHANISM_AND_WHY_IT_MATTERS}}

{{STRONGEST_EVIDENCE_WITH_COMPARISON_BASIS}}

{{COST_BOUNDARY_AND_RESEARCH_MEANING}}

---

## 论证地图 | Argument Map

<!--
Map logical links, not the table of contents. Use 4–7 rows.
The Reading column states what the evidence warrants, not what the authors advertise.
-->

| 论证环节 | 内容 | 证据 / 位置 | 阅读判断 |
|---|---|---|---|
| 问题 | {{FIELD_BOTTLENECK}} | {{ANCHOR}} | {{WHY_PRIOR_WORK_IS_INSUFFICIENT}} |
| 命题 | {{CENTRAL_THESIS}} | {{ANCHOR}} | {{WHAT_MUST_BE_ESTABLISHED}} |
| 机制 | {{LOAD_BEARING_MECHANISM}} | {{ANCHOR}} | {{HOW_IT_IS_SUPPOSED_TO_WORK}} |
| 证据 | {{STRONGEST_RESULT}} | {{ANCHOR}} | {{DIRECT_CONVERGENT_OR_SUGGESTIVE}} |
| 边界 | {{VALIDITY_BOUNDARY}} | {{ANCHOR_OR_MISSING_CONTROL}} | {{WHERE_THE_INFERENCE_STOPS}} |

---

## 关键证据 | Evidence & Tensions

<!--
Each bullet begins with § / Table / Figure / Eq. / Appendix anchor and makes one main observation.
Use 2–5 bullets where warranted; do not force both subsections to have equal length.
-->

### 值得吸收 | What Transfers

- {{ANCHOR}}：{{REUSABLE_MECHANISM_OR_CLEAN_EVIDENCE}}
- {{ANCHOR}}：{{REUSABLE_IMPLEMENTATION_DETAIL_OR_ABLATION}}

### 值得推敲 | What Remains Unsettled

- {{ANCHOR}}：{{MEASUREMENT_BASELINE_OR_MISSING_CONTROL_ISSUE}}
- {{ANCHOR}}：{{GENERALIZATION_EFFICIENCY_OR_REPRODUCIBILITY_ISSUE}}

---

## 研究者评注 | Researcher Commentary

<!--
2–4 insight-led subsections. Synthesize across the paper and, when verified, the field.
Do not expand evidence bullets or restate the summary. Distinguish paper facts from inference.
Possible angles: actual vs advertised contribution; model/data/system attribution;
field consequence; central ceiling; one decisive falsification experiment.
-->

### {{INSIGHT_LED_TITLE_1}}

{{CROSS_PAPER_SYNTHESIS_OR_COUNTERFACTUAL_ARGUMENT}}

### {{INSIGHT_LED_TITLE_2}}

{{FIELD_POSITION_OR_DECISIVE_ASSUMPTION}}

### {{INSIGHT_LED_TITLE_3_OPTIONAL}}

{{ONE_DECISIVE_NEXT_EXPERIMENT_OR_LONGER_TERM_CONSEQUENCE}}

---

## 原文精读 | Semantic-chunk Bilingual Reading

<!--
Preserve original heading order. The translation unit is a coherent argument, normally
1–3 adjacent source paragraphs or ~120–300 English words—not one sentence at a time.
Split at genuine conceptual, rhetorical, equation, algorithm, figure, or table boundaries.
Use source-range comments while auditing coverage; they may remain hidden in the article.
Add 句读 only where wording, scope, terminology, or notation is load-bearing.
-->

### Abstract

<!-- chunk: A.01 | source: p1 abstract | role: thesis -->

**Original**

{{ABSTRACT_COHERENT_SOURCE_UNIT}}

**译文**

{{ABSTRACT_CONNECTED_CHINESE_TRANSLATION}}

> **句读**：{{OPTIONAL_SCOPE_OR_WORDING_NOTE}}

### 1. Introduction

<!-- chunk: 1.01 | source: p1 ¶1–p2 ¶1 | role: problem-and-gap -->

**Original**

{{ONE_TO_THREE_RELATED_SOURCE_PARAGRAPHS}}

**译文**

{{ONE_CONNECTED_CHINESE_TRANSLATION_BLOCK}}

<!-- chunk: 1.02 | source: p2 ¶2–3 | role: thesis-and-contribution -->

**Original**

{{NEXT_COHERENT_SOURCE_UNIT}}

**译文**

{{NEXT_CONNECTED_CHINESE_TRANSLATION}}

### 2. Related Work

{{CONTINUE_IN_SEMANTIC_UNITS}}

### 3. Method

<!-- Keep displayed formulas and identifiers unchanged. Explain operational meaning in Chinese prose. -->

{{CONTINUE_IN_SEMANTIC_UNITS}}

### 4. Experiments

<!-- Keep comparison protocol, units, evaluator, and uncertainty attached to each result. -->

{{CONTINUE_IN_SEMANTIC_UNITS}}

### 5. Limitations and Conclusion

{{CONTINUE_IN_SEMANTIC_UNITS}}

<!--
Skip bibliography entries. If Appendix/Supplementary appears after References, resume translation
according to the promised mode and scope. Never stop composition merely because References appeared.
-->

*References omitted — see original PDF.*

### Appendix

{{APPENDIX_SCOPE_REQUIRED_BY_MODE}}

---

## 术语与符号 | Terms & Notation

<!-- Optional. Keep only paper-specific, ambiguous, or load-bearing entries. -->

| 原文 | 译法 / 保留形式 | 本文中的具体含义 |
|---|---|---|
| {{TERM_OR_SYMBOL}} | {{CHOSEN_RENDERING}} | {{PAPER_SPECIFIC_MEANING}} |
