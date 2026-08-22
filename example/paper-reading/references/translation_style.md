# Translation and Close-reading Style

The target is faithful Chinese research prose: complete in meaning, natural in syntax, stable in terminology, and exact about evidence. Literal surface correspondence is not the goal; proposition-level fidelity is.

## 1. Segment by semantic unit

### Default unit

Group adjacent source material when it performs one rhetorical job, commonly:

- posing a problem and explaining why it matters;
- contrasting prior work with the paper's choice;
- defining one mechanism and its consequence;
- presenting one experiment and interpreting it;
- stating one limitation or implication.

A typical unit is 1–3 source paragraphs or about 120–300 English words. This is a heuristic, not a quota.

### Start a new unit when

- the heading or subsection changes;
- the topic, actor, time scale, or logical role changes;
- prose moves from claim to evidence, method to experiment, or result to limitation;
- a displayed equation, algorithm, figure, or table needs its own explanatory context;
- combining more text would force the Chinese translation to carry two unrelated centers of gravity.

### Do not let PDF layout decide

Merge false splits caused by columns, page breaks, hyphenation, captions, or text boxes. Conversely, split a single extracted block when it contains two genuine rhetorical units. Preserve original order and record source ranges in a scratch ledger so no content disappears.

## 2. Translate propositions, then rebuild Chinese syntax

For each unit:

1. Identify subject, action, object, conditions, comparison, causal relation, and degree of certainty.
2. Resolve pronouns and references before translating.
3. Decide stable renderings for paper-specific terms and symbols.
4. Draft connected Chinese around the argument, not around English punctuation.
5. Compare the translation back against the source proposition by proposition.

Chinese sentence boundaries may differ from English. Split an overloaded English sentence when its logic becomes clearer; merge short adjacent English sentences when Chinese cohesion benefits. Do not add a conclusion, causal claim, or emphasis that the source does not contain.

## 3. Research Chinese that reads naturally

- Put the topic and governing claim early. Avoid carrying a long English premodifier into the end of a Chinese sentence.
- Restore an omitted or passive subject when Chinese would otherwise be ambiguous, but do not invent agency.
- Translate logical relations explicitly when needed: contrast, concession, condition, cause, result, and scope should be easy to follow.
- Prefer concrete research verbs: “刻画、约束、估计、消融、归因、支持、表明、提示、依赖、退化”. Avoid generic “进行、实现、做了”.
- Vary repeated “本文提出/我们提出” when the discourse permits, but retain authorial first person where it matters.
- Avoid translationese such as “被展示为”“有能力去”“在……的设置之下” when “结果表明”“能够”“在……设置中” is cleaner.
- Do not force every English noun into a Chinese noun phrase. Convert nominalizations back into actions when that improves clarity.
- Use punctuation as Chinese prose requires. A semicolon should connect genuinely parallel or contrastive clauses, not hide an overfull sentence.

The analysis sections use the researcher's voice. The translated body preserves the paper's voice. Do not blur “作者认为” and “我判断”.

## 4. Preserve epistemic force

| Source force | Safe Chinese tendency | Do not inflate to |
|---|---|---|
| may / might | 可能 / 或可 | 必然 / 证明 |
| can | 能够 / 可 | 总能 / 必然会 |
| suggests / indicates | 提示 / 表明 | 证明 |
| demonstrates empirically | 实验表明 / 结果显示 | 理论上证明 |
| is consistent with | 与……一致 / 不矛盾 | 证实 |
| outperforms on X | 在 X 上优于 | 整体优于 / 更强 |
| we hypothesize / conjecture | 我们假设 / 推测 | 我们发现 |
| approximately / up to | 约 / 最高达到 | 达到（无范围） |

Preserve negation, exceptions, comparison denominators, uncertainty intervals, averages versus maxima, and whether a result is measured or inferred.

## 5. Terminology

### Keep unchanged

- model, dataset, benchmark, metric, framework, and library names;
- standard abbreviations and algorithm names where Chinese expansion would be less recognizable;
- tensor shapes, variables, equations, code, and pseudocode identifiers.

### Translate with restraint

- Use an established Chinese rendering when one is stable.
- At first important occurrence, write `中文（English / abbreviation）` only when it disambiguates or defines the paper's usage.
- Keep later occurrences consistent; do not alternate synonyms for stylistic variety.
- If no stable rendering exists, retain English and explain it once rather than coining a term.
- Avoid dense Chinese–English switching. Translate ordinary technical concepts; preserve proper names and genuinely field-native notation.

Before drafting, make a small paper-local terminology sheet with: source term, chosen Chinese, first-occurrence form, and context-specific caveat. Consult [../reference.md](../reference.md) for reusable preferences, but paper context wins when a term is explicitly redefined.

## 6. Equations, algorithms, figures, and tables

- Keep identifiers and mathematical notation unchanged.
- Translate prose surrounding an equation; explain the equation's operational meaning separately when useful.
- Preserve pseudocode in English unless the user asks for a translated algorithm. A short Chinese gloss may follow.
- Translate figure/table captions as complete semantic units.
- Place an extracted image near its first substantive discussion, while preserving the paper's numbering.
- Do not OCR a complex table into Markdown by default; quote only the rows needed for analysis and retain the rendered table image.
- State units, directions, normalization, and whether higher/lower is better when the paper makes them clear.

## 7. Selective microscopic notes

Use a `句读` note when one of these is true:

- a phrase controls the scope or strength of the central claim;
- a term has competing translations or a paper-specific definition;
- a long construction hides a contrast, condition, or causal leap;
- a formula's notation encodes a key assumption;
- a sentence is easy to over-interpret in Chinese.

Do not use `句读` merely because a sentence is long. The note should help a researcher reason, not display the translator's effort.

## 8. Worked example: chunk, not sentence pairs

Synthetic source:

> Existing systems reduce memory by discarding old states, but this often weakens long-range consistency. We instead retain a compressed anchor state and update only a bounded active window. This design does not guarantee exact recovery of the full history; rather, it preserves the information that the model repeatedly uses during streaming inference. Across three evaluation horizons, the method matches the full-context baseline while using less peak memory.

Good chunk translation:

> 现有系统通常通过丢弃旧状态来压低内存开销，但这样做往往会削弱长程一致性。我们保留一个压缩后的锚点状态，只更新大小受限的活动窗口。该设计并不保证精确恢复全部历史，而是尽量保存模型在流式推理中反复调用的信息。实验覆盖三个时间跨度：与完整上下文基线相比，该方法在降低峰值内存的同时保持了相当的性能。

Why this works:

- Four English sentences form one mechanism-and-evidence unit and are displayed together.
- “does not guarantee” remains an explicit boundary.
- The last sentence preserves the comparison and resource trade-off without implying superiority.
- Chinese sentence structure is rebuilt; it is not aligned line by line.

Possible close-reading note:

> **句读**：`does not guarantee exact recovery` 排除了“压缩状态等价于完整历史”的强解释。这里应译为“并不保证精确恢复”，不能弱化成“未必需要恢复”。

## 9. Back-check after every section

Compare source and translation for:

- all propositions present and none added;
- entities, numbers, units, citations, equations, and references correct;
- modality and causal strength preserved;
- pronouns and comparison scopes resolved;
- terminology consistent;
- Chinese reads smoothly without seeing the English;
- chunk boundaries follow reasoning rather than typography.

If fidelity and fluency conflict, first restate the exact proposition in plain language, then write the cleanest Chinese sentence that preserves it. Do not solve the conflict by omitting detail.
