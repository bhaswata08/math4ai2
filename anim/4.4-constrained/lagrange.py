# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (after 3Blue1Brown's Khan Academy Lagrange multiplier lessons)

from shared.anim.house import *
import numpy as np

LABEL_BG = dict(color=BG, opacity=0.85, buff=0.08)
R2 = np.sqrt(2.0)


def bg(m):
    m.add_background_rectangle(**LABEL_BG)
    return m


# =============================================================================
# Shared geometry for the Act 1 pair (same frame, so the second continues the first)
# =============================================================================
S_W = 1.8
C_W = np.array([-2.55, -0.3, 0.0])
XL, YL = 1.25, 1.0


def wp(x, y):
    return C_W + S_W * np.array([x, y, 0.0])


def unit(t):
    return np.array([np.cos(t), np.sin(t), 0.0])


def contour_ends(c):
    """End points (unit coordinates) of the line x + y = c clipped to the picture box."""
    x0 = max(-XL, c - YL)
    x1 = min(XL, c + YL)
    return wp(x0, c - x0), wp(x1, c - x1)


def contour_line(c, **kw):
    a, b = contour_ends(c)
    return Line(a, b, **kw)


# =============================================================================
# SCENE 1: ConstraintWalk
# =============================================================================
class ConstraintWalk(Scene):
    def construct(self):
        th = ValueTracker(0.0)

        def fval():
            t = th.get_value()
            return float(np.cos(t) + np.sin(t))

        def pt():
            t = th.get_value()
            return wp(np.cos(t), np.sin(t))

        # thin teal contours f = c, one label each, placed at a distinct free spot
        cs = (-1.0, 0.0, 1.0, R2)
        tex = {-1.0: r"c=-1", 0.0: r"c=0", 1.0: r"c=1", R2: r"c=\sqrt{2}"}
        contours = VGroup(*[contour_line(c, color=V_COLOR, stroke_width=2.5, stroke_opacity=0.8)
                            for c in cs])
        labels = VGroup()
        for c in cs:
            a, b = contour_ends(c)
            hi, lo = (a, b) if a[1] > b[1] else (b, a)  # upper-left end, lower-right end
            m = MathTex(tex[c], font_size=40, color=V_COLOR)
            if c == 1.0:
                m.next_to(hi, UP, buff=0.12)
            elif c in (R2, 0.0):
                m.next_to(lo, RIGHT, buff=0.12)
            else:
                m.next_to(lo, DOWN, buff=0.12)
            labels.add(bg(m))

        circle = Circle(radius=S_W, color=W_COLOR, stroke_width=6).move_to(C_W)

        gold = always_redraw(lambda: contour_line(fval(), color=HIGHLIGHT, stroke_width=7))
        dot = Dot(pt(), radius=0.13, color=V_COLOR)
        dot.add_updater(lambda m: m.move_to(pt()))

        row_f = MathTex(r"f = x + y", font_size=57)
        row_f[0][0].set_color(V_COLOR)
        row_g = MathTex(r"x^2 + y^2 = 1", font_size=57, color=W_COLOR)
        legend = VGroup(row_f, row_g).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        legend.move_to([2.7, 1.25, 0])

        f_lab = MathTex(r"f =", font_size=57, color=V_COLOR).move_to([2.0, -0.45, 0])
        num = DecimalNumber(fval(), num_decimal_places=2, font_size=57, color=V_COLOR)
        num.add_updater(lambda m: m.set_value(fval()).next_to(f_lab, RIGHT, buff=0.2))
        num.next_to(f_lab, RIGHT, buff=0.2)

        self.add(contours, labels, circle, gold, legend, f_lab, num, dot)
        self.wait(2.0)
        # clockwise once past the minimum, up to the maximum (-315 degrees = +45 degrees)
        self.play(th.animate.set_value(-7 * np.pi / 4), run_time=10, rate_func=smooth)
        dot.clear_updaters()
        num.clear_updaters()
        assert abs(fval() - R2) < 1e-9
        num.set_value(R2)
        dot.move_to(wp(1 / R2, 1 / R2))
        self.wait(1.5)  # hold the peak value before the tangent appears
        touch = MathTex(r"\text{touches the circle}", font_size=44, color=RESULT_COLOR)
        touch.move_to([2.7, -1.5, 0])
        self.play(
            dot.animate.set_color(RESULT_COLOR).scale(1.35),
            gold.animate.set_color(RESULT_COLOR),
            Flash(dot.get_center(), color=HIGHLIGHT, flash_radius=0.4, line_length=0.18),
            FadeIn(touch),
            run_time=1.0,
        )
        self.wait(2.5)


# =============================================================================
# SCENE 2: TangencyGradients
# =============================================================================
class TangencyGradients(Scene):
    def construct(self):
        K = 0.62
        th = ValueTracker(np.radians(-30))
        gf_v = np.array([1.0, 1.0, 0.0])

        def P():
            return wp(*unit(th.get_value())[:2])

        def gg_v():
            return 2 * unit(th.get_value())

        def angle_deg():
            a, b = gf_v[:2], gg_v()[:2]
            cosv = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            return float(np.degrees(np.arccos(np.clip(cosv, -1, 1))))

        def fval():
            t = th.get_value()
            return float(np.cos(t) + np.sin(t))

        circle = Circle(radius=S_W, color=W_COLOR, stroke_width=6).move_to(C_W)
        contours = VGroup(*[contour_line(c, color=V_COLOR, stroke_width=2.5, stroke_opacity=0.55)
                            for c in (-1.0, 0.0, 1.0, R2)])
        gold = always_redraw(lambda: contour_line(fval(), color=HIGHLIGHT, stroke_width=7))

        def arrow(vec, color, stroke):
            return Arrow(P(), P() + K * vec, buff=0, color=color, stroke_width=stroke,
                         tip_length=0.28, max_tip_length_to_length_ratio=0.35)

        arr_f = always_redraw(lambda: arrow(gf_v, RESULT_COLOR, 6))
        arr_g = always_redraw(lambda: arrow(gg_v(), W_COLOR, 10))

        def lab(tex_, vec, color, side):
            v = K * vec
            d = v / np.linalg.norm(v)
            n = np.array([-d[1], d[0], 0.0])
            m = MathTex(tex_, font_size=48, color=color)
            m.move_to(P() + v + 0.45 * d + side * 0.5 * n)
            return bg(m)

        lf = always_redraw(lambda: lab(r"\nabla f", gf_v, RESULT_COLOR, 1))
        lg = always_redraw(lambda: lab(r"\nabla g", gg_v(), W_COLOR, -1))

        dot = Dot(P(), radius=0.13, color=V_COLOR)
        dot.add_updater(lambda m: m.move_to(P()))

        f_lab = MathTex(r"f =", font_size=57, color=V_COLOR).move_to([1.9, 2.0, 0])
        f_num = DecimalNumber(fval(), num_decimal_places=2, font_size=57, color=V_COLOR)
        f_num.add_updater(lambda m: m.set_value(fval()).next_to(f_lab, RIGHT, buff=0.2))
        f_num.next_to(f_lab, RIGHT, buff=0.2)

        a_lab = MathTex(r"\text{angle} =", font_size=57).move_to([2.5, 1.0, 0])
        a_num = DecimalNumber(angle_deg(), num_decimal_places=0, unit=r"^\circ", font_size=57)
        a_num.add_updater(lambda m: m.set_value(angle_deg()).next_to(a_lab, RIGHT, buff=0.2))
        a_num.next_to(a_lab, RIGHT, buff=0.2)
        a_sub = MathTex(r"\nabla f\text{ vs }\nabla g", font_size=40, color=INK_DIM)
        a_sub.next_to(a_lab, DOWN, buff=0.3, aligned_edge=LEFT)

        self.add(contours, circle, gold, arr_g, arr_f, lf, lg, f_lab, f_num, a_lab, a_num,
                 a_sub, dot)
        self.wait(2.5)
        self.play(th.animate.set_value(np.pi / 4), run_time=7, rate_func=smooth)
        dot.clear_updaters()
        f_num.clear_updaters()
        a_num.clear_updaters()
        self.wait(1.5)

        # lambda: ratio of the two gradient lengths, computed
        lam = float(np.linalg.norm(gf_v) / np.linalg.norm(gg_v()))
        assert abs(lam - 1 / R2) < 1e-9 and angle_deg() < 1e-6
        eq = MathTex(r"\nabla f", r"=", r"\lambda\,", r"\nabla g", font_size=57)
        eq[0].set_color(RESULT_COLOR)
        eq[3].set_color(W_COLOR)
        lam_eq = MathTex(rf"\lambda = {lam:.2f}", font_size=57, color=RESULT_COLOR)
        VGroup(eq, lam_eq).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([2.9, 0.4, 0]).align_to([1.3, 0, 0], LEFT)
        self.play(FadeOut(a_lab, a_num, a_sub), run_time=0.6)
        self.play(
            FadeIn(eq),
            dot.animate.set_color(RESULT_COLOR),
            Flash(P(), color=HIGHLIGHT, flash_radius=0.4, line_length=0.18),
            run_time=1.2,
        )
        self.wait(1.0)
        self.play(FadeIn(lam_eq), run_time=0.8)
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
        S, K = 1.7, 0.6
        C = np.array([-2.6, 0.0, 0.0])
        th = ValueTracker(np.radians(-30))
        gf_v = np.array([1.0, 1.0, 0.0])

        def P():
            return C + S * unit(th.get_value())

        def gg_v():
            return 2 * unit(th.get_value())

        circle = Circle(radius=S, color=W_COLOR, stroke_width=6).move_to(C)

        def arrow(vec, color, stroke):
            return Arrow(P(), P() + K * vec, buff=0, color=color, stroke_width=stroke,
                         tip_length=0.26, max_tip_length_to_length_ratio=0.35)

        arr_f = always_redraw(lambda: arrow(gf_v, RESULT_COLOR, 6))
        arr_g = always_redraw(lambda: arrow(gg_v(), W_COLOR, 10))

        def lab(tex_, vec, color, side):
            v = K * vec
            d = v / np.linalg.norm(v)
            n = np.array([-d[1], d[0], 0.0])
            m = MathTex(tex_, font_size=44, color=color)
            m.move_to(P() + v + 0.42 * d + side * 0.45 * n)
            return bg(m)

        lf = always_redraw(lambda: lab(r"\nabla f", gf_v, RESULT_COLOR, 1))
        lg = always_redraw(lambda: lab(r"\nabla g", gg_v(), W_COLOR, -1))
        dot = Dot(P(), radius=0.12, color=V_COLOR)
        dot.add_updater(lambda m: m.move_to(P()))
        pl = MathTex(r"P", font_size=44, color=V_COLOR)
        pl.add_updater(lambda m: m.move_to(P() - 0.42 * unit(th.get_value())))
        pl.move_to(P() - 0.42 * unit(th.get_value()))
        axes_hint = MathTex(r"x^2+y^2=1", font_size=40, color=W_COLOR).move_to(C + [0, -S - 0.5, 0])

        FS = 52
        X0 = 0.9  # left edge of the equation column

        def left(m, y):
            m.move_to([0, y, 0])
            m.align_to([X0, 0, 0], LEFT)
            return m

        r1 = left(MathTex(r"\nabla f", r"=", r"(1,\ 1)", font_size=FS), 1.7)
        colour_parts(r1, {0: RESULT_COLOR})
        r2 = left(MathTex(r"\nabla g", r"=", r"(2x,\ 2y)", font_size=FS), 0.9)
        colour_parts(r2, {0: W_COLOR})
        r3 = left(MathTex(r"\nabla f", r"=", r"\lambda\,", r"\nabla g", font_size=FS), 0.1)
        colour_parts(r3, {0: RESULT_COLOR, 3: W_COLOR})
        e1 = left(MathTex(r"1", r"=", r"2\lambda x", font_size=FS, color=X_COLOR), 0.1)
        e2 = left(MathTex(r"1", r"=", r"2\lambda y", font_size=FS, color=Y_COLOR), -0.7)
        e3 = left(MathTex(r"x^2 + y^2", r"=", r"1", font_size=FS, color=W_COLOR), -1.5)
        tags = VGroup(
            left(MathTex(r"x\text{-part}", font_size=40, color=X_COLOR), 0.1),
            left(MathTex(r"y\text{-part}", font_size=40, color=Y_COLOR), -0.7),
            left(MathTex(r"\text{constraint}", font_size=40, color=W_COLOR), -1.5),
        )
        for t in tags:
            t.shift(RIGHT * 2.3)
        # (tags kept off-screen if they do not fit: see assert)

        self.add(circle, arr_g, arr_f, lf, lg, axes_hint, dot, pl)
        self.wait(2.0)

        # 1. gradients, each next to its arrow
        self.play(FadeIn(r1), Indicate(arr_f, color=HIGHLIGHT, scale_factor=1.0), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(r2), Indicate(arr_g, color=HIGHLIGHT, scale_factor=1.0), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(r3), run_time=1.0)
        self.wait(2.0)

        # 2. components and the constraint
        self.play(FadeOut(r3), run_time=0.5)
        self.play(FadeIn(e1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(e2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(e3), Indicate(circle, color=HIGHLIGHT, scale_factor=1.0), run_time=1.2)
        self.wait(1.5)

        # 3. solve
        self.play(FadeOut(r1, r2, e1, e2, e3), run_time=0.7)
        s1 = left(MathTex(r"\text{divide:}\ x = y", font_size=FS), 1.6)
        s2 = left(MathTex(r"\text{so}\ 2x^2 = 1", font_size=FS), 0.6)
        s3 = left(MathTex(r"x = y = \tfrac{1}{\sqrt{2}}", font_size=FS, color=RESULT_COLOR), -0.4)
        s4 = left(MathTex(r"\lambda = \tfrac{1}{\sqrt{2}}", font_size=FS, color=RESULT_COLOR), -1.3)
        s5 = left(MathTex(r"\max f = \sqrt{2}", font_size=FS, color=RESULT_COLOR), -2.2)
        self.play(FadeIn(s1), run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(s2), run_time=0.9)
        self.wait(1.5)
        # numeric check of the algebra
        x = 1 / R2
        assert abs(2 * x * x - 1) < 1e-12 and abs(1 / (2 * x) - 1 / R2) < 1e-12
        assert abs(2 * x - R2) < 1e-12
        self.play(FadeIn(s3), th.animate.set_value(np.pi / 4), run_time=3.0, rate_func=smooth)
        self.wait(1.0)
        self.play(FadeIn(s4), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(s5), Flash(P(), color=HIGHLIGHT, flash_radius=0.35, line_length=0.15),
                  run_time=0.9)
        self.wait(2.0)


# =============================================================================
# SCENE 4: LambdaIsPrice
# =============================================================================
class LambdaIsPrice(Scene):
    def construct(self):
        U = 1.7  # screen units per unit of side
        BL = np.array([-3.2, -1.3, 0.0])  # bottom-left corner, fixed
        Pt = ValueTracker(4.0)

        def best(P):
            return P / 4.0, (P / 4.0) ** 2   # side of the best rectangle, its area

        def rect():
            s, _ = best(Pt.get_value())
            r = Rectangle(width=U * s, height=U * s, stroke_color=W_COLOR, stroke_width=6,
                          fill_color=V_COLOR, fill_opacity=0.3)
            return r.move_to(BL + np.array([U * s / 2, U * s / 2, 0]))

        sq = always_redraw(rect)
        ghost = Rectangle(
            width=U, height=U, stroke_color=INK_FAINT, stroke_width=3
        ).move_to(BL + np.array([U / 2, U / 2, 0]))

        def xlab():
            s, _ = best(Pt.get_value())
            m = MathTex(rf"x = {s:.2f}", font_size=40, color=X_COLOR)
            return m.next_to(BL + np.array([U * s / 2, 0, 0]), DOWN, buff=0.15)

        def ylab():
            s, _ = best(Pt.get_value())
            m = MathTex(rf"y = {s:.2f}", font_size=40, color=Y_COLOR)
            return m.next_to(BL + np.array([0, U * s / 2, 0]), LEFT, buff=0.15)

        xl = always_redraw(xlab)
        yl = always_redraw(ylab)

        X0 = -0.9
        p_lab = MathTex(r"P =", font_size=57, color=W_COLOR)
        p_num = DecimalNumber(4.0, num_decimal_places=1, font_size=57, color=W_COLOR)
        a_lab = MathTex(r"A =", font_size=57, color=V_COLOR)
        a_num = DecimalNumber(1.0, num_decimal_places=2, font_size=57, color=V_COLOR)
        p_lab.move_to([X0 + 0.4, 2.2, 0])
        a_lab.move_to([X0 + 0.4, 1.4, 0])
        p_num.add_updater(lambda m: m.set_value(Pt.get_value()).next_to(p_lab, RIGHT, buff=0.2))
        a_num.add_updater(lambda m: m.set_value(best(Pt.get_value())[1]).next_to(a_lab, RIGHT, buff=0.2))
        p_num.next_to(p_lab, RIGHT, buff=0.2)
        a_num.next_to(a_lab, RIGHT, buff=0.2)

        self.add(ghost, sq, xl, yl, p_lab, p_num, a_lab, a_num)
        self.wait(2.0)
        self.play(Pt.animate.set_value(4.4), run_time=3.0, rate_func=smooth)
        p_num.clear_updaters()
        a_num.clear_updaters()
        self.wait(1.5)

        # numbers, all computed
        P0, P1 = 4.0, 4.4
        dA = best(P1)[1] - best(P0)[1]
        dP = P1 - P0
        h = 1e-6
        lam = (best(P0 + h)[1] - best(P0 - h)[1]) / (2 * h)  # dA*/dP at P = 4
        pred = lam * dP
        assert abs(dA - 0.21) < 1e-9 and abs(lam - 0.5) < 1e-6 and abs(pred - 0.2) < 1e-6
        l1 = MathTex(rf"\Delta A = {dA:.2f}", font_size=52, color=V_COLOR)
        l2 = MathTex(rf"\lambda\,\Delta P = {lam:.1f} \times {dP:.1f} = {pred:.2f}",
                     font_size=46, color=RESULT_COLOR)
        l1.move_to([X0 + 1.4, 0.4, 0]).align_to([X0, 0, 0], LEFT)
        l2.move_to([X0 + 1.4, -0.3, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(l1), run_time=0.9)
        self.wait(1.5)
        self.play(FadeIn(l2), run_time=0.9)
        self.wait(2.0)
        t1 = MathTex(r"\lambda = 0.5", font_size=57, color=RESULT_COLOR)
        t2 = MathTex(r"\text{area gained per unit of }P", font_size=40)
        t3 = MathTex(r"\text{the shadow price of }P", font_size=40, color=INK_DIM)
        T = VGroup(t1, t2, t3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        T.move_to([X0 + 2.0, -1.55, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(T), run_time=1.0)
        self.wait(2.5)
