# Block 1.4 — Basis and dimension (105 min, presenter-led)

Syllabus: basis vectors and dimension; changing basis; intersection of
subspaces. Builds on 1.3 (span, independence, subspaces) and 1.2
(orthonormal coordinates are dot products).
Source: 3b1b Essence of Linear Algebra chapter 2 (`refs/3b1b/_2016/eola/chapter2.py`:
WhatIfWeChoseADifferentBasis, TechnicalDefinitionOfBasis) and chapter 13,
change of basis (`refs/3b1b/_2016/eola/chapter9.py`: JennysGrid,
ShowOriginOfGrid, TranslateFromJenny).
Matrices arrive on Day 2. Change of basis here is done with linear
combinations and two equations only; the change-of-basis matrix is named as
"Day 2" and not used.

## Numbers used everywhere (checked)

- Jennifer's basis: b1 = [2, 1], b2 = [−1, 1] (3b1b's choice).
- Her [−1, 2] → ours: −1·[2, 1] + 2·[−1, 1] = [−4, 1].
- Our [3, 2] → hers: 2a − b = 3, a + b = 2 → a = 5/3, b = 1/3.
  Check: (5/3)[2, 1] + (1/3)[−1, 1] = [10/3 − 1/3, 5/3 + 1/3] = [3, 2].
- Intersection example: plane z = 0 is span{[1,0,0], [0,1,0]}, plane x = 0 is
  span{[0,1,0], [0,0,1]}; they meet in the y-axis, span{[0,1,0]}.

## Acts

| # | Act | Min | Clips (anim/1.4-basis, class names exact) | Interactive figure |
|---|---|---|---|---|
| 0 | Title, credits, outcomes | 3 | | |
| 1 | What a basis is | 20 | BasisDefinition, SameVectorTwoBases | |
| 2 | Dimension | 15 | DimensionCount | |
| 3 | Changing basis | 35 | JennysGrid, TranslateFromJenny, TranslateToJenny | `basis` (drag b1, b2 and a target x; the b1/b2 grid is drawn; readout gives x's coordinates in that basis, or "not a basis" when b1, b2 are parallel) |
| 4 | Intersection of subspaces | 20 | SubspaceIntersection3D | |
| 5 | Recap and practice | 12 | | |

## Clip specs

- BasisDefinition (authored, from TechnicalDefinitionOfBasis): "a basis is a set of linearly independent vectors that span the space". î, ĵ span the plane and are independent: a basis. Then b1 = [2, 1], b2 = [−1, 1]: their combinations also fill the plane (skewed grid appears): also a basis. Then two parallel vectors: span only a line, not a basis. Then three vectors in the plane: they span, but one is redundant: not a basis.
- SameVectorTwoBases (from WhatIfWeChoseADifferentBasis): the arrow to [3, 2]. In the standard grid its coordinates are (3, 2) = 3î + 2ĵ. Switch to the b1, b2 grid: the same arrow is (5/3)b1 + (1/3)b2, coordinates (5/3, 1/3). Same arrow, different numbers: coordinates depend on the basis.
- DimensionCount (authored, ThreeDScene allowed): a line through the origin needs 1 basis vector, a plane 2, space 3. Dimension = number of vectors in any basis. Adding one more vector makes the set dependent; removing one loses part of the span.
- JennysGrid (from JennysGrid, ShowOriginOfGrid): our grid; Jennifer's grid drawn over it from b1, b2. Same origin, different grid lines and different first steps.
- TranslateFromJenny (from TranslateFromJenny): Jennifer says [−1, 2]. Build −1·b1 + 2·b2 tip to tail on her grid, then read the tip on our grid: [−4, 1].
- TranslateToJenny (authored, the reverse): we say [3, 2]. Ask for a, b with a·b1 + b·b2 = [3, 2]; write the two equations 2a − b = 3, a + b = 2; solve a = 5/3, b = 1/3; show the arrow as (5/3)b1 + (1/3)b2 on her grid.
- SubspaceIntersection3D (authored, ThreeDScene): plane z = 0 and plane x = 0, both through the origin, slowly rotating camera; their intersection highlights as the y-axis line. Caption: "the intersection of subspaces is a subspace". Then a line through the origin not in a plane: they meet only at the origin, {0}.

## Slides beyond clips

- Act 1: definition slide (independent + spans), and a "standard basis in n dimensions" slide e1..en.
- Act 2: dimension examples table: R² → 2, R³ → 3, a plane through 0 in R³ → 2, a line → 1, {0} → 0. Hook: an embedding with 768 numbers lives in a 768-dimensional space.
- Act 3: after the clips, the `basis` figure; then "an orthonormal basis makes this easy: coordinates are dot products" (recall 1.2 OrthonormalCoordinates; no new clip); hook: PCA (Day 3) is choosing a better basis for the data.
- Act 4: worked example slide with the z = 0 / x = 0 planes (numbers above). Note that a union of subspaces is usually not a subspace.
- Act 5: recap beats; practice. Problem 1 (worked, fragment): is {[1, 0], [1, 1]} a basis of R²? Coordinates of [3, 2] in it? Answer: yes, independent and 2 vectors in R²; [3, 2] = 1·[1, 0] + 2·[1, 1]. Problems 2–5, no answers: the two syllabus assignments ({[3,0,4], [−1,0,7], [2,9,11]} independent?; X = [0 1 3]ᵀ, Y = [2 4 0]ᵀ, describe span(X), span(Y), their intersection), Jennifer's [1, 1] in our coordinates, our [1, 3] in Jennifer's coordinates.
