"""Block 2.1: a linear map plus a shift (affine map). The origin no longer stays put.

Idea from Visual Kernel, "SEE Matrix" chapter 1 (the dot engine, plus a shift).
"""

from shared.anim.house import *
from shared.anim.linmap import *


class AffineMap(Scene):
    def construct(self):
        U = 0.7
        A = m2(1.5, 0, 0.5, 1)
        plane = lin_plane(U)
        dots = dot_cloud((-1, 1), (-0.75, 0.75), step=0.125)
        fm = f_marker(0.55)
        fm.set_fill(INK, opacity=0.15)
        org = Dot(ORIGIN, radius=0.1, color=HIGHLIGHT)
        mat = matrix_tex([[1.5, 0], [0.5, 1]], col_colors=(None, None))
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        eq0 = label_box(MathTex(r"y=Ax", font_size=MIN_FONT).to_corner(UR, buff=0.25))
        eq1 = label_box(MathTex(r"y=Ax+b", font_size=MIN_FONT).to_corner(UR, buff=0.25))
        cap0 = label_box(MathTex(r"A\mathbf 0=\mathbf 0", font_size=MIN_FONT).move_to([0, -2.3, 0]))
        cap1 = label_box(MathTex(r"A\mathbf 0+b=b\neq \mathbf 0", font_size=MIN_FONT).move_to([0, -2.3, 0]))

        self.add(plane, dots, fm, org, mat, eq0)
        self.wait(1)
        self.play(move_dots(dots, A), ApplyMatrix(A[:2, :2], fm), run_time=2.5)
        self.play(FadeIn(cap0))
        self.wait(1)

        b = np.array([2 * U, 1 * U, 0.0])
        barrow = Arrow(ORIGIN, b, buff=0, color=RESULT_COLOR, stroke_width=6,
                       max_tip_length_to_length_ratio=0.25, tip_length=0.18)
        self.play(Transform(eq0, eq1), FadeOut(cap0))
        self.play(GrowArrow(barrow), run_time=0.8)
        self.play(shift_dots(dots, (2 * U, 1 * U)), fm.animate.shift(b), org.animate.shift(b),
                  run_time=2.5)
        self.bring_to_front(barrow, org)
        self.play(FadeIn(cap1))
        self.play(Indicate(org, color=HIGHLIGHT, scale_factor=2), run_time=1)
        self.wait(1.5)
