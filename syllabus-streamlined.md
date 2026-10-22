# Mathematics for AI — 4-day plan

4 days, 8 hours a day. Each day has 4 blocks of about 1h45 of teaching, with
breaks between them. 16 blocks in total: 10 on linear algebra, 6 on calculus
and optimization.

Each topic appears once. Later blocks build only on earlier ones.

---

## Day 1 — Vectors and vector spaces

### Block 1.1 — Vectors

- What a vector is: a list of numbers, an arrow, a data point
- Scalars, vector addition, scalar multiplication
- Dot product: algebraic and geometric definitions

### Block 1.2 — Geometry of vectors

- Vector norms: L1, L2, L∞
- Vector projection
- Cosine similarity (embeddings, document similarity)
- Orthogonal, normal (unit) and orthonormal vectors

### Block 1.3 — Vector spaces

- Vector space and subspace
- Linear combination and linear span
- Linear independence

### Block 1.4 — Basis and dimension

- Basis vectors and dimension
- Changing basis
- Intersection of subspaces

**Assignments**

1. Are the vectors $\{[3, 0, 4], [-1, 0, 7], [2, 9, 11]\}$ linearly
   independent?
2. Let $X = [0\ 1\ 3]^T$ and $Y = [2\ 4\ 0]^T$. Let $V = \text{span}(X)$ and
   $W = \text{span}(Y)$. Describe $V$, $W$ and $V \cap W$.

---

## Day 2 — Matrices and eigenvectors

### Block 2.1 — Matrices as linear maps

- Matrix definition, addition, scalar multiplication, transpose
- Linear mappings: a matrix as a function that transforms space
- Matrix multiplication as composing maps, and its properties
- Hadamard (element-wise) product
- Affine maps: linear map plus translation

### Block 2.2 — Determinant, inverse, rank

- Identity matrix
- Determinant: how a map scales area and volume
- Invertible matrices and the inverse
- Rank and its link to linear independence
- Trace

### Block 2.3 — Special matrices

- Symmetric, diagonal, orthogonal matrices
- Positive definite and positive semi-definite matrices
- How the matrix types relate (one family-tree diagram)
- Eigenvalues and eigenvectors: concept and intuition

### Block 2.4 — Eigendecomposition

- Computing eigenvalues and eigenvectors
- Diagonalization
- Eigenvectors of symmetric matrices
- Where eigenvectors show up in AI

**Assignment**

3. Find the eigenvalues and eigenvectors of
   $$\begin{bmatrix} 5 & -10 & -5 \\ 2 & 14 & 2 \\ -4 & -8 & 6 \end{bmatrix}$$

---

## Day 3 — SVD, PCA, and derivatives

### Block 3.1 — Singular value decomposition

- SVD: concept and geometry (rotate, stretch, rotate)
- Properties, and how SVD relates to eigendecomposition
- Low-rank matrix approximation (image compression example)

### Block 3.2 — Principal component analysis

- The covariance matrix
- PCA through eigenvectors of the covariance matrix
- PCA through SVD
- Applications: dimensionality reduction, visualization
- Hands-on: PCA on a real dataset in NumPy

### Block 3.3 — Derivatives

- Functions, the scalar derivative: definition and intuition
- Common rules of differentiation
- Chain rule
- Partial derivatives

### Block 3.4 — Gradients

- Gradient: concept, intuition, properties
- Directional derivative
- Gradients of vector-valued functions: the Jacobian

**Assignment**

4. Let $f(x,y,z) = xye^x + z^2 - 5$. Compute the gradient of $f$ at
   $(1, 3, -2)$, and the directional derivative $D_v f$ at that point in the
   direction of $v = (3, -1, 4)$.

---

## Day 4 — Matrix calculus and optimization

### Block 4.1 — Matrix calculus and backpropagation

- The four cases: scalar or vector, with respect to scalar or vector
- Gradients with respect to matrices
- Useful identities for computing gradients
- Backpropagation and automatic differentiation

### Block 4.2 — The shape of a function

- Linearization and multivariate Taylor series
- The Hessian
- Critical points: local and global minima and maxima, saddle points
- Convex functions

### Block 4.3 — Gradient descent

- Gradient descent and the learning rate
- Batch, mini-batch and stochastic gradient descent
- Performance comparison
- Hands-on: the three variants on the same loss surface

### Block 4.4 — Constrained and convex optimization

- Constrained optimization and Lagrange multipliers
- Convex optimization
- Course review
