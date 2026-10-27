"""Block 2.1: one vector, many vectors, and Av as a mix of columns.

Idea from Visual Kernel, "SEE Matrix" chapter 1, and 3Blue1Brown, Essence of Linear Algebra ch.3.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def arr(U, a, b, col, tip=0.18, sw=6):
    return Arrow([U * a[0], U * a[1], 0], [U * b[0], U * b[1], 0], buff=0, color=col, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25, tip_length=tip)


class OneVectorIn(Scene):
    """The matrix is on screen from the first frame; v goes in, Av comes out."""

    def construct(self):
        U = 0.8
        A = np.array([[1.0, 2.0], [0.0, 1.0]])
        plane = lin_plane(U)
        mat = matrix_tex([[1, 2], [0, 1]], col_colors=(None, None))
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        v = arr(U, (0, 0), (1, 2), V_COLOR)
        lv = label_box(MathTex(r"\mathbf v=(1,2)", font_size=MIN_FONT, color=V_COLOR))
        lv.next_to(v.get_end(), LEFT, buff=0.2)
        self.add(plane, mat, v, lv)
        self.wait(2.5)
        w = A @ np.array([1.0, 2.0])
        out = arr(U, (0, 0), w, RESULT_COLOR)
        lo = label_box(MathTex(r"A\mathbf v=(%g,%g)" % tuple(w), font_size=MIN_FONT, color=RESULT_COLOR))
        lo.move_to([2.4, 2.0, 0])
        ghost = v.copy().set_opacity(0.35)
        self.add(ghost)
        self.play(Transform(v, out), FadeOut(lv), run_time=2.5)
        self.play(FadeIn(lo), run_time=0.6)
        self.wait(4.5)


class ManyArrows(Scene):
    """24 arrows at equal angles. The same matrix moves every one; their order is kept."""

    def construct(self):
        U = 0.8
        A = np.array([[1.0, 2.0], [0.0, 1.0]])
        bg = ghost_plane(U)
        grid = lin_plane(U)
        mat = matrix_tex([[1, 2], [0, 1]], col_colors=(None, None))
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        n, R = 24, 1.6
        ang = [2 * np.pi * k / n for k in range(n)]
        src = [(R * np.cos(a), R * np.sin(a)) for a in ang]
        arrows = [arr(U, (0, 0), p, INK_DIM, tip=0.14, sw=4) for p in src]
        hi = 3
        arrows[hi].set_color(V_COLOR).set_stroke(width=7)
        self.add(bg, grid, *arrows, mat)
        arrows[hi].set_z_index(5)
        self.wait(1.5)
        dst = [arr(U, (0, 0), A @ np.array(p), INK_DIM, tip=0.14, sw=4) for p in src]
        dst[hi].set_color(RESULT_COLOR).set_stroke(width=7)
        self.play(ApplyMatrix(A, grid), *[Transform(a, d) for a, d in zip(arrows, dst)], run_time=3.5)
        self.wait(5)


class ColumnMixFormula(Scene):
    """Av = x col1 + y col2: two scalings, then a tip-to-tail sum. One fixed layout."""

    def construct(self):
        U = 0.8
        O = np.array([-2.0, -1.9, 0.0])
        a, b, c, d = 2, -1, 1, 1
        x, y = 2, 3
        col1, col2 = (a, c), (b, d)
        s1 = (x * a, x * c)
        s2 = (y * b, y * d)
        res = (s1[0] + s2[0], s1[1] + s2[1])
        assert res == (1, 5) and (a * x + b * y, c * x + d * y) == res

        def P(p):
            return O + np.array([U * p[0], U * p[1], 0.0])

        def A(p, q, col):
            return Arrow(P(p), P(q), buff=0, color=col, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25, tip_length=0.18)

        plane = lin_plane(U).shift(O)
        panel = Rectangle(width=3.5, height=5.625, fill_color=BG, fill_opacity=1, stroke_width=0)
        panel.move_to([5 - 3.5 / 2, 0, 0]).set_z_index(10)
        mat = matrix_tex([[a, b], [c, d]])
        vec = Matrix([[str(x)], [str(y)]], element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
                     v_buff=0.7, bracket_h_buff=0.15)
        vec.get_brackets().set_color(INK)
        vec.get_entries()[0].set_color(X_COLOR)
        vec.get_entries()[1].set_color(Y_COLOR)
        head = VGroup(mat, vec).arrange(RIGHT, buff=0.3).move_to([3.25, 2.0, 0]).set_z_index(11)
        g1 = A((0, 0), col1, X_COLOR)
        g2 = A((0, 0), col2, Y_COLOR)

        def lab(tex, col, anchor, direction):
            return label_box(MathTex(tex, font_size=MIN_FONT, color=col), opacity=1).next_to(anchor, direction, buff=0.15)

        l1 = lab(r"\text{col}_1", X_COLOR, P(col1), DOWN)
        l2 = lab(r"\text{col}_2", Y_COLOR, P(col2), LEFT)
        self.add(plane, g1, g2, l1, l2, panel, head)
        self.wait(1.5)

        def line(parts, colors, y):
            t = MathTex(*parts, font_size=MIN_FONT)
            for p, col in zip(t, colors):
                p.set_color(col)
            t.move_to([0, y, 0]).align_to([1.65, 0, 0], LEFT).set_z_index(11)
            return t

        eq1 = line([str(x), r"(%d,%d)=" % col1, "(%d,%d)" % s1], [X_COLOR, X_COLOR, RESULT_COLOR], 0.7)
        eq2 = line([str(y), r"(%d,%d)=" % col2, "(%d,%d)" % s2], [Y_COLOR, Y_COLOR, RESULT_COLOR], -0.1)
        eq3 = line([r"A\mathbf v=", "(%d,%d)" % s1, "+"], [INK, X_COLOR, INK], -1.1)
        eq4 = line(["(%d,%d)" % s2, "=", "(%d,%d)" % res], [Y_COLOR, INK, RESULT_COLOR], -1.8)

        self.play(Indicate(vec.get_entries()[0], color=HIGHLIGHT, scale_factor=1.5), run_time=1)
        self.play(Transform(g1, A((0, 0), s1, X_COLOR)), l1.animate.next_to(P(s1), UP, buff=0.2).shift(LEFT * 0.3),
                  FadeIn(eq1), run_time=2.5)
        self.wait(1.5)
        self.play(Indicate(vec.get_entries()[1], color=HIGHLIGHT, scale_factor=1.5), run_time=1)
        self.play(Transform(g2, A((0, 0), s2, Y_COLOR)), l2.animate.next_to(P(s2), UP, buff=0.15),
                  FadeIn(eq2), run_time=2.5)
        self.wait(1.5)
        self.play(FadeOut(l1), FadeOut(l2))
        self.play(Transform(g2, A(s1, res, Y_COLOR)), FadeIn(eq3), run_time=2)
        self.wait(1)
        total = A((0, 0), res, RESULT_COLOR)
        lt = lab("(%d,%d)" % res, RESULT_COLOR, P(res), RIGHT)
        self.play(GrowArrow(total), FadeIn(lt), FadeIn(eq4), run_time=2)
        self.wait(3)
