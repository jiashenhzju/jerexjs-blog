# JerexJs Blog

> 个人研究阅读日志 —— 用中英双语精读 AI / CV / Graphics 论文，托管在 GitHub Pages。

[![Deploy to GitHub Pages](https://github.com/jiashenhzju/jerexjs-blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/jiashenhzju/jerexjs-blog/actions/workflows/deploy.yml)

基于 [Astro](https://astro.build) + Tailwind 的极简静态站点。暖米白底色、衬线/无衬线混排、专门用于沉淀论文阅读笔记。每篇笔记是一段双语对照的精读 + 独立分析 + 内嵌图表。

线上预览：[jiashenhzju.github.io/jerexjs-blog](https://jiashenhzju.github.io/jerexjs-blog/)

---

## 特性

- **双语对照**：英文段落与中文翻译交替排版，配合 KaTeX 公式渲染。
- **图表内联**：每篇笔记的图、表都被抽出来作为 PNG 放在同名子目录里，markdown 直接引用，不依赖外链。
- **本地 PDF 加速**：大 PDF 放在 Git 忽略的 `local-papers/`，开发态通过 Range 请求按需加载；生产态自动回退 arXiv。
- **内容集合 + 类型校验**：用 Astro Content Collections + Zod schema 强约束 frontmatter，写错会在 build 时报错。
- **零运行时**：纯静态、零数据库、`npm run build` 即得 `dist/` 全量站点。
- **自动部署**：push 到 `main` 即触发 GitHub Actions，自动构建 + 发布到 GitHub Pages。

---

## 技术栈

| 层 | 选型 |
| --- | --- |
| 框架 | Astro 5 |
| 样式 | Tailwind CSS 3 |
| Markdown 增强 | `@astrojs/mdx`、`remark-math`、`rehype-katex` |
| SEO | `@astrojs/sitemap`、`@astrojs/rss` |
| 部署 | GitHub Actions → GitHub Pages |
| 包管理 | npm |
| 推荐 Node 版本 | ≥ 20 |

---

## 目录结构

```
jerexjs-blog/
├── astro.config.mjs           # site / base / markdown 插件
├── tailwind.config.mjs
├── tsconfig.json
├── public/
│   ├── favicon.svg
│   └── pdfjs/                 # 构建前生成，不提交 Git
├── local-papers/              # 本地 PDF 或软链接；不提交、不进 dist
├── src/
│   ├── content.config.ts      # papers collection 的 zod schema
│   ├── content/
│   │   └── papers/
│   │       ├── PhotoAgent_2602.md
│   │       ├── PhotoAgent_2602/
│   │       │   └── images/    # 该论文的图、表 PNG
│   │       ├── vision_banana_2604.md
│   │       └── vision_banana_2604/
│   │           └── images/
│   ├── components/            # 顶栏、卡片、目录等
│   ├── layouts/               # Page / Paper 布局
│   ├── pages/                 # 首页、tag 页、RSS、sitemap
│   ├── styles/                # 全局样式
│   └── assets/
└── .github/
    └── workflows/
        └── deploy.yml         # GitHub Pages 自动部署
```

---

## 快速上手

```bash
git clone https://github.com/jiashenhzju/jerexjs-blog.git
cd jerexjs-blog
npm install

ASTRO_TELEMETRY_DISABLED=1 npm run dev      # http://localhost:4321/jerexjs-blog
ASTRO_TELEMETRY_DISABLED=1 npm run build    # 输出到 dist/
ASTRO_TELEMETRY_DISABLED=1 npm run preview  # 本地预览构建产物
```

> `ASTRO_TELEMETRY_DISABLED=1` 是关掉 Astro 的匿名遥测，可选。

---

## 新增论文：放哪里、怎么读

### 1. 放置原始 PDF

把待处理 PDF 放到仓库根目录下、已被 Git 忽略的 `local-papers/inbox/`。不要放进 `public/`、`src/`，也不要提交到 Git。

单篇论文：

```text
local-papers/inbox/MyPaper_2604.pdf
```

一批论文可以按主题或日期建目录：

```text
local-papers/inbox/world-models-2026/
├── Paper-A.pdf
├── Paper-B.pdf
└── Paper-C.pdf
```

PDF 原本已经在下载目录、文献库或外置硬盘时，不必复制进仓库；调用 skill 时直接给它**绝对路径**即可。`paper-reading` 会在 `local-papers/` 下建立软链接，不重复占用一份空间。

> `example/MiniWorld-2608.pdf` 仅用于演示完整流程，不建议把 `example/` 当成日常论文库，因为它没有被 Git 忽略。

### 2. 在 Codex 中调用 `paper-reading`

在本项目的 Codex 任务输入框中直接发送下面的内容。推荐显式写 `$paper-reading`，并使用绝对路径，避免工作目录变化导致找不到文件。

单篇深度精读（默认模式）：

```text
$paper-reading 深度精读 /Users/you/projects/jerexjs-blog/local-papers/inbox/MyPaper_2604.pdf，生成到当前 JerexJs Blog，完成图表核对并运行 build。
```

整目录逐篇处理：

```text
$paper-reading 依次深度精读 /Users/you/projects/jerexjs-blog/local-papers/inbox/world-models-2026/ 下的所有 PDF。每篇生成独立文章；逐篇完成提取、核图和 build，遇到失败时停下并报告。
```

也可以按阅读目标切换颗粒度：

| 目标 | 调用示例 |
| --- | --- |
| 快速读懂 | `$paper-reading 快速读懂 /absolute/path/paper.pdf，只输出宏观总结、论证地图、关键证据与局限。` |
| 深度精读 | `$paper-reading 深度精读 /absolute/path/paper.pdf，并生成博客文章。` |
| 全文翻译 | `$paper-reading 全文翻译 /absolute/path/paper.pdf，按语义大段双语展示。` |
| 精读某节 | `$paper-reading 精读 /absolute/path/paper.pdf 的第 3 节，补充关键句、术语和公式分析。` |
| 翻译某节 | `$paper-reading 翻译 /absolute/path/paper.pdf 的 Related Work，尽量少做扩展分析。` |
| 论文分享 PPT | `$paper-reading 为 /absolute/path/paper.pdf 制作一份英文为主、极简 researcher 风格的论文分享 PPT。` |
| 精读 + PPT | `$paper-reading 深度精读 /absolute/path/paper.pdf，生成博客文章，并制作英文论文分享 PPT。` |

未指定模式时使用 `deep`：先给出宏观结论和论证链，再做研究者分析与正文语义分块精读，而不是逐句机械翻译。

PPT 与阅读深度是两个独立维度：可以只生成分享 PPT，也可以在精读后同时生成博客和 PPT。未指定分享场景时，默认面向相邻领域研究者、时长 15–20 分钟，按“问题压力 → 核心洞见 → 方法机制 → 关键证据 → 成本与边界 → Takeaways & Discussion”组织 8–14 页；画面文字以英文为主，原论文图表作为主要视觉证据。

### 3. 生成产物

每篇论文会生成一个 Markdown 文件和同名资源目录：

```
src/content/papers/MyPaper_2604.md
src/content/papers/MyPaper_2604/
├── paper.raw.json             # 带版面信息的抽取结果
├── paper.raw.md               # 便于检查的原始文本
└── images/
    ├── fig_01.png
    └── fig_02.png
local-papers/MyPaper_2604.pdf  # 指向原 PDF 的本地软链接
presentations/MyPaper_2604-paper-talk.pptx  # 仅在请求 PPT 时生成
```

最终发布内容是 `MyPaper_2604.md` 和其中引用的图片；原 PDF 与 `local-papers/` 不进入 GitHub Pages 部署包。

### 4. 手工新增时的 frontmatter

markdown 顶部的 frontmatter 是必需的：

```yaml
---
title: "Paper title in English"
titleZh: "中文标题"
authors:
  - "Alice"
  - "Bob"
affiliations:
  - "Google"
venue: "CVPR"
year: 2026
arxiv: "2604.12345"
projectPage: "https://..."          # 可选
github: "https://github.com/..."    # 可选
huggingface: "https://..."          # 可选
localPdf: "MyPaper_2604.pdf"        # 可选；仅本地开发使用
date: 2026-04-26
summary: "一句话讲清楚论文做了什么。"
tags:
  - "image-generation"
rating: 4                            # 0–5，可选
status: done                         # reading | done | skimmed | draft
---
```

推荐让 `paper-reading` 自动生成这些字段；手工编写时，完整 schema 见 [`src/content.config.ts`](./src/content.config.ts)。任何字段类型不匹配，`npm run build` 都会报错。

### 写作约定

- 标题层级：H2 用于一级章节（Summary / Highlights / 深度思考 / Bilingual Full Text），H3 用于子节。
- 双语段落：英文原段在前、中文译文在后，交替排列，便于对照。
- 公式用 `$...$` / `$$...$$`，会经 `remark-math` + `rehype-katex` 渲染。
- 图、表统一用 `![](./MyPaper_2604/images/fig_01.png)` 相对引用。

### 5. 大体积本地 PDF 的加载策略

PDF 不应放入 `public/`：Astro 会把它复制进 `dist/`，GitHub 仓库和部署包都会迅速膨胀。本项目采用双源策略：

```bash
mkdir -p local-papers
ln -s /absolute/path/MyPaper_2604.pdf local-papers/MyPaper_2604.pdf
```

frontmatter 设置 `localPdf: "MyPaper_2604.pdf"`，并保留 `arxiv`：

- `npm run dev`：优先走本地 PDF；开发服务器支持 HTTP Range，PDF.js 按块读取。
- `npm run build`：忽略 `local-papers/`，页面自动使用 arXiv PDF。
- 如果手工管理外置论文库，也可以在启动前设置 `PAPER_LIBRARY_DIR=/path/to/library`；此时 `localPdf` 应填写相对于该目录的路径。

---

## 部署到 GitHub Pages

当前仓库已配置为：

```ts
site: "https://jiashenhzju.github.io"
base: "/jerexjs-blog"
```

部署工作流位于 [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)，push 到 `main` 后会自动执行 `npm ci`、`npm run build` 并发布 `dist/`。

### 当前仓库首次部署

1. 在 GitHub 仓库进入 **Settings → Pages**，将 **Source** 设为 **GitHub Actions**。
2. 本地先验证，然后提交并推送：

```bash
ASTRO_TELEMETRY_DISABLED=1 npm run build
git add README.md src/content/papers
git commit -m "Add paper reading note"
git push origin main
```

3. 到 **Actions → Deploy to GitHub Pages** 查看状态。成功后访问 [jiashenhzju.github.io/jerexjs-blog](https://jiashenhzju.github.io/jerexjs-blog/)。

以后每次 push 到 `main` 都会重新部署。也可以在 Actions 页面用 `workflow_dispatch` 手动触发。

> `local-papers/` 和原始 PDF 不会被上传。线上论文页优先使用 frontmatter 的 `arxiv` 作为 PDF 来源；没有可公开访问的 `arxiv` 或 `pdf` 时，正文仍可发布，但线上不会出现原文对照入口。

### Fork 后部署到自己的仓库

把 `astro.config.mjs` 的 `site` 和 `base` 换成自己的 GitHub Pages 地址：

```ts
// astro.config.mjs
export default defineConfig({
  site: "https://<your-username>.github.io",
  base: "/jerexjs-blog",   // 必须和 GitHub 仓库名完全一致
  ...
});
```

> 如果你把仓库名改成 `<your-username>.github.io`（用户/组织主页），`base` 改成 `"/"`。

然后推到自己的 GitHub 仓库：

```bash
cd jerexjs-blog
git init
git add .
git commit -m "Initial commit: JerexJs Blog"
git branch -M main
git remote add origin https://github.com/<your-username>/jerexjs-blog.git
git push -u origin main
```

最后同样在 **Settings → Pages** 选择 **GitHub Actions**，等待首次 workflow 完成。

---

## 留言板（开放式评论）

每篇论文页底部有一个开放留言板：**无需登录，任何人都可以新增、编辑或删除任何留言**。后端是 Supabase Free Tier，前端纯静态、不引 SDK，直接用 `fetch` 调 PostgREST。

### 设置步骤

1. 去 [supabase.com](https://supabase.com) 新建一个免费项目。
2. 在项目 → SQL Editor 里执行 [`supabase/comments.sql`](./supabase/comments.sql)，会创建 `public.comments` 表 + 4 条 RLS 策略（select / insert / update / delete 全部对 `anon` 开放）。
3. 在项目 → Settings → API 拷贝 `Project URL` 和 `anon public key`。
4. 在 GitHub 仓库 → **Settings → Secrets and variables → Actions → Variables** 新建两个 **Repository variables**：
   - `PUBLIC_SUPABASE_URL` = 你的 Project URL
   - `PUBLIC_SUPABASE_ANON_KEY` = 你的 anon public key
5. push 到 `main` 触发重新部署。文章页底部就会出现「留言板」区块。

> 用 **Variables** 而不是 **Secrets**：anon key 本来就要暴露到浏览器，不算秘密；GitHub Actions 也不会把 secret 注入到带 `PUBLIC_` 前缀的 env 上。

### 本地开发

复制 [`.env.example`](./.env.example) 为 `.env`，填入同样两个变量。Astro dev server 会自动读取 `.env`。没有这两个变量时，留言板区块会渲染一个「未配置」提示，不会报错。

### 安全提醒

这是设计成**完全开放**的 —— 任何访问者都能改/删任何留言，相当于一块公共白板。如果不想要这种语义：

- 想要只能本人编辑：在 SQL 里把 update/delete policy 改成检查某个客户端生成的 `edit_token`（写入时存 hash，编辑时验证）。
- 想要审核制：加一个 `approved boolean default false`，select policy 改为 `using (approved)`，靠你自己手工在 dashboard 里 approve。
- 想要防垃圾：上 [hCaptcha](https://www.hcaptcha.com/) 或 Cloudflare Turnstile 做客户端校验。

---

## paper-reading skill

本仓库保存了一份可维护的 skill 源码：`example/paper-reading/`；当前机器安装后的路径是 `~/.codex/skills/paper-reading/`。

- 输入：本地 PDF 路径
- 输出：可选博客笔记、抽取产物、图表、本地 PDF 软链接，以及 `presentations/<stem>-paper-talk.pptx`
- 内置：宏观总结、论证地图、证据核验、独立分析、语义分块双语精读、英文极简论文分享 PPT、frontmatter/构建与幻灯片渲染验收

首次在其他机器使用时，先复制到个人 skill 目录：

```bash
mkdir -p ~/.codex/skills/paper-reading
cp -R example/paper-reading/. ~/.codex/skills/paper-reading/
```

重新打开 Codex 任务后，在输入框中使用 `$paper-reading` 调用：

```text
$paper-reading 请精读 /absolute/path/paper.pdf，生成到当前 JerexJs Blog 并跑完验证。
```

只制作论文分享 PPT：

```text
$paper-reading 为 /absolute/path/paper.pdf 制作一份英文为主、极简 researcher 风格的论文分享 PPT，讲清楚核心方法、关键证据与局限，并完成逐页渲染检查。
```

精读后同时生成博客与 PPT：

```text
$paper-reading 深度精读 /absolute/path/paper.pdf，生成到当前 JerexJs Blog；再制作一份 15 分钟英文论文分享 PPT，并分别完成 build 与幻灯片 QA。
```

自然语言也会自动触发，例如：

```text
帮我精读 /Users/you/projects/jerexjs-blog/example/MiniWorld-2608.pdf，生成双语论文笔记。
```

修改 skill 时以 `example/paper-reading/` 为源文件，校验通过后再同步安装：

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py example/paper-reading
cp -R example/paper-reading/. ~/.codex/skills/paper-reading/
```

详细的论文放置、单篇/批量调用方式见上文“新增论文：放哪里、怎么读”。

---

## 常见问题

**Q：本地预览 404？**
A：`base: "/jerexjs-blog"` 设置后，dev server 的根路径是 `http://localhost:4321/jerexjs-blog/`，不是 `localhost:4321/`。

**Q：图片在 GitHub Pages 上 404？**
A：确认图片路径是相对路径（`./MyPaper/images/foo.png`）而不是绝对路径（`/images/foo.png`）。绝对路径在 `base != "/"` 时会拼错。

**Q：Build 报 `Invalid frontmatter`？**
A：照着 [`src/content.config.ts`](./src/content.config.ts) 的 zod schema 对一遍 —— 多半是 `tags` 写成了字符串而不是数组，或者 `date` 缺失。

**Q：能不能用 pnpm / yarn？**
A：可以，但 `deploy.yml` 是用 `npm ci`，要换的话同步改 workflow。

---

## License

文章版权归本人所有；模板代码（`src/components/`、`src/layouts/`、`astro.config.mjs` 等）以 [MIT](./LICENSE) 开源，欢迎 fork 自建。

如果觉得有帮助，欢迎 star 或在你的 blog footer 里挂个链接。
