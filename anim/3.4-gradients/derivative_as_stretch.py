# Adapted from 3b1b/videos _2018/alt_calc.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *


class GraphVsTransform(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # Single top title for the scene (replacing bottom caption)
        # -------------------------------------------------------------
        title = MathTex(r"\text{A function moves points}", font_size=MIN_FONT + 2, color=INK)
        title.move_to(np.array([0.0, 2.35, 0.0]))
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # -------------------------------------------------------------
        # Left side: The graph view of f(x) = x^2 (~4 units tall, centered)
        # -------------------------------------------------------------
        left_center_x = -2.50

        axes = Axes(
            x_range=[0, 2.2, 1],
            y_range=[0, 4.2, 1],
            x_length=3.6,
            y_length=3.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.2,
                "include_ticks": True,
                "tick_size": 0.08,
            },
            tips=False,
        ).move_to(np.array([left_center_x, -0.05, 0.0]))

        # Coordinate labels with background rectangles
        lbl_x1 = MathTex("1", font_size=MIN_FONT, color=INK_DIM)
        lbl_x1.next_to(axes.c2p(1, 0), DOWN, buff=0.15)
        lbl_x1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_x2 = MathTex("2", font_size=MIN_FONT, color=INK_DIM)
        lbl_x2.next_to(axes.c2p(2, 0), DOWN, buff=0.15)
        lbl_x2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y1 = MathTex("1", font_size=MIN_FONT, color=INK_DIM)
        lbl_y1.next_to(axes.c2p(0, 1), LEFT, buff=0.15)
        lbl_y1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y4 = MathTex("4", font_size=MIN_FONT, color=INK_DIM)
        lbl_y4.next_to(axes.c2p(0, 4), LEFT, buff=0.15)
        lbl_y4.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        curve = axes.plot(lambda x: x**2, x_range=[0, 2.02], color=V_COLOR, stroke_width=3.5)
        curve_lbl = MathTex(r"f(x) = x^2", font_size=MIN_FONT, color=V_COLOR)
        curve_lbl.move_to(axes.c2p(1.10, 3.40))
        curve_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        pt_1 = axes.c2p(1, 1)
        dot_1 = Dot(pt_1, radius=0.08, color=RESULT_COLOR)
        dot_1.set_z_index(5)

        dash_v = DashedLine(axes.c2p(1, 0), pt_1, color=INK_FAINT, stroke_width=1.8)
        dash_h = DashedLine(axes.c2p(0, 1), pt_1, color=INK_FAINT, stroke_width=1.8)

        # Tangent line at x = 1 (slope = 2)
        tangent = axes.plot(lambda x: 2 * x - 1, x_range=[0.45, 1.80], color=RESULT_COLOR, stroke_width=3.5)
        tangent.set_z_index(4)

        slope_lbl = MathTex(r"\text{slope} = 2", font_size=MIN_FONT, color=RESULT_COLOR)
        slope_lbl.move_to(axes.c2p(0.40, 2.30))
        slope_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # -------------------------------------------------------------
        # Right side: The transformation view (~4.5 units wide, centered)
        # -------------------------------------------------------------
        right_center_x = 2.45
        in_y = 0.85
        out_y = -1.05

        in_line = NumberLine(
            x_range=[0, 2.2, 0.5],
            length=4.4,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([right_center_x, in_y, 0.0]))

        in_tag = MathTex(r"x", font_size=MIN_FONT + 2, color=V_COLOR)
        in_tag.next_to(in_line, LEFT, buff=0.20)
        in_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        in_nums = VGroup()
        for val in [0, 1, 2]:
            lbl = MathTex(str(val), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(in_line.n2p(val), UP, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            in_nums.add(lbl)

        out_line = NumberLine(
            x_range=[0, 4.4, 1.0],
            length=4.4,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([right_center_x, out_y, 0.0]))

        out_tag = MathTex(r"x^2", font_size=MIN_FONT + 2, color=RESULT_COLOR)
        out_tag.next_to(out_line, LEFT, buff=0.20)
        out_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        out_nums = VGroup()
        for val in [0, 1, 2, 3, 4]:
            lbl = MathTex(str(val), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(out_line.n2p(val), DOWN, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            out_nums.add(lbl)

        # Input dots
        x_vals = np.linspace(0.0, 2.0, 11)
        ghost_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.065, color=V_COLOR).set_opacity(0.35)
            for x in x_vals
        ])

        moving_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.075, color=V_COLOR)
            for x in x_vals
        ])
        moving_dots.set_z_index(5)

        # Frame 0: All givens visible!
        self.add(
            title, axes, lbl_x1, lbl_x2, lbl_y1, lbl_y4, curve, curve_lbl,
            dash_v, dash_h, dot_1,
            in_line, in_tag, in_nums, out_line, out_tag, out_nums,
            moving_dots
        )
        self.wait(1.0)

        # 1. Left side: tangent line and slope
        self.play(Create(tangent), FadeIn(slope_lbl), run_time=1.5)
        self.wait(0.6)

        # 2. Right side: ghost dots appear, moving dots flow along arcs to output line
        self.add(ghost_dots)
        self.bring_to_front(moving_dots)
        move_anims = [
            dot.animate(path_arc=-0.35).move_to(out_line.n2p(x**2)).set_color(RESULT_COLOR)
            for dot, x in zip(moving_dots, x_vals)
        ]
        self.play(LaggedStart(*move_anims, lag_ratio=0.12, run_time=3.5))
        self.wait(0.8)

        # 3. Momentary highlight at x = 1 (on tangent, graph dot, and output dot at 1)
        dot_1_out = moving_dots[5]  # x = 1.0 is index 5
        self.play(
            tangent.animate.set_color(HIGHLIGHT),
            dot_1_out.animate.set_color(HIGHLIGHT).scale(1.3),
            dot_1.animate.set_color(HIGHLIGHT).scale(1.3),
            run_time=0.4,
        )
        self.play(
            tangent.animate.set_color(RESULT_COLOR),
            dot_1_out.animate.set_color(RESULT_COLOR).scale(1 / 1.3),
            dot_1.animate.set_color(RESULT_COLOR).scale(1 / 1.3),
            run_time=0.4,
        )
        self.wait(2.0)


class ZoomStretch(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # Single top title (replacing duplicate bottom caption)
        # -------------------------------------------------------------
        title = MathTex(
            r"\text{Zoom in: every smooth map is a scaling}",
            font_size=MIN_FONT + 2,
            color=INK,
        ).move_to(np.array([0.0, 2.30, 0.0]))
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        in_y = 0.40
        out_y = -1.40
        line_len = 6.4
        center_x = 0.40
        col_x = -3.00

        in_tag = MathTex(r"\text{input } x", font_size=MIN_FONT, color=V_COLOR)
        in_tag.next_to(np.array([col_x, in_y, 0.0]), LEFT, buff=0.0)
        in_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        out_tag = MathTex(r"\text{output } x^2", font_size=MIN_FONT, color=RESULT_COLOR)
        out_tag.next_to(np.array([col_x, out_y, 0.0]), LEFT, buff=0.0)
        out_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        def make_number_line(center_val, y_pos, step=0.1, half_range=0.30):
            val_min = center_val - half_range
            val_max = center_val + half_range
            nline = NumberLine(
                x_range=[val_min, val_max, step],
                length=line_len,
                color=INK_DIM,
                stroke_width=2.2,
                include_ticks=False,
            ).move_to(np.array([center_x, y_pos, 0.0]))

            k_max = int(np.floor(half_range / step + 1e-6))
            ticks = VGroup(*[
                nline.get_tick(center_val + k * step, 0.08)
                for k in range(-k_max, k_max + 1)
            ])
            nline.add(ticks)

            nums = VGroup()
            for k in [-1, 0, 1]:
                val = center_val + k * step
                if abs(val - round(val)) < 1e-5:
                    v_str = str(int(round(val)))
                elif step < 0.1:
                    v_str = f"{val:.2f}"
                elif abs(val * 10 - round(val * 10)) < 1e-5:
                    v_str = f"{val:.1f}"
                else:
                    v_str = f"{val:.2f}"
                lbl = MathTex(v_str, font_size=MIN_FONT, color=INK_DIM)
                pos_dir = UP if y_pos > 0 else DOWN
                lbl.next_to(nline.n2p(val), pos_dir, buff=0.15)
                lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
                nums.add(lbl)
            return nline, nums

        # Overview line pair for Frame 0 (unzoomed context)
        global_in_line = NumberLine(
            x_range=[0, 4.0, 1.0],
            length=line_len,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([center_x, in_y, 0.0]))

        global_in_nums = VGroup()
        for v in [0, 1, 2, 3, 4]:
            lbl = MathTex(str(v), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(global_in_line.n2p(v), UP, buff=0.15)
            if v == 0:
                lbl.align_to(global_in_line.n2p(0), LEFT)
            elif v == 4:
                lbl.align_to(global_in_line.n2p(4), RIGHT)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            global_in_nums.add(lbl)

        global_out_line = NumberLine(
            x_range=[0, 16.0, 4.0],
            length=line_len,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([center_x, out_y, 0.0]))

        global_out_nums = VGroup()
        for v in [0, 4, 8, 12, 16]:
            lbl = MathTex(str(v), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(global_out_line.n2p(v), DOWN, buff=0.15)
            if v == 0:
                lbl.align_to(global_out_line.n2p(0), LEFT)
            elif v == 16:
                lbl.align_to(global_out_line.n2p(16), RIGHT)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            global_out_nums.add(lbl)

        init_dots = VGroup(*[
            Dot(global_in_line.n2p(1.0 + k * 0.08), radius=0.075, color=V_COLOR)
            for k in [-2, -1, 0, 1, 2]
        ])
        init_dots.set_z_index(5)

        readout_y = 1.60
        init_readout = MathTex(r"\text{zoom in near } x = 1", font_size=MIN_FONT + 2, color=RESULT_COLOR)
        init_readout.move_to(np.array([center_x, readout_y, 0.0]))
        init_readout.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0: Givens visible (no bottom caption)
        self.add(
            title, in_tag, out_tag,
            global_in_line, global_in_nums, global_out_line, global_out_nums,
            init_dots, init_readout
        )
        self.wait(0.6)

        cases = [
            (1.0, 1.0, 2.0, 0.05, 0.1, 0.30, r"\text{stretch} = f'(1) = 2"),
            (3.0, 9.0, 6.0, 0.02, 0.1, 0.30, r"\text{stretch} = f'(3) = 6"),
            (0.25, 0.0625, 0.5, 0.05, 0.05, 0.15, r"\text{stretch} = f'(1/4) = 1/2"),
            (0.0, 0.0, 0.0, 0.05, 0.1, 0.30, r"\text{stretch} = f'(0) = 0"),
        ]

        k_indices = np.array([-2, -1, 0, 1, 2])

        # Step 0 -> Case 1: Zoom in (scale lines about x=1)
        x0, y0, deriv0, dx0, step0, half_range0, final_str0 = cases[0]
        cur_in_line, cur_in_nums = make_number_line(x0, in_y, step=step0, half_range=half_range0)
        cur_out_line, cur_out_nums = make_number_line(y0, out_y, step=step0, half_range=half_range0)
        cur_dots = VGroup(*[
            Dot(cur_in_line.n2p(x0 + k * dx0), radius=0.075, color=V_COLOR)
            for k in k_indices
        ])
        cur_dots.set_z_index(5)

        # Zoom in animation
        self.play(
            FadeOut(global_in_line), FadeOut(global_in_nums),
            FadeOut(global_out_line), FadeOut(global_out_nums),
            FadeOut(init_dots), FadeOut(init_readout),
            FadeIn(cur_in_line), FadeIn(cur_in_nums),
            FadeIn(cur_out_line), FadeIn(cur_out_nums),
            FadeIn(cur_dots),
            run_time=1.2,
        )

        cur_readout = None
        # Balanced hold times to hit 20%, 50%, 80%, 100% sheets precisely:
        hold_times = [2.2, 4.0, 4.0, 2.0]

        for idx, (x_val, y_val, deriv_val, dx_val, step_val, half_range_val, final_tex_str) in enumerate(cases):
            if idx > 0:
                new_in_line, new_in_nums = make_number_line(x_val, in_y, step=step_val, half_range=half_range_val)
                new_out_line, new_out_nums = make_number_line(y_val, out_y, step=step_val, half_range=half_range_val)

                new_dots = VGroup(*[
                    Dot(new_in_line.n2p(x_val + k * dx_val), radius=0.075, color=V_COLOR)
                    for k in k_indices
                ])
                new_dots.set_z_index(5)

                self.play(
                    FadeOut(cur_in_line), FadeOut(cur_in_nums),
                    FadeOut(cur_out_line), FadeOut(cur_out_nums),
                    FadeOut(cur_dots),
                    FadeOut(cur_readout),
                    FadeIn(new_in_line), FadeIn(new_in_nums),
                    FadeIn(new_out_line), FadeIn(new_out_nums),
                    FadeIn(new_dots),
                    run_time=0.8,
                )
                cur_in_line, cur_in_nums = new_in_line, new_in_nums
                cur_out_line, cur_out_nums = new_out_line, new_out_nums
                cur_dots = new_dots

            # Measure screen distance ratio and assert
            in_dist = abs(cur_dots[-1].get_center()[0] - cur_dots[0].get_center()[0])
            out_p_last = cur_out_line.n2p((x_val + k_indices[-1] * dx_val)**2)[0]
            out_p_first = cur_out_line.n2p((x_val + k_indices[0] * dx_val)**2)[0]
            out_dist = abs(out_p_last - out_p_first)
            if deriv_val != 0:
                measured_ratio = out_dist / in_dist
                print(f"[MEASURED RATIO] ZoomStretch x0={x_val}: {measured_ratio:.4f} (expected {abs(deriv_val):.4f})")
                assert abs(measured_ratio - abs(deriv_val)) / abs(deriv_val) < 0.10, (
                    f"ZoomStretch ratio {measured_ratio} not within 10% of {abs(deriv_val)}"
                )

            # Ghost dots on input line
            ghosts = VGroup(*[
                Dot(cur_in_line.n2p(x_val + k * dx_val), radius=0.065, color=V_COLOR).set_opacity(0.35)
                for k in k_indices
            ])
            self.add(ghosts)

            # Live tracker for stretch readout
            tracker = ValueTracker(1.0)
            live_lbl = always_redraw(
                lambda: MathTex(
                    f"\\text{{stretch}} \\approx {tracker.get_value():.1f}",
                    font_size=MIN_FONT + 2,
                    color=RESULT_COLOR,
                )
                .move_to(np.array([center_x, readout_y, 0.0]))
                .add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            )
            self.add(live_lbl)

            out_anims = [
                dot.animate(path_arc=-0.25).move_to(cur_out_line.n2p((x_val + k * dx_val)**2)).set_color(RESULT_COLOR)
                for dot, k in zip(cur_dots, k_indices)
            ]

            self.play(
                LaggedStart(*out_anims, lag_ratio=0.04),
                tracker.animate.set_value(deriv_val),
                run_time=1.6,
            )

            # Remove live_lbl, replace with final exact equation
            self.remove(live_lbl)
            final_tex = MathTex(final_tex_str, font_size=MIN_FONT + 2, color=RESULT_COLOR)
            final_tex.move_to(np.array([center_x, readout_y, 0.0]))
            final_tex.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

            self.play(FadeIn(final_tex), run_time=0.3)
            cur_readout = final_tex

            self.wait(hold_times[idx])
            self.remove(ghosts)


class NegativeStretch(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # Single top title (replacing duplicate bottom caption)
        # -------------------------------------------------------------
        title = MathTex(
            r"\text{Negative derivative} \implies \text{orientation flip}",
            font_size=MIN_FONT + 2,
            color=INK,
        ).move_to(np.array([0.0, 2.30, 0.0]))
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        center_x = 0.40
        readout_y = 1.70
        readout = MathTex(r"f'(-1) = -2", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        readout.move_to(np.array([center_x, readout_y, 0.0]))
        readout.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        in_y = 0.25
        out_y = -1.15
        line_len = 6.4
        col_x = -3.00

        in_tag = MathTex(r"\text{input } x", font_size=MIN_FONT, color=V_COLOR)
        in_tag.next_to(np.array([col_x, in_y, 0.0]), LEFT, buff=0.0)
        in_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        out_tag = MathTex(r"\text{output } x^2", font_size=MIN_FONT, color=RESULT_COLOR)
        out_tag.next_to(np.array([col_x, out_y, 0.0]), LEFT, buff=0.0)
        out_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Input line centered at x = -1.0
        in_line = NumberLine(
            x_range=[-1.3, -0.7, 0.1],
            length=line_len,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=False,
        ).move_to(np.array([center_x, in_y, 0.0]))

        k_max_in = int(np.floor(0.30 / 0.1 + 1e-6))
        in_ticks = VGroup(*[
            in_line.get_tick(-1.0 + k * 0.1, 0.08)
            for k in range(-k_max_in, k_max_in + 1)
        ])
        in_line.add(in_ticks)

        # Tick numbers go ABOVE the input line (buff 0.15)
        in_nums = VGroup()
        for val in [-1.1, -1.0, -0.9]:
            lbl = MathTex(f"{val:.1f}", font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(in_line.n2p(val), UP, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            in_nums.add(lbl)

        # Output line centered at y = 1.0 (same unit_size and tick step as input line)
        out_line = NumberLine(
            x_range=[0.7, 1.3, 0.1],
            length=line_len,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=False,
        ).move_to(np.array([center_x, out_y, 0.0]))

        k_max_out = int(np.floor(0.30 / 0.1 + 1e-6))
        out_ticks = VGroup(*[
            out_line.get_tick(1.0 + k * 0.1, 0.08)
            for k in range(-k_max_out, k_max_out + 1)
        ])
        out_line.add(out_ticks)

        # Tick numbers go BELOW the output line (buff 0.15)
        out_nums = VGroup()
        for val in [0.9, 1.0, 1.1]:
            lbl = MathTex(f"{val:.1f}", font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(out_line.n2p(val), DOWN, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            out_nums.add(lbl)

        # 5 colour-ordered dots near x = -1 (+-0.1 input cluster -> +-0.2 output cluster, reversed)
        # Gradient from X_COLOR (green, leftmost) to Y_COLOR (rose, rightmost)
        xs = np.linspace(-1.10, -0.90, 5)
        n_dots = len(xs)
        dot_colors = [
            interpolate_color(ManimColor(X_COLOR), ManimColor(Y_COLOR), i / (n_dots - 1))
            for i in range(n_dots)
        ]

        input_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.08, color=col)
            for x, col in zip(xs, dot_colors)
        ])
        input_dots.set_z_index(5)

        ghost_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.07, color=col).set_opacity(0.35)
            for x, col in zip(xs, dot_colors)
        ])

        # Measure in code: assert ratio
        in_dist = abs(input_dots[-1].get_center()[0] - input_dots[0].get_center()[0])
        out_p_last = out_line.n2p(xs[-1]**2)[0]
        out_p_first = out_line.n2p(xs[0]**2)[0]
        out_dist = abs(out_p_last - out_p_first)
        measured_ratio = out_dist / in_dist
        print(f"[MEASURED RATIO] NegativeStretch x0=-1: {measured_ratio:.4f} (expected 2.0000)")
        assert abs(measured_ratio - 2.0) / 2.0 < 0.10, (
            f"NegativeStretch ratio {measured_ratio} not within 10% of 2.0"
        )

        # Arrow above input numbers at y = 1.15 indicating original left-to-right order
        p_start_in = np.array([in_line.n2p(xs[0])[0], 1.15, 0.0])
        p_end_in = np.array([in_line.n2p(xs[-1])[0], 1.15, 0.0])
        arrow_in = Arrow(
            p_start_in, p_end_in,
            color=INK,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )
        arrow_in_lbl = MathTex(r"\text{original order}", font_size=MIN_FONT, color=INK)
        arrow_in_lbl.next_to(arrow_in, RIGHT, buff=0.20)
        arrow_in_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0: Givens visible (no bottom caption)
        self.add(
            title, readout, in_tag, out_tag, in_line, in_nums, out_line, out_nums,
            input_dots, arrow_in, arrow_in_lbl
        )
        self.wait(1.0)

        # 1. Moving dots cross over down to output line (flight corridor is completely empty!)
        self.add(ghost_dots)
        self.bring_to_front(input_dots)

        move_anims = [
            dot.animate(path_arc=-0.25).move_to(out_line.n2p(x**2))
            for dot, x in zip(input_dots, xs)
        ]
        self.play(
            LaggedStart(*move_anims, lag_ratio=0.08, run_time=3.5),
        )
        self.wait(0.8)

        # 2. Arrow below output numbers showing reversed order (points LEFT)
        # xs[0] is green, lands at xs[0]**2 = 1.21 (on the right)
        # xs[-1] is rose, lands at xs[-1]**2 = 0.81 (on the left)
        # Arrow points from green to rose, which points LEFT!
        p_start_out = np.array([out_line.n2p(xs[0]**2)[0], -1.80, 0.0])
        p_end_out = np.array([out_line.n2p(xs[-1]**2)[0], -1.80, 0.0])
        arrow_out = Arrow(
            p_start_out, p_end_out,
            color=RESULT_COLOR,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
        )
        arrow_out_lbl = MathTex(r"\text{order reversed!}", font_size=MIN_FONT, color=RESULT_COLOR)
        arrow_out_lbl.next_to(arrow_out, DOWN, buff=0.15)
        arrow_out_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(
            Create(arrow_out),
            FadeIn(arrow_out_lbl),
            run_time=1.5,
        )
        self.wait(0.8)

        # 3. Momentary highlight on flipped dots
        self.play(
            input_dots.animate.scale(1.25),
            run_time=0.4,
        )
        self.play(
            input_dots.animate.scale(1 / 1.25),
            run_time=0.4,
        )
        self.wait(2.0)
