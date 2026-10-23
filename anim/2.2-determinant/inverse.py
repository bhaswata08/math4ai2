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
        cloud = dot_cloud((-1, 1), (-0.75, 0.75), step=0.25, radius=0.045)
        F = f_marker(scale=0.4).shift([-0.2, -0.27, 0])
        self.add(plane, cloud, F, lab_a)
        self.wait(1)
        self.play(move_dots(cloud, A), ApplyMatrix(A, F), run_time=3)
        self.wait(0.6)
        self.play(ReplacementTransform(lab_a, lab_i), run_time=0.6)
        self.play(move_dots(cloud, Ai), ApplyMatrix(Ai, F), run_time=3)
        eq = label_box(tag(r"A^{-1}A=I").to_corner(DR, buff=0.25))
        self.play(Write(eq), run_time=1)
        self.wait(1.3)
