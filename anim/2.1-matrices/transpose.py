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
        self.wait(1)
        copies = VGroup(*[e.copy() for e in A.get_entries()])
        targets = AT.get_entries()
        order = [0, 2, 4, 1, 3, 5]
        self.play(FadeIn(arrow), FadeIn(AT.get_brackets()), FadeIn(tAT), run_time=0.6)
        self.play(*[Transform(copies[k], targets[order[k]].copy().set_color(copies[k].get_color()))
                    for k in range(6)], run_time=2.2)
        self.wait(1.5)

        self.play(FadeOut(VGroup(A, tA, AT.get_brackets(), tAT, arrow, copies)), run_time=0.6)
        B = mat([[1, 7, 8], [2, 5, 9], [3, 4, 6]], 52, 0.65)
        BT = mat([[1, 2, 3], [7, 5, 4], [8, 9, 6]], 52, 0.65)
        B.move_to([-2.7, 0.3, 0])
        BT.move_to([2.7, 0.3, 0])
        BT.get_entries().set_opacity(0)
        be = B.get_entries()
        for k in (1, 2, 5):
            be[k].set_color(V_COLOR)
        for k in (3, 6, 7):
            be[k].set_color(W_COLOR)
        tB, tBT = tag("B", B), tag("B^{\\top}", BT)
        arrow2 = MathTex(r"\longrightarrow", font_size=56)
        self.play(FadeIn(B), FadeIn(tB), run_time=0.8)
        self.play(*[Indicate(be[k], color=HIGHLIGHT, scale_factor=1.5) for k in (0, 4, 8)], run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(arrow2), FadeIn(BT.get_brackets()), FadeIn(tBT), run_time=0.6)
        bt = BT.get_entries()
        cps = [e.copy() for e in be]
        self.add(*cps)
        anims = []
        for k, e in enumerate(cps):
            i, j = divmod(k, 3)
            anims.append(e.animate.move_to(bt[j * 3 + i].get_center()))
        self.play(*anims, run_time=2.2)
        self.play(*[Indicate(cps[k], color=HIGHLIGHT, scale_factor=1.5) for k in (0, 4, 8)], run_time=1.0)
        self.wait(1.5)
