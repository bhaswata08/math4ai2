"""Block 3.1: the block structure of A = U Sigma V^T, and erase-then-stretch.

Idea from Gilbert Strang's SVD lectures (shape of the three factors) and
Visual Kernel, "SEE Matrix" (dimension eraser followed by a stretch).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def mat(rows, entry_color=INK, h=0.55, v=0.5):
    M = Matrix(rows, element_to_mobject=MathTex,
               element_to_mobject_config={"font_size": MIN_FONT},
               h_buff=h, v_buff=v, bracket_h_buff=0.15)
    M.get_entries().set_color(entry_color)
    M.get_brackets().set_color(INK)
    return M


def build_blocks(m, n):
    """The four blocks for an m x n matrix A, as dict name -> (matrix, size label)."""
    A = mat([[r"\bullet"] * n for _ in range(m)], h=0.5, v=0.5)
    sig = mat([[(rf"\sigma_{i + 1}" if i == j else "0") for j in range(n)] for i in range(m)])
    ucols = [rf"\mathbf{{u}}_{i + 1}" for i in range(m)]
    U = mat([["|"] * m, ucols, ["|"] * m], RESULT_COLOR, h=0.5, v=0.45)
    dash = r"\text{--}\ "
    V = mat([[rf"\mathbf{{v}}_{i + 1}^T"] for i in range(n)], V_COLOR, h=0.5, v=0.75)
    return {
        "A": (A, rf"{m}\times {n}"),
        "S": (sig, rf"{m}\times {n}"),
        "U": (U, rf"{m}\times {m}"),
        "V": (V, rf"{n}\times {n}"),
    }


class _Shapes(Scene):
    m, n = 2, 3

    def construct(self):
        m, n = self.m, self.n
        blocks = build_blocks(m, n)
        eq = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=MIN_FONT, color=INK)
        eq[2].set_color(RESULT_COLOR)
        eq[4].set_color(V_COLOR)
        eq.to_edge(UP, buff=0.3)

        eqs = tex("=")
        row = VGroup(blocks["A"][0], eqs, blocks["U"][0], blocks["S"][0], blocks["V"][0])
        row.arrange(RIGHT, buff=0.2)
        row.move_to([0, -0.15, 0])
        assert row.width < 9.6, row.width

        sizes, notes = {}, {}
        for k, (M, s) in blocks.items():
            lab = tex(s, INK_DIM)
            lab.next_to(M, UP, buff=0.2)
            sizes[k] = lab
        top = max(l.get_top()[1] for l in sizes.values())
        for l in sizes.values():
            l.set_y(top - l.height / 2)
        bottom = min(M.get_bottom()[1] for M, _ in blocks.values())
        for k, word, name, col in (("U", "AA^T", "U", RESULT_COLOR), ("V", "A^TA", "V", V_COLOR)):
            n1 = Tex("eigenvectors", font_size=MIN_FONT, color=col)
            n2 = MathTex(rf"\text{{of }}{word}", font_size=MIN_FONT, color=col)
            g = VGroup(n1, n2).arrange(DOWN, buff=0.12)
            g.move_to([blocks[k][0].get_center()[0], bottom - 0.2 - g.height / 2, 0])
            notes[k] = g

        # first frame: the equation and A with its size
        self.add(eq, blocks["A"][0], sizes["A"])
        self.wait(1)
        self.play(FadeIn(eqs), run_time=0.4)
        order = [("U", 2, notes.get("U")), ("S", 3, None), ("V", 4, notes.get("V"))]
        for key, idx, note in order:
            M = blocks[key][0]
            adds = [FadeIn(M), FadeIn(sizes[key])]
            if note is not None:
                adds.append(FadeIn(note))
            hi = eq[idx]
            old = hi.get_color()
            self.play(hi.animate.set_color(HIGHLIGHT), *adds, run_time=1.0)
            self.play(hi.animate.set_color(old), run_time=0.4)
            self.wait(1.2)
        self.extra(blocks, sizes, eq)
        self.wait(1.2)

    def extra(self, blocks, sizes, eq):
        pass


class SVDShapes2x3(_Shapes):
    """A is 2x3: U is 2x2, Sigma is 2x3, V^T is 3x3."""
    m, n = 2, 3


class SVDShapes4x2(_Shapes):
    """A is 4x2: Sigma is 4x2, the two zero rows add the missing dimensions."""
    m, n = 4, 2

    def extra(self, blocks, sizes, eq):
        S = blocks["S"][0]
        zeros = VGroup(*[S.get_rows()[i][j] for i in (2, 3) for j in (0, 1)])
        self.play(zeros.animate.set_color(HIGHLIGHT), run_time=0.5)
        self.play(Indicate(zeros, color=HIGHLIGHT, scale_factor=1.2), run_time=1.0)
        self.play(sizes["A"].animate.set_color(HIGHLIGHT), sizes["S"].animate.set_color(HIGHLIGHT),
                  run_time=0.6)
        self.wait(1.0)
        self.play(zeros.animate.set_color(INK), sizes["A"].animate.set_color(INK_DIM),
                  sizes["S"].animate.set_color(INK_DIM), run_time=0.5)


class EraseThenStretch(ThreeDScene):
    """Eraser [[1,0,0],[0,1,0]] flattens a cylinder to a disc; [[4,0],[0,2]] stretches it."""

    def construct(self):
        plane = house_plane(x_range=[-5, 5, 1], y_range=[-3, 3, 1], x_length=10, y_length=6)
        plane.set_opacity(0.5)
        xax = Line([-3.2, 0, 0], [3.2, 0, 0], color=X_COLOR, stroke_width=4)
        yax = Line([0, -1.3, 0], [0, 1.3, 0], color=Y_COLOR, stroke_width=4)
        zax = Line([0, 0, -1.2], [0, 0, 1.2], color=INK_DIM, stroke_width=4)
        cyl = Cylinder(radius=0.5, height=1.2, direction=Z_AXIS, resolution=(12, 48),
                       fill_color=W_COLOR, fill_opacity=0.55, show_ends=True)
        cyl.set_stroke(INK, width=1, opacity=0.6)

        def fixed(*mobs):
            g = VGroup(*mobs)
            return g

        def caption(mat_s, word):
            m = tex(mat_s)
            w = Tex(word, font_size=MIN_FONT, color=INK)
            g = VGroup(m, w).arrange(RIGHT, buff=0.4)
            g.to_edge(UP, buff=0.2)
            return g

        cap1 = caption(r"\begin{bmatrix}1&0&0\\0&1&0\end{bmatrix}", "erase $z$")
        cap2 = caption(r"\begin{bmatrix}4&0\\0&2\end{bmatrix}", "stretch")
        prod = tex(r"\begin{bmatrix}4&0\\0&2\end{bmatrix}\begin{bmatrix}1&0&0\\0&1&0\end{bmatrix}="
                   r"\begin{bmatrix}4&0&0\\0&2&0\end{bmatrix}")
        prod.to_edge(UP, buff=0.2)
        for c in (cap1, cap2, prod):
            label_box(c, opacity=1.0, buff=0.12)
        assert prod.width < 9.7, prod.width

        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)
        self.add(plane, xax, yax, zax, cyl)
        self.add_fixed_in_frame_mobjects(cap1)
        self.add(cap1)
        self.wait(1.2)
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=3.5, added_anims=[
            cyl.animate.apply_matrix(np.diag([1, 1, 0.001])),
            zax.animate.apply_matrix(np.diag([1, 1, 0.001])),
        ])
        self.wait(0.5)
        self.play(FadeOut(cap1), run_time=0.4)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(FadeIn(cap2), run_time=0.4)
        self.play(cyl.animate.apply_matrix(np.diag([4, 2, 1])), run_time=3)
        self.wait(0.8)
        self.play(FadeOut(cap2), run_time=0.4)
        self.add_fixed_in_frame_mobjects(prod)
        self.play(FadeIn(prod), run_time=0.6)
        self.wait(1.5)
