# Continuation: 4.3 gradient descent on a 3D loss surface

Written 2026-11-02. Pick this up on the office machine.

## The standing instruction

Every loss picture in Block 4.3 shows the loss as a **3D surface**, never as a
2D contour map. The user rejected the contour look twice. Block 4.2's
`ConvexAlongEveryLine` is the reference for how a surface should look: a mesh
in `V_COLOR` with alternating face opacity, axes coloured `X_COLOR` / `Y_COLOR`,
and every label fixed in the frame by projecting with
`self.camera.project_point`.

## Done

**4.2 `anim/4.2-shape/curvature.py`, scene `ConvexAlongEveryLine`** (rendered at
1080p, in the deck): rewritten from two flat 2D parabola panels to a
`ThreeDScene`. The surface is drawn as a disc, not a square patch, because the
corners of a square patch of `x^2 + y^2` reach `f = 2R^2` and run off the top
of the frame. The x slice is green, the y slice rose, the chord amber, and each
panel label names its direction ("along x", "along y").

**4.2 `decks/4.2-shape/sections/03-critical.html`**: the crammed "Solve ∇f = 0"
slide is now four slides, one per step (partials, solve, Hessian, classify).

**4.3 `anim/4.3-gd/valley.py`**: rewritten onto the 3D bowl. New shared pieces
near the top of the file:

- `L_MAX = 12.0`, the level set the surface is drawn out to.
- `LOSS(w)`, `bowl_axes()`, `bowl_surface(ax)`, `on_bowl(ax, w)`, `trail(...)`.
- `class BowlScene(ThreeDScene)` with `setup_bowl()` and `fixed(*mobs)`.
  Both scenes in the file now subclass it.

`bowl_surface` is parametrised so the rim is a true level set: for `s` in
`[0,1]` and angle `a`, `L = L_MAX s^2`, `w1 = sqrt(2L) cos a`,
`w2 = sqrt(L/4) sin a`, which satisfies `0.5 w1^2 + 4 w2^2 = L` exactly.

Framing that survived several passes, do not re-tune it blind:
`phi=58°`, `theta=-68°`, `x_length=7.4`, `y_length=3.4`, `z_length=2.8`,
`z_range=[0,20]`, `ax.shift(DOWN * 0.95)`. The diverging run in
`ValleyThreeRates` was cut from 4 steps to 3; the fourth step reaches `L ≈ 19`
and climbs out of the frame through the header.

## Not done

1. **`ValleyThreeRates` and `MomentumVsPlain` are only drafted.** The clips sitting
   in `decks/4.3-gd/assets/clips/` are still the old 2D contour renders. Render
   both at full quality and rebuild:

       bash shared/anim/render.sh anim/4.3-gd/valley.py ValleyThreeRates decks/4.3-gd
       bash shared/anim/render.sh anim/4.3-gd/valley.py MomentumVsPlain decks/4.3-gd
       node shared/site.mjs

2. **`MomentumVsPlain` has never been looked at.** Its velocity-kick arrows were
   changed from flat `Arrow` to `Arrow3D` (`thickness=0.012`, `base_radius=0.05`)
   and nobody has seen a frame of it. Check the five decomposition arrows read
   clearly against the mesh; if `Arrow3D` is too fat or too dark, fall back to a
   thick `Line` plus a small `Dot3D` at the tip.

3. **`anim/4.3-gd/stochastic.py` is untouched.** Two scenes there still draw
   filled contour ellipses and must move to the same bowl:
   - `BatchVsSGD` (line ~209), uses `bowl_contours` at line ~224.
   - `NoiseBallSchedule` (line ~404), draws two panels of concentric `Circle`
     rings, one per schedule.
   The helper `bowl_contours` at line ~52 dies with them. Import the bowl
   helpers from `valley.py` rather than copying them, or lift them into a small
   shared module if the import reads badly. `NoiseBallSchedule` is two
   side-by-side bowls, so it needs its own narrower axes, not `bowl_axes()`.

4. Scenes that are **not** contour plots and must stay as they are: `Descent1D`
   and `LearningRates` (1D parabolas), `LossCurves` (loss against step),
   `WhyNoise` (data scatter and a gradient-vector plot).

5. `decks/4.3-gd/sections/*.html` hold no inline figures, only `<video>` tags,
   so no slide markup needs to change for any of this.

## Two loose ends

- A memory file, `memory/no-contour-plots-use-3d-surfaces.md`, was written
  mid-session. It is right about 4.3 and 4.2 but it is phrased as an absolute;
  `WhyNoise`'s gradient-vector plot and the 1D loss panels are not contour maps
  and should not be swept up by it.
- Another session edited `anim/4.2-shape/curvature.py` while this work was in
  flight, renaming the slice labels from `\mathbf h` to `\boldsymbol\delta`.
  That matches the deck's δ-for-the-step notation, so it was left alone.
