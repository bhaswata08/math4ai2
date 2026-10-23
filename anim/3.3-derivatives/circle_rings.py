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

        # 1. Frame one already shows the disc and its radius; the radius sweeps once
        self.add(circle, radius_line, r_label)
        self.wait(1.0)
        self.play(
            Rotate(radius_line, 2 * np.pi - 0.001, about_point=circle_center),
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

        dr_label = MathTex(r"dr = 0.5", font_size=MIN_FONT + 2, color=X_COLOR)
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
        self.wait(0.8)
        # end on one highlighted ring
        self.play(ring_list[4].animate.set_fill(RESULT_COLOR, 0.85), run_time=0.8)
        self.wait(2.0)


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
            color=X_COLOR,
        )
        dr_label = MathTex("dr", font_size=MIN_FONT, color=X_COLOR)
        dr_label.next_to(dr_arrow.get_start(), RIGHT, buff=0.1)

        self.add(isolated_ring, r_line, r_label, dr_arrow, dr_label)
        self.wait(2.0)

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
        side_label = MathTex("dr", font_size=MIN_FONT, color=X_COLOR)
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
        formula[4].set_color(X_COLOR)
        formula.move_to(DOWN * 2.15)

        self.play(Write(formula), run_time=1.2)
        self.wait(2.0)


class ShrinkDr(Scene):
    def construct(self):
        r_val = 1.0
        W = 2 * np.pi * r_val
        strip_center = UP * 1.1
        tracker = ValueTracker(0.4)

        rect = always_redraw(
            lambda: Rectangle(
                width=W, height=tracker.get_value(),
                stroke_color=RESULT_COLOR, stroke_width=2,
                fill_color=RESULT_COLOR, fill_opacity=0.6,
            ).move_to(strip_center)
        )
        ears = always_redraw(
            lambda: get_mismatch_ears(
                r=r_val, dr=tracker.get_value(), center=strip_center,
                fill_color=Y_COLOR, fill_opacity=0.85,
            )
        )
        top_br = always_redraw(lambda: Brace(rect, UP, buff=0.10))
        top_lbl = always_redraw(
            lambda: MathTex(r"2\pi r", font_size=MIN_FONT, color=INK).next_to(top_br, UP, buff=0.08)
        )

        def rows(dr, prev_err=None):
            err = np.pi * dr ** 2
            strip = 2 * np.pi * r_val * dr
            g = VGroup(
                MathTex(rf"dr = {dr:.2f}", font_size=MIN_FONT, color=X_COLOR),
                MathTex(rf"\text{{error}} = \pi\,dr^2 = {err:.3f}", font_size=MIN_FONT, color=Y_COLOR),
                MathTex(rf"\text{{strip}} = 2\pi r\,dr = {strip:.3f}", font_size=MIN_FONT, color=RESULT_COLOR),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            g.move_to(np.array([-1.4, -0.65, 0.0]))
            g.to_edge(LEFT, buff=0.5)
            return g

        self.add(rect, ears, top_br, top_lbl)
        cur = rows(0.4)
        self.add(cur)
        legend = MathTex(r"\text{error} = \text{the two rose corners}", font_size=MIN_FONT, color=Y_COLOR)
        legend.move_to(DOWN * 2.45)
        self.wait(2.0)
        self.play(FadeIn(legend), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(legend), run_time=0.4)

        prev = 0.4
        for dr in (0.2, 0.1, 0.05):
            self.play(FadeOut(cur), run_time=0.3)
            self.play(tracker.animate.set_value(dr), run_time=1.2)
            cur = rows(dr)
            ratio = (np.pi * prev ** 2) / (np.pi * dr ** 2)
            note = MathTex(rf"dr \div 2 \Rightarrow \text{{error}} \div {ratio:.0f}", font_size=MIN_FONT, color=INK)
            note.move_to(np.array([2.6, -2.45, 0.0])) if False else note.move_to(DOWN * 2.45)
            self.play(FadeIn(cur), FadeIn(note), run_time=0.6)
            self.wait(2.0)
            self.play(FadeOut(note), run_time=0.3)
            prev = dr

        # the error per unit of dr goes to zero
        per = MathTex(rf"\text{{error}}/dr = \pi\,dr = {np.pi * prev:.2f} \to 0", font_size=MIN_FONT, color=Y_COLOR)
        per.move_to(DOWN * 2.35)
        self.play(FadeIn(per), run_time=0.8)
        self.wait(2.2)

        self.play(*[FadeOut(m) for m in (rect, ears, top_br, top_lbl, cur, per)], run_time=0.8)
        deriv_formula = MathTex(r"\frac{dA}{dr}", r"=", r"2\pi r", font_size=MIN_FONT + 14)
        deriv_formula[0].set_color(RESULT_COLOR)
        deriv_formula[1].set_color(INK)
        deriv_formula[2].set_color(RESULT_COLOR)
        deriv_formula.move_to(UP * 0.3)
        caption = MathTex(r"\text{circumference} = \text{derivative of area}", font_size=MIN_FONT, color=INK_DIM)
        caption.next_to(deriv_formula, DOWN, buff=0.55)
        self.play(Write(deriv_formula), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(caption), run_time=0.8)
        self.wait(2.5)
