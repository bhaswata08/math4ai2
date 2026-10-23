"""Block 2.1: the Hadamard (entrywise) product, and masking with it.

Idea from Visual Kernel, "SEE Matrix" chapter 1 (matrices as arrays of numbers).
"""

from shared.anim.house import *
from shared.anim.linmap import *

FS = 52


def mat(rows, color):
    m = Matrix([[str(e) for e in r] for r in rows],
               element_to_mobject=lambda e: MathTex(e, font_size=FS, color=color),
               h_buff=0.75, v_buff=0.9, bracket_h_buff=0.15)
    m.get_brackets().set_color(INK)
    return m


def op(tex):
    return MathTex(tex, font_size=FS, color=INK)


def build(a, b, c, texts):
    A, B, C = mat(a, V_COLOR), mat(b, W_COLOR), mat(c, RESULT_COLOR)
    row = VGroup(A, op(r"\odot"), B, op("="), C).arrange(RIGHT, buff=0.25)
    cp = VGroup()
    for m, t in zip((A, B, C), texts):
        cp.add(MathTex(t, font_size=FS, color=INK_DIM).next_to(m, DOWN, buff=0.35))
    both = VGroup(row, cp).move_to(ORIGIN)
    C.get_entries().set_opacity(0)
    return both, A, B, C


def run(scene, A, B, C):
    for k in range(6):
        scene.play(Indicate(A.get_entries()[k], color=HIGHLIGHT, scale_factor=1.4),
                   Indicate(B.get_entries()[k], color=HIGHLIGHT, scale_factor=1.4),
                   C.get_entries()[k].animate.set_opacity(1), run_time=0.45)


class Hadamard(Scene):
    def construct(self):
        a = [[1, 2, 3], [4, 0, 2]]
        b = [[2, 1, 0], [1, 3, 2]]
        c = [[x * y for x, y in zip(r, s)] for r, s in zip(a, b)]
        g1, A, B, C = build(a, b, c, ["A", "B", r"A\odot B"])
        self.add(g1)
        self.wait(1)
        run(self, A, B, C)
        self.wait(1.5)

        m = [[1, 0, 1], [1, 1, 0]]
        h = [[3, 2, 5], [4, 1, 2]]
        r = [[x * y for x, y in zip(p, q)] for p, q in zip(m, h)]
        g2, M2, H2, R2 = build(m, h, r, [r"\text{mask}", r"\text{values}", r"\text{masked}"])
        self.play(FadeOut(g1), run_time=0.6)
        self.play(FadeIn(g2), run_time=0.8)
        self.wait(0.6)
        run(self, M2, H2, R2)
        self.wait(2.5)
