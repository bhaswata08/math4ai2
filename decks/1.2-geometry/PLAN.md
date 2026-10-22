# Block 1.2 — Geometry of vectors (105 min, presenter-led)

Syllabus: vector norms L1, L2, L∞; vector projection; cosine similarity
(embeddings, document similarity); orthogonal, normal (unit) and orthonormal vectors.
Builds on Block 1.1 (vectors, add, scale, dot product as Σ v_i w_i and as
projection × length). No 3b1b chapter covers norms or cosine similarity, so
every clip here is authored from scratch in the 3b1b style (house.py).

## Acts

| # | Act | Min | Clips (anim/1.2-geometry, class names exact) | Interactive figure |
|---|---|---|---|---|
| 0 | Title, credits, outcomes | 3 | | |
| 1 | Length: the L2 norm | 15 | NormPythagoras | `norms` (drag v; live L1, L2, L∞) |
| 2 | Other ways to measure: L1 and L∞ | 15 | NormManhattan, UnitBalls | |
| 3 | Unit vectors and normalizing | 10 | Normalize | |
| 4 | Projection | 20 | ProjectionFormula | `project` (drag v and w; projection and formula) |
| 5 | Cosine similarity | 20 | CosineAngle, CosineScaleInvariant | `cosine` (drag v and w; angle and cos θ) |
| 6 | Orthogonal and orthonormal | 15 | OrthogonalTest, OrthonormalCoordinates | |
| 7 | Recap and practice | 7 | | |

## Clip specs

- NormPythagoras: v = [3, 2] on the plane, legs 3 (X_COLOR) and 2 (Y_COLOR), right angle mark, ‖v‖ = √(3² + 2²) = √13; then the same rule written for n entries.
- NormManhattan: from the origin to [3, 2] along grid streets (L1 = |3| + |2| = 5, RESULT_COLOR path) versus the straight line (L2 = √13 ≈ 3.61, V_COLOR); then L∞ = max(|3|, |2|) = 3.
- UnitBalls: every vector of length 1 under each norm, traced as tips: L2 circle, L1 diamond, L∞ square, morphing between them, each labelled with its formula.
- Normalize: five vectors of different lengths; each divided by its own length shrinks or stretches onto the unit circle; caption v̂ = v / ‖v‖.
- ProjectionFormula: v and w, the line through v, w dropped perpendicular onto it, the shadow proj_v w (RESULT_COLOR); formula proj_v w = (v·w / v·v) v built in steps; right angle mark at the foot.
- CosineAngle: v and w with the angle θ arc; v·w = ‖v‖‖w‖cos θ, rearranged to cos θ = v·w / (‖v‖‖w‖); w swings through 0°, 90°, 180° with cos θ = 1, 0, −1 shown.
- CosineScaleInvariant: w stretched to 3w; the dot product triples, cos θ stays fixed. Then two "documents" as word-count vectors (a short and a long article on the same topic) point the same way: cosine 1 despite different lengths.
- OrthogonalTest: v = [2, 1], w = [−1, 2]; v·w = −2 + 2 = 0; right-angle mark appears; then a pair that is not orthogonal for contrast.
- OrthonormalCoordinates: a rotated orthonormal pair u1, u2 (unit length, 90° apart); a vector x; its coordinates in that basis are just the two dot products x·u1 and x·u2, shown as projections.

## AI hooks (slides, not clips)

- Vector search ranks documents by cosine similarity to the query embedding.
- L2 and L1 penalties on model weights (ridge and lasso) are these norms.
