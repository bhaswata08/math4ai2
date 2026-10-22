// Editing-mode bootstrap. A deck's index.html loads only this file.
//
// It reads shared/manifest.json and the deck's own deck.json, adds the
// stylesheets, loads the scripts in order, and hands over to deck.js, which
// fetches the sections. shared/build.mjs does the same job at build time by
// inlining everything, so the shipped deck.html never runs this file.
(async () => {
  const ROOT = '../../';
  const manifest = await (await fetch(ROOT + 'shared/manifest.json')).json();
  window.DECK = await (await fetch('deck.json')).json();

  for (const href of manifest.css) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = ROOT + href;
    document.head.appendChild(link);
  }

  const load = (src) => new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = () => reject(new Error('could not load ' + src));
    document.body.appendChild(s);
  });

  for (const src of manifest.js) await load(ROOT + src);
  for (const src of window.DECK.scripts || []) await load(src);
  await load(ROOT + manifest.boot);
})();
