# Adapted from 3b1b/videos _2017/eoc/chapter10.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


def get_clipped_poly_range(poly_fn, x_min=-6.0, x_max=6.0, y_min=-1.35, y_max=1.35, x_center=0.0):
    """Finds contiguous [x_left, x_right] containing x_center where y is in [y_min, y_max]."""
    dx = 0.02
    x_r = x_center
    while x_r + dx <= x_max:
        y_val = poly_fn(x_r + dx)
        if y_val < y_min or y_val > y_max:
            break
        x_r += dx

    x_l = x_center
    while x_l - dx >= x_min:
        y_val = poly_fn(x_l - dx)
        if y_val < y_min or y_val > y_max:
            break
        x_l -= dx

    if x_r - x_l < 0.2:
        x_l = x_center - 0.1
        x_r = x_center + 0.1
    return [max(x_l, x_min), min(x_r, x_max)]


# =============================================================================
# SCENE 1: ConstructQuadratic
# =============================================================================
class ConstructQuadratic(Scene):
    def construct(self):
        # 1. Coordinate Axes
        axes = Axes(
            x_range=[-3.0, 3.001, 2],
            y_range=[-1.5, 1.501, 1],
            x_length=5.4,
            y_length=3.2,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.5,
                "include_ticks": True,
                "include_tip": False,
            },
            tips=False,
        ).move_to(LEFT * 1.8 + DOWN * 0.45)

        axes.add_coordinates(font_size=MIN_FONT)
        for axis in axes.get_axes():
            if hasattr(axis, "numbers"):
                for num in axis.numbers:
                    num.set_color(INK_DIM)

        x_axis_label = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        x_axis_label.next_to(axes.c2p(3.0, 0), RIGHT, buff=0.15).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Given curve cos(x)
        cos_curve = axes.plot(
            np.cos,
            x_range=[-3.0, 3.0],
            color=V_COLOR,
            stroke_width=3.5,
        )
        # Position cos(x) label in the open upper-left quadrant of axes
        cos_label = MathTex(r"\cos(x)", font_size=MIN_FONT, color=V_COLOR)
        cos_label.move_to(axes.c2p(-2.2, 1.25)).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Polynomial formula title at top
        poly_title = MathTex(
            r"P(x) = c_0 + c_1 x + c_2 x^2",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        ).move_to(UP * 2.15)

        # 2. Live ValueTrackers
        c0 = ValueTracker(0.0)
        c1 = ValueTracker(0.0)
        c2 = ValueTracker(0.0)

        # Dynamic quadratic curve clipped cleanly so it doesn't overshoot
        p_curve = always_redraw(
            lambda: axes.plot(
                lambda x: c0.get_value() + c1.get_value() * x + c2.get_value() * (x**2),
                x_range=get_clipped_poly_range(
                    lambda x: c0.get_value() + c1.get_value() * x + c2.get_value() * (x**2),
                    x_min=-2.9,
                    x_max=2.9,
                    y_min=-1.05,
                    y_max=1.20,
                ),
                color=RESULT_COLOR,
                stroke_width=3.5,
            )
        )

        # Right-hand side readout panel
        panel_x = 3.35

        # c0 readout & condition
        c0_title = MathTex(r"c_0 =", font_size=MIN_FONT, color=RESULT_COLOR)
        c0_num = DecimalNumber(
            0.0,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        c0_num.add_updater(lambda m: m.set_value(c0.get_value()))
        c0_row = VGroup(c0_title, c0_num).arrange(RIGHT, buff=0.12)
        c0_row.move_to(RIGHT * panel_x + UP * 0.95)
        c0_num.add_updater(lambda m: m.next_to(c0_title, RIGHT, buff=0.12))

        c0_cond = MathTex(r"P(0) = \cos(0)", font_size=MIN_FONT, color=INK)
        c0_cond.next_to(c0_row, DOWN, buff=0.15)

        # c1 readout & condition
        c1_title = MathTex(r"c_1 =", font_size=MIN_FONT, color=RESULT_COLOR)
        c1_num = DecimalNumber(
            0.0,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        c1_num.add_updater(lambda m: m.set_value(c1.get_value()))
        c1_row = VGroup(c1_title, c1_num).arrange(RIGHT, buff=0.12)
        c1_row.move_to(RIGHT * panel_x + DOWN * 0.05)
        c1_num.add_updater(lambda m: m.next_to(c1_title, RIGHT, buff=0.12))

        c1_cond = MathTex(r"P'(0) = \cos'(0)", font_size=MIN_FONT, color=INK)
        c1_cond.next_to(c1_row, DOWN, buff=0.15)

        # c2 readout & condition
        c2_title = MathTex(r"c_2 =", font_size=MIN_FONT, color=RESULT_COLOR)
        c2_num = DecimalNumber(
            0.0,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        c2_num.add_updater(lambda m: m.set_value(c2.get_value()))
        c2_row = VGroup(c2_title, c2_num).arrange(RIGHT, buff=0.12)
        c2_row.move_to(RIGHT * panel_x + DOWN * 1.05)
        c2_num.add_updater(lambda m: m.next_to(c2_title, RIGHT, buff=0.12))

        c2_cond = MathTex(r"P''(0) = \cos''(0)", font_size=MIN_FONT, color=INK)
        c2_cond.next_to(c2_row, DOWN, buff=0.15)

        # Opening frame shows givens
        self.add(axes, x_axis_label, cos_curve, cos_label, poly_title, p_curve)
        self.wait(1.0)

        # --- Step 1: Match Value at 0 (c0 = 1) ---
        target_dot = Dot(axes.c2p(0, 1), radius=0.08, color=RESULT_COLOR)
        self.play(FadeIn(c0_row), FadeIn(c0_cond), FadeIn(target_dot), run_time=0.8)
        self.play(c0.animate.set_value(1.0), run_time=1.6)
        # Settle on c0 = 1.00 (sheet 20% sample falls here)
        self.wait(2.0)

        # --- Step 2: Match Slope at 0 (c1 = 0) ---
        self.play(FadeIn(c1_row), FadeIn(c1_cond), run_time=0.8)
        self.play(c1.animate.set_value(0.65), run_time=1.2)
        self.play(c1.animate.set_value(-0.65), run_time=1.2)
        self.play(c1.animate.set_value(0.0), run_time=1.0)
        # Settle on c1 = 0.00 (sheet 50% sample falls here)
        self.wait(2.0)

        # --- Step 3: Match Curvature at 0 (c2 = -0.5) ---
        self.play(FadeIn(c2_row), FadeIn(c2_cond), run_time=0.8)
        self.play(c2.animate.set_value(0.35), run_time=1.2)
        self.play(c2.animate.set_value(-0.50), run_time=1.8)
        # Settle on c2 = -0.50 (sheet 80% and last frame fall here)
        self.wait(4.6)


# =============================================================================
# SCENE 2: MoreTerms
# =============================================================================
class MoreTerms(Scene):
    def construct(self):
        # 1. Coordinate Axes
        axes = Axes(
            x_range=[-6.5, 6.501, 2],
            y_range=[-1.6, 1.601, 1],
            x_length=8.6,
            y_length=3.2,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.5,
                "include_ticks": True,
                "include_tip": False,
            },
            tips=False,
        ).move_to(DOWN * 0.45)

        axes.add_coordinates(font_size=MIN_FONT)
        for axis in axes.get_axes():
            if hasattr(axis, "numbers"):
                for num in axis.numbers:
                    num.set_color(INK_DIM)

        x_label = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        x_label.next_to(axes.c2p(6.5, 0), RIGHT, buff=0.15).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Cosine graph
        cos_curve = axes.plot(
            np.cos,
            x_range=[-6.3, 6.3],
            color=V_COLOR,
            stroke_width=3.5,
        )
        # Position cos(x) label in upper-left open region away from all curves and ticks
        cos_label = MathTex(r"\cos(x)", font_size=MIN_FONT, color=V_COLOR)
        cos_label.move_to(axes.c2p(-5.8, 1.25)).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Polynomial definitions
        def p2_fn(x):
            return 1.0 - 0.5 * (x**2)

        def p4_fn(x):
            return p2_fn(x) + (x**4) / 24.0

        def p6_fn(x):
            return p4_fn(x) - (x**6) / 720.0

        def p8_fn(x):
            return p6_fn(x) + (x**8) / 40320.0

        # Curves clipped cleanly to axes y-bounds [-1.25, 1.20]
        curve_p2 = axes.plot(
            p2_fn,
            x_range=get_clipped_poly_range(p2_fn, x_min=-6.2, x_max=6.2, y_min=-1.25, y_max=1.20),
            color=RESULT_COLOR,
            stroke_width=3.5,
        )
        curve_p4 = axes.plot(
            p4_fn,
            x_range=get_clipped_poly_range(p4_fn, x_min=-6.2, x_max=6.2, y_min=-1.25, y_max=1.20),
            color=RESULT_COLOR,
            stroke_width=3.5,
        )
        curve_p6 = axes.plot(
            p6_fn,
            x_range=get_clipped_poly_range(p6_fn, x_min=-6.2, x_max=6.2, y_min=-1.25, y_max=1.20),
            color=RESULT_COLOR,
            stroke_width=3.5,
        )
        curve_p8 = axes.plot(
            p8_fn,
            x_range=get_clipped_poly_range(p8_fn, x_min=-6.2, x_max=6.2, y_min=-1.25, y_max=1.20),
            color=RESULT_COLOR,
            stroke_width=3.5,
        )

        # Formulas across degrees
        f2 = MathTex(
            r"P(x) = 1 - \frac{x^2}{2}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        ).move_to(UP * 2.05)

        f4 = MathTex(
            r"P(x) = 1 - \frac{x^2}{2} + \frac{x^4}{24}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        ).move_to(UP * 2.05)

        f6 = MathTex(
            r"P(x) = 1 - \frac{x^2}{2} + \frac{x^4}{24} - \frac{x^6}{720}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        ).move_to(UP * 2.05)

        f8 = MathTex(
            r"P(x) = 1 - \frac{x^2}{2} + \frac{x^4}{24} - \frac{x^6}{720} + \frac{x^8}{40320}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        ).move_to(UP * 2.05)

        # Frame 1 shows P2 initial state
        self.add(axes, x_label, cos_curve, cos_label, curve_p2, f2)
        # Settle on P2 (sheet 20% sample falls here)
        self.wait(3.5)

        # Degree 4
        self.play(
            FadeOut(f2),
            FadeIn(f4),
            ReplacementTransform(curve_p2, curve_p4),
            run_time=1.0,
        )
        # Settle on P4 (sheet 50% sample falls here)
        self.wait(4.0)

        # Degree 6
        self.play(
            FadeOut(f4),
            FadeIn(f6),
            ReplacementTransform(curve_p4, curve_p6),
            run_time=1.0,
        )
        # Settle on P6 (sheet 80% sample falls here)
        self.wait(4.0)

        # Degree 8
        self.play(
            FadeOut(f6),
            FadeIn(f8),
            ReplacementTransform(curve_p6, curve_p8),
            run_time=1.0,
        )
        # Settle on P8 (sheet last frame falls here)
        self.wait(2.2)


# =============================================================================
# SCENE 3: FactorialTerms
# =============================================================================
class FactorialTerms(Scene):
    def construct(self):
        # 4 lines built vertically with buff >= 0.35, all fonts >= MIN_FONT
        line1 = MathTex(
            r"\frac{d^n}{dx^n}\bigl(",
            r"c_n",
            r"\,x^n\bigr) = n!",
            r"c_n",
            font_size=MIN_FONT + 2,
        )
        line1[0].set_color(INK)
        line1[1].set_color(RESULT_COLOR)
        line1[2].set_color(INK)
        line1[3].set_color(RESULT_COLOR)

        line2 = MathTex(
            r"P^{(n)}(0) = ",
            r"f^{(n)}(0)",
            r"\implies n!",
            r"c_n",
            r"=",
            r"f^{(n)}(0)",
            font_size=MIN_FONT + 2,
        )
        line2[0].set_color(RESULT_COLOR)
        line2[1].set_color(V_COLOR)
        line2[2].set_color(INK)
        line2[3].set_color(RESULT_COLOR)
        line2[4].set_color(INK)
        line2[5].set_color(V_COLOR)

        line3 = MathTex(
            r"c_n",
            r"=",
            r"\frac{f^{(n)}(0)}{n!}",
            font_size=MIN_FONT + 4,
        )
        line3[0].set_color(RESULT_COLOR)
        line3[1].set_color(INK)
        line3[2].set_color(V_COLOR)

        line4 = MathTex(
            r"P(x)",
            r"=",
            r"\sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}\,(x - a)^n",
            font_size=MIN_FONT + 4,
        )
        line4[0].set_color(RESULT_COLOR)
        line4[1].set_color(INK)
        line4[2].set_color(V_COLOR)

        lines = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.42)
        lines.move_to(ORIGIN)

        # Frame 1 shows line1 (never an empty opening frame)
        self.add(line1)
        # Settle on Line 1 (sheet 20% sample falls here at ~4.0s)
        self.wait(4.5)

        # Step 2: Match derivative equation
        self.play(Write(line2), run_time=1.2)
        # Settle on Lines 1 & 2 (sheet 50% sample falls here at ~9.8s)
        self.wait(4.5)

        # Step 3: Solve for coefficient c_n
        self.play(Write(line3), run_time=1.2)
        # Settle on Lines 1, 2, 3 (sheet 80% sample falls here at ~15.5s)
        self.wait(5.0)

        # Step 4: General Taylor series expansion
        self.play(Write(line4), run_time=1.4)
        # Settle on all 4 lines (sheet last frame falls here at ~19.5s)
        self.wait(2.2)


# =============================================================================
# SCENE 4: ApproximateNearPoint
# =============================================================================
class ApproximateNearPoint(Scene):
    def construct(self):
        # 1. Coordinate Axes for f(x) = e^{x/2}
        axes = Axes(
            x_range=[-0.5, 3.201, 1],
            y_range=[0, 3.801, 1],
            x_length=6.4,
            y_length=3.0,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.5,
                "include_ticks": True,
                "include_tip": False,
            },
            tips=False,
        ).move_to(LEFT * 0.9 + UP * 0.45)

        axes.add_coordinates(font_size=MIN_FONT)
        for axis in axes.get_axes():
            if hasattr(axis, "numbers"):
                for num in axis.numbers:
                    num.set_color(INK_DIM)

        x_axis_label = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        x_axis_label.next_to(axes.c2p(3.2, 0), RIGHT, buff=0.15).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Function f(x) = exp(x / 2)
        def f_fn(x):
            return np.exp(0.5 * x)

        f_curve = axes.plot(
            f_fn,
            x_range=[-0.4, 2.65],
            color=V_COLOR,
            stroke_width=3.5,
        )
        # Position f(x) label in open space above curve and right of y-axis
        f_label = MathTex(r"f(x) = e^{x/2}", font_size=MIN_FONT, color=V_COLOR)
        f_label.move_to(axes.c2p(0.8, 3.3)).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Expansion point a = 1
        a_val = 1.0
        fa_val = f_fn(a_val)  # approx 1.6487
        dfa_val = 0.5 * fa_val  # approx 0.8244
        d2fa_val = 0.25 * fa_val  # approx 0.4122

        p_a = axes.c2p(a_val, fa_val)
        p_axis = axes.c2p(a_val, 0)
        v_dash = DashedLine(p_axis, p_a, stroke_color=INK_DIM, stroke_width=2)
        dot_a = Dot(p_a, radius=0.08, color=RESULT_COLOR)
        a_label = MathTex("a = 1", font_size=MIN_FONT, color=X_COLOR)
        a_label.next_to(p_axis, DOWN, buff=0.18).add_background_rectangle(
            color=BG, opacity=1.0, buff=0.10
        )
        a_label.set_z_index(5)

        # Approximations
        def lin_fn(x):
            return fa_val + dfa_val * (x - a_val)

        def quad_fn(x):
            return lin_fn(x) + 0.5 * d2fa_val * ((x - a_val) ** 2)

        lin_curve = axes.plot(
            lin_fn,
            x_range=[0.0, 3.0],
            color=RESULT_COLOR,
            stroke_width=3.5,
        )
        lin_label = MathTex(r"\text{linear}", font_size=MIN_FONT, color=RESULT_COLOR)
        lin_label.move_to(axes.c2p(2.85, 2.5)).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        quad_curve = axes.plot(
            quad_fn,
            x_range=[0.0, 2.7],
            color=RESULT_COLOR,
            stroke_width=3.5,
        )
        # Position quadratic label below the curve in clear open space
        quad_label = MathTex(r"\text{quadratic}", font_size=MIN_FONT, color=RESULT_COLOR)
        quad_label.move_to(axes.c2p(2.45, 2.25)).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Error gap at x = 2.1
        x_err = 2.1
        err_line = DoubleArrow(
            axes.c2p(x_err, lin_fn(x_err)),
            axes.c2p(x_err, f_fn(x_err)),
            buff=0.0,
            stroke_width=2.5,
            color=Y_COLOR,
            max_tip_length_to_length_ratio=0.35,
        )
        err_label = MathTex(r"\text{error}", font_size=MIN_FONT, color=Y_COLOR)
        err_label.next_to(err_line, LEFT, buff=0.12).add_background_rectangle(
            color=BG, opacity=0.85, buff=0.08
        )

        # Final Taylor approximation formula setting up multivariate version
        final_formula = MathTex(
            r"f(a+h)",
            r"\approx",
            r"f(a)",
            r"+",
            r"f'(a)\,h",
            r"+",
            r"\tfrac12 f''(a)\,h^2",
            font_size=MIN_FONT + 2,
        )
        final_formula[0].set_color(V_COLOR)
        final_formula[1].set_color(INK)
        final_formula[2].set_color(V_COLOR)
        final_formula[3].set_color(INK)
        final_formula[4].set_color(RESULT_COLOR)
        final_formula[5].set_color(INK)
        final_formula[6].set_color(RESULT_COLOR)
        final_formula.move_to(DOWN * 2.15)

        # Opening frame shows function and expansion point
        self.add(axes, x_axis_label, f_curve, f_label, v_dash, dot_a, a_label)
        # Settle on givens (sheet 20% sample falls here)
        self.wait(3.5)

        # 1. Linear approximation
        self.play(Create(lin_curve), FadeIn(lin_label), run_time=1.0)
        self.play(Create(err_line), FadeIn(err_label), run_time=0.8)
        # Settle on linear + error (sheet 50% sample falls here)
        self.wait(3.8)

        # 2. Quadratic approximation hugs closer and shrinks the error
        self.play(
            FadeOut(err_line),
            FadeOut(err_label),
            ReplacementTransform(lin_curve, quad_curve),
            FadeOut(lin_label),
            FadeIn(quad_label),
            run_time=1.2,
        )
        # Settle on quadratic (sheet 80% sample falls here)
        self.wait(3.2)

        # 3. Final multivariate-ready formula
        self.play(Write(final_formula), run_time=1.2)
        # Settle on final state (sheet last frame falls here)
        self.wait(1.5)
