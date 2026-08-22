# Paper Reading — Living Reference

This file contains only reusable vocabulary, extraction knowledge, and the update protocol. Core reading, translation, and writing rules live in `references/` and should not drift during an ordinary paper reading.

## 1. Update protocol

During a reading, keep a scratch list of:

- recurring field terms whose established Chinese rendering is genuinely ambiguous;
- extraction failures not covered below;
- paper-specific conventions that should remain local to that paper.

At the end:

1. Propose only reusable glossary or extractor additions. Do not add obvious translations or one-paper coinages.
2. Mark uncertain proposals explicitly and explain the trade-off.
3. Wait for user approval before changing this file.
4. Keep paper-specific choices in the article's `术语与符号` section, not in this global glossary.
5. Add one concise changelog entry only when a reusable update is actually merged.

A glossary candidate should be frequent in LLM, multimodal, agent, vision, RL, or world-model research; have a stable community rendering or a stable convention to retain English; and materially prevent mistranslation. When no rendering is dominant, prefer retaining English.

## 2. Preferred Chinese renderings

Paper context overrides this table when authors explicitly redefine a term. Annotate English only at the first important occurrence and only when it helps disambiguation.

### Foundation models and post-training

| English | Preferred Chinese | First occurrence |
|---|---|---|
| alignment | 对齐 | 可括注 `alignment` |
| chain-of-thought | 思维链 | `思维链（CoT）` |
| direct preference optimization | 直接偏好优化 | `直接偏好优化（DPO）` |
| emergent ability | 涌现能力 | 可不注 |
| group relative policy optimization | 保留 `GRPO` | 首次解释全称 |
| in-context learning | 上下文学习 | `上下文学习（ICL）` |
| inference-time compute | 推理时算力 | 可括注 |
| instruction tuning | 指令微调 | 可不注 |
| mixture-of-experts | 专家混合 | `专家混合（MoE）` |
| reinforcement learning from human feedback | 基于人类反馈的强化学习 | `…（RLHF）` |
| retrieval-augmented generation | 检索增强生成 | `…（RAG）` |
| scaling law | 扩展律 | 可括注 `scaling law` |
| supervised fine-tuning | 监督微调 | `监督微调（SFT）` |
| test-time scaling | 测试时扩展 | 可括注 |

### Multimodal, vision, and generation

| English | Preferred Chinese | First occurrence |
|---|---|---|
| classifier-free guidance | 无分类器引导 | `…（CFG）` |
| diffusion model | 扩散模型 | 可不注 |
| grounding | 按语境用“定位 / 语义落地”；必要时保留 English | 建议括注 |
| image-text alignment | 图文对齐 | 可不注 |
| latent space | 潜空间 | 可不注 |
| multimodal large language model | 多模态大模型 | `…（MLLM）` |
| noise schedule | 噪声调度 | 可不注 |
| vision-language model | 视觉-语言模型 | `…（VLM）` |
| world model | 世界模型 | 首次可括注 |

### Agents, search, and systems

| English | Preferred Chinese | First occurrence |
|---|---|---|
| agent / agentic | 智能体 / 智能体式 | 首次可括注 |
| function calling | 函数调用 | 可不注 |
| Monte Carlo Tree Search | 蒙特卡洛树搜索 | `…（MCTS）` |
| rollout | 通常保留 `rollout`；解释其具体含义 | 视语境 |
| sim-to-real gap | 通常保留 `sim-to-real gap` | 首次解释 |
| tool use | 工具使用 / 工具调用 | 可不注 |
| UCT | 保留 `UCT` | 首次解释 |

### Architecture and notation

Keep model, dataset, benchmark, metric, library, and standard component names in English where that is the community norm: `Transformer`, `Softmax`, `LayerNorm`, `RMSNorm`, `RoPE`, `KV cache`, `LoRA`, `PyTorch`, `JAX`. Keep tensor shapes and formula identifiers unchanged.

Use natural Chinese for stable generic concepts: 自注意力、交叉注意力、多头注意力、前馈网络、词表、预训练、微调、交叉熵损失、消融实验、零样本、少样本. Do not add English parentheses mechanically.

## 3. Figure and table conventions

- Figures are page-region PNGs so vector and composite figures survive.
- Final path: `./<pdf_stem>/images/fig_NN.png`.
- Place a figure near its first substantive discussion.
- Preserve numbering and translate the complete caption.
- Keep complex tables as rendered images unless the user requests a Markdown reconstruction.
- If a crop is missing, leave `<!-- figure missing; see original PDF page N -->` and continue rather than inventing content.

Recommended shape:

```markdown
**Figure 3.** <English caption>

![Figure 3](./<pdf_stem>/images/fig_03.png)

**图 3.** <Chinese caption>
```

## 4. Extraction pitfalls

| Symptom | Likely cause | Repair |
|---|---|---|
| Adjacent blocks should be one paragraph | Column or page break | Merge before semantic chunking. |
| One block contains unrelated prose | PDF text boxes were concatenated | Split at the genuine rhetorical boundary. |
| Reading order is wrong | Multi-column layout heuristic failed | Reorder against page coordinates and visual PDF. |
| Heading level is wrong | Display-font heuristic failed | Correct hierarchy manually. |
| Caption exists but no image | Crop detection failed or figure is vector-only | Inspect the page; hand-crop the exact region when it matters. |
| Figure appears twice | Caption and first textual reference both inserted it | Keep one placement near the first substantive discussion. |
| Figure-internal labels leak into prose | Figure overlaps text blocks | Drop fragments with high emoji density, many ultra-short lines, or strong caption overlap. |
| Unpunctuated `Figure 1 Overview` is missed | Caption regex expects punctuation | Accept when the label is followed by an uppercase caption phrase, not prose such as `Figure 2a reports`. |
| Table crop includes body text | Crop heuristic crossed the table boundary | Stop at the next full-width body-sized, low-numeric-density block. |
| Old `fig_NN.png` remains after rerun | Output directory was reused | Remove only deterministic extractor-owned `fig_*.png` before extraction. |
| Appendix disappears after References | Composition stopped at bibliography heading | Skip bibliography entries, then resume at Appendix/Supplementary headings. |
| Words contain line-break hyphens | PDF layout hyphenation | Join only when the dictionary/visual line break supports it; retain true compounds. |

## 5. Do not do these things

- Do not invent metadata, citations, numbers, equations, or paper names.
- Do not treat extracted block boundaries as semantic boundaries.
- Do not silently omit content from an output called “full”.
- Do not translate bibliography entries unless explicitly requested.
- Do not let a global glossary override a paper's explicit definition.
- Do not place large source PDFs in `public/`, `dist/`, or version control.

## 6. Changelog

Newest first. Keep entries short and record only skill-level changes or user-approved reusable additions.

- 2026-08-20 — Deep rewrite: semantic-chunk translation; macro/argument/micro reading; evidence ledger; calibrated academic Chinese; selective close reading; appendix-aware coverage; explicit QA gates.
- 2026-08-20 — MiniWorld: added punctuation-free caption handling, numeric-table crop guards, stale-figure cleanup, and local range-served PDF workflow.
- 2026-05-05 — Added GRPO preference and vector-composite figure recovery notes.
- 2026-04-26 — Added MCTS, UCT, rollout, sim-to-real gap, and UGC terminology guidance; documented figure-internal text leakage.
