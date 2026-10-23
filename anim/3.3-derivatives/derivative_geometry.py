# Adapted from 3b1b/videos _2017/eoc/chapter3.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *


class NudgeSquare(Scene):
    def construct(self):
        L = 2.6
        sq_center = np.array([-2.4, -0.25, 0.0])

        square = Square(
            side_length=L,
            stroke_color=V_COLOR,
            stroke_width=2.5,
            fill_color=V_COLOR,
            fill_opacity=0.35,
        ).move_to(sq_center)

        left_brace = Brace(square, LEFT, buff=0.10)
        left_label = MathTex("x", font_size=MIN_FONT, color=INK)
        left_label.next_to(left_brace, LEFT, buff=0.08)

        top_brace = Brace(square, UP, buff=0.10)
        top_label = MathTex("x", font_size=MIN_FONT, color=INK)
        top_label.next_to(top_brace, UP, buff=0.08)

        area_label = MathTex("x^2", font_size=MIN_FONT + 4, color=V_COLOR)
        area_label.move_to(sq_center)

        f_label = MathTex(r"f(x) = x^2", font_size=MIN_FONT + 4, color=V_COLOR)
        f_label.move_to(np.array([2.4, 1.85, 0.0]))
        f_label.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0: givens are visible
        self.add(square, left_brace, left_label, top_brace, top_label, area_label, f_label)
        self.wait(1.0)

        # Initial nudge dx = 0.46
        dx_val = 0.46
        sq_bottom = sq_center[1] - L / 2
        sq_right = sq_center[0] + L / 2

        right_rect = Rectangle(
            width=dx_val,
            height=L,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
        )
        right_rect.move_to(np.array([sq_right + dx_val / 2, sq_center[1], 0.0]))

        bottom_rect = Rectangle(
            width=L,
            height=dx_val,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
        )
        bottom_rect.move_to(np.array([sq_center[0], sq_bottom - dx_val / 2, 0.0]))

        corner_sq = Rectangle(
            width=dx_val,
            height=dx_val,
            stroke_color=INK_FAINT,
            stroke_width=1.5,
            fill_color=INK_FAINT,
            fill_opacity=0.45,
        )
        corner_sq.move_to(np.array([sq_right + dx_val / 2, sq_bottom - dx_val / 2, 0.0]))

        dx_brace_r = Brace(corner_sq, RIGHT, buff=0.08)
        dx_label_r = MathTex("dx", font_size=MIN_FONT, color=X_COLOR)
        dx_label_r.next_to(dx_brace_r, RIGHT, buff=0.08)

        dx_brace_b = Brace(corner_sq, DOWN, buff=0.08)
        dx_label_b = MathTex("dx", font_size=MIN_FONT, color=X_COLOR)
        dx_label_b.next_to(dx_brace_b, DOWN, buff=0.08)

        self.play(
            FadeIn(right_rect),
            FadeIn(bottom_rect),
            FadeIn(corner_sq),
            Create(dx_brace_r),
            Write(dx_label_r),
            Create(dx_brace_b),
            Write(dx_label_b),
            run_time=1.5,
        )
        self.wait(0.6)

        # Formula: df = 2x dx + (dx)^2
        df_eq = MathTex(
            r"df", r"=", r"2x\,dx", r"+", r"(dx)^2",
            font_size=MIN_FONT + 2,
        )
        df_eq[0].set_color(RESULT_COLOR)
        df_eq[1].set_color(INK)
        df_eq[2].set_color(RESULT_COLOR)
        df_eq[3].set_color(INK)
        df_eq[4].set_color(INK_FAINT)
        df_eq.move_to(np.array([2.4, 0.85, 0.0]))

        strips_tag = MathTex(r"\text{two strips } (x \cdot dx)", font_size=MIN_FONT, color=RESULT_COLOR)
        strips_tag.move_to(np.array([2.4, 0.20, 0.0]))

        corner_tag = MathTex(r"\text{corner } (dx \cdot dx)", font_size=MIN_FONT, color=INK_FAINT)
        corner_tag.move_to(np.array([2.4, -0.35, 0.0]))

        self.play(Write(df_eq), run_time=1.2)
        self.play(FadeIn(strips_tag), FadeIn(corner_tag), run_time=1.0)
        self.wait(0.6)

        # Momentary highlight flash on the corner square (negligible term)
        flash_sq = corner_sq.copy().set_color(HIGHLIGHT).set_fill(HIGHLIGHT, opacity=0.8)
        self.play(FadeIn(flash_sq), run_time=0.35)
        self.play(FadeOut(flash_sq), run_time=0.35)
        self.wait(0.5)

        # Shrink dx with ValueTracker
        tracker = ValueTracker(dx_val)

        # Remove static pieces and braces before dynamic shrink
        self.remove(right_rect, bottom_rect, corner_sq, dx_brace_r, dx_label_r, dx_brace_b, dx_label_b)

        dyn_r = always_redraw(
            lambda: Rectangle(
                width=tracker.get_value(),
                height=L,
                stroke_color=RESULT_COLOR,
                stroke_width=1.5,
                fill_color=RESULT_COLOR,
                fill_opacity=0.65,
            ).move_to(np.array([sq_right + tracker.get_value() / 2, sq_center[1], 0.0]))
        )
        dyn_b = always_redraw(
            lambda: Rectangle(
                width=L,
                height=tracker.get_value(),
                stroke_color=RESULT_COLOR,
                stroke_width=1.5,
                fill_color=RESULT_COLOR,
                fill_opacity=0.65,
            ).move_to(np.array([sq_center[0], sq_bottom - tracker.get_value() / 2, 0.0]))
        )
        dyn_c = always_redraw(
            lambda: Rectangle(
                width=tracker.get_value(),
                height=tracker.get_value(),
                stroke_color=INK_FAINT,
                stroke_width=1.2,
                fill_color=INK_FAINT,
                fill_opacity=0.45,
            ).move_to(np.array([sq_right + tracker.get_value() / 2, sq_bottom - tracker.get_value() / 2, 0.0]))
        )

        self.add(dyn_r, dyn_b, dyn_c)

        # Tracker readout on the right
        readout = always_redraw(
            lambda: MathTex(
                f"dx = {tracker.get_value():.2f}",
                font_size=MIN_FONT,
                color=X_COLOR,
            ).move_to(np.array([2.4, -0.95, 0.0]))
        )
        self.play(FadeIn(readout), run_time=0.6)

        # Continuous shrink from 0.46 down to 0.04
        self.play(
            tracker.animate.set_value(0.04),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(1.0)

        # Clean up tags and readout for final derivative
        self.play(
            FadeOut(strips_tag),
            FadeOut(corner_tag),
            FadeOut(readout),
            FadeOut(df_eq),
            run_time=0.8,
        )

        # Derivative step then final formula
        step1 = MathTex(
            r"\frac{df}{dx} = 2x + dx",
            font_size=MIN_FONT + 4,
            color=INK,
        ).move_to(np.array([2.4, 0.10, 0.0]))
        step1.set_color_by_tex("2x", RESULT_COLOR)
        step1.set_color_by_tex("dx", X_COLOR)

        deriv_final = MathTex(
            r"\frac{d(x^2)}{dx} = 2x",
            font_size=MIN_FONT + 8,
            color=RESULT_COLOR,
        ).move_to(np.array([2.4, 0.10, 0.0]))

        self.play(Write(step1), run_time=1.0)
        self.wait(1.0)
        self.play(TransformMatchingTex(step1, deriv_final), run_time=1.2)
        self.wait(2.2)


class NudgeCube(ThreeDScene):
    def construct(self):
        # 3D view with camera looking at cube
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)

        # Scaled up ~15% (1.6 * 1.15 = 1.84)
        x_len = 1.84
        dx_val = 0.38
        c_pos = np.array([-2.8, -0.05, -0.1])

        # Main cube
        cube = Cube(
            side_length=x_len,
            fill_color=V_COLOR,
            fill_opacity=0.35,
            stroke_color=V_COLOR,
            stroke_width=1.5,
        ).move_to(c_pos)

        # Three slabs (x^2 * dx) on +X, +Y, +Z faces
        slab_x = Prism(
            dimensions=[dx_val, x_len, x_len],
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
        ).move_to(c_pos + np.array([x_len / 2 + dx_val / 2, 0.0, 0.0]))

        slab_y = Prism(
            dimensions=[x_len, dx_val, x_len],
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
        ).move_to(c_pos + np.array([0.0, x_len / 2 + dx_val / 2, 0.0]))

        slab_z = Prism(
            dimensions=[x_len, x_len, dx_val],
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
        ).move_to(c_pos + np.array([0.0, 0.0, x_len / 2 + dx_val / 2]))

        # Three edge bars (x * dx * dx) - faint
        bar_xy = Prism(
            dimensions=[dx_val, dx_val, x_len],
            fill_color=INK_FAINT,
            fill_opacity=0.25,
            stroke_color=INK_FAINT,
            stroke_width=1.0,
        ).move_to(c_pos + np.array([x_len / 2 + dx_val / 2, x_len / 2 + dx_val / 2, 0.0]))

        bar_xz = Prism(
            dimensions=[dx_val, x_len, dx_val],
            fill_color=INK_FAINT,
            fill_opacity=0.25,
            stroke_color=INK_FAINT,
            stroke_width=1.0,
        ).move_to(c_pos + np.array([x_len / 2 + dx_val / 2, 0.0, x_len / 2 + dx_val / 2]))

        bar_yz = Prism(
            dimensions=[x_len, dx_val, dx_val],
            fill_color=INK_FAINT,
            fill_opacity=0.25,
            stroke_color=INK_FAINT,
            stroke_width=1.0,
        ).move_to(c_pos + np.array([0.0, x_len / 2 + dx_val / 2, x_len / 2 + dx_val / 2]))

        # Corner cube (dx^3) - faint
        corner = Prism(
            dimensions=[dx_val, dx_val, dx_val],
            fill_color=INK_FAINT,
            fill_opacity=0.25,
            stroke_color=INK_FAINT,
            stroke_width=1.0,
        ).move_to(c_pos + np.array([x_len / 2 + dx_val / 2, x_len / 2 + dx_val / 2, x_len / 2 + dx_val / 2]))

        # Fixed in frame UI labels on the right
        title = MathTex(r"f(x) = x^3", font_size=MIN_FONT + 4, color=V_COLOR)
        title.to_corner(UP + LEFT, buff=0.35)

        eq1 = MathTex(r"d(x^3) \approx 3x^2\,dx", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        eq1.move_to(np.array([2.4, 1.35, 0.0]))

        tag_slabs = MathTex(r"3\text{ slabs: } 3x^2\,dx", font_size=MIN_FONT, color=RESULT_COLOR)
        tag_slabs.move_to(np.array([2.4, 0.65, 0.0]))

        tag_bars = MathTex(r"\text{bars \& corner } \to 0", font_size=MIN_FONT, color=INK_FAINT)
        tag_bars.move_to(np.array([2.4, 0.0, 0.0]))

        deriv = MathTex(r"\frac{d(x^3)}{dx} = 3x^2", font_size=MIN_FONT + 8, color=RESULT_COLOR)
        deriv.move_to(np.array([2.4, -1.2, 0.0]))

        for mob in [title, eq1, tag_slabs, tag_bars, deriv]:
            mob.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.add_fixed_in_frame_mobjects(title)
        self.add(cube)
        self.wait(1.0)

        # Introduce slabs, bars, corner
        self.play(
            FadeIn(slab_x),
            FadeIn(slab_y),
            FadeIn(slab_z),
            FadeIn(bar_xy),
            FadeIn(bar_xz),
            FadeIn(bar_yz),
            FadeIn(corner),
            run_time=1.8,
        )
        self.wait(0.6)

        # Slow ambient swing during slab pull-apart, stopping before formulas
        pull_dist = 0.40
        self.begin_ambient_camera_rotation(rate=0.08)
        self.play(
            slab_x.animate.shift(pull_dist * RIGHT),
            slab_y.animate.shift(pull_dist * UP),
            slab_z.animate.shift(pull_dist * OUT),
            run_time=3.8,
        )
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)

        # Fixed in frame equations
        self.add_fixed_in_frame_mobjects(eq1, tag_slabs, tag_bars)
        self.play(
            FadeIn(eq1),
            FadeIn(tag_slabs),
            FadeIn(tag_bars),
            run_time=1.5,
        )
        self.wait(1.2)

        self.add_fixed_in_frame_mobjects(deriv)
        self.play(Write(deriv), run_time=1.4)
        self.wait(2.2)


class OneOverX(Scene):
    def construct(self):
        # Scale: u = 1.9
        u = 1.9
        x_val = 1.6
        dx_val = 0.5
        y_val = 1.0 / x_val  # 0.625
        x_new = x_val + dx_val  # 2.1
        y_new = 1.0 / x_new  # ~0.47619
        dy_val = y_val - y_new  # ~0.14881

        W = x_val * u          # 3.04
        H = y_val * u          # 1.1875
        dx_geom = dx_val * u   # 0.95
        H_new = y_new * u      # ~0.90476
        dy_geom = dy_val * u   # ~0.28274

        # Position rectangle in the left half, vertically centered
        bl = np.array([-4.10, -0.74, 0.0])
        rect_center = bl + np.array([W / 2, H / 2, 0.0])

        rect = Rectangle(
            width=W,
            height=H,
            stroke_color=V_COLOR,
            stroke_width=2.5,
            fill_color=V_COLOR,
            fill_opacity=0.35,
        ).move_to(rect_center)

        area_lbl = MathTex(r"\text{area } = 1", font_size=MIN_FONT, color=V_COLOR)
        area_lbl.move_to(rect_center)

        brace_x = Brace(rect, DOWN, buff=0.10)
        lbl_x = MathTex("x", font_size=MIN_FONT, color=INK)
        lbl_x.next_to(brace_x, DOWN, buff=0.08)

        brace_y = Brace(rect, LEFT, buff=0.10)
        lbl_y = MathTex(r"\frac{1}{x}", font_size=MIN_FONT, color=INK)
        lbl_y.next_to(brace_y, LEFT, buff=0.08)

        title = MathTex(r"f(x) = \frac{1}{x} \quad (\text{area } = 1)", font_size=MIN_FONT + 2, color=V_COLOR)
        title.to_corner(UP + LEFT, buff=0.35)

        # Frame 0: givens visible
        self.add(rect, area_lbl, brace_x, lbl_x, brace_y, lbl_y, title)
        self.wait(1.0)

        # Step 1: Widen width by dx (temporarily area > 1)
        gain_strip_initial = Rectangle(
            width=dx_geom,
            height=H,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
        ).move_to(bl + np.array([W + dx_geom / 2, H / 2, 0.0]))

        brace_dx = Brace(gain_strip_initial, UP, buff=0.08)
        lbl_dx = MathTex("dx", font_size=MIN_FONT, color=X_COLOR)
        lbl_dx.next_to(brace_dx, UP, buff=0.08)

        self.play(
            FadeIn(gain_strip_initial),
            Create(brace_dx),
            Write(lbl_dx),
            run_time=1.4,
        )
        self.wait(0.8)

        # Step 2: Lower the top so area returns to 1
        # Right gain strip has NEW height H_new (top aligned with lowered top edge)
        gain_strip_new = Rectangle(
            width=dx_geom,
            height=H_new,
            stroke_color=RESULT_COLOR,
            stroke_width=1.5,
            fill_color=RESULT_COLOR,
            fill_opacity=0.65,
        ).move_to(bl + np.array([W + dx_geom / 2, H_new / 2, 0.0]))

        rect_lowered = Rectangle(
            width=W,
            height=H_new,
            stroke_color=V_COLOR,
            stroke_width=2.5,
            fill_color=V_COLOR,
            fill_opacity=0.35,
        ).move_to(bl + np.array([W / 2, H_new / 2, 0.0]))

        # Removed top band: INK_FAINT fill with dashed outline
        loss_fill = Rectangle(
            width=W,
            height=dy_geom,
            stroke_width=0,
            fill_color=INK_FAINT,
            fill_opacity=0.30,
        ).move_to(bl + np.array([W / 2, H_new + dy_geom / 2, 0.0]))

        loss_outline = DashedVMobject(
            Rectangle(
                width=W,
                height=dy_geom,
                stroke_color=INK_FAINT,
                stroke_width=1.5,
                fill_opacity=0,
            ).move_to(bl + np.array([W / 2, H_new + dy_geom / 2, 0.0])),
            num_dashes=24,
        )
        loss_band = VGroup(loss_fill, loss_outline)

        loss_tag = MathTex(r"\text{loss (removed)}", font_size=MIN_FONT, color=INK_FAINT)
        loss_tag.next_to(loss_band, UP, buff=0.10)
        loss_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        gain_tag = MathTex(r"\text{gain}", font_size=MIN_FONT, color=RESULT_COLOR)
        gain_tag.next_to(gain_strip_new, RIGHT, buff=0.10)
        gain_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        brace_dx_new = Brace(gain_strip_new, UP, buff=0.08)
        lbl_dx_new = MathTex("dx", font_size=MIN_FONT, color=X_COLOR)
        lbl_dx_new.next_to(brace_dx_new, UP, buff=0.08)

        # Animate lowering top edge
        self.play(
            Transform(rect, rect_lowered),
            Transform(gain_strip_initial, gain_strip_new),
            Transform(brace_dx, brace_dx_new),
            Transform(lbl_dx, lbl_dx_new),
            FadeIn(loss_band),
            FadeIn(loss_tag),
            FadeIn(gain_tag),
            run_time=1.8,
        )
        self.wait(0.8)

        # Equation column on the right half, top-aligned, buff >= 0.3
        eq_gain = MathTex(
            r"\text{gain: } \frac{1}{x}\,dx",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        eq_loss = MathTex(
            r"\text{loss: } -x\,d\!\left(\frac{1}{x}\right)",
            font_size=MIN_FONT + 2,
            color=INK_FAINT,
        )
        eq_balance = MathTex(
            r"x\,d\!\left(\frac{1}{x}\right) = -\frac{1}{x}\,dx",
            font_size=MIN_FONT + 4,
            color=INK,
        )
        deriv = MathTex(
            r"\frac{d(1/x)}{dx} = -\frac{1}{x^2}",
            font_size=MIN_FONT + 8,
            color=RESULT_COLOR,
        )

        eq_col = VGroup(eq_gain, eq_loss, eq_balance, deriv).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        eq_col.move_to(np.array([2.65, 0.15, 0.0]))

        self.play(FadeIn(eq_gain), FadeIn(eq_loss), run_time=1.2)
        self.wait(0.8)
        self.play(Write(eq_balance), run_time=1.2)
        self.wait(0.8)
        self.play(Write(deriv), run_time=1.4)
        self.wait(2.2)


class SineSlope(Scene):
    def construct(self):
        R = 1.6
        C = np.array([-2.9, -0.45, 0.0])
        theta = 52.0 * np.pi / 180.0
        cos_t, sin_t = np.cos(theta), np.sin(theta)

        h_axis = Line(C + 1.85 * LEFT, C + 1.85 * RIGHT, stroke_color=GRID, stroke_width=2)
        v_axis = Line(C + 1.85 * DOWN, C + 2.0 * UP, stroke_color=GRID, stroke_width=2)
        circle = Circle(radius=R, stroke_color=V_COLOR, stroke_width=2.5).move_to(C)
        P = C + R * np.array([cos_t, sin_t, 0.0])
        P_drop = np.array([P[0], C[1], 0.0])
        radial = Line(C, P, stroke_color=INK, stroke_width=2.5)
        arc_th = Arc(radius=0.5, start_angle=0.0, angle=theta, arc_center=C, color=INK)
        th_lbl = MathTex(r"\theta", font_size=MIN_FONT, color=INK).move_to(
            C + 0.9 * np.array([np.cos(theta / 2), np.sin(theta / 2) - 0.05, 0]))
        sin_seg = Line(P_drop, P, stroke_color=RESULT_COLOR, stroke_width=3.5)
        sin_lbl = MathTex(r"\sin\theta", font_size=MIN_FONT, color=RESULT_COLOR).next_to(sin_seg, RIGHT, buff=0.1)
        cos_seg = Line(C, P_drop, stroke_color=INK_DIM, stroke_width=3.5)
        dot_P = Dot(P, color=INK, radius=0.07)

        # magnifier square on the circle, shrinks while the panel zooms
        PW, PH = 4.2, 4.0
        PC = np.array([2.75, 0.0, 0.0])
        Pp = np.array([PC[0] + 0.7, -0.45, 0.0])     # where P sits in the panel
        m = ValueTracker(3.0)

        def mag_box():
            side = 2.0 / m.get_value()
            return Square(side_length=side, stroke_color=HIGHLIGHT, stroke_width=2.5).move_to(P)
        mag = always_redraw(mag_box)

        panel_box = Rectangle(width=PW, height=PH, stroke_color=INK_FAINT, stroke_width=2).move_to(PC)

        def inside(pt):
            return abs(pt[0] - PC[0]) <= PW / 2 and abs(pt[1] - PC[1]) <= PH / 2

        def panel_pt(phi):
            mm = m.get_value()
            return Pp + mm * R * np.array([np.cos(phi) - cos_t, np.sin(phi) - sin_t, 0.0])

        def curve():
            mm = m.get_value()
            span = 6.0 / (R * mm)
            pts = [panel_pt(phi) for phi in np.linspace(theta - span, theta + span, 500)]
            pts = [q for q in pts if inside(q)]
            mob = VMobject(stroke_color=V_COLOR, stroke_width=5)
            mob.set_points_as_corners(pts if len(pts) > 1 else [Pp, Pp + 0.01 * RIGHT])
            return mob
        curve_m = always_redraw(curve)
        P_in = Dot(Pp, color=INK, radius=0.08)
        zoom_lbl = always_redraw(lambda: MathTex(
            rf"\times {m.get_value():.0f}", font_size=MIN_FONT, color=INK_DIM
        ).move_to(np.array([PC[0] + PW / 2 - 0.65, PC[1] + PH / 2 - 0.4, 0])))

        self.add(h_axis, v_axis, circle, radial, arc_th, th_lbl, sin_seg, sin_lbl, cos_seg, dot_P, mag)
        self.wait(1.5)
        self.play(FadeIn(panel_box), FadeIn(curve_m), FadeIn(P_in), FadeIn(zoom_lbl), run_time=1.0)
        self.wait(1.2)
        self.play(m.animate.set_value(40.0), run_time=4.0, rate_func=smooth)
        self.wait(1.5)

        # a nudge dtheta whose arc is 1.2 long on screen
        L_scr = 1.4
        dth = L_scr / (m.get_value() * R)
        Q = panel_pt(theta + dth)
        K = np.array([Q[0], Pp[1], 0.0])
        hyp = Line(Pp, Q, stroke_color=X_COLOR, stroke_width=5)
        vleg = Line(K, Q, stroke_color=RESULT_COLOR, stroke_width=4)
        hleg = DashedLine(Pp, K, stroke_color=INK_DIM, stroke_width=2.5)
        dth_lbl = MathTex(r"d\theta", font_size=MIN_FONT, color=X_COLOR).move_to(
            (Pp + Q) / 2 + np.array([0.45, 0.4, 0]))
        dsin_lbl = MathTex(r"d(\sin\theta)", font_size=MIN_FONT, color=RESULT_COLOR)
        dsin_lbl.next_to(vleg, LEFT, buff=0.12)
        ang = Arc(radius=0.4, start_angle=-np.pi / 2, angle=theta, arc_center=Q, color=INK)
        ang_lbl = MathTex(r"\theta", font_size=MIN_FONT, color=INK).move_to(
            Q + 0.75 * np.array([np.cos(-np.pi / 2 + theta / 2), np.sin(-np.pi / 2 + theta / 2), 0]))
        self.play(Create(hyp), FadeIn(dth_lbl), run_time=1.2)
        self.wait(0.8)
        self.play(Create(vleg), Create(hleg), FadeIn(dsin_lbl), run_time=1.2)
        self.wait(1.0)
        self.play(Create(ang), FadeIn(ang_lbl), run_time=0.8)
        self.wait(1.0)

        # similar triangles: the radius triangle has the same angle theta
        cos_lbl = MathTex(r"\cos\theta", font_size=MIN_FONT, color=INK_DIM).next_to(cos_seg, DOWN, buff=0.12)
        hyp_big = MathTex(r"1", font_size=MIN_FONT, color=INK).move_to(
            C + 0.5 * R * np.array([cos_t, sin_t, 0]) + 0.3 * np.array([-sin_t, cos_t, 0]))
        flash1 = Arc(radius=0.5, start_angle=0.0, angle=theta, arc_center=C, color=HIGHLIGHT, stroke_width=5)
        flash2 = Arc(radius=0.4, start_angle=-np.pi / 2, angle=theta, arc_center=Q, color=HIGHLIGHT, stroke_width=5)
        self.play(FadeIn(cos_lbl), FadeIn(hyp_big), run_time=0.8)
        self.play(Create(flash1), Create(flash2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(flash1), FadeOut(flash2), run_time=0.4)

        ratio = MathTex(r"\frac{d(\sin\theta)}{d\theta} = \frac{\cos\theta}{1}", font_size=MIN_FONT, color=INK)
        ratio.set_color_by_tex(r"d(\sin\theta)", RESULT_COLOR)
        ratio.set_color_by_tex(r"d\theta", X_COLOR)
        grp = VGroup(panel_box, curve_m, P_in, zoom_lbl, hyp, vleg, hleg, dth_lbl, dsin_lbl, ang, ang_lbl)
        self.play(FadeOut(grp), run_time=0.7)
        final = MathTex(r"\frac{d(\sin\theta)}{d\theta} = \cos\theta", font_size=MIN_FONT + 8, color=RESULT_COLOR)
        final.move_to(np.array([2.6, 0.3, 0.0]))
        self.play(Write(final), run_time=1.2)
        self.wait(2.5)
