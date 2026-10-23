"""Block 2.4: the eigenvectors of a covariance matrix show where a cloud spreads most.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.14 (eigenvectors); sets up PCA on Day 3.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class CovarianceEllipse(Scene):
    """Correlated point cloud, its covariance matrix, and the covariance eigenvectors."""

    def construct(self):
        U = 0.65
        plane = lin_plane(U)
        rng = np.random.default_rng(7)
        true_cov = np.array([[2.25, 1.2], [1.2, 1.0]])  # sd 1.5 and 1.0, correlation 0.8
        pts = rng.multivariate_normal([0.0, 0.0], true_cov, size=200)
        mean = pts.mean(axis=0)
        C = np.cov(pts.T)
        evals, evecs = np.linalg.eigh(C)
        order = np.argsort(evals)[::-1]
        evals, evecs = evals[order], evecs[:, order]
        for j in range(2):
            if evecs[0, j] < 0:
                evecs[:, j] *= -1

        dots = VGroup(*[Dot([p[0] * U, p[1] * U, 0], radius=0.045, color=V_COLOR) for p in pts])
        mu = np.array([mean[0] * U, mean[1] * U, 0])

        rows = [[f"{C[0,0]:.2f}", f"{C[0,1]:.2f}"], [f"{C[1,0]:.2f}", f"{C[1,1]:.2f}"]]
        mat = Matrix(rows, element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
                     h_buff=1.6, v_buff=0.7, bracket_h_buff=0.15)
        mat.get_brackets().set_color(INK)
        sigma = tex(r"\Sigma=")
        g = VGroup(sigma, mat).arrange(RIGHT, buff=0.15)
        g.to_corner(UL, buff=0.25)
        label_box(g)

        r1 = tex(rf"\lambda_1={evals[0]:.2f}", RESULT_COLOR)
        r2 = tex(rf"\lambda_2={evals[1]:.2f}", W_COLOR)
        rg = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rg.to_corner(DR, buff=0.25)
        label_box(rg)

        def ev_arrow(j, colour):
            v = evecs[:, j] * 2 * np.sqrt(evals[j]) * U
            return Arrow(mu, mu + np.array([v[0], v[1], 0]), buff=0, color=colour, stroke_width=7,
                         max_tip_length_to_length_ratio=0.25, tip_length=0.2)

        a1 = ev_arrow(0, RESULT_COLOR)
        a2 = ev_arrow(1, W_COLOR)
        ang = np.degrees(np.arctan2(evecs[1, 0], evecs[0, 0]))
        ell = Ellipse(width=2 * 2 * np.sqrt(evals[0]) * U, height=2 * 2 * np.sqrt(evals[1]) * U,
                      color=INK_DIM, stroke_width=3).rotate(np.radians(ang)).move_to(mu)
        print("cov", C.round(2).tolist(), "evals", evals.round(2).tolist(), "evec1", evecs[:, 0].round(2).tolist())

        self.add(plane, dots, g)
        self.wait(1.2)
        self.play(Create(ell), run_time=1.5)
        self.play(GrowArrow(a1), FadeIn(r1), run_time=1.5)
        self.wait(0.5)
        self.play(GrowArrow(a2), FadeIn(r2), run_time=1.5)
        self.wait(1.5)
