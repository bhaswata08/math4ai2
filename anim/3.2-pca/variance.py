"""Block 3.2: captured variance versus reconstruction error, and keeping the top direction.

CapturedVsLost: a unit direction p rotates; every point splits into its
projection (amber foot) and residual (violet). captured + lost = tr C.
KeepTopK: drop p2, slide points onto the p1 line, read them as one number each.
"""

from pathlib import Path

from shared.anim.house import *

X = np.loadtxt(Path(__file__).parent / "data" / "cloud2d.csv", delimiter=",", skiprows=1)
M = len(X)
C = X.T @ X / M
LAM, VEC = np.linalg.eigh(C)
LAM, VEC = LAM[::-1], VEC[:, ::-1]
P1, P2 = VEC[:, 0], VEC[:, 1]
if P1[0] < 0:
    P1 = -P1
if P2[1] < 0:
    P2 = -P2
TR = float(np.trace(C))
assert np.allclose(LAM, [4, 0.25], atol=1e-4) and abs(TR - 4.25) < 1e-4
TH1 = float(np.degrees(np.arctan2(P1[1], P1[0])))  # 26.57


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def unit(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a)])


def captured(p):
    return float(p @ C @ p)


def lost(p):
    r = X - np.outer(X @ p, p)
    return float((r ** 2).sum() / M)


def faint_axes(origin, length_x, length_y):
    return VGroup(
        Line(origin + LEFT * length_x, origin + RIGHT * length_x),
        Line(origin + DOWN * length_y, origin + UP * length_y),
    ).set_stroke(INK_FAINT, 2, opacity=0.6)


class CapturedVsLost(Scene):
    def construct(self):
        SC = 0.63
        O = np.array([-1.7, 0.0, 0.0])
        XL, XR, YM = -4.65, 0.6, 2.55  # left panel clip box for the line

        def reach(d):
            ts = []
            if abs(d[0]) > 1e-9:
                ts.append(((XR if d[0] > 0 else XL) - O[0]) / d[0])
            if abs(d[1]) > 1e-9:
                ts.append(YM / abs(d[1]))
            return min(ts)
        th = ValueTracker(90.0)

        def P(v):
            return O + np.array([v[0], v[1], 0.0]) * SC

        def foot(i):
            p = unit(th.get_value())
            return P(np.dot(X[i], p) * p)

        axes = VGroup(Line([XL, 0, 0], [XR, 0, 0]), Line(O + DOWN * YM, O + UP * YM)).set_stroke(INK_FAINT, 2, opacity=0.6)
        line = Line(O, O + RIGHT)
        line.set_stroke(RESULT_COLOR, 3, opacity=0.55)
        line.add_updater(lambda m: m.put_start_and_end_on(
            O - reach(-unit(th.get_value())) * np.append(unit(th.get_value()), 0),
            O + reach(unit(th.get_value())) * np.append(unit(th.get_value()), 0)))
        arrow = Arrow(O, O + RIGHT * SC, buff=0, color=RESULT_COLOR, stroke_width=7,
                      tip_length=0.16, max_tip_length_to_length_ratio=0.5)
        arrow.add_updater(lambda m: m.put_start_and_end_on(
            O, O + SC * np.append(unit(th.get_value()), 0)))
        plab = tex(r"\mathbf p", RESULT_COLOR)

        def place_plab(m):
            d = unit(th.get_value())
            n = np.array([-d[1], d[0]])
            e = -d  # label at the far end of the line, away from the cloud's tail
            m.move_to(O + np.append(e * (reach(e) - 0.4) + n * 0.62, 0))

        plab.add_updater(place_plab)

        segs, feet, dots = [], [], []
        for i in range(M):
            s = Line(ORIGIN, RIGHT).set_stroke(W_COLOR, 2.5, opacity=0.9)
            s.add_updater(lambda m, i=i: m.put_start_and_end_on(
                P(X[i]), foot(i) + 1e-6 * RIGHT))
            f = Dot(radius=0.045, color=RESULT_COLOR)
            f.add_updater(lambda m, i=i: m.move_to(foot(i)))
            d = Dot(P(X[i]), radius=0.05, color=V_COLOR)
            segs.append(s); feet.append(f); dots.append(d)
        for g in segs + feet + [line, arrow, plab]:
            g.update()
        segs_g, feet_g, dots_g = VGroup(*segs), VGroup(*feet), VGroup(*dots)

        # right panel
        H, BX = 4.4, 1.3
        TOT = H
        amber = Rectangle(width=0.6, height=1, stroke_width=0, fill_color=RESULT_COLOR, fill_opacity=1)
        viol = Rectangle(width=0.6, height=1, stroke_width=0, fill_color=W_COLOR, fill_opacity=1)

        def bars(_=None):
            p = unit(th.get_value())
            ha = max(captured(p) / TR * H, 1e-3)
            hv = max(H - ha, 1e-3)
            amber.stretch_to_fit_height(ha).move_to([BX, -H / 2 + ha / 2, 0])
            viol.stretch_to_fit_height(hv).move_to([BX, -H / 2 + ha + hv / 2, 0])

        bars()
        amber.add_updater(bars)
        outline = Rectangle(width=0.6, height=H, stroke_color=INK_DIM, stroke_width=2).move_to([BX, 0, 0])

        TX = 1.95

        def row(label, color, fn, y):
            lab = tex(r"\text{%s}" % label, color)
            num = DecimalNumber(fn(unit(90.0)), num_decimal_places=2, font_size=MIN_FONT, color=color)
            lab.move_to([TX, y, 0], aligned_edge=LEFT)
            num.move_to([TX + 1.85, y, 0], aligned_edge=LEFT)
            num.add_updater(lambda m: m.set_value(fn(unit(th.get_value()))).set_color(color))
            return lab, num

        cl, cn = row("captured", RESULT_COLOR, captured, 1.5)
        ll, ln = row("lost", W_COLOR, lost, 0.1)
        # keep number columns steady: fix left edge after each set_value
        for n in (cn, ln):
            n.edge_to_fix = LEFT
        rule = Line([TX, -1.0, 0], [TX + 2.75, -1.0, 0]).set_stroke(INK_DIM, 2)
        tl = tex(r"\text{total}", INK).move_to([TX, -1.7, 0], aligned_edge=LEFT)
        tn = DecimalNumber(captured(unit(90)) + lost(unit(90)), num_decimal_places=2,
                           font_size=MIN_FONT, color=INK).move_to([TX + 1.85, -1.7, 0], aligned_edge=LEFT)
        tn.add_updater(lambda m: m.set_value(captured(unit(th.get_value())) + lost(unit(th.get_value()))))
        assert abs(tn.get_value() - TR) < 1e-6

        self.add(axes, segs_g, line, feet_g, dots_g, arrow, plab,
                 outline, amber, viol, cl, cn, ll, ln, rule, tl, tn)
        self.wait(3.5)
        # sweep through p2 (worst) round to p1 (best); line is the same at theta and theta+180
        th2 = float(np.degrees(np.arctan2(P2[1], P2[0])))  # 116.57
        self.play(th.animate.set_value(th2), run_time=6, rate_func=smooth)
        self.wait(2)
        self.play(th.animate.set_value(TH1 + 180), run_time=8, rate_func=smooth)
        th.set_value(TH1)
        self.wait(0.5)
        assert abs(captured(unit(th.get_value())) - LAM[0]) < 1e-3
        self.play(Flash(arrow.get_end(), color=HIGHLIGHT, flash_radius=0.4), Indicate(cn, color=HIGHLIGHT, scale_factor=1.12),
                  run_time=1.2)
        e1 = tex(r"=\lambda_1", RESULT_COLOR).move_to([TX + 0.85, 0.8, 0], aligned_edge=LEFT)
        e2 = tex(r"=\lambda_2", W_COLOR).move_to([TX + 0.85, -0.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(e1), FadeIn(e2), run_time=1)
        self.wait(2.5)


class KeepTopK(Scene):
    def construct(self):
        SC = 0.8
        O = np.array([0.5, 0.0, 0.0])

        def P(v):
            return O + np.array([v[0], v[1], 0.0]) * SC

        alpha = X @ P1
        feet_pts = [P(a * P1) for a in alpha]
        L1 = max(abs(alpha.max()), abs(alpha.min())) * SC + 0.25
        L2 = 2.45
        axes = faint_axes(O, 3.9, 2.55)
        l1 = Line(O - L1 * np.append(P1, 0), O + L1 * np.append(P1, 0)).set_stroke(RESULT_COLOR, 3, opacity=0.8)
        l2 = Line(O - L2 * np.append(P2, 0), O + L2 * np.append(P2, 0)).set_stroke(W_COLOR, 3, opacity=0.8)
        n1 = np.array([-P1[1], P1[0], 0])
        lab1 = tex(r"\mathbf p_1", RESULT_COLOR).move_to(O + L1 * np.append(P1, 0) + n1 * 0.45 + RIGHT * 0.0)
        lab1.shift(LEFT * 0.35 + DOWN * 0.0)
        lab2 = tex(r"\mathbf p_2", W_COLOR).move_to(O + L2 * np.append(P2, 0) + np.array([-0.55, -0.1, 0]))
        dots = VGroup(*[Dot(P(x), radius=0.05, color=V_COLOR) for x in X])
        self.add(axes, l1, l2, dots, lab1, lab2)
        self.wait(2.5)

        # drop p2
        self.play(FadeOut(l2), FadeOut(lab2), FadeOut(axes), run_time=1.2)
        self.wait(0.5)
        # slide each point along its perpendicular onto the p1 line
        segs = VGroup(*[
            Line(P(X[i]), feet_pts[i] + 1e-6 * RIGHT).set_stroke(W_COLOR, 2.5, opacity=0.9)
            for i in range(M)])
        self.play(FadeIn(segs), run_time=0.8)
        self.wait(0.5)
        for i, s in enumerate(segs):
            s.add_updater(lambda m, i=i: m.put_start_and_end_on(dots[i].get_center(), feet_pts[i] + 1e-6 * RIGHT))
        self.play(*[dots[i].animate.move_to(feet_pts[i]) for i in range(M)], run_time=3, rate_func=smooth)
        for s in segs:
            s.clear_updaters()
        self.play(FadeOut(segs), run_time=0.5)
        self.wait(1)

        # rotate the p1 line to horizontal and turn it into a number line
        ang = np.arctan2(P1[1], P1[0])
        line_grp = VGroup(l1, dots)
        self.play(FadeOut(lab1), Rotate(line_grp, -ang, about_point=O), run_time=3)
        # axis from -5..4 in data units, centred on screen
        lo, hi = -5, 4
        shift = np.array([-(lo + hi) / 2 * SC - O[0], 0.15 - O[1], 0])
        ticks = VGroup()
        nums = VGroup()
        for v in range(lo, hi + 1):
            x = O[0] + v * SC
            ticks.add(Line([x, -0.09, 0], [x, 0.09, 0]).set_stroke(INK_DIM, 3))
            t = tex(str(v) if v >= 0 else r"-%d" % -v, INK_DIM, 40).move_to([x, -0.45, 0])
            nums.add(t)
        nl = Line(O + (lo - 0.3) * SC * RIGHT, O + (hi + 0.3) * SC * RIGHT).set_stroke(INK_DIM, 3)
        new_l = nl
        self.play(FadeOut(l1), FadeIn(nl), FadeIn(ticks), FadeIn(nums), line_grp.animate.shift(shift * 0),
                  run_time=1.2)
        grp = VGroup(nl, ticks, nums, dots)
        self.play(grp.animate.shift(shift).scale(1.25, about_point=np.array([0, 0.15, 0])), run_time=1.4)
        self.wait(0.5)

        # labels: one example point, shape of the new data, and the variance kept
        k = int(np.argsort(np.abs(alpha - 1.2))[0])
        hi_dot = Dot(dots[k].get_center(), radius=0.09, color=HIGHLIGHT)
        al = tex(r"\alpha_{i1}", HIGHLIGHT).move_to(dots[k].get_center() + UP * 0.75)
        pointer = Line(al.get_bottom() + DOWN * 0.05, dots[k].get_center() + UP * 0.14).set_stroke(HIGHLIGHT, 2.5)
        top = tex(r"\hat X_1 = X\mathbf p_1 \in \mathbb R^{m\times 1}", RESULT_COLOR).move_to([0, 2.15, 0])
        self.play(FadeIn(top), FadeIn(hi_dot), FadeIn(al), FadeIn(pointer), run_time=1.2)
        self.wait(1.5)
        kept = captured(P1)
        bot = tex(r"\text{kept }%.2f\,/\,%.2f = %.1f\%%" % (kept, TR, 100 * kept / TR), RESULT_COLOR)
        bot.move_to([0, -1.95, 0])
        self.play(FadeIn(bot), run_time=1)
        self.wait(2.5)
