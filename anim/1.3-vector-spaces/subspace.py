# Block 1.3, authored in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class SubspaceTest(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Part 1: Line through the origin (Subspace)
        line1 = Line(
            np.array([-4.5, -2.25, 0.0]),
            np.array([4.5, 2.25, 0.0]),
            stroke_width=4,
            color=RESULT_COLOR,
        )

        title1 = Tex(r"Test 1: Line through origin $L_1$", font_size=MIN_FONT, color=INK)
        title1.to_corner(UL, buff=0.4)
        title1.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # Frame 1 givens
        self.add(line1, title1)
        self.wait(1.2)

        # Vectors on L1
        v1_coords = np.array([2.0, 1.0, 0.0])
        w1_coords = np.array([-1.0, -0.5, 0.0])
        sum1_coords = v1_coords + w1_coords  # [1.0, 0.5, 0.0]

        v1_arrow = Arrow(
            ORIGIN,
            v1_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        v1_label = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        v1_label.next_to(v1_coords, DR, buff=0.15)
        v1_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w1_arrow = Arrow(
            ORIGIN,
            w1_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w1_label = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w1_label.next_to(w1_coords, UL, buff=0.15)
        w1_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            GrowArrow(v1_arrow),
            Write(v1_label),
            GrowArrow(w1_arrow),
            Write(w1_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # Tip to tail: shift w1 to tip of v1
        w1_shifted = Arrow(
            v1_coords,
            sum1_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w1_label_shifted = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w1_label_shifted.next_to(w1_shifted.get_center(), UL, buff=0.15)
        w1_label_shifted.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        sum1_arrow = Arrow(
            ORIGIN,
            sum1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        subspace_ok = Tex(
            r"$\vec{v} + \vec{w} \in L_1$ and $\vec{0} \in L_1 \implies$ Subspace",
            font_size=MIN_FONT - 4,
            color=RESULT_COLOR,
        )
        subspace_ok.to_edge(DOWN, buff=0.35)
        subspace_ok.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Transform(w1_arrow, w1_shifted),
            Transform(w1_label, w1_label_shifted),
            run_time=1.4,
        )
        self.play(
            GrowArrow(sum1_arrow),
            FadeIn(subspace_ok, shift=0.1 * DOWN),
            run_time=1.4,
        )
        self.wait(1.8)

        # Part 2: Line NOT through origin (Not a Subspace)
        title2 = Tex(
            r"Test 2: Line not through origin $L_2$",
            font_size=MIN_FONT,
            color=INK,
        )
        title2.to_corner(UL, buff=0.4)
        title2.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        line2 = Line(
            np.array([-4.5, 0.8, 0.0]),
            np.array([4.5, 0.8, 0.0]),
            stroke_width=4,
            color=HIGHLIGHT,
        )

        # Clear part 1 items
        self.play(
            FadeOut(title1),
            FadeIn(title2),
            FadeOut(line1),
            FadeIn(line2),
            FadeOut(v1_arrow),
            FadeOut(v1_label),
            FadeOut(w1_arrow),
            FadeOut(w1_label),
            FadeOut(sum1_arrow),
            FadeOut(subspace_ok),
            run_time=1.5,
        )
        self.wait(0.5)

        # Vectors on L2: tips land at y = 0.8
        v2_coords = np.array([1.2, 0.8, 0.0])
        w2_coords = np.array([-1.2, 0.8, 0.0])
        sum2_coords = v2_coords + w2_coords  # [0.0, 1.6, 0.0]

        v2_arrow = Arrow(
            ORIGIN,
            v2_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        v2_label = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        v2_label.next_to(v2_coords, UR, buff=0.15)
        v2_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w2_arrow = Arrow(
            ORIGIN,
            w2_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w2_label = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w2_label.next_to(w2_coords, UL, buff=0.15)
        w2_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            GrowArrow(v2_arrow),
            Write(v2_label),
            GrowArrow(w2_arrow),
            Write(w2_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # Tip to tail for part 2: shift w2 to tip of v2
        w2_shifted = Arrow(
            v2_coords,
            sum2_coords,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        w2_label_shifted = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        w2_label_shifted.next_to(w2_shifted.get_center(), UR, buff=0.15)
        w2_label_shifted.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        sum2_arrow = Arrow(
            ORIGIN,
            sum2_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        sum2_label = MathTex(r"\vec{v} + \vec{w}", font_size=MIN_FONT, color=RESULT_COLOR)
        sum2_label.next_to(sum2_coords, LEFT, buff=0.18)
        sum2_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        subspace_fail = Tex(
            r"$\vec{v} + \vec{w} \notin L_2$ and $\vec{0} \notin L_2 \implies$ NOT a subspace",
            font_size=MIN_FONT - 4,
            color=HIGHLIGHT,
        )
        subspace_fail.to_edge(DOWN, buff=0.35)
        subspace_fail.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Transform(w2_arrow, w2_shifted),
            Transform(w2_label, w2_label_shifted),
            run_time=1.4,
        )
        self.play(
            GrowArrow(sum2_arrow),
            Write(sum2_label),
            FadeIn(subspace_fail, shift=0.1 * DOWN),
            run_time=1.5,
        )
        self.wait(2.5)
