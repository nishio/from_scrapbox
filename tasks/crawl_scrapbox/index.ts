// Derived from [scrapbox-external-backup]:
// https://github.com/meganii/sandbox-github-actions-scheduler/blob/main/index.ts

import { readableStreamFromIterable } from "https://deno.land/std@0.166.0/streams/mod.ts";
import { JsonStringifyStream } from "https://deno.land/std@0.166.0/encoding/json/stream.ts";
import { parse } from "https://deno.land/std/flags/mod.ts";
import { ensureDir } from "https://deno.land/std/fs/mod.ts";

interface TitlePage {
  id: string;
  title: string;
  created: number;
  updated: number;
}

const args = parse(Deno.args);
const project = args.project ?? "villagepump";
const dist_data = `./crawl_data/${project}.jsonl`;
const dist_stats = `./crawl_data/${project}/stat_pages.json`;
ensureDir(`./crawl_data/${project}`);

const pagesResponse = await fetch(
  `https://scrapbox.io/api/pages/${project}/?limit=1`
);
const pageNum = (await pagesResponse.json()).count;
if (pageNum === undefined) {
  Deno.exit(0);
}

const limitParam = 1000;
const maxIndex = Math.floor(pageNum / 1000) + 1;

const pages: any[] = [];
const promises = [...Array(maxIndex)].map(async (_, index) => {
  const json = await fetch(
    `https://scrapbox.io/api/pages/${project}/?limit=${limitParam}&skip=${
      index * 1000
    }`
  ).then((res) => res.json());
  pages.push(...json.pages);
});
await Promise.all(promises);

const titles = pages.map((page) => {
  return {
    id: page.id,
    title: page.title,
    created: page.created,
    updated: page.updated,
    image: page.image,
    descriptions: page.descriptions,
  } as TitlePage;
});
titles.sort((a: TitlePage, b: TitlePage): number => {
  return a.created - b.created;
});

writeJson(dist_stats, {
  projectName: project,
  count: pageNum,
  pages: titles,
});

const skip = 100;
const detailPages: Array<Object> = [];
// skip件づつfetchする
for (let i = 0; i < titles.length; i += skip) {
  console.log(
    `[scrapbox-external-backup] Start fetching ${i} - ${i + skip} pages.`
  );
  // 一気にAPIを叩いてページ情報を取得する
  const promises = titles
    .slice(i, i + skip)
    .map(async (pageTitle: TitlePage, j: number) => {
      console.log(
        `[page ${i + j}@scrapbox-external-backup] start fetching "/${project}/${
          pageTitle.title
        }"`
      );
      const res = await fetch(
        `https://scrapbox.io/api/pages/${project}/${encodeURIComponent(
          pageTitle.title
        )}`
      );
      console.log(
        `[page ${
          i + j
        }@scrapbox-external-backup] finish fetching "/${project}/${
          pageTitle.title
        }"`
      );
      detailPages.push(await res.json());
    });
  await Promise.all(promises);
  console.log(`Finish fetching ${i} - ${i + skip} pages.`);
}

// JSON Lines形式でpagesを出力 - 出力処理後JSON形式に変換が必要
const file = await Deno.open(dist_data, { create: true, write: true });
readableStreamFromIterable(detailPages)
  .pipeThrough(new JsonStringifyStream({ suffix: "\n" })) // convert to JSON Text Sequences
  .pipeThrough(new TextEncoderStream()) // convert a string to a Uint8Array
  .pipeTo(file.writable)
  .then(() => console.log("write success"));

function writeJson(path: string, data: object): string {
  try {
    Deno.writeTextFileSync(path, JSON.stringify(data));

    return "Written to " + path;
  } catch (e) {
    return e.message;
  }
}
