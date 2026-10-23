# Adapted from 3b1b/videos _2017/eoc/chapter2.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *


def s_fn(t):
    """Smooth sigmoid-like distance trajectory s(t) from 0 to 100m over [0, 8]s."""
    tau = np.clip(t / 8.0, 0.0, 1.0)
    return 100.0 * (10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5)


def s_prime_fn(t):
    """Derivative ds/dt of s(t) in m/s."""
    tau = np.clip(t / 8.0, 0.0, 1.0)
    return (3000.0 / 8.0) * (tau**2) * ((1.0 - tau) ** 2)


def get_car():
    """Simple car built from primitives: rounded rectangle body + 2 wheel circles."""
    body = RoundedRectangle(
        corner_radius=0.08,
        width=0.74,
        height=0.22,
        stroke_color=INK_DIM,
        stroke_width=2,
        fill_color=INK_DIM,
        fill_opacity=1.0,
    )
    cabin = RoundedRectangle(
        corner_radius=0.06,
        width=0.42,
        height=0.15,
        stroke_color=INK_DIM,
        stroke_width=2,
        fill_color=INK_DIM,
        fill_opacity=1.0,
    ).move_to(body.get_top() + UP * 0.06 + LEFT * 0.04)
    w1 = Circle(
        radius=0.07,
        stroke_color=INK,
        stroke_width=2,
        fill_color=BG,
        fill_opacity=1.0,
    ).move_to(body.get_bottom() + LEFT * 0.22)
    w2 = Circle(
        radius=0.07,
        stroke_color=INK,
        stroke_width=2,
        fill_color=BG,
        fill_opacity=1.0,
    ).move_to(body.get_bottom() + RIGHT * 0.22)
    car = VGroup(body, cabin, w1, w2)
    return car


def get_trajectory_axes():
    """Consistent coordinate axes for the distance-time graph."""
    axes = Axes(
        x_range=[0, 8.001, 2],
        y_range=[0, 100.001, 25],
        x_length=7.2,
        y_length=3.0,
        axis_config={
            "stroke_color": INK_DIM,
            "stroke_width": 2.5,
            "include_tip": False,
            "include_ticks": True,
        },
        tips=False,
    )
    axes.move_to(np.array([-0.1, -0.75, 0]))
    axes.add_coordinates(font_size=MIN_FONT)
    for axis in axes.get_axes():
        if hasattr(axis, "numbers"):
            for num in axis.numbers:
                num.set_color(INK_DIM)
    return axes


class CarTrajectory(Scene):
    def construct(self):
        road_y = 2.05
        road_x_start = -3.7
        road_x_end = 3.5

        # 1. Road setup
        road = Line(LEFT * 4.3 + UP * road_y, RIGHT * 4.1 + UP * road_y, color=INK_DIM, stroke_width=2.5)
        tick_0 = Line(UP * (road_y - 0.1) + LEFT * 3.7, UP * (road_y + 0.1) + LEFT * 3.7, color=INK_DIM, stroke_width=2)
        tick_100 = Line(UP * (road_y - 0.1) + RIGHT * 3.5, UP * (road_y + 0.1) + RIGHT * 3.5, color=INK_DIM, stroke_width=2)
        lbl_0 = MathTex(r"0\,\text{m}", font_size=MIN_FONT, color=INK_DIM)
        lbl_0.next_to(tick_0, DOWN, buff=0.12).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        lbl_100 = MathTex(r"100\,\text{m}", font_size=MIN_FONT, color=INK_DIM)
        lbl_100.next_to(tick_100, DOWN, buff=0.12).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Axes setup
        axes = get_trajectory_axes()

        t_axis_lbl = MathTex(r"t\text{ (s)}", font_size=MIN_FONT, color=X_COLOR)
        t_axis_lbl.next_to(axes.c2p(8, 0), RIGHT, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        s_axis_lbl = MathTex(r"s\text{ (m)}", font_size=MIN_FONT, color=Y_COLOR)
        s_axis_lbl.next_to(axes.c2p(0, 100), UP + RIGHT, buff=0.15).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 3. Car setup
        car = get_car()
        car.move_to(np.array([road_x_start, road_y + 0.17, 0]))

        # 4. Animated elements tracking t
        t_tracker = ValueTracker(0.0)

        # Graph curve traced in sync
        traced_graph = always_redraw(
            lambda: axes.plot(
                s_fn,
                x_range=[0, max(0.01, t_tracker.get_value())],
                color=V_COLOR,
                stroke_width=4,
            )
        )

        # Dot on the graph tracking the car
        tracking_dot = always_redraw(
            lambda: Dot(
                axes.c2p(t_tracker.get_value(), s_fn(t_tracker.get_value())),
                color=RESULT_COLOR,
                radius=0.08,
            )
        )

        # Subtle vertical and horizontal guide lines
        v_guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(t_tracker.get_value(), 0),
                axes.c2p(t_tracker.get_value(), s_fn(t_tracker.get_value())),
                color=X_COLOR,
                stroke_width=2,
                dash_length=0.08,
            )
        )
        h_guide = always_redraw(
            lambda: DashedLine(
                axes.c2p(0, s_fn(t_tracker.get_value())),
                axes.c2p(t_tracker.get_value(), s_fn(t_tracker.get_value())),
                color=Y_COLOR,
                stroke_width=2,
                dash_length=0.08,
            )
        )

        # Car updater: x follows s(t)
        car.add_updater(
            lambda m: m.move_to(
                np.array([
                    road_x_start + (s_fn(t_tracker.get_value()) / 100.0) * (road_x_end - road_x_start),
                    road_y + 0.17,
                    0,
                ])
            )
        )

        # 5. First frame: never open on an empty frame
        self.add(
            road, tick_0, tick_100, lbl_0, lbl_100,
            axes, t_axis_lbl, s_axis_lbl,
            car, traced_graph, v_guide, h_guide, tracking_dot
        )
        self.wait(0.5)

        # 6. Drive the car smoothly from t=0 to t=8
        self.play(
            t_tracker.animate.set_value(8.0),
            run_time=8.0,
            rate_func=linear,
        )

        # Label the completed graph s(t)
        s_graph_label = MathTex(r"s(t)", font_size=MIN_FONT + 4, color=V_COLOR)
        s_graph_label.next_to(axes.c2p(7.3, s_fn(7.3)), UP + LEFT, buff=0.20)
        s_graph_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        self.play(FadeIn(s_graph_label), run_time=0.8)
        self.wait(1.5)


class TwoTimes(Scene):
    def construct(self):
        road_y = 2.05
        road_x_start = -3.7
        road_x_end = 3.5

        # 1. Base road and axes
        road = Line(LEFT * 4.3 + UP * road_y, RIGHT * 4.1 + UP * road_y, color=INK_DIM, stroke_width=2.5)
        tick_0 = Line(UP * (road_y - 0.1) + LEFT * 3.7, UP * (road_y + 0.1) + LEFT * 3.7, color=INK_DIM, stroke_width=2)
        tick_100 = Line(UP * (road_y - 0.1) + RIGHT * 3.5, UP * (road_y + 0.1) + RIGHT * 3.5, color=INK_DIM, stroke_width=2)

        axes = get_trajectory_axes()

        t_axis_lbl = MathTex(r"t\text{ (s)}", font_size=MIN_FONT, color=X_COLOR)
        t_axis_lbl.next_to(axes.c2p(8, 0), RIGHT, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        s_axis_lbl = MathTex(r"s\text{ (m)}", font_size=MIN_FONT, color=Y_COLOR)
        s_axis_lbl.next_to(axes.c2p(0, 100), UP + RIGHT, buff=0.15).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Full trajectory curve
        full_graph = axes.plot(s_fn, x_range=[0, 8], color=V_COLOR, stroke_width=4)
        s_lbl = MathTex(r"s(t)", font_size=MIN_FONT + 4, color=V_COLOR)
        s_lbl.next_to(axes.c2p(8.0, 100.0), UP + RIGHT * 0.1, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Pick t = 3.0 and t+dt = 5.0
        t1, t2 = 3.0, 5.0
        s1, s2 = s_fn(t1), s_fn(t2)

        # Car 1 at t = 3.0
        car1_x = road_x_start + (s1 / 100.0) * (road_x_end - road_x_start)
        car1 = get_car().move_to(np.array([car1_x, road_y + 0.17, 0]))

        # Point 1 on graph
        p1 = axes.c2p(t1, s1)
        dot1 = Dot(p1, color=RESULT_COLOR, radius=0.08)
        v_line1 = DashedLine(axes.c2p(t1, 0), p1, color=X_COLOR, stroke_width=2, dash_length=0.08)

        # First frame shows the setup with time t
        self.add(
            road, tick_0, tick_100,
            axes, t_axis_lbl, s_axis_lbl,
            full_graph, s_lbl, car1, dot1, v_line1
        )
        self.wait(1.0)

        # Introduce time t + dt: second car on the road
        car2_x = road_x_start + (s2 / 100.0) * (road_x_end - road_x_start)
        car2 = get_car().move_to(np.array([car2_x, road_y + 0.17, 0]))
        car2.set_opacity(0.85)

        p2 = axes.c2p(t2, s2)
        dot2 = Dot(p2, color=RESULT_COLOR, radius=0.08)
        v_line2 = DashedLine(axes.c2p(t2, 0), p2, color=X_COLOR, stroke_width=2, dash_length=0.08)

        self.play(
            FadeIn(car2),
            Create(dot2),
            Create(v_line2),
            run_time=1.5,
        )
        self.wait(1.0)

        # Rise/run triangle on graph
        p_corner = axes.c2p(t2, s1)
        run_seg = Line(p1, p_corner, color=X_COLOR, stroke_width=3.5)
        rise_seg = Line(p_corner, p2, color=Y_COLOR, stroke_width=3.5)
        secant_seg = Line(p1, p2, color=RESULT_COLOR, stroke_width=3.5)

        brace_dt = Brace(run_seg, DOWN, buff=0.08)
        lbl_dt = MathTex(r"dt", font_size=MIN_FONT, color=X_COLOR)
        lbl_dt.next_to(brace_dt, DOWN, buff=0.08).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        brace_ds = Brace(rise_seg, RIGHT, buff=0.08)
        lbl_ds = MathTex(r"ds", font_size=MIN_FONT, color=Y_COLOR)
        lbl_ds.next_to(brace_ds, RIGHT, buff=0.08).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(
            Create(run_seg),
            Create(rise_seg),
            Create(secant_seg),
            Create(brace_dt),
            Write(lbl_dt),
            Create(brace_ds),
            Write(lbl_ds),
            run_time=1.5,
        )
        self.wait(1.0)

        # Remove road and cars after the first beat so upper frame is clean
        self.play(
            FadeOut(road),
            FadeOut(tick_0),
            FadeOut(tick_100),
            FadeOut(car1),
            FadeOut(car2),
            FadeOut(v_line1),
            FadeOut(v_line2),
            run_time=0.8,
        )

        # Average speed formula in open space above curve
        formula = MathTex(
            r"\frac{ds}{dt} = \frac{s(t+dt) - s(t)}{dt}",
            font_size=MIN_FONT + 2,
        )
        formula.set_color_by_tex(r"ds", Y_COLOR)
        formula.set_color_by_tex(r"dt", X_COLOR)
        formula.set_color_by_tex(r"s", V_COLOR)

        sub_lbl = MathTex(
            rf"\text{{average}} = {s2 - s1:.1f}/{t2 - t1:g} = {(s2 - s1) / (t2 - t1):.1f}\ \text{{m/s}}",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )

        formula_group = VGroup(formula, sub_lbl).arrange(DOWN, buff=0.20)
        formula_group.move_to(RIGHT * 0.2 + UP * 1.90)
        formula_group.add_background_rectangle(color=BG, opacity=0.85, buff=0.10)

        self.play(FadeIn(formula_group), run_time=1.2)
        self.wait(3.0)


class ShrinkDt(Scene):
    def construct(self):
        # 1. Base axes and graph
        axes = get_trajectory_axes()

        t_axis_lbl = MathTex(r"t\text{ (s)}", font_size=MIN_FONT, color=X_COLOR)
        t_axis_lbl.next_to(axes.c2p(8, 0), RIGHT, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        s_axis_lbl = MathTex(r"s\text{ (m)}", font_size=MIN_FONT, color=Y_COLOR)
        s_axis_lbl.next_to(axes.c2p(0, 100), UP + RIGHT, buff=0.15).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        full_graph = axes.plot(s_fn, x_range=[0, 8], color=V_COLOR, stroke_width=4)
        s_lbl = MathTex(r"s(t)", font_size=MIN_FONT + 4, color=V_COLOR)
        s_lbl.next_to(axes.c2p(8.0, 100.0), UP + RIGHT * 0.1, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Fixed point at t0 = 3.5
        t0 = 3.5
        s0 = s_fn(t0)
        p0 = axes.c2p(t0, s0)
        dot0 = Dot(p0, color=RESULT_COLOR, radius=0.08)

        # Continuous ValueTracker for dt
        dt_tracker = ValueTracker(1.50)

        # Dynamic second point and triangle
        dot_dt = always_redraw(
            lambda: Dot(
                axes.c2p(t0 + dt_tracker.get_value(), s_fn(t0 + dt_tracker.get_value())),
                color=RESULT_COLOR,
                radius=0.08,
            )
        )
        run_line = always_redraw(
            lambda: Line(
                p0,
                axes.c2p(t0 + dt_tracker.get_value(), s0),
                color=X_COLOR,
                stroke_width=3.5,
            )
        )
        rise_line = always_redraw(
            lambda: Line(
                axes.c2p(t0 + dt_tracker.get_value(), s0),
                axes.c2p(t0 + dt_tracker.get_value(), s_fn(t0 + dt_tracker.get_value())),
                color=Y_COLOR,
                stroke_width=3.5,
            )
        )
        hypot = always_redraw(
            lambda: Line(
                p0,
                axes.c2p(t0 + dt_tracker.get_value(), s_fn(t0 + dt_tracker.get_value())),
                color=RESULT_COLOR,
                stroke_width=3.5,
            )
        )

        # Self-contained dynamic readouts panel in open top-left quadrant
        # Row 1: dt
        dt_lbl = MathTex(r"dt =", font_size=MIN_FONT, color=X_COLOR)
        dt_num = DecimalNumber(
            dt_tracker.get_value(),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=X_COLOR,
        )
        dt_num.add_updater(lambda m: m.set_value(dt_tracker.get_value()))
        dt_unit = MathTex(r"\text{s}", font_size=MIN_FONT, color=X_COLOR)
        dt_unit.add_updater(lambda m: m.next_to(dt_num, RIGHT, buff=0.10))
        dt_num.next_to(dt_lbl, RIGHT, buff=0.15)
        dt_unit.next_to(dt_num, RIGHT, buff=0.10)
        row_dt = VGroup(dt_lbl, dt_num, dt_unit)

        # Row 2: ds
        ds_lbl = MathTex(r"ds =", font_size=MIN_FONT, color=Y_COLOR)
        ds_num = DecimalNumber(
            s_fn(t0 + dt_tracker.get_value()) - s0,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=Y_COLOR,
        )
        ds_num.add_updater(lambda m: m.set_value(s_fn(t0 + dt_tracker.get_value()) - s0))
        ds_unit = MathTex(r"\text{m}", font_size=MIN_FONT, color=Y_COLOR)
        ds_unit.add_updater(lambda m: m.next_to(ds_num, RIGHT, buff=0.10))
        ds_num.next_to(ds_lbl, RIGHT, buff=0.15)
        ds_unit.next_to(ds_num, RIGHT, buff=0.10)
        row_ds = VGroup(ds_lbl, ds_num, ds_unit)

        # Row 3: ds/dt (inline, not stacked fraction)
        ratio_lbl = MathTex(r"ds/dt =", font_size=MIN_FONT, color=RESULT_COLOR)
        ratio_num = DecimalNumber(
            (s_fn(t0 + dt_tracker.get_value()) - s0) / dt_tracker.get_value(),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        ratio_num.add_updater(
            lambda m: m.set_value((s_fn(t0 + dt_tracker.get_value()) - s0) / dt_tracker.get_value())
        )
        ratio_unit = MathTex(r"\text{m/s}", font_size=MIN_FONT, color=RESULT_COLOR)
        ratio_unit.add_updater(lambda m: m.next_to(ratio_num, RIGHT, buff=0.10))
        ratio_num.next_to(ratio_lbl, RIGHT, buff=0.15)
        ratio_unit.next_to(ratio_num, RIGHT, buff=0.10)
        row_ratio = VGroup(ratio_lbl, ratio_num, ratio_unit)

        # Arrange the three readout lines as a VGroup
        readout_lines = VGroup(row_dt, row_ds, row_ratio).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        readout_lines.move_to(LEFT * 0.5 + UP * 1.45)

        # Size the card from the group
        readout_card = RoundedRectangle(
            corner_radius=0.12,
            width=readout_lines.width + 0.6,
            height=readout_lines.height + 0.5,
            stroke_color=INK_DIM,
            stroke_width=1.5,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to(readout_lines)

        # Compute true derivative value in code dynamically
        true_speed = s_prime_fn(t0)
        settle_note = MathTex(
            rf"\to {true_speed:.1f}\,\text{{m/s}}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        settle_note.next_to(readout_card, DOWN, buff=0.22, aligned_edge=LEFT).shift(RIGHT * 0.3)
        settle_note.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 1. First frame
        self.add(
            axes, t_axis_lbl, s_axis_lbl,
            full_graph, s_lbl, dot0,
            run_line, rise_line, hypot, dot_dt,
            readout_card,
            row_dt, row_ds, row_ratio
        )
        self.wait(1.0)

        # 2. Shrink dt continuously from 1.50 to 0.05
        self.play(
            dt_tracker.animate.set_value(0.05),
            run_time=6.0,
            rate_func=linear,
        )
        self.wait(2.0)

        # 3. Flash highlight on the settled ratio
        flash_box = SurroundingRectangle(row_ratio, color=HIGHLIGHT, buff=0.08, stroke_width=2.5)
        self.play(FadeIn(flash_box), run_time=0.4)
        self.play(FadeOut(flash_box), run_time=0.4)

        # 4. Reveal settled conclusion
        self.play(FadeIn(settle_note), run_time=1.0)
        self.wait(3.0)


class SecantToTangent(Scene):
    def construct(self):
        # 1. Base axes and graph
        axes = get_trajectory_axes()

        t_axis_lbl = MathTex(r"t\text{ (s)}", font_size=MIN_FONT, color=X_COLOR)
        t_axis_lbl.next_to(axes.c2p(8, 0), RIGHT, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        s_axis_lbl = MathTex(r"s\text{ (m)}", font_size=MIN_FONT, color=Y_COLOR)
        s_axis_lbl.next_to(axes.c2p(0, 100), UP + RIGHT, buff=0.15).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        full_graph = axes.plot(s_fn, x_range=[0, 8], color=V_COLOR, stroke_width=4)
        s_lbl = MathTex(r"s(t)", font_size=MIN_FONT + 4, color=V_COLOR)
        s_lbl.next_to(axes.c2p(8.0, 100.0), UP + RIGHT * 0.1, buff=0.18).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Value trackers
        t_tracker = ValueTracker(3.5)
        dt_tracker = ValueTracker(2.0)

        # Extended secant / tangent line across the axes
        def get_secant_tangent_line():
            t_val = t_tracker.get_value()
            dt_val = dt_tracker.get_value()
            p1 = axes.c2p(t_val, s_fn(t_val))
            h = max(dt_val, 0.005)
            p2 = axes.c2p(t_val + h, s_fn(t_val + h))
            diff = p2 - p1
            unit = diff / np.linalg.norm(diff)
            back = 1.1 * unit
            fwd = (np.linalg.norm(diff) + 1.1) * unit if dt_val > 0.05 else 1.1 * unit
            return Line(p1 - back, p1 + fwd, color=RESULT_COLOR, stroke_width=3.5)

        ext_line = always_redraw(get_secant_tangent_line)

        # Dots
        dot1 = always_redraw(
            lambda: Dot(
                axes.c2p(t_tracker.get_value(), s_fn(t_tracker.get_value())),
                color=RESULT_COLOR,
                radius=0.08,
            )
        )
        dot2 = always_redraw(
            lambda: Dot(
                axes.c2p(
                    t_tracker.get_value() + dt_tracker.get_value(),
                    s_fn(t_tracker.get_value() + dt_tracker.get_value()),
                ),
                color=RESULT_COLOR,
                radius=0.08,
            )
        )

        # 1. First frame
        self.add(
            axes, t_axis_lbl, s_axis_lbl,
            full_graph, s_lbl, ext_line, dot1, dot2
        )
        self.wait(1.0)

        # 2. Rotate secant into tangent line as dt -> 0
        self.play(
            dt_tracker.animate.set_value(0.001),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(FadeOut(dot2), run_time=0.4)
        self.wait(1.0)

        # 3. True derivative definition above the plot in open space
        deriv_def = MathTex(
            r"\frac{ds}{dt}(t) = \lim_{dt \to 0} \frac{s(t+dt) - s(t)}{dt}",
            font_size=MIN_FONT + 2,
        )
        deriv_def.set_color_by_tex(r"ds", Y_COLOR)
        deriv_def.set_color_by_tex(r"dt", X_COLOR)
        deriv_def.set_color_by_tex(r"s", V_COLOR)
        deriv_def.move_to(UP * 2.05)
        deriv_def.add_background_rectangle(color=BG, opacity=0.85, buff=0.10)

        self.play(FadeIn(deriv_def), run_time=1.2)
        self.wait(1.0)

        # 4. Slide t along the curve: the derivative depends on t
        caption = MathTex(
            r"\text{Derivative depends on } t",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        caption.next_to(deriv_def, DOWN, buff=0.18)
        caption.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(FadeIn(caption), run_time=0.8)
        self.play(
            t_tracker.animate.set_value(1.5),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(
            t_tracker.animate.set_value(6.0),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(2.0)


class TCubed(Scene):
    def construct(self):
        # 1. Algebra expansion column on the left
        title = MathTex(r"\text{Example: } s(t) = t^3", font_size=MIN_FONT + 2, color=V_COLOR)

        # Step 1: Difference quotient
        step1 = MathTex(
            r"\frac{ds}{dt} = \frac{(t+dt)^3 - t^3}{dt}",
            font_size=MIN_FONT,
        )
        step1.set_color_by_tex(r"dt", X_COLOR)
        step1.set_color_by_tex(r"ds", Y_COLOR)

        # Step 2: Expanded numerator
        step2 = MathTex(
            r"= \frac{3t^2\,dt + 3t(dt)^2 + dt^3}{dt}",
            font_size=MIN_FONT,
        )
        step2.set_color_by_tex(r"dt", X_COLOR)

        # Step 3: Divide out dt
        step3 = MathTex(
            r"= 3t^2 + 3t\,dt + dt^2",
            font_size=MIN_FONT,
        )
        step3.set_color_by_tex(r"3t^2", RESULT_COLOR)
        step3.set_color_by_tex(r"dt", X_COLOR)

        # Step 5: Final limit
        step5 = MathTex(
            r"\to 3t^2",
            font_size=MIN_FONT + 4,
            color=RESULT_COLOR,
        )

        column = VGroup(title, step1, step2, step3, step5).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if column.height > 5.0:
            column.scale_to_fit_height(5.0)
        if column.width > 4.4:
            column.scale_to_fit_width(4.4)
        column.move_to(LEFT * 2.45)

        # Step 4: Dim the dt terms
        step4 = MathTex(
            r"= 3t^2",
            r"{} + 3t\,dt + dt^2",
            font_size=step3.font_size,
        )
        step4[0].set_color(RESULT_COLOR)
        step4[1].set_color(INK_FAINT)
        step4.move_to(step3)

        # 2. Small geometric graph of s(t) = t^3 on the right
        right_axes = Axes(
            x_range=[0, 2.001, 1],
            y_range=[0, 8.001, 4],
            x_length=3.0,
            y_length=2.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_tip": False,
                "include_ticks": True,
            },
            tips=False,
        )
        right_axes.move_to(RIGHT * 3.1 + DOWN * 0.35)
        right_axes.add_coordinates(font_size=MIN_FONT)
        for axis in right_axes.get_axes():
            if hasattr(axis, "numbers"):
                for n in axis.numbers:
                    n.set_color(INK_DIM)

        t_lbl = MathTex(r"t", font_size=MIN_FONT, color=X_COLOR)
        t_lbl.next_to(right_axes.c2p(2, 0), RIGHT, buff=0.12)
        s_lbl = MathTex(r"s", font_size=MIN_FONT, color=Y_COLOR)
        s_lbl.next_to(right_axes.c2p(0, 8), UP, buff=0.15)

        t3_curve = right_axes.plot(lambda t: t**3, x_range=[0, 2.0], color=V_COLOR, stroke_width=3.5)
        curve_name = MathTex(r"t^3", font_size=MIN_FONT, color=V_COLOR)
        curve_name.next_to(right_axes.c2p(1.75, 1.75**3), LEFT, buff=0.12)

        # Point and tangent line at t = 1.0 (where slope = 3*1^2 = 3)
        t_pt = 1.0
        p_t = right_axes.c2p(t_pt, t_pt**3)
        dot_t = Dot(p_t, color=RESULT_COLOR, radius=0.08)

        # Tangent line constrained above x-axis
        p_start = right_axes.c2p(0.75, 1.0 - 3.0 * 0.25)
        p_end = right_axes.c2p(1.45, 1.0 + 3.0 * 0.45)
        tangent_seg = Line(p_start, p_end, color=RESULT_COLOR, stroke_width=3.5)

        slope_readout = MathTex(r"\text{slope} = 3t^2", font_size=MIN_FONT, color=RESULT_COLOR)
        slope_readout.move_to(np.array([3.1, 1.45, 0]))
        slope_readout.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        graph_group = VGroup(
            right_axes, t_lbl, s_lbl,
            t3_curve, curve_name, dot_t, tangent_seg, slope_readout
        )

        # First frame shows title, initial equation, and graph
        self.add(title, graph_group, step1)
        self.wait(1.0)

        # Step 2 appears
        self.play(FadeIn(step2), run_time=1.2)
        self.wait(1.0)

        # Step 3 appears
        self.play(FadeIn(step3), run_time=1.2)
        self.wait(1.0)

        # Step 4: dt terms dim/fade as dt -> 0
        self.play(TransformMatchingTex(step3, step4), run_time=1.0)
        self.wait(1.0)

        # Step 5: 3t^2 stays as derivative
        self.play(FadeIn(step5), run_time=1.0)

        # Flash highlight on the result
        flash_rect = SurroundingRectangle(step5, color=HIGHLIGHT, buff=0.12, stroke_width=3)
        self.play(FadeIn(flash_rect), run_time=0.4)
        self.play(FadeOut(flash_rect), run_time=0.4)
        self.wait(2.0)
