// Starts a deck. Runs last, after reveal, KaTeX, plane.js, clips.js and the
// deck's own figure scripts have loaded.
//
// window.DECK is the deck's deck.json. In editing mode (dev.js) the sections
// are fetched here; in the built deck.html they are already in the page.
(async () => {
  const cfg = window.DECK;
  const slides = document.querySelector('.reveal .slides');
  document.title = cfg.title;

  if (!slides.children.length) {
    for (const file of cfg.sections) {
      const res = await fetch('sections/' + file);
      if (!res.ok) { console.error('could not load sections/' + file, res.status); continue; }
      const holder = document.createElement('div');
      holder.innerHTML = await res.text();
      for (const node of [...holder.children]) slides.appendChild(node);
    }
  }

  // Only \( \) and $$ $$. Single dollars are left alone so prices and shell
  // snippets never turn into maths by accident.
  renderMathInElement(slides, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '\\(', right: '\\)', display: false },
    ],
    throwOnError: false,
    errorColor: '#ff6b6b',
  });

  Figures.mountAll(slides);

  await Reveal.initialize({
    width: 1280,
    height: 720,
    // Every section owns its own vertical layout as a full height flex column.
    // Reveal's centring fights that and leaves a dead band.
    center: false,
    margin: 0.04,
    minScale: 0.2,
    maxScale: 2.0,
    // Written directly, not through the History API, so #/12 works on file://.
    hash: true,
    slideNumber: 'c/t',
    transition: 'fade',
    transitionSpeed: 'fast',
  });

  Clips.attach(Reveal);
})();
