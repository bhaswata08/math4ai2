# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


def f_func(x, y):
    """Smooth asymmetric hill with peak at (0.5, -0.3) of height 2.0."""
    return 2.0 * np.exp(-((x - 0.5) ** 2 + 2.0 * (y + 0.3) ** 2) / 2.5)


def grad_func(x, y):
    """Analytical gradient of f_func."""
    val = f_func(x, y)
    df_dx = val * (-2.0 * (x - 0.5) / 2.5)
    df_dy = val * (-4.0 * (y + 0.3) / 2.5)
    return np.array([df_dx, df_dy])


# =============================================================================
# SCENE 1: GradientOnSurface (3D)
# =============================================================================
class GradientOnSurface(ThreeDScene):
    def construct(self):
        # 1. Camera orientation
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-55 * DEGREES,
        )

        # Scale axes so surface height is ~70% of frame height (height ~3.95 scene units)
        scale = 0.92
        axes = ThreeDAxes(
            x_range=[-1.4, 2.0, 1.0],
            y_range=[-1.8, 1.5, 1.0],
            z_range=[0.0, 2.5, 1.0],
            x_length=3.4 * scale,
            y_length=3.3 * scale,
            z_length=2.5 * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 1.5,
                "include_ticks": False,
                "include_tip": False,
            },
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.z_axis.set_color(INK_DIM)

        # Shift axes in 3D to center the surface in the right ~55% of the frame (screen x ≈ +1.65, y ≈ -0.5)
        # keeping it 0.25 units clear of every edge during the whole orbit
        R0 = self.camera.get_rotation_matrix()
        v_shift = np.dot(np.array([2.7, -0.9, 0.0]), R0)
        axes.shift(v_shift)

        # Orientation-fixed axis labels
        label_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        label_x.move_to(axes.c2p(2.15, 0, 0))
        label_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        label_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        label_y.move_to(axes.c2p(0, 1.65, 0))
        label_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        label_f = MathTex("f", font_size=MIN_FONT, color=INK_DIM)
        label_f.move_to(axes.c2p(0, 0, 2.65))
        label_f.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Checkerboard surface z = f(x, y)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f_func(u, v)),
            u_range=[-1.3, 2.0],
            v_range=[-1.6, 1.2],
            resolution=(16, 16),
            stroke_color=V_COLOR,
            stroke_width=0.4,
            stroke_opacity=0.3,
        )
        for face in surface.submobjects:
            opac = 0.35 if (face.u_index + face.v_index) % 2 == 0 else 0.65
            face.set_fill(color=V_COLOR, opacity=opac)

        # Evaluation point p = (-0.5, -0.8) where gx ≈ 0.88, gy ≈ 0.88, |grad f| ≈ 1.24
        # On-screen gradient arrow length is ~1.49 scene units (>= 1.2 required)
        x0, y0 = -0.5, -0.8
        z0 = f_func(x0, y0)
        gx, gy = grad_func(x0, y0)

        p_floor = axes.c2p(x0, y0, 0.0)
        p_surf = axes.c2p(x0, y0, z0)

        dot_floor = Dot3D(point=p_floor, radius=0.09, color=RESULT_COLOR)
        dot_surf = Dot3D(point=p_surf, radius=0.10, color=RESULT_COLOR)
        vert_dash = DashedLine(p_floor, p_surf, color=INK_FAINT, stroke_width=2.5)

        # Component endpoints on floor
        p_x_end = axes.c2p(x0 + gx, y0, 0.0)
        p_xy_end = axes.c2p(x0 + gx, y0 + gy, 0.0)

        # Tip-to-tail arrows: x and y components with stroke >= 5 and 3D cones
        arrow_x = Arrow3D(
            p_floor, p_x_end,
            color=X_COLOR,
            thickness=0.065,
            height=0.38,
            base_radius=0.15,
        )
        arrow_x.set_stroke(width=5.5)

        arrow_y = Arrow3D(
            p_x_end, p_xy_end,
            color=Y_COLOR,
            thickness=0.065,
            height=0.38,
            base_radius=0.15,
        )
        arrow_y.set_stroke(width=5.5)

        arrow_grad = Arrow3D(
            p_floor, p_xy_end,
            color=RESULT_COLOR,
            thickness=0.075,
            height=0.42,
            base_radius=0.17,
        )
        arrow_grad.set_stroke(width=6.0)

        # Surface uphill arrow in gradient direction
        s_surf = 0.55
        p_surf_end = axes.c2p(
            x0 + s_surf * gx,
            y0 + s_surf * gy,
            z0 + s_surf * (gx ** 2 + gy ** 2),
        )
        arrow_surf = Arrow3D(
            p_surf, p_surf_end,
            color=RESULT_COLOR,
            thickness=0.075,
            height=0.42,
            base_radius=0.17,
        )
        arrow_surf.set_stroke(width=6.0)
        dash_tip = DashedLine(p_xy_end, axes.c2p(x0 + gx, y0 + gy, f_func(x0 + gx, y0 + gy)), color=INK_FAINT, stroke_width=2.5)

        # Left-column cards in fixed frame coordinates
        c1_a = MathTex(r"f(x,y):\ \text{one hill}", font_size=MIN_FONT, color=V_COLOR)
        c1_b = MathTex(r"\text{at } p = (-0.5, -0.8)", font_size=MIN_FONT, color=INK_DIM)
        c1 = VGroup(c1_a, c1_b).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        c1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c2 = MathTex(
            r"\nabla f = \begin{bmatrix}",
            r"\partial f/\partial x",
            r"\\",
            r"\partial f/\partial y",
            r"\end{bmatrix}",
            font_size=MIN_FONT,
        )
        c2[1].set_color(X_COLOR)
        c2[3].set_color(Y_COLOR)
        c2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c3 = MathTex(r"\nabla f \text{ points uphill}", font_size=MIN_FONT, color=RESULT_COLOR)
        c3.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        cards = VGroup(c1, c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cards.to_corner(UL, buff=0.35)

        self.camera.add_fixed_in_frame_mobjects(c2, c3)

        # 2. First frame: givens present immediately
        self.add(axes, surface, dot_floor, dot_surf, vert_dash)
        self.add_fixed_orientation_mobjects(label_x, label_y, label_f)
        self.add_fixed_in_frame_mobjects(c1)
        self.wait(1.5)

        # 3. Show partial x component in X_COLOR
        self.play(Create(arrow_x), FadeIn(c2), run_time=1.4)
        self.wait(0.6)

        # 4. Show partial y component in Y_COLOR (tip to tail)
        self.play(Create(arrow_y), run_time=1.4)
        self.wait(0.6)

        # 5. Gradient vector in RESULT_COLOR
        self.play(Create(arrow_grad), run_time=1.4)
        self.wait(0.6)

        # 6. Uphill direction on the surface in RESULT_COLOR
        self.play(Create(arrow_surf), Create(dash_tip), FadeIn(c3), run_time=1.5)
        self.wait(0.8)

        # 7. Slow camera orbit
        self.begin_ambient_camera_rotation(rate=0.035)
        self.wait(8.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)


# =============================================================================
# SCENE 2: GradientField (2D)
# =============================================================================
class GradientField(Scene):
    def construct(self):
        # Left ~55% of frame width (5.425 units), ~83% of frame height (4.65 units)
        scale = 1.55
        x_min, x_max = -1.25, 2.25
        y_min, y_max = -1.8, 1.2

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([-1.95, 0.0, 0.0]))
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)

        lbl_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        lbl_x.next_to(axes.x_axis.get_end(), DL, buff=0.10)
        lbl_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        lbl_y.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Elliptical contour lines and bands
        peak_pos = axes.c2p(0.5, -0.3)
        levels = [0.65, 0.90, 1.15, 1.40, 1.65, 1.85]
        opacities = [0.06, 0.11, 0.16, 0.22, 0.28, 0.35]

        contour_mobs = []
        for lvl, opac in zip(levels, opacities):
            a = np.sqrt(2.5 * np.log(2.0 / lvl))
            b = a / np.sqrt(2.0)
            ell = Ellipse(
                width=2.0 * a * scale,
                height=2.0 * b * scale,
                stroke_color=INK_DIM,
                stroke_width=1.5,
                fill_color=V_COLOR,
                fill_opacity=opac,
            ).move_to(peak_pos)
            contour_mobs.append(ell)

        contours_group = VGroup(*contour_mobs)
        peak_dot = Dot(peak_pos, radius=0.07, color=V_COLOR)

        # Prominent grid of gradient arrows: stroke_width >= 4 and visible tips
        x_grid = [-0.9, -0.4, 0.1, 0.6, 1.1, 1.6, 2.0]
        y_grid = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0]

        grid_arrows = []
        for xg in x_grid:
            for yg in y_grid:
                g = grad_func(xg, yg)
                m = np.linalg.norm(g)
                if m > 0.10:
                    u = g / m
                    length = min(0.60, 0.32 * m)
                    start_pt = axes.c2p(xg, yg)
                    end_pt = start_pt + length * np.array([u[0], u[1], 0.0])
                    arr = Arrow(
                        start_pt, end_pt,
                        buff=0,
                        stroke_width=4.2,
                        max_tip_length_to_length_ratio=0.35,
                        color=RESULT_COLOR,
                    )
                    grid_arrows.append(arr)

        arrows_group = VGroup(*grid_arrows)

        # Exactly two text lines in the right column, centered at x = 3.10
        right_x = 3.10
        c_steep = MathTex(r"|\nabla f| = \text{steepness}", font_size=MIN_FONT, color=RESULT_COLOR)
        c_steep.move_to(np.array([right_x, 0.70, 0.0]))
        c_steep.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c_perp = MathTex(r"\nabla f \perp \text{contour}", font_size=MIN_FONT, color=RESULT_COLOR)
        c_perp.move_to(np.array([right_x, -0.70, 0.0]))
        c_perp.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Highlight 1: dense contours region
        pt1 = np.array([0.5, 0.5])
        pos1 = axes.c2p(*pt1)
        ring1 = Circle(radius=0.35, color=HIGHLIGHT, stroke_width=3.5).move_to(pos1)

        # Highlight 2: perpendicular to contour
        a3 = np.sqrt(2.5 * np.log(2.0 / 1.15))
        b3 = a3 / np.sqrt(2.0)
        phi3 = 135.0 * DEGREES
        pt3 = np.array([0.5 + a3 * np.cos(phi3), -0.3 + b3 * np.sin(phi3)])
        pos3 = axes.c2p(*pt3)
        dot3 = Dot(pos3, radius=0.08, color=RESULT_COLOR)
        ring3 = Circle(radius=0.35, color=HIGHLIGHT, stroke_width=3.5).move_to(pos3)

        g3 = grad_func(*pt3)
        u3 = g3 / np.linalg.norm(g3)
        arr3 = Arrow(
            pos3,
            pos3 + 0.75 * np.array([u3[0], u3[1], 0.0]),
            buff=0,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.30,
            color=RESULT_COLOR,
        )

        tan_dir = np.array([-u3[1], u3[0], 0.0])
        tan_line = Line(pos3 - 0.70 * tan_dir, pos3 + 0.70 * tan_dir, color=INK_DIM, stroke_width=3.0)

        sz = 0.18
        elbow = VGroup(
            Line(pos3 + sz * tan_dir, pos3 + sz * tan_dir + sz * np.array([u3[0], u3[1], 0.0]), color=HIGHLIGHT, stroke_width=2.5),
            Line(pos3 + sz * tan_dir + sz * np.array([u3[0], u3[1], 0.0]), pos3 + sz * np.array([u3[0], u3[1], 0.0]), color=HIGHLIGHT, stroke_width=2.5),
        )

        # 1. First frame: contour map present immediately
        self.add(axes, lbl_x, lbl_y, contours_group, peak_dot)
        self.wait(1.5)

        # 2. Grid of gradient arrows appears
        self.play(FadeIn(arrows_group, lag_ratio=0.02), run_time=1.8)
        self.wait(1.0)

        # 3. Highlight steepness -> Line 1
        self.play(FadeIn(ring1), FadeIn(c_steep), run_time=1.2)
        self.play(FadeOut(ring1), run_time=0.6)
        self.wait(1.2)

        # 4. Highlight perpendicular to contour -> Line 2
        self.play(FadeIn(ring3), FadeIn(dot3), Create(arr3), Create(tan_line), Create(elbow), FadeIn(c_perp), run_time=1.4)
        self.play(FadeOut(ring3), run_time=0.6)
        self.wait(3.5)


# =============================================================================
# SCENE 3: DirectionalDerivative (2D)
# =============================================================================
class DirectionalDerivative(Scene):
    def construct(self):
        # Left ~55% of frame width (5.425 units), ~83% of frame height (4.65 units)
        scale = 1.25
        x_min, x_max = -1.25, 2.25
        y_min, y_max = -1.8, 1.2

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([-2.45, 0.0, 0.0]))
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)

        lbl_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        lbl_x.next_to(axes.x_axis.get_end(), DL, buff=0.10)
        lbl_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        lbl_y.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Contour lines
        peak_pos = axes.c2p(0.5, -0.3)
        levels = [0.65, 0.90, 1.15, 1.40, 1.65, 1.85]
        opacities = [0.06, 0.11, 0.16, 0.22, 0.28, 0.35]

        contour_mobs = []
        for lvl, opac in zip(levels, opacities):
            a = np.sqrt(2.5 * np.log(2.0 / lvl))
            b = a / np.sqrt(2.0)
            ell = Ellipse(
                width=2.0 * a * scale,
                height=2.0 * b * scale,
                stroke_color=INK_DIM,
                stroke_width=1.5,
                fill_color=V_COLOR,
                fill_opacity=opac,
            ).move_to(peak_pos)
            contour_mobs.append(ell)

        contours_group = VGroup(*contour_mobs)
        peak_dot = Dot(peak_pos, radius=0.07, color=V_COLOR)

        # Evaluation point p = (-0.5, -0.8) where |grad f| = 1.24
        p_pt = np.array([-0.5, -0.8])
        p_center = axes.c2p(*p_pt)
        p_dot = Dot(p_center, radius=0.08, color=RESULT_COLOR)

        g_vec = grad_func(*p_pt)
        g_mag = np.linalg.norm(g_vec)
        alpha = np.arctan2(g_vec[1], g_vec[0])

        # Fixed gradient arrow
        grad_end = p_center + (g_mag * 0.90) * np.array([np.cos(alpha), np.sin(alpha), 0.0])
        grad_arrow = Arrow(
            p_center, grad_end,
            buff=0,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        grad_lbl = MathTex(r"\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        grad_lbl.next_to(grad_end, UR, buff=0.18)
        grad_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Rotating unit vector u (ValueTracker for angle theta)
        u_tracker = ValueTracker(0.0)

        def get_u_arrow():
            th = u_tracker.get_value()
            phi = alpha + th
            end = p_center + 1.0 * np.array([np.cos(phi), np.sin(phi), 0.0])
            return Arrow(
                p_center, end,
                buff=0,
                stroke_width=4.5,
                max_tip_length_to_length_ratio=0.28,
                color=W_COLOR,
            )

        u_arrow = always_redraw(get_u_arrow)

        def get_u_lbl():
            th = u_tracker.get_value()
            phi = alpha + th
            end = p_center + 1.0 * np.array([np.cos(phi), np.sin(phi), 0.0])
            # on the clockwise side of the shaft, clear of the grad label
            d = np.array([np.cos(phi), np.sin(phi), 0.0])
            perp_cw = np.array([np.sin(phi), -np.cos(phi), 0.0])
            lbl = MathTex(r"\mathbf{u}", font_size=MIN_FONT, color=W_COLOR)
            lbl.move_to(p_center + 0.70 * d + 0.45 * perp_cw)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            return lbl

        u_lbl = always_redraw(get_u_lbl)

        # Right-side elements centered at x = 3.05 (pulled inward, clearing all edges and map)
        right_x = 2.6

        # Live readout at the top
        readout_lbl = MathTex(r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} =", font_size=MIN_FONT, color=INK)
        readout_num = DecimalNumber(
            g_mag,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
            include_sign=True,
        )
        readout_num.add_updater(lambda d: d.set_value(g_mag * np.cos(u_tracker.get_value())))

        readout_box = VGroup(readout_lbl, readout_num).arrange(DOWN, buff=0.10)
        readout_box.move_to(np.array([right_x, 1.95, 0.0]))
        readout_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Mini plot of D_u f vs theta (compact width 2.1, completely clear of edge and contour map)
        plot_axes = Axes(
            x_range=[0, 2 * np.pi + 0.1, np.pi],
            y_range=[-1.5, 1.5, 1.2],
            x_length=2.1,
            y_length=1.45,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 1.5,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([right_x + 0.4, 0.05, 0.0]))

        plot_lbl_x = MathTex(r"\theta", font_size=MIN_FONT, color=INK_DIM)
        plot_lbl_x.next_to(plot_axes.x_axis.get_end(), UR, buff=0.12)
        plot_lbl_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_t0 = MathTex("0", font_size=MIN_FONT, color=INK_DIM)
        lbl_t0.next_to(plot_axes.c2p(0, 0), DOWN, buff=0.08)
        lbl_t0.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_tpi = MathTex(r"\pi", font_size=MIN_FONT, color=INK_DIM)
        lbl_tpi.next_to(plot_axes.c2p(np.pi, 0), DOWN, buff=0.08)
        lbl_tpi.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_t2pi = MathTex(r"2\pi", font_size=MIN_FONT, color=INK_DIM)
        lbl_t2pi.next_to(plot_axes.c2p(2 * np.pi, 0), DOWN, buff=0.08)
        lbl_t2pi.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        plot_ticks = VGroup(lbl_t0, lbl_tpi, lbl_t2pi)

        # Upper and lower guide dashed lines showing max and min values (+|grad f|, -|grad f|)
        dash_max = DashedLine(plot_axes.c2p(0, g_mag), plot_axes.c2p(2 * np.pi, g_mag), color=INK_FAINT, stroke_width=1.5)
        dash_min = DashedLine(plot_axes.c2p(0, -g_mag), plot_axes.c2p(2 * np.pi, -g_mag), color=INK_FAINT, stroke_width=1.5)

        lbl_max = MathTex(r"+|\nabla f|", font_size=MIN_FONT - 4, color=INK_DIM)
        lbl_max.next_to(dash_max.get_start(), LEFT, buff=0.08)
        lbl_max.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_min = MathTex(r"-|\nabla f|", font_size=MIN_FONT - 4, color=INK_DIM)
        lbl_min.next_to(dash_min.get_start(), LEFT, buff=0.08)
        lbl_min.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Dynamic cosine curve building up as u rotates
        def get_cos_curve():
            th_curr = u_tracker.get_value()
            if th_curr < 0.05:
                th_curr = 0.05
            return plot_axes.plot(
                lambda t: g_mag * np.cos(t),
                x_range=[0, th_curr],
                color=RESULT_COLOR,
                stroke_width=3.2,
            )

        cos_curve = always_redraw(get_cos_curve)

        dot_curve = always_redraw(
            lambda: Dot(
                plot_axes.c2p(u_tracker.get_value(), g_mag * np.cos(u_tracker.get_value())),
                radius=0.07,
                color=W_COLOR,
            )
        )

        # Final formula at the bottom, punchy and clear
        summary_card = MathTex(
            r"D_{\mathbf{u}} f = |\nabla f|\cos\theta",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        summary_card.move_to(np.array([right_x, -1.65, 0.0]))
        summary_card.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 1. First frame: givens present
        self.add(
            axes, lbl_x, lbl_y, contours_group, peak_dot, p_dot,
            grad_arrow, grad_lbl, u_arrow, u_lbl,
            readout_lbl, readout_num,
            plot_axes, plot_lbl_x, plot_ticks, dash_max, dash_min, lbl_max, lbl_min,
            cos_curve, dot_curve,
        )
        self.wait(1.5)

        # 2. Rotate u a full turn (0 to 2*pi)
        self.play(
            u_tracker.animate.set_value(2 * np.pi),
            run_time=12.0,
            rate_func=linear,
        )
        self.wait(0.8)

        # 3. Reveal final MathTex formula
        self.play(FadeIn(summary_card), run_time=1.2)
        self.wait(2.5)


# =============================================================================
# SCENE 4: SteepestAscent (2D)
# =============================================================================
class SteepestAscent(Scene):
    def construct(self):
        # Left ~55% of frame width (5.425 units), ~83% of frame height (4.65 units)
        scale = 1.25
        x_min, x_max = -1.25, 2.25
        y_min, y_max = -1.8, 1.2

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([-2.45, 0.0, 0.0]))
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)

        lbl_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        lbl_x.next_to(axes.x_axis.get_end(), DL, buff=0.10)
        lbl_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        lbl_y.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Elliptical contour lines
        peak_pos = axes.c2p(0.5, -0.3)
        levels = [0.65, 0.90, 1.15, 1.40, 1.65, 1.85]
        opacities = [0.06, 0.11, 0.16, 0.22, 0.28, 0.35]

        contour_mobs = []
        for lvl, opac in zip(levels, opacities):
            a = np.sqrt(2.5 * np.log(2.0 / lvl))
            b = a / np.sqrt(2.0)
            ell = Ellipse(
                width=2.0 * a * scale,
                height=2.0 * b * scale,
                stroke_color=INK_DIM,
                stroke_width=1.5,
                fill_color=V_COLOR,
                fill_opacity=opac,
            ).move_to(peak_pos)
            contour_mobs.append(ell)

        contours_group = VGroup(*contour_mobs)
        peak_dot = Dot(peak_pos, radius=0.07, color=V_COLOR)
        peak_lbl = MathTex(r"\text{peak}", font_size=MIN_FONT, color=V_COLOR)
        peak_lbl.next_to(peak_pos, UP, buff=0.22)
        peak_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Exactly two lines in the right column, centered at x = 3.10 (clear of all edges)
        right_x = 2.6
        c_ascent = MathTex(r"\text{ascent: follow } +\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        c_ascent.move_to(np.array([right_x, 0.70, 0.0]))
        c_ascent.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c_descent = MathTex(r"\text{descent: follow } -\nabla f", font_size=MIN_FONT, color=W_COLOR)
        c_descent.move_to(np.array([right_x, -0.70, 0.0]))
        c_descent.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # -------------------------------------------------------------
        # Part 1: Steepest Ascent to peak
        # -------------------------------------------------------------
        p_start = np.array([-1.0, -1.2])
        dot_start = Dot(axes.c2p(*p_start), radius=0.08, color=RESULT_COLOR)
        lbl_start = MathTex(r"\mathbf{x}_0", font_size=MIN_FONT, color=RESULT_COLOR)
        lbl_start.next_to(axes.c2p(*p_start), DR, buff=0.10)
        lbl_start.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Calculate ascent trajectory
        ascent_pts = [p_start]
        lr = 0.40
        curr = p_start.copy()
        for _ in range(6):
            g = grad_func(curr[0], curr[1])
            curr = curr + lr * g
            ascent_pts.append(curr.copy())

        ascent_arrows = []
        for i in range(len(ascent_pts) - 1):
            p1 = axes.c2p(*ascent_pts[i])
            p2 = axes.c2p(*ascent_pts[i + 1])
            arr = Arrow(
                p1, p2,
                buff=0,
                stroke_width=4.5,
                max_tip_length_to_length_ratio=0.30,
                color=RESULT_COLOR,
            )
            ascent_arrows.append(arr)

        flash_peak = Dot(peak_pos, radius=0.18, color=HIGHLIGHT)

        # -------------------------------------------------------------
        # Part 2: Contrast with Steepest Descent
        # -------------------------------------------------------------
        q_start = np.array([1.1, -0.6])
        dot_q = Dot(axes.c2p(*q_start), radius=0.08, color=W_COLOR)
        lbl_q = MathTex(r"\mathbf{w}_0", font_size=MIN_FONT, color=W_COLOR)
        lbl_q.next_to(axes.c2p(*q_start), UR, buff=0.10)
        lbl_q.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        descent_pts = [q_start]
        curr_d = q_start.copy()
        for _ in range(3):
            g = grad_func(curr_d[0], curr_d[1])
            curr_d = curr_d - 0.32 * g
            descent_pts.append(curr_d.copy())

        descent_arrows = []
        for i in range(len(descent_pts) - 1):
            q1 = axes.c2p(*descent_pts[i])
            q2 = axes.c2p(*descent_pts[i + 1])
            arr = Arrow(
                q1, q2,
                buff=0,
                stroke_width=4.5,
                max_tip_length_to_length_ratio=0.30,
                color=W_COLOR,
            )
            descent_arrows.append(arr)

        # 1. First frame: givens present
        self.add(
            axes, lbl_x, lbl_y, contours_group, peak_dot, peak_lbl,
            dot_start, lbl_start, c_ascent,
        )
        self.wait(1.5)

        # 2. Draw steepest ascent steps one by one
        for arr in ascent_arrows:
            self.play(GrowArrow(arr), run_time=0.45)
        self.wait(0.5)

        # Flash peak
        self.play(FadeIn(flash_peak, run_time=0.25))
        self.play(FadeOut(flash_peak, run_time=0.25))
        self.wait(0.8)

        # 3. Contrast with steepest descent
        self.play(FadeIn(dot_q), Write(lbl_q), FadeIn(c_descent), run_time=1.0)
        self.wait(0.4)

        for arr in descent_arrows:
            self.play(GrowArrow(arr), run_time=0.45)
        self.wait(4.0)
