# Adapted from 3b1b/videos _2016/eola/chapter1.py CoordinateSystemWalkthrough, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class CoordinatePlane(Scene):
    def construct(self):
        # Base house number plane
        plane = house_plane()
        x_axis = plane.x_axis
        y_axis = plane.y_axis

        # Axis labels (MIN_FONT = 40), positioned well within the frame
        x_label = MathTex("x", font_size=MIN_FONT, color=INK_DIM)
        x_label.next_to(plane.c2p(4.7, 0), UL, buff=0.15)
        y_label = MathTex("y", font_size=MIN_FONT, color=INK_DIM)
        y_label.next_to(plane.c2p(0, 2.5), DR, buff=0.15)

        # 1. x axis visible on frame 1, then y axis
        self.add(x_axis, x_label)
        self.wait(0.5)
        self.play(Create(y_axis), Write(y_label), run_time=1.5)
        self.wait(0.5)

        # 2. "Origin" callout
        origin_dot = Dot(ORIGIN, radius=0.12, color=HIGHLIGHT)
        origin_text = Tex("Origin", font_size=MIN_FONT, color=INK)
        origin_text.shift(2.0 * UP + 2.5 * LEFT)
        origin_text.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        origin_line = Line(
            origin_text.get_bottom(),
            origin_dot.get_corner(UP + LEFT),
            color=HIGHLIGHT,
            stroke_width=3,
        )
        origin_group = VGroup(origin_text, origin_dot, origin_line)

        self.play(
            GrowFromCenter(origin_dot),
            Write(origin_text),
            Create(origin_line),
            run_time=1.5,
        )
        self.wait(1.5)
        self.play(FadeOut(origin_group), run_time=1.0)
        self.wait(0.5)

        # 3. Unit tick marks with a brace labelled 1 (within [-4.7, 4.7] x [-2.5, 2.5])
        x_ticks = VGroup(*[
            Line(plane.c2p(x, -0.12), plane.c2p(x, 0.12), color=INK_DIM, stroke_width=3)
            for x in range(-4, 5) if x != 0
        ])
        y_ticks = VGroup(*[
            Line(plane.c2p(-0.12, y), plane.c2p(0.12, y), color=INK_DIM, stroke_width=3)
            for y in range(-2, 3) if y != 0
        ])
        ticks = VGroup(x_ticks, y_ticks)

        unit_line = Line(ORIGIN, RIGHT)
        unit_brace = Brace(unit_line, DOWN, color=INK, buff=0.1)
        one = MathTex("1", font_size=MIN_FONT, color=INK).next_to(
            unit_brace, DOWN, buff=0.15
        )
        brace_group = VGroup(unit_brace, one)

        self.play(Create(ticks), run_time=1.2)
        self.play(GrowFromCenter(unit_brace), Write(one), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(brace_group), run_time=1.0)
        self.wait(0.5)

        # 4. Grid lines grow in
        self.play(Create(plane.background_lines), run_time=2.0)
        self.wait(2.0)


class CoordsToArrow(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Column vector [3, -1] written first
        col_vec = IntegerMatrix(
            [[3], [-1]],
            element_to_mobject_config={"font_size": MIN_FONT},
        )
        col_vec.to_corner(UL, buff=0.8)
        col_vec.get_brackets().set_color(INK)
        col_vec.get_entries()[0].set_color(X_COLOR)
        col_vec.get_entries()[1].set_color(Y_COLOR)
        col_vec.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(Write(col_vec), run_time=1.5)
        self.wait(1.0)

        # Walk 3 along x
        x_seg = Line(ORIGIN, 3.0 * RIGHT, stroke_width=6, color=X_COLOR)
        x_label = MathTex("3", font_size=MIN_FONT, color=X_COLOR)
        x_label.next_to(x_seg, UP, buff=0.2)
        x_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(x_seg), Write(x_label), run_time=1.5)
        self.wait(1.0)

        # Walk -1 along y
        y_seg = Line(3.0 * RIGHT, 3.0 * RIGHT + 1.0 * DOWN, stroke_width=6, color=Y_COLOR)
        y_label = MathTex("-1", font_size=MIN_FONT, color=Y_COLOR)
        y_label.next_to(y_seg, RIGHT, buff=0.2)
        y_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(y_seg), Write(y_label), run_time=1.5)
        self.wait(1.0)

        # Arrow grows to tip
        arrow = Arrow(
            ORIGIN,
            3.0 * RIGHT + 1.0 * DOWN,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        self.play(GrowArrow(arrow), run_time=1.5)
        self.wait(2.5)


class ArrowToCoords(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        target = np.array([-2.0, -1.5, 0.0])
        arrow = Arrow(
            ORIGIN,
            target,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )

        # 1. Arrow to (-2, -1.5) first
        self.play(GrowArrow(arrow), run_time=1.5)
        self.wait(1.0)

        # 2. Drop x and y components
        x_seg = Line(ORIGIN, -2.0 * RIGHT, stroke_width=6, color=X_COLOR)
        x_label = MathTex("-2", font_size=MIN_FONT, color=X_COLOR)
        x_label.next_to(x_seg, UP, buff=0.2)
        x_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        y_seg = Line(-2.0 * RIGHT, target, stroke_width=6, color=Y_COLOR)
        y_label = MathTex("-1.5", font_size=MIN_FONT, color=Y_COLOR)
        y_label.next_to(y_seg, LEFT, buff=0.2)
        y_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(x_seg), Write(x_label), run_time=1.5)
        self.play(Create(y_seg), Write(y_label), run_time=1.5)
        self.wait(1.0)

        # 3. Read off column vector
        col_vec = Matrix(
            [["-2"], ["-1.5"]],
            element_to_mobject_config={"font_size": MIN_FONT},
        )
        col_vec.to_corner(UR, buff=1.0)
        col_vec.get_brackets().set_color(INK)
        col_vec.get_entries()[0].set_color(X_COLOR)
        col_vec.get_entries()[1].set_color(Y_COLOR)
        col_vec.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            Write(col_vec),
            run_time=1.5,
        )
        self.wait(1.5)

        # 4. Point vs arrow contrast
        pt = Dot(target, radius=0.12, color=HIGHLIGHT)
        pt_label = Tex("Point $(-2, -1.5)$", font_size=MIN_FONT, color=HIGHLIGHT)
        pt_label.next_to(pt, DOWN, buff=0.25)
        pt_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
        pt_group = VGroup(pt, pt_label)

        self.play(FadeIn(pt_group), run_time=1.0)
        self.wait(1.0)
        self.play(
            col_vec.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=1.5,
        )
        self.play(FadeOut(pt_group), run_time=1.0)
        self.wait(2.0)
