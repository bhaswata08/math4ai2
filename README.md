# Mathematics for AI — slides

Lecture decks for the 4-day course in `syllabus-streamlined.md`. One reveal.js
deck per block, maths in KaTeX, animations rendered with Manim Community
Edition. Dark theme.

## Layout

    flake.nix, flake.lock    pinned dev shell: manim (tests skipped, see flake), node, ffmpeg, chromium
    package.json             reveal.js, katex, fonts (vendored through node_modules, no CDN)
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

## Who owns what

Two agents work in this repo at once. Linear algebra (Days 1-3.2) owns
`decks/1.*`, `decks/2.*`, `decks/3.1*`, `decks/3.2*` and the matching `anim/`
folders. Calculus owns `decks/3.3*`, `decks/3.4*`, `decks/4.*` and the matching
`anim/` folders. Everything under `shared/` is common: change it only with a
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
| highlight | `#ffd166` | momentary emphasis only |

## Manim

    shared/anim/render.sh anim/1.1-vectors/addition.py AdditionTipToTail decks/1.1-vectors -ql   # draft
    shared/anim/render.sh anim/1.1-vectors/addition.py AdditionTipToTail decks/1.1-vectors       # final, 1080p30

Scene files start with `from shared.anim.house import *`. Clips are 10-30
seconds, one idea each; split a long upstream scene into several. Every
MathTex/Text has `font_size >= 40` (a clip shows at about 0.57x on the slide).
No Pi creatures. A port of 3b1b code names the upstream file in its header:
"Adapted from 3b1b/videos <path>, (c) 3Blue1Brown, CC BY-NC-SA 4.0".

## Licence

Decks are CC BY-NC-SA 4.0 and credit Grant Sanderson wherever 3b1b material is
used. CDAC cleared CC BY-NC for this programme, and reuse of 3b1b/videos was
cleared (recorded in ../math4ai, commit 705f222).
