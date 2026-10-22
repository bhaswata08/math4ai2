# Adapted from 3b1b/videos _2016/eola/chapter2.py VectorsToDotsScene, (c) 3Blue1Brown, CC BY-NC-SA 4.0
# Adapted from 3b1b/videos _2016/eola/chapter2.py WhenVectorsLineUp, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class SpanAsDots(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Given vectors v and w
        v_coords = np.array([1.5, 0.5, 0.0])
        w_coords = np.array([-0.6, 1.2, 0.0])

        v_arrow = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        v_label = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        v_label.next_to(v_coords, DR, buff=0.15)
        v_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w_arrow = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w_label = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w_label.next_to(w_coords, UL, buff=0.15)
        w_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title = Tex(r"Span of $\vec{v}$ and $\vec{w}$", font_size=MIN_FONT, color=INK)
        title.to_corner(UL, buff=0.4)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # Frame 1 givens
        self.add(v_arrow, v_label, w_arrow, w_label, title)
        self.wait(1.2)

        # 1. Sample combinations drawn as arrows
        sample_scalars = [
            (1.0, 1.0),
            (1.8, 0.3),
            (0.5, 1.4),
            (-1.2, 0.8),
            (-0.8, -1.2),
            (1.3, -1.0),
            (2.0, -0.4),
            (-1.6, -0.5),
            (0.2, 1.6),
            (-1.4, 1.1),
            (0.7, -1.5),
            (-1.2, -0.1),
            (1.4, 1.1),
            (-0.4, 1.6),
            (1.6, -1.2),
            (-1.5, -1.1),
        ]

        combo_arrows = []
        for a, b in sample_scalars:
            end_pt = a * v_coords + b * w_coords
            arrow = Arrow(
                ORIGIN,
                end_pt,
                buff=0,
                stroke_width=3.5,
                max_tip_length_to_length_ratio=0.2,
                color=RESULT_COLOR,
            )
            combo_arrows.append(arrow)

        combo_group = VGroup(*combo_arrows)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in combo_arrows], lag_ratio=0.05),
            run_time=2.2,
        )
        self.wait(0.8)

        # 2. Replace arrows with dots at tips
        dots = [
            Dot(a.get_end(), radius=0.08, color=RESULT_COLOR)
            for a in combo_arrows
        ]
        self.play(
            *[Transform(a, d) for a, d in zip(combo_arrows, dots)],
            run_time=1.8,
        )
        self.wait(0.8)

        # 3. Dense cloud of dots fills the 2D plane
        dense_dots = []
        for x in np.arange(-4.2, 4.3, 0.5):
            for y in np.arange(-2.2, 2.3, 0.5):
                dense_dots.append(
                    Dot(
                        np.array([x, y, 0.0]),
                        radius=0.05,
                        color=RESULT_COLOR,
                        fill_opacity=0.65,
                    )
                )

        dense_group = VGroup(*dense_dots)
        span_def = Tex(
            r"Span = set of all tips (full 2D plane)",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        span_def.to_edge(UP, buff=0.4)
        span_def.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            FadeOut(title),
            FadeIn(dense_group, lag_ratio=0.01),
            FadeIn(span_def, shift=0.1 * DOWN),
            run_time=2.5,
        )
        self.wait(2.5)


class SpanLine(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Part 1: Collinear vectors on the line y = 0.5 x
        v_coords = np.array([2.0, 1.0, 0.0])
        w_coords = np.array([1.0, 0.5, 0.0])

        v_arrow = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        v_label = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        v_label.next_to(v_coords, DR, buff=0.15)
        v_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w_arrow = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w_label = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w_label.next_to(w_coords, UL, buff=0.15)
        w_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title1 = Tex(r"When vectors line up:", font_size=MIN_FONT, color=INK)
        title1.to_corner(UL, buff=0.4)
        title1.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # Frame 1 givens
        self.add(v_arrow, v_label, w_arrow, w_label, title1)
        self.wait(1.5)

        # Combinations stay on the line
        combo_arrow = Arrow(
            ORIGIN,
            np.array([3.0, 1.5, 0.0]),
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        combo_label = MathTex(r"1.5\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        combo_label.next_to(np.array([3.0, 1.5, 0.0]), UP, buff=0.15)
        combo_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(GrowArrow(combo_arrow), Write(combo_label), run_time=1.5)
        self.wait(0.5)

        # Move to another combination on the line
        combo_arrow_neg = Arrow(
            ORIGIN,
            np.array([-2.4, -1.2, 0.0]),
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        combo_label_neg = MathTex(r"-1.2\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        combo_label_neg.next_to(np.array([-2.4, -1.2, 0.0]), DOWN, buff=0.15)
        combo_label_neg.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(combo_arrow, combo_arrow_neg),
            Transform(combo_label, combo_label_neg),
            run_time=1.8,
        )
        self.wait(0.5)

        # Full line span
        span_line = Line(
            np.array([-4.5, -2.25, 0.0]),
            np.array([4.5, 2.25, 0.0]),
            color=RESULT_COLOR,
            stroke_width=5,
        )
        line_desc = Tex(
            r"$\text{Span}(\vec{v}, \vec{w}) =$ line through origin",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        line_desc.next_to(title1, DOWN, buff=0.25, aligned_edge=LEFT)
        line_desc.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Create(span_line),
            FadeIn(line_desc, shift=0.1 * DOWN),
            FadeOut(combo_arrow),
            FadeOut(combo_label),
            run_time=2.0,
        )
        self.wait(2.0)

        # Part 2: Both vectors are zero
        title2 = Tex(r"When both vectors are zero:", font_size=MIN_FONT, color=INK)
        title2.to_corner(UL, buff=0.4)
        title2.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        zero_origin_dot = Dot(ORIGIN, radius=0.12, color=RESULT_COLOR)
        zero_desc = Tex(
            r"$\text{Span}(\vec{0}, \vec{0}) = \{\vec{0}\}$ (single point)",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        zero_desc.next_to(title2, DOWN, buff=0.25, aligned_edge=LEFT)
        zero_desc.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            FadeOut(title1),
            FadeIn(title2),
            FadeOut(span_line),
            FadeOut(line_desc),
            FadeOut(v_label),
            FadeOut(w_label),
            Transform(v_arrow, zero_origin_dot.copy()),
            Transform(w_arrow, zero_origin_dot.copy()),
            FadeIn(zero_origin_dot),
            FadeIn(zero_desc, shift=0.1 * DOWN),
            run_time=2.2,
        )
        self.wait(2.5)
