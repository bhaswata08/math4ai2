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
  cases, compare f at the four candidates). The rectangle example stays as
  "Second example", with LambdaIsPrice.
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
