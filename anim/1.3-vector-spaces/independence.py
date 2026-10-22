# Adapted from 3b1b/videos _2016/eola/chapter2.py LinearDependentEquations, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class LinearDependence(Scene):
    def construct(self):
        # Frame 1 givens
        title_dep = Tex(r"Linearly Dependent", font_size=MIN_FONT + 6, color=HIGHLIGHT)
        title_dep.to_edge(UP, buff=0.45)
        title_dep.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # u = a v + b w
        eq_dep = MathTex(
            r"\vec{u}",
            r"=",
            r"a",
            r"\vec{v}",
            r"+",
            r"b",
            r"\vec{w}",
            font_size=MIN_FONT + 4,
        )
        eq_dep[0].set_color(HIGHLIGHT)
        eq_dep[1].set_color(INK)
        eq_dep[2].set_color(INK)
        eq_dep[3].set_color(V_COLOR)
        eq_dep[4].set_color(INK)
        eq_dep[5].set_color(INK)
        eq_dep[6].set_color(W_COLOR)
        eq_dep.shift(0.8 * UP)
        eq_dep.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        desc_dep = Tex(
            r"$\vec{u}$ is redundant: it adds no new dimension",
            font_size=MIN_FONT,
            color=INK,
        )
        desc_dep.next_to(eq_dep, DOWN, buff=0.45)
        desc_dep.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.add(title_dep, eq_dep, desc_dep)
        self.wait(1.8)

        # Symmetric form: c1 v + c2 w + c3 u = 0
        eq_sym = MathTex(
            r"a\vec{v} + b\vec{w} - 1\vec{u} = \vec{0}",
            font_size=MIN_FONT + 4,
        )
        eq_sym[0][:3].set_color(V_COLOR)
        eq_sym[0][3].set_color(INK)
        eq_sym[0][4:7].set_color(W_COLOR)
        eq_sym[0][7].set_color(INK)
        eq_sym[0][8:11].set_color(HIGHLIGHT)
        eq_sym[0][11:].set_color(INK)
        eq_sym.move_to(eq_dep)
        eq_sym.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        desc_sym = Tex(
            r"$c_1\vec{v} + c_2\vec{w} + c_3\vec{u} = \vec{0}$ with not all $c_i = 0$",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        desc_sym.next_to(eq_sym, DOWN, buff=0.45)
        desc_sym.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            FadeOut(eq_dep),
            FadeIn(eq_sym),
            FadeOut(desc_dep),
            FadeIn(desc_sym),
            run_time=2.0,
        )
        self.wait(2.2)

        # Contrast: Linearly Independent
        title_indep = Tex(
            r"Linearly Independent",
            font_size=MIN_FONT + 6,
            color=RESULT_COLOR,
        )
        title_indep.to_edge(UP, buff=0.45)
        title_indep.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        eq_indep = MathTex(
            r"c_1\vec{v} + c_2\vec{w} + c_3\vec{u} = \vec{0} \implies c_1 = c_2 = c_3 = 0",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        eq_indep.move_to(eq_sym)
        eq_indep.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        desc_indep = Tex(
            r"The ONLY combination giving $\vec{0}$ is all zero scalars",
            font_size=MIN_FONT,
            color=INK,
        )
        desc_indep.next_to(eq_indep, DOWN, buff=0.45)
        desc_indep.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        sub_desc = Tex(
            r"No vector can be formed from the others",
            font_size=MIN_FONT - 2,
            color=INK_DIM,
        )
        sub_desc.next_to(desc_indep, DOWN, buff=0.25)
        sub_desc.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            FadeOut(title_dep),
            FadeIn(title_indep),
            FadeOut(eq_sym),
            FadeIn(eq_indep),
            FadeOut(desc_sym),
            FadeIn(desc_indep),
            FadeIn(sub_desc),
            run_time=2.2,
        )
        self.wait(2.8)
