# Block 1.1. Authored for this course; idea from Crimson Sciences, 'You've Learned The Dot Product Wrong' (youtube GPZ_WlwcEjI).

import numpy as np
from shared.anim.house import *


class DotCosineForm(Scene):
    """Start with v=[3,1] and w=[1,2] on the plane (as in DotGeometric),
    angle arc theta between them.
    Draw the perpendicular drop from w's tip to the line through v and the
    projection segment in RESULT_COLOR; label the projection length '||w|| cos θ'.
    Then build, at the left on a background card:
        v · w = ||v|| (||w|| cos θ)
              = ||v|| ||w|| cos θ
    Then dim ||v|| and ||w|| with a small note '≥ 0 always' under them,
    and box cos θ in HIGHLIGHT with a note 'sign lives here'.
    Numbers: v·w = 5, ||v||=√10, ||w||=√5, cos θ = 1/√2, θ=45°.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Givens: v = [3, 1], w = [1, 2]
        # v . w = 3*1 + 1*2 = 5
        # ||v|| = sqrt(10), ||w|| = sqrt(5)
        # cos(theta) = 5 / (sqrt(10)*sqrt(5)) = 5 / sqrt(50) = 1 / sqrt(2) -> theta = 45 deg
        # proj = (v . w / ||v||^2) * v = (5 / 10) * [3, 1] = [1.5, 0.5]
        v_coords = np.array([3.0, 1.0, 0.0])
        w_coords = np.array([1.0, 2.0, 0.0])
        proj_coords = np.array([1.5, 0.5, 0.0])

        theta_v = np.arctan2(1.0, 3.0)  # ~18.435 deg
        theta_w = np.arctan2(2.0, 1.0)  # ~63.435 deg
        d_theta = theta_w - theta_v     # 45 deg = PI / 4

        # Fixed given vector v (teal)
        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_coords, DR, buff=0.15)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Second given vector w (purple)
        w_arr = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w_coords, UL, buff=0.15)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Angle arc theta between v and w
        arc_radius = 0.8
        arc_theta = Arc(
            radius=arc_radius,
            start_angle=theta_v,
            angle=d_theta,
            color=HIGHLIGHT,
            stroke_width=3.5,
        )
        mid_angle = theta_v + d_theta / 2.0
        l_theta = MathTex(r"\theta", font_size=MIN_FONT, color=HIGHLIGHT)
        l_theta.move_to(1.15 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0.0]))
        l_theta.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows the givens (vectors on screen, angle arc theta, plane)
        self.add(v_arr, l_v, w_arr, l_w, arc_theta, l_theta)
        self.wait(1.5)

        # 2. Line through v (starts just left of origin, stays clear of left card)
        u_v = v_coords / np.linalg.norm(v_coords)
        line_v = Line(-0.35 * u_v, 3.6 * u_v, color=INK_DIM, stroke_width=2.5)
        self.play(Create(line_v), run_time=1.0)
        self.wait(0.3)

        # 3. Dashed drop line from w perpendicular to line through v
        drop_line = DashedLine(
            w_coords,
            proj_coords,
            color=INK_DIM,
            stroke_width=3,
            dash_length=0.08,
        )

        # Right angle mark at foot [1.5, 0.5]
        u_n = (w_coords - proj_coords) / np.linalg.norm(w_coords - proj_coords)
        s = 0.20
        p1 = proj_coords - s * u_v
        p2 = proj_coords - s * u_v + s * u_n
        p3 = proj_coords + s * u_n
        elbow = VGroup(
            Line(p1, p2, stroke_width=2.5, color=HIGHLIGHT),
            Line(p2, p3, stroke_width=2.5, color=HIGHLIGHT),
        )
        self.play(Create(drop_line), Create(elbow), run_time=1.0)
        self.wait(0.3)

        # 4. Projection vector along v and label ||w|| cos theta
        proj_arr = Arrow(
            ORIGIN,
            proj_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_proj = MathTex(r"\|\vec{w}\|\cos\theta", font_size=MIN_FONT, color=RESULT_COLOR)
        l_proj.move_to(np.array([1.25, -0.22, 0.0]))
        l_proj.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(GrowArrow(proj_arr), Write(l_proj), run_time=1.1)
        self.wait(0.5)

        # 5. Build on the left a background card
        card_w = 4.1
        card_h = 4.6
        card_center = np.array([-2.65, 0.0, 0.0])
        card_bg = RoundedRectangle(
            corner_radius=0.15,
            width=card_w,
            height=card_h,
            stroke_color=INK_DIM,
            stroke_width=1.5,
            fill_color=BG,
            fill_opacity=0.92,
        ).move_to(card_center)

        # First equation: v . w = ||v|| (||w|| cos theta)
        eq1 = MathTex(
            r"\vec{v} \cdot \vec{w} =",
            r"\|\vec{v}\|",
            r"(",
            r"\|\vec{w}\|\cos\theta",
            r")",
            font_size=MIN_FONT,
        )
        eq1[0].set_color(INK)
        eq1[1].set_color(V_COLOR)
        eq1[2].set_color(INK)
        eq1[3].set_color(RESULT_COLOR)
        eq1[4].set_color(INK)
        eq1.move_to(np.array([-2.65, 1.5, 0.0]))

        self.play(FadeIn(card_bg), Write(eq1), run_time=1.2)
        self.wait(0.8)

        # Second equation: = ||v|| ||w|| cos theta
        eq2 = MathTex(
            r"=",
            r"\|\vec{v}\|",
            r"\|\vec{w}\|",
            r"\cos\theta",
            font_size=MIN_FONT + 2,
        )
        eq2[0].set_color(INK)
        eq2[1].set_color(V_COLOR)
        eq2[2].set_color(W_COLOR)
        eq2[3].set_color(INK)
        eq2.move_to(np.array([-2.65, 0.7, 0.0]))

        self.play(Write(eq2), run_time=1.0)
        self.wait(0.6)

        # 6. Dim ||v|| and ||w|| with note ">= 0 always" under them
        # Box cos theta in HIGHLIGHT with note "sign lives here"
        v_w_group = VGroup(eq2[1], eq2[2])
        note_nonneg = Tex(r"$\ge 0$ always", font_size=MIN_FONT, color=INK_DIM)
        note_nonneg.move_to(np.array([v_w_group.get_x() - 0.1, 0.05, 0.0]))

        box_cos = SurroundingRectangle(eq2[3], color=HIGHLIGHT, buff=0.08, stroke_width=2.5)
        note_sign = Tex(r"sign lives here", font_size=MIN_FONT, color=HIGHLIGHT)
        note_sign.move_to(np.array([box_cos.get_x(), -0.7, 0.0]))

        arr_sign = Arrow(
            np.array([box_cos.get_x(), -0.52, 0.0]),
            np.array([box_cos.get_x(), -0.15, 0.0]),
            buff=0.04,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.35,
            color=HIGHLIGHT,
        )

        self.play(
            eq2[1].animate.set_color(INK_FAINT),
            eq2[2].animate.set_color(INK_FAINT),
            FadeIn(note_nonneg),
            Create(box_cos),
            Create(arr_sign),
            FadeIn(note_sign),
            run_time=1.2,
        )
        self.wait(0.8)

        # 7. Numerical check at bottom of card
        # v.w = 5, ||v||=sqrt(10), ||w||=sqrt(5), cos theta = 1/sqrt(2)
        num_check = MathTex(
            r"5",
            r"=",
            r"\sqrt{10}",
            r"\cdot",
            r"\sqrt{5}",
            r"\cdot",
            r"\frac{1}{\sqrt{2}}",
            font_size=MIN_FONT,
        )
        num_check[0].set_color(INK)
        num_check[1].set_color(INK)
        num_check[2].set_color(V_COLOR)
        num_check[3].set_color(INK)
        num_check[4].set_color(W_COLOR)
        num_check[5].set_color(INK)
        num_check[6].set_color(HIGHLIGHT)
        num_check.move_to(np.array([-2.65, -1.55, 0.0]))

        self.play(Write(num_check), run_time=1.0)
        self.wait(2.5)


class DotAlignmentCircles(Scene):
    """Three unit circles side by side (each radius ~1.1 units across 10-unit frame),
    headed 'v·w < 0', 'v·w = 0', 'v·w > 0'.
    In each circle v is a fixed teal arrow pointing right from centre (along theta=0).
    Shaded ranges:
      - left circle: obtuse arc 90° < theta < 270° (Y_COLOR thick arc + sector fill)
      - middle circle: points theta = 90° and theta = 270° (HIGHLIGHT dots, right-angle mark)
      - right circle: acute range -90° < theta < 90° (X_COLOR thick arc + sector fill)
    Label 90° and 270° on each circle.
    w arrow sweeps through each region (middle snaps to 90° then 270°).
    Caption at bottom: 'The dot product measures alignment'
    Verdict under each circle: 'misaligned', 'perpendicular', 'aligned'.
    """

    def construct(self):
        # Centers of the 3 circles
        R = 1.02
        c1 = np.array([-3.2, 0.22, 0.0])
        c2 = np.array([0.0, 0.22, 0.0])
        c3 = np.array([3.2, 0.22, 0.0])

        centers = [c1, c2, c3]

        # Subtle dashed coordinate crosshairs inside each circle
        crosshairs = VGroup()
        circles = VGroup()
        for c in centers:
            ch_h = DashedLine(c - R * RIGHT, c + R * RIGHT, color=GRID, stroke_width=1.5, dash_length=0.06)
            ch_v = DashedLine(c - R * UP, c + R * UP, color=GRID, stroke_width=1.5, dash_length=0.06)
            circ = Circle(radius=R, color=INK_DIM, stroke_width=2.0).move_to(c)
            crosshairs.add(ch_h, ch_v)
            circles.add(circ)

        # Headings above circles
        head1 = MathTex(r"\vec{v}\cdot\vec{w} < 0", font_size=MIN_FONT + 4, color=Y_COLOR).move_to(np.array([-3.2, 2.18, 0.0]))
        head2 = MathTex(r"\vec{v}\cdot\vec{w} = 0", font_size=MIN_FONT + 4, color=HIGHLIGHT).move_to(np.array([0.0, 2.18, 0.0]))
        head3 = MathTex(r"\vec{v}\cdot\vec{w} > 0", font_size=MIN_FONT + 4, color=X_COLOR).move_to(np.array([3.2, 2.18, 0.0]))

        # Shaded θ regions
        # Left circle: obtuse arc 90° < theta < 270° (Y_COLOR)
        sec1 = Sector(
            radius=R,
            start_angle=PI / 2,
            angle=PI,
            arc_center=c1,
            color=Y_COLOR,
            fill_opacity=0.18,
            stroke_width=0,
        )
        arc1 = Arc(
            radius=R,
            start_angle=PI / 2,
            angle=PI,
            arc_center=c1,
            color=Y_COLOR,
            stroke_width=5.0,
        )

        # Middle circle: points at 90° and 270° (HIGHLIGHT dots) and right-angle mark
        p_top = c2 + R * UP
        p_bot = c2 + R * DOWN
        dot_top = Dot(p_top, radius=0.08, color=HIGHLIGHT)
        dot_bot = Dot(p_bot, radius=0.08, color=HIGHLIGHT)

        s_ra = 0.20
        elbow_top = VGroup(
            Line(c2 + s_ra * RIGHT, c2 + s_ra * RIGHT + s_ra * UP, stroke_width=2.5, color=HIGHLIGHT),
            Line(c2 + s_ra * RIGHT + s_ra * UP, c2 + s_ra * UP, stroke_width=2.5, color=HIGHLIGHT),
        )
        elbow_bot = VGroup(
            Line(c2 + s_ra * RIGHT, c2 + s_ra * RIGHT - s_ra * UP, stroke_width=2.5, color=HIGHLIGHT),
            Line(c2 + s_ra * RIGHT - s_ra * UP, c2 - s_ra * UP, stroke_width=2.5, color=HIGHLIGHT),
        )

        # Right circle: acute range -90° < theta < 90° (X_COLOR)
        sec3 = Sector(
            radius=R,
            start_angle=-PI / 2,
            angle=PI,
            arc_center=c3,
            color=X_COLOR,
            fill_opacity=0.18,
            stroke_width=0,
        )
        arc3 = Arc(
            radius=R,
            start_angle=-PI / 2,
            angle=PI,
            arc_center=c3,
            color=X_COLOR,
            stroke_width=5.0,
        )

        # Angle labels 90° and 270° on each circle
        angle_labels = VGroup()
        for c in centers:
            lbl_90 = MathTex(r"90^\circ", font_size=MIN_FONT, color=INK_DIM)
            lbl_90.move_to(c + (R + 0.22) * UP)
            lbl_90.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

            lbl_270 = MathTex(r"270^\circ", font_size=MIN_FONT, color=INK_DIM)
            lbl_270.move_to(c + (R + 0.22) * DOWN)
            lbl_270.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

            angle_labels.add(lbl_90, lbl_270)

        # Fixed teal v arrow pointing right in each circle (along theta = 0)
        v_arrows = VGroup()
        v_labels = VGroup()
        for c in centers:
            v_arr = Arrow(
                c,
                c + R * RIGHT,
                buff=0,
                stroke_width=5.5,
                max_tip_length_to_length_ratio=0.25,
                color=V_COLOR,
            )
            l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
            l_v.move_to(c + 0.52 * RIGHT - 0.25 * UP)
            v_arrows.add(v_arr)
            v_labels.add(l_v)

        # Purple w arrows and labels
        # Circle 1: starts at 135° (obtuse)
        th1 = 135 * DEGREES
        w1_dir = np.array([np.cos(th1), np.sin(th1), 0.0])
        w1_arr = Arrow(c1, c1 + R * w1_dir, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR)
        l_w1 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w1.move_to(c1 + (R + 0.28) * w1_dir)
        l_w1.add_background_rectangle(color=BG, opacity=0.85, buff=0.05)

        # Circle 2: starts at 90° (perpendicular), label w next to top arrowhead
        w2_dir = UP
        w2_arr = Arrow(c2, c2 + R * w2_dir, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR)
        l_w2 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w2.move_to(c2 + 0.82 * R * UP + 0.38 * LEFT)
        l_w2.add_background_rectangle(color=BG, opacity=0.85, buff=0.05)

        # Circle 3: starts at 55° (acute)
        th3 = 55 * DEGREES
        w3_dir = np.array([np.cos(th3), np.sin(th3), 0.0])
        w3_arr = Arrow(c3, c3 + R * w3_dir, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR)
        l_w3 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w3.move_to(c3 + (R + 0.28) * w3_dir)
        l_w3.add_background_rectangle(color=BG, opacity=0.85, buff=0.05)

        # 1. Frame one shows givens: circles, crosshairs, headings, shaded ranges, dots/elbow, angle labels, v and w
        self.add(
            crosshairs, circles,
            head1, head2, head3,
            sec1, arc1,
            dot_top, dot_bot, elbow_top,
            sec3, arc3,
            angle_labels,
            v_arrows, v_labels,
            w1_arr, l_w1,
            w2_arr, l_w2,
            w3_arr, l_w3,
        )
        self.wait(1.5)

        # 2. Beat 1: Circle 1 w sweeps through obtuse region (135° -> 215° -> 145°)
        th1_tracker = ValueTracker(135 * DEGREES)

        def update_w1(mob):
            val = th1_tracker.get_value()
            d = np.array([np.cos(val), np.sin(val), 0.0])
            mob.become(Arrow(c1, c1 + R * d, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR))

        def update_lw1(mob):
            val = th1_tracker.get_value()
            d = np.array([np.cos(val), np.sin(val), 0.0])
            mob.move_to(c1 + (R + 0.28) * d)

        w1_arr.add_updater(update_w1)
        l_w1.add_updater(update_lw1)

        self.play(th1_tracker.animate.set_value(215 * DEGREES), run_time=1.8, rate_func=smooth)
        self.play(th1_tracker.animate.set_value(145 * DEGREES), run_time=1.4, rate_func=smooth)
        self.wait(0.4)
        w1_arr.clear_updaters()
        l_w1.clear_updaters()

        # 3. Beat 2: Circle 2 w snaps from 90° to 270°
        w2_down = Arrow(c2, c2 + R * DOWN, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR)
        l_w2_down = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w2_down.move_to(c2 + 0.82 * R * DOWN + 0.38 * LEFT)
        l_w2_down.add_background_rectangle(color=BG, opacity=0.85, buff=0.05)

        self.play(
            Transform(w2_arr, w2_down),
            Transform(l_w2, l_w2_down),
            FadeOut(elbow_top),
            FadeIn(elbow_bot),
            run_time=0.9,
            rate_func=rush_into,
        )
        self.wait(0.8)

        # 4. Beat 3: Circle 3 w sweeps through acute region (55° -> -55° -> 45°)
        th3_tracker = ValueTracker(55 * DEGREES)

        def update_w3(mob):
            val = th3_tracker.get_value()
            d = np.array([np.cos(val), np.sin(val), 0.0])
            mob.become(Arrow(c3, c3 + R * d, buff=0, stroke_width=5.5, max_tip_length_to_length_ratio=0.25, color=W_COLOR))

        def update_lw3(mob):
            val = th3_tracker.get_value()
            d = np.array([np.cos(val), np.sin(val), 0.0])
            mob.move_to(c3 + (R + 0.28) * d)

        w3_arr.add_updater(update_w3)
        l_w3.add_updater(update_lw3)

        self.play(th3_tracker.animate.set_value(-55 * DEGREES), run_time=1.8, rate_func=smooth)
        self.play(th3_tracker.animate.set_value(45 * DEGREES), run_time=1.4, rate_func=smooth)
        self.wait(0.4)
        w3_arr.clear_updaters()
        l_w3.clear_updaters()

        # 5. Verdicts under each circle
        verdict1 = Tex(r"\textbf{misaligned}", font_size=MIN_FONT, color=Y_COLOR).move_to(np.array([-3.2, -1.68, 0.0]))
        verdict2 = Tex(r"\textbf{perpendicular}", font_size=MIN_FONT, color=HIGHLIGHT).move_to(np.array([0.0, -1.68, 0.0]))
        verdict3 = Tex(r"\textbf{aligned}", font_size=MIN_FONT, color=X_COLOR).move_to(np.array([3.2, -1.68, 0.0]))

        caption = Tex(r"The dot product measures alignment", font_size=MIN_FONT + 2, color=INK)
        caption.move_to(np.array([0.0, -2.28, 0.0]))

        self.play(
            FadeIn(verdict1),
            FadeIn(verdict2),
            FadeIn(verdict3),
            FadeIn(caption),
            run_time=1.2,
        )
        self.wait(2.5)
