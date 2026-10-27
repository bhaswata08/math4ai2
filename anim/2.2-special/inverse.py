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
        det = label_box(tag(r"\text{flattened}\iff\text{no inverse}").to_corner(UR, buff=0.25))
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
        ghost_grid = ghost_plane(U)
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
        self.add(ghost_grid, plane, ghost, F, lab_a)
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
    """Ax = b: x counts steps along the columns of A that reach b. A^-1 turns
    the column grid back into the square grid, so those counts become b's
    ordinary coordinates."""

    def construct(self):
        U = 0.72
        A = np.array([[3.0, 1.0], [2.0, 2.0]])
        b = np.array([5.0, 6.0])
        Ai = np.linalg.inv(A)
        x = Ai @ b
        assert np.allclose(x, [1, 2])
        o = np.array([-4.3, -2.3, 0])
        PANEL_X = 1.15

        def P(px, py):
            return o + U * np.array([px, py, 0])

        plane = house_plane(x_range=[-8, 14, 1], y_range=[-6, 10, 1],
                            x_length=22 * U, y_length=16 * U)
        plane.shift(o - plane.c2p(0, 0))

        # the grid built from the columns: lines along a1 are green, along a2 rose
        G = VGroup()
        for k in range(-6, 11):
            G.add(Line(P(*(A @ [-6, k])), P(*(A @ [10, k])), stroke_width=2.5,
                       stroke_opacity=0.6, color=X_COLOR))
            G.add(Line(P(*(A @ [k, -6])), P(*(A @ [k, 10])), stroke_width=2.5,
                       stroke_opacity=0.6, color=Y_COLOR))

        def arrow(p0, p1, color):
            return Arrow(P(*p0), P(*p1), buff=0, color=color, stroke_width=7,
                         tip_length=0.2, max_tip_length_to_length_ratio=0.3).set_z_index(4)

        a1v, a2v = A[:, 0], A[:, 1]
        a1 = arrow((0, 0), a1v, X_COLOR)
        a2 = arrow((0, 0), a2v, Y_COLOR)
        l1 = MathTex(r"\mathbf{a}_1", font_size=MIN_FONT, color=X_COLOR).next_to(a1.get_center(), DR, buff=0.08)
        l2 = MathTex(r"\mathbf{a}_2", font_size=MIN_FONT, color=Y_COLOR).next_to(a2.get_center(), LEFT, buff=0.12)
        bdot = Dot(P(*b), radius=0.11, color=RESULT_COLOR).set_z_index(6)
        blab = MathTex(r"\mathbf{b}", font_size=MIN_FONT, color=RESULT_COLOR).next_to(bdot, RIGHT, buff=0.15)

        # right-hand panel: an opaque column the grid never draws over
        panel = Rectangle(width=10, height=6, stroke_width=0, fill_color=BG, fill_opacity=1)
        panel.next_to([PANEL_X, 0, 0], RIGHT, buff=0).set_z_index(10)
        edge = Line([PANEL_X, -2.9, 0], [PANEL_X, 2.9, 0], stroke_width=2, color=INK_FAINT).set_z_index(10)
        cx = (PANEL_X + 5) / 2

        def row(*parts):
            return MathTex(*parts, font_size=MIN_FONT, color=INK).set_z_index(11)

        mat = VGroup(row(r"A="), matrix_tex(A.tolist()).set_z_index(11)).arrange(RIGHT, buff=0.15)
        mat.move_to([cx, 1.85, 0])
        goal = row(r"x_1", r"\mathbf{a}_1", "+", r"x_2", r"\mathbf{a}_2", r"=\mathbf{b}")
        goal[1].set_color(X_COLOR)
        goal[4].set_color(Y_COLOR)
        goal[5][1].set_color(RESULT_COLOR)
        goal.move_to([cx, 0.45, 0])

        self.add(plane, panel, edge, a1, a2, l1, l2, bdot, blab, mat)
        self.wait(1.5)
        self.play(Write(goal), run_time=1.5)
        self.wait(2.0)

        # 1. swap the square grid for the grid built from a1 and a2
        self.play(plane.animate.set_stroke(opacity=0.15), FadeIn(G), run_time=2)
        self.wait(1.0)

        # 2. walk to b on that grid: one step of a1, then two steps of a2
        s1 = arrow(a1v, a1v + a2v, Y_COLOR)
        s2 = arrow(a1v + a2v, a1v + 2 * a2v, Y_COLOR)
        n1 = MathTex("1", font_size=MIN_FONT, color=X_COLOR).next_to(a1.get_center(), UL, buff=0.08)
        n2 = MathTex("1", font_size=MIN_FONT, color=Y_COLOR).next_to(s1.get_center(), RIGHT, buff=0.12)
        n3 = MathTex("2", font_size=MIN_FONT, color=Y_COLOR).next_to(s2.get_center(), RIGHT, buff=0.12)
        self.play(Indicate(a1, color=HIGHLIGHT, scale_factor=1.15), FadeIn(n1), run_time=1.0)
        self.play(GrowArrow(s1), FadeIn(n2), run_time=1.0)
        self.play(GrowArrow(s2), FadeIn(n3), run_time=1.0)
        self.wait(0.8)
        found = row("1", r"\mathbf{a}_1", "+", "2", r"\mathbf{a}_2", r"=\mathbf{b}")
        found[0:2].set_color(X_COLOR)
        found[3:5].set_color(Y_COLOR)
        found[5][1].set_color(RESULT_COLOR)
        found.move_to(goal)
        xrow = row(r"\mathbf{x}=(1,2)").set_color(RESULT_COLOR).move_to([cx, -0.6, 0])
        self.play(TransformMatchingTex(goal, found), run_time=1.2)
        self.play(FadeIn(xrow, shift=0.1 * DOWN), run_time=0.8)
        self.wait(2.5)

        # 3. A^-1 turns the slanted grid back into the square one; b lands on x
        inv = row(r"A^{-1}\mathbf{b}=\mathbf{x}").move_to([cx, -1.65, 0])
        self.play(FadeIn(inv), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(VGroup(l1, l2, n1, n2, n3, blab)), run_time=0.5)
        self.play(ApplyMatrix(Ai, G, about_point=o),
                  plane.animate.set_stroke(opacity=0.0),
                  Transform(a1, arrow((0, 0), (1, 0), X_COLOR)),
                  Transform(a2, arrow((0, 0), (0, 1), Y_COLOR)),
                  Transform(s1, arrow((1, 0), (1, 1), Y_COLOR)),
                  Transform(s2, arrow((1, 1), (1, 2), Y_COLOR)),
                  bdot.animate.move_to(P(*x)), run_time=4)
        xlab = MathTex(r"(1,2)", font_size=MIN_FONT, color=RESULT_COLOR).next_to(bdot, RIGHT, buff=0.15)
        self.play(FadeIn(xlab), Indicate(xrow, color=HIGHLIGHT, scale_factor=1.1), run_time=1.0)
        self.wait(3.0)
