"""Block 2.4: repeated multiplication finds the top eigenvector.

Idea from Visual Kernel, "SEE Matrix" ch.2 and 3Blue1Brown,
Essence of Linear Algebra ch.14 (eigenvectors).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class PowerIteration(Scene):
    """x_k = A^k x0 / |A^k x0| swings onto the eigenvector with the largest eigenvalue."""

    def construct(self):
        U = 0.6
        plane = lin_plane(U)
        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        Ls = 2.4  # half-length of eigen-lines, scene units
        d1 = np.array([1, 1, 0]) / np.sqrt(2)
        d2 = np.array([1, -1, 0]) / np.sqrt(2)
        l1 = DashedLine(-Ls * d1, Ls * d1, color=W_COLOR, stroke_width=4)
        l2 = DashedLine(-Ls * d2, Ls * d2, color=INK_FAINT, stroke_width=4)
        lab1 = tex(r"\lambda=3", W_COLOR).next_to(Ls * d1, RIGHT, buff=0.15)
        lab2 = tex(r"\lambda=1", INK_DIM).next_to(Ls * d2, RIGHT, buff=0.15)
        label_box(lab1)
        label_box(lab2)

        mat = matrix_tex([[2, 1], [1, 2]], col_colors=(None, None))
        mat.to_corner(UL, buff=0.25)
        label_box(mat)
        rule = tex(r"\mathbf{x}_k=\frac{A^{k}\mathbf{x}_0}{\lVert A^{k}\mathbf{x}_0\rVert}")
        rule.to_corner(DL, buff=0.25)
        label_box(rule)

        k_lab = tex("k=")
        k_num = Integer(0, font_size=MIN_FONT, color=INK)
        kg = VGroup(k_lab, k_num).arrange(RIGHT, buff=0.12)
        kg.to_corner(UR, buff=0.25)
        label_box(kg)

        R = 1.9
        x = np.array([np.cos(np.radians(110)), np.sin(np.radians(110))])

        def arr(v, colour):
            return Arrow(ORIGIN, [v[0] * R, v[1] * R, 0], buff=0, color=colour, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25, tip_length=0.2)

        cur = arr(x, V_COLOR)
        self.add(plane, l1, l2, lab1, lab2, mat, rule, kg, cur)
        self.wait(1)
        trail = []
        for k in range(1, 7):
            x = A @ x
            x = x / np.linalg.norm(x)
            nxt = arr(x, RESULT_COLOR)
            new_k = Integer(k, font_size=MIN_FONT, color=INK).move_to(k_num, aligned_edge=LEFT)
            self.play(TransformFromCopy(cur, nxt), Transform(k_num, new_k), run_time=1.3)
            trail.append(cur)
            for i, old in enumerate(reversed(trail)):
                old.generate_target()
            self.play(*[old.animate.set_opacity(max(0.12, 0.6 - 0.15 * i))
                        for i, old in enumerate(reversed(trail))], run_time=0.3)
            cur = nxt
        self.wait(1.2)
