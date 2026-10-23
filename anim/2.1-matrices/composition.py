"""Block 2.1: composing two maps. The order matters, and RS means S first.

Idea from Visual Kernel, "SEE Matrix" chapter 1 (matrix product as one map after another).
"""

from shared.anim.house import *
from shared.anim.linmap import *

U = 0.7
S = m2(1, 1, 0, 1)
R = m2(0, -1, 1, 0)
XR, YR, STEP = (-1.4, 1.4), (-1.0, 1.0), 0.15


def name_box(name, rows, corner=True):
    g = VGroup(MathTex(name + "=", font_size=MIN_FONT), matrix_tex(rows, col_colors=(None, None))).arrange(RIGHT, buff=0.2)
    if corner:
        g.to_corner(UL, buff=0.25)
    return label_box(g)


def caption(tex):
    c = MathTex(tex, font_size=MIN_FONT)
    c.move_to([-2.6, -2.3, 0])
    return label_box(c)


def fresh():
    f = f_marker(1.0)
    f.set_fill(INK, opacity=0.15)
    return VGroup(dot_cloud(XR, YR, step=STEP), f)


class ComposeMaps(Scene):
    def construct(self):
        plane = lin_plane(U)
        shape = fresh()
        dots, fm = shape[0], shape[1]
        cur = name_box("S", [[1, 1], [0, 1]])
        self.add(plane, shape, cur)
        self.wait(1)

        def apply(M):
            return AnimationGroup(move_dots(dots, M), ApplyMatrix(M[:2, :2], fm), run_time=2)

        def swap(new):
            nonlocal cur
            self.play(FadeTransform(cur, new), run_time=0.8)
            cur = new

        # first S, then R
        self.play(apply(S))
        self.wait(0.3)
        swap(name_box("R", [[0, -1], [1, 0]]))
        self.play(apply(R))
        cap1 = caption(r"\text{first } S \text{, then } R")
        self.play(FadeIn(cap1))
        swap(name_box("RS", [[0, -1], [1, 1]]))
        self.wait(1.2)
        shotA = shape.copy()

        # reset
        self.play(Transform(shape, fresh()), FadeOut(cap1), run_time=1.2)
        swap(name_box("R", [[0, -1], [1, 0]]))

        # first R, then S
        self.play(apply(R))
        swap(name_box("S", [[1, 1], [0, 1]]))
        self.play(apply(S))
        cap2 = caption(r"\text{first } R \text{, then } S")
        self.play(FadeIn(cap2))
        swap(name_box("SR", [[1, -1], [1, 0]]))
        self.wait(1.2)

        # side by side
        shotA.scale(0.65).move_to([-2.5, -0.7, 0])
        labA = name_box("RS", [[0, -1], [1, 1]], corner=False).move_to([-2.5, 1.95, 0])
        labB = name_box("SR", [[1, -1], [1, 0]], corner=False).move_to([2.5, 1.95, 0])
        self.play(FadeOut(plane), FadeOut(cap2), FadeOut(cur),
                  shape.animate.scale(0.65).move_to([2.5, -0.7, 0]), run_time=1.2)
        self.play(FadeIn(shotA), FadeIn(labA), FadeIn(labB), run_time=1)
        self.wait(2)
