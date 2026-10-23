"""Block 2.2: a matrix with no inverse, and one that can be undone.

Idea from Visual Kernel, SEE Matrix ch.1 (the dot engine) and
3Blue1Brown, Essence of Linear Algebra ch.7 (inverse matrices).
"""

from shared.anim.house import *
from shared.anim.linmap import *

U = 0.5


def tag(tex, color=INK):
    return MathTex(tex, font_size=MIN_FONT, color=color)


class NoInverse(Scene):
    """Projection onto the x axis: three different dots land on one point."""

    def construct(self):
        plane = lin_plane(U)
        M = np.array([[1.0, 0.0], [0.0, 0.0]])
        mat = matrix_tex([[1, 0], [0, 0]])
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        cloud = dot_cloud((-1.5, 1.5), (-1, 1), step=0.25, radius=0.045)
        picks = []
        for y in (0.75, 0.0, -0.75):
            d = min(cloud, key=lambda m: np.linalg.norm(m.get_center() - np.array([0.75, y, 0])))
            picks.append(d)
        self.add(plane, cloud, mat)
        self.wait(0.8)
        for d in picks:
            d.set_color(HIGHLIGHT).scale(1.9).set_z_index(5)
        self.play(*[Indicate(d, color=HIGHLIGHT, scale_factor=1.4) for d in picks], run_time=1)
        self.wait(0.4)
        self.play(move_dots(cloud, M), run_time=3)
        trace = DashedLine([0.75, 0.75, 0], [0.75, -0.75, 0], color=HIGHLIGHT, stroke_width=3, dash_length=0.1)
        trace.set_z_index(4)
        self.play(Create(trace), run_time=0.8)
        self.play(trace.animate.set_color(RESULT_COLOR),
                  *[d.animate.set_color(RESULT_COLOR) for d in picks], run_time=0.6)
        det = label_box(tag(r"\det A=0\iff\text{no inverse}").to_corner(UR, buff=0.25))
        many = label_box(tag(r"\text{many inputs}\to\text{one output}").to_corner(DL, buff=0.25))
        undo = label_box(tag(r"\text{nothing can undo it}", RESULT_COLOR).next_to(many, UP, buff=0.15, aligned_edge=LEFT))
        self.play(FadeIn(many), run_time=0.6)
        self.play(FadeIn(undo), run_time=0.6)
        self.play(FadeIn(det), run_time=0.8)
        self.wait(1.5)


class InverseUndo(Scene):
    """A moves the cloud and F; A^{-1} moves them back: A^{-1} A = I."""

    def construct(self):
        plane = lin_plane(U)
        A = np.array([[2.0, 1.0], [1.0, 1.0]])
        Ai = np.array([[1.0, -1.0], [-1.0, 2.0]])

        def corner(prefix, rows):
            g = VGroup(MathTex(prefix, font_size=MIN_FONT, color=INK), matrix_tex(rows)).arrange(RIGHT, buff=0.15)
            g.to_corner(UL, buff=0.25)
            return label_box(g)

        lab_a = corner("A=", [[2, 1], [1, 1]])
        lab_i = corner("A^{-1}=", [[1, -1], [-1, 2]])
        cloud = dot_cloud((-1.1, 1.1), (-0.8, 0.8), step=0.275, radius=0.06)
        F = f_marker(scale=0.75).shift([-0.4, -0.5, 0])
        self.add(plane, cloud, F, lab_a)
        self.wait(1)
        self.play(move_dots(cloud, A), ApplyMatrix(A, F), run_time=3)
        self.wait(2.0)
        self.play(ReplacementTransform(lab_a, lab_i), run_time=0.6)
        self.play(move_dots(cloud, Ai), ApplyMatrix(Ai, F), run_time=3)
        eq = label_box(tag(r"A^{-1}A=I").to_corner(DR, buff=0.25))
        self.play(Write(eq), run_time=1)
        self.wait(3.0)


class ScaleUndo(Scene):
    """A = 0.5 I shrinks the F and the grid; A^-1 = 2 I brings them back."""

    def construct(self):
        U = 0.6
        plane = lin_plane(U)
        A = 0.5 * np.eye(2)
        Ai = np.linalg.inv(A)
        assert np.allclose(Ai @ A, np.eye(2))

        def corner(prefix, M):
            g = VGroup(MathTex(prefix, font_size=MIN_FONT, color=INK),
                       matrix_tex(M.tolist())).arrange(RIGHT, buff=0.15)
            g.to_corner(UL, buff=0.25)
            return label_box(g)

        lab_a = corner("A=", A)
        lab_i = corner("A^{-1}=", Ai)
        F = f_marker(scale=1.2).shift([-0.6, -0.8, 0])
        ghost = f_marker(scale=1.2).shift([-0.6, -0.8, 0])
        ghost.set_fill(opacity=0).set_stroke(INK_FAINT, width=2)
        self.add(plane, ghost, F, lab_a)
        self.wait(2.0)
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, F), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lab_a), run_time=0.4)
        self.play(FadeIn(lab_i), run_time=0.4)
        self.play(ApplyMatrix(Ai, plane), ApplyMatrix(Ai, F), run_time=3)
        eq = label_box(tag(r"A^{-1}A=I").to_corner(DR, buff=0.25))
        self.play(Write(eq), run_time=1)
        self.wait(2.5)


class SolveAsCoordinates(Scene):
    """Ax = b: x tells how much of each column of A it takes to reach b."""

    def construct(self):
        U = 0.8
        A = np.array([[3.0, 1.0], [2.0, 2.0]])
        b = np.array([5.0, 6.0])
        Ai = np.linalg.inv(A)
        x = Ai @ b
        assert np.allclose(x, [1, 2]) and np.allclose(Ai, np.array([[2, -1], [-2, 3]]) / 4)
        o = np.array([-3.0, -2.4, 0])

        def P(px, py):
            return o + U * np.array([px, py, 0])

        plane = house_plane(x_range=[-20, 20, 1], y_range=[-12, 12, 1],
                            x_length=40 * U, y_length=24 * U).shift(o)
        plane.set_opacity(0.5)

        def grid(M):
            lines = VGroup()
            for k in range(-4, 8):
                for (p0, p1) in (((k, -4), (k, 8)), ((-4, k), (8, k))):
                    q0, q1 = M @ np.array(p0), M @ np.array(p1)
                    lines.add(Line(P(*q0), P(*q1), stroke_width=2, stroke_opacity=0.55,
                                   color=X_COLOR if p0[0] == p1[0] else Y_COLOR))
            return lines

        def arrow(p0, p1, color):
            return Arrow(P(*p0), P(*p1), buff=0, color=color, stroke_width=6, tip_length=0.18)

        c1, c2 = A[:, 0], A[:, 1]
        a1 = arrow((0, 0), c1, X_COLOR)
        bdot = Dot(P(*b), radius=0.12, color=RESULT_COLOR).set_z_index(6)
        blab = label_box(tag(rf"\mathbf{{b}}=({b[0]:g},{b[1]:g})", RESULT_COLOR).next_to(bdot, RIGHT, buff=0.2))
        mat = matrix_tex(A.tolist()).to_corner(UL, buff=0.25)
        label_box(mat)
        eqn = label_box(tag(r"A\mathbf{x}=\mathbf{b}").next_to(mat, RIGHT, buff=0.3))

        self.add(plane, a1, bdot, blab, mat, eqn)
        self.wait(2.0)

        G = grid(A)
        self.play(FadeIn(G), run_time=2)
        self.bring_to_back(plane)
        # one step along column 1, two along column 2, tip to tail
        s1 = arrow(c1, c1 + c2, Y_COLOR)
        s2 = arrow(c1 + c2, c1 + 2 * c2, Y_COLOR)
        self.play(GrowArrow(s1), run_time=1.2)
        self.play(GrowArrow(s2), run_time=1.2)
        read = MathTex(r"\mathbf{b}=", "1", r"\,\mathbf{a}_1", "+", "2", r"\,\mathbf{a}_2",
                       font_size=MIN_FONT, color=INK)
        read[1:3].set_color(X_COLOR)
        read[4:6].set_color(Y_COLOR)
        read.move_to([2.4, 0.5, 0])
        label_box(read)
        self.play(FadeIn(read), run_time=1.0)
        xlab = label_box(tag(rf"\mathbf{{x}}=({x[0]:g},{x[1]:g})", RESULT_COLOR).next_to(read, DOWN, buff=0.3))
        self.play(FadeIn(xlab), run_time=1.0)
        self.wait(2.5)

        # apply A^-1: the A-grid straightens, b slides to x
        inv_mat = VGroup(MathTex(r"A^{-1}=\tfrac14", font_size=MIN_FONT, color=INK),
                         matrix_tex((np.array([[2, -1], [-2, 3]])).tolist())).arrange(RIGHT, buff=0.15)
        inv_mat.to_corner(UR, buff=0.25)
        label_box(inv_mat)
        self.play(FadeOut(eqn), FadeIn(inv_mat), run_time=0.8)
        new_a1 = arrow((0, 0), Ai @ c1, X_COLOR)
        new_s1 = arrow(Ai @ c1, Ai @ (c1 + c2), Y_COLOR)
        new_s2 = arrow(Ai @ (c1 + c2), Ai @ (c1 + 2 * c2), Y_COLOR)
        self.play(ApplyMatrix(Ai, G, about_point=o), Transform(a1, new_a1), Transform(s1, new_s1),
                  Transform(s2, new_s2), bdot.animate.move_to(P(*x)),
                  FadeOut(blab), run_time=4)
        xp = label_box(tag(rf"({x[0]:g},{x[1]:g})", RESULT_COLOR).next_to(bdot, RIGHT, buff=0.2))
        self.play(FadeIn(xp), run_time=0.8)
        self.wait(2.0)
        chk = VGroup(tag(rf"3\cdot{x[0]:g}+1\cdot{x[1]:g}={A[0] @ x:g}"),
                     tag(rf"2\cdot{x[0]:g}+2\cdot{x[1]:g}={A[1] @ x:g}")).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        chk.move_to([2.7, -1.5, 0])
        label_box(chk)
        self.play(FadeIn(chk), run_time=1.0)
        self.wait(3.0)
