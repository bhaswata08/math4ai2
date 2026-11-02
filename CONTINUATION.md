# Continuation: Day 4 loss surfaces and the 4.4 Lagrange acts

Updated 2026-11-02.

## Standing instruction

Every loss picture in Block 4.3 shows the loss as a **3D surface**, never as a
2D contour map. Block 4.2's `ConvexAlongEveryLine` is the reference look: a mesh
in `V_COLOR` with alternating face opacity, axes in `X_COLOR` / `Y_COLOR`, labels
fixed in the frame by projecting with `self.camera.project_point`. Shared
helpers live in `shared/anim/bowl.py`.

## Done

**4.3** (`anim/4.3-gd/valley.py`, `stochastic.py`): ValleyThreeRates,
MomentumVsPlain, BatchVsSGD and NoiseBallSchedule are 3D, rendered at 1080p
and in the deck. BatchVsSGD's legend sits in the empty bottom-left corner.
NoiseBallSchedule re-pins its eta_k readouts in the updater, because
`DecimalNumber.set_value` drops new digits out of the fixed-in-frame set.

**4.4 Acts 1 and 2**, rebuilt after Trefor Bazett, "Lagrange Multipliers |
Geometric Meaning & Full Example" (youtube 8mjcnxGMwFo; transcript and
contact sheets in `build/yt/v8m/`). Running example: f = xy + 1 on the unit
circle, which has two highs (1.5) and two lows (0.5).

- `anim/4.4-constrained/saddle.py`:
  - `SaddleOnCircle`: the 3D saddle, the circle lifted onto it, and the
    highs and lows marked. The camera sits at theta = -67.5 degrees: at -45
    or -90, two of the four points share a line of sight.
  - `LevelCurvesTouch`: the level xy + 1 = c rises until it only touches
    the circle, then the shared tangent line, then grad f and grad g on
    one line (lambda = 1/2 at the highs, -1/2 at the lows).
- `01-constraints.html`: the two clips, plus a "touching curves share a
  tangent line" derivation slide.
- `02-lagrange.html`: the old f = x + y `LagrangeSystem` clip is gone. Four
  worked-example slides follow the recipe (set up, three equations, two
  cases, compare f at the four candidates).
- Credits slide (`00-open.html`) names Bazett.

**4.4 Act 2, second example** (after Brian Douglas, MATLAB Tech Talk): the
lagrange.py scenes ConstrainedSlice, LevelOnTheCurve, LagrangeSystem and
ShadowPrice are fixed and in the deck, after the Bazett worked example.
- Layout: a smaller bowl further left, and a text column at x = 0 that
  clears its rim.
- Sign convention: the scenes now use the deck recipe L = f - lambda (g - c),
  so lambda = -3 and dJ*/dt = lambda.
- ShadowPrice replaces LambdaIsPrice, whose source scene was gone. The
  rectangle example is dropped, and the unused clips (ConstraintWalk,
  TangencyGradients, LambdaIsPrice) are deleted.
- Douglas is on the credits slide.

## Not done

- The day-4 release tag still points at f5ca4a2. The assets are current,
  but moving the tag needs a force-push, which the harness blocks. Run
  `git tag -f day-4 <sha> && git push -f origin day-4` by hand if wanted.

## Gotchas found this session

- Do not render two scenes from the same file in parallel. They share the
  Tex cache and partial-movie folders, and one of them fails with
  FileNotFoundError.
- In this harness's Bash tool, `\;` inside a command (sed, node -e) is
  stripped to `;`. Make TeX edits that contain `\;` with the Edit tool.
- `ThreeDAxes.c2p` maps through the axis objects, so shifting `ax.x_axis`
  moves every point. Draw separate lines to put the axes on a floor plane.

---

# Continuation: 4.4 Lagrange multipliers, rebuilt from the MATLAB Tech Talk

Written 2026-11-02, same day, different thread. Pick this up on the office
machine. The Python is committed and pushed; the slides are not written yet.

## What was asked

"Build the lagrangian section using this, look at its visuals as well. Keep
talking points beside animations and slides", pointing at Brian Douglas,
*Constrained Optimization: Intuition behind the Lagrangian*, MATLAB Tech Talk,
YouTube `GR4ff0dTLTw`.

The transcript and sample frames were pulled with `yt-dlp` and looked at. The
talk's argument, in its order: stationary points of an unconstrained problem
sit where the gradient is zero; add a constraint and only a line of points is
allowed; the objective restricted to that line is a parabola; at its lowest
point your path is tangent to a level curve, so it is perpendicular to the
gradient; the constraint's own gradient is perpendicular to the same line, so
the two gradients are parallel there; scale one by lambda to make them equal
and the whole thing collapses to a single gradient of a single function. Second
order is named (bordered Hessian) and skipped.

The artwork was **not** copied. The clips are original, in house style.

## The one real design decision

The deck's Acts 1 and 2 used to maximise `f = x + y` on the unit circle. That
example is now gone. Its surface is a flat tilted plane, so it has no 3D shape
at all, and the only way to draw it is the 2D contour map with gradient arrows
that `memory/no-contour-plots-use-3d-surfaces.md` forbids. The talk's example
replaces it everywhere in Acts 1 and 2:

    minimise   J(x1, x2) = x1^2 + x2^2        a bowl, a real surface
    subject to c(x1, x2) = x1 + x2 + 3 = 0    a line in the x1-x2 plane
    answer     x1 = x2 = -1.5, J* = 4.5, lambda = 3

Note the sign convention changed with it: the deck now uses `L = J + lambda*c`,
where it used to use `L = f - lambda*(g - c)`.

## Done: `anim/4.4-constrained/lagrange.py`, rewritten end to end

All four old scenes were thrown away. The four new ones are:

- **`ConstrainedSlice`** (3D). The bowl, then the constraint line on the floor,
  then a translucent violet wall standing on it, then the amber curve where the
  wall meets the bowl. A dot walks the curve with a live `J` readout: it falls,
  bottoms out, rises. Lands on `x1 = x2 = -1.5, J = 4.5`.
- **`LevelOnTheCurve`** (3D). The tangency argument without a contour map. A
  level ring is drawn *on the surface* at `z = 9`; the constraint curve crosses
  it twice. Shrink the ring to `z = 4.5` and the two crossings slide together
  and merge: it touches. Then a dashed line drops to the floor and the two
  gradients are drawn there at a shared scale, ending on `grad J = -3 grad c`.
- **`LagrangeSystem`** (2D, equations only, no plot). The Lagrangian, the three
  partials set to zero, the solve. The 3x3 system is solved with
  `np.linalg.solve` and asserted before any number is shown.
- **`ShadowPrice`** (3D). The bowl stays still and only the wall, the curve and
  the minimum dot move as the constraint relaxes from `t = 0` to `t = 1`. Ends
  on `dJ*/dt = -3 = -lambda`, with the `-3` from a central difference.

### Geometry that survived tuning, do not re-tune blind

`R = 3.3` (the bowl is a **disc**, not a square patch: a square patch of
`x1^2 + x2^2` spikes at the corners). `ZMAX = R*R`, so the drawn rim is a true
level set and the constraint chord ends exactly on it. `PHI = 64 deg`.

`THETA = -100 deg` is a compromise and the comment in the file explains it.
Looking straight down the constraint normal `(1,1)` (around `-125 deg`) lays
the chord flat across the picture but squashes `grad c` to a stub, and `grad c`
is the one arrow `LevelOnTheCurve` needs. At `-100 deg` the chord keeps 82% of
its length across the screen and the normal keeps 57%.

Along the constraint line, writing `s` for signed distance from the line's
closest point to the origin, `J = |foot|^2 + s^2`. That is why the slice is
exactly a parabola whose vertex is the answer, and it is what the live readout
and the half-chord calculation both use.

### Two things worth keeping

- `hud()` asserts that every fixed-in-frame label is inside the frame before
  pinning it. The column beside the bowl is about 5.3 units wide and lines kept
  running off the slide unnoticed. Three lines had to be split in half by
  `stack()` to pass it. If a new label fails the assert, split it, do not
  shrink it below the font floor.
- `live_number()` exists because **`DecimalNumber` updaters do not work in a
  `ThreeDScene`**. `set_value` rebuilds the digits, the new digits are not on
  the camera's fixed-in-frame list, and the number ends up smeared across the
  floor in 3D. The fix is to re-pin and re-place it on every frame. Both `J`
  readouts were invisible before this.


## State as of the handover

A second session was working the same deck in parallel and has carried this
further than the list below was first written for. As of commit `4317393` and
the one after it:

- All four scenes are **rendered at 1080p and in the deck**. `LevelOnTheCurve`'s
  poster frame was checked: the last framing change (`GSCALE` 0.5 -> 0.75, axes
  `LEFT*2.0 + UP*0.35`) survived. `grad J` fits, `grad c` is a real arrow rather
  than a stub, and the bowl is not clipped.
- The old circle-example clips are gone, and two more have appeared from the
  other session: `SaddleOnCircle` and `LevelCurvesTouch`, used by
  `01-constraints.html`.
- `02-lagrange.html` is written. It keeps a `xy + 1` on the unit circle worked
  example (after Trefor Bazett) for the algebra and uses all four of these
  clips for the geometry. So the deck now carries two examples on purpose, not
  the single one the rewrite assumed.

## Not done

1. **A sign contradiction, and it is on a slide.** The `LevelOnTheCurve`
   caption in `02-lagrange.html` reads "`grad J = -3 grad c`, so `lambda = -3`".
   With `L = J + lambda*c` the stationarity condition is
   `grad J + lambda*grad c = 0`, so `grad J = -lambda*grad c` and
   `lambda = +3`. `LagrangeSystem` shows `lambda = 3` on screen, so the slide
   and the clip disagree. Fix the caption, not the clip.

2. **Talking points are not beside the clips yet.** The instruction was "keep
   talking points beside animations and slides". The four new clip slides use a
   single `<p class="caption">` under the video. They should use the `clip-talk`
   grid (points left, clip right) that `4.1-backprop/01-four-cases.html` and the
   3.1 deck use, with the caption's content broken into two or three `<li>`.

3. **Small render nit.** In `LevelOnTheCurve` the `grad c` label box still
   clips the top of its own arrow. Nudge it further right in `lab_c`
   (`RIGHT * 0.55 + UP * 0.3` today) and re-render that one scene.

4. **Check the KKT takeaway still reads true.** `03-convex.html` line 69 says
   "Act 2 maximised with `L = f - lambda(g - c)`; here we minimise, so the sign
   flips." That was written against the old act. Act 2 now carries both a
   maximise-on-the-circle example and a minimise-the-bowl example, so the
   sentence needs a second look rather than a straight deletion.

5. **Rebuild the whole site, not the single deck**: `node shared/site.mjs`.
   See `memory/rebuild-site-after-every-change.md`.
