# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


# =============================================================================
# SCENE 1: TangentPlaneAndBowl (ThreeDScene)
# =============================================================================
class TangentPlaneAndBowl(ThreeDScene):
    def construct(self):
        # 1. Camera orientation and placement
        # Frame center shifted to position surface on the right, leaving UL clear for formula
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-38 * DEGREES,
            frame_center=LEFT * 0.7 + UP * 0.9,
        )

        # 2. 3D Axes
        axes = ThreeDAxes(
            x_range=[-1.8, 1.8, 1.0],
            y_range=[-1.8, 1.8, 1.0],
            z_range=[-0.6, 1.3, 1.0],
            x_length=5.5,
            y_length=5.5,
            z_length=3.2,
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

        # Billboarded axis labels near positive tips
        label_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        label_x.move_to(axes.c2p(2.0, 0, 0))

        label_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        label_y.move_to(axes.c2p(0, 2.0, 0))

        label_f = MathTex("f", font_size=MIN_FONT, color=INK_DIM)
        label_f.move_to(axes.c2p(0, 0, 1.45))

        # Base non-quadratic function:
        # f(x, y) = sin(x)*cos(y)/1.2 + 0.2*(x^2 + y^2)
        def f(u, v):
            return np.sin(u) * np.cos(v) / 1.2 + 0.2 * (u**2 + v**2)

        # Base surface checkerboard
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-1.6, 1.6],
            v_range=[-1.6, 1.6],
            resolution=(16, 16),
            stroke_color=V_COLOR,
            stroke_width=0.4,
            stroke_opacity=0.3,
        )
        for face in surface.submobjects:
            opac = 0.35 if (face.u_index + face.v_index) % 2 == 0 else 0.65
            face.set_fill(color=V_COLOR, opacity=opac)

        # Base point p = (-0.5, 0.4)
        x0, y0 = -0.5, 0.4
        z0 = f(x0, y0)

        # Derivatives at p
        # df/dx = cos(x)*cos(y)/1.2 + 0.4*x
        fx = np.cos(x0) * np.cos(y0) / 1.2 + 0.4 * x0
        # df/dy = -sin(x)*sin(y)/1.2 + 0.4*y
        fy = -np.sin(x0) * np.sin(y0) / 1.2 + 0.4 * y0
        # fxx = -sin(x)*cos(y)/1.2 + 0.4
        fxx = -np.sin(x0) * np.cos(y0) / 1.2 + 0.4
        # fyy = -sin(x)*cos(y)/1.2 + 0.4
        fyy = -np.sin(x0) * np.cos(y0) / 1.2 + 0.4
        # fxy = -cos(x)*sin(y)/1.2
        fxy = -np.cos(x0) * np.sin(y0) / 1.2

        # Approximating plane: first-order
        def z_plane(u, v):
            hx = u - x0
            hy = v - y0
            return z0 + fx * hx + fy * hy

        # Approximating bowl: second-order (quadratic)
        def z_quad(u, v):
            hx = u - x0
            hy = v - y0
            return z0 + fx * hx + fy * hy + 0.5 * (fxx * (hx**2) + 2 * fxy * hx * hy + fyy * (hy**2))

        patch_rad = 1.0
        u_lims = [x0 - patch_rad, x0 + patch_rad]
        v_lims = [y0 - patch_rad, y0 + patch_rad]

        tangent_plane = Surface(
            lambda u, v: axes.c2p(u, v, z_plane(u, v)),
            u_range=u_lims,
            v_range=v_lims,
            resolution=(14, 14),
            stroke_color=RESULT_COLOR,
            stroke_width=0.4,
            stroke_opacity=0.4,
        )
        for face in tangent_plane.submobjects:
            opac = 0.50 if (face.u_index + face.v_index) % 2 == 0 else 0.75
            face.set_fill(color=RESULT_COLOR, opacity=opac)

        quad_surface = Surface(
            lambda u, v: axes.c2p(u, v, z_quad(u, v)),
            u_range=u_lims,
            v_range=v_lims,
            resolution=(14, 14),
            stroke_color=RESULT_COLOR,
            stroke_width=0.4,
            stroke_opacity=0.4,
        )
        for face in quad_surface.submobjects:
            opac = 0.50 if (face.u_index + face.v_index) % 2 == 0 else 0.75
            face.set_fill(color=RESULT_COLOR, opacity=opac)

        # Dot at evaluation point p
        point_dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.08, color=RESULT_COLOR)
        flash_dot = Dot3D(point=axes.c2p(x0, y0, z0), radius=0.15, color=HIGHLIGHT)

        # One fixed-in-frame formula, revealed in two pieces
        formula = MathTex(
            r"f(\mathbf p + \mathbf h) \approx f(\mathbf p) + \nabla f^{\top}\mathbf h",
            r"+ \dfrac{1}{2}\,\mathbf h^{\top} H\,\mathbf h",
            font_size=MIN_FONT,
        )
        formula[1].set_color(RESULT_COLOR)
        formula.to_edge(UP, buff=0.3).shift(UP * 0.9 + LEFT * 0.7)  # frame_center shifts fixed mobjects too
        line1 = VGroup(BackgroundRectangle(formula[0], color=BG, fill_opacity=0.85, buff=0.08), formula[0])
        line2 = VGroup(BackgroundRectangle(formula[1], color=BG, fill_opacity=0.85, buff=0.08), formula[1])

        # Register animated cards for fixed-in-frame
        self.camera.add_fixed_in_frame_mobjects(line1, line2)

        # 3. First frame: givens present immediately (never open on empty frame)
        self.add(axes, surface, point_dot)
        self.add_fixed_orientation_mobjects(label_x, label_y, label_f)
        self.wait(1.5)

        # 4. Tangent plane appears at p + line 1
        self.play(FadeIn(tangent_plane), FadeIn(line1), run_time=1.5)
        self.play(FadeIn(flash_dot, run_time=0.25))
        self.play(FadeOut(flash_dot, run_time=0.25))
        self.wait(1.0)

        # 5. Morph tangent plane into quadratic surface (bowl hugging surface) + line 2
        self.play(
            Transform(tangent_plane, quad_surface),
            FadeIn(line2),
            run_time=2.5,
        )
        self.wait(1.0)

        # 6. Slow orbit to showcase how quadratic bowl hugs the surface near p
        self.begin_ambient_camera_rotation(rate=-0.04)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


# =============================================================================
# SCENE 2: CriticalPoints (ThreeDScene)
# =============================================================================
class CriticalPoints(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-45 * DEGREES, frame_center=UP * 0.5)

        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 1.0],
            y_range=[-1.5, 1.5, 1.0],
            z_range=[-1.5, 1.5, 1.0],
            x_length=4.8,
            y_length=4.8,
            z_length=3.75,
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

        label_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR).move_to(axes.c2p(1.95, 0, 0))
        label_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR).move_to(axes.c2p(0, -1.95, 0))
        label_f = MathTex("f", font_size=MIN_FONT, color=INK_DIM).move_to(axes.c2p(0, 0, 1.8))

        s = 0.4
        R = 1.15

        def make_surface(fn):
            surf = Surface(
                lambda u, v: axes.c2p(u, v, fn(u, v)),
                u_range=[-R, R],
                v_range=[-R, R],
                resolution=(16, 16),
                stroke_color=V_COLOR,
                stroke_width=0.4,
                stroke_opacity=0.3,
            )
            for face in surf.submobjects:
                opac = 0.35 if (face.u_index + face.v_index) % 2 == 0 else 0.65
                face.set_fill(color=V_COLOR, opacity=opac)
            return surf

        surf = make_surface(lambda u, v: s * (u**2 + v**2))
        surf_cap = make_surface(lambda u, v: -s * (u**2 + v**2))
        surf_saddle = make_surface(lambda u, v: s * (u**2 - v**2))

        # Flat tangent plane at the origin (grad f = 0)
        pr = 0.7
        tan_plane = Surface(
            lambda u, v: axes.c2p(u, v, 0.0),
            u_range=[-pr, pr],
            v_range=[-pr, pr],
            resolution=(10, 10),
            stroke_color=RESULT_COLOR,
            stroke_width=0.4,
            stroke_opacity=0.4,
        )
        for face in tan_plane.submobjects:
            opac = 0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60
            face.set_fill(color=RESULT_COLOR, opacity=opac)

        origin_dot = Dot3D(point=axes.c2p(0, 0, 0), radius=0.07, color=RESULT_COLOR)

        # Saddle principal curves: up along x, down along y
        curve_up = axes.plot_parametric_curve(
            lambda t: np.array([t, 0.0, s * t**2]), t_range=[-R, R], color=X_COLOR, stroke_width=6
        )
        curve_down = axes.plot_parametric_curve(
            lambda t: np.array([0.0, t, -s * t**2]), t_range=[-R, R], color=Y_COLOR, stroke_width=6
        )

        def card(tex):
            m = MathTex(tex, font_size=MIN_FONT)
            m.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            m.to_edge(UP, buff=0.3).shift(UP * 0.5)  # fixed mobjects follow frame_center
            return m

        card_min = card(r"\text{minimum:}\ \lambda_1 > 0,\ \lambda_2 > 0")
        card_max = card(r"\text{maximum:}\ \lambda_1 < 0,\ \lambda_2 < 0")
        card_saddle = card(r"\text{saddle:}\ \lambda_1 > 0 > \lambda_2")
        self.camera.add_fixed_in_frame_mobjects(card_min, card_max, card_saddle)
        self.remove(card_max, card_saddle)

        self.add(axes, surf, tan_plane, origin_dot, card_min)
        self.add_fixed_orientation_mobjects(label_x, label_y, label_f)
        self.wait(2.5)

        self.play(FadeOut(card_min), Transform(surf, surf_cap), run_time=1.6)
        self.play(FadeIn(card_max), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(card_max), Transform(surf, surf_saddle), run_time=1.6)
        self.play(FadeIn(card_saddle), run_time=0.6)
        self.wait(0.8)

        self.play(Create(curve_up), Create(curve_down), run_time=1.8)
        self.wait(0.5)

        self.begin_ambient_camera_rotation(rate=-0.04)
        self.wait(4.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

# =============================================================================
# SCENE 3: HessianMatrix (2D)
# =============================================================================
def bg(m, buff=0.08):
    m.add_background_rectangle(color=BG, opacity=0.85, buff=buff)
    return m


def tex(s, color=INK):
    return MathTex(s, font_size=MIN_FONT, color=color)


class HessianMatrix(Scene):
    def construct(self):
        # ---- Part A: the saddle's Hessian, built entry by entry -------------
        title = MathTex(r"f(x, y) = x^2 - y^2", font_size=50, color=V_COLOR).move_to(UP * 1.7)

        sym = Matrix(
            [[r"f_{xx}", r"f_{xy}"], [r"f_{yx}", r"f_{yy}"]],
            element_to_mobject=lambda t: MathTex(t, font_size=50),
            h_buff=1.2,
            v_buff=0.85,
        )
        num = Matrix(
            [["2", "0"], ["0", "-2"]],
            element_to_mobject=lambda t: MathTex(t, font_size=50),
            h_buff=1.0,
            v_buff=0.85,
        )
        h_eq = MathTex(r"H =", font_size=50)
        eq = MathTex(r"=", font_size=50)
        row = VGroup(h_eq, sym, eq, num).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.1)

        # colour the diagonal by direction
        sym.get_entries()[0].set_color(X_COLOR)
        sym.get_entries()[3].set_color(Y_COLOR)
        num.get_entries()[0].set_color(X_COLOR)
        num.get_entries()[3].set_color(Y_COLOR)

        self.add(title, h_eq, sym.get_brackets())
        self.wait(1.0)
        for e in sym.get_entries():
            self.play(FadeIn(e), run_time=0.6)
        self.play(FadeIn(eq), FadeIn(num.get_brackets()), run_time=0.6)
        for e in num.get_entries():
            self.play(FadeIn(e), run_time=0.6)
        self.wait(2.0)

        # ---- Part B: f = xy, eigenvectors on its contour map ----------------
        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            x_length=4.3,
            y_length=4.3,
            axis_config={
                "stroke_color": GRID,
                "stroke_width": 2,
                "include_ticks": False,
                "include_tip": False,
            },
        ).move_to(RIGHT * 2.55 + UP * 0.3)

        x_label = bg(tex("x", X_COLOR)).next_to(axes.c2p(2.2, 0), RIGHT, buff=0.05)
        y_label = bg(tex("y", Y_COLOR)).next_to(axes.c2p(0, 2.2), RIGHT, buff=0.08)
        map_title = tex(r"f(x, y) = xy", V_COLOR)

        contours = VGroup()
        for c in [0.4, 0.9, 1.6, -0.4, -0.9, -1.6]:
            x0 = max(abs(c) / 1.95, 0.19)
            for sign in (1, -1):
                xr = [x0, 2.0] if sign > 0 else [-2.0, -x0]
                contours.add(
                    axes.plot(lambda x, c=c: c / x, x_range=xr, color=INK_DIM, stroke_width=2)
                )

        s2 = 1 / np.sqrt(2)
        v1_arrow = Arrow(axes.c2p(0, 0), axes.c2p(1.7, 1.7), buff=0, color=X_COLOR,
                         stroke_width=6, max_tip_length_to_length_ratio=0.2)
        v2_arrow = Arrow(axes.c2p(0, 0), axes.c2p(1.7, -1.7), buff=0, color=Y_COLOR,
                         stroke_width=6, max_tip_length_to_length_ratio=0.2)

        h2 = MathTex(r"H = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}", font_size=50)
        l1 = tex(r"\lambda_1 = +1\ \text{(up)}", X_COLOR)
        e1 = tex(r"\mathbf v_1 = (1, 1)/\sqrt{2}", X_COLOR)
        l2 = tex(r"\lambda_2 = -1\ \text{(down)}", Y_COLOR)
        e2 = tex(r"\mathbf v_2 = (1, -1)/\sqrt{2}", Y_COLOR)
        left = VGroup(map_title, h2, l1, e1, l2, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        left.to_edge(LEFT, buff=0.3).set_y(0.25)
        note = bg(tex(r"\text{symmetric } H \Rightarrow \text{real } \lambda,\ \text{orthogonal } \mathbf v", RESULT_COLOR))
        note.to_edge(DOWN, buff=0.25)

        self.play(FadeOut(VGroup(title, h_eq, sym, eq, num)), run_time=0.8)
        self.play(FadeIn(VGroup(axes, x_label, y_label, map_title, h2)), run_time=1.2)
        self.play(Create(contours), run_time=1.8)
        self.play(GrowArrow(v1_arrow), FadeIn(l1), FadeIn(e1), run_time=1.5)
        self.wait(0.6)
        self.play(GrowArrow(v2_arrow), FadeIn(l2), FadeIn(e2), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(3.0)


# =============================================================================
# SCENE 4: Convexity (2D)
# =============================================================================
class Convexity(Scene):
    def construct(self):
        caption_def = bg(tex(r"f(t\,a + (1-t)\,b) \le t\,f(a) + (1-t)\,f(b)")).move_to(UP * 2.3)
        caption_min = bg(
            tex(r"\text{convex} \Rightarrow \text{every local minimum is global}", RESULT_COLOR)
        ).move_to(UP * 2.3)

        axes = Axes(
            x_range=[-2.3, 2.3, 1],
            y_range=[0, 3.2, 1],
            x_length=7.4,
            y_length=3.9,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
                "include_tip": False,
            },
        ).move_to(DOWN * 0.5)
        x_label = bg(tex("x", X_COLOR)).next_to(axes.c2p(2.3, 0), RIGHT, buff=0.08)
        f_label = bg(tex("f", INK_DIM)).next_to(axes.c2p(0, 3.2), LEFT, buff=0.1)

        def f_conv(x):
            return 0.3 * x**2 + 0.04 * x**4 + 0.3

        def g_non(x):
            return 0.22 * x**4 - 1.1 * x**2 + 0.2 * x + 2.5

        m = ValueTracker(0.0)  # 0 = convex function, 1 = two-basin function

        def F(x):
            k = m.get_value()
            return (1 - k) * f_conv(x) + k * g_non(x)

        curve = always_redraw(
            lambda: axes.plot(F, x_range=[-2.2, 2.2], color=V_COLOR, stroke_width=4)
        )

        a_val = ValueTracker(-1.8)
        b_val = ValueTracker(1.8)

        def chord_color():
            return interpolate_color(ManimColor(RESULT_COLOR), ManimColor(Y_COLOR), m.get_value())

        def pa():
            return axes.c2p(a_val.get_value(), F(a_val.get_value()))

        def pb():
            return axes.c2p(b_val.get_value(), F(b_val.get_value()))

        chord = always_redraw(lambda: Line(pa(), pb(), color=chord_color(), stroke_width=5))
        dots = always_redraw(
            lambda: VGroup(
                Dot(pa(), radius=0.09, color=chord_color()),
                Dot(pb(), radius=0.09, color=chord_color()),
            )
        )

        lab_pos = axes.c2p(1.5, 2.95)
        label_conv = bg(tex(r"\text{convex}", V_COLOR)).move_to(lab_pos)
        label_non = bg(tex(r"\text{non-convex}", V_COLOR)).move_to(lab_pos)

        # the two minima of g_non
        r = np.roots([0.88, 0, -2.2, 0.2])
        r = np.sort(r.real)
        x_glob, x_loc = r[0], r[2]
        dot_glob = Dot(axes.c2p(x_glob, g_non(x_glob)), radius=0.1, color=RESULT_COLOR)
        dot_loc = Dot(axes.c2p(x_loc, g_non(x_loc)), radius=0.1, color=RESULT_COLOR)
        lab_glob = bg(tex(r"\text{global}", RESULT_COLOR)).next_to(dot_glob, DOWN, buff=0.2)
        lab_loc = bg(tex(r"\text{local}", RESULT_COLOR)).next_to(dot_loc, DOWN, buff=0.2)

        self.add(axes, x_label, f_label, curve, label_conv, chord, dots, caption_def)
        self.wait(1.5)

        self.play(a_val.animate.set_value(-0.8), b_val.animate.set_value(2.0), run_time=2.2)
        self.play(a_val.animate.set_value(-2.0), b_val.animate.set_value(0.6), run_time=2.2)
        self.play(a_val.animate.set_value(-1.6), b_val.animate.set_value(1.6), run_time=1.6)
        self.wait(0.6)

        self.play(FadeOut(label_conv), run_time=0.4)
        self.play(m.animate.set_value(1.0), run_time=2.5)
        self.play(FadeIn(label_non), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(chord), FadeOut(dots), FadeOut(label_non), FadeOut(caption_def), run_time=0.8)
        self.play(
            FadeIn(dot_glob), FadeIn(lab_glob), FadeIn(dot_loc), FadeIn(lab_loc),
            FadeIn(caption_min),
            run_time=1.5,
        )
        self.wait(3.5)
