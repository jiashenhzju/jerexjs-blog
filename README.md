# JerexJs Blog

> 个人研究阅读日志 —— 用中英双语精读 AI / CV / Graphics 论文，托管在 GitHub Pages。

[![Deploy to GitHub Pages](https://github.com/<your-username>/jerexjs-blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/<your-username>/jerexjs-blog/actions/workflows/deploy.yml)

基于 [Astro](https://astro.build) + Tailwind 的极简静态站点。暖米白底色、衬线/无衬线混排、专门用于沉淀论文阅读笔记。每篇笔记是一段双语对照的精读 + 独立分析 + 内嵌图表。

线上预览：`https://<your-username>.github.io/jerexjs-blog/`（请把 `<your-username>` 换成你自己的 GitHub 用户名）

---

## 特性

- **双语对照**：英文段落与中文翻译交替排版，配合 KaTeX 公式渲染。
- **图表内联**：每篇笔记的图、表都被抽出来作为 PNG 放在同名子目录里，markdown 直接引用，不依赖外链。
- **PDF 镜像**：原 PDF 拷贝到 `public/papers/`，在文章页可对照阅读。
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
│   └── papers/                # 原始 PDF 镜像（被文章 frontmatter 的 pdf 字段引用）
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
git clone https://github.com/<your-username>/jerexjs-blog.git
cd jerexjs-blog
npm install

ASTRO_TELEMETRY_DISABLED=1 npm run dev      # http://localhost:4321/jerexjs-blog
ASTRO_TELEMETRY_DISABLED=1 npm run build    # 输出到 dist/
ASTRO_TELEMETRY_DISABLED=1 npm run preview  # 本地预览构建产物
```

> `ASTRO_TELEMETRY_DISABLED=1` 是关掉 Astro 的匿名遥测，可选。

---

## 新增一篇笔记

每篇笔记 = 一个 markdown 文件 + 同名子目录（放图）。

```
src/content/papers/MyPaper_2604.md
src/content/papers/MyPaper_2604/
└── images/
    ├── fig_01.png
    ├── fig_02.png
    └── tab_01.png
```

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
pdf: "papers/MyPaper_2604.pdf"      # 可选；放在 public/papers/ 下
date: 2026-04-26
summary: "一句话讲清楚论文做了什么。"
tags:
  - "image-generation"
rating: 4                            # 0–5，可选
status: done                         # reading | done | skimmed | draft
---
```

完整 schema 见 [`src/content.config.ts`](./src/content.config.ts)。任何字段类型不匹配，`npm run build` 都会报错。

> **推荐用 [`paper-reading`](https://github.com/<your-username>/jerexjs-blog#paper-reading-skill) skill 自动生成**：它会按本仓库的 frontmatter 规范输出双语精读 + 自动抽图 + PDF 镜像，开箱即用。

### 写作约定

- 标题层级：H2 用于一级章节（Summary / Highlights / 深度思考 / Bilingual Full Text），H3 用于子节。
- 双语段落：英文原段在前、中文译文在后，交替排列，便于对照。
- 公式用 `$...$` / `$$...$$`，会经 `remark-math` + `rehype-katex` 渲染。
- 图、表统一用 `![](./MyPaper_2604/images/fig_01.png)` 相对引用。

---

## 部署到 GitHub Pages

仓库已经包含 `.github/workflows/deploy.yml`，**无需任何 CI 配置**，按下面步骤推上去就会自动部署。

### 1. 改 `astro.config.mjs`

把 `site` 和 `base` 换成你自己的：

```ts
// astro.config.mjs
export default defineConfig({
  site: "https://<your-username>.github.io",
  base: "/jerexjs-blog",   // 必须和 GitHub 仓库名完全一致
  ...
});
```

> 如果你把仓库名改成 `<your-username>.github.io`（用户/组织主页），`base` 改成 `"/"`。

### 2. 推到 GitHub（首次）

```bash
cd jerexjs-blog
git init
git add .
git commit -m "Initial commit: JerexJs Blog"
git branch -M main
git remote add origin https://github.com/<your-username>/jerexjs-blog.git
git push -u origin main
```

### 3. 在 GitHub 启用 Pages

- 进仓库 → **Settings → Pages**
- **Source** 选 **GitHub Actions**（不是 Deploy from a branch）

### 4. 等首次部署

- 进 **Actions** 标签页 → 看 `Deploy to GitHub Pages` 是否绿。
- 绿了之后访问 `https://<your-username>.github.io/jerexjs-blog/`。

之后每次 `git push` 到 `main`，都会自动重建 + 发布。

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

本仓库的笔记格式正好对接我自己写的 [`paper-reading`](https://docs.cursor.com/agent/skills) skill：

- 输入：本地 PDF 路径
- 输出：直接落到 `src/content/papers/<stem>.md` + `src/content/papers/<stem>/images/*.png` + `public/papers/<stem>.pdf`，frontmatter 完全符合本仓库的 schema。
- 内置：双语对照翻译、图表抽取、独立分析模板、tag 候选提示。

如果你也想给自己的 blog 接一套，可以参考 `~/.claude/skills/paper-reading/`（或 Cursor 的 `~/.cursor/skills-cursor/`）。

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
