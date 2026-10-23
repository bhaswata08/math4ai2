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

        dots = dot_cloud((-1, 1), (-1, 2), step=0.125)
        for d in dots:
            d.set_color(INK_DIM).set_opacity(0.7)
        v = Arrow(ORIGIN, [U * 1, U * 2, 0], buff=0, color=V_COLOR, stroke_width=6,
                  max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        tip = Dot([U * 1, U * 2, 0], radius=0.08, color=V_COLOR)
        lab_in = MathTex("(1,2)", font_size=MIN_FONT, color=V_COLOR)
        lab_in.next_to(v.get_end(), LEFT, buff=0.2)
        label_box(lab_in)
        # the dot cloud lives in plane coordinates scaled by U
        dots.scale(U, about_point=ORIGIN)
        self.add(plane, mat, dots, v, tip, lab_in)
        self.wait(2)
        w = M @ np.array([1.0, 2.0, 1.0])
        assert (w[0], w[1]) == (5.0, 2.0)
        lab_out = MathTex("(5,2)", font_size=MIN_FONT, color=RESULT_COLOR)
        lab_out.move_to([U * 5, U * 2 + 0.55, 0])
        label_box(lab_out)
        MU = m2(1, 2, 0, 1)
        out = Arrow(ORIGIN, [U * 5, U * 2, 0], buff=0, color=RESULT_COLOR, stroke_width=6,
                    max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        self.play(move_dots(dots, MU), Transform(v, out), tip.animate.move_to([U * 5, U * 2, 0]),
                  FadeOut(lab_in), run_time=3.5)
        tip.set_color(RESULT_COLOR)
        self.play(FadeIn(lab_out), run_time=0.6)
        self.wait(4)
