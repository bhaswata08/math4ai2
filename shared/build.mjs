// Compiles one deck into a single self-contained HTML file.
//
//   node shared/build.mjs decks/1.1-vectors      # writes decks/1.1-vectors/deck.html
//
// The result opens from disk with no server and no network: every
// stylesheet, font, script, section, image and clip is inlined. Never edit
// deck.html by hand; edit the sections and rebuild.
//
// The shared CSS and JS come from shared/manifest.json, the same list the
// editing bootstrap (shared/js/dev.js) loads, so the two modes cannot drift.

import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const DECK = resolve(process.argv[2] ?? '');
const cfg = JSON.parse(await readFile(join(DECK, 'deck.json'), 'utf8'));
const manifest = JSON.parse(await readFile(join(ROOT, 'shared/manifest.json'), 'utf8'));

const MIME = {
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', svg: 'image/svg+xml',
  gif: 'image/gif', mp4: 'video/mp4', woff2: 'font/woff2',
};
const dataUri = async (file) => {
  const ext = file.split('.').pop().toLowerCase();
  if (!MIME[ext]) throw new Error(`no mime type for ${file}; add it to MIME in shared/build.mjs`);
  return `data:${MIME[ext]};base64,${(await readFile(file)).toString('base64')}`;
};

// Inline a stylesheet's fonts and images. Only woff2 is kept: every browser that runs
// reveal reads it, and the woff/ttf fallbacks would double the file.
async function inlineCss(rel) {
  const file = join(ROOT, rel);
  let css = await readFile(file, 'utf8');
  css = css.replace(/,\s*url\([^)]*\.(woff|ttf)\)\s*format\(['"][a-z]+['"]\)/g, '');
  const urls = [...new Set([...css.matchAll(/url\((['"]?)([^)'"]+\.(?:woff2|png|svg))\1\)/g)].map((m) => m[2]))];
  for (const u of urls) css = css.split(u).join(await dataUri(join(dirname(file), u)));
  return css;
}

// Escape the one sequence that would end an inline <script> early.
const script = (src) => `<script>\n${src.replace(/<\/script/gi, '<\\/script')}\n</script>`;

const css = [];
for (const rel of manifest.css) css.push(await inlineCss(rel));

let slides = '';
for (const file of cfg.sections) {
  slides += `\n<!-- ===== ${file} ===== -->\n` + (await readFile(join(DECK, 'sections', file), 'utf8'));
}
// Drop author comments (and commented-out slides) so their clips are not inlined.
slides = slides.replace(/<!--(?! =====)[\s\S]*?-->/g, '');
const media = [...new Set([...slides.matchAll(/(?:src|poster)="((?:assets|\.\.\/\.\.\/shared\/assets)\/[^"]+)"/g)].map((m) => m[1]))];
for (const src of media) slides = slides.split(`"${src}"`).join(`"${await dataUri(join(DECK, src))}"`);

// The chalkboard plugin finds its images (chalk cursors, sponge, board texture)
// next to its own script URL. An inline script has no URL, so inline them.
async function inlineJs(rel) {
  let js = await readFile(join(ROOT, rel), 'utf8');
  const imgs = [...new Set([...js.matchAll(/path \+ '(img\/[\w-]+\.png)'/g)].map((m) => m[1]))];
  for (const img of imgs) js = js.split(`path + '${img}'`).join(JSON.stringify(await dataUri(join(ROOT, dirname(rel), img))));
  return js;
}

const scripts = [];
for (const rel of manifest.js) scripts.push(script(await inlineJs(rel)));
for (const rel of cfg.scripts ?? []) scripts.push(script(await readFile(join(DECK, rel), 'utf8')));
scripts.push(script(`window.DECK = ${JSON.stringify(cfg)};`));
scripts.push(script(await readFile(join(ROOT, manifest.boot), 'utf8')));

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${cfg.title}</title>
<!-- Built by shared/build.mjs. Do not edit: edit sections/*.html and rebuild. -->
<style>
${css.join('\n')}
</style>
</head>
<body>
<div class="reveal">
  <div class="slides">
${slides}
  </div>
</div>
${scripts.join('\n')}
</body>
</html>
`;

const out = join(DECK, 'deck.html');
await writeFile(out, html);
const mb = (Buffer.byteLength(html) / 1024 / 1024).toFixed(2);
console.log(`${out}: ${cfg.sections.length} sections, ${(slides.match(/<section/g) || []).length} slides, ${mb} MB`);
