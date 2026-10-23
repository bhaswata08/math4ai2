"""Block 2.1: the transpose turns rows into columns.

Idea from Visual Kernel, "SEE Matrix" chapter 1 (matrices as arrays of numbers).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def mat(rows, fs, hb, vb=0.9):
    m = Matrix([[str(e) for e in r] for r in rows],
               element_to_mobject=lambda e: MathTex(e, font_size=fs, color=INK),
               h_buff=hb, v_buff=vb, bracket_h_buff=0.15)
    m.get_brackets().set_color(INK)
    return m


def tag(tex, below):
    t = MathTex(tex, font_size=56, color=INK_DIM)
    t.next_to(below, DOWN, buff=0.35)
    return t


class TransposeFlip(Scene):
    def construct(self):
        A = mat([[1, 2, 3], [4, 5, 6]], 56, 0.8)
        AT = mat([[1, 4], [2, 5], [3, 6]], 56, 0.8)
        A.move_to([-2.7, 0.3, 0])
        AT.move_to([2.7, 0.3, 0])
        A.get_rows()[0].set_color(V_COLOR)
        A.get_rows()[1].set_color(W_COLOR)
        arrow = MathTex(r"\longrightarrow", font_size=56)
        tA, tAT = tag("A", A), tag("A^{\\top}", AT)
        self.add(A, tA)
        self.wait(2)
        copies = VGroup(*[e.copy() for e in A.get_entries()])
        targets = AT.get_entries()
        order = [0, 2, 4, 1, 3, 5]
        self.play(FadeIn(arrow), FadeIn(AT.get_brackets()), FadeIn(tAT), run_time=0.6)
        self.play(*[Transform(copies[k], targets[order[k]].copy().set_color(copies[k].get_color()))
                    for k in range(6)], run_time=2.2)
        self.wait(1.0)

        note = MathTex(r"a_{13}=3 \;\to\; (A^{\top})_{31}=3", font_size=MIN_FONT, color=INK)
        note.move_to([0, -2.3, 0])
        self.play(Indicate(A.get_entries()[2], color=HIGHLIGHT, scale_factor=1.5),
                  Indicate(copies[2], color=HIGHLIGHT, scale_factor=1.5), FadeIn(note), run_time=1.5)
        self.wait(3.5)
