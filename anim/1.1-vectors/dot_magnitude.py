# Block 1.1. Authored for this course.

import numpy as np
from shared.anim.house import *


class DotAlignMagnitude(Scene):
    """A language model scores candidate next words by:
        score = h · w = ||h|| (||w|| cos θ) = ||h|| × shadow of w on h
    Direction picks the sign, length scales it.
    Four candidate words cover the 2x2 of alignment x magnitude:
        - spaghetti:   cos θ = +0.9, ||w|| = 6.0, shadow = +5.4,  score = +54
        - orecchiette: cos θ = +0.9, ||w|| = 1.5, shadow = +1.35, score = +13.5
        - sushi:       cos θ = -0.9, ||w|| = 6.0, shadow = -5.4,  score = -54
        - tacos:       cos θ = -0.9, ||w|| = 1.5, shadow = -1.35, score = -13.5
    Drawing scale: 2/3 scene unit per vector unit.
    """

    def construct(self):
        # 1. Fixed top-left caption
        top_cap = MathTex(
            r"\text{score} = ",
            r"h",
            r"\cdot",
            r"w",
            r"= \|h\| \times \text{shadow of }",
            r"w",
            r"\text{ on }",
            r"h",
            font_size=MIN_FONT,
        )
        top_cap[1].set_color(V_COLOR)
        top_cap[3].set_color(W_COLOR)
        top_cap[5].set_color(W_COLOR)
        top_cap[7].set_color(V_COLOR)
        top_cap.to_corner(UL, buff=0.40)
        top_cap.add_background_rectangle(color=BG, opacity=0.9, buff=0.10)

        # 2. Horizontal reference line through h across the frame
        Y0 = -0.30  # whole diagram sits a bit below centre to clear the top caption
        def P(x, y=0.0):
            return np.array([x, Y0 + y, 0.0])

        h_line = Line(P(-4.6), P(4.6), color=INK_DIM, stroke_width=2.0)

        # 3. Teal arrow h along +x from origin, drawn 2 units long (representing ||h|| = 10)
        h_arr = Arrow(P(0), P(2.0), buff=0, stroke_width=6,
                      max_tip_length_to_length_ratio=0.20, color=V_COLOR)
        l_h = MathTex(r"h", font_size=MIN_FONT + 4, color=V_COLOR)
        l_h.move_to(P(0.0, 0.50))
        l_h.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)

        # ||h|| note above the axis, directly above the h label, inside the wedge
        l_hnorm = MathTex(r"\|h\| = 10", font_size=MIN_FONT, color=INK_DIM)
        l_hnorm.move_to(P(0.0, 1.15))
        l_hnorm.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)

        # Drawing scale 2/3 scene unit per vector unit: long words 4.0, short 1.0
        sin_th = np.sqrt(0.19)
        cos_th = 0.9
        p_spag = P(4.0 * cos_th, 4.0 * sin_th)
        p_orec = P(1.0 * cos_th, -1.0 * sin_th)
        p_sush = P(-4.0 * cos_th, 4.0 * sin_th)
        p_taco = P(-1.0 * cos_th, -1.0 * sin_th)

        def word_arrow(tip, ratio):
            return Arrow(P(0), tip, buff=0, stroke_width=5.5,
                         max_tip_length_to_length_ratio=ratio, color=W_COLOR)

        a_spag = word_arrow(p_spag, 0.20)
        a_orec = word_arrow(p_orec, 0.35)
        a_sush = word_arrow(p_sush, 0.20)
        a_taco = word_arrow(p_taco, 0.35)

        def word_label(text, tip, direction, buff):
            lbl = Tex(text, font_size=MIN_FONT, color=W_COLOR)
            lbl.next_to(tip, direction, buff=buff)
            lbl.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
            return lbl

        lbl_spag = word_label("spaghetti", p_spag, UP, 0.10)
        lbl_sush = word_label("sushi", p_sush, UP, 0.10)
        lbl_orec = word_label("orecchiette", p_orec, DR, 0.08)
        lbl_taco = word_label("tacos", p_taco, DL, 0.08)

        # Dashed perpendicular drops to the h line
        def drop(p):
            return DashedLine(p, P(p[0]), color=INK_DIM, stroke_width=2.5, dash_length=0.07)
        d_spag, d_orec, d_sush, d_taco = drop(p_spag), drop(p_orec), drop(p_sush), drop(p_taco)

        # Shadows on the h line (length = score / ||h|| * 0.4 ... honest 4:1 ratio)
        # Long shadows just below the line so the teal h arrow stays visible;
        # short ones slightly lower and thicker so they read on top.
        sh_spag = Line(P(0, -0.04), P(3.6, -0.04), color=RESULT_COLOR, stroke_width=6)
        sh_sush = Line(P(0, -0.04), P(-3.6, -0.04), color=Y_COLOR, stroke_width=6)
        sh_orec = Line(P(0, -0.09), P(0.9, -0.09), color=RESULT_COLOR, stroke_width=10)
        sh_taco = Line(P(0, -0.09), P(-0.9, -0.09), color=Y_COLOR, stroke_width=10)

        # Score labels on one row under each shadow end
        SC_Y = -1.30
        def score(text, x, color):
            m = MathTex(text, font_size=MIN_FONT, color=color)
            m.move_to(P(x, SC_Y))
            m.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
            return m
        sc_spag = score(r"+54", 3.6, RESULT_COLOR)
        sc_orec = score(r"+13.5", 0.9, RESULT_COLOR)
        sc_sush = score(r"-54", -3.6, Y_COLOR)
        sc_taco = score(r"-13.5", -0.9, Y_COLOR)

        # End caption at bottom
        bot_cap = Tex("Direction picks the sign. Length scales it.", font_size=MIN_FONT, color=INK)
        bot_cap.to_edge(DOWN, buff=0.45)
        bot_cap.add_background_rectangle(color=BG, opacity=0.9, buff=0.10)

        # =========================================================================
        # ANIMATION SEQUENCE
        # =========================================================================

        # Beat 1: Frame 1 shows the givens (top caption, h line, h arrow and labels)
        self.add(top_cap, h_line, h_arr, l_h, l_hnorm)
        self.wait(1.5)

        # Beat 2: spaghetti arrow grows; dashed perpendicular drop; shadow segment +2.7; score +54
        self.play(GrowArrow(a_spag), FadeIn(lbl_spag), run_time=1.2)
        self.wait(0.2)
        self.play(Create(d_spag), run_time=0.8)
        self.wait(0.2)
        self.play(Create(sh_spag), run_time=0.8)
        self.play(FadeIn(sc_spag), run_time=0.6)
        self.wait(1.0)

        # Beat 3: orecchiette (short, aligned): shadow +0.675, label +13.5
        self.play(GrowArrow(a_orec), FadeIn(lbl_orec), run_time=1.0)
        self.wait(0.2)
        self.play(Create(d_orec), run_time=0.6)
        self.wait(0.2)
        self.play(Create(sh_orec), run_time=0.6)
        self.play(FadeIn(sc_orec), run_time=0.6)
        self.wait(1.0)

        # Beat 4: sushi (long, opposite): drop, shadow -2.7 in Y_COLOR, label -54
        self.play(GrowArrow(a_sush), FadeIn(lbl_sush), run_time=1.2)
        self.wait(0.2)
        self.play(Create(d_sush), run_time=0.8)
        self.wait(0.2)
        self.play(Create(sh_sush), run_time=0.8)
        self.play(FadeIn(sc_sush), run_time=0.6)
        self.wait(1.0)

        # Beat 5: tacos (short, opposite): shadow -0.675 in Y_COLOR, label -13.5
        self.play(GrowArrow(a_taco), FadeIn(lbl_taco), run_time=1.0)
        self.wait(0.2)
        self.play(Create(d_taco), run_time=0.6)
        self.wait(0.2)
        self.play(Create(sh_taco), run_time=0.6)
        self.play(FadeIn(sc_taco), run_time=0.6)
        self.wait(1.0)

        # Beat 6: End caption crossfaded in at bottom; final resting state hold
        self.play(FadeIn(bot_cap), run_time=1.2)
        self.wait(2.5)
