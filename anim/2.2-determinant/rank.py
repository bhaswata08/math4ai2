"""Block 2.2: rank is the dimension of the output.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.7 (inverse matrices, column space, rank)
and Visual Kernel, SEE Matrix ch.1.
"""

from shared.anim.house import *
from shared.anim.linmap import *

U = 1.0


def tag(tex, color=INK):
    return MathTex(tex, font_size=MIN_FONT, color=color)


class RankOutputs(Scene):
    """The same dot cloud under a rank 2, a rank 1 and a rank 0 matrix."""

    def construct(self):
        plane = lin_plane(U)
        self.add(plane)

        beats = [
            ([[1, 0.5], [0.5, 1]], 2),
            ([[1, 1], [0.5, 0.5]], 1),
            ([[0, 0], [0, 0]], 0),
        ]
        for n, (rows, rank) in enumerate(beats):
            M = np.array(rows, dtype=float)
            mat = matrix_tex(rows)
            mat.to_corner(UL, buff=0.25)
            label_box(mat)
            cloud = disc_cloud(radius=1.6, step=0.14, dot_radius=0.04)
            i_hat, j_hat = basis_arrows(np.eye(2) * U)
            rk = MathTex(r"\text{rank}=", str(rank), font_size=MIN_FONT, color=INK)
            rk.to_corner(UR, buff=0.25)
            rk[1].set_color(RESULT_COLOR)
            label_box(rk)

            if n == 0:
                self.add(cloud, i_hat, j_hat, mat)
                self.wait(1)
            else:
                self.play(FadeIn(cloud), FadeIn(i_hat), FadeIn(j_hat), FadeIn(mat), run_time=0.6)
                self.wait(0.4)

            extra = []
            if rank == 1:
                d = np.array([1.0, 0.5, 0]) / np.linalg.norm([1.0, 0.5])
                span = Line(-3.3 * d, 3.3 * d, color=RESULT_COLOR,
                            stroke_width=5, stroke_opacity=0.4)
                self.add(span)
                self.bring_to_back(span)
                self.remove(plane)
                self.add(plane)
                self.bring_to_back(plane)
                span.set_opacity(0)
                extra.append(span)
            if rank == 0:
                shrink = ApplyMatrix(0.001 * np.eye(2), VGroup(i_hat, j_hat))
                self.play(move_dots(cloud, M), shrink, run_time=2.5)
                end = Dot(ORIGIN, radius=0.14, color=RESULT_COLOR).set_z_index(6)
                self.play(FadeIn(end, scale=3), run_time=0.5)
                extra.append(end)
            else:
                i2, j2 = basis_arrows(M * U)
                anims = [move_dots(cloud, M), Transform(i_hat, i2), Transform(j_hat, j2)]
                if rank == 1:
                    anims.append(extra[0].animate.set_stroke(opacity=0.4))
                self.play(*anims, run_time=2.5)
            self.play(FadeIn(rk), run_time=0.5)
            if rank == 1:
                dep = VGroup(tag(r"\text{columns lie}", RESULT_COLOR), tag(r"\text{on one line}", RESULT_COLOR))
                dep.arrange(DOWN, buff=0.1).move_to([3.4, -1.0, 0])
                label_box(dep)
                self.play(FadeIn(dep), run_time=0.5)
                extra.append(dep)
            self.wait(3.0)
            if n < len(beats) - 1:
                self.play(FadeOut(VGroup(cloud, i_hat, j_hat, mat, rk, *extra)), run_time=0.5)
        self.wait(0.4)
