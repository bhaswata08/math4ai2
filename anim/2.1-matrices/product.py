"""Block 2.1: how a matrix product is built. Columns of AB, and one entry as row times column.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.4, and Visual Kernel, "SEE Matrix" chapter 1.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def arr(U, a, b, col, tip=0.18, sw=6):
    return Arrow([U * a[0], U * a[1], 0], [U * b[0], U * b[1], 0], buff=0, color=col, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25, tip_length=tip)


class MatrixProductColumns(Scene):
    """AB: apply B to the basis vectors, then A to where they landed."""

    def construct(self):
        U = 0.8
        A = np.array([[1.0, 2.0], [0.0, 1.0]])
        B = np.array([[2.0, 0.0], [1.0, 1.0]])
        AB = A @ B
        assert (AB == np.array([[4, 2], [1, 1]])).all()
        bg = ghost_plane(U)
        grid = lin_plane(U)
        matB = matrix_tex([[2, 0], [1, 1]])
        matA = matrix_tex([[1, 2], [0, 1]], col_colors=(None, None))
        nB = MathTex("B=", font_size=MIN_FONT)
        nA = MathTex("A=", font_size=MIN_FONT)
        gB = VGroup(nB, matB).arrange(RIGHT, buff=0.15).to_corner(DL, buff=0.25)
        gA = VGroup(nA, matA).arrange(RIGHT, buff=0.15).to_corner(DR, buff=0.25)
        rB = Rectangle(width=gB.width + 0.6, height=gB.height + 0.6, fill_color=BG, fill_opacity=1, stroke_width=0)
        rB.move_to(gB).set_z_index(10)
        rA = Rectangle(width=gA.width + 0.6, height=gA.height + 0.6, fill_color=BG, fill_opacity=1, stroke_width=0)
        rA.move_to(gA).set_z_index(10)
        gA.set_opacity(0.4)
        gB.set_z_index(11)
        gA.set_z_index(11)

        def lab(txt, col):
            return label_box(MathTex(txt, font_size=MIN_FONT, color=col), opacity=1).set_z_index(12)

        i0, j0 = basis_arrows(U * np.eye(2))
        li0 = lab(r"\hat\imath", X_COLOR).next_to(i0.get_end(), DOWN, buff=0.15)
        lj0 = lab(r"\hat\jmath", Y_COLOR).next_to(j0.get_end(), LEFT, buff=0.2)
        self.add(bg, grid, i0, j0, li0, lj0, rB, rA, gB, gA)
        self.wait(1.5)

        # B first
        i1, j1 = basis_arrows(U * B)
        li1 = lab("(%g,%g)" % tuple(B[:, 0]), X_COLOR).next_to(i1.get_end(), RIGHT, buff=0.15)
        lj1 = lab("(%g,%g)" % tuple(B[:, 1]), Y_COLOR).next_to(j1.get_end(), LEFT, buff=0.2)
        self.play(ApplyMatrix(B, grid), Transform(i0, i1), Transform(j0, j1),
                  FadeOut(li0), FadeOut(lj0), run_time=3)
        self.play(FadeIn(li1), FadeIn(lj1), run_time=0.6)
        self.wait(1.5)

        # then A, on the grid that is already bent
        self.play(gB.animate.set_opacity(0.4), gA.animate.set_opacity(1), run_time=0.8)
        i2, j2 = basis_arrows(U * AB)
        li2 = lab("(%g,%g)" % tuple(AB[:, 0]), X_COLOR).next_to(i2.get_end(), UP, buff=0.15)
        lj2 = lab("(%g,%g)" % tuple(AB[:, 1]), Y_COLOR).next_to(j2.get_end(), UP, buff=0.15)
        self.play(ApplyMatrix(A, grid), Transform(i0, i2), Transform(j0, j2),
                  FadeOut(li1), FadeOut(lj1), run_time=3)
        self.play(FadeIn(li2), FadeIn(lj2), run_time=0.6)
        self.wait(1.5)

        # AB written from the two landing points
        matAB = matrix_tex([[int(e) for e in r] for r in AB])
        gAB = VGroup(MathTex("AB=", font_size=MIN_FONT), matAB).arrange(RIGHT, buff=0.15).to_corner(DL, buff=0.25)
        rAB = Rectangle(width=gAB.width + 0.6, height=gAB.height + 0.6, fill_color=BG, fill_opacity=1, stroke_width=0)
        rAB.move_to(gAB).set_z_index(10)
        gAB.set_z_index(11)
        self.play(FadeOut(gB), FadeOut(gA), run_time=0.5)
        self.play(FadeIn(gAB), FadeIn(rAB), run_time=0.6)
        cols = matAB.get_columns()
        self.play(Indicate(cols[0], color=HIGHLIGHT, scale_factor=1.25), Indicate(li2[1:], color=HIGHLIGHT, scale_factor=1.2), run_time=1)
        self.play(Indicate(cols[1], color=HIGHLIGHT, scale_factor=1.25), Indicate(lj2[1:], color=HIGHLIGHT, scale_factor=1.2), run_time=1)
        eq = label_box(MathTex(r"(AB)\,\hat\imath = A\,(B\,\hat\imath)", font_size=MIN_FONT).move_to([0, 2.3, 0]), opacity=1).set_z_index(12)
        self.play(FadeIn(eq), run_time=0.8)
        self.wait(3)


def entry_mat(rows, fs, color, hb=0.8):
    m = Matrix([[str(e) for e in r] for r in rows],
               element_to_mobject=lambda e: MathTex(e, font_size=fs, color=color),
               h_buff=hb, v_buff=0.8, bracket_h_buff=0.15)
    m.get_brackets().set_color(INK)
    return m


class RowTimesColumn(Scene):
    """Entry (i,j) of AB: row i of A against column j of B."""

    def construct(self):
        a = [[1, 2], [3, 4]]
        b = [[0, 1], [1, 5]]
        c = [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        assert c == [[2, 11], [4, 23]]
        fs = 48
        MA, MB = entry_mat(a, fs, V_COLOR), entry_mat(b, fs, W_COLOR)
        MC = entry_mat(c, fs, RESULT_COLOR)
        MC.get_entries().set_opacity(0)
        row = VGroup(MA, MB, MathTex("=", font_size=fs), MC).arrange(RIGHT, buff=0.3).move_to([0, 1.25, 0])
        names = VGroup(MathTex("A", font_size=MIN_FONT, color=INK_DIM).next_to(MA, DOWN, buff=0.2),
                       MathTex("B", font_size=MIN_FONT, color=INK_DIM).next_to(MB, DOWN, buff=0.2),
                       MathTex("AB", font_size=MIN_FONT, color=INK_DIM).next_to(MC, DOWN, buff=0.2))
        self.add(row, names)
        self.wait(1.5)
        ea, eb, ec = MA.get_entries(), MB.get_entries(), MC.get_entries()
        box = None
        done = []
        calc = None
        for i in range(2):
            for j in range(2):
                ra = SurroundingRectangle(VGroup(ea[2 * i], ea[2 * i + 1]), color=HIGHLIGHT, buff=0.12)
                cb = SurroundingRectangle(VGroup(eb[j], eb[2 + j]), color=HIGHLIGHT, buff=0.12)
                parts = [str(a[i][0]), r"\cdot", str(b[0][j]), "+", str(a[i][1]), r"\cdot", str(b[1][j]), "=", str(c[i][j])]
                t = MathTex(*parts, font_size=56)
                for k, col in ((0, V_COLOR), (4, V_COLOR), (2, W_COLOR), (6, W_COLOR), (8, RESULT_COLOR)):
                    t[k].set_color(col)
                t.move_to([0, -1.5, 0])
                lab = MathTex(r"\text{row }%d\cdot\text{column }%d" % (i + 1, j + 1), font_size=MIN_FONT, color=INK_DIM)
                lab.move_to([0, -2.4, 0])
                if box is None:
                    self.play(Create(ra), Create(cb), run_time=0.8)
                else:
                    self.play(Transform(box[0], ra), Transform(box[1], cb), FadeOut(calc), FadeOut(lab_old), run_time=0.8)
                box = box or (ra, cb)
                self.play(FadeIn(t[:8]), FadeIn(lab), run_time=1)
                self.wait(0.8)
                res = t[8]
                self.play(FadeIn(res), run_time=0.5)
                self.play(res.copy().animate.scale(0.9).move_to(ec[2 * i + j].get_center()), run_time=0.8)
                ec[2 * i + j].set_opacity(1)
                calc, lab_old = t, lab
                self.wait(0.4)
        self.play(FadeOut(box[0]), FadeOut(box[1]), FadeOut(calc), FadeOut(lab_old), run_time=0.6)
        fin = MathTex(r"(AB)_{ij}=\text{row } i \text{ of } A\cdot\text{column } j \text{ of } B", font_size=MIN_FONT, color=INK)
        fin.move_to([0, -1.8, 0])
        self.play(FadeIn(fin))
        self.wait(2.5)
