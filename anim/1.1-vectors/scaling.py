# Adapted from 3b1b/videos _2016/eola/chapter1.py ShowScalarMultiplication, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class ScalingStretch(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Base vector v = [2, 1]
        v_coords = np.array([2.0, 1.0, 0.0])
        v = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v.point_from_proportion(0.6), UL, buff=0.2)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # v is the given, on screen from frame one (the paused slide shows it).
        self.add(v, l_v)
        self.wait(1.5)

        # 1. Scale by 2 (stretch)
        scalar = MathTex("2", font_size=52, color=RESULT_COLOR)
        scalar.to_corner(UL, buff=0.8)
        scalar.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        v_2 = Arrow(
            ORIGIN,
            2.0 * v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_2 = MathTex(r"2\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_2.next_to(v_2.point_from_proportion(0.75), UL, buff=0.25)
        l_2.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Write(scalar),
            GrowArrow(v_2),
            Write(l_2),
            FadeOut(v),
            FadeOut(l_v),
            run_time=1.8,
        )
        self.wait(1.5)
        self.play(
            FadeOut(v_2),
            FadeOut(l_2),
            FadeIn(v),
            FadeIn(l_v),
            run_time=1.0,
        )
        self.wait(0.5)

        # 2. Scale by 1/3 (squish)
        scalar_third = MathTex(r"\frac{1}{3}", font_size=52, color=RESULT_COLOR)
        scalar_third.to_corner(UL, buff=0.8)
        scalar_third.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        v_third = Arrow(
            ORIGIN,
            (1.0 / 3.0) * v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_third = MathTex(r"\frac{1}{3}\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_third.next_to(v_third.point_from_proportion(0.5), DR, buff=0.25)
        l_third.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            FadeOut(scalar, shift=0.1 * UP),
            FadeIn(scalar_third, shift=0.1 * UP),
            GrowArrow(v_third),
            Write(l_third),
            run_time=1.8,
        )
        self.wait(1.5)
        self.play(FadeOut(v_third), FadeOut(l_third), run_time=1.0)
        self.wait(0.5)

        # 3. Scale by -1.8 (flip and stretch backwards)
        scalar_neg = MathTex(r"-1.8", font_size=52, color=RESULT_COLOR)
        scalar_neg.to_corner(UL, buff=0.8)
        scalar_neg.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        v_neg = Arrow(
            ORIGIN,
            -1.8 * v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_neg = MathTex(r"-1.8\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_neg.next_to(v_neg.point_from_proportion(0.55), UL, buff=0.35)
        l_neg.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            FadeOut(scalar_third, shift=0.1 * UP),
            FadeIn(scalar_neg, shift=0.1 * UP),
            GrowArrow(v_neg),
            Write(l_neg),
            run_time=2.0,
        )
        self.wait(2.5)


class ScalingNumerically(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Base vector v = [2, 1]
        v_coords = np.array([2.0, 1.0, 0.0])
        v = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v.point_from_proportion(0.6), UL, buff=0.2)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Components for v
        vx_line = Line(ORIGIN, 2.0 * RIGHT, stroke_width=5, color=X_COLOR)
        vy_line = Line(2.0 * RIGHT, v_coords, stroke_width=5, color=Y_COLOR)

        # v is the given, on screen from frame one (the paused slide shows it).
        self.add(v, l_v)
        self.wait(1.0)
        self.play(Create(vx_line), Create(vy_line), run_time=1.2)
        self.wait(0.8)

        # Concrete matrix calculation on top left:
        # 2 * [2, 1] = [2*2, 2*1] = [4, 2]
        two_dot = MathTex(r"2 \cdot", font_size=MIN_FONT, color=RESULT_COLOR)

        m_v = IntegerMatrix([[2], [1]], element_to_mobject_config={"font_size": MIN_FONT})
        m_v.get_brackets().set_color(INK)
        m_v.get_entries()[0].set_color(X_COLOR)
        m_v.get_entries()[1].set_color(Y_COLOR)

        eq1 = MathTex("=", font_size=MIN_FONT, color=INK)

        m_mid = Matrix(
            [[r"2 \cdot 2"], [r"2 \cdot 1"]],
            element_to_mobject_config={"font_size": MIN_FONT},
        )
        m_mid.get_brackets().set_color(INK)
        m_mid.get_entries()[0].set_color(X_COLOR)
        m_mid.get_entries()[1].set_color(Y_COLOR)

        eq2 = MathTex("=", font_size=MIN_FONT, color=INK)

        m_res = IntegerMatrix([[4], [2]], element_to_mobject_config={"font_size": MIN_FONT})
        m_res.get_brackets().set_color(INK)
        m_res.get_entries()[0].set_color(X_COLOR)
        m_res.get_entries()[1].set_color(Y_COLOR)

        concrete_eq = VGroup(two_dot, m_v, eq1, m_mid, eq2, m_res)
        concrete_eq.arrange(RIGHT, buff=0.12)
        concrete_eq.to_corner(UL, buff=0.35)
        concrete_eq.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            Write(concrete_eq),
            run_time=2.2,
        )
        self.wait(1.0)

        # Arrow grows to [4, 2]
        two_v = Arrow(
            ORIGIN,
            2.0 * v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        two_vx_line = Line(ORIGIN, 4.0 * RIGHT, stroke_width=5, color=X_COLOR)
        two_vy_line = Line(4.0 * RIGHT, 2.0 * v_coords, stroke_width=5, color=Y_COLOR)
        l_2v = MathTex(r"2\vec{v}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_2v.next_to(two_v.point_from_proportion(0.7), UL, buff=0.25)
        l_2v.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            GrowArrow(two_v),
            Transform(vx_line, two_vx_line),
            Transform(vy_line, two_vy_line),
            FadeOut(v),
            FadeOut(l_v),
            run_time=1.8,
        )
        self.play(Write(l_2v), run_time=0.8)
        self.wait(1.2)

        # General algebraic formula: 2 * [x, y] = [2x, 2y]
        two_dot_gen = MathTex(r"2 \cdot", font_size=MIN_FONT, color=RESULT_COLOR)

        m_gen_in = Matrix(
            [["x"], ["y"]], element_to_mobject_config={"font_size": MIN_FONT}
        )
        m_gen_in.get_brackets().set_color(INK)
        m_gen_in.get_entries()[0].set_color(X_COLOR)
        m_gen_in.get_entries()[1].set_color(Y_COLOR)

        eq_gen = MathTex("=", font_size=MIN_FONT, color=INK)

        m_gen_out = Matrix(
            [["2x"], ["2y"]], element_to_mobject_config={"font_size": MIN_FONT}
        )
        m_gen_out.get_brackets().set_color(INK)
        m_gen_out.get_entries()[0].set_color(X_COLOR)
        m_gen_out.get_entries()[1].set_color(Y_COLOR)

        general_eq = VGroup(two_dot_gen, m_gen_in, eq_gen, m_gen_out)
        general_eq.arrange(RIGHT, buff=0.2)
        general_eq.to_corner(UL, buff=0.35)
        general_eq.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            FadeOut(concrete_eq, shift=0.1 * UP),
            FadeIn(general_eq, shift=0.1 * UP),
            run_time=1.8,
        )
        self.wait(2.5)
