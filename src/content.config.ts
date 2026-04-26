import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const papers = defineCollection({
  loader: glob({
    pattern: "**/*.{md,mdx}",
    base: "./src/content/papers",
  }),
  schema: z.object({
    title: z.string(),
    titleZh: z.string().optional(),
    authors: z.array(z.string()).optional(),
    affiliations: z.array(z.string()).optional(),
    venue: z.string().optional(),
    year: z.union([z.string(), z.number()]).optional(),
    arxiv: z.string().optional(),
    projectPage: z.string().url().optional(),
    github: z.string().url().optional(),
    huggingface: z.string().url().optional(),
    pdf: z.string().optional(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    summary: z.string().optional(),
    tags: z.array(z.string()).default([]),
    rating: z.number().min(0).max(5).optional(),
    status: z
      .enum(["reading", "done", "skimmed", "draft"])
      .default("done"),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { papers };
