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
    const blockString =
      typeof page["lines"][0] === "string"
        ? page["lines"].join("\n") // linesが文字列の配列の場合
        : page["lines"].map((line: { text: string }) => line.text).join("\n"); // linesがオブジェクトの場合

    const blocks = parse(blockString);
    const obsidianPage = blocks
      .map((block: unknown) => convertScrapboxToObsidian(block, 0, projectName))
      .join("\n");

    const title = page["title"];
    if (title === "2020-01-16") {
      continue;
    }
    const quotedTitle = title.replace(/\//gi, "-");
    const obsidianPagePath = `${outdir}/${quotedTitle}.md`;

    // YAMLで使用するためにタイトルをエスケープ
    const escapeYamlString = (str: string): string => {
      if (str.includes('"')) {
        // ダブルクォートを含む場合はシングルクォートで囲み、シングルクォートをエスケープ
        return `'${str.replace(/'/g, "''")}'`;
      } else {
        // それ以外はダブルクォートで囲み、ダブルクォートをエスケープ
        return `"${str.replace(/"/g, '\\"')}"`;
      }
    };

    const title_for_quartz = escapeYamlString(title);

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
