# Block 1.3 — Vector spaces (105 min, presenter-led)

Syllabus: vector space and subspace; linear combination and linear span;
linear independence. Builds on 1.1 (add, scale) and 1.2 (geometry).
Source: 3b1b Essence of Linear Algebra chapter 2 (`refs/3b1b/_2016/eola/chapter2.py`),
plus chapter 16 (`chapter11.py`, abstract vector spaces) for one optional idea.
Basis, dimension and change of basis belong to Block 1.4: only name "basis
vectors î, ĵ" here, as the scalars-on-basis reading of coordinates.

## Acts

| # | Act | Min | Clips (anim/1.3-vector-spaces, class names exact) | Interactive figure |
|---|---|---|---|---|
| 0 | Title, credits, outcomes | 3 | | |
| 1 | Coordinates are scalars | 10 | BasisScalars | |
| 2 | Linear combinations | 20 | LinearCombinationVary | `combo` (drag v and w, sliders a and b; shows a v + b w) |
| 3 | Span | 25 | SpanAsDots, SpanLine, Span3D | `span` (drag v and w; their span shaded: plane, line or point) |
| 4 | Linear independence | 20 | ThirdVector3D, LinearDependence | |
| 5 | Vector spaces and subspaces | 20 | SubspaceTest | |
| 6 | Recap and practice | 7 | | |

## Clip specs

- BasisScalars (from CoordinatesAsScalars): î and ĵ; [3, −2] read as 3 î + (−2) ĵ, each basis vector scaled then added tip to tail.
- LinearCombinationVary (from ShowVaryingLinearCombinations): fixed v, w; a and b vary (shown as live numbers), the tip of a v + b w sweeps around, reaching every point of the plane.
- SpanAsDots (from VectorsToDotsScene / VectorsInThePlane): many combinations drawn as arrows, then replaced by their tips; the tips fill the plane. Span = set of all tips.
- SpanLine (from LinearDependentVectors / WhenVectorsLineUp / BothVectorsCouldBeZero): when v and w line up, every combination stays on one line; when both are zero, the span is just the origin.
- Span3D (authored, ThreeDScene; upstream used separate 3D renders): two vectors in 3D, their span is a plane through the origin, camera rotates slowly.
- ThirdVector3D (authored, ThreeDScene): add a third vector. On the plane: span unchanged (dependent). Off the plane: span becomes all of 3D space (independent).
- LinearDependence (from LinearDependentEquations / AlternateDefOfLinearlyDependent): u = a v + b w means u is redundant; equivalently a v + b w + c u = 0 with not all of a, b, c zero; independent means only a = b = c = 0 works.
- SubspaceTest (authored): a line through the origin: add two vectors on it, still on it; scale, still on it: a subspace. A line not through the origin: the sum leaves the line, and 0 times a vector is not on it: not a subspace.

## Practice

Includes the syllabus assignment: are {[3, 0, 4], [−1, 0, 7], [2, 9, 11]} linearly
independent? It is not problem 1 (problem 1 gets the only worked answer).
