// take args from command line

import { parse } from "https://deno.land/std/flags/mod.ts";
const args = parse(Deno.args);
const project = args.project ?? "villagepump";
const outfile = args.outfile ?? "./data,json";
const a_b = args["a-b"] ?? "a";
console.log(project, outfile, a_b);
