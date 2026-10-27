"""Block 2.2: the identity, and what a scaling does that a shear does not.

Idea from Visual Kernel, SEE Matrix ch.1 and 3Blue1Brown, Essence of Linear
Algebra ch.6 (the determinant). The scenes are redrawn in Manim.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tag(tex, color=INK):
    return MathTex(tex, font_size=MIN_FONT, color=color)


def corner_matrix(rows, corner=UL):
    mat = matrix_tex(rows)
    mat.to_corner(corner, buff=0.25)
    return label_box(mat)


class IdentityNothingMoves(Scene):
    """I leaves a marked point, the F and the basis vectors exactly where they are."""

    def construct(self):
        U = 0.8
        I = np.eye(2)
        plane = lin_plane(U)
        mat = corner_matrix([[1, 0], [0, 1]])
        p = np.array([2.0, 1.0])
        F = f_marker(scale=1.0).shift([-3.0, -1.7, 0])
        dot = Dot([p[0] * U, p[1] * U, 0], radius=0.14, color=HIGHLIGHT).set_z_index(6)
        lab = label_box(tag(r"p=(2,1)", HIGHLIGHT).next_to(dot, UP, buff=0.2))
        i_hat, j_hat = basis_arrows(I * U)

        self.add(plane, F, i_hat, j_hat, dot, lab, mat)
        self.wait(2.0)
        self.play(ApplyMatrix(I, plane), ApplyMatrix(I, F), ApplyMatrix(I, dot), run_time=3)
        q = I @ p
        res = label_box(tag(rf"I\,(2,1)=({q[0]:g},{q[1]:g})").to_corner(DR, buff=0.25))
        self.play(Write(res), run_time=1.2)
        self.play(Indicate(dot, color=HIGHLIGHT, scale_factor=1.8), run_time=1.0)
        self.wait(2.0)


class ShearVsScale(Scene):
    """Shear [[1,1],[0,1]] keeps the area of the unit square; scaling 2I multiplies it by 4."""

    def construct(self):
        U = 0.95
        S = np.array([[1.0, 1.0], [0.0, 1.0]])
        D = 2 * np.eye(2)

        def panel(cx):
            pl = house_plane(x_range=[-0.5, 4.5, 1], y_range=[-0.5, 3, 1],
                             x_length=5 * U, y_length=3.5 * U)
            pl.move_to([cx, -0.45, 0])
            return pl

        def poly(pl, M, color=RESULT_COLOR, op=0.35):
            pts = [pl.c2p(*(M @ np.array(v))) for v in ((0, 0), (1, 0), (1, 1), (0, 1))]
            return Polygon(*pts, color=color, stroke_width=4, fill_color=color, fill_opacity=op)

        def arrows(pl, M):
            o = pl.c2p(0, 0)
            a = Arrow(o, pl.c2p(M[0, 0], M[1, 0]), buff=0, color=X_COLOR, stroke_width=6, tip_length=0.18)
            b = Arrow(o, pl.c2p(M[0, 1], M[1, 1]), buff=0, color=Y_COLOR, stroke_width=6, tip_length=0.18)
            return a, b

        pl_l, pl_r = panel(-2.5), panel(2.5)
        mat_l = matrix_tex([[1, 1], [0, 1]]).move_to([-2.5, 2.0, 0])
        mat_r = matrix_tex([[2, 0], [0, 2]]).move_to([2.5, 2.0, 0])
        sq_l, sq_r = poly(pl_l, np.eye(2)), poly(pl_r, np.eye(2))
        al, bl = arrows(pl_l, np.eye(2))
        ar, br = arrows(pl_r, np.eye(2))

        def area_lbl(cx, n, color=RESULT_COLOR):
            return label_box(tag(rf"\text{{area}}={n:g}", color).move_to([cx, -2.5, 0]))

        a_l, a_r = area_lbl(-2.5, 1), area_lbl(2.5, 1)
        self.add(pl_l, pl_r, sq_l, sq_r, al, bl, ar, br, mat_l, mat_r, a_l, a_r)
        self.wait(2.0)

        area_s = abs(np.linalg.det(S))
        sq_l2, (al2, bl2) = poly(pl_l, S), arrows(pl_l, S)
        self.play(Transform(sq_l, sq_l2), Transform(al, al2), Transform(bl, bl2), run_time=2.5)
        self.play(ReplacementTransform(a_l, area_lbl(-2.5, area_s)), run_time=0.8)
        self.wait(1.5)

        area_d = abs(np.linalg.det(D))
        sq_r2, (ar2, br2) = poly(pl_r, D), arrows(pl_r, D)
        self.play(Transform(sq_r, sq_r2), Transform(ar, ar2), Transform(br, br2), run_time=2.5)
        self.play(ReplacementTransform(a_r, area_lbl(2.5, area_d)), run_time=0.8)
        self.wait(2.5)


class ZeroCollapse(Scene):
    """The zero matrix sends every point to the origin."""

    def construct(self):
        U = 0.8
        plane = lin_plane(U)
        mat = corner_matrix([[0, 0], [0, 0]])
        cloud = disc_cloud(radius=1.6, step=0.14, dot_radius=0.04).shift([1.2, 0.3, 0])
        F = f_marker(scale=0.8).shift([-3.6, -1.8, 0])
        i_hat, j_hat = basis_arrows(np.eye(2) * U)
        self.add(plane, cloud, F, i_hat, j_hat, mat)
        self.wait(2.0)
        Z = np.zeros((2, 2))
        self.play(move_dots(cloud, Z), ApplyMatrix(Z + 1e-3 * np.eye(2), F),
                  ApplyMatrix(1e-3 * np.eye(2), VGroup(i_hat, j_hat)), run_time=3)
        end = Dot(ORIGIN, radius=0.14, color=RESULT_COLOR).set_z_index(6)
        ring = Circle(radius=0.4, color=HIGHLIGHT, stroke_width=5)
        self.play(FadeIn(end, scale=3), Create(ring), run_time=1.0)
        lab = label_box(tag(r"\text{every point}\to(0,0)", RESULT_COLOR).to_corner(DR, buff=0.25))
        self.play(FadeIn(lab), run_time=0.8)
        self.wait(2.5)
