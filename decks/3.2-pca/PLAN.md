# Block 3.2 — Principal component analysis: plan

Source of the storyline: Mitesh M. Khapra, CS7015 Deep Learning (IIT Madras, NPTEL),
Lecture 6, modules 6.2–6.7: PCA as a change of basis, then three interpretations
(decorrelate, minimum reconstruction error, maximum variance), then eigenfaces.
Level: Khapra's. Derivations are shown in full, with matrix shapes, not hand-waved.
The video footage is not used (beamer slides with a talking head); every figure is
rebuilt in Manim. PCA through SVD and the NumPy hands-on are added for the syllabus.

## Notation (same on every slide and in every clip)

- \(m\) data points, \(n\) features. \(X \in \mathbb{R}^{m\times n}\), row \(i\) is \(\mathbf{x}_i^T\). Columns are centred.
- New orthonormal basis \(\mathbf{p}_1,\dots,\mathbf{p}_n\), columns of \(P\) (\(n\times n\), \(P^TP = I\)).
- Coordinates \(\alpha_{ij} = \mathbf{x}_i^T\mathbf{p}_j\). All of them: \(\hat X = XP\) (\(m\times n\)).
- Covariance \(C = \tfrac1m X^TX\) (\(n\times n\)). Khapra writes \(\Sigma\); this deck writes \(C\) so that
  \(\Sigma\) keeps its Block 3.1 meaning (singular values).
- Eigenpairs of \(C\): \(\lambda_1 \ge \dots \ge \lambda_n \ge 0\), eigenvectors \(\mathbf{p}_j\).

## Colours (on top of the README roles)

- data points: teal `V_COLOR`
- \(\mathbf p_1\) (first principal direction) and anything "kept/captured": amber `RESULT_COLOR`
- \(\mathbf p_2\) and anything "dropped/lost": violet `W_COLOR`
- standard axes \(x, y\): `INK_DIM`; x / y parts: `X_COLOR` / `Y_COLOR`

## Shared 2D dataset

`anim/3.2-pca/data/cloud2d.csv`: 40 points, exact mean 0, \(C = \tfrac{1}{40}X^TX = \begin{bmatrix}3.25&1.5\\1.5&1\end{bmatrix}\).
Eigenpairs: \(\lambda_1 = 4\), \(\mathbf p_1 = (2,1)/\sqrt5\); \(\lambda_2 = 0.25\), \(\mathbf p_2 = (-1,2)/\sqrt5\).
\(\operatorname{tr} C = 4.25\); keeping \(\mathbf p_1\) keeps \(4/4.25 = 94.1\%\) of the variance.
Range x in [-4.53, 3.31], y in [-2.14, 1.90].

## Worked example (slides, by hand)

\(X = \begin{bmatrix}2&2\\-2&-2\\1&-1\\-1&1\end{bmatrix}\), \(m = 4\): \(C = \begin{bmatrix}2.5&1.5\\1.5&2.5\end{bmatrix}\),
\(\lambda = 4, 1\), \(\mathbf p_1 = (1,1)/\sqrt2\), \(\mathbf p_2 = (1,-1)/\sqrt2\),
\(\hat X = XP = \begin{bmatrix}2\sqrt2&0\\-2\sqrt2&0\\0&\sqrt2\\0&-\sqrt2\end{bmatrix}\), \(\tfrac14\hat X^T\hat X = \mathrm{diag}(4, 1)\).
SVD: \(\sigma = 4, 2\), \(\sigma^2/m = 4, 1\).

## Acts

0. Title, credits, outcomes
1. A better basis — NewBasis clip; dropping a column is not PCA; redundant columns (Khapra's x, y, z table); goals
2. Data in a new basis — CoordinatesXP clip; \(\hat X = XP\); centred stays centred; covariance matrix, CovarianceSigns clip
3. Interpretation 1: decorrelate — \(\hat C = P^TCP\); want diagonal; spectral theorem; Decorrelate clip; worked example
4. Interpretation 2: least reconstruction error — derivation; lemma \(\max_{\|\mathbf p\|=1}\mathbf p^TC\mathbf p = \lambda_1\) (proof in the eigenbasis); CapturedVsLost clip
5. Interpretation 3: most variance — variance along \(\mathbf p_j\) is \(\lambda_j\); KeepTopK clip; three interpretations, one answer; the algorithm; ThreeToTwo clip
6. PCA through the SVD — \(X = U\Sigma V^T\), \(C = V\tfrac{\Sigma^2}{m}V^T\); scores \(XV = U\Sigma\); the \(XX^T\) trick when \(n \gg m\)
7. Eigenfaces — Eigenfaces and FaceReconstruction clips (Olivetti faces, 400 × 4096); applications and limits
8. Hands-on — NumPy PCA on sklearn digits (1797 × 64); DigitsScatter clip shows the target plot
9. Recap and practice

## Clips (anim/3.2-pca/)

| Scene | File | Idea |
|---|---|---|
| NewBasis | basis.py | Same cloud, two bases: in x, y both coordinates vary; in p1, p2 the second coordinate is tiny |
| CoordinatesXP | basis.py | One point, its coordinates as dot products; all points: X̂ = XP |
| CovarianceSigns | covariance.py | Centred products: quadrant signs; sum gives C12 |
| Decorrelate | decorrelate.py | Rotate the basis; live P^T C P; off-diagonal hits 0 at the eigenvectors |
| CapturedVsLost | variance.py | Rotating unit p: captured p^T C p plus lost = tr C; max at p1, min at p2 |
| KeepTopK | variance.py | Drop p2: points fall onto the p1 line, become 1D coordinates |
| ThreeToTwo | threed.py | 3D cloud, three eigenvectors, project onto the top-2 plane |
| DigitsScatter | digits.py | Digits 64D to 2D, three classes |
| Eigenfaces | faces.py | Mean face and the first eigenfaces, eigenvalue spectrum |
| FaceReconstruction | faces.py | One face rebuilt from k = 1 … 200 components |
