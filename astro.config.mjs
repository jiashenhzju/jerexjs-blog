import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import { localPdfDevServer } from "./scripts/local-pdf-dev-server.mjs";

// To deploy on GitHub Pages, set the following two values:
//   site: "https://<your-username>.github.io"
//   base: "/jerexjs-blog"   (the repo name)
// If you publish under <username>.github.io (a user/organization site), use base: "/".
export default defineConfig({
  site: "https://jiashenhzju.github.io",
  base: "/jerexjs-blog",
  trailingSlash: "ignore",
  integrations: [tailwind({ applyBaseStyles: false }), mdx(), sitemap()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      theme: "github-light",
      wrap: true,
    },
  },
  vite: {
    plugins: [localPdfDevServer({ base: "/jerexjs-blog" })],
    server: {
      fs: { strict: false },
    },
  },
});
