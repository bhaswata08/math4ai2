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

**Shared 3D bowl module `shared/anim/bowl.py`**:
Extracted bowl surface and axes helpers for Block 4.3 scenes:
- `L_MAX = 12.0`, `LIFT = 0.45`
- `LOSS(w)`, `bowl_axes()`, `bowl_surface(ax)`, `on_bowl(ax, w, lift)`, `trail(...)`
- `BowlScene(ThreeDScene)` with `setup_bowl()` and `fixed(*mobs)`
- Circular isotropic bowl helpers: `circular_bowl_axes(cx, cy)`, `circular_bowl_surface(ax)`, `on_circular_bowl(ax, w, lift)`

**4.3 `anim/4.3-gd/valley.py`**:
- `ValleyThreeRates` and `MomentumVsPlain` subclass `BowlScene`.
- Diverging run in `ValleyThreeRates` cut to 3 steps so it doesn't climb out through the header.
- Imports shared bowl helpers from `shared.anim.bowl`.

**4.3 `anim/4.3-gd/stochastic.py`**:
- `BatchVsSGD`: rewritten to subclass `BowlScene`, showing batch (RESULT_COLOR), mini-batch (W_COLOR), and SGD (Y_COLOR) 3D paths floating at staggered lift levels above the bowl with fixed 2D legend in frame.
- `NoiseBallSchedule`: rewritten to `ThreeDScene` with two side-by-side circular 3D bowls (`cx = -2.6` and `cx = 2.6`) showing constant vs decaying step size convergence, paired with 2D $\eta_k$ readouts below.
- Deleted dead helper `bowl_contours`.

**4.3 `anim/4.3-gd/descent.py`**:
- Removed unused legacy `get_bowl_contours` helper.

## Rendered 2026-11-02

All four 4.3 clips (ValleyThreeRates, MomentumVsPlain, BatchVsSGD,
NoiseBallSchedule) are rendered at 1080p and in the deck. Review fixes made
before the final render:

- BatchVsSGD: the legend ran off the left edge and sat on the bowl and the
  w_0 label. It now sits in the empty bottom-left corner with the short
  labels LossCurves uses ("Mini-batch: 4", "SGD: 64").
- NoiseBallSchedule: the eta_k readouts were skewed because
  DecimalNumber.set_value rebuilds the digits and drops them out of the
  fixed-in-frame set. The updater now re-pins them beside "eta_k =". The two
  bowls are placed so their minima project to the same screen height.

Notes:

Scenes that are not contour plots and stay as they are:
   - `Descent1D` and `LearningRates` (1D parabolas)
   - `LossCurves` (loss against step)
   - `WhyNoise` (data scatter and gradient vectors)
