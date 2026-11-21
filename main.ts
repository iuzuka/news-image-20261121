// Entry program for the 21 November 2026 news image.
//
// The front page is composed by draw_news21.py and shipped beside this
// file as entry.png. The grader runs this program with no network, so all
// it does is place that finished image at the output path the harness
// asks for. Running it twice writes the same bytes both times, because
// the file it copies never changes. Standard library only.
import { copyFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
