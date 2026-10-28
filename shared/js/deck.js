// Starts a deck. Runs last, after reveal, KaTeX, plane.js, clips.js and the
// deck's own figure scripts have loaded.
//
// window.DECK is the deck's deck.json. In editing mode (dev.js) the sections
// are fetched here; in the built deck.html they are already in the page.
(async () => {
  const cfg = window.DECK;

  // On-screen annotation toolbar, for a tablet with no keyboard. Icons are
  // inline SVG drawn in currentColor, so no icon font is needed. While the pen
  // is on, its canvas swallows swipes and covers reveal's arrows, so the
  // toolbar, which sits above it, carries its own prev and next.
  const icon = (d) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;
  const tools = [
    { id: 'tool-prev', title: 'Previous', action: 'Reveal.prev()', icon: icon('<path d="M15 5l-7 7 7 7"/>') },
    { id: 'tool-next', title: 'Next', action: 'Reveal.next()', icon: icon('<path d="M9 5l7 7-7 7"/>') },
    { id: 'tool-pen', title: 'Draw on slide (C)', action: 'RevealChalkboard.toggleNotesCanvas()',
      icon: icon('<path d="M4 20l1.5-5L16 4.5l3.5 3.5L9 18.5z"/><path d="M14 6.5l3.5 3.5"/>') },
    { id: 'tool-board', title: 'Blank board (B)', action: 'RevealChalkboard.toggleChalkboard()',
      icon: icon('<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20l4-4 4 4"/>') },
    { id: 'tool-clear', title: 'Clear this slide (DEL)', action: 'RevealChalkboard.clear()',
      icon: icon('<path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/>') },
    { id: 'tool-full', title: 'Fullscreen (F)',
      action: 'document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()',
      icon: icon('<path d="M4 9V4h5"/><path d="M20 9V4h-5"/><path d="M4 15v5h5"/><path d="M20 15v5h-5"/>') },
  ];

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
    // A clip's play step is a fragment. Keep it out of the URL so #/9 and
    // #/9/0/0 do not look like two slides.
    fragmentInURL: false,
    slideNumber: 'c/t',
    // Reveal's own bar counts fragment steps, so it jumps when a clip's play
    // step fires. The bar below counts slides only.
    progress: false,
    transition: 'fade',
    transitionSpeed: 'fast',
    // C draws on the slide, B opens a blank board, X/Y change colour,
    // DEL clears this slide. Drawings survive a reload in the same tab.
    plugins: [RevealChalkboard, RevealCustomControls],
    customcontrols: {
      controls: tools,
      tooltip: 'Annotation tools',
      expandIcon: icon('<path d="M4 20l1.5-5L16 4.5l3.5 3.5L9 18.5z"/>'),
      collapseIcon: icon('<path d="M15 5l-7 7 7 7"/>'),
    },
    chalkboard: {
      storage: 'chalkboard:' + location.pathname,
      // Reveal's B (blackout) is taken by the board; "." still blacks out.
      // The plugin also binds BACKSPACE to wipe every slide: too easy to hit.
      keyBindings: { resetAll: null },
      // Pens for drawing on a slide. The plugin's first is black, invisible on
      // this background, so use the colour roles, ink first. Board chalks keep
      // the plugin's defaults.
      boardmarkers: ['--ink', '--v', '--w', '--result', '--accent', '--warn'].map((role) => ({
        color: getComputedStyle(document.documentElement).getPropertyValue(role).trim(),
        cursor: 'crosshair',
      })),
    },
  });

  Clips.attach(Reveal);

  // The toolbar starts closed, as a tab in the margin. Light up the pen or
  // board button while that mode is on, and close the toolbar when a tap
  // turns the last one off. The plugin keeps no state it exposes, so read it
  // off its two overlays.
  const toolbar = document.getElementById('customcontrols');
  toolbar.classList.add('collapsed');
  const syncTools = (e) => {
    const notes = document.getElementById('notescanvas');
    const board = document.getElementById('chalkboard');
    const boardOpen = board?.style.visibility === 'visible';
    document.getElementById('tool-board')?.classList.toggle('active', boardOpen);
    document.getElementById('tool-full')?.classList.toggle('active', !!document.fullscreenElement);
    const penOn = !boardOpen && notes?.style.pointerEvents === 'auto';
    document.getElementById('tool-pen')?.classList.toggle('active', penOn);
    if (e?.target.closest?.('#tool-pen, #tool-board') && !penOn && !boardOpen) toolbar.classList.add('collapsed');
  };
  toolbar.addEventListener('click', syncTools);
  document.addEventListener('keyup', syncTools);
  document.addEventListener('fullscreenchange', () => syncTools());

  const bar = document.createElement('div');
  bar.className = 'deck-progress';
  document.querySelector('.reveal').appendChild(bar);
  const total = Reveal.getTotalSlides();
  const update = () => {
    bar.style.width = (total > 1 ? (Reveal.getSlidePastCount() / (total - 1)) * 100 : 100) + '%';
  };
  Reveal.on('slidechanged', update);
  update();
})();
