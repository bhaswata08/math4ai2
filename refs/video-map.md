# 3Blue1Brown, Essence of Linear Algebra: video to source to block

Playlist: https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
Scraped with yt-dlp into `playlists/3b1b-essence-linear-algebra.tsv` (index, id, length, title).
Scene source is in https://github.com/3b1b/videos. Upstream file numbers do not match
video chapter numbers; the mapping below was made by matching each file's content.
Copy a file into `3b1b/` (mirroring the upstream path) before porting from it.

| Ch | Video | ID | Upstream source | Block(s) |
|---|---|---|---|---|
| 1 | Vectors | fNk_zzaMoSs | `_2016/eola/chapter1.py` | 1.1 (done) |
| 2 | Linear combinations, span, and basis vectors | k7RM-ot2NWY | `_2016/eola/chapter2.py` | 1.3, 1.4 |
| 3 | Linear transformations and matrices | kYB8IZa5AuE | `_2016/eola/chapter3.py` | 2.1 |
| 4 | Matrix multiplication as composition | XkY2DOUCWMU | `_2016/eola/chapter4.py` | 2.1 |
| 5 | Three-dimensional linear transformations | rHLEWRxRGiM | `_2016/eola/footnote.py` | 2.1 (optional) |
| 6 | The determinant | Ip3X9LOh2dk | `_2016/eola/chapter5.py` | 2.2 |
| 7 | Inverse matrices, column space and null space | uQhTuRlWMxw | `_2016/eola/chapter6.py` | 2.2 (rank) |
| 8 | Nonsquare matrices as transformations | v8VSDg_WQlA | `_2016/eola/footnote2.py` | 2.1 (optional) |
| 9 | Dot products and duality | LyGKycYT2v0 | `_2016/eola/chapter7.py` | 1.1 dot product (done); projection reused in 1.2; duality in 2.1 |
| 10 | Cross products | eu6i7WJeinw | `_2016/eola/chapter8.py` | not in syllabus |
| 11 | Cross products as linear transformations | BaM7OCEm3G0 | `_2016/eola/chapter8p2.py` | not in syllabus |
| 12 | Cramer's rule, explained geometrically | jBsC34PxzoM | `_2018/cramer.py` | 2.2 (optional) |
| 13 | Change of basis | P2LTAUO1TdA | `_2016/eola/chapter9.py` | 1.4 |
| 14 | Eigenvectors and eigenvalues | PFDu9oVAE-g | `_2016/eola/chapter10.py` | 2.3, 2.4 |
| 15 | A quick trick for computing eigenvalues | e50Bj7jn9IQ | `_2021/quick_eigen.py` | 2.4 |
| 16 | Abstract vector spaces | TgKwz5Ikpc8 | `_2016/eola/chapter11.py` | 1.3 (optional) |

## Gaps: no chapter covers these, so scenes are authored from scratch

- 1.2: vector norms (L1, L2, L-infinity), cosine similarity. Projection can reuse chapter 9 scenes.
- 2.2: trace. 2.3: positive definite matrices.
- 3.1: SVD and low-rank approximation. 3.2: PCA.
