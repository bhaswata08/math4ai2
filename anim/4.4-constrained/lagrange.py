# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (after 3Blue1Brown's Khan Academy Lagrange multiplier lessons)

from shared.anim.house import *
import numpy as np

LABEL_BG = dict(color=BG, opacity=0.85, buff=0.08)
R2 = np.sqrt(2.0)


def bg(m):
    m.add_background_rectangle(**LABEL_BG)
    return m


# =============================================================================
# SCENE 1: ConstraintWalk
# =============================================================================
class ConstraintWalk(Scene):
    def construct(self):
        S = 1.9
        C = np.array([-2.1, 0.0, 0.0])
        XL, YL = 1.3, 1.05

        def p(x, y):
            return C + S * np.array([x, y, 0.0])

        def contour_ends(c):
            x0 = max(-XL, c - YL)
            x1 = min(XL, c + YL)
            return p(x0, c - x0), p(x1, c - x1)

        contours = {}
        for c in (-1.0, 0.0, 1.0, R2):
            a, b = contour_ends(c)
            contours[c] = Line(a, b, color=INK_DIM, stroke_width=3.5, stroke_opacity=0.9)

        labels = VGroup()
        tex = {-1.0: r"-1", 0.0: r"0", 1.0: r"1", R2: r"\sqrt{2}"}
        lab = {}
        out = np.array([0.707, -0.707, 0.0])
        for c, line in contours.items():
            a, b = contour_ends(c)
            end = a if a[0] > b[0] else b  # lower-right end
            m = MathTex(tex[c], font_size=52, color=INK_DIM).move_to(end + 0.55 * out)
            bg(m)
            lab[c] = m
            labels.add(m)

        circle = Circle(radius=S, color=W_COLOR, stroke_width=6).move_to(C)

        # right-hand panel
        row_f = MathTex(r"f = x + y", font_size=57)
        row_f[0][0].set_color(V_COLOR)
        row_g = MathTex(r"x^2 + y^2 = 1", font_size=57, color=W_COLOR)
        legend = VGroup(row_f, row_g).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        legend.move_to([3.1, 1.25, 0])

        th = ValueTracker(-3 * np.pi / 4)

        def fval():
            t = th.get_value()
            return np.cos(t) + np.sin(t)

        def pt():
            t = th.get_value()
            return p(np.cos(t), np.sin(t))

        dot = Dot(radius=0.13, color=V_COLOR)
        dot.add_updater(lambda m: m.move_to(pt()))

        f_lab = MathTex(r"f =", font_size=57, color=V_COLOR)
        f_lab.move_to([2.2, -0.5, 0])
        num = DecimalNumber(fval(), num_decimal_places=2, font_size=57, color=V_COLOR,
                            include_sign=False)
        num.add_updater(lambda m: m.set_value(fval()).next_to(f_lab, RIGHT, buff=0.2))
        num.next_to(f_lab, RIGHT, buff=0.2)

        self.add(*contours.values(), labels, circle, legend, f_lab, num, dot)
        self.wait(1.5)
        self.play(th.animate.set_value(np.pi / 4 - 0.0), run_time=9.5, rate_func=smooth)
        dot.clear_updaters()
        num.clear_updaters()
        dot.move_to(p(1 / R2, 1 / R2))
        self.play(
            dot.animate.set_color(RESULT_COLOR).scale(1.35),
            contours[R2].animate.set_color(RESULT_COLOR).set_stroke(width=6),
            lab[R2][1].animate.set_color(RESULT_COLOR),
            Flash(dot.get_center(), color=HIGHLIGHT, flash_radius=0.4, line_length=0.18),
            run_time=1.0,
        )
        fmax = MathTex(r"\text{max } f = \sqrt{2}", font_size=57, color=RESULT_COLOR)
        fmax.move_to([3.1, -0.5, 0])
        self.play(FadeOut(f_lab, num), FadeIn(fmax), run_time=0.8)
        self.wait(2.5)


# =============================================================================
# SCENE 2: TangencyGradients
# =============================================================================
class TangencyGradients(Scene):
    def construct(self):
        S = 1.9
        K = 0.72
        C = np.array([-2.5, -0.62, 0.0])

        def unit(t):
            return np.array([np.cos(t), np.sin(t), 0.0])

        th = ValueTracker(np.radians(10))

        def P():
            return C + S * unit(th.get_value())

        def gf():
            return K * np.array([1.0, 1.0, 0.0])

        def gg():
            return K * 2 * unit(th.get_value())

        circle = Circle(radius=S, color=W_COLOR, stroke_width=6).move_to(C)

        def tangent():
            t = th.get_value()
            d = np.array([-np.sin(t), np.cos(t), 0.0])
            return DashedLine(P() - 1.35 * d, P() + 1.35 * d, color=INK_DIM, stroke_width=3.5,
                              dash_length=0.12)

        tan_line = always_redraw(tangent)

        def tan_part():
            t = th.get_value()
            d = np.array([-np.sin(t), np.cos(t), 0.0])
            amp = float(np.dot(gf(), d))
            if abs(amp) < 0.04:
                return VGroup()
            return Line(P(), P() + amp * d, color=RESULT_COLOR, stroke_width=14, stroke_opacity=0.45)

        tan_bar = always_redraw(tan_part)

        def arrow(vec, color, stroke):
            return Arrow(P(), P() + vec, buff=0, color=color, stroke_width=stroke, tip_length=0.28,
                         max_tip_length_to_length_ratio=0.35)

        arr_f = always_redraw(lambda: arrow(gf(), RESULT_COLOR, 6))
        arr_g = always_redraw(lambda: arrow(gg(), W_COLOR, 10))

        def lab_f():
            v = gf()
            d = v / np.linalg.norm(v)
            n = np.array([-d[1], d[0], 0.0])
            m = MathTex(r"\nabla f", font_size=52, color=RESULT_COLOR)
            m.move_to(P() + v + 0.42 * d + 0.5 * n)
            return bg(m)

        def lab_g():
            v = gg()
            d = v / np.linalg.norm(v)
            n = np.array([-d[1], d[0], 0.0])
            m = MathTex(r"\nabla g", font_size=52, color=W_COLOR)
            m.move_to(P() + v + 0.42 * d - 0.5 * n)
            return bg(m)

        lf = always_redraw(lab_f)
        lg = always_redraw(lab_g)

        dot = Dot(P(), radius=0.13, color=V_COLOR)
        dot.add_updater(lambda m: m.move_to(P()))

        eq1 = MathTex(r"\nabla f", r"\not\parallel", r"\nabla g", font_size=52)
        eq1[0].set_color(RESULT_COLOR)
        eq1[2].set_color(W_COLOR)
        eq1.move_to([3.3, 0.2, 0])

        self.add(circle, tan_line, dot)
        self.wait(1.0)
        self.play(FadeIn(arr_g), FadeIn(arr_f), FadeIn(lf), FadeIn(lg), FadeIn(eq1), run_time=1.2)
        self.add(tan_bar)
        self.wait(2.5)
        self.play(th.animate.set_value(np.pi / 4), run_time=5, rate_func=smooth)
        dot.clear_updaters()
        self.wait(0.5)
        eq2 = MathTex(r"\nabla f", r"=\lambda\,", r"\nabla g", font_size=52)
        eq2[0].set_color(RESULT_COLOR)
        eq2[2].set_color(W_COLOR)
        eq2.move_to(eq1)
        self.play(
            TransformMatchingTex(eq1, eq2),
            dot.animate.set_color(RESULT_COLOR),
            Flash(P(), color=HIGHLIGHT, flash_radius=0.4, line_length=0.18),
            run_time=1.4,
        )
        self.wait(3.0)


# =============================================================================
# SCENE 3: LagrangeSystem
# =============================================================================
def colour_parts(m, spec):
    for i, col in spec.items():
        m[i].set_color(col)
    return m


class LagrangeSystem(Scene):
    def construct(self):
        FS = 76
        # Step A: two rows
        a1 = MathTex(r"\nabla f", r"=", r"\lambda\,", r"\nabla g", font_size=FS)
        colour_parts(a1, {0: RESULT_COLOR, 3: W_COLOR})
        a2 = MathTex(r"g", r"=", r"1", font_size=FS)
        colour_parts(a2, {0: W_COLOR})
        A = VGroup(a1, a2).arrange(DOWN, buff=0.6)

        # Step B: three rows
        b1 = MathTex(r"1", r"=", r"2\lambda x", font_size=FS)
        b2 = MathTex(r"1", r"=", r"2\lambda y", font_size=FS)
        b3 = MathTex(r"x^2 + y^2", r"=", r"1", font_size=FS)
        colour_parts(b3, {0: W_COLOR})
        B = VGroup(b1, b2, b3).arrange(DOWN, buff=0.6)

        # Step C
        c1 = MathTex(r"x = y = 1/\sqrt{2}", font_size=FS, color=RESULT_COLOR)
        c2 = MathTex(r"\lambda = 1/\sqrt{2}", font_size=FS, color=RESULT_COLOR)
        c3 = MathTex(r"\text{max } f = \sqrt{2}", font_size=FS, color=RESULT_COLOR)
        C = VGroup(c1, c2, c3).arrange(DOWN, buff=0.6)

        # Step D
        d1 = MathTex(r"\mathcal{L}(x, y, \lambda)", r"=", r"f", r"-", r"\lambda\,(", r"g", r"- 1)",
                     font_size=64)
        d1[0].set_color(RESULT_COLOR)
        d1[2].set_color(V_COLOR)
        d1[5].set_color(W_COLOR)
        d2 = MathTex(r"\nabla \mathcal{L} = \mathbf{0}", r"\text{ gives the same equations}",
                     font_size=52)
        d2[0].set_color(RESULT_COLOR)
        D = VGroup(d1, d2).arrange(DOWN, buff=0.6)

        self.add(a1, a2)
        A.move_to(ORIGIN)
        self.wait(2.0)
        B.move_to(ORIGIN)
        self.play(
            TransformMatchingTex(a1.copy(), b2),
            TransformMatchingTex(a1, b1),
            TransformMatchingTex(a2, b3),
            run_time=2.0,
        )
        self.wait(3.0)
        C.move_to(ORIGIN)
        self.play(FadeOut(B), FadeIn(c1), FadeIn(c2), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(c3), run_time=0.8)
        self.wait(2.5)
        D.move_to(ORIGIN)
        self.play(FadeOut(C), run_time=0.8)
        self.play(FadeIn(d1), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(d2), run_time=1.0)
        self.wait(3.0)


# =============================================================================
# SCENE 4: ConvexVsNot
# =============================================================================
class ConvexVsNot(Scene):
    def construct(self):
        SX, SY = 1.8, 0.46

        def sp(x, y):
            return np.array([SX * x, -1.6 + (y + 1.6) * SY, 0.0])

        def f_convex(x):
            return 0.9 * x * x - 1.5

        def df_convex(x):
            return 1.8 * x

        def f_non(x):
            return 0.25 * x ** 4 - x * x + 0.35 * x

        def df_non(x):
            return x ** 3 - 2 * x + 0.35

        def curve(f):
            return ParametricFunction(lambda t: sp(t, f(t)), t_range=[-2.5, 2.5], color=V_COLOR,
                                      stroke_width=6)

        def flow(df, x0, lr, T, n=400):
            xs = [x0]
            dt = T / n
            for _ in range(n):
                xs.append(xs[-1] - lr * df(xs[-1]) * dt)
            return np.array(xs)

        starts = [-2.2, 0.6, 2.2]

        def balls_for(f):
            bs = VGroup(*[Dot(radius=0.15, color=RESULT_COLOR).move_to(sp(x, f(x))) for x in starts])
            return bs

        def run(balls, f, paths, T):
            n = len(paths[0]) - 1

            def upd(mob, alpha):
                k = int(round(alpha * n))
                for b, path in zip(mob, paths):
                    x = path[k]
                    b.move_to(sp(x, f(x)))
            return UpdateFromAlphaFunc(balls, upd, run_time=T, rate_func=linear)

        # --- convex phase
        c_curve = curve(f_convex)
        c_balls = balls_for(f_convex)
        self.add(c_curve, c_balls)
        self.wait(3.0)
        paths_c = [flow(df_convex, x, 0.35, 7.0) for x in starts]
        self.play(run(c_balls, f_convex, paths_c, 7.0))
        self.wait(1.5)

        # --- non-convex phase
        n_curve = curve(f_non)
        n_balls = balls_for(f_non)
        cap = VGroup(
            MathTex(r"\text{convex problem:}", font_size=48),
            MathTex(r"\text{every local minimum is global}", font_size=48),
        ).arrange(DOWN, buff=0.2).move_to([0, 1.9, 0])
        self.play(FadeOut(c_balls), ReplacementTransform(c_curve, n_curve), FadeIn(cap), run_time=1.5)
        self.play(FadeIn(n_balls), run_time=0.8)
        self.wait(1.0)
        paths_n = [flow(df_non, x, 0.45, 7.0) for x in starts]
        self.play(run(n_balls, f_non, paths_n, 7.0))
        xg, xl = -1.4907, 1.3135
        glob = MathTex(r"\text{global}", font_size=52, color=RESULT_COLOR)
        glob.move_to(sp(xg, f_non(xg)) + DOWN * 0.45)
        loc = MathTex(r"\text{local}", font_size=52, color=INK_DIM)
        loc.move_to(sp(xl, f_non(xl)) + DOWN * 0.45)
        self.play(FadeIn(glob), FadeIn(loc), run_time=0.8)
        self.wait(2.0)
        self.wait(4.0)
