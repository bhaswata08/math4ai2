"""Block 2.1: the columns of a matrix are where the basis vectors land.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.3.
"""

from shared.anim.house import *
from shared.anim.linmap import *


class BasisColumns(Scene):
    """The grid is carried along; i-hat and j-hat land on the two columns."""

    def construct(self):
        U = 0.8
        A = np.array([[2.0, -1.0], [1.0, 1.0]])
        bg = lin_plane(U).fade(0.65)
        grid = lin_plane(U)
        mat = matrix_tex([[2, -1], [1, 1]])
        mat.to_corner(UL, buff=0.25)
        label_box(mat)

        i0, j0 = basis_arrows(U * np.eye(2))
        i1, j1 = basis_arrows(U * A)
        li0 = MathTex(r"\hat\imath", font_size=MIN_FONT, color=X_COLOR)
        lj0 = MathTex(r"\hat\jmath", font_size=MIN_FONT, color=Y_COLOR)
        li0.next_to(i0.get_end(), DOWN, buff=0.15)
        lj0.next_to(j0.get_end(), LEFT, buff=0.2)
        li1 = MathTex("(2,1)", font_size=MIN_FONT, color=X_COLOR)
        lj1 = MathTex("(-1,1)", font_size=MIN_FONT, color=Y_COLOR)
        li1.next_to(i1.get_end(), RIGHT, buff=0.2)
        lj1.next_to(j1.get_end(), LEFT, buff=0.2)
        for l in (li0, lj0, li1, lj1):
            label_box(l)

        self.add(bg, grid, i0, j0, li0, lj0, mat)
        self.wait(1)
        self.play(ApplyMatrix(A, grid), Transform(i0, i1), Transform(j0, j1),
                  FadeTransform(li0, li1), FadeTransform(lj0, lj1), run_time=3)
        self.wait(0.3)
        cols = mat.get_columns()
        self.play(Indicate(cols[0], color=HIGHLIGHT, scale_factor=1.25), Indicate(li1, color=HIGHLIGHT, scale_factor=1.2), run_time=1)
        self.play(Indicate(cols[1], color=HIGHLIGHT, scale_factor=1.25), Indicate(lj1, color=HIGHLIGHT, scale_factor=1.2), run_time=1)
        self.wait(1.5)


class ColumnsCombine(Scene):
    """A v is the same combination of the new basis vectors: 1*col1 + 2*col2."""

    def construct(self):
        U = 0.8
        A = np.array([[2.0, -1.0], [1.0, 1.0]])
        bg = lin_plane(U).fade(0.65)
        grid = lin_plane(U)
        mat = matrix_tex([[2, -1], [1, 1]])
        mat.to_corner(UL, buff=0.25)
        label_box(mat)

        def P(x, y):
            return np.array([U * x, U * y, 0.0])

        def arr(a, b, col):
            return Arrow(P(*a), P(*b), buff=0, color=col, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25, tip_length=0.18)

        v = arr((0, 0), (1, 2), V_COLOR)
        a1 = arr((0, 0), (1, 0), X_COLOR)
        a2 = arr((1, 0), (1, 2), Y_COLOR)
        eq0 = MathTex(r"\mathbf v", "=", "1", r"\hat\imath", "+", "2", r"\hat\jmath", font_size=MIN_FONT)
        eq0.set_color_by_tex(r"\mathbf v", V_COLOR)
        for t, c in (("1", X_COLOR), (r"\hat\imath", X_COLOR), ("2", Y_COLOR), (r"\hat\jmath", Y_COLOR)):
            eq0.set_color_by_tex(t, c)
        eq0.move_to([0, -2.3, 0])
        label_box(eq0)

        self.add(bg, grid, v, mat, eq0)
        self.wait(0.8)
        self.play(Create(a1), run_time=0.8)
        self.play(Create(a2), run_time=0.8)
        self.wait(0.8)

        v1 = arr((0, 0), (0, 3), RESULT_COLOR)
        a1t = arr((0, 0), (2, 1), X_COLOR)
        a2t = arr((2, 1), (0, 3), Y_COLOR)
        eq1 = MathTex(r"A\mathbf v", "=", "1", r"\cdot", r"\text{col}_1", "+", "2", r"\cdot", r"\text{col}_2",
                      "=", "(0,3)", font_size=MIN_FONT)
        eq1.set_color_by_tex(r"A\mathbf v", RESULT_COLOR)
        eq1.set_color_by_tex("(0,3)", RESULT_COLOR)
        for t, c in (("1", X_COLOR), (r"\text{col}_1", X_COLOR), ("2", Y_COLOR), (r"\text{col}_2", Y_COLOR)):
            eq1.set_color_by_tex(t, c)
        eq1.move_to([0, -2.3, 0])
        label_box(eq1)
        self.play(ApplyMatrix(A, grid), Transform(a1, a1t), Transform(a2, a2t), Transform(v, v1),
                  FadeOut(eq0), run_time=3)
        self.play(FadeIn(eq1), run_time=0.8)
        self.wait(2)
