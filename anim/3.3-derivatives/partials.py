# Original work for Mathematics for AI (notation inspired by 3b1b/videos _2017/gradient.py, CC BY-NC-SA 4.0)

from shared.anim.house import *


def get_base_surface_and_axes():
    """Builds the 3D axes, axis labels, and checkerboard surface z = f(x, y) = x^2 y - y^2/2."""
    axes = ThreeDAxes(
        x_range=[-0.5, 2.0, 1.0],
        y_range=[-0.4, 1.6, 1.0],
        z_range=[-0.8, 2.5, 1.0],
        x_length=2.8,
        y_length=2.3,
        z_length=2.5,
        axis_config={
            "stroke_color": INK_DIM,
            "stroke_width": 1.5,
            "include_ticks": False,
            "include_tip": False,
        },
    )
    # Shift axes in 3D to ensure the surface stays strictly clear of the formula cards
    v_shift = np.array([0.85 * np.cos(-55 * DEGREES), -0.85 * np.sin(-55 * DEGREES), 0.0])
    axes.shift(v_shift)
    axes.x_axis.set_color(X_COLOR)
    axes.y_axis.set_color(Y_COLOR)
    axes.z_axis.set_color(INK_DIM)

    # Orientation-fixed axis labels near positive tips
    label_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
    label_x.move_to(axes.c2p(2.2, 0, 0))

    label_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
    label_y.move_to(axes.c2p(0, 1.8, 0))

    label_f = MathTex("f", font_size=MIN_FONT, color=INK_DIM)
    label_f.move_to(axes.c2p(0, 0, 2.7))

    def f(x, y):
        return (x ** 2) * y - 0.5 * (y ** 2)

    # Surface z = f(x, y) over domain x in [-1.15, 1.45], y in [-0.6, 1.35]
    surface = Surface(
        lambda u, v: axes.c2p(u, v, f(u, v)),
        u_range=[-1.15, 1.45],
        v_range=[-0.6, 1.35],
        resolution=(16, 16),
        stroke_color=V_COLOR,
        stroke_width=0.4,
        stroke_opacity=0.3,
    )
    for face in surface.submobjects:
        opac = 0.35 if (face.u_index + face.v_index) % 2 == 0 else 0.65
        face.set_fill(color=V_COLOR, opacity=opac)

    return axes, surface, f, (label_x, label_y, label_f)


class PartialX(ThreeDScene):
    def construct(self):
        # 1. Camera orientation and placement
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-55 * DEGREES,
            frame_center=LEFT * 1.2 + DOWN * 0.1,
        )

        axes, surface, f, (label_x, label_y, label_f) = get_base_surface_and_axes()
        x0, y0 = 1.0, 0.5
        z0 = f(x0, y0)

        # Base point dot
        dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.08, color=RESULT_COLOR)

        # Slicing plane y = y0 in X_COLOR tint
        plane_corners = [
            axes.c2p(-1.15, y0, -0.4),
            axes.c2p(1.45, y0, -0.4),
            axes.c2p(1.45, y0, 1.1),
            axes.c2p(-1.15, y0, 1.1),
        ]
        slice_plane = Polygon(
            *plane_corners,
            fill_color=X_COLOR,
            fill_opacity=0.25,
            stroke_color=X_COLOR,
            stroke_width=1.5,
            stroke_opacity=0.7,
        )

        # Intersection curve z = f(x, y0) along plane
        curve_x = axes.plot_parametric_curve(
            lambda t: np.array([t, y0, f(t, y0)]),
            t_range=[-1.15, 1.45],
            color=X_COLOR,
            stroke_width=6,
        )

        # Tangent line along x at (x0, y0, z0): df/dx = 2xy = 1.0
        df_dx = 2 * x0 * y0
        L = 0.55
        tangent_x = Line(
            axes.c2p(x0 - L, y0, z0 - L * df_dx),
            axes.c2p(x0 + L, y0, z0 + L * df_dx),
            color=RESULT_COLOR,
            stroke_width=5,
        )

        # Momentary highlight flash
        flash_dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.16, color=HIGHLIGHT)

        # --- Fixed-in-frame Cards ---
        # Card 1: Function and evaluation point
        c1_a = MathTex(r"f(x, y) = x^2 y - y^2/2", font_size=MIN_FONT, color=V_COLOR)
        c1_b = MathTex(r"\text{at } (1, 0.5)", font_size=MIN_FONT, color=INK_DIM)
        c1 = VGroup(c1_a, c1_b).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        c1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Card 2: Conceptual definition of partial derivative w.r.t x
        c2_a = MathTex(r"\frac{\partial f}{\partial x} = \text{slope along } x", font_size=MIN_FONT, color=X_COLOR)
        c2_b = MathTex(r"\text{with } y \text{ held fixed}", font_size=MIN_FONT, color=INK_DIM)
        c2 = VGroup(c2_a, c2_b).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        c2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Card 3: Formula and computed value
        c3 = MathTex(r"\frac{\partial f}{\partial x}", r"=", r"2xy", r"=", r"1", font_size=MIN_FONT)
        c3[0].set_color(X_COLOR)
        c3[1:4].set_color(INK)
        c3[4].set_color(RESULT_COLOR)
        c3.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Pre-arrange cards in UL corner
        all_cards = VGroup(c1, c2, c3).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        all_cards.to_corner(UL, buff=0.28)

        # Register animated cards as fixed in frame before animating
        self.camera.add_fixed_in_frame_mobjects(c2, c3)

        # 2. First frame: givens present immediately (never open on empty frame)
        self.add(axes, surface, dot)
        self.add_fixed_orientation_mobjects(label_x, label_y, label_f)
        self.add_fixed_in_frame_mobjects(c1)
        self.wait(1.5)

        # 3. Show slicing plane y = y0
        self.play(FadeIn(slice_plane), run_time=1.2)
        self.wait(0.5)

        # 4. Intersection curve drawn bold in X_COLOR + concept label
        self.play(Create(curve_x), FadeIn(c2), run_time=1.8)
        self.wait(0.5)

        # 5. Tangent line at the point in RESULT_COLOR + momentary flash
        self.play(Create(tangent_x), run_time=1.2)
        self.play(FadeIn(flash_dot, run_time=0.25))
        self.play(FadeOut(flash_dot, run_time=0.25))

        # 6. Computed formula and value
        self.play(FadeIn(c3), run_time=1.2)
        self.wait(0.5)

        # 7. Slow camera orbit to reveal 3D curvature and slicing geometry
        self.begin_ambient_camera_rotation(rate=0.04)
        self.wait(10.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)


class PartialY(ThreeDScene):
    def construct(self):
        # 1. Camera orientation and placement
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-55 * DEGREES,
            frame_center=LEFT * 1.2 + DOWN * 0.1,
        )

        axes, surface, f, (label_x, label_y, label_f) = get_base_surface_and_axes()
        x0, y0 = 1.0, 0.5
        z0 = f(x0, y0)

        # Base point dot
        dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.08, color=RESULT_COLOR)

        # Slicing plane x = x0 in Y_COLOR tint
        plane_corners = [
            axes.c2p(x0, -0.6, -0.85),
            axes.c2p(x0, 1.35, -0.85),
            axes.c2p(x0, 1.35, 0.7),
            axes.c2p(x0, -0.6, 0.7),
        ]
        slice_plane = Polygon(
            *plane_corners,
            fill_color=Y_COLOR,
            fill_opacity=0.25,
            stroke_color=Y_COLOR,
            stroke_width=1.5,
            stroke_opacity=0.7,
        )

        # Intersection curve z = f(x0, y) along plane
        curve_y = axes.plot_parametric_curve(
            lambda t: np.array([x0, t, f(x0, t)]),
            t_range=[-0.6, 1.35],
            color=Y_COLOR,
            stroke_width=6,
        )

        # Tangent line along y at (x0, y0, z0): df/dy = x^2 - y = 0.5
        df_dy = (x0 ** 2) - y0
        L = 0.55
        tangent_y = Line(
            axes.c2p(x0, y0 - L, z0 - L * df_dy),
            axes.c2p(x0, y0 + L, z0 + L * df_dy),
            color=RESULT_COLOR,
            stroke_width=5,
        )

        # Tangent line along x (to show together at the end)
        df_dx = 2 * x0 * y0
        tangent_x = Line(
            axes.c2p(x0 - L, y0, z0 - L * df_dx),
            axes.c2p(x0 + L, y0, z0 + L * df_dx),
            color=RESULT_COLOR,
            stroke_width=5,
        )

        # Momentary highlight flash
        flash_dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.16, color=HIGHLIGHT)

        # --- Fixed-in-frame Cards ---
        # Card 1: Function and evaluation point
        c1_a = MathTex(r"f(x, y) = x^2 y - y^2/2", font_size=MIN_FONT, color=V_COLOR)
        c1_b = MathTex(r"\text{at } (1, 0.5)", font_size=MIN_FONT, color=INK_DIM)
        c1 = VGroup(c1_a, c1_b).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        c1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Card 2: Conceptual definition of partial derivative w.r.t y
        c2_a = MathTex(r"\frac{\partial f}{\partial y} = \text{slope along } y", font_size=MIN_FONT, color=Y_COLOR)
        c2_b = MathTex(r"\text{with } x \text{ held fixed}", font_size=MIN_FONT, color=INK_DIM)
        c2 = VGroup(c2_a, c2_b).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        c2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Card 3: Formula and computed value
        c3 = MathTex(r"\frac{\partial f}{\partial y}", r"=", r"x^2 - y", r"=", r"0.5", font_size=MIN_FONT)
        c3[0].set_color(Y_COLOR)
        c3[1:4].set_color(INK)
        c3[4].set_color(RESULT_COLOR)
        c3.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Card 4: Faint teaser for gradient in next block
        teaser = MathTex(
            r"\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)",
            font_size=MIN_FONT,
            color=INK_DIM,
        )
        teaser.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Pre-arrange cards in UL corner with compact spacing
        all_cards = VGroup(c1, c2, c3, teaser).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        all_cards.to_corner(UL, buff=0.28)

        # Register animated cards as fixed in frame before animating
        self.camera.add_fixed_in_frame_mobjects(c2, c3, teaser)

        # 2. First frame: givens present immediately (never open on empty frame)
        self.add(axes, surface, dot)
        self.add_fixed_orientation_mobjects(label_x, label_y, label_f)
        self.add_fixed_in_frame_mobjects(c1)
        self.wait(1.5)

        # 3. Show slicing plane x = x0
        self.play(FadeIn(slice_plane), run_time=1.2)
        self.wait(0.5)

        # 4. Intersection curve drawn in Y_COLOR + concept label
        self.play(Create(curve_y), FadeIn(c2), run_time=1.8)
        self.wait(0.5)

        # 5. Tangent line at the point in RESULT_COLOR + momentary flash
        self.play(Create(tangent_y), run_time=1.2)
        self.play(FadeIn(flash_dot, run_time=0.25))
        self.play(FadeOut(flash_dot, run_time=0.25))

        # 6. Computed formula and value
        self.play(FadeIn(c3), run_time=1.2)
        self.wait(0.5)

        # 7. Show both tangent lines together at point + teaser for gradient
        self.play(FadeIn(tangent_x), FadeIn(teaser), run_time=1.4)
        self.wait(0.5)

        # 8. Slow camera orbit showing both tangent vectors spanning the tangent plane
        self.begin_ambient_camera_rotation(rate=0.04)
        self.wait(10.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)
