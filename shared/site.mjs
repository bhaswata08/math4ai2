// Builds every deck and assembles a static site with a landing page.
//
//   node shared/site.mjs            # writes site/
//   python -m http.server -d site   # or any static host
//
// Each block becomes site/<block>/index.html (the self-contained deck.html), so
// every deck loads on its own. The landing page lists blocks by day, in order.

import { execFileSync } from 'node:child_process';
import { copyFile, mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';

const ROOT = dirname(import.meta.dirname);
const OUT = join(ROOT, 'site');
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

const blocks = [];
for (const e of await readdir(join(ROOT, 'decks'), { withFileTypes: true })) {
  if (!e.isDirectory() || !/^\d+\.\d+-/.test(e.name)) continue;
  const dir = join(ROOT, 'decks', e.name);
  const cfg = JSON.parse(await readFile(join(dir, 'deck.json'), 'utf8'));
  blocks.push({ name: e.name, dir, num: e.name.split('-')[0], title: cfg.title.split(' · ')[0] });
}
const key = (b) => b.num.split('.').map(Number);
blocks.sort((a, b) => key(a)[0] - key(b)[0] || key(a)[1] - key(b)[1]);

await rm(OUT, { recursive: true, force: true });
for (const b of blocks) {
  execFileSync('node', [join(ROOT, 'shared/build.mjs'), b.dir], { stdio: 'inherit' });
  await mkdir(join(OUT, b.name), { recursive: true });
  await copyFile(join(b.dir, 'deck.html'), join(OUT, b.name, 'index.html'));
}

const days = Map.groupBy(blocks, (b) => key(b)[0]);
const body = [...days].map(([day, bs]) => `
  <h2>Day ${day}</h2>
  <ol>${bs.map((b) => `
    <li><a href="${b.name}/"><span class="n">${esc(b.num)}</span>${esc(b.title)}</a></li>`).join('')}
  </ol>`).join('');

await writeFile(join(OUT, 'index.html'), `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mathematics for AI</title>
<!-- Built by shared/site.mjs. Do not edit. -->
<style>
  :root { color-scheme: light dark; --fg: #1a1a1a; --bg: #fafafa; --mut: #666; --acc: #1f5fbf; --line: #ddd; }
  @media (prefers-color-scheme: dark) { :root { --fg: #eee; --bg: #151515; --mut: #999; --acc: #7ab0ff; --line: #333; } }
  body { font: 18px/1.5 system-ui, sans-serif; color: var(--fg); background: var(--bg); max-width: 40rem; margin: 3rem auto; padding: 0 1rem; }
  h1 { margin-bottom: .25rem; }
  h2 { font-size: 1rem; text-transform: uppercase; letter-spacing: .08em; color: var(--mut); margin: 2rem 0 .5rem; }
  ol { list-style: none; padding: 0; margin: 0; border-top: 1px solid var(--line); }
  li { border-bottom: 1px solid var(--line); }
  a { display: block; padding: .6rem .25rem; color: var(--acc); text-decoration: none; }
  a:hover { background: color-mix(in srgb, var(--acc) 10%, transparent); }
  .n { display: inline-block; width: 3rem; color: var(--mut); font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<h1>Mathematics for AI</h1>
<p>Open a block to start its slides. Press <kbd>Esc</kbd> inside a deck for the overview.</p>${body}
</body>
</html>
`);
console.log(`site/: ${blocks.length} decks`);
