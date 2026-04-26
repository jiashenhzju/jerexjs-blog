import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";

export async function GET(context: APIContext) {
  const papers = (await getCollection("papers"))
    .filter((p) => !p.data.draft)
    .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());

  return rss({
    title: "JerexJs Blog",
    description: "Research reading log.",
    site: context.site ?? "http://localhost:4321/",
    items: papers.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.summary ?? "",
      link: `/papers/${p.id}`,
      categories: p.data.tags,
    })),
  });
}
