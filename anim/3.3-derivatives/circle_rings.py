# Adapted from 3b1b/videos _2017/eoc/chapter1.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *



def get_ring_polygon(r, dr, center=ORIGIN, num_points=80, fill_color=RESULT_COLOR, fill_opacity=0.75):
    """Constructs an annulus polygon with matching parametrization to get_trapezoid_polygon."""
    outer_angles = np.linspace(-np.pi / 2, 3 * np.pi / 2, num_points)
    outer_pts = [
        center + np.array([(r + dr) * np.cos(th), (r + dr) * np.sin(th), 0.0])
        for th in outer_angles
    ]
    inner_angles = np.linspace(3 * np.pi / 2, -np.pi / 2, num_points)
    inner_pts = [
        center + np.array([r * np.cos(th), r * np.sin(th), 0.0])
        for th in inner_angles
    ]
    poly = Polygon(
        *outer_pts,
        *inner_pts,
        stroke_width=1,
        stroke_color=fill_color,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    return poly


def get_trapezoid_polygon(r, dr, center=ORIGIN, num_points=80, fill_color=RESULT_COLOR, fill_opacity=0.75):
    """Constructs an unwrapped trapezoid with matching parametrization to get_ring_polygon."""
    L_out = 2 * np.pi * (r + dr)
    L_in = 2 * np.pi * r
    bottom_x = np.linspace(-L_out / 2, L_out / 2, num_points)
    bottom_pts = [
        center + np.array([x, -dr / 2, 0.0])
        for x in bottom_x
    ]
    top_x = np.linspace(L_in / 2, -L_in / 2, num_points)
    top_pts = [
        center + np.array([x, dr / 2, 0.0])
        for x in top_x
    ]
    poly = Polygon(
        *bottom_pts,
        *top_pts,
        stroke_width=1,
        stroke_color=fill_color,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    return poly


def get_mismatch_ears(r, dr, center=ORIGIN, fill_color=INK_FAINT, fill_opacity=0.45):
    """Left and right triangular mismatch ears where trapezoid extends beyond the rectangle."""
    W = 2 * np.pi * r
    left_ear = Polygon(
        center + np.array([-W / 2, dr / 2, 0.0]),
        center + np.array([-W / 2, -dr / 2, 0.0]),
        center + np.array([-W / 2 - np.pi * dr, -dr / 2, 0.0]),
        stroke_width=1,
        stroke_color=INK_DIM,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    right_ear = Polygon(
        center + np.array([W / 2, dr / 2, 0.0]),
        center + np.array([W / 2 + np.pi * dr, -dr / 2, 0.0]),
        center + np.array([W / 2, -dr / 2, 0.0]),
        stroke_width=1,
        stroke_color=INK_DIM,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )
    return VGroup(left_ear, right_ear)


class CircleArea(Scene):
    def construct(self):
        # Scale: radius 2.1 scene units, filling ~75% of frame height (5.625 units)
        R = 2.1
        circle_center = LEFT * 1.6

        # Radius line and label above line
        radius_line = Line(circle_center, circle_center + R * RIGHT, color=INK, stroke_width=3)
        radius_line.set_z_index(10)

        # Explicitly position label comfortably above the midpoint of the radius line
        r_mid = circle_center + (R / 2) * RIGHT
        r_label = MathTex("r = 3", font_size=MIN_FONT, color=INK)
        r_label.move_to(r_mid + UP * 0.40)
        r_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        r_label.set_z_index(10)

        circle = Circle(
            radius=R,
            stroke_color=V_COLOR,
            stroke_width=3,
            fill_color=V_COLOR,
            fill_opacity=0.35,
        ).move_to(circle_center)
        circle.set_z_index(1)

        # 1. Circle appears with rotating radius line
        self.play(Create(radius_line), Write(r_label), run_time=1.0)
        self.play(
            Rotate(radius_line, 2 * np.pi - 0.001, about_point=circle_center),
            Create(circle),
            run_time=2.0,
        )
        self.wait(0.5)

        # 2. Display question "Area = ?" on the right
        area_q = MathTex(r"\text{Area} = {?}", font_size=MIN_FONT + 8)
        area_q.set_color_by_tex(r"\text{Area}", RESULT_COLOR)
        area_q.set_color_by_tex("?", RESULT_COLOR)
        area_q.move_to(RIGHT * 2.7 + UP * 0.6)

        self.play(Write(area_q), run_time=1.0)
        self.wait(0.8)

        # 3. Slice into 6 concentric rings (dr = 0.5)
        num_rings = 6
        dr_geom = R / num_rings
        ring_list = []
        for i in range(num_rings):
            r_in = i * dr_geom
            r_out = (i + 1) * dr_geom
            opac = 0.40 if i % 2 == 0 else 0.70
            if i == 0:
                ring = Circle(
                    radius=r_out,
                    stroke_color=BG,
                    stroke_width=2,
                    fill_color=V_COLOR,
                    fill_opacity=opac,
                ).move_to(circle_center)
            else:
                ring = Annulus(
                    inner_radius=r_in,
                    outer_radius=r_out,
                    stroke_color=BG,
                    stroke_width=2,
                    fill_color=V_COLOR,
                    fill_opacity=opac,
                ).move_to(circle_center)
            ring.set_z_index(2)
            ring_list.append(ring)

        rings = VGroup(*ring_list)

        dr_label = MathTex(r"dr = 0.5", font_size=MIN_FONT + 2, color=Y_COLOR)
        dr_label.next_to(area_q, DOWN, buff=0.6)

        # Rings fanning in with lagged animation
        self.play(
            FadeOut(circle),
            FadeIn(rings, lag_ratio=0.25),
            run_time=2.2,
        )
        self.bring_to_front(radius_line, r_label)
        self.play(Write(dr_label), run_time=1.0)
        self.wait(0.8)

        # Subtle rotation to demonstrate independent slices
        self.play(
            Rotate(rings, np.pi / 4, about_point=circle_center),
            run_time=1.8,
        )
        self.bring_to_front(radius_line, r_label)
        self.wait(1.5)


class UnwrapRing(Scene):
    def construct(self):
        # Circle stays on screen dimmed in the upper region
        c_pos = UP * 1.15
        R = 1.35
        num_rings = 5
        dr_geom = R / num_rings

        faded_rings = []
        for i in range(num_rings):
            r_in = i * dr_geom
            r_out = (i + 1) * dr_geom
            opac = 0.15 if i % 2 == 0 else 0.25
            if i == 0:
                r_mob = Circle(
                    radius=r_out,
                    stroke_color=BG,
                    stroke_width=1.5,
                    fill_color=V_COLOR,
                    fill_opacity=opac,
                ).move_to(c_pos)
            else:
                r_mob = Annulus(
                    inner_radius=r_in,
                    outer_radius=r_out,
                    stroke_color=BG,
                    stroke_width=1.5,
                    fill_color=V_COLOR,
                    fill_opacity=opac,
                ).move_to(c_pos)
            faded_rings.append(r_mob)
        faded_circle = VGroup(*faded_rings)
        self.add(faded_circle)

        # Isolate ring at r = 0.90, dr = 0.28 (clearly visible in radius-1.35 circle)
        r_val = 0.90
        dr_val = 0.28

        isolated_ring = get_ring_polygon(
            r=r_val,
            dr=dr_val,
            center=c_pos,
            fill_color=RESULT_COLOR,
            fill_opacity=0.8,
        )
        self.play(FadeIn(isolated_ring), run_time=0.8)

        # r label placed along radius line inside, deep in interior
        r_end = c_pos + r_val * (np.cos(np.pi / 4) * RIGHT + np.sin(np.pi / 4) * UP)
        r_line = Line(c_pos, r_end, color=INK, stroke_width=2.5)
        r_label = MathTex("r", font_size=MIN_FONT, color=INK)
        r_label.move_to(c_pos + (r_val * 0.5) * (np.cos(np.pi / 4) * RIGHT + np.sin(np.pi / 4) * UP) + UP * 0.22 + LEFT * 0.12)

        # dr arrow outside the ring on the right with no overlap
        dr_arrow = Arrow(
            c_pos + (r_val + dr_val + 0.7) * RIGHT,
            c_pos + (r_val + dr_val) * RIGHT,
            buff=0.05,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25,
            color=Y_COLOR,
        )
        dr_label = MathTex("dr", font_size=MIN_FONT, color=Y_COLOR)
        dr_label.next_to(dr_arrow.get_start(), RIGHT, buff=0.1)

        self.play(
            Create(r_line),
            Write(r_label),
            Create(dr_arrow),
            Write(dr_label),
            run_time=1.2,
        )
        self.wait(0.8)

        # Clear ring labels before unrolling
        self.play(
            FadeOut(r_line),
            FadeOut(r_label),
            FadeOut(dr_arrow),
            FadeOut(dr_label),
            run_time=0.6,
        )

        # Physical unroll: same mobject morphs into flat strip directly below circle
        strip_y = -1.25
        unwrapped_strip = get_trapezoid_polygon(
            r=r_val,
            dr=dr_val,
            center=np.array([0.0, strip_y, 0.0]),
            fill_color=RESULT_COLOR,
            fill_opacity=0.8,
        )
        self.play(Transform(isolated_ring, unwrapped_strip), run_time=2.5)
        self.wait(0.6)

        # Approximate as rectangle of width 2*pi*r and height dr
        W = 2 * np.pi * r_val
        rect_approx = Rectangle(
            width=W,
            height=dr_val,
            stroke_color=RESULT_COLOR,
            stroke_width=2,
            fill_color=RESULT_COLOR,
            fill_opacity=0.8,
        ).move_to(np.array([0.0, strip_y, 0.0]))

        self.play(Transform(isolated_ring, rect_approx), run_time=1.2)

        # Braces attached exactly to the rectangle
        top_brace = Brace(rect_approx, UP, buff=0.08)
        top_label = MathTex(r"2\pi r", font_size=MIN_FONT, color=INK)
        top_label.next_to(top_brace, UP, buff=0.08)

        side_brace = Brace(rect_approx, LEFT, buff=0.08)
        side_label = MathTex("dr", font_size=MIN_FONT, color=Y_COLOR)
        side_label.next_to(side_brace, LEFT, buff=0.08)

        self.play(
            Create(top_brace),
            Write(top_label),
            Create(side_brace),
            Write(side_label),
            run_time=1.2,
        )
        self.wait(0.8)

        # End on MathTex "dA \approx 2\pi r \, dr"
        formula = MathTex(r"dA", r"\approx", r"2\pi r", r"\,", r"dr", font_size=MIN_FONT + 6)
        formula[0].set_color(RESULT_COLOR)
        formula[1].set_color(INK)
        formula[2].set_color(INK)
        formula[4].set_color(Y_COLOR)
        formula.move_to(DOWN * 2.15)

        self.play(Write(formula), run_time=1.2)
        self.wait(2.0)


class ShrinkDr(Scene):
    def construct(self):
        r_val = 1.0
        W = 2 * np.pi * r_val  # approx 6.283
        strip_center = UP * 1.05

        # Continuous ValueTracker for dr
        tracker = ValueTracker(0.38)

        # Continuously updated rectangle
        rect = always_redraw(
            lambda: Rectangle(
                width=W,
                height=tracker.get_value(),
                stroke_color=RESULT_COLOR,
                stroke_width=2,
                fill_color=RESULT_COLOR,
                fill_opacity=0.6,
            ).move_to(strip_center)
        )

        # Continuously updated mismatch ears (error term: INK_FAINT fill)
        ears = always_redraw(
            lambda: get_mismatch_ears(
                r=r_val,
                dr=tracker.get_value(),
                center=strip_center,
                fill_color=INK_FAINT,
                fill_opacity=0.45,
            )
        )

        # Fixed top width brace = 2*pi*r
        top_br = always_redraw(lambda: Brace(rect, UP, buff=0.10))
        top_lbl = always_redraw(
            lambda: MathTex(r"2\pi r", font_size=MIN_FONT, color=INK).next_to(top_br, UP, buff=0.08)
        )

        # Non-overlapping readouts:
        # Line 1: dr readout at y = -0.15
        dr_readout = always_redraw(
            lambda: MathTex(
                f"dr = {tracker.get_value():.2f}",
                font_size=MIN_FONT,
                color=Y_COLOR,
            ).move_to(DOWN * 0.15)
        )

        # Line 2: relative error readout at y = -1.15
        err_label = MathTex(r"\frac{\text{error}}{\text{strip area}} \approx", font_size=MIN_FONT, color=INK)
        err_label.move_to(LEFT * 0.55 + DOWN * 1.15)

        err_num = DecimalNumber(
            tracker.get_value() / (2 * r_val),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        err_num.add_updater(lambda d: d.set_value(tracker.get_value() / (2 * r_val)))
        err_num.add_updater(lambda d: d.next_to(err_label, RIGHT, buff=0.22))

        # 1. Initial display at dr = 0.38
        self.play(
            FadeIn(rect),
            FadeIn(ears),
            Create(top_br),
            Write(top_lbl),
            FadeIn(dr_readout),
            FadeIn(err_label),
            FadeIn(err_num),
            run_time=1.5,
        )

        # Momentary highlight flash of the mismatch ears
        flash_ears = get_mismatch_ears(
            r=r_val,
            dr=0.38,
            center=strip_center,
            fill_color=HIGHLIGHT,
            fill_opacity=0.8,
        )
        self.play(FadeIn(flash_ears), run_time=0.4)
        self.play(FadeOut(flash_ears), run_time=0.4)
        self.wait(1.0)

        # 2. ValueTracker continuously shrinks dr from 0.38 to 0.04
        self.play(
            tracker.animate.set_value(0.04),
            run_time=5.0,
            rate_func=linear,
        )
        self.wait(1.5)

        # 3. Fade out strip and readout for final derivative formula
        self.play(
            FadeOut(rect),
            FadeOut(ears),
            FadeOut(top_br),
            FadeOut(top_lbl),
            FadeOut(dr_readout),
            FadeOut(err_label),
            FadeOut(err_num),
            run_time=1.0,
        )

        # Big, centered derivative formula
        deriv_formula = MathTex(r"\frac{dA}{dr}", r"=", r"2\pi r", font_size=MIN_FONT + 14)
        deriv_formula[0].set_color(RESULT_COLOR)
        deriv_formula[1].set_color(INK)
        deriv_formula[2].set_color(RESULT_COLOR)
        deriv_formula.move_to(ORIGIN + UP * 0.45)

        caption = MathTex(r"\text{circumference} = \text{derivative of area}", font_size=MIN_FONT, color=INK_DIM)
        caption.next_to(deriv_formula, DOWN, buff=0.55)

        self.play(Write(deriv_formula), FadeIn(caption), run_time=1.5)
        self.wait(2.5)
