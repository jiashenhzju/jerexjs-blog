# Research Reading Framework

Use this framework to reconstruct what a paper establishes, not merely what it says. The three reading resolutions answer different questions and must remain distinguishable in the final note.

## 1. Evidence first: the claim ledger

Before writing prose, build a scratch ledger. One row should correspond to one load-bearing claim, not one section.

| Field | Question |
|---|---|
| Claim | What exactly is asserted? Preserve population, task, regime, and comparison scope. |
| Claim type | Algorithmic, empirical, system, theoretical, interpretive, or positioning? |
| Mechanism | What causal or operational story is proposed? |
| Evidence | Which section, equation, figure, table, or appendix supports it most directly? |
| Comparator | Against what baseline, budget, data, prompt, model size, or oracle? |
| Measurement | What metric/evaluator/human protocol turns the observation into evidence? |
| Resources | What data, compute, latency, memory, labels, tools, or proprietary components are required? |
| Boundary | Where does the claim stop? What setting was not tested? |
| Alternative | What else could explain the result? Which missing control would distinguish it? |
| Status | Author claim, directly observed fact, or analyst inference? |

Do not promote a claim from “suggested” to “established” merely because it appears in the abstract. Evidence strength comes from design, comparison, and controls.

## 2. Macro reading: what kind of paper is this?

Answer these after reading the complete paper:

1. **Problem pressure** — What field-level bottleneck makes the work necessary? Is the bottleneck quality, scale, data, compute, latency, memory, controllability, evaluation, or reproducibility?
2. **Central thesis** — What is the narrowest sentence that would make the paper true if supported? Strip away contribution-list rhetoric.
3. **Actual novelty** — Is the novelty a new principle, objective, architecture, data recipe, training curriculum, inference procedure, evaluation protocol, or systems integration?
4. **Strongest evidence** — Which result carries the thesis? Prefer a fair controlled comparison over the largest headline number.
5. **Cost of the result** — What extra data, compute, modules, latency, supervision, privileged information, or engineering is consumed?
6. **Boundary of validity** — Which domains, scales, horizons, languages, modalities, or deployment regimes remain untested?
7. **Field consequence** — If the claim holds, what should a researcher do differently? If it fails, what still remains useful?

The macro summary should follow **thesis → mechanism → evidence → boundary**, but it should read as connected prose rather than four labeled answers.

## 3. Meso reading: reconstruct the argument

### 3.1 Map rhetorical roles, not section titles

A paper's section order is not necessarily its logical order. Reconstruct the chain:

`problem → insufficiency of prior approaches → proposed thesis → mechanism → implementation → evidence → scope`

For each section, ask which link it contributes. If two adjacent sections do not connect, name the missing premise. If an experiment measures an outcome but does not isolate the proposed mechanism, classify it as performance evidence, not causal evidence.

### 3.2 Decompose the method on the right axes

For foundation-model work, separate:

- **model**: architecture, parameterization, representation, routing, memory;
- **data**: source, filtering, mixture, curriculum, synthetic generation, leakage risk;
- **objective**: loss, reward, distillation target, supervision granularity;
- **optimization**: schedule, sampling, stability devices, stages;
- **inference**: decoding, search, tools, cache, test-time compute, serving constraints;
- **evaluation**: benchmark construction, evaluator, protocol, aggregation, uncertainty.

Then ask which axis changed relative to the strongest baseline. A paper that changes model, data, objective, and inference simultaneously demonstrates an integrated recipe, not necessarily the causal value of each ingredient.

### 3.3 Domain lenses

Use only the lenses relevant to the paper.

**LLMs and reasoning**

- Is improvement due to pretraining, post-training, inference-time search, verifier quality, or more sampled tokens?
- Are comparisons compute-matched and model-matched?
- Is the evaluator independent of the reward or training signal?
- Are gains robust across tasks, languages, prompt formats, and contamination-sensitive sets?

**Multimodal and vision-language models**

- Where does cross-modal information enter, and is alignment learned or inherited?
- Does the evaluation distinguish perception, grounding, reasoning, and generation?
- Are image resolution, video duration, frame sampling, and visual-token budgets controlled?
- Does a language prior mask weak visual evidence?

**Video and world models**

- What is predicted: pixels, latents, actions, states, rewards, or observations?
- How are temporal causality, long-range memory, compounding error, and action conditioning handled?
- Are open-loop visual quality and action-conditioned dynamics evaluated separately?
- Is “world model” supported by interaction/dynamics evidence or used as a broad label for video generation?

**Agents and tool use**

- Separate planner, policy, memory, tool router, executor, environment, and evaluator.
- Check whether success comes from better reasoning, extra attempts, privileged tools, or an evaluator loop.
- Compare against equal-budget sampling or Best-of-N before crediting search structure.

**Systems and efficiency**

- Distinguish algorithmic complexity from measured wall-clock behavior.
- Check hardware, batch size, precision, cache policy, compilation, and warm-up.
- Report quality–latency–memory trade-offs together; an isolated throughput number is not efficiency.

### 3.4 Grade the evidence

Use this internal scale; do not mechanically print it unless useful.

- **Direct** — the design isolates the claim with a fair control or derivation.
- **Convergent** — several imperfect measurements point the same way.
- **Suggestive** — result is compatible with the claim but alternatives remain.
- **Anecdotal** — examples or qualitative cases without a representative protocol.
- **Unsupported** — rhetoric exceeds the presented evidence.

Evaluate criticism in this order:

1. validity of the measurement;
2. fairness of the comparison;
3. identification of the proposed mechanism;
4. generalization beyond the tested regime;
5. efficiency and reproducibility.

This ordering prevents minor presentation issues from overshadowing a valid central result.

## 4. Micro reading: what does the decisive passage actually commit to?

Use microscopic notes selectively on load-bearing passages. Inspect:

- **modality**: may, can, tends to, suggests, demonstrates, proves;
- **quantifier and scope**: some/all, average/worst case, seen/unseen, tested/universal;
- **comparison class**: stronger than what, under which budget and protocol;
- **causal connective**: “because”, “therefore”, and “enables” often carry an untested mechanism;
- **definition**: whether a familiar term is being narrowed, broadened, or operationalized unusually;
- **antecedent**: what “this”, “it”, “such”, or a symbol actually refers to;
- **notation**: domains, index ranges, conditioning variables, normalization, hidden independence assumptions;
- **omission**: what a carefully worded sentence avoids claiming.

A useful close-reading note has up to four parts:

```markdown
> **句读**
> - **原句关键处**：`<short decisive phrase>`
> - **译法**：为什么采用当前中文，而不是更强或更字面的说法。
> - **逻辑**：该短语限定了主张的范围、因果强度或比较对象。
> - **研究含义**：它如何影响对方法、实验或结论的判断。
```

Omit any part that adds no information. Do not turn every paragraph into a linguistic lecture.

## 5. Independent researcher judgment

Separate three voices explicitly:

- **作者主张**: what the paper says;
- **证据所示**: what the reported design and results warrant;
- **研究者判断**: the interpretation after weighing alternatives.

Strong commentary often takes one of these forms:

- advertised novelty versus actual reusable contribution;
- mechanism claimed versus mechanism identified;
- scale effect versus recipe effect;
- benchmark gain versus capability gain;
- algorithmic gain versus systems gain;
- near-term usefulness versus long-term research consequence;
- one decisive experiment that would confirm or falsify the central interpretation.

Be opinionated only to the degree the evidence permits. A precise “现有证据不足以区分 A 与 B” is stronger than an invented verdict.

## 6. Positioning in the 2026 literature

The paper itself is the primary evidence source. When broader positioning matters:

1. distinguish stable background knowledge from time-sensitive 2026 claims;
2. verify recent comparisons from original papers, official repositories, or benchmark documentation when web access is authorized;
3. compare on the same contribution axis rather than listing nearby paper names;
4. label extrapolation as inference;
5. narrow or omit a claim that cannot be verified.

Never use “the first”, “state of the art”, “currently”, or “the field has converged” from memory alone.
