# Adapted from 3b1b/videos _2016/eola/chapter1.py VectorAddition, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class AdditionTipToTail(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Vectors v = [1, 2], w = [3, -1]
        v1_coords = np.array([1.0, 2.0, 0.0])
        w_coords = np.array([3.0, -1.0, 0.0])
        sum_coords = v1_coords + w_coords  # [4, 1, 0]

        v1 = Arrow(
            ORIGIN,
            v1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l1 = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l1.next_to(np.array([0.0, 1.2, 0.0]), LEFT, buff=0.25)
        l1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        v2 = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l2 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l2.next_to(v2.point_from_proportion(0.5), DOWN, buff=0.25)
        l2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. v and w are the givens, so they are on screen from frame one:
        # the slide shows that frame before the clip plays.
        self.add(v1, l1, v2, l2)
        self.wait(1.5)
        self.wait(1.0)

        # 2. w slides to v's tip
        v2_group = VGroup(v2, l2)
        self.play(v2_group.animate.shift(v1_coords), run_time=2.0)
        self.wait(1.0)

        # 3. Sum v + w drawn with label
        v_sum = Arrow(
            ORIGIN,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_sum = MathTex(r"\vec{v} + \vec{w}", font_size=MIN_FONT, color=RESULT_COLOR)
        # Position clearly below the x-axis with a background rectangle
        l_sum.move_to(np.array([2.5, -0.65, 0.0]))
        l_sum.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(GrowArrow(v_sum), Write(l_sum), run_time=1.8)
        self.wait(2.5)


class AdditionWhyNotThis(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        v1_coords = np.array([1.0, 2.0, 0.0])
        w_coords = np.array([3.0, -1.0, 0.0])
        sum_coords = v1_coords + w_coords  # [4, 1, 0]

        v1 = Arrow(
            ORIGIN,
            v1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l1 = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l1.next_to(np.array([0.0, 1.2, 0.0]), LEFT, buff=0.25)
        l1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # w already at tip of v
        v2 = Arrow(
            v1_coords,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l2 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l2.next_to(v2.point_from_proportion(0.5), UR, buff=0.15)
        l2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        v_sum = Arrow(
            ORIGIN,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_sum = MathTex(r"\vec{v} + \vec{w}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_sum.move_to(np.array([2.5, -0.65, 0.0]))
        l_sum.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.add(v1, l1, v2, l2, v_sum, l_sum)
        self.wait(1.0)

        # 1. "Why?" callout
        why = Tex("Why?", font_size=MIN_FONT + 8, color=INK)
        why.to_corner(UR, buff=0.45)
        why.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(Write(why), run_time=1.0)
        self.wait(1.5)

        # 2. Wrong alternative: w back at origin, vector connecting tips
        w_at_origin = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l2_origin = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l2_origin.next_to(w_at_origin.point_from_proportion(0.5), DOWN, buff=0.25)
        l2_origin.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        wrong_vector = Arrow(
            v1_coords,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        why_not_this = Tex(r"Why not this?", font_size=MIN_FONT + 6, color=HIGHLIGHT)
        why_not_this.to_corner(UR, buff=0.45)
        why_not_this.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            FadeOut(why, shift=0.1 * UP),
            FadeIn(why_not_this, shift=0.1 * UP),
            Transform(v2, w_at_origin),
            Transform(l2, l2_origin),
            Transform(v_sum, wrong_vector),
            FadeOut(l_sum),
            run_time=2.0,
        )
        self.wait(2.0)

        # 3. Restore tip-to-tail setup
        v2_tip = Arrow(
            v1_coords,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l2_tip = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l2_tip.next_to(v2_tip.point_from_proportion(0.5), UR, buff=0.15)
        l2_tip.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        sum_restored = Arrow(
            ORIGIN,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        self.play(
            FadeOut(why_not_this, shift=0.1 * UP),
            Transform(v2, v2_tip),
            Transform(l2, l2_tip),
            Transform(v_sum, sum_restored),
            FadeIn(l_sum),
            run_time=1.5,
        )
        self.wait(1.0)

        # 4. Answer why: Dot walks along v then w, then along v+w
        dot = Dot(ORIGIN, radius=0.14, color=HIGHLIGHT)
        self.play(FadeIn(dot), run_time=0.6)

        # Walk along v
        self.play(dot.animate.move_to(v1_coords), run_time=1.5)
        self.wait(0.5)

        # Walk along w
        self.play(dot.animate.move_to(sum_coords), run_time=1.5)
        self.wait(1.0)

        # Reset to origin and walk along v+w
        self.play(dot.animate.move_to(ORIGIN), run_time=0.8)
        self.play(dot.animate.move_to(sum_coords), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(dot), run_time=0.8)
        self.wait(2.0)


class AdditionNumerically(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Vectors: v = [1, 2], w = [3, -1], sum = [4, 1]
        v1_coords = np.array([1.0, 2.0, 0.0])
        w_offset = np.array([3.0, -1.0, 0.0])
        sum_coords = v1_coords + w_offset  # [4, 1, 0]

        v1 = Arrow(
            ORIGIN,
            v1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        v2 = Arrow(
            v1_coords,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        v_sum = Arrow(
            ORIGIN,
            sum_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        # Draw arrows first
        self.play(GrowArrow(v1), run_time=1.2)
        self.play(GrowArrow(v2), run_time=1.2)
        self.play(GrowArrow(v_sum), run_time=1.2)
        self.wait(0.5)

        # Components for v1: 1 along x, 2 along y
        v1_x_line = Line(ORIGIN, 1.0 * RIGHT, stroke_width=5, color=X_COLOR)
        v1_y_line = Line(1.0 * RIGHT, v1_coords, stroke_width=5, color=Y_COLOR)

        # Components for v2: 3 along x, -1 along y
        v2_x_line = Line(v1_coords, v1_coords + 3.0 * RIGHT, stroke_width=5, color=X_COLOR)
        v2_y_line = Line(v1_coords + 3.0 * RIGHT, sum_coords, stroke_width=5, color=Y_COLOR)

        self.play(Create(v1_x_line), Create(v1_y_line), run_time=1.2)
        self.play(Create(v2_x_line), Create(v2_y_line), run_time=1.2)
        self.wait(0.8)

        # Braces along combined x and y motion
        # Combine x movements along x axis: 0 to 4
        x_total_line = Line(ORIGIN, 4.0 * RIGHT)
        x_brace = Brace(x_total_line, DOWN, color=X_COLOR, buff=0.1)
        x_calc = MathTex("1 + 3 = 4", font_size=MIN_FONT, color=X_COLOR).next_to(
            x_brace, DOWN, buff=0.15
        )
        x_calc.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Combine y movements: along y axis, y goes from 0 to 1
        y_total_line = Line(plane.c2p(0, 0), plane.c2p(0, 1))
        y_brace = Brace(y_total_line, LEFT, color=Y_COLOR, buff=0.1)
        y_calc = MathTex("2 + (-1) = 1", font_size=MIN_FONT, color=Y_COLOR)
        y_calc.next_to(y_brace, LEFT, buff=0.15)
        y_calc.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            GrowFromCenter(x_brace),
            Write(x_calc),
            GrowFromCenter(y_brace),
            Write(y_calc),
            run_time=1.5,
        )
        self.wait(1.0)

        # Numerical vector equation on top-left of the screen
        # [1, 2] + [3, -1] = [4, 1]
        eq_group = VGroup()
        m1 = IntegerMatrix([[1], [2]], element_to_mobject_config={"font_size": MIN_FONT})
        m1.get_brackets().set_color(INK)
        m1.get_entries()[0].set_color(X_COLOR)
        m1.get_entries()[1].set_color(Y_COLOR)

        plus = MathTex("+", font_size=MIN_FONT, color=INK)

        m2 = IntegerMatrix([[3], [-1]], element_to_mobject_config={"font_size": MIN_FONT})
        m2.get_brackets().set_color(INK)
        m2.get_entries()[0].set_color(X_COLOR)
        m2.get_entries()[1].set_color(Y_COLOR)

        equals = MathTex("=", font_size=MIN_FONT, color=INK)

        m3 = IntegerMatrix([[4], [1]], element_to_mobject_config={"font_size": MIN_FONT})
        m3.get_brackets().set_color(INK)
        m3.get_entries()[0].set_color(X_COLOR)
        m3.get_entries()[1].set_color(Y_COLOR)

        eq_group.add(m1, plus, m2, equals, m3)
        eq_group.arrange(RIGHT, buff=0.12)
        eq_group.to_corner(UL, buff=0.35)
        eq_group.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            Write(eq_group),
            run_time=2.0,
        )
        self.wait(2.5)
