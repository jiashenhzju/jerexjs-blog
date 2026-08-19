---
title: "MOSS-VL Technical Report"
titleZh: "MOSS-VL 技术报告：面向实时交互的开放视觉—语言模型"
authors:
  - "OpenMOSS Team"
affiliations:
  - "Fudan University"
  - "Shanghai Innovation Institute"
  - "MOSI Intelligence"
venue: "Technical Report"
year: 2026
arxiv: "2608.15045"
projectPage: "https://openmoss.ai/MOSS-VL/"
github: "https://github.com/OpenMOSS/MOSS-VL"
huggingface: "https://huggingface.co/OpenMOSS-Team"
localPdf: "MOSS-VL-2608.pdf"
date: 2026-08-20
summary: "MOSS-VL 通过门控交叉注意力、显式时间编码和交互式 Realtime-SFT，把视频理解从流式输入推进到生成过程中持续感知，并给出开放模型、训练配方与实时推理实现。"
tags:
  - "vision-language-model"
  - "video-understanding"
  - "real-time-interaction"
  - "streaming-inference"
  - "multimodal-learning"
status: done
---

## 一页读懂 | Executive Reading

MOSS-VL 要解决的并不是“让 VLM 再多看一些视频帧”，而是改变视频、语言生成与时间之间的接口。多数离线模型在视频结束后统一理解；现有流式模型虽可持续接收输入，却会在生成一段回复期间停止感知。论文把能力划为 L1–L5：真正的实时交互是 L5——模型说话时仍继续看，场景一旦推翻旧证据，回复应立即修正或中断。MOSS-VL 的核心命题是：这一能力必须由架构、数据、训练目标与运行时共同构造，不能靠给离线 VLM 外接一个轮询循环解决。

架构上，11.3B 参数的 MOSS-VL 以 Qwen3-8B 初始化语言解码器，以 Qwen3-VL 初始化视觉编码器，但视觉 patch token 不进入自回归解码序列，只作为 12 层门控交叉注意力的 key/value。新帧到达时，只需编码该帧并向 cross-attention cache 追加 KV；文本解码状态无需重建。XRoPE 把文本与视觉 patch 排在共享的三轴相对坐标中，绝对时间戳 token 则显式提供真实秒数。行为侧，Realtime-SFT 将每一帧之后都变成一次“说或等”的决策，以 `<|silence|>`、`<|response|>` 和分帧展开的回复监督常驻指令、持续查询、自主择时发言与中途修正。

论文最扎实的两组证据分别支持“何时说”和“如何高效地一直看”。在四个流式 benchmark 上，MOSS-VL-Realtime 的平均分有三个第一、一个第二；最贴近主动发言的 PA、PO、FAR 三个子集均领先，例如 OmniMMI Proactive Alerting 为 66.0，对最好基线 37.5。系统侧采用同一个 Qwen3-8B 语言 backbone、同版 SGLang、单张 H200 与 BF16：匹配视觉 token 数时，随上下文增长，MOSS-VL 相对 Qwen3-VL-8B 的 TTFT 优势由 2.8× 扩大到 5.1×。这说明把视觉历史移出解码序列，确实改变了长视频下的延迟增长曲线。

但最醒目的 L5 命题仍只得到定性支持。公共 benchmark 最多覆盖 L2–L4，Figure 5 的两段 live demo 展示了条件触发与连续解说，却没有统计“回复期间证据突变后多久检测、多久修正、多少次漏改或误打断”。此外，“轻量的最后阶段”是相对于完整训练而言：Realtime-SFT 仍包含 34.8B token 和 0.56M 样本；整条六阶段课程合计恰为 1.4T token。因而最稳妥的结论是：MOSS-VL 给出了一套可信、开放、工程闭环的实时交互配方，并在流式择时和服务效率上提供了较强证据；它尚未用量化实验完成对“生成时持续感知”这一最高层能力的验收。

---

## 论证地图 | Argument Map

| 论证环节 | 内容 | 证据 / 位置 | 阅读判断 |
|---|---|---|---|
| 问题 | 流式模型在回复期间失明，无法在证据变化时修正正在生成的内容 | §1、Table 1 | L2–L5 的区分抓住了实时交互中常被“低延迟”掩盖的并发感知问题 |
| 命题 | 真正实时的 VLM 需要架构、交互数据、训练目标和运行时协同设计 | Abstract、§1、§7 | 论文证明了完整系统可运行；单个组件的独立因果贡献没有被完全隔离 |
| 架构机制 | 视觉 token 位于解码序列之外，新帧只追加 cross-attention KV；XRoPE 与时间戳分别编码逻辑顺序和墙钟时间 | §2、Figure 2–3 | 对“生成状态不因新帧到达而重算”是直接的结构性保证 |
| 行为机制 | 每帧设置决策槽位，用状态 token、类别重加权和交互式合成数据学习说、等、续说与修正 | §4.2–§4.3、Eq. (2) | 配方清楚，但 Table 6 没有 data / loss / prompt 的析因消融 |
| 性能证据 | 四个流式 benchmark 中三项平均第一，主动发言子集全部领先 | Table 6、§6.2 | 多 benchmark 结果相互印证；基线沿用各自协议与官方结果，并非严格等算力比较 |
| 系统证据 | 同语言 backbone 比较下，视觉上下文越长，TTFT 与端到端延迟优势越大 | Figure 4、§6.3 | 在给定 H200/SGLang 离线服务设置中证据直接，但不等价于端到端 L5 交互延迟 |
| 边界 | L5 只有 live demo；推理/文档能力存在短板，音频未评测 | §6.4、§7 | 核心最高层主张仍缺专门 benchmark 和统计性验证 |

---

## 关键证据 | Evidence & Tensions

### 值得吸收 | What Transfers

- §2.5：新帧只编码一次并追加 cross-attention KV，旧帧不重编码、旧 KV 不重算；这是一条比“降低视觉 token 数”更根本的在线接口设计。
- §2.3–§2.4：XRoPE 负责跨模态逻辑次序，明文时间戳负责真实时间，两者刻意解耦，避免把可变帧率误当作等间隔时间。
- §4.2：把回复拆到连续帧槽位中，使训练样本显式覆盖“正在说话时世界仍在变化”，而不是只学习离散 turn 的问答。
- §4.3 + Eq. (2)：对稀少的发言状态同时使用逆频率系数与 focal factor，直接针对“模型学会永远沉默”这一类别不平衡退化。
- §5：`cross_kv_boundary` 用每个 query 一个 32-bit 边界描述可见前缀，并在 kernel 中裁掉不可见 tile，避免构造 text × vision 的稠密 mask。
- Figure 4：同视频实验中 MOSS-VL 由于不做时间压缩，承担约 2× 视觉 token 仍未落后；这使效率结果不只是“少看帧”的产物。

### 值得推敲 | What Remains Unsettled

- §4.2–§4.3：论文把流式提升归因于 Realtime-SFT 的数据、状态 token、损失重加权、终止 token mask 和 system prompt，但只报告了终止 token mask 的单变量效应，无法区分其余因素。
- §6.1：离线基线大多直接取各官方报告，视频帧数和推理设置可能不同；因此 Table 5 更适合看能力轮廓，不宜做小数点级排序。
- §6.2：各流式模型运行各自协议。MOSS-VL 的 8.2B 语言 backbone 与 7–8B 基线相近，但其总参数为 11.3B，也没有统一视觉 token、帧率、上下文或推理预算。
- Figure 5：两个成功案例属于可读的定性证据，却不足以估计触发精度、修正延迟、错误打断率和长流稳定性。
- Figure 4：测量是离线 SGLang serving，不包含摄像头采集、视觉编码排队、逐帧 handshake 与回复中插帧的完整实时链路。
- §3–§4：论文披露了 token、样本、序列长度和峰值学习率，但没有给出训练硬件规模、总 GPU-hours、合成数据生成成本或关键数据比例，复现成本仍不完全透明。

---

## 研究者评注 | Researcher Commentary

### 真正可复用的创新是“并发接口契约”

MOSS-VL 最重要的贡献不是简单地把 Flamingo 式交叉注意力重新用于视频，也不是单独提出 XRoPE，而是让四个时间尺度形成一致契约：视觉侧以帧为单位追加状态，语言侧保持自回归序列连续，训练侧每帧给出一次发言决策，运行时则复现同样的 frame–decision 交替。许多所谓实时系统只把离线模型调用得更频繁；MOSS-VL 则把“世界继续推进”和“回复继续生成”同时写入模型状态。这一接口可以迁移到具身智能、会议助手、监控与交互式 agent，甚至未必要求沿用本文的具体 backbone。

### “最后一小步”建立在一个很大的地基上

Realtime-SFT 只占总训练 token 的 2.49%，确实支持“实时行为可集中到最后阶段安装”的工程判断；但比例小不意味着绝对成本小。其 34.8B token 已超过不少独立模型的完整训练量，前面还有 1.2624T token 预训练与 102.8B token 标准 SFT。更准确的研究问题不是“能否用少量数据让任意 VLM 变实时”，而是“一个已经具备强感知、长上下文与时间理解的 foundation，在多大的、何种结构的交互监督下会出现稳定发言策略”。论文没有用弱底座、冻结底座或不同 Realtime-SFT 规模回答这一点。

### 流式 benchmark 测到了择时，但尚未测到并发感知

PA、PO 与 FAR 的领先说明模型更会在正确时点主动开口，BT 则提示历史信息在流中仍可利用；这些证据与训练目标高度对齐。不过，模型可以在开始回复前做出正确触发，却仍在整个回复期间停止看新帧，因此 L2–L4 的成功不能自动升级为 L5。论文对此表述是克制的：量化验证止于 L2–L4，L5 只展示行为。读者也应保持同样的证据强度，不把“架构允许并发感知”写成“模型已被统计性证明能可靠修正”。

### 一个能够真正验收 L5 的实验

最关键的后续实验应在模型生成长回复期间，以可控时间注入会推翻答案的视觉事件，并比较三种系统：回复期间完全盲、周期性缓冲后重启生成、真正持续追加视觉 KV。指标至少应包括事件出现到首次语言修正的延迟、正确中断率、错误中断率、过时 token 数、视觉吞吐与端到端延迟；同时匹配语言 backbone、视觉帧预算、回复长度和硬件。若 MOSS-VL 只在“更早看到新帧”上获益，而不能以更低过时 token 数修正内容，那么论文证明的是并发输入管线；只有二者同时成立，才真正支持 L5 交互能力。

---

## 原文精读 | Semantic-chunk Bilingual Reading

### Abstract

<!-- chunk: A.01 | source: p1 abstract | role: thesis-mechanism-evidence -->

**Original**

We present MOSS-VL, an open vision–language model family that treats real-time interaction—perceiving while it speaks—as a first-class capability. It is co-designed across the stack: the language decoder attends to vision only through gated cross-attention, so the model can naturally see incoming frames while generating; a synthesized interaction corpus supervises when to speak, when to stay silent, and when to revise; and a staged curriculum concentrates all real-time-specific training in one light final stage over a strong offline foundation. Offline, MOSS-VL-Instruct is competitive at comparable scale and leads temporal-reasoning video sets. Across four streaming benchmarks, MOSS-VL-Realtime posts the best average on three (second on the fourth) among open-source streaming models, sweeping the three subsets that squarely test proactive behavior—66.0 vs. 37.5 for the best baseline on OmniMMI Proactive Alerting. With 11.3B parameters but visual tokens outside the decoded sequence, MOSS-VL widens its time-to-first-token advantage over same-backbone Qwen3-VL-8B from 2.8× to 5.1× as visual context grows. We release all five checkpoints, the training curriculum, and the real-time inference code at https://github.com/OpenMOSS/MOSS-VL.

**译文**

我们提出 MOSS-VL，一个把实时交互——即模型说话时仍持续感知——作为一等能力的开放视觉—语言模型家族。整套系统采用协同设计：语言解码器只通过门控交叉注意力访问视觉信息，因此能在生成期间自然接收新帧；合成的交互语料监督模型何时开口、何时沉默以及何时修正；分阶段课程则以强离线底座为基础，把所有实时专用训练集中到最后一个较轻的阶段。离线场景下，MOSS-VL-Instruct 在相近规模模型中具有竞争力，并在时间推理视频数据集上领先。在四个流式 benchmark 上，MOSS-VL-Realtime 相对开源流式模型取得三个平均分第一、一个第二，并包揽三个直接考查主动行为的子集；其中 OmniMMI Proactive Alerting 得分 66.0，最好基线为 37.5。模型虽有 11.3B 参数，但视觉 token 不进入解码序列；随着视觉上下文增长，相对同语言 backbone 的 Qwen3-VL-8B，首 token 延迟优势由 2.8× 扩大到 5.1×。作者发布全部五个 checkpoint、训练课程和实时推理代码。

> **句读**：`perceiving while it speaks` 是全文最严格的能力定义，不应泛化译成“支持流式视频”。后者只要求输入连续，前者要求回复生成与视觉更新并发。

### 1. Introduction

<!-- chunk: 1.01 | source: p1–p2 | role: capability-hierarchy -->

**Original**

Most open vision–language models understand video offline: given a finished clip, they read it end to end and then answer questions about it [3, 4, 14]. The settings where video understanding matters most do not wait for the clip to end. A live assistant watches a scene that is still unfolding, decides for itself when something is worth saying, and must keep watching while it says it. Table 1 organizes this capability space into five levels. L1 is the offline regime. L2–L4 form the streaming regime occupied by recent streaming models [11, 24, 41, 47]: input arrives continuously, deliberate silence and persistent queries come into play, yet the model stays blind for the duration of each reply. L5 adds the ability that separates real-time interaction from everything below: perceiving while generating, so a reply can be revised or cut short the moment the evidence changes.

**译文**

多数开放视觉—语言模型以离线方式理解视频：给定一段已经结束的视频，它们从头读到尾，再回答相关问题 [3, 4, 14]。真正需要视频理解的场景却不会等待片段结束。实时助手必须观看仍在展开的场景，自主判断何时值得开口，并在说话期间继续观察。Table 1 将这一能力空间划为五级：L1 是离线范式；近期流式模型 [11, 24, 41, 47] 所处的 L2–L4 会持续接收输入，并逐步加入主动沉默和持续查询，但每次回复期间依旧失去视觉输入；L5 才加入区分真正实时交互的能力——生成时持续感知，使模型能在证据改变的那一刻修正或中断回复。

| 等级 | 范式 | 定义性行为 | 流式输入 | 主动沉默 | 多次回复 | 生成时感知 |
|---|---|---|---:|---:|---:|---:|
| L1 | 离线 | 先看完整视频，再回答问题 | ✗ | — | ✗ | ✗ |
| L2 | 流式 | 视频持续到达，用户可随时提问；回复期间失明 | ✓ | ✗ | ✗ | ✗ |
| L3 | 流式 | 证据不足时等待，关键证据出现后再回答 | ✓ | ✓ | ✗ | ✗ |
| L4 | 流式 | 查询持续驻留，场景变化后可再次回答；单次回复期间仍失明 | ✓ | ✓ | ✓ | ✗ |
| L5 | 实时 | 回复期间继续观察，证据变化时修正或中断 | ✓ | ✓ | ✓ | ✓ |

<!-- chunk: 1.02 | source: p1–p2 | role: co-designed-solution -->

**Original**

MOSS-VL is an open vision–language model family that treats real-time interaction as a first-class capability, and it reaches that capability by co-design rather than through any single component. The architecture enables the behavior: the language decoder attends to vision only through gated cross-attention, so visual tokens never enter the decoded sequence, and an arriving frame merely appends to the cross-attention cache—the model naturally keeps perceiving while it generates (§2). XRoPE orders text and vision along one shared timeline, and absolute timestamp tokens make wall-clock time explicit. The data injects the behavior: a synthesized corpus of real-time interaction supervises when to speak, when to stay silent, and how to revise a reply the scene has overturned (§4). The training strategy keeps the stack stable: a four-stage pre-training curriculum and standard supervised fine-tuning build the offline foundation, every real-time-specific choice is concentrated in Realtime-SFT, one light final stage, and a single system prompt moves the same weights among offline, streaming, and real-time operation.

**译文**

MOSS-VL 是一个把实时交互作为一等能力的开放视觉—语言模型家族；这一能力来自系统协同设计，而非某个孤立组件。架构负责让行为成为可能：语言解码器只经由门控交叉注意力访问视觉信息，视觉 token 从不进入解码序列；新帧到达时只需追加到交叉注意力缓存，模型因而能在生成期间自然地继续感知（§2）。XRoPE 把文本与视觉排在共享时间线上，绝对时间戳 token 则显式表示墙钟时间。数据负责注入行为：合成的实时交互语料监督何时开口、何时沉默，以及场景推翻原回复时如何修正（§4）。训练策略负责稳定整个系统：四阶段预训练与标准监督微调先建立离线底座，所有实时专用选择都集中在最后一个 Realtime-SFT 阶段；同一组权重只需一个 system prompt，便可在离线、流式和实时三种模式间切换。

<!-- chunk: 1.03 | source: p2 | role: evidence-preview-and-boundary -->

**Original**

Figure 1 previews the outcome. Offline, MOSS-VL-Instruct is competitive with open models of comparable scale and leads the temporal-reasoning video sets Minerva, TOMATO, and VideoMME-Logical (§6.1). In the streaming regime, the wins land precisely where timing is being tested: across four streaming benchmarks against open-source streaming baselines, MOSS-VL-Realtime posts the best average on three of the four (and is second on the fourth), sweeping the three subsets that squarely test proactive behavior—66.0 vs. 37.5 on OmniMMI’s Proactive Alerting (§6.2). Efficiency follows from the same design: against Qwen3-VL-8B, built on the same Qwen3-8B language backbone, the time-to-first-token gap widens from 2.8× to 5.1× as visual context grows (§6.3). L5 behavior itself is demonstrated qualitatively, through live demos and the released real-time inference code (§6.4); quantitative validation covers L2–L4, where public benchmarks exist.

**译文**

Figure 1 预览了整体结果。离线场景下，MOSS-VL-Instruct 在同规模开放模型中具有竞争力，并在 Minerva、TOMATO 与 VideoMME-Logical 等时间推理视频集上领先（§6.1）。流式场景的优势则恰好集中在考查发言时机的位置：面对开源流式基线，四个 benchmark 中三个平均分第一、一个第二，三个直接测试主动行为的子集全部领先；OmniMMI Proactive Alerting 为 66.0，而最好基线为 37.5（§6.2）。同一设计也带来效率收益：与使用相同 Qwen3-8B 语言 backbone 的 Qwen3-VL-8B 相比，视觉上下文越长，首 token 延迟差距由 2.8× 扩大到 5.1×（§6.3）。L5 行为本身通过 live demo 与开放实时推理代码作定性展示（§6.4）；量化验证只覆盖已有公共 benchmark 的 L2–L4。

**Figure 1.** Results overview: streaming benchmark averages, proactive subsets, and selected offline strengths.

![Figure 1](./MOSS-VL-2608/images/fig_01.png)

**图 1.** 结果总览：四个流式 benchmark 的平均分、主动行为子集，以及若干离线优势项。绿色为 MOSS-VL，灰色为图中标注的竞争模型。

<!-- chunk: 1.04 | source: p3 contributions | role: stated-contributions -->

**Original**

In summary, our main contributions are: (1) a stack co-designed for real-time interaction—the architecture enables it, synthesized streams supervise response timing, and zero-initialized gates keep the language backbone intact; (2) Realtime-SFT, an interaction paradigm in one light stage, where two state tokens, one shared system prompt, and a reweighted next-token loss teach when to speak, when to stay silent, and when to revise using under 3% of total training tokens; (3) timing understanding that also appears offline, with MOSS-VL-Instruct leading the temporal-reasoning video sets in our comparison; and (4) measured serving efficiency: although MOSS-VL uses 11.3B parameters, visual tokens remain outside the decoded sequence, so latency grows more slowly with visual context than for its same-backbone interleaved counterpart. We release the complete training curriculum and all five checkpoints.

**译文**

作者把贡献归纳为四点。第一，整套系统围绕实时交互协同设计：架构提供并发感知的可能，合成流式数据监督回复时机，零初始化门控则保护原有语言 backbone。第二，Realtime-SFT 在一个最终阶段内，以两个状态 token、一个共享 system prompt 和重加权的 next-token loss 教会模型何时说、何时等、何时修正，所用 token 少于总训练量的 3%。第三，时间理解也体现在离线模型上，MOSS-VL-Instruct 在论文比较的时间推理视频集上领先。第四，服务效率经过实测：MOSS-VL 虽有 11.3B 参数，但视觉 token 位于解码序列之外，因此随视觉上下文增长，延迟比同语言 backbone 的交错式模型增长更慢。作者开放完整训练课程和五个 checkpoint。

### 2. Architecture

<!-- chunk: 2.01 | source: p3–p4 §2 opening–§2.1 | role: model-and-parameterization -->

**Original**

MOSS-VL pairs a native-resolution vision encoder with a language decoder initialized from Qwen3-8B [49], and the two interact only through gated cross-attention (Figure 2). Visual tokens never enter the decoded sequence: each frame contributes a few timestamp tokens and one placeholder token to the text stream, while its patch tokens are consumed as cross-attention keys and values. The vision encoder is a 27-layer transformer initialized from the Qwen3-VL vision encoder [4]; it processes images and frames at native resolution, from 4,096 to 16.8M pixels, drawing features from three intermediate layers and the final layer. The projection module merges each 2 × 2 patch group and maps it into the decoder’s hidden space. The decoder stacks 48 layers: 36 self-attention layers carried over from Qwen3-8B, and 12 gated cross-attention layers, one at every fourth position. Of the 11.3B total parameters, roughly 8.2B form the language backbone, 2.3B the cross-attention stack, and 0.8B the vision encoder and projection module.

**译文**

MOSS-VL 将原生分辨率视觉编码器与由 Qwen3-8B [49] 初始化的语言解码器配对，两者只通过门控交叉注意力交互（Figure 2）。视觉 token 从不进入解码序列：每帧只向文本流贡献少量时间戳 token 和一个占位 token，其 patch token 则作为交叉注意力的 key/value。视觉编码器是由 Qwen3-VL 视觉编码器 [4] 初始化的 27 层 Transformer，按原生分辨率处理 4,096 到 16.8M 像素的图像与视频帧，并抽取三个中间层和最后一层的特征。投影模块先合并每个 2 × 2 patch 组，再映射到解码器隐空间。解码器共 48 层，其中 36 层 self-attention 继承自 Qwen3-8B，另有 12 层门控 cross-attention，每四层插入一次。总计 11.3B 参数中，约 8.2B 属于语言 backbone、2.3B 属于 cross-attention stack、0.8B 属于视觉编码器与投影模块。

**Figure 2.** MOSS-VL architecture. Visual tokens remain on the cross-attention side; zero-initialized gates connect 12 cross-attention layers to an otherwise intact language decoder.

![Figure 2](./MOSS-VL-2608/images/fig_02.png)

**图 2.** MOSS-VL 架构。视觉 token 始终位于交叉注意力侧；12 个交叉注意力层以零初始化门控接入其余部分保持完整的语言解码器。

<!-- chunk: 2.02 | source: p4 §2.2 | role: gated-cross-attention -->

**Original**

Each cross-attention layer follows the gated design of Flamingo [2]—queries come from the text hidden states, keys and values from the visual tokens—implemented here with grouped-query attention (32 query / 8 key–value heads) and QK-RMSNorm. The layer wraps its attention and feed-forward paths in tanh gates whose scalars are zero-initialized, so training starts from an intact language backbone (§3). The 36 self-attention layers never see visual tokens.

**译文**

每个交叉注意力层沿用 Flamingo [2] 的门控设计：query 来自文本隐状态，key/value 来自视觉 token；具体实现采用 grouped-query attention（32 个 query head、8 个 key–value head）和 QK-RMSNorm。注意力路径与前馈路径外各有一个 tanh gate，其标量从零初始化，因此训练从一个未被扰动的语言 backbone 出发（§3）。其余 36 个 self-attention 层始终看不到视觉 token。

<!-- chunk: 2.03 | source: p4–p5 §2.3 | role: XRoPE -->

**Original**

To our knowledge, XRoPE (cross-attention rotary position embedding) is the first position encoding introduced for the cross-attention channel of a vision–language architecture: it gives the visual stream position information that this channel otherwise lacks. XRoPE places text tokens and visual patches in one three-axis coordinate space $(t,h,w)$, ordered by their logical position in the stream (Figure 3). A text token advances all three axes together, taking coordinate $(x,x,x)$. A frame whose merged patch grid is $h'\times w'$ anchors at the coordinate $t$ following the preceding text, and its patches use

$$
p_{a,b}=(t,t+a,t+b),\quad 0\le a<h',\;0\le b<w'.
\tag{1}
$$

The separator token that closes the frame on the vision side and the frame’s placeholder token in the text stream receive the same coordinate, so both channels advance along a single timeline. The 64 rotary frequency pairs are split $(24,20,20)$ across $(t,h,w)$, and rotations are applied to text-side queries and vision-side keys before they meet in cross-attention. The $t$ axis is a relative sequence coordinate, not wall-clock time; real timing enters through the timestamp tokens of §2.4.

**译文**

作者称，XRoPE（cross-attention rotary position embedding）是首个专为视觉—语言架构的交叉注意力通道引入的位置编码，用于补上该通道原本缺失的视觉流位置信息。XRoPE 按流中的逻辑顺序，把文本 token 与视觉 patch 放入共享的三轴坐标空间 $(t,h,w)$（Figure 3）。文本 token 会同步推进三个轴，坐标为 $(x,x,x)$。对于合并后 patch 网格为 $h'\times w'$ 的一帧，它以紧随前文的坐标 $t$ 为锚点，各 patch 位置为

$$
p_{a,b}=(t,t+a,t+b),\quad 0\le a<h',\;0\le b<w'.
\tag{1}
$$

视觉侧结束该帧的 separator token 与文本流中对应的帧占位 token 使用相同坐标，因此两个通道沿同一时间线前进。64 对旋转频率按 $(24,20,20)$ 分配到 $(t,h,w)$ 三轴；文本侧 query 与视觉侧 key 在进入交叉注意力前分别施加旋转。这里的 $t$ 是相对序列坐标，不是墙钟时间；真实时间由 §2.4 的时间戳 token 提供。

> **句读**：`shared timeline` 指逻辑位置的一致编号，并不意味着 XRoPE 自身编码真实秒数。论文随后专门用绝对时间戳补足可变帧率下的物理时间。

**Figure 3.** XRoPE places text tokens and visual patches in one shared three-axis coordinate system before cross-attention.

![Figure 3](./MOSS-VL-2608/images/fig_03.png)

**图 3.** XRoPE 在进入交叉注意力前，把文本 token 与视觉 patch 放到共享的三轴坐标系统中。

<!-- chunk: 2.04 | source: p5 §2.4 | role: wall-clock-time -->

**Original**

Positions alone say nothing about wall-clock time, and frame rates vary: MOSS-VL samples video at 1–16 fps, motion-adaptive (Table 2). Each frame is therefore preceded in the text stream by an absolute timestamp, `<|time_start|>X.X seconds<|time_end|>`, so the model reads real time from tokens rather than inferring it from positions, and timing stays explicit under any sampling rate.

**译文**

位置本身不携带墙钟时间，而视频帧率会变化：MOSS-VL 以运动自适应方式按 1–16 fps 采样视频（Table 2）。因此，每一帧之前都在文本流中插入绝对时间戳 `<|time_start|>X.X seconds<|time_end|>`。模型直接从 token 读取真实时间，而不是由位置推断；无论采样率如何变化，时间信息始终显式存在。

<!-- chunk: 2.05 | source: p5 §2.5 | role: append-only-realtime -->

**Original**

When a new frame arrives, only that frame is encoded; its keys and values are appended to the cross-attention cache, and earlier frames are neither re-encoded nor their keys and values recomputed. The decoded sequence grows by the frame’s timestamp tokens and a single placeholder token—patch tokens stay on the vision side—so an arriving stream leaves the decoding state intact, and the next generated token already attends to the updated cache through the gated layers. §6 quantifies the efficiency this yields at inference time (Figure 4).

**译文**

新帧到达时，系统只编码这一帧，并把它的 key/value 追加到 cross-attention cache；早期帧既不重新编码，其 key/value 也不重新计算。解码序列只增加该帧的时间戳 token 和一个占位 token，patch token 始终留在视觉侧。因此，持续到达的视频流不会破坏已有解码状态，而下一个生成 token 已能通过门控层访问更新后的缓存。§6 的 Figure 4 对这一设计的推理效率进行了量化。

<!-- chunk: 2.06 | source: p5–p6 §2.6 and Table 2 | role: released-models-and-configuration -->

**Original**

We release five checkpoints of one architecture (Table 3). The 0708 run—MOSS-VL-Base, MOSS-VL-Instruct, MOSS-VL-Realtime—is the subject of this report; the 0408 pair is an earlier, independently trained run of the same architecture, released for research continuity. The released processor defaults to 1 fps and 256 frames, while our evaluations keep 1 fps with the cap raised to 768 frames.

**译文**

作者为同一架构发布五个 checkpoint（Table 3）。本报告主要讨论 0708 训练运行：MOSS-VL-Base 是预训练模型，MOSS-VL-Instruct 在其上做标准 SFT，MOSS-VL-Realtime 再继续接受 Realtime-SFT。0408 的 Base/Instruct 是同架构的一次更早、独立训练的运行，为保持研究连续性而一并开放。发布的 processor 默认采用 1 fps、最多 256 帧；论文评测保持 1 fps，但把上限提高到 768 帧。

| 配置项 | MOSS-VL |
|---|---|
| 语言解码器 | 48 层：36 self-attention + 12 gated cross-attention；hidden 4096；FFN 12288；32Q/8KV GQA |
| 位置编码 | XRoPE 三轴 $(t,h,w)$，频率段 $(24,20,20)$，base $5\times10^6$ |
| 上下文 / 词表 | 262,144 token / 151,936 |
| 视觉编码器 | 27 层；hidden 1152；FFN 4304；16 heads；16×16 spatial patch |
| 视觉特征与投影 | layers {8,16,24} + final；2×2 spatial merge + MLP → 4096 |
| 输入分辨率 | 原生动态分辨率，4,096–16.8M 像素 |
| 视频采样 | 运动自适应 1–16 fps，通常 1–2 fps；训练最多 2,048 帧，评测最多 768 帧 |
| 总参数 | 11.3B，BF16 |

**Table 3.** Released MOSS-VL checkpoints and their initialization/training lineage.

![Table 3](./MOSS-VL-2608/images/fig_04.png)

**表 3.** 已发布 checkpoint 及其初始化与训练承接关系。

### 3. Pre-Training

<!-- chunk: 3.01 | source: p6 §3 opening | role: curriculum-shape -->

**Original**

MOSS-VL is pre-trained with a four-stage curriculum: vision–language alignment, large-scale multimodal pre-training, high-quality multimodal pre-training, and a final stage of annealing and long-context training. Table 4 lists the token budget, sample count, maximum sequence length, trainable modules, and peak learning rate of every stage, including the two post-training stages of §4. The table shows the shape of the curriculum: the maximum sequence length grows from 8K to 256K tokens, and the token budget shifts toward the later stages while sample counts fall by orders of magnitude—many short samples early, far fewer but much longer and denser ones late. Throughout, the data is decontaminated against our evaluation suites.

**译文**

MOSS-VL 采用四阶段预训练课程：视觉—语言对齐、大规模多模态预训练、高质量多模态预训练，以及最后的退火与长上下文训练。Table 4 列出每个阶段的 token 预算、样本数、最大序列长度、可训练模块和峰值学习率，同时包含 §4 的两个后训练阶段。课程结构很清楚：最大序列长度由 8K 逐步扩大到 256K，token 预算向后期集中，而样本数下降数个数量级——早期使用大量短样本，后期则使用少得多、但更长且信息密度更高的样本。作者称，所有阶段的数据都针对评测集做过去污染处理。

**Table 4.** Four pre-training stages followed by SFT and Realtime-SFT. Token counts are inputs to the language model after 2×2 visual-token compression.

![Table 4](./MOSS-VL-2608/images/fig_05.png)

**表 4.** 四阶段预训练以及随后的 SFT 与 Realtime-SFT。token 数按 2×2 视觉 token 压缩之后、实际送入语言模型的输入统计。

<!-- chunk: 3.02 | source: p6 | role: synthetic-data-foundation -->

**Original**

A defining trait of this training run is the scale of our data synthesis. Alongside data collected and reorganized from existing corpora, we synthesize high-quality caption, OCR, grounding, and temporal-grounding data at large scale throughout the curriculum. These four types cover the perceptual fundamentals of a vision–language model—describing scenes, reading embedded text, localizing objects, and anchoring events in time—and this synthesized core underpins the strong perception and temporal-understanding foundations of the released models.

**译文**

这次训练的显著特征，是合成数据的规模。除了收集并重新组织现有语料，作者还贯穿整个课程大规模合成高质量 caption、OCR、grounding 与 temporal-grounding 数据。这四类任务分别覆盖 VLM 的基础感知能力：描述场景、读取图中文字、定位对象以及把事件锚定到时间。论文将开放模型较强的感知与时间理解底座归因于这一合成数据核心。

<!-- chunk: 3.03 | source: p6–p7 §3.1–§3.2 | role: alignment-and-breadth -->

**Original**

Stage 1 connects the two pre-trained components. Only the newly introduced parameters—the projection module and the cross-attention layers—are updated, while the vision encoder and the language model remain frozen; the high peak learning rate in Table 4 applies to these fresh modules alone. The data comprises two categories, image captioning and OCR, and sequences stay short at 8K tokens. With the connectors aligned, Stage 2 unfreezes the full model and supplies breadth. The mixture spans image and video captioning, OCR, grounding, interleaved image–text documents, and text-only pre-training corpora, together with multimodal understanding data over single images, multi-image sets, videos, and plain text across diverse domains, and reasoning data. The context window extends to 64K tokens, which admits long interleaved documents and video.

**译文**

Stage 1 用于连接两个预训练组件。只更新新增的投影模块和交叉注意力层，视觉编码器与语言模型保持冻结；Table 4 中较高的峰值学习率只作用于这些新模块。数据仅包含图像 caption 与 OCR 两类，序列长度保持在 8K。连接器对齐后，Stage 2 解冻完整模型并扩展能力覆盖面。数据混合包括图像/视频 caption、OCR、grounding、图文交错文档、纯文本预训练语料，以及覆盖单图、多图、视频和纯文本多领域的多模态理解数据与推理数据；上下文扩展至 64K，以容纳长图文文档和视频。

<!-- chunk: 3.04 | source: p7 §3.3 | role: quality-rebalancing -->

**Original**

Stage 3 spends the largest token budget of the curriculum (Table 4) on its highest-quality data. The mixture keeps the Stage-2 categories but rebalances them: captioning recedes, multimodal understanding and reasoning data take a larger share, and mathematics, knowledge-intensive data, and temporal grounding enter the mixture. Sequences extend to 128K tokens.

**译文**

Stage 3 把课程中最大的 token 预算投入最高质量数据（Table 4）。它保留 Stage 2 的数据类别，但重新调整比例：caption 数据减少，多模态理解与推理数据占比上升，同时加入数学、知识密集型数据与 temporal grounding；序列长度扩展至 128K。

<!-- chunk: 3.05 | source: p7 §3.4 | role: long-context-and-annealing -->

**Original**

The final stage combines long-context training with high-quality annealing. One data strand consists of long-video captioning, long-video QA, and long-video temporal grounding, together with long-document and long-text data, mixed with a small share of the regular categories, and stretches sequences to 256K tokens. The other is an annealing mixture that re-weights toward mathematics, knowledge-intensive data, and instruction-tuning and QA data, and includes identity data. The curriculum yields MOSS-VL-Base, the starting point for post-training (§4).

**译文**

最后阶段把长上下文训练与高质量退火结合起来。一条数据支线包含长视频 caption、长视频 QA、长视频 temporal grounding，以及长文档和长文本，并混入少量常规类别，把序列拉长到 256K。另一条支线是退火混合数据，增加数学、知识密集型数据、指令微调与 QA 数据的权重，同时包含 identity data。四阶段课程最终得到 MOSS-VL-Base，作为后训练的起点（§4）。

### 4. Post-Training

<!-- chunk: 4.01 | source: p8 §4 opening | role: two-stage-posttraining -->

**Original**

Post-training proceeds in two supervised stages (Table 4); neither uses reinforcement learning or a thinking mode. Standard supervised fine-tuning (SFT) turns MOSS-VL-Base into MOSS-VL-Instruct, an offline instruction follower. Realtime-SFT then continues from MOSS-VL-Instruct (Table 3) and installs the real-time interaction paradigm: deciding at every frame whether to speak, staying silent while nothing needs saying, and revising an answer when the scene overturns it. Every real-time-specific design choice in MOSS-VL lives in this final stage, which accounts for under 3% of the total training tokens.

**译文**

后训练包含两个监督阶段（Table 4），均不使用强化学习或 thinking mode。标准 SFT 先把 MOSS-VL-Base 训练成离线指令跟随模型 MOSS-VL-Instruct；Realtime-SFT 再从 MOSS-VL-Instruct 继续训练（Table 3），安装实时交互范式：每一帧都判断是否开口，无事可说时保持沉默，场景推翻旧答案时进行修正。MOSS-VL 的所有实时专用设计都位于最后这个阶段，其 token 数少于总训练量的 3%。

> **句读**：`under 3%` 是相对比例。由 Table 4 可算出全课程共 1.4T token，Realtime-SFT 的 34.8B 占 2.49%；“轻”不能理解为绝对训练成本很低。

#### 4.1 Supervised Fine-Tuning

<!-- chunk: 4.02 | source: p8 §4.1 | role: offline-sft-mixture -->

**Original**

We fine-tune MOSS-VL-Base on 7.6M instruction samples (102.8B tokens) with the standard next-token cross-entropy loss over assistant responses, with sequences up to 128K tokens (Table 4). The samples combine data collected and reorganized from existing corpora with data synthesized in house, and all of it passes filtering, deduplication, decontamination against our evaluation suites, and quality screening before entering the mixture. The mixture covers general question answering over single images, multi-image sets, videos, and plain text; perception-centric tasks including OCR, document understanding, and spatial and temporal grounding; image and video captioning; and reasoning-centric tasks spanning multimodal reasoning, mathematics and other academic disciplines, code, and knowledge-intensive QA, together with identity data.

**译文**

作者使用 7.6M 条指令样本、共 102.8B token 对 MOSS-VL-Base 进行微调，最大序列长度 128K，并对 assistant 回复使用标准 next-token cross-entropy loss（Table 4）。数据既包括从现有语料收集重组的部分，也包括内部合成部分；进入混合数据前，会经过过滤、去重、针对评测集的去污染与质量筛选。任务覆盖单图、多图、视频和纯文本的一般问答；OCR、文档理解、空间与时间 grounding 等感知任务；图像和视频 caption；以及多模态推理、数学与其他学科、代码、知识密集型 QA 等推理任务，同时加入 identity data。

#### 4.2 Realtime-SFT: Learning When to Speak

<!-- chunk: 4.03 | source: p8 §4.2 | role: decision-slot-formulation -->

**Original**

Realtime-SFT teaches the model to treat incoming video as a stream of decisions rather than a finished artifact. Training samples interleave text with frames in arrival order: every frame is followed by a decision slot, and each slot takes one of three forms—`<|silence|>` (keep watching), `<|response|>` followed by text (speak now), or a reply that ends with `<|silence|>` (finish speaking). A reply is spread over consecutive slots frame by frame, emulating rate-limited real-time output, and a single user turn may contain several separate emissions. Supporting this costs exactly two new vocabulary entries—the two state tokens, initialized from the embeddings of semantically related existing tokens. The speak-or-wait decision itself is ordinary next-token prediction: whenever the most probable next token is `<|silence|>`, the model waits for the next frame; otherwise it decodes a reply. No dedicated decision head is attached.

**译文**

Realtime-SFT 教模型把到达的视频视为一串持续决策，而不是已经完成的对象。训练样本按到达顺序交错排列文本与帧：每帧之后都有一个决策槽位，每个槽位有三种形式——`<|silence|>` 表示继续观察，`<|response|>` 后接文本表示现在开口，回复以 `<|silence|>` 结束则表示说完。一次回复会逐帧铺在连续槽位上，模拟受速率限制的实时输出；同一个 user turn 可以包含多次独立发言。为此只新增两个词表项，即两个状态 token，并用语义相近的现有 token embedding 初始化。说或等本身仍是普通 next-token prediction：若概率最高的下一个 token 是 `<|silence|>`，模型等待下一帧；否则开始解码回复，不额外设置决策 head。

<!-- chunk: 4.04 | source: p8 §4.2 | role: interaction-roles -->

**Original**

What sets the Realtime-SFT corpus (0.56M samples, approximately 34.8B tokens; Table 4) apart is that every sample casts the model in an explicit interaction role rather than a plain QA role: standing instructions that must fire exactly once when their condition is met; resident questions whose answers must update as evidence accumulates; continuous real-time commentary; counting that accumulates across a stream; probes of whether this is the right moment to speak; and video-independent dialogue that maintains identity consistency. A further share of offline QA and general multimodal data preserves offline ability.

**译文**

Realtime-SFT 语料包含 0.56M 样本、约 34.8B token（Table 4）。它与普通 QA 数据的区别在于，每个样本都为模型赋予明确交互角色：条件满足时必须准确触发一次的常驻指令；随着证据累积而更新答案的持续查询；连续实时解说；跨视频流累加的计数；判断当前是否是开口时机的探测任务；以及维持身份一致性的、与视频无关的对话。数据中还保留一部分离线 QA 与一般多模态数据，以维持离线能力。

<!-- chunk: 4.05 | source: p8 | role: data-synthesis-and-grounding -->

**Original**

The corpus draws on two sources. We first collect open-source datasets for streaming video understanding and subject them to strict filtering and re-annotation. More important, however, is the data we synthesize ourselves, targeting the behaviors that existing datasets provide scarcely or not at all: staying silent until evidence appears, revising an answer as the scene evolves, and recovering when a new event interrupts a reply midway. Synthesis follows the caption-driven pipeline introduced in MOSS-Video-Preview [39]: hierarchical, densely time-anchored captions are mined for state transitions of a focal object; each transition yields a question, an immediately answerable reply, and a trajectory of updates; replies are anchored to visual moments, laid out over frames with silence in between, and filtered for quality. This round verifies temporal anchoring frame by frame against the footage, rewrites a reply overtaken by a new event as a natural-language self-correction rather than a dedicated interrupt token, and checks that every retained reply is grounded in what is visible at emission time.

**译文**

语料来自两类来源。作者先收集流式视频理解的开源数据集，并严格过滤、重新标注；更重要的是自行合成的数据，它专门覆盖现有数据稀缺或完全缺失的行为：证据出现前保持沉默、场景演化时修正答案，以及新事件在回复中途发生时恢复。合成沿用 MOSS-Video-Preview [39] 的 caption 驱动流水线：从具有层级结构、密集时间锚点的 caption 中挖掘焦点对象的状态转移；每次转移生成一个问题、一个当下即可回答的回复，以及后续更新轨迹；回复被锚定到相应视觉时刻，铺在帧序列上，中间插入沉默，再接受质量过滤。本轮改进会逐帧对照真实视频验证时间锚点；若新事件使旧回复失效，就把后续内容改写为自然语言自我修正，而不是使用专门 interrupt token；最后还会检查保留的每条回复是否在发出时刻有可见证据支持。

<!-- chunk: 4.06 | source: p9 corpus statistics | role: decision-distribution -->

**Original**

Across the corpus the model is supervised on 2.2M emission decisions, 58.7% of which are self-timed rather than prompted by a fresh user question; in 5.1% of samples the target event never occurs, and the correct behavior is to stay silent throughout. Streams run at 1 fps for up to 768 frames (approximately 12.8 minutes) per window. The corpus is decontaminated against our evaluation suites: benchmark videos are excluded via held-out lists.

**译文**

整个语料提供 2.2M 次发言决策监督，其中 58.7% 属于模型自主择时，而非由新的用户问题触发。5.1% 的样本中目标事件始终不会发生，正确行为是全程沉默。每个窗口以 1 fps 运行，最多 768 帧，约 12.8 分钟。作者使用 held-out list 排除 benchmark 视频，对语料做评测集去污染。

#### 4.3 Mode Control and Training Objective

<!-- chunk: 4.07 | source: p9 §4.3 | role: prompt-and-loss -->

**Original**

Mode control in MOSS-VL amounts to a single system prompt. The streaming and real-time modes share one prompt—real-time operation is a special case of streaming—and offline inference uses none. One set of weights thus operates in three inference modes with zero architecture change:

> You are a helpful AI assistant specializing in real-time video analysis. The video streams to you frame by frame. At every frame, you decide independently whether to respond or stay silent—output `<|silence|>` when nothing relevant has happened, and respond when the visual content warrants it.

Supervision covers only what the assistant controls: reply text and the two state tokens. System and user turns and the expanded visual tokens are excluded from the loss. Silence slots vastly outnumber emission decisions, so under uniform weights the model simply learns to stay silent. The state tokens are therefore reweighted with a focal factor and inverse-frequency class coefficients:

$$
\mathcal{L}=\frac{\sum_i m_i w_i \ell_i}{\sum_i m_i},\qquad
w_i=\begin{cases}
\alpha_{y_i}(1-p_i)^\gamma,& y_i\text{ is a state token},\\
1,&\text{otherwise},
\end{cases}
\tag{2}
$$

where $\ell_i$ is token-level cross-entropy, $m_i$ the supervision mask, $p_i$ the predicted probability of the target token, and $\gamma=2$. The coefficient $\alpha_k=(n_s+n_r)/(2n_k)$ is computed from silence and response targets in the current global batch, equalizing the nominal aggregate weight of the two state-token classes before focal modulation; reply text keeps unit weight.

**译文**

MOSS-VL 的模式控制只依赖一个 system prompt。流式与实时模式共享同一 prompt——实时运行被视为流式运行的特殊情况——离线推理则不使用它。因此，同一组权重无需修改架构即可运行在三种推理模式：

> 你是一名擅长实时视频分析的 AI 助手。视频会逐帧流入。每一帧到来时，你都要独立判断是回复还是保持沉默：若没有发生相关事件，输出 `<|silence|>`；当视觉内容值得回应时再作答。

监督只覆盖 assistant 能控制的内容，即回复文本与两个状态 token；system/user turn 和展开后的视觉 token 均不进入 loss。由于沉默槽位远多于发言决策，使用均匀权重时模型会退化为始终沉默。因此，作者对两个状态 token 同时应用 focal factor 与逆频率类别系数：

$$
\mathcal{L}=\frac{\sum_i m_i w_i \ell_i}{\sum_i m_i},\qquad
w_i=\begin{cases}
\alpha_{y_i}(1-p_i)^\gamma,& y_i\text{ 为状态 token},\\
1,&\text{其他情况},
\end{cases}
\tag{2}
$$

其中 $\ell_i$ 是 token 级交叉熵，$m_i$ 是监督 mask，$p_i$ 是目标 token 的预测概率，$\gamma=2$。系数 $\alpha_k=(n_s+n_r)/(2n_k)$ 由当前 global batch 中的 silence/response 目标数计算，使 focal 调制前两个状态类别的名义总权重相等；回复文本仍保持单位权重。

<!-- chunk: 4.08 | source: p9 | role: turn-end-masking -->

**Original**

One further masking choice matters specifically in streams. In offline chat, the token closing an assistant turn marks the end of an exchange; in a stream, a turn boundary usually means the user interjected while the world—and the conversation—continue. We therefore also exclude the assistant’s turn-final end token from supervision, so the model never learns to wrap up merely because a new user turn appears. In a controlled single-variable comparison, this masking raised emission frequency by 39% and mean reply length by 68%. The behaviors installed here are evaluated quantitatively on four streaming benchmarks in §6 and qualitatively in Figure 5.

**译文**

还有一个 mask 选择对视频流尤其重要。离线聊天中，assistant turn 的结束 token 表示一轮交换结束；在流中，turn 边界通常只是用户插话，世界与对话都仍在继续。因此，作者也把 assistant turn 末尾的结束 token 排除在监督之外，避免模型仅仅因为出现新的 user turn 就学习收尾。在一个只改变该因素的对照中，这种 mask 使发言频率提高 39%，平均回复长度提高 68%。这些行为在 §6 的四个流式 benchmark 上定量评测，并在 Figure 5 中定性展示。

> **句读**：这里的单变量实验只支持“结束 token mask 会改变发言频率与长度”，并未说明这种改变必然提高发言正确性；频率上升也可能增加误触发，需要与 precision/false alarm 联合判断。

### 5. Infrastructure

<!-- chunk: 5.01 | source: p9–p10 §5 | role: training-stack-and-kernel -->

**Original**

MOSS-VL is trained on a Megatron-LM stack [35] that combines data, tensor, sequence, and context parallelism to carry the curriculum from 8K- to 256K-token sequences. Variable-length multimodal samples are packed into full sequences, keeping batches dense across mixed image, video, and text data. The gated cross-attention has a visibility pattern that off-the-shelf attention kernels do not serve: each text query attends to the visual tokens of every frame that precedes it, so visibility is a per-query prefix of the key–value sequence, growing frame by frame.

FlashAttention exposes causal or windowed masks, and materializing this pattern as a dense cross-attention mask costs memory and bandwidth proportional to the product of text and visual sequence lengths. We therefore extend FlashAttention-3 [33] with `cross_kv_boundary`, which encodes the visible prefix of each query row as one 32-bit integer and carries it through the operator schema, scheduler, and CUDA forward/backward kernels. Key–value tiles beyond a row’s boundary are pruned rather than computed and masked, so kernel cost tracks visibility. The backend covers dense, variable-length, and KV-cache paths and remains compatible with packed training.

**译文**

MOSS-VL 使用 Megatron-LM [35] 训练栈，组合 data、tensor、sequence 与 context parallelism，把课程从 8K 序列推进到 256K。不同长度的多模态样本会被 pack 成完整序列，使混合图像、视频与文本数据的 batch 保持稠密。门控交叉注意力具有现成 kernel 无法直接表达的可见性模式：每个文本 query 只能访问它之前所有帧的视觉 token，因此可见区域是 key–value 序列上一个逐帧增长、且因 query 而异的前缀。

FlashAttention 原生提供 causal 或 window mask；若把上述模式物化为稠密 cross-attention mask，内存与带宽成本会与文本长度和视觉长度的乘积成正比。作者因此扩展 FlashAttention-3 [33]，引入 `cross_kv_boundary`：每个 query row 只用一个 32-bit 整数编码可见前缀边界，并把该信息贯穿 operator schema、scheduler 与 CUDA 前后向 kernel。超过该行边界的 KV tile 会直接被裁掉，而不是先计算再 mask，因此 kernel 成本随实际可见区域变化。后端覆盖 dense、variable-length 与 KV-cache 三条执行路径，也就能兼容 packed training。

<!-- chunk: 5.02 | source: p10 | role: serving-release -->

**Original**

Our SGLang [56] integration of MOSS-VL is merged upstream, and the offline-serving measurements of §6 (Figure 4) run on this stack. Real-time interaction ships separately as a Transformers reference implementation, released with the model weights on GitHub and HuggingFace.

**译文**

MOSS-VL 的 SGLang [56] 集成已经合入上游，§6 Figure 4 的离线服务测量即运行在这套栈上。实时交互则以单独的 Transformers 参考实现发布，并与模型权重一同放在 GitHub 和 HuggingFace。

### 6. Evaluation

<!-- chunk: 6.00 | source: p10–p11 §6 opening | role: evaluation-regimes -->

**Original**

We evaluate each model in the regime it is built for: MOSS-VL-Instruct on an offline suite of 39 benchmarks across five capability domains (Table 5), and MOSS-VL-Realtime on four streaming benchmarks—OVO-Bench [20], OmniMMI [44], StreamingBench [21], and ProactiveVideoQA [43]—which together cover levels L2–L4 of the capability hierarchy in Table 1. All streaming evaluation is carried out in streaming fashion: frames are fed as they would arrive, and every model runs under its own streaming protocol. Measured serving efficiency (§6.3) and qualitative real-time sessions (§6.4) complete the picture.

**译文**

论文在各模型原本面向的范式中进行评测：MOSS-VL-Instruct 使用覆盖五类能力、共 39 个 benchmark 的离线套件（Table 5）；MOSS-VL-Realtime 则使用 OVO-Bench [20]、OmniMMI [44]、StreamingBench [21] 与 ProactiveVideoQA [43] 四个流式 benchmark，它们合计覆盖 Table 1 能力层级中的 L2–L4。所有流式评测都按视频实际到达的方式逐帧输入，但每个模型运行在自己的流式协议下。§6.3 的服务效率实测与 §6.4 的实时定性会话构成另外两类证据。

#### 6.1 Offline Results

<!-- chunk: 6.01 | source: p12 §6.1 | role: protocol-and-comparability -->

**Original**

Table 5 compares MOSS-VL-Instruct with open models of comparable scale—Qwen3-VL-8B [4], Qwen2.5-VL-7B [5], LLaVA-OneVision-2-8B [3], and Gemma-4-12B-IT [14]—over multimodal perception, video understanding, grounding, document/OCR, and reasoning. MOSS-VL results sample video at 1 fps with at most 768 frames, following a benchmark’s official protocol wherever one is prescribed; DocVQA and InfoVQA use the validation split. Baseline numbers are taken from the respective official reports and reflect their authors’ inference settings, which may differ from ours, particularly in video frame count. The exceptions are Gemma-4-12B-IT, which we evaluated under the same protocol as MOSS-VL, and Qwen3-VL on OmniDocBench v1.6, evaluated with the official cookbook’s Markdown prompt; remaining OmniDocBench baselines are omitted because their official numbers are not metric-comparable.

**译文**

Table 5 从多模态感知、视频理解、grounding、文档/OCR 与推理五个领域，对比 MOSS-VL-Instruct 和相近规模的开放模型：Qwen3-VL-8B [4]、Qwen2.5-VL-7B [5]、LLaVA-OneVision-2-8B [3] 与 Gemma-4-12B-IT [14]。MOSS-VL 以 1 fps、最多 768 帧采样视频；benchmark 有官方协议时按官方协议执行，DocVQA 与 InfoVQA 使用 validation split。基线数值大多来自各自官方报告，因此继承了原作者的推理设置，尤其视频帧数可能与 MOSS-VL 不同。例外是 Gemma-4-12B-IT，由作者按 MOSS-VL 相同协议评测；Qwen3-VL 的 OmniDocBench v1.6 使用官方 cookbook 的 Markdown prompt。其他 OmniDocBench 基线因官方指标不可比而省略。

<!-- chunk: 6.02 | source: p12 §6.1 | role: offline-results -->

**Original**

Perception is the strongest block: MOSS-VL-Instruct takes five of the twelve rows—MMBench-EN (88.1), POPE (89.4), V* (89.0), and both MME-RealWorld (66.3) and BLINK (78.0) by 8.9-point margins. On video, it leads the temporal-reasoning sets—Minerva (40.5), TOMATO (39.5), and VideoMME-Logical (17.1), each by 4.9 points or more—plus EgoSchema (67.0), consistent with the perception and temporal-understanding foundations built in §3. The wins extend across the remaining domains: Ref-Adv grounding (57.0), OmniDocBench document parsing (88.9), VisuLogic (27.5), and a shared top ERQA score (45.8). The main gaps sit in MMMU, document understanding, and standard grounding, both referring and temporal; the first two are revisited in §7.

**译文**

感知是 MOSS-VL-Instruct 最强的一组：12 项中拿下 5 项，包括 MMBench-EN 88.1、POPE 89.4、V* 89.0，以及均领先 8.9 分的 MME-RealWorld 66.3 与 BLINK 78.0。视频领域中，它在 Minerva 40.5、TOMATO 39.5 与 VideoMME-Logical 17.1 三个时间推理数据集上领先，优势均不少于 4.9 分，并在 EgoSchema 得到 67.0；这一结果与 §3 建立的感知和时间理解底座相符。其他领域的领先项包括 Ref-Adv grounding 57.0、OmniDocBench 文档解析 88.9、VisuLogic 27.5，以及并列第一的 ERQA 45.8。主要短板位于 MMMU、文档理解与标准 grounding，包括 referring 和 temporal grounding；§7 会再次讨论前两项。

**Table 5.** Offline results across 39 benchmarks and five capability domains. Bold and underline denote the best and second-best reported values.

![Table 5](./MOSS-VL-2608/images/fig_07.png)

**表 5.** 五类能力、39 个离线 benchmark 的结果。粗体与下划线分别表示所列结果中的第一和第二。

#### 6.2 Streaming Benchmarks

<!-- chunk: 6.03 | source: p12 §6.2 | role: baselines-and-metrics -->

**Original**

Table 6 reports subset-level results on four streaming benchmarks. Baselines are open-source streaming models—AURA [24], M4 [44], ROMA [36], JoyAI-VL-Interaction [51], VideoChat3-4B [18], ViSpeak-7B [11], and the MMDuet family [41–43]. Baseline numbers come from their official reports, except MMDuet’s OmniMMI entry, which comes from the ROMA report; MOSS-VL-Realtime numbers are from our evaluation under each benchmark’s official protocol. MOSS-VL-Realtime runs an 8.2B language backbone, comparable to the 7–8B-class baselines; its additional parameters lie outside the decoded sequence, in the vision encoder and cross-attention stack.

Each benchmark reports at subset level. OVO-Bench separates forward active responding (FAR), backward tracing (BT), and real-time visual perception (RTVP). OmniMMI covers proactive alerting (PA), dynamic state grounding (SG), multi-turn dependency (MD), action prediction (AP), and speaker identification (SI). StreamingBench reports real-time visual understanding (RT), contextual understanding (CTX), proactive output (PO), and sequential QA (SQA); its visual average covers RT and CTX, while MOSS-VL takes no audio input and therefore has no official overall score. ProactiveVideoQA splits web, egocentric, TV-series, and video-anomaly videos.

**译文**

Table 6 给出四个流式 benchmark 的子集级结果。基线包括 AURA [24]、M4 [44]、ROMA [36]、JoyAI-VL-Interaction [51]、VideoChat3-4B [18]、ViSpeak-7B [11] 与 MMDuet 系列 [41–43]。基线数值来自各自官方报告，只有 MMDuet 的 OmniMMI 条目取自 ROMA 报告；MOSS-VL-Realtime 则由作者按各 benchmark 官方协议评测。其语言 backbone 为 8.2B，与 7–8B 级基线相近；额外参数位于解码序列之外的视觉编码器和 cross-attention stack。

各 benchmark 都提供子集结果。OVO-Bench 分为 forward active responding（FAR）、backward tracing（BT）与 real-time visual perception（RTVP）。OmniMMI 包含 proactive alerting（PA）、dynamic state grounding（SG）、multi-turn dependency（MD）、action prediction（AP）和 speaker identification（SI）。StreamingBench 报告 real-time visual understanding（RT）、contextual understanding（CTX）、proactive output（PO）与 sequential QA（SQA）；visual average 只平均 RT 与 CTX。MOSS-VL 不接收音频，因此没有包含 audio-dependent Omni-Source 的官方总分。ProactiveVideoQA 则按 web、egocentric、TV-series 与 video anomaly detection 四种来源划分。

<!-- chunk: 6.04 | source: p12–p13 §6.2 | role: streaming-results -->

**Original**

MOSS-VL-Realtime posts the best average on three of the four benchmarks—OVO-Bench (70.2 vs. 65.3 for the runner-up), OmniMMI (32.7 vs. 25.4), and ProactiveVideoQA (47.2 vs. 42.7)—and is second on StreamingBench’s visual average (69.7 vs. AURA’s 71.1). The subset pattern says more than the averages. The three subsets that squarely test proactive behavior—speaking unprompted, at the right moment—all go to MOSS-VL-Realtime: Proactive Alerting on OmniMMI (66.0 vs. 37.5), Proactive Output on StreamingBench (60.0 vs. 53.2), and Forward Active Responding on OVO-Bench (62.1 vs. 55.8). ProactiveVideoQA follows in aggregate, and Backward Tracing on OVO-Bench (72.6 vs. 60.4) shows accumulated stream history staying usable. The wins concentrate where response timing is the skill under test—the behavior Realtime-SFT supervises directly; where a subset reduces to perception QA over the current scene, AURA keeps the edge.

**译文**

MOSS-VL-Realtime 在四个 benchmark 中取得三个平均分第一：OVO-Bench 为 70.2，第二名 65.3；OmniMMI 为 32.7，第二名 25.4；ProactiveVideoQA 为 47.2，第二名 42.7。StreamingBench visual average 则以 69.7 位居第二，AURA 为 71.1。比平均分更重要的是子集分布。三个直接测试主动行为——即无需新问题、在正确时点开口——的子集全部由 MOSS-VL-Realtime 领先：OmniMMI PA 为 66.0 对 37.5，StreamingBench PO 为 60.0 对 53.2，OVO-Bench FAR 为 62.1 对 55.8。ProactiveVideoQA 的汇总结果也保持这一趋势，OVO-Bench BT 的 72.6 对 60.4 则提示累积的视频流历史仍可利用。优势集中在“回复时机”本身是待测能力的地方，这正是 Realtime-SFT 直接监督的行为；当子集退化为当前场景上的感知 QA 时，AURA 仍占优。

**Table 6.** Subset-level results on four streaming benchmarks.

![Table 6](./MOSS-VL-2608/images/fig_08.png)

**表 6.** 四个流式 benchmark 的子集级结果。比较面板按各官方报告的覆盖范围而异。

#### 6.3 Inference Efficiency

<!-- chunk: 6.05 | source: p13 §6.3 | role: controlled-serving-comparison -->

**Original**

Figure 4 measures serving latency against Qwen3-VL-8B, which shares the Qwen3-8B language backbone; the comparison therefore isolates the vision-integration architecture. Both models run offline SGLang serving on a single H200 (TP=1, BF16, identical engine version), with an identical generation-length cap that every run reaches; every point is the mean of five independent cold starts. With ViT output matched, the time-to-first-token gap widens from 2.8× to 5.1× as visual context grows, and end-to-end latency from 1.9× to 4.3×. The same-video comparison is stricter for MOSS-VL: it forgoes temporal compression so that each arriving frame can be encoded immediately, and thus carries about twice the vision tokens of Qwen3-VL on identical input—yet it never falls behind at any measured point. The advantage widens with visual context, exactly the regime a real-time assistant occupies.

**译文**

Figure 4 以 Qwen3-VL-8B 为对手测量服务延迟；两者共享 Qwen3-8B 语言 backbone，因此比较主要隔离视觉集成架构。两模型都在单张 H200 上以 SGLang 离线服务，TP=1、BF16、engine 版本相同，设置相同的生成长度上限且每次运行都达到上限；每个点是五次独立冷启动的均值。匹配 ViT 输出 token 数时，随着视觉上下文增长，首 token 延迟差距由 2.8× 扩至 5.1×，端到端延迟差距由 1.9× 扩至 4.3×。同视频比较对 MOSS-VL 更严格：为了让新帧可立即独立编码，它放弃时间轴压缩，因此相同输入约有 Qwen3-VL 两倍的视觉 token，但所有测量点都未落后。优势随视觉上下文增大，而这正是实时助手会长期处于的工作区间。

**Figure 4.** Measured serving latency of MOSS-VL and Qwen3-VL-8B under matched visual tokens and identical videos/frame counts.

![Figure 4](./MOSS-VL-2608/images/fig_06.png)

**图 4.** MOSS-VL 与 Qwen3-VL-8B 在匹配视觉 token，以及相同视频/帧数两种条件下的实测服务延迟；误差条为五次冷启动的样本标准差。

#### 6.4 Qualitative Results

<!-- chunk: 6.06 | source: p13–p14 §6.4 | role: live-demonstrations -->

**Original**

Figure 5 shows the installed behaviors in live operation, with two sessions from the released demo. Under a standing conditional instruction, the model holds silence over the full stream and fires at each of the four target contacts, and only there; under a single commentary instruction, it opens within a second and tracks a free-kick sequence through the whistle, the strike, the celebration, and the updated scoreline. Between them, the sessions exercise the core interaction roles of the Realtime-SFT corpus—a standing instruction that must fire exactly when its condition is met, and continuous real-time commentary—under real-world timing.

**译文**

Figure 5 展示了发布版 live demo 中的两段实际会话。第一段给出常驻条件指令：只有猫碰到胡萝卜时才说“真棒”，其他时候保持沉默。模型在整条流中只于四次目标接触时触发。第二段只给出一次“实时解说”指令，模型不到一秒即开口，并依次跟随任意球准备、裁判鸣哨、射门、庆祝与比分更新。两段会话分别覆盖 Realtime-SFT 的核心交互角色：条件满足时准确触发的常驻指令，以及在真实时间中连续展开的实时解说。

**Figure 5.** Two live sessions: conditional alerting and continuous real-time commentary.

![Figure 5](./MOSS-VL-2608/images/fig_09.png)

**图 5.** 两段 live session：条件触发与连续实时解说。空心标记示意静默区间中的 `<|silence|>` 输出。

### 7. Discussion

<!-- chunk: 7.01 | source: p14 §7 | role: integrated-interpretation -->

**Original**

Read as a whole, the evaluation shows a pattern rather than a score. The streaming wins concentrate in the subsets that test when to speak; the serving advantage widens exactly where visual history accumulates; the offline strengths cluster on temporal-reasoning video sets. No single component explains this shape. It is what co-design looks like from the outside: an architecture in which perception runs naturally alongside generation, a corpus that supervises response timing, and a curriculum that builds the foundation before one light final stage makes it interactive. We treat the full system, not just the weights, as the release: alongside all five checkpoints come the staged training curriculum, the complete Realtime-SFT dialogue template, the real-time inference implementation, the extended FlashAttention-3 backend, and the recorded live sessions.

**译文**

从整体看，评测呈现的是一种结构，而不只是若干分数：流式优势集中于考查何时开口的子集；服务优势恰在视觉历史不断累积的区间扩大；离线优势则集中在时间推理视频集。没有任何单一组件足以解释这一形状。它从外部体现了协同设计的结果：架构使感知能够与生成自然并行，语料监督回复时机，课程先建立底座，再由最后一个较轻阶段赋予交互能力。作者把完整系统而不仅是权重视为发布物：五个 checkpoint 之外，还包括分阶段训练课程、完整 Realtime-SFT 对话模板、实时推理实现、扩展的 FlashAttention-3 后端与录制的 live session。

<!-- chunk: 7.02 | source: p14–p15 §7 | role: limitations-and-agenda -->

**Original**

The limits are equally visible. MOSS-VL-Instruct trails the strongest open models of its scale on reasoning-heavy suites such as MMMU and on document-centric benchmarks: MOSS-VL ships without a thinking mode, and its training optimizes for real-time video rather than exam-style reasoning. The capability this report is built around is, at its highest level, still qualitatively attested: quantitative validation stops at L2–L4 because public streaming benchmarks stop there, and no existing benchmark measures perception during generation—whether a model revises or cuts short a reply the moment the scene overturns it. Both limits mark the near-term agenda: reinforcement-learning post-training for the MOSS-VL series, already on the public roadmap, and a dedicated benchmark for L5 behavior.

**译文**

系统边界同样清楚。MOSS-VL-Instruct 在 MMMU 等重推理套件和文档类 benchmark 上落后于同规模最强开放模型；它没有 thinking mode，训练目标也更偏向实时视频而非考试式推理。更关键的是，本报告围绕的最高层能力仍只有定性证据：公共流式 benchmark 止于 L2–L4，因此量化验证也止于此；现有 benchmark 没有测量生成过程中的持续感知，即场景推翻旧证据时，模型是否会立即修正或中断回复。两项限制对应近期议程：为 MOSS-VL 加入强化学习后训练，以及建立专门的 L5 benchmark。

### 8. Conclusion

<!-- chunk: 8.01 | source: p15 §8 | role: conclusion -->

**Original**

MOSS-VL makes real-time interaction a first-class capability of an open vision–language model family. It is built in, not bolted on: gated cross-attention with XRoPE lets frames arrive while text is being generated, synthesized interaction data teaches the model when to speak, when to wait, and when to revise, and a staged curriculum confines every real-time-specific choice to one light final stage. In evaluation, MOSS-VL-Instruct holds strong offline ground, especially on temporal-reasoning tasks, MOSS-VL-Realtime leads streaming benchmarks wherever response timing is tested, and serving latency grows more slowly with visual context than an interleaved peer’s. Weights, curriculum, and code are open.

**译文**

MOSS-VL 把实时交互变成开放视觉—语言模型家族的一等能力。这项能力内生于系统，而非事后外挂：带 XRoPE 的门控交叉注意力允许文本生成时继续接收视频帧；合成交互数据教模型何时说、何时等、何时修正；分阶段课程则把全部实时专用选择约束在最后一个较轻阶段。评测中，MOSS-VL-Instruct 保持较强离线能力，尤其擅长时间推理；MOSS-VL-Realtime 在考查回复时机的流式 benchmark 上领先；随视觉上下文增加，其服务延迟也比视觉 token 与文本交错的同类模型增长更慢。作者开放了权重、课程和代码。

*References omitted — see original PDF.*

### Appendix A. Real-Time Interaction Details

#### A.1 Real-Time Dialogue Template

<!-- chunk: App.A.01 | source: p21 Appendix A.1 | role: three-mode-template -->

**Original**

All three inference modes share the released ChatML-style chat template. Offline inference is standard: the full video is encoded as one vision block and the model replies as an ordinary chat assistant, with no dedicated system prompt. The streaming and real-time modes prepend the shared system prompt of §4.3 and lay every assistant turn out as an alternating stream of decision slots $t_i$ and frame placeholders, so $N$ frames leave the model $N+1$ decisions. Each slot takes one of three forms: `<|silence|>`—nothing to say at this frame; `<|response|>` followed by a text chunk—speaking, not yet finished; or a chunk closed by `<|silence|>`—the reply ends here.

**译文**

三种推理模式共享发布的 ChatML 风格模板。离线推理采用标准形式：完整视频编码为一个 vision block，模型像普通聊天助手一样回复，不设置专用 system prompt。流式与实时模式会在开头加入 §4.3 的共享 prompt，并把每个 assistant turn 排成决策槽位 $t_i$ 与帧占位符交替的序列，因此 $N$ 帧对应 $N+1$ 次决策。每个槽位有三种形式：`<|silence|>` 表示这一帧无话可说；`<|response|>` 后跟一段文本，表示正在说但尚未结束；文本片段以 `<|silence|>` 收尾，则表示回复到此结束。

<!-- chunk: App.A.02 | source: p21 template | role: end-to-end-layout -->

**Original**

```text
<|im_start|>system
the shared streaming / real-time system prompt (§4.3)<|im_end|>
<|im_start|>user
Tell me when the door opens.<|im_end|>
<|im_start|>assistant
<|silence|><|video|><|silence|><|video|><|silence|><|video|>
<|response|>The door is opening,<|video|>
<|response|>and a man in a red jacket steps in.<|silence|><|video|><|silence|>
<|video|><|response|>The door opens again,<|video|>
<|response|>another man, in a white shirt, steps in.<|silence|><|im_end|>
```

The example also includes a leading-slot-dropout variant where the frame arrives first. A reply can span consecutive frames, and a standing instruction can fire more than once in one assistant turn.

**译文**

上面的端到端布局展示了一条常驻指令：模型先对若干帧持续输出沉默；门第一次打开后，回复跨两个连续帧展开并以 `<|silence|>` 结束；门再次打开时，同一指令在同一个 assistant turn 中再次触发。附录还给出 leading-slot dropout 变体，即由 `<|video|>` 先出现，用来覆盖帧先于决策槽位到达的情况。

<!-- chunk: App.A.03 | source: p22 | role: processor-expansion-and-handshake -->

**Original**

The template keeps each frame as a single `<|video|>` placeholder; the processor—the same code path at training and inference time—expands it into a timestamped vision block:

```text
<|vision_start|><|time_start|>7.0 seconds<|time_end|><|image_pad|><|vision_end|>
```

The timestamp is plain text carrying the frame’s arrival time, so the model reads the current stream time directly from its input; `<|image_pad|>` is then replaced by the frame’s visual tokens according to its resolution. Training and inference must agree on this expansion byte for byte—any deviation shifts the model off its training distribution and suppresses emission.

At inference the runtime reproduces the training-time alternation with a strict handshake: it pushes one frame, waits for the model to emit a fresh `<|silence|>`, and only then pushes the next. While a long reply is still unfolding, a length budget releases the next frame instead, so the stream never stalls behind the reply. Replies therefore unfold across consecutive slots, one chunk per frame, exactly as in training.

**译文**

模板中每一帧只保留一个 `<|video|>` 占位符；训练与推理共用同一条 processor 代码路径，把它展开为带时间戳的 vision block：

```text
<|vision_start|><|time_start|>7.0 seconds<|time_end|><|image_pad|><|vision_end|>
```

时间戳是携带帧到达时刻的明文，因此模型可直接从输入读取当前流时间；`<|image_pad|>` 再根据分辨率替换为该帧的视觉 token。训练与推理必须逐 byte 保持一致，任何差异都会使模型偏离训练分布并抑制发言。

推理运行时以严格 handshake 复现训练中的交替结构：先推入一帧，等待模型产生新的 `<|silence|>`，然后才推入下一帧。若长回复仍在展开，长度预算会提前释放下一帧，避免视频流被回复阻塞。因此，回复会像训练时一样跨连续槽位展开，每帧承载一个文本 chunk。

> **句读**：`strict handshake` 与“生成时持续感知”之间存在一个需要实现层解释的张力。普通沉默状态下必须等模型完成本帧决策再送下一帧；长回复期间则由长度预算打破等待、插入新帧。L5 的实际时间分辨率因此取决于该预算和视觉编码/解码调度，而不仅是模型权重。

#### A.2 Live-Demo Session Transcripts

<!-- chunk: App.A.04 | source: p22 Table 7 | role: translated-live-outputs -->

**Original**

Figure 5 shows excerpts of the model’s Chinese outputs; Table 7 gives our English translations of both sessions, in output order. In the conditional-alert session, the model emits “Great!” at each of the four contacts and the silence token on every other frame. In the real-time commentary session, it describes the free-kick chance, the referee’s whistle, Ronaldo’s run-up and strike, his celebration, and the 3–3 scoreline.

**译文**

Figure 5 展示模型中文输出的节选，Table 7 则按输出顺序给出两段会话的英文翻译。条件触发会话中，模型在四次接触发生时分别输出“真棒！”，其他所有帧都输出沉默 token。实时解说会话依次描述关键任意球、裁判鸣哨、C 罗助跑射门、庆祝，以及葡萄牙将比分扳为 3–3。

**Table 7.** English translations of the two Chinese live-demo sessions in Figure 5.

![Table 7](./MOSS-VL-2608/images/fig_10.png)

**表 7.** Figure 5 两段中文 live demo 的英文翻译。

---

## 术语与符号 | Terms & Notation

| 原文 | 译法 / 保留形式 | 本文中的具体含义 |
|---|---|---|
| real-time interaction | 实时交互 | 专指 L5：模型在生成回复期间仍持续感知，不等同于一般流式输入 |
| streaming | 流式 | L2–L4；输入连续，但每次回复期间模型可能失去视觉输入 |
| perceive while generating | 生成时持续感知 | 场景变化能够作用于尚在生成的回复 |
| gated cross-attention | 门控交叉注意力 | 文本作 query、视觉作 KV，attention/FFN 路径外使用零初始化 tanh gate |
| XRoPE | XRoPE | 交叉注意力 Q/K 的三轴旋转位置编码，描述逻辑次序而非真实秒数 |
| absolute timestamp | 绝对时间戳 | 以明文 token 表示帧到达时间，和 XRoPE 的相对坐标互补 |
| decision slot | 决策槽位 | 每一帧之后的一次说/等机会 |
| emission decision | 发言决策 | 以 silence / response 两类状态 token 为目标的说或等预测 |
| standing instruction | 常驻指令 | 条件在视频流中持续有效，满足时才触发回复 |
| persistent query | 持续查询 | 问题保持驻留，证据变化时可以多次更新答案 |
| self-timed | 模型自主择时 | 发言不是由新的 user turn 直接触发 |
| `cross_kv_boundary` | 保留代码名 | 每个 query 的可见 KV 前缀边界，用于裁剪 FlashAttention tile |
