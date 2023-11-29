import { convertScrapboxToObsidian } from "./ScrapboxToObsidian/convert.js";
import { parse } from "https://esm.sh/@progfay/scrapbox-parser@8.1.0";
import { ensureDir } from "https://deno.land/std@0.170.0/fs/mod.ts";

const outdir = "./quartzPages"; // originally "./obsidianPages"
await ensureDir(outdir);

const filePath = Deno.args[0];
const projectName = Deno.args[1] ?? "PROJECT_NAME";
try {
  const projectFile = await Deno.readTextFile(`./${filePath}`);
  const projectJson = JSON.parse(projectFile);
  const pages = projectJson["pages"];
  for (const page of pages) {
    const blocks = parse(page["lines"].join("\n"));
    const obsidianPage = blocks
      .map((block) => convertScrapboxToObsidian(block, 0, projectName))
      .join("\n");

    const title = page["title"];
    if (title === "2020-01-16") {
      continue;
    }
    const quotedTitle = title.replace(/\//gi, "-");
    const obsidianPagePath = `${outdir}/${quotedTitle}.md`;

    const title_for_quartz = title.match(/"/) ? `'${title}'` : `"${title}"`;
    const frontmatter = `---\ntitle: ${title_for_quartz}\n---\n`;
    await Deno.writeTextFile(obsidianPagePath, frontmatter + obsidianPage);
    await Deno.utime(obsidianPagePath, new Date(), page["updated"]);
  }
} catch (error) {
  if (error instanceof Deno.errors.NotFound) {
    console.error("the file was not found");
  } else {
    throw error;
  }
}
