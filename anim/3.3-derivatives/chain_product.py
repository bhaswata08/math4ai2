# Adapted from 3b1b/videos _2017/eoc/chapter4.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


class SumRule(Scene):
    def construct(self):
        # 1. Coordinate axes taking ~55% of frame width and ~75% of frame height (x_length=5.0, y_length=4.2)
        # Keeps graphs strictly on left half, completely isolated from right-hand equations
        axes = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[0, 3.2, 1.0],
            x_length=5.0,
            y_length=4.2,
            axis_config={"color": INK_DIM, "stroke_width": 2.5, "include_ticks": True},
        ).move_to(LEFT * 2.20 + UP * 0.05)

        x_axis_label = MathTex(r"x", font_size=MIN_FONT, color=INK_DIM).next_to(
            axes.x_axis.get_end(), RIGHT, buff=0.10
        )
        y_axis_label = MathTex(r"y", font_size=MIN_FONT, color=INK_DIM).next_to(
            axes.y_axis.get_end(), UP, buff=0.10
        )

        # Graphs: g(x) = sin(x), h(x) = x^2, f(x) = sin(x) + x^2
        g_graph = axes.plot(lambda x: np.sin(x), x_range=[0, 1.25], color=V_COLOR, stroke_width=3.5)
        h_graph = axes.plot(lambda x: x**2, x_range=[0, 1.35], color=W_COLOR, stroke_width=3.5)
        f_graph = axes.plot(
            lambda x: np.sin(x) + x**2, x_range=[0, 1.30], color=RESULT_COLOR, stroke_width=4.0
        )

        # Graph labels positioned cleanly outside the curve bundle
        f_label = MathTex(r"f = g + h", font_size=MIN_FONT, color=RESULT_COLOR)
        f_label.move_to(axes.c2p(0.80, np.sin(0.80) + 0.80**2) + LEFT * 0.95 + UP * 0.25)
        f_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        h_label = MathTex(r"h = x^2", font_size=MIN_FONT, color=W_COLOR)
        h_label.next_to(h_graph.get_end(), RIGHT, buff=0.10)
        h_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        g_label = MathTex(r"g = \sin(x)", font_size=MIN_FONT, color=V_COLOR)
        g_label.next_to(g_graph.get_end(), RIGHT, buff=0.10)
        g_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Top title on the left
        func_def = MathTex(
            r"f(x)", r"=", r"g(x)", r"+", r"h(x)", font_size=MIN_FONT
        )
        func_def[0].set_color(RESULT_COLOR)
        func_def[2].set_color(V_COLOR)
        func_def[4].set_color(W_COLOR)
        func_def.move_to(LEFT * 2.30 + UP * 2.38)
        func_def.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0 must already show the givens (never open on empty frame)
        self.add(
            axes,
            x_axis_label,
            y_axis_label,
            g_graph,
            h_graph,
            f_graph,
            g_label,
            h_label,
            f_label,
            func_def,
        )
        self.wait(0.8)

        # 2. Show vertical stacking at x = 0.50
        x_0 = 0.50
        g_0 = np.sin(x_0)
        h_0 = x_0**2
        f_0 = g_0 + h_0

        p_base = axes.c2p(x_0, 0)
        p_g = axes.c2p(x_0, g_0)
        p_sum = axes.c2p(x_0, f_0)

        line_g = Line(p_base, p_g, color=V_COLOR, stroke_width=5)
        line_h_base = Line(p_base, axes.c2p(x_0, h_0), color=W_COLOR, stroke_width=5)
        line_h_stacked = Line(p_g, p_sum, color=W_COLOR, stroke_width=5)

        x0_dot = Dot(p_base, color=INK, radius=0.06)

        self.play(Create(line_g), Create(line_h_base), FadeIn(x0_dot), run_time=1.2)
        self.wait(0.4)

        # Stack h on top of g to reach sum graph f
        self.play(
            Transform(line_h_base, line_h_stacked),
            run_time=1.4,
        )
        self.wait(0.6)

        # 3. Nudge x by dx (~0.3 in x-units): dx brace placed cleanly below x-axis
        dx_val = 0.30
        x_1 = x_0 + dx_val
        g_1 = np.sin(x_1)
        h_1 = x_1**2
        f_1 = g_1 + h_1

        p1_base = axes.c2p(x_1, 0)
        p1_g = axes.c2p(x_1, g_1)
        p1_sum = axes.c2p(x_1, f_1)

        dx_seg = Line(p_base, p1_base, color=X_COLOR, stroke_width=4)
        dx_brace = Brace(dx_seg, DOWN, buff=0.06)
        dx_label = MathTex(r"dx", color=X_COLOR, font_size=MIN_FONT).next_to(dx_brace, DOWN, buff=0.06)
        dx_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        line1_g = Line(p1_base, p1_g, color=V_COLOR, stroke_width=4)
        line1_h = Line(p1_g, p1_sum, color=W_COLOR, stroke_width=4)

        self.play(
            Create(dx_seg),
            Create(dx_brace),
            Write(dx_label),
            Create(line1_g),
            Create(line1_h),
            run_time=1.5,
        )
        self.wait(0.5)

        # 4. Show vertical increments:
        # dg and dh braces placed on the RIGHT of the x_1 line
        # df (total increment) brace placed on the LEFT of the x_1 line
        p1_g0 = axes.c2p(x_1, g_0)
        p1_f0 = axes.c2p(x_1, f_0)

        guide_g = DashedLine(p_g, p1_g0, color=INK_DIM, stroke_width=2)
        guide_f = DashedLine(p_sum, p1_f0, color=INK_DIM, stroke_width=2)

        inc_dg = Line(p1_g0, p1_g, color=V_COLOR, stroke_width=6)
        inc_dh = Line(axes.c2p(x_1, g_1 + h_0), p1_sum, color=W_COLOR, stroke_width=6)
        inc_df = Line(p1_f0, p1_sum, color=RESULT_COLOR, stroke_width=5)

        brace_dg = Brace(inc_dg, RIGHT, buff=0.06)
        lbl_dg = MathTex(r"dg", color=V_COLOR, font_size=MIN_FONT).next_to(brace_dg, RIGHT, buff=0.06)
        lbl_dg.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        brace_dh = Brace(inc_dh, RIGHT, buff=0.06)
        lbl_dh = MathTex(r"dh", color=W_COLOR, font_size=MIN_FONT).next_to(brace_dh, RIGHT, buff=0.06)
        lbl_dh.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        brace_df = Brace(inc_df, LEFT, buff=0.06)
        lbl_df = MathTex(r"df", color=RESULT_COLOR, font_size=MIN_FONT).next_to(brace_df, LEFT, buff=0.06)
        lbl_df.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(guide_g), Create(guide_f), run_time=0.8)
        self.play(
            Create(inc_dg),
            Create(brace_dg),
            Write(lbl_dg),
            Create(inc_dh),
            Create(brace_dh),
            Write(lbl_dh),
            run_time=1.4,
        )
        self.play(Create(inc_df), Create(brace_df), Write(lbl_df), run_time=1.0)
        self.wait(0.5)

        # 5. Formulas on the right side (centered at x = 2.75, completely clear of left half)
        eq_nudge = MathTex(r"df", r"=", r"dg", r"+", r"dh", font_size=MIN_FONT + 2)
        eq_nudge[0].set_color(RESULT_COLOR)
        eq_nudge[2].set_color(V_COLOR)
        eq_nudge[4].set_color(W_COLOR)
        eq_nudge.move_to(RIGHT * 2.75 + UP * 1.35)

        self.play(Write(eq_nudge), run_time=1.2)
        self.wait(0.6)

        eq_ratio = MathTex(
            r"\frac{df}{dx}", r"=", r"\frac{dg}{dx}", r"+", r"\frac{dh}{dx}", font_size=MIN_FONT
        )
        eq_ratio[0].set_color(RESULT_COLOR)
        eq_ratio[2].set_color(V_COLOR)
        eq_ratio[4].set_color(W_COLOR)
        eq_ratio.move_to(RIGHT * 2.75 + UP * 0.05)

        self.play(Write(eq_ratio), run_time=1.2)
        self.wait(0.6)

        # End by boxing the derivative form: the full d/dx(g+h) line is too
        # wide for the right column without hitting the g label or x axis.
        final_box = SurroundingRectangle(eq_ratio, color=RESULT_COLOR, buff=0.15, stroke_width=2)

        self.play(FadeIn(final_box), run_time=0.6)
        self.wait(2.0)


class ProductAsArea(Scene):
    def construct(self):
        # 1. Main box with width g(x) and height h(x)
        # Shifted left so the right column has plenty of room without edge clipping
        box_w = 2.2
        box_h = 1.8
        box_center = LEFT * 2.5 + DOWN * 0.45

        base_box = Rectangle(
            width=box_w,
            height=box_h,
            stroke_color=INK_DIM,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.6,
        ).move_to(box_center)

        top_brace = Brace(base_box, UP, buff=0.08)
        top_label = MathTex(r"g", color=V_COLOR, font_size=MIN_FONT).next_to(top_brace, UP, buff=0.08)

        left_brace = Brace(base_box, LEFT, buff=0.08)
        left_label = MathTex(r"h", color=W_COLOR, font_size=MIN_FONT).next_to(left_brace, LEFT, buff=0.08)

        area_label = MathTex(r"\text{Area} = gh", color=RESULT_COLOR, font_size=MIN_FONT).move_to(
            base_box.get_center()
        )

        # Title on the right side
        prod_title = MathTex(r"f(x) = g(x) \cdot h(x)", font_size=MIN_FONT + 2)
        prod_title.set_color_by_tex(r"g(x)", V_COLOR)
        prod_title.set_color_by_tex(r"h(x)", W_COLOR)
        prod_title.set_color_by_tex(r"f(x)", RESULT_COLOR)
        prod_title.move_to(RIGHT * 2.05 + UP * 2.15)

        # Frame 0 setup
        self.add(base_box, top_brace, top_label, left_brace, left_label, area_label, prod_title)
        self.wait(0.8)

        # 2. Nudge x: width grows by dg, height grows by dh
        dg_val = 0.60
        dh_val = 0.50

        right_strip = Rectangle(
            width=dg_val,
            height=box_h,
            stroke_color=RESULT_COLOR,
            stroke_width=2,
            fill_color=V_COLOR,
            fill_opacity=0.35,
        ).next_to(base_box, RIGHT, buff=0)

        bottom_strip = Rectangle(
            width=box_w,
            height=dh_val,
            stroke_color=RESULT_COLOR,
            stroke_width=2,
            fill_color=W_COLOR,
            fill_opacity=0.35,
        ).next_to(base_box, DOWN, buff=0)

        corner_strip = Rectangle(
            width=dg_val,
            height=dh_val,
            stroke_color=INK_FAINT,
            stroke_width=1.5,
            fill_color=INK_FAINT,
            fill_opacity=0.25,
        ).next_to(bottom_strip, RIGHT, buff=0)

        # Braces for the nudges
        dg_brace = Brace(right_strip, UP, buff=0.08)
        dg_label = MathTex(r"dg", color=V_COLOR, font_size=MIN_FONT).next_to(dg_brace, UP, buff=0.08)

        dh_brace = Brace(bottom_strip, LEFT, buff=0.08)
        dh_label = MathTex(r"dh", color=W_COLOR, font_size=MIN_FONT).next_to(dh_brace, LEFT, buff=0.08)

        self.play(
            FadeIn(right_strip),
            Create(dg_brace),
            Write(dg_label),
            FadeIn(bottom_strip),
            Create(dh_brace),
            Write(dh_label),
            FadeIn(corner_strip),
            run_time=1.8,
        )
        self.wait(0.6)

        # Labels for the three increment areas outside the box, keeping interior clean
        right_area = MathTex(r"h\,dg", color=RESULT_COLOR, font_size=MIN_FONT).next_to(
            right_strip, RIGHT, buff=0.15
        )
        right_area.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        bottom_area = MathTex(r"g\,dh", color=RESULT_COLOR, font_size=MIN_FONT).next_to(
            bottom_strip, DOWN, buff=0.15
        )
        bottom_area.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        corner_area = MathTex(r"dg\,dh", color=INK_FAINT, font_size=MIN_FONT).next_to(
            corner_strip, DOWN + RIGHT, buff=0.15
        )
        corner_area.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        self.play(Write(right_area), Write(bottom_area), Write(corner_area), run_time=1.2)
        self.wait(0.6)

        # 3. Write differential equation on the right side (centered at x = 2.05 to avoid edge clipping)
        eq1 = MathTex(
            r"d(gh)", r"=", r"g\,dh", r"+", r"h\,dg", r"+", r"dg\,dh", font_size=MIN_FONT
        )
        eq1[0].set_color(RESULT_COLOR)
        eq1[2].set_color(RESULT_COLOR)
        eq1[4].set_color(RESULT_COLOR)
        eq1[6].set_color(INK_FAINT)
        eq1.move_to(RIGHT * 2.05 + UP * 1.25)

        self.play(Write(eq1), run_time=1.4)
        self.wait(0.6)

        # Point out corner is negligible: dg dh -> 0
        slash = Line(eq1[6].get_corner(DL), eq1[6].get_corner(UR), color=INK_FAINT, stroke_width=2.5)
        approx_zero = MathTex(r"\approx 0", color=INK_FAINT, font_size=MIN_FONT).next_to(
            eq1[6], UP, buff=0.12
        )

        self.play(Create(slash), Write(approx_zero), run_time=0.8)
        self.wait(0.6)

        # End on d(gh) = g dh + h dg
        eq2 = MathTex(r"d(gh)", r"=", r"g\,dh", r"+", r"h\,dg", font_size=MIN_FONT + 4)
        eq2[0].set_color(RESULT_COLOR)
        eq2[2].set_color(V_COLOR)
        eq2[4].set_color(W_COLOR)
        eq2.move_to(RIGHT * 2.05 + UP * 0.15)

        self.play(Write(eq2), run_time=1.2)
        self.wait(0.6)

        # And the mnemonic "left d-right + right d-left" as MathTex \text{}
        mnemonic = MathTex(
            r"\text{``left } d\text{-right} + \text{right } d\text{-left''}",
            font_size=MIN_FONT,
        )
        mnemonic.set_color_by_tex(r"left", V_COLOR)
        mnemonic.set_color_by_tex(r"right", W_COLOR)
        mnemonic.move_to(RIGHT * 2.05 + DOWN * 1.2)

        mnemonic_box = SurroundingRectangle(mnemonic, color=RESULT_COLOR, buff=0.12, stroke_width=2)

        self.play(Write(mnemonic), run_time=1.0)
        self.play(FadeIn(mnemonic_box), run_time=0.6)
        self.wait(2.0)


class ChainRuleLines(Scene):
    def construct(self):
        # 1. Three horizontal number lines labelled x, h = x^2, g(h) = sin(h)
        # Centered at x = -0.35, length 4.4 units; right arrows and labels comfortably within frame (x < 4.1)
        line_x_center = -0.35
        line_length = 4.4

        line1 = NumberLine(
            x_range=[0, 2.0, 0.5],
            length=line_length,
            color=INK_DIM,
            stroke_width=2.5,
            include_numbers=False,
            include_ticks=True,
        ).move_to(RIGHT * line_x_center + UP * 1.85)

        line2 = NumberLine(
            x_range=[0, 3.0, 0.5],
            length=line_length,
            color=INK_DIM,
            stroke_width=2.5,
            include_numbers=False,
            include_ticks=True,
        ).move_to(RIGHT * line_x_center + UP * 0.60)

        # Widen line 3 range to [-1.0, 1.5] so d sin dot and interval never run off the end
        line3 = NumberLine(
            x_range=[-1.0, 1.5, 0.5],
            length=line_length,
            color=INK_DIM,
            stroke_width=2.5,
            include_numbers=False,
            include_ticks=True,
        ).move_to(RIGHT * line_x_center + DOWN * 0.65)

        # Labels on the left: level with their lines, right-aligned in one single column
        col_x = -2.85
        lbl_line1 = MathTex(r"x", color=X_COLOR, font_size=MIN_FONT).move_to(
            np.array([col_x, line1.get_y(), 0]), aligned_edge=RIGHT
        )
        lbl_line2 = MathTex(r"h = x^2", color=W_COLOR, font_size=MIN_FONT).move_to(
            np.array([col_x, line2.get_y(), 0]), aligned_edge=RIGHT
        )
        lbl_line3 = MathTex(r"g = \sin(h)", color=RESULT_COLOR, font_size=MIN_FONT).move_to(
            np.array([col_x, line3.get_y(), 0]), aligned_edge=RIGHT
        )

        for lbl in [lbl_line1, lbl_line2, lbl_line3]:
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # ValueTracker for x: sweep keeps dot and interval well inside all lines
        x_init = 0.75
        dx_val = 0.10
        tracker = ValueTracker(x_init)

        # Dynamic dots on the three lines
        dot1 = always_redraw(
            lambda: Dot(line1.n2p(tracker.get_value()), color=X_COLOR, radius=0.08)
        )
        dot2 = always_redraw(
            lambda: Dot(line2.n2p(tracker.get_value() ** 2), color=W_COLOR, radius=0.08)
        )
        dot3 = always_redraw(
            lambda: Dot(line3.n2p(np.sin(tracker.get_value() ** 2)), color=RESULT_COLOR, radius=0.08)
        )

        # Dynamic intervals on each line
        int1 = always_redraw(
            lambda: Line(
                line1.n2p(tracker.get_value()),
                line1.n2p(tracker.get_value() + dx_val),
                color=X_COLOR,
                stroke_width=6,
            )
        )
        int2 = always_redraw(
            lambda: Line(
                line2.n2p(tracker.get_value() ** 2),
                line2.n2p((tracker.get_value() + dx_val) ** 2),
                color=W_COLOR,
                stroke_width=6,
            )
        )
        int3 = always_redraw(
            lambda: Line(
                line3.n2p(np.sin(tracker.get_value() ** 2)),
                line3.n2p(np.sin((tracker.get_value() + dx_val) ** 2)),
                color=RESULT_COLOR,
                stroke_width=6,
            )
        )

        # Dynamic interval tags directly above the moving intervals
        lbl_int1 = always_redraw(
            lambda: MathTex(r"dx", color=X_COLOR, font_size=MIN_FONT)
            .next_to(line1.n2p(tracker.get_value() + dx_val / 2), UP, buff=0.14)
            .add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
        )
        lbl_int2 = always_redraw(
            lambda: MathTex(r"d(x^2)", color=W_COLOR, font_size=MIN_FONT)
            .next_to(line2.n2p(tracker.get_value() ** 2 + dx_val), UP, buff=0.14)
            .add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
        )
        lbl_int3 = always_redraw(
            lambda: MathTex(r"d\sin", color=RESULT_COLOR, font_size=MIN_FONT)
            .next_to(line3.n2p(np.sin(tracker.get_value() ** 2)), UP, buff=0.14)
            .add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
        )

        # Curved mapping arrows on the right side connecting the lines (positioned safely, x < 4.1)
        right_x = line1.get_right()[0] + 0.30
        arr_1_to_2 = CurvedArrow(
            np.array([right_x, 1.75, 0]),
            np.array([right_x, 0.70, 0]),
            angle=-np.pi / 2,
            color=W_COLOR,
            stroke_width=2.5,
        )
        lbl_arr1 = MathTex(r"\times 2x", color=W_COLOR, font_size=MIN_FONT).next_to(
            arr_1_to_2, RIGHT, buff=0.10
        )

        arr_2_to_3 = CurvedArrow(
            np.array([right_x, 0.50, 0]),
            np.array([right_x, -0.55, 0]),
            angle=-np.pi / 2,
            color=RESULT_COLOR,
            stroke_width=2.5,
        )
        lbl_arr2 = MathTex(r"\times \cos(x^2)", color=RESULT_COLOR, font_size=MIN_FONT).next_to(
            arr_2_to_3, RIGHT, buff=0.10
        )

        # Readout text for line 2 and line 3 relationships
        readout2 = always_redraw(
            lambda: MathTex(
                r"d(x^2) = 2x\,dx",
                color=W_COLOR,
                font_size=MIN_FONT,
            ).move_to(LEFT * 0.80 + UP * 0.12)
            .add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
        )

        readout3 = always_redraw(
            lambda: MathTex(
                r"d\sin = \cos(x^2)\,d(x^2)",
                color=RESULT_COLOR,
                font_size=MIN_FONT,
            ).move_to(LEFT * 0.80 + DOWN * 1.15)
            .add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
        )

        # Frame 0 setup
        self.add(
            line1,
            line2,
            line3,
            lbl_line1,
            lbl_line2,
            lbl_line3,
            dot1,
            dot2,
            dot3,
            int1,
            int2,
            int3,
            lbl_int1,
            lbl_int2,
            lbl_int3,
            arr_1_to_2,
            lbl_arr1,
            arr_2_to_3,
            lbl_arr2,
            readout2,
            readout3,
        )
        self.wait(1.0)

        # 2. Animate x moving with the intervals updating (staying well inside lines)
        self.play(
            tracker.animate.set_value(1.15),
            run_time=3.5,
            rate_func=linear,
        )
        self.wait(0.8)

        self.play(
            tracker.animate.set_value(1.00),
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(1.0)

        # 3. End on the final derivative formula at the bottom (clear of readout3 with buff >= 0.3)
        final_deriv = MathTex(
            r"\frac{d}{dx}\sin(x^2)", r"=", r"\cos(x^2)", r"\cdot", r"2x", font_size=MIN_FONT + 2
        )
        final_deriv[0].set_color(RESULT_COLOR)
        final_deriv[2].set_color(RESULT_COLOR)
        final_deriv[4].set_color(W_COLOR)
        final_deriv.move_to(DOWN * 2.10)
        final_deriv.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        final_box = SurroundingRectangle(final_deriv, color=RESULT_COLOR, buff=0.12, stroke_width=2)

        self.play(Write(final_deriv), run_time=1.0)
        self.play(FadeIn(final_box), run_time=0.6)
        self.wait(2.0)


class ChainRuleGeneral(Scene):
    def construct(self):
        # 1. Start from previous specific case from Scene 3
        spec = MathTex(
            r"\frac{d}{dx}", r"\sin(", r"x^2", r")", r"=", r"\cos(", r"x^2", r")", r"\cdot", r"2x",
            font_size=MIN_FONT + 2,
        )
        spec[0].set_color(INK)
        spec[1].set_color(RESULT_COLOR)
        spec[2].set_color(W_COLOR)
        spec[3].set_color(RESULT_COLOR)
        spec[4].set_color(INK)
        spec[5].set_color(RESULT_COLOR)
        spec[6].set_color(W_COLOR)
        spec[7].set_color(RESULT_COLOR)
        spec[8].set_color(INK)
        spec[9].set_color(W_COLOR)
        spec.move_to(UP * 2.05)

        # 2. 3-box chain: x -> h -> g with local derivative factor on each arrow
        # Box dimensions and positions in the middle tier
        chain_y = 0.45
        box_w = 1.3
        box_h = 0.75

        box_x = RoundedRectangle(
            corner_radius=0.1, width=box_w, height=box_h,
            stroke_color=X_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=0.85
        ).move_to(LEFT * 3.1 + UP * chain_y)
        txt_x = MathTex(r"x", color=X_COLOR, font_size=MIN_FONT).move_to(box_x.get_center())

        box_h_mob = RoundedRectangle(
            corner_radius=0.1, width=box_w, height=box_h,
            stroke_color=W_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=0.85
        ).move_to(UP * chain_y)
        txt_h = MathTex(r"h(x)", color=W_COLOR, font_size=MIN_FONT).move_to(box_h_mob.get_center())

        box_g = RoundedRectangle(
            corner_radius=0.1, width=box_w, height=box_h,
            stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=0.85
        ).move_to(RIGHT * 3.1 + UP * chain_y)
        txt_g = MathTex(r"g(h)", color=V_COLOR, font_size=MIN_FONT).move_to(box_g.get_center())

        arr1 = Arrow(
            box_x.get_right(), box_h_mob.get_left(),
            buff=0.1, color=INK_DIM, stroke_width=3, max_tip_length_to_length_ratio=0.22
        )
        lbl_arr1 = MathTex(r"\times \frac{dh}{dx}", color=W_COLOR, font_size=MIN_FONT).next_to(
            arr1, UP, buff=0.1
        )
        flow_arr1 = MathTex(r"dx \to dh", color=INK_FAINT, font_size=MIN_FONT).next_to(
            arr1, DOWN, buff=0.1
        )

        arr2 = Arrow(
            box_h_mob.get_right(), box_g.get_left(),
            buff=0.1, color=INK_DIM, stroke_width=3, max_tip_length_to_length_ratio=0.22
        )
        lbl_arr2 = MathTex(r"\times \frac{dg}{dh}", color=V_COLOR, font_size=MIN_FONT).next_to(
            arr2, UP, buff=0.1
        )
        flow_arr2 = MathTex(r"dh \to dg", color=INK_FAINT, font_size=MIN_FONT).next_to(
            arr2, DOWN, buff=0.1
        )

        chain_group = VGroup(
            box_x, txt_x, arr1, lbl_arr1, flow_arr1,
            box_h_mob, txt_h, arr2, lbl_arr2, flow_arr2,
            box_g, txt_g
        )

        # Frame 0 must show the given setup (never open on empty frame)
        self.add(spec, chain_group)
        self.wait(1.0)

        # 3. Generalize via TransformMatchingTex into general form
        gen = MathTex(
            r"\frac{d}{dx}", r"g(", r"h(x)", r")", r"=",
            r"\frac{dg}{dh}(h(x))", r"\cdot", r"\frac{dh}{dx}(x)",
            font_size=MIN_FONT + 2,
        )
        gen[0].set_color(INK)
        gen[1].set_color(V_COLOR)
        gen[2].set_color(W_COLOR)
        gen[3].set_color(V_COLOR)
        gen[4].set_color(INK)
        gen[5].set_color(V_COLOR)
        gen[6].set_color(INK)
        gen[7].set_color(W_COLOR)
        gen.move_to(UP * 2.05)

        self.play(TransformMatchingTex(spec, gen), run_time=1.8)
        self.wait(0.8)

        # 4. Product at the end (chain rule Leibniz formula)
        chain_product = MathTex(
            r"\frac{dg}{dx}", r"=", r"\frac{dg}{", r"dh", r"}", r"\cdot", r"\frac{", r"dh", r"}{dx}",
            font_size=MIN_FONT + 4,
        )
        chain_product[0].set_color(RESULT_COLOR)
        chain_product[1].set_color(INK)
        chain_product[2].set_color(V_COLOR)
        chain_product[3].set_color(W_COLOR)  # denominator dh
        chain_product[4].set_color(V_COLOR)
        chain_product[5].set_color(INK)
        chain_product[6].set_color(W_COLOR)
        chain_product[7].set_color(W_COLOR)  # numerator dh
        chain_product[8].set_color(X_COLOR)
        chain_product.move_to(DOWN * 0.95)

        self.play(Write(chain_product), run_time=1.4)
        self.wait(0.6)

        # Brief HIGHLIGHT flash on the dh pair
        flash1 = SurroundingRectangle(chain_product[3], color=HIGHLIGHT, buff=0.06, stroke_width=2.5)
        flash2 = SurroundingRectangle(chain_product[7], color=HIGHLIGHT, buff=0.06, stroke_width=2.5)

        self.play(FadeIn(flash1), FadeIn(flash2), run_time=0.35)
        self.play(FadeOut(flash1), FadeOut(flash2), run_time=0.35)

        # Diagonal strike lines showing cancellation
        slash1 = Line(chain_product[3].get_corner(DL), chain_product[3].get_corner(UR), color=HIGHLIGHT, stroke_width=2.5)
        slash2 = Line(chain_product[7].get_corner(DL), chain_product[7].get_corner(UR), color=HIGHLIGHT, stroke_width=2.5)

        self.play(Create(slash1), Create(slash2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(slash1), FadeOut(slash2), run_time=0.4)
        self.wait(0.4)

        # 5. Takeaway label and surrounding box
        rule_label = MathTex(
            r"\text{Nudges multiply along the chain}",
            color=RESULT_COLOR,
            font_size=MIN_FONT,
        ).next_to(chain_product, DOWN, buff=0.35)

        prod_box = SurroundingRectangle(
            VGroup(chain_product, rule_label), color=RESULT_COLOR, buff=0.15, stroke_width=2
        )

        self.play(FadeIn(rule_label), run_time=0.8)
        self.play(FadeIn(prod_box), run_time=0.6)
        self.wait(2.2)
