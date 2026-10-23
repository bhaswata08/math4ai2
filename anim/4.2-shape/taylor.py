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

        def deg(n):
            return MathTex(rf"\text{{degree }}{n}", font_size=MIN_FONT, color=RESULT_COLOR).move_to(axes.c2p(-5.0, -1.2))

        d2, d4, d6, d8 = deg(2), deg(4), deg(6), deg(8)

        # Frame 1 shows P2 initial state
        self.add(axes, x_label, cos_curve, cos_label, curve_p2, f2, d2)
        self.wait(3.0)

        cur = curve_p2
        for fo, fi, do, di, cn in ((f2, f4, d2, d4, curve_p4), (f4, f6, d4, d6, curve_p6), (f6, f8, d6, d8, curve_p8)):
            self.play(FadeOut(fo), FadeOut(do), run_time=0.4)
            self.play(FadeIn(fi), FadeIn(di), ReplacementTransform(cur, cn), run_time=1.2)
            cur = cn
            self.wait(3.0)
        self.wait(1.0)


# =============================================================================
# SCENE 3: FactorialByDifferentiating
# =============================================================================
class FactorialByDifferentiating(Scene):
    def construct(self):
        n = 4
        # row k holds the k-fold derivative of c_4 x^4, built from the real product n(n-1)...
        rows = []
        factors = []
        for k in range(n + 1):
            power = n - k
            mult = [n - j for j in range(k)]            # 4, 3, 2, 1 as far as differentiated
            prod = int(np.prod(mult)) if mult else 1
            parts = []
            if k == 0:
                parts = [r"c_4x^4"]
            else:
                parts = [r"\cdot".join(str(m) for m in mult), r"\,c_4" + ("" if power == 0 else (r"x" if power == 1 else rf"x^{power}"))]
            rows.append((parts, prod, power))
        assert rows[-1][1] == 24 == int(np.prod(range(1, n + 1)))

        mobs = []
        for k, (parts, prod, power) in enumerate(rows):
            if k == 0:
                m = MathTex(parts[0], font_size=MIN_FONT + 4, color=RESULT_COLOR)
                new_factor = None
            else:
                eq = rf"=\,{prod}\,c_4" + ("" if power == 0 else (r"x" if power == 1 else rf"x^{power}"))
                m = MathTex(parts[0], parts[1], *([] if k == 1 else [eq]), font_size=MIN_FONT + 2, color=RESULT_COLOR)
            mobs.append(m)
        col = VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        col.move_to(LEFT * 0.4 + UP * 0.1)
        col.align_to(RIGHT * -1.6, LEFT)
        dd = []
        for k in range(1, n + 1):
            lab = MathTex(r"\mathrm{d}/\mathrm{d}x", font_size=MIN_FONT, color=INK_DIM)
            lab.next_to(mobs[k], LEFT, buff=0.3)
            dd.append(lab)
        tag = MathTex(r"4\cdot3\cdot2\cdot1=4!=24", font_size=MIN_FONT + 4, color=HIGHLIGHT)
        tag.next_to(mobs[-1], DOWN, buff=0.35).align_to(mobs[-1], LEFT)
        # the mixed multiplier's newest factor flashes gold, then rests amber
        self.add(mobs[0])
        self.wait(2.0)
        for k in range(1, n + 1):
            m = mobs[k]
            newest = m[0]
            self.play(FadeIn(dd[k - 1]), FadeIn(m), run_time=0.8)
            self.play(Indicate(newest, color=HIGHLIGHT, scale_factor=1.15), run_time=0.8)
            self.wait(0.3)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in (*mobs, *dd, tag)], run_time=0.8)

        # match with cos at 0
        d4 = int(np.round(np.cos(0.0)))  # cos''''(x) = cos(x), so cos''''(0) = 1
        l1 = MathTex(r"P^{(4)}(0)=24\,c_4", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        l2 = MathTex(rf"\cos^{{(4)}}(0)={d4}", font_size=MIN_FONT + 4, color=V_COLOR)
        l3 = MathTex(rf"24\,c_4={d4}\ \Rightarrow\ c_4=\frac{{{d4}}}{{24}}", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        l4 = MathTex(r"P(x)=1-\frac{x^2}{2}+", r"\frac{x^4}{24}", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        l4[1].set_color(HIGHLIGHT)
        grp = VGroup(l1, l2, l3, l4).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(ORIGIN)
        for l in (l1, l2, l3):
            self.play(FadeIn(l), run_time=0.8)
            self.wait(1.0)
        self.play(FadeIn(l4), run_time=0.8)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in (l1, l2, l3, l4)], run_time=0.8)

        # general rule, stated at 0 first, then shifted to a
        g1 = MathTex(r"c_4=\frac{f^{(4)}(0)}{4!}=\frac{f^{(4)}(0)}{24}", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        g2 = MathTex(r"c_n=\frac{f^{(n)}(0)}{n!}", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        g3 = MathTex(r"\text{around }a:\ c_n(x-a)^n,\ c_n=\frac{f^{(n)}(a)}{n!}", font_size=MIN_FONT + 4, color=INK)
        gg = VGroup(g1, g2, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(ORIGIN)
        for g_ in (g1, g2, g3):
            self.play(FadeIn(g_), run_time=0.8)
            self.wait(1.4)
        self.wait(1.0)


# =============================================================================
# SCENE 4: ApproximateNearPoint
# =============================================================================
class ApproximateNearPoint(Scene):
    def construct(self):
        a = 1.0
        f_fn = lambda x: np.exp(0.5 * x)
        fa = f_fn(a)
        f1 = 0.5 * fa
        f2 = 0.25 * fa
        lin_fn = lambda x: fa + f1 * (x - a)
        quad_fn = lambda x: lin_fn(x) + 0.5 * f2 * (x - a) ** 2

        axes = Axes(
            x_range=[-0.5, 3.201, 1], y_range=[0, 3.801, 1], x_length=6.4, y_length=3.0,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5, "include_ticks": True, "include_tip": False},
            tips=False,
        ).move_to(LEFT * 0.9 + UP * 0.45)
        axes.add_coordinates(font_size=MIN_FONT)
        for axis in axes.get_axes():
            if hasattr(axis, "numbers"):
                for num in axis.numbers:
                    num.set_color(INK_DIM)
        x_axis_label = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        x_axis_label.next_to(axes.c2p(3.2, 0), RIGHT, buff=0.15).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        f_curve = axes.plot(f_fn, x_range=[-0.4, 2.65], color=V_COLOR, stroke_width=3.5)
        f_label = MathTex(r"f(x)=e^{x/2}", font_size=MIN_FONT, color=V_COLOR)
        f_label.move_to(axes.c2p(0.8, 3.35)).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        p_a = axes.c2p(a, fa)
        v_dash = DashedLine(axes.c2p(a, 0), p_a, stroke_color=INK_DIM, stroke_width=2)
        dot_a = Dot(p_a, radius=0.08, color=RESULT_COLOR)
        a_label = MathTex("a=1", font_size=MIN_FONT, color=X_COLOR)
        a_label.next_to(axes.c2p(a, 0), DOWN, buff=0.55).add_background_rectangle(color=BG, opacity=1.0, buff=0.10)

        lin_curve = axes.plot(lin_fn, x_range=[0.0, 2.65], color=RESULT_COLOR, stroke_width=3.5)
        lin_label = MathTex(r"\text{linear}", font_size=MIN_FONT, color=RESULT_COLOR)
        lin_label.move_to(axes.c2p(0.7, 0.55)).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        quad_curve = axes.plot(quad_fn, x_range=[0.0, 2.65], color=RESULT_COLOR, stroke_width=3.5)
        quad_label = MathTex(r"\text{quadratic}", font_size=MIN_FONT, color=RESULT_COLOR)
        quad_label.move_to(axes.c2p(0.7, 2.45)).add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        x_err = 2.6
        err_bar = DoubleArrow(axes.c2p(x_err, lin_fn(x_err)), axes.c2p(x_err, f_fn(x_err)), buff=0.0,
                              stroke_width=3, color=HIGHLIGHT, max_tip_length_to_length_ratio=0.35)
        err_label = MathTex(r"\text{error}", font_size=MIN_FONT, color=HIGHLIGHT)
        err_label.next_to(err_bar, RIGHT, buff=0.15)
        err_bar2 = DoubleArrow(axes.c2p(x_err, quad_fn(x_err)), axes.c2p(x_err, f_fn(x_err)), buff=0.0,
                               stroke_width=3, color=HIGHLIGHT, max_tip_length_to_length_ratio=0.35)

        final_formula = MathTex(r"f(a+h)", r"\approx", r"f(a)", r"+", r"f'(a)\,h", r"+", r"\tfrac12 f''(a)\,h^2",
                                font_size=MIN_FONT + 2)
        for i, c in enumerate([V_COLOR, INK, V_COLOR, INK, RESULT_COLOR, INK, RESULT_COLOR]):
            final_formula[i].set_color(c)
        final_formula.move_to(DOWN * 2.35)

        self.add(axes, x_axis_label, f_curve, f_label, v_dash, dot_a, a_label)
        self.wait(2.0)
        self.play(Create(lin_curve), FadeIn(lin_label), run_time=1.0)
        self.play(Create(err_bar), FadeIn(err_label), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(err_bar), FadeOut(err_label), FadeOut(lin_label), run_time=0.5)
        self.play(ReplacementTransform(lin_curve, quad_curve), FadeIn(quad_label), run_time=1.2)
        self.play(Create(err_bar2), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(err_bar2), FadeIn(final_formula), run_time=1.0)
        self.wait(3.0)

        # ---- numbers: how fast the error shrinks with h ----
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        def fmt(v, sig=4):
            return np.format_float_positional(v, precision=sig, unique=False, fractional=False, trim="-")

        head = MathTex(rf"f(1)={fmt(fa,4)},\ f'(1)={fmt(f1,3)},\ f''(1)={fmt(f2,3)}", font_size=MIN_FONT, color=V_COLOR)
        head.move_to(UP * 2.3)
        rows = []
        errs = []
        for h in (0.5, 0.1):
            ft = f_fn(a + h)
            li, qu = lin_fn(a + h), quad_fn(a + h)
            errs.append((abs(ft - li), abs(ft - qu)))
            r = MathTex(rf"h={h:g}:\ f({a+h:g})={fmt(ft,4)},\ \text{{lin}}={fmt(li,4)},\ \text{{quad}}={fmt(qu,4)}",
                        font_size=MIN_FONT)
            rows.append(r)
        rows[0].move_to(UP * 1.5)
        rows[1].move_to(UP * 0.8)
        # error table
        cx = [-3.7, -0.5, 3.0]
        h1 = MathTex(r"\text{linear error}\sim h^2", font_size=MIN_FONT, color=INK_DIM).move_to(RIGHT * cx[1] + DOWN * 0.1)
        h2 = MathTex(r"\text{quad error}\sim h^3", font_size=MIN_FONT, color=INK_DIM).move_to(RIGHT * cx[2] + DOWN * 0.1)
        h1.shift(LEFT * 0.0)
        cells = VGroup()
        for i, h in enumerate((0.5, 0.1)):
            y = -0.9 - 0.7 * i
            cells.add(MathTex(rf"h={h:g}", font_size=MIN_FONT, color=INK).move_to(RIGHT * cx[0] + UP * y))
            cells.add(MathTex(fmt(errs[i][0], 2), font_size=MIN_FONT, color=RESULT_COLOR).move_to(RIGHT * cx[1] + UP * y))
            cells.add(MathTex(fmt(errs[i][1], 2), font_size=MIN_FONT, color=RESULT_COLOR).move_to(RIGHT * cx[2] + UP * y))
        # sanity: shrinking h by 5 cuts the errors by about 5^2 and 5^3
        assert 20 < errs[0][0] / errs[1][0] < 35 and 70 < errs[0][1] / errs[1][1] < 160
        self.add(head)
        self.wait(1.5)
        self.play(FadeIn(rows[0]), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(rows[1]), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(h1), FadeIn(h2), FadeIn(cells[0:3]), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(cells[3:6]), run_time=1.0)
        self.wait(4.0)
