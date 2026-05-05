# context_omni_2604

> Auto-extracted preview. 14 pages, 2-column, 0 figures.

In the native multimodal regime, unified multimodal models [8, 11, 14, 18, 33, 35, 48] learn a world knowledge
manifold by taking inputs and predicting outputs across multiple modalities. Each modality provides only a
partial and biased view of this multimodal manifold, capturing complementary aspects of world knowledge.
We argue that native multimodal models can explicitly benefit from Context Unrolling - reasoning across
these heterogeneous modal projections to recover a more complete approximation of the shared multimodal
manifold. We observe that prediction quality improves as models perform Context Unrolling across more
modalities, integrating information from a broader set of modalities before producing outputs. By structuring
reasoning across different modal projections, the model forms a more faithful representation of the multimodal
manifold, producing outputs that are more coherent, faithful, and semantically accurate.

To realize this vision, we follow the design philosophy of BAGEL [8], and expand training modalities from
image–text pairs to a broader set of modalities including text, images, videos, 3D geometry, and hidden visual
representations. The expanded set of modalities provides complementary projections of world knowledge,
capturing information such as pixel appearance, spatial-temporal structure, camera transformations, depth,
physical dynamics, semantic abstraction, and dense conversational reasoning, which are essential for learning
grounded world knowledge at scale. Building upon the interleaved data paradigm introduced in BAGEL [8],
we further incorporate reasoning-oriented multimodal content to encourage structured cross-modal reasoning
during training. This enables generation to leverage not only short textual reasoning but also long-form

# Context Unrolling in O

# arXiv:2604.21921v1  [cs.CV]  23 Apr 2026

∗Equal contribution, †Corresponding authors

### We present O

Date: April 24, 2026

Project Page: https://omni-model.com/

1
Introduction

# mni Models

Ceyuan Yang∗,†, Zhijie Lin∗, Yang Zhao∗, Fei Xiao∗, Hao He∗, Qi Zhao∗,
Chaorui Deng, Kunchang Li, Zihan Ding, Yuwei Guo, Fuyun Wang,
Fangqi Zhu, Xiaonan Nie, Shenhan Zhu, Shanchuan Lin,
Hongsheng Li, Weiling Huang, Guang Shi†, Haoqi Fan

## Abstract

mni, a unified multimodal model natively trained on diverse modalities, including
text, images, videos, 3D geometry, and hidden representations. We find that such training enables
Context Unrolling, where the model explicitly reasons across multiple modal representations before
producing predictions. This process enables the model to aggregate complementary information
across heterogeneous modalities, facilitating a more faithful approximation of the shared mul-
timodal knowledge manifold and improving downstream reasoning fidelity. As a result, O mni
achieves strong performance on both multimodal generation and understanding benchmarks, while
demonstrating advanced multimodal reasoning capabilities, including in-context generation of text,
image, video, and 3D geometry.

mni selectively activates task-relevant contexts from a heterogeneous context
pool—spanning text, image, video, 3D geometry, and beyond—into a shared workspace before producing predictions.
This mechanism enables the model to aggregate complementary information across modalities, improving downstream
reasoning and generation fidelity.

structured descriptions with dense attributes, spatial grounding, and geometric constraints such as depth
maps and camera transformations. We additionally introduce a hidden reasoning space as a dedicated latent
representational space to support latent multimodal reasoning. Through this design, the unified model learns
to reason across heterogeneous modal projections while producing coherent multimodal predictions, enabling
richer cross-modal interaction and strengthening native multimodal learning capabilities.

mni, a multimodal foundation model that supports any-to-any multimodal learning.
Built upon BAGEL [8], O mni perform context unrolling across modalities to enable cross-modal reasoning. It
contains 3B active parameters and adopts a mixture-of-experts architecture. Compared with existing models
that typically map multimodal inputs to a single output modality, O mni unifies image, video, and text for
understanding, generation, and editing within a single architecture, achieving competitive or state-of-the-art
performance across a wide range of benchmarks.

The model achieves competitive or superior performance compared to leading open-source vision-language
models, including Qwen3-VL [1] and InternVL3.5 [42], across standard multimodal understanding benchmarks.
It also outperforms strong public image generators such as Z-Image [4], Flux [28], and Qwen-Image [43] on
the GenEval2 benchmark, and demonstrates consistently stronger qualitative performance on classical image
editing tasks compared to Step1X [29], Qwen-Image-Edit [43], and Z-Image-Edit [4]. Beyond static image
manipulation, O mni extends unified multimodal modeling to video generation and editing, demonstrating
strong semantic instruction-following capabilities in temporal visual reasoning and achieving superior qualitative
performance compared to Wan2.1 [38] and Hunyuan [22] on video generation and editing tasks. In 3D geometry,
O mni also achieves comparable performances to VGGT [40] in camera estimation and to Depth-Anything
3 [27] in depth estimation. By incorporating video as a native modality, O mni provides a unified framework
for text, image, video and 3D geometry within a single model architecture.

mni, we observe an emerging capability that we term Context Unrolling.
Given an arbitrary task, a native multimodal model develops the ability to unroll its internal “thinking”
across heterogeneous modalities. Each modality can be viewed as a projection of a shared latent world
knowledge space, where modality-specific representations provide complementary evidence for completing
the reasoning process. Through this mechanism, the model dynamically integrates and selects modality-
specific information, enabling more comprehensive and structured inference. The emergent Context Unrolling
capabilities are supported not only by test-time improvements across diverse public benchmarks, including
visual understanding and visual generation tasks, but also by probing tasks such as depth estimation and
spatial reasoning. These findings suggest that native unified multimodal pretraining naturally encourages

Figure 1 Given an arbitrary task, O

### We finally introduce O

### With modality-scaled pretraining in O

Figure 2 Context Unrolling. Multi-model model benefits from multi-granularity contexts. With more fine-grained
textual specifications and visual tokens that carry strong structural signals, generation obtains significant gains. Spatial
understanding can be improved via 3D geometry and visual imagination. Monocular depth estimation can be promoted
by both textural and visual reasoning.

Table 1 Understanding with Self-Thinking. We validate the performance on an internal donwsampled benchmark.

cross-modal reasoning and externalization of world knowledge through modality-specific contexts. This ability
substantially improves inference-time reasoning quality and demonstrates the potential of unified multimodal
models as foundational reasoning systems.

A unified model should not be understood as a “multi-task container” that merely places multimodal
understanding, image/video generation, and 3D geometry behind a shared backbone. The more substantive
benefit is unified context unrolling: unification turns each capability into an atomic primitive that can be
invoked, composed, and written back into a shared workspace (context), which then conditions subsequent
computation. Under this view, tasks are not isolated endpoints; they are operators over a growing context—a
context that can include (i) fine-grained textual reasoning (chain-of-thoughts), (ii) structured intermediate
representations such as visual tokens rolled out by the model itself, and (iii) geometric cues (camera pose,
depth, and view synthesis). As the model expands this workspace, downstream predictions become better
constrained (less ambiguous), more structure-preserving, and more cross-task consistent.

### Concretely, we model inference as iterative context construction followed by context-conditioned decoding:

where x denotes the multimodal inputs, ϕt are atomic primitives (e.g., “describe,” “predict pose,” “roll out
visual tokens,” “synthesize a novel view,” “estimate depth”), and ⊕denotes context composition.
This
reframes “unification” as a mechanism that scales context—not only in length, but in structure and utility for
downstream decisions. Figure 2 presents the overall results with context unrolling, which are further unfolded
in the following content.

Here, context unrolling primarily occurs through the spontaneous “think” / CoT-style textual rollout, which
enriches the latent workspace with finer semantic decompositions before producing the final answer. The
resulting context improves compositional reasoning even when the task itself is “standard” VLM. We validate
the performance of O mni on a downsampled visual understanding benchmark. As expected in Table 1, visual
understanding can be improved with thinking context on various dimensions.

53.4
GenEval2

#### 35

#### 55

#### 34

48.0
49.2

#### 50

#### 33

#### 43.9

#### 32

#### 45

#### Score

#### Score

#### 31

#### +24.2

#### 40

#### 37.4

#### 30

#### 29

#### 35

#### 28.1

#### 28

#### 29.2

#### 30

#### 27.1

#### 27

#### 26

#### 25

Baseline
+General

#### +Long

+Long
+Visual
Contexts

Baseline
+Short

#### +Visual

+Short
+Visual

#### Thinking

#### Text

#### Text

#### Token

Context
BLINK↑
MMStar↑
MMBench-V11↑
SimpleVQA↑
AI2D↑
Chartqa↑
Docvqa↑
HallusionBench↑
Erqa↑
MMSI↑

O mni
60.8
59.4
76.2
50.4
90.2
85.5
93.5
69.6
41.5
31.5
+ thinking
61.6
66.5
77.1
51.4
92.3
88.0
94.0
71.3
44.5
32.6

2
Context Unrolling

2.1
Visual Understanding

#### Spatial Understanding

#### Monocular Depth Estimation

#### 84.2

#### 34.2

#### 84.0

#### 84.0

#### 83.9

#### 83.8

#### Delta_1

#### +7.0

#### +0.8

#### 30.1

#### 83.6

#### 83.4

#### 83.3

#### 83.2

#### 83.2

#### 83.0

#### +Textural

+Visual
Contexts
Contexts

Baseline
+Detailed

+Depth
Caption

#### +Visual

#### Contexts

#### Caption

Tokens
Contexts

Ct+1 = Ct ⊕ϕt(x, Ct),
y = ψ(x | CT ) ,
(1)

Table 2 Text-to-Image Generation on Benchmarks. GenEval-2 (left) and inhouse evaluation (right) provide a
comprehensive validation where TIFAGM measures prompt-level correctness. Atomicity is also reported to evaluate
robustness under increasing prompt compositionality. Regarding contexts, visual contexts denote the discrete visual
tokens. Short and long texts are also derived from our model itself, providing fine-grained detailed descriptions. The
oracle text is produced by Gemini-3 Pro in the zero-shot manner, plus oracle visual contexts, to see how far our
generation can go.

Visual generation particularly benefits from multi-granularity context to reduce the inherent ambiguity of
mapping language to images. From the unified context unrolling perspective, image synthesis is not an isolated
endpoint; instead, it is a context-conditioned decoding process where upstream atomic primitives (e.g., textual
reasoning and structural token rollouts) can be invoked to construct a richer workspace before pixel synthesis.

To isolate the effect of different contexts, we focus on text-to-image (T2I) generation as an analysis pretext
task, leveraging its comprehensive and standardized benchmarks. Concretely, before synthesizing an image,
O mni can optionally (i) roll out more fine-grained textual specifications (attributes, counts, relations, spatial
constraints) via text-think , and/or (ii) roll out visual tokens that carry strong structural information.
Conditioning the generator on these intermediate contexts improves prompt following, object counting, and
spatial/relational fidelity—illustrating that the unified model’s gain stems from unrolling usable contexts.

Self-Unrolling Contexts. Table 2 reports results on GenEval-2 and inhouse evaluation, where Soft TIFAGM
measures prompt-level correctness. We also report atomicity, which evaluates robustness under increasing
prompt compositionality. As highlighted by GenEval-2, T2I performance typically drops sharply as com-
positionality increases. Therefore, atomicity serves as a stress test for text following and compositional
generalization.

Following prior practices of unified models (e.g., BAGEL), we can ask the model to think before generation,
producing fine-grained textual descriptions under different token budgets. In our setup, short thinking
consumes around 100 tokens on average, while long thinking uses around 250 tokens and typically yields
richer information, including coarse structural layouts.

Overall, richer textual context consistently improves both the aggregate performance and the performance
under higher atomicity (i.e., more compositional prompts), confirming the benefit of unrolling textual context.
Moreover, using visual tokens only enhances generation across metrics, with particularly strong gains on
counting- and action/verb-related prompts, consistent with the hypothesis that visual tokens inject explicit
structural cues that are otherwise difficult to preserve through pure text conditioning. Importantly, as the
number of atomic requirements in the prompt increases (i.e., more complex descriptions), O mni retains a
moderate level of prompt-following ability, indicating improved robustness under compositional stress. Finally,
textual and visual contexts are complementary: combining text-think with visual token rollout yields the
most consistent improvements, supporting our central claim that unified models excel by composing multiple
atomic capabilities into a stronger shared context.

Oracle Contexts. While self-rollout contexts already bring significant improvements, the limited capacity of
current models can introduce noise and hallucinated details, which may cap the benefit of context unrolling.
We therefore perform oracle studies to estimate how far generation can be pushed under near-ground-truth

Context
TIFAGM
Object
Attribute
Count
Position
Verb

O mni
29.25
91.64
90.00
52.03
77.67
26.25

+ short
37.35
93.18
92.45
60.14
76.92
38.83
+ long
43.94
91.86
91.13
67.03
77.03
38.31
+ visual
48.02
94.42
92.96
66.92
79.28
53.96

+ short and visual
49.16
93.13
92.68
68.36
76.83
43.34
+ long and visual
53.44
92.34
92.32
72.98
80.23
42.81

+ oracle
52.20
95.72
87.35
67.91
91.69
43.31
+ oracle and visual
57.21
94.77
97.89
69.47
90.64
56.00

2.2
Visual Generation

Overall
Object
Attribute
Relation

0.56
0.60
0.58
0.53

0.59
0.68
0.61
0.58
0.61
0.72
0.64
0.57
0.61
0.70
0.65
0.62

0.64
0.74
0.65
0.62
0.66
0.74
0.69
0.64

0.71
0.75
0.73
0.74
0.73
0.79
0.76
0.73

Figure 3 Illustration of Context Unrolling on Spatial Understanding. Given a question about an object’s relative
position across two views, the baseline (direct prediction) and text-only chain-of-thought both fail. Augmenting the
VLM with explicit 3D textual context (relative camera pose) or 3D visual context (synthesized views under canonical
motions: up/down/left/right) enables correct prediction.

We view the rolled textual context as a form of understanding-driven prompt rewriting: it reduces uncertainty
by making high-level concepts, spatial configurations, and fine-grained appearance constraints more explicit.
To approximate an upper bound on textual contexts beyond the current computation scale, we use Gemini-3
Pro to provide higher-quality rewrites in a zero-shot manner, serving as an oracle textual context in this study.

Table 2 shows that oracle contexts yield a substantial leap in generation quality, while simultaneously exposing
the gap to current self-rollout contexts—direct evidence that unrolling context (quality and structure) is a
primary driver of performance. Notably, even when Gemini-3 Pro provides strong textual contexts, adding
self-rollout visual tokens further improves results, suggesting that (i) textual and visual contexts provide
non-redundant constraints, and (ii) structural visual tokens remain valuable as an additional context channel.
Together, these findings reinforce our thesis: the unified model improves generation by invoking and composing
atomic capabilities to construct richer, more actionable context prior to decoding.

As multimodal understanding models mature, a key question emerges: can they understand the real world in
3D? This capability, often referred to as spatial intelligence, is widely regarded as essential for physical-world
operation and embodied deployment.

### A key challenge is the mismatch between visual and textual modalities: the real world is visually redundant

Photo 1
Photo 2

Direct predict

Baseline
(w/o. thinking)

With
Thinking

Generate poses

<campose>1.041259 
0.007027 0.328047 -
0.201365 -0.271789 -
0.020875</campose>

With 3D
Textual Context

#### Bakery

Generate views

Up
Down

With 3D
Visual Context

#### Bakery

Left
Right

### contexts.

2.3
Spatial Understanding

Q: When you took photo 1, where was the black small sofa in 
relation to you?

A: On your right 
B: Behind you 
C: In front of you to the left 
D: Behind you to the left

Output: C

Text chain of thought
Thinking: 
… photo 2 shows a sofa in front …
So the sofa should in front …

Output: C

Thinking:
… the camera move right, and turn

Output: A

#### Bakery

#### left… sofa is front, so in the first image,

#### it may in my right direction .…

Thinking:
… “look right” synthetic image it 
shows the lounge chairs and the area to 
the right of the real image… The real 
image’s right side has the lounge chairs, 
which matches the “look right” 
synthetic. So the camera must have 
moved to the right…

Output: A

Table 3 Spatial Understanding Evaluation. Textural contexts denote the geometry-grounded text (e.g., camera pose
estimation results). Visual contexts refer to the novel-view synthesis results as contexts if applicable. Performances are
reported on a downsampled MMSI-Bench.

and geometrically complex, while textual reasoning is compact and abstract. Reasoning purely in freeform text
often struggles with geometric ambiguities such as viewpoint changes, foreshortening, and occlusions, limiting
performance on questions requiring consistent 3D interpretation across multiple views. Our unified context
unrolling framework addresses this gap by incorporating 3D-related capabilities—camera pose estimation,
novel view synthesis, and depth estimation—as atomic primitives that can be invoked within the reasoning
loop. To validate the effectiveness of context unrolling for spatial understanding, we select 200 questions from
the MMSI benchmark [45] that are closely related to 3D spatial reasoning as the testbed.

mni can enable a
text-think mode before answering. For spatial questions, however, the most useful intermediate signal is
often explicitly geometric. We therefore allow the model to first perform camera pose estimation from the
input views before thinking and answering. The estimated camera poses serves as a 3D textual context that
disambiguates spatial relations across images.

As shown in Table 3, injecting this geometry-grounded context improves MMSI accuracy and consistently
outperforms baselines that rely on latent, free-form text-only reasoning, indicating that explicit 3D contexts
provide actionable constraints for downstream decision making.

3D Visual Contexts: Imagination-as-Context. Beyond textual contexts, a unified model can leverage its
generative capabilities to "think with images." Before answering spatial questions, the model first synthesizes
novel views around each given observation—imagining the surrounding environment from up, down, left, and
right viewpoints, etc. This process enriches the visual context by completing a more comprehensive scene
representation, allowing the model to reason from a near-omniscient perspective rather than being limited to
the provided viewpoints. Table 3 shows that adding such NVS-derived visual contexts (+ visual contexts)
yields the strongest MMSI performance. This demonstrates that generative imagination of unseen views
provides more discriminative evidence for spatial reasoning than relying solely on the given observations.

In both settings, the critical point is that geometry estimation and generation are not auxiliary tasks evaluated
in isolation. They function as context-producing primitives, textual (pose summaries) or visual (synthesized
evidence), that are composed to scale the effective context for spatial reasoning. Figure 3 provides a concrete
qualitative example of this mechanism: while standard text-only reasoning fails due to geometric ambiguity,
our approach successfully invokes 3D primitives to construct actionable context—either by explicitly grounding
reasoning in pose data or by "imagining" intermediate visual evidence—thereby correcting the reasoning
path and guiding the model to the correct answer. Namely, the gains of unified models come from unified
context unrolling, i.e., the ability to invoke and compose heterogeneous capabilities to construct richer, more
actionable context before making a decision.

Recent feed-forward 3D models (e.g., VGGT [40]) highlight the value of multi-task training, where a strong
visual encoder which is often learned via self-supervision provides rich priors for geometry prediction. In this
section, we use the long-standing problem of monocular depth estimation to illustrate that the main gain of
unification is not simply multi-task parameter sharing, but unified context unrolling, where other capabilities
become atomic primitives that supply additional constraints to 3D Geometry.

Context
Overall Score
MSR
Motion
Positional Relationship

O mni
27.14
17.65
0.0
19.63

+ thinking
28.15
17.65
33.33
30.25
+ textural contexts
30.15
11.76
33.33
33.95
+ visual contexts
34.17
26.47
33.33
35.80

3D Textural Contexts: Geometry-as-Context. Analogous to general visual understanding, O

2.4
3D Geometry mni can think before predicting.
Here, the detailed caption means to produce general-purpose descriptions for the input image. The depth caption
focuses on the spatial cues. Visual contexts denote the proposed visual tokens that enhance the structural information.

We formulate depth estimation as depth-map generation (predicting a depth image conditioned on the input
RGB). This protocol is standard and has been explored by diffusion-based approaches (e.g., Marigold [20]).
However, purely generative formulations may lag behind state-of-the-art feed-forward regressors when used
in isolation. Our approach differs in that depth generation is embedded in a unified model that can first
construct contexts including textual and visual ones before decoding the depth map.

Textual Contexts (Depth Caption). Before estimating depth, we let the model explicitly reason about scene
geometry and produce a concise textual summary of relative spatial structure (e.g., front/back ordering,
occlusion relations, support/contact), which we term a “depth caption”. As a control, we also enable an
unrestricted think mode to produce detailed, general-purpose image captions. As shown in Table 4 that
geometry-focused textual context (the depth caption) improves depth estimation quality, whereas generic
detailed captions provide little to no benefit. This suggests that context unrolling is most effective when the
intermediate context is task-relevant and constraint-like, rather than merely verbose.

Visual Contexts (Visual Tokens). Depth estimation remains a visual prediction problem in our framework.
We therefore further augment the conditioning signal with self-rollout visual tokens, which tend to encode
structured information (objectness, layout, coarse geometry cues) more explicitly. Injecting these tokens as
visual context stabilizes the depth generation process and yields sharper, more globally consistent predictions.

We visualize depth estimation results with different contexts in Figure 4. For example, without any context,
the model fails to properly separate the plant’s leaves (the first column) and misses the ceiling lamps entirely
(the third column). Depth captions help identify these objects, but ignore the depth difference between the
left and right part of the wall, or incorrectly place the emitted light at the same depth plane as the lamp

RGB w/o. caption 
& visual tokens

+depth caption

+visual tokens

#### Figure 4 Depth Estimation with Different Contexts.

Table 4 Depth Estimation Errors. Different from traditional depth estimators, O

Context
δ1 ↑
AbsRel ↓

### O

mni
83.21%
0.2028
+ detailed caption
83.27%
0.2029
+ depth caption
83.88%
0.1988
+ visual contexts
84.01%
0.1970

Table 5 Multimodal Understanding. Performances on the standard benchmarks are reported, compared to other
approaches with similar MoE architecture, activations and inference scheme (i.e., no-thinking).

fixtures. Visual token context further corrects the geometry by distinguishing the depth difference between
the wall’s different parts and assigning illuminated areas depths similar to the background wall.

Overall, these results suggest, in a unified model, multimodal understanding and structured visual rollouts
are not auxiliary add-ons. They function as context-producing primitives that constrain and guide 3D
geometry, turning depth estimation from direct regression (I →D) into context-conditioned inference
(D = Depth(I | Ctext, Cvis)).

Our results consistently support a single conclusion across understanding, generation, 3D geometry, and 3D
spatial reasoning: the primary value of a unified model is not capability aggregation, but unified context
unrolling. Once multiple modalities and 3D operators are trained within one model, each task becomes
an atomic primitive that can be invoked to construct intermediate, task-relevant context: “text-think” for
constraint extraction, “ visual tokens” for structural scaffolding, “camera prediction” and “novel view synthesis”
for geometry-grounded verification. The final prediction is thus better viewed as context-conditioned inference
rather than a direct mapping.

While our experiments focus on supervised/standard evaluations, unified context unrolling also suggests a
plausible interaction with post-training (e.g., RL-style optimization), which we leave as future work. Intuitively,
unifying more primitives enlarges the model decision space at inference time: the system could choose whether
to answer directly or to first allocate compute to intermediate steps such as text-think, rolling out visual
tokens, predicting camera pose, or running novel view synthesis as verification. In this view, post-training
may be able to learn a policy over when and how to construct context, potentially improving robustness by
adapting the context-building strategy to input difficulty and domain shift. More broadly, these considerations
point to multimodal chain-of-thought / multimodal context construction as a promising research direction:
instead of treating intermediate reasoning as purely textual, future systems may benefit from reasoning
trajectories that interleave text, visual structure, and geometry-aware synthesis i.e., thinking with multiple
modalities to build actionable context before decoding the final output.

mni on multiple benchmarks, including multimodal
understanding, image generation (i.e., text-to-image generation, image editing), video generation (i.e., text-
to-video generation, video editing), 3D reconstruction (i.e., camera pose estimation and depth estimation).

BLINK [10]
67.7
60.4
63.0
MMStar [5]
78.4
72.0
63.8
MMBench-v11 [30]
78.4
84.8
75.3
VlmsAreBlind [34]
67.5
-
76.4
SimpleVQA [6]
52.7
-
53.3
RealWorldQA [44]
73.7
72.3
76.0
Textvqa [36]
-
80.5
81.0
AI2D [21]
85.0
86.8
91.5
Chartqa [31]
86.8
87.4
86.9
Docvqa [32]
95.0
94.2
92.8
HallusionBench [15]
61.5
53.8
70.1
MuirBench [39]
73.0
53.1
64.2
Erqa [37]
51.3
41.5
45.0
MMSI-Bench [45]
30.3
27.5
31.5
MVBench [24]
72.3
72.1
68.4
Video-MMEw/osub. [9]
74.5
68.7
67.2

2.5
Discussion

3
Evaluation

### In this section, we evaluate the performance of O

Qwen3-VL-30B-A3B-Instruct [1]
InternVL3.5-30B-A3B [42]
O mni

Table 6 Image Generation Evaluation. We validate the text-to-image and image editing on multiple open benchmarks,
compared against various expertise approaches.

Table 7 Video Generation Evaluation. We validate the text-to-video on VBench1.0, compared against various
expertise approaches.

mni is built upon an MoE architecture that usually contains more parameters yet less activations
than prior unified models, we focus our comparison on VLMs at the similar scale. We therefore include
Qwen3-VL-30B-A3B-Instruct [1] and InternVL3.5-30B-A3B [42] in our evaluation, as both are based on the
same LLM backbone (i.e., Qwen3-30A3). That said, strict one-to-one comparisons are inherently difficult,
since differences in training data, optimization recipes, compute budgets, and vision encoders can all affect
final performance. We summarize the visual understanding results in Table 5 to position our unified model
among these representative baselines. Without heavy post-training and distillation, O mni achieves comparable
performances across general VQA, chart and graph understanding, alignment, video and spatial understanding.

We mainly evaluate the proposed method from two perspectives: image generation with text-only prompt
or image-instruction pair. Current open-source image generators usually deliver two separate models for
text-to-image and editing respectively. As a unified model, O mni can naturally perform image generation and
editing tasks, depending on the modality combination of input contexts. We thus report the performances on
various benchmarks, comparing our proposed method with the expertise models.

Table 6 presents the main results on both text-to-image and image editing tasks, including GenEval2 [19],
DPG [16], LongText-EN [12], Inhouse evaluation, and GEdit [29]. Although prior approaches usually derive
expertise models that focus on different tasks respectively, O mni benefits from the MoE architecture and
task unification, achieving comparable performances with only 3B activations.

mni can also synthesize videos with various combinations of multimodal instruc-
tions. Similarly, we report the performances on general text-to-video generation and video editing on widely
used benchmarks (i.e., VBench [17] and FiVE [25].) Table 7 presents the text-to-video results on VBench
where the proposed method achieves comparable performances. However, the current O mni can only produce
videos with the resolution of 480 × 640 and the duration of 12 seconds, which is far behind the state-of-the-art
video generation expertise models. We believe these shortcomings would be weakened as further scaling up.
Meanwhile, Table 8 compares the video editing performances at the similar resolution and duration. Clearly,
our method shows the significant superiority over other approaches in instruction following.

Models
GenEval2↑
DPG↑
LongText-EN↑
LongText-CN↑
Inhouse↑

Qwen-Image [43]
30.67
88.32
94.3
94.6
55.16
Z-Image [4]
41.83
88.14
93.5
93.6
55.19
Flux [3]
34.59
83.84
60.7
0.5
49.91 mni
54.12
88.55
97.5
96.8
63.87

O mni
83.35
83.11
84.29

O

3.1
Multimodal Understanding

### Given that O

3.2
Image Generation

3.3
Video Generation

### Beyond image generation, O

Models
GEdit-Bench-EN (Full set)↑

G_SC
G_PQ
G_O

Flux-Kontext-dev [2]
7.16
7.37
6.51
Step1X-Edit-v1.1 [29]
7.66
7.35
6.97
Step1X-Edit-v1.2 [29]
7.77
7.65
7.24
Emu-3.5 [7]
8.11
7.70
7.59
Z-Image-Edit [4]
8.11
7.72
7.57
Qwen-Image-Edit [43]
8.15
7.86
7.54 mni
8.42
7.85
7.75

O

Models
Total Score↑
Quality Score↑
Semantic Score↑
Wan2.1 [38]
83.69
85.59
76.11
Hunyuan Video [22]
83.43
85.07
76.88

TokenFlow [13]
35.62
19.06
263.61
72.51
26.46
21.15
89.00
19.36
35.51
36.68
18.18
27.43
DMT [47]
85.95
14.71
404.60
51.64
26.66
21.44
82.30
34.78
62.06
62.98
33.86
48.42
VidToMe [26]
22.37
21.15
263.91
70.69
26.84
21.05
90.06
20.03
33.50
36.20
17.34
26.77
AnyV2V [23]
71.36
15.90
348.59
50.77
24.89
19.72
60.36
30.62
45.42
48.96
27.09
38.02
VideoGrain [46]
12.40
27.05
185.21
79.13
25.69
20.31
88.57
30.50
43.97
44.30
30.17
37.23
Pyramid-Edit [25]
28.65
20.84
276.59
71.72
26.82
20.20
80.59
33.67
54.01
56.36
31.31
43.84
Wan-Edit [25]
12.53
25.57
94.61
82.55
26.39
21.23
89.43
41.41
52.53
55.72
38.22
46.97

As recent feedforward models (i.e., VGGT) have already demonstrated the effectiveness of unifying multiple
3D tasks, O mni also supports typical tasks in 3D vision: camera pose estimation and monocular depth
estimation, which together define 3D correspondences. We therefore compare against the expertise model in
the 3D field to anchor the capability of unified models.

Camera Pose Estimation. As shown in Table 9, we evaluate our method on camera pose estimation against
Flare, Cut3r, and VGGT on the RealEstate10K and CO3Dv2 datasets. On RealEstate10K, our method
achieves state-of-the-art performance, surpassing all baselines across all three metrics. On the object-centric
CO3Dv2 benchmark, our approach secures the best result in translation error, although other metrics are not
as competitive. We attribute this discrepancy to our data collection process, which may not have sufficiently
covered object-centric scenes. Although it is challenging to make a perfectly fair comparison, these results are
significant: they demonstrate that a unified model, even without explicit 3D inductive biases and using only
text to represent camera parameters, can achieve strong performance with appropriate training data. Such
3D capability can be regarded as one built-in context, revealing the potential in spatial understanding.

Monocular Depth Estimation.
We further validate our model on the monocular depth estimation task,
with results benchmarked against specialist models on five standard datasets presented in Table 10. Our
method demonstrates remarkable zero-shot performances on multiple benchmarks. These comprehensive
results underscore our model’s strong generalization capabilities, proving it can achieve or even exceed the

#### Table 8 Video Editing Results on FiVE Benchmark [25].

Method
Structure
Background Preservation
Text Alignment
Motion
FiVE

Source Videos
0.00
∞
0.00
100.00
24.59
19.87
93.76
–
–
–
–
–

O

#### Table 9 Camera Pose Estimation on RealEstate10K and CO3Dv2.

Method
RealEstate10K
CO3Dv2

Flare [49]
84.42
0.4215
0.0532
72.23
2.1242
0.0342
Cut3r [41]
85.32
0.4023
0.0424
75.62
1.5321
0.0331
VGGT [40]
88.23
0.3886
0.0386
86.23
1.1432
0.0285

### O

#### Table 10 Monocular Depth Estimation.

Method
NYU
KITTI
SINTEL
ETH3D
DIODE

Marigold [20]
92.75
0.0781
87.87
0.1108
62.24
0.4666
97.12
0.0564
81.64
0.2266
Cut3r [41]
91.64
0.0824
86.42
0.1253
55.64
0.4723
95.34
0.0632
75.21
0.3521
DA3 giant [27]
94.78
0.0579
93.96
0.0824
66.54
0.3821
98.79
0.0324
82.69
0.2050
VGGT [40]
96.10
0.0499
94.29
0.0803
66.11
0.4551
98.35
0.0326
82.15
0.2115

O

3.4
3D Geometry

Dist.×103 ↓
PSNR↑
LPIPS×103 ↓
SSIM×102 ↑
CLIPS.↑
CLIPS.edit ↑
Fid S.×102 ↑
YN↑
MC↑
∪↑
∩↑
Acc↑ mni
34.94
22.95
217.55
73.78
26.92
21.19
84.22
62.83
81.81
84.33
60.23
72.41

AUC@30 ↑
RPE trans ↓
RPE rot ↓
AUC@30 ↑
RPE trans ↓
RPE rot ↓ mni
88.32
0.3766
0.0289
75.21
1.5955
0.0269 δ1 ↑
AbsRel↓
δ1 ↑
AbsRel↓
δ1 ↑
AbsRel↓
δ1 ↑
AbsRel↓
δ1 ↑
AbsRel↓ mni
96.22
0.0542
96.92
0.0621
74.27
0.3340
98.91
0.0312
83.83
0.2034

### performance of specialized, single-task models across a wide range of domains without task-specific fine-tuning.

We thank Shu Liu, Xuejiao Zeng, Xiaojie Li, Renfei Sun, Ashley Kim, Ruoqing Hu, Xi Lin, Liyang Liu, Xinyu
Zhang, Liang Li, Shuangye Li, Yuhong Yang, Hongxiang Hao, Heng Zhang, Zanbo Wang, Lishu Luo, Sijin
Wu, Faming Wu, Xudong Sun for their helpful contribution and discussion.

4
Acknowledgment

[1] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang
Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo, Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shutong Jiang,
Zhaohai Li, Mingsheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu,
Yang Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xuancheng
Ren, Xingzhang Ren, Sibo Song, Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng Wang, Pengfei
Wang, Qiuyue Wang, Yuxuan Wang, Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo Yang, Mingkun Yang,
Jianxin Yang, An Yang, Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng, Humen Zhong, Jingren Zhou,
Fan Zhou, Jing Zhou, Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report. arXiv preprint arXiv:2511.21631,
2025.

[2] Black Forest Labs. FLUX.1 Kontext [dev] - Open Weights for Image Editing, 2025. URL https://bfl.ai/blog/
flux-1-kontext-dev.

[3] Black Forest Labs. FLUX.2-klein-9B. https://huggingface.co/black-forest-labs/FLUX.2-klein-9B, 2026.
Hugging Face Model Card. License: FLUX Non-Commercial License.

[4] Huanqia Cai, Sihan Cao, Ruoyi Du, Peng Gao, Steven Hoi, Zhaohui Hou, Shijie Huang, Dengyang Jiang, Xin
Jin, Liangchen Li, et al. Z-image: An efficient image generation foundation model with single-stream diffusion
transformer. arXiv preprint arXiv:2511.22699, 2025.

[5] Lin Chen, Jinsong Li, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Zehui Chen, Haodong Duan, Jiaqi Wang, Yu Qiao,
Dahua Lin, et al. Are we on the right way for evaluating large vision-language models? Advances in Neural
Information Processing Systems, 37:27056–27087, 2024.

[6] Xianfu Cheng, Wei Zhang, Shiwei Zhang, Jian Yang, Xiangyuan Guan, Xianjie Wu, Xiang Li, Ge Zhang, Jiaheng
Liu, Yuying Mai, et al. Simplevqa: Multimodal factuality evaluation for multimodal large language models. In
Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 4637–4646, 2025.

[7] Yufeng Cui, Honghao Chen, Haoge Deng, Xu Huang, Xinghang Li, Jirong Liu, Yang Liu, Zhuoyan Luo, Jin-
sheng Wang, Wenxuan Wang, et al. Emu3. 5: Native multimodal models are world learners. arXiv preprint
arXiv:2510.26583, 2025.

[8] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan
Nie, Ziang Song, Guang Shi, and Haoqi Fan. Emerging properties in unified multimodal pretraining. arXiv
preprint arXiv:2505.14683, 2025.

[9] Chaoyou Fu, Yuhan Dai, Yongdong Luo, Lei Li, Shuhuai Ren, Renrui Zhang, Zihan Wang, Chenyu Zhou, Yunhang
Shen, Mengdan Zhang, et al. Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms
in video analysis. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 24108–24118,
2025.

[10] Xingyu Fu, Yushi Hu, Bangzheng Li, Yu Feng, Haoyu Wang, Xudong Lin, Dan Roth, Noah A Smith, Wei-Chiu
Ma, and Ranjay Krishna. Blink: Multimodal large language models can see but not perceive. In European
Conference on Computer Vision, pages 148–166. Springer, 2024.

[11] Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv

[12] Zigang Geng, Yibing Wang, Yeyao Ma, Chen Li, Yongming Rao, Shuyang Gu, Zhao Zhong, Qinglin Lu, Han Hu,
Xiaosong Zhang, et al. X-omni: Reinforcement learning makes discrete autoregressive image generative models
great again. arXiv preprint arXiv:2507.22058, 2025.

[13] Michal Geyer, Omer Bar-Tal, Shai Bagon, and Tali Dekel. Tokenflow: Consistent diffusion features for consistent
video editing. arXiv preprint arXiv:2307.10373, 2023.

[14] Biao Gong, Cheng Zou, Chuanyang Zheng, and et al. Ming-omni: A unified multimodal model for perception and
generation. arXiv preprint arXiv:2506.09344, 2025. URL https://arxiv.org/abs/2506.09344.

[15] Tianrui Guan, Fuxiao Liu, Xiyang Wu, Ruiqi Xian, Zongxia Li, Xiaoyu Liu, Xijun Wang, Lichang Chen, Furong
Huang, Yaser Yacoob, et al. Hallusionbench: an advanced diagnostic suite for entangled language hallucination
and visual illusion in large vision-language models. In Proceedings of the IEEE/CVF Conference on Computer
Vision and Pattern Recognition, pages 14375–14385, 2024.

## References

preprint arXiv:2403.05530, 2024. URL https://arxiv.org/abs/2403.05530.

Proceedings of the IEEE/CVF winter conference on applications of computer vision, pages 2200–2209, 2021.

arXiv:2402.12226, 2024. URL https://arxiv.org/abs/2402.12226.
