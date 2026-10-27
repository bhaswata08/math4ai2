# Mathematics for AI — slides

Lecture decks for the 4-day course in `syllabus-streamlined.md`. One reveal.js
deck per block, maths in KaTeX, animations rendered with Manim Community
Edition. Dark theme.

## Layout

    flake.nix, flake.lock    pinned dev shell: manim (tests skipped, see flake), node, ffmpeg, chromium
    package.json             reveal.js, chalkboard plugin, katex, fonts (vendored through node_modules, no CDN)
    shared/
      css/custom.css         theme tokens and slide archetypes, shared by every deck
      js/                    deck loader, video playback, interactive figures
      build.mjs              node shared/build.mjs decks/<deck>  ->  decks/<deck>/deck.html
      serve.mjs              node shared/serve.mjs  ->  http://localhost:8000/decks/<deck>/
      anim/house.py          manim house style: background, colour roles, font floor
      anim/render.sh         renders one scene into a deck's assets/clips/
    decks/<block>-<name>/    one deck per syllabus block, e.g. decks/1.1-vectors
      index.html, deck.json  deck.json holds the title and the running order of sections
      sections/NN-name.html  one file per act
      assets/clips/          rendered mp4 clips (and a last-frame png per clip)
    anim/<block>-<name>/     manim scene sources for that deck
    refs/3b1b/               upstream 3b1b/videos source, read only, mirrors upstream paths
    anim/footage-*.tsv       third-party video segments used as clips (deck, name, video, start, end)
    shared/cut-footage.sh    cuts those segments into decks/<deck>/assets/clips/ (videos not in repo)

## Who owns what

Several agents work in this repo at once. Linear algebra owns `decks/1.*`
and the matching `anim/` folders. The calculus agent
owns `decks/2.*` (Day 2, matrices; reassigned 2026-10-22), `decks/3.3*`,
`decks/3.4*`, `decks/4.*` and the matching `anim/` folders. The SVD agent
(assigned 2026-10-23) owns `decks/3.1*`, `anim/3.1*` and the spectral
decomposition slides in `decks/2.4-eigen/sections/03-symmetric.html`; tell the
calculus agent before touching any other 2.x file. The SVD agent also owns `decks/3.2*` and `anim/3.2*` (PCA, reassigned 2026-10-27). Everything under `shared/` is common: change it only with a
note in the commit message saying why, and never rename a token or class
another deck uses.

## Colour roles

The same meaning on every slide and in every clip. Tokens live in
`shared/css/custom.css` and `shared/anim/house.py`; use the role, never a hex.

| Role | Hex | Use |
|---|---|---|
| background | `#12151b` | slide and clip background, identical so clips have no frame |
| v / first given | `#6fd0c0` teal | the first input vector or function |
| w / second given | `#c792ea` violet | the second input |
| result | `#f0a35e` amber | anything derived: sums, scaled vectors, gradients, projections |
| x component | `#8bd17c` green | x parts, x-axis motion |
| y component | `#e8798a` rose | y parts, y-axis motion |
| structure / highlight | `#ffd166` gold | act tags, list markers, emphasis on slides; momentary emphasis in clips |
| mistake | `#ff6b6b` red | common mistakes, "what goes wrong" (slides only) |

## Manim

    shared/anim/render.sh anim/1.1-vectors/addition.py AdditionTipToTail decks/1.1-vectors -ql   # draft
    shared/anim/render.sh anim/1.1-vectors/addition.py AdditionTipToTail decks/1.1-vectors       # final, 1080p30

Scene files start with `from shared.anim.house import *`. Clips are 10-30
seconds, one idea each; split a long upstream scene into several. Every
MathTex/Text has `font_size >= 40` (a clip shows at about 0.57x on the slide).
No Pi creatures. A port of 3b1b code names the upstream file in its header
(source files only; on slides, credit goes on the Credits slide):
"Adapted from 3b1b/videos <path>, (c) 3Blue1Brown, CC BY-NC-SA 4.0".

## Licence

Decks are CC BY-NC-SA 4.0 and credit Grant Sanderson wherever 3b1b material is
used. CDAC cleared CC BY-NC for this programme, and reuse of 3b1b/videos was
cleared (recorded in ../math4ai, commit 705f222).

## Decks

    node shared/serve.mjs 8123                     # then open http://localhost:8123/decks/1.1-vectors/
    node shared/build.mjs decks/1.1-vectors        # single self-contained deck.html, clips inlined
    shared/shot.sh http://localhost:8123/decks/1.1-vectors/ <out-dir> 0 3 7   # screenshots of #/0, #/3, #/7

A deck is `index.html` (identical boilerplate in every deck), `deck.json`
(title, section order, optional per-deck scripts) and `sections/`. Shared CSS
and JS are listed once, in `shared/manifest.json`, which both the editing view
and the build read.

Slide types (classes in `shared/css/custom.css`): `title-slide`, `act-open`,
`act-body` (with `act-tag`), `clip-slide`. Maths is KaTeX with `\( \)` inline
and `$$ $$` display; single `$` is not maths.

A clip slide is a `<video class="clip" src="assets/clips/X.mp4">` plus one
invisible `<span class="fragment clip-play"></span>`: "next" plays the clip,
"next" again moves on, going back rewinds. See `shared/js/clips.js`.

Interactive figures: `<div data-fig="name">` in a section, and a deck script
(listed under `scripts` in deck.json) that calls `Figures.register(name, mount)`.
`shared/js/plane.js` gives a coordinate plane with arrows, dashed segments,
KaTeX labels and draggable handles. Colours come from `role('v')` etc.

Annotation (reveal.js-plugins chalkboard, set up in `shared/js/deck.js`): `C`
draws on the slide, `B` opens a blank chalkboard, `X`/`Y` change colour, `DEL`
clears the current slide, `D` downloads the drawings as JSON. `B` no longer
blacks out the screen; `.` still does. Drawings persist across a reload in the
same browser tab.

On a tablet with no keyboard, tap the small pen tab on the left edge. It opens
a toolbar with previous, next, pen, board and clear; turning the pen or board
off closes it again. Use the toolbar's previous and next while the pen is on,
because the drawing layer takes swipes and covers reveal's arrows. Closed, the
tab sits in the margin strip the slide never reaches, so it hides nothing.

## House rules for content

- Practice and check slides: show a worked solution for the **first problem
  only**, revealed as a fragment right after it. Never show answers to the
  other problems, on the slide or anywhere else in the deck. Students do those.
- Attribution lives on **slide 2 only**, a Credits slide (`ul.credits`): video
  and scene sources, papers behind any example, tools, and the deck licence.
  No credit or citation lines on individual slides. A caveat such as
  "illustrative values" is not attribution and stays on its slide.
- Slide 1 carries the presenter: "Presented by Bhaswata Choudhury, Design Engineer,
  C-DAC Bangalore, AI-Team". No licence blurb on the Credits slide.
- The C-DAC logo sits top right on every slide, from CSS (`section::after` in
  `shared/css/custom.css`); do not add logo markup to sections.
