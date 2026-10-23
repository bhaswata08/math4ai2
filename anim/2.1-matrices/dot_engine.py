"""Block 2.1: a matrix moves every point of the plane.

Idea from Visual Kernel, "SEE Matrix" chapter 1 (the dot engine).
"""

from shared.anim.house import *
from shared.anim.linmap import *


class DotEngine(Scene):
    """One matrix moves one vector, then every dot in a patch of the plane."""

    def construct(self):
        U = 0.8
        plane = lin_plane(U)
        M = m2(1, 2, 0, 1)
        mat = matrix_tex([[1, 2], [0, 1]], col_colors=(None, None))
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        self.add(plane, mat)

        v = Arrow(ORIGIN, [U, 2 * U, 0], buff=0, color=V_COLOR, stroke_width=6, max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        lab_in = MathTex("(1,2)", font_size=MIN_FONT, color=V_COLOR)
        lab_in.next_to(v.get_end(), LEFT, buff=0.2)
        label_box(lab_in)
        self.add(v, lab_in)
        self.wait(0.5)
        out = Arrow(ORIGIN, [5 * U, 2 * U, 0], buff=0, color=RESULT_COLOR, stroke_width=6, max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        lab_out = MathTex("(5,2)", font_size=MIN_FONT, color=RESULT_COLOR)
        lab_out.next_to(out.get_end(), UP, buff=0.2)
        label_box(lab_out)
        self.play(Transform(v, out), FadeOut(lab_in), run_time=2)
        self.play(FadeIn(lab_out), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(v), FadeOut(lab_out))

        dots = dot_cloud((-1.2, 1.2), (-0.8, 0.8), step=0.1)
        self.play(FadeIn(dots, lag_ratio=0.01), run_time=1.5)
        self.wait(0.5)
        self.play(move_dots(dots, M), run_time=3)
        self.wait(1)
