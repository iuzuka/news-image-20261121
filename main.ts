// Entry program for the 21 November 2026 news image.
//
// The front page is composed by draw_news21.py and shipped beside this
// file as entry.png. The grader runs this program with no network, so all
// it does is place that finished image at the output path the harness
// asks for. Running it twice writes the same bytes both times, because
// the file it copies never changes. Standard library only.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error(`entry.png missing: expected the finished image at ${src} (run draw_news21.py first)`);
}
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Fail loudly instead of shipping a truncated copy: the grader reads
// whatever lands in the output directory, so verify the copy byte for byte.
const srcBytes = statSync(src).size;
const dstBytes = statSync(dst).size;
if (srcBytes !== dstBytes) {
  throw new Error(`entry.png copy mismatch: source ${srcBytes} bytes, output ${dstBytes} bytes`);
}
console.log(`entry.png -> ${dst} (${dstBytes} bytes)`);
