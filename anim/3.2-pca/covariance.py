"""Block 3.2: signs of the products x1*x2 decide the sign of the covariance C_12."""

from pathlib import Path

from shared.anim.house import *

X = np.loadtxt(Path(__file__).parent / "data" / "cloud2d.csv", delimiter=",", comments="#")
M = len(X)
C = X.T @ X / M
assert M == 40 and np.allclose(C, [[3.25, 1.5], [1.5, 1.0]], atol=1e-6)


def sums(pts):
    pr = pts[:, 0] * pts[:, 1]
    return pr, pr[pr > 0].sum(), pr[pr < 0].sum()


PROD, S_POS, S_NEG = sums(X)
XF = X * np.array([1, -1])                 # reflected across the x1 axis
PROD_F, S_POS_F, S_NEG_F = sums(XF)
assert np.isclose((S_POS + S_NEG) / M, C[0, 1])
C12_F = (S_POS_F + S_NEG_F) / M
assert np.isclose(C12_F, -C[0, 1]) and np.isclose(S_POS_F, -S_NEG) and np.isclose(S_NEG_F, -S_POS)

SC = 0.7                      # scene units per data unit, same on both axes
ORG = np.array([-1.49, 0.0, 0])
XR, YR = (-4.8, 3.5), (-3.7, 3.7)   # shaded region in data units


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def P(x, y):
    return ORG + np.array([x * SC, y * SC, 0])


def sign_color(p):
    return X_COLOR if p > 0 else Y_COLOR


class CovarianceSigns(Scene):
    def construct(self):
        def quad(x0, x1, y0, y1, col):
            r = Rectangle(width=(x1 - x0) * SC, height=(y1 - y0) * SC, stroke_width=0,
                          fill_color=col, fill_opacity=0.13)
            r.move_to(P((x0 + x1) / 2, (y0 + y1) / 2))
            return r

        qs = VGroup(quad(0, XR[1], 0, YR[1], X_COLOR), quad(XR[0], 0, 0, YR[1], Y_COLOR),
                    quad(XR[0], 0, YR[0], 0, X_COLOR), quad(0, XR[1], YR[0], 0, Y_COLOR))
        plane = house_plane(x_range=[XR[0], XR[1], 1], y_range=[YR[0], YR[1], 1],
                            x_length=(XR[1] - XR[0]) * SC, y_length=(YR[1] - YR[0]) * SC)
        plane.move_to(P((XR[0] + XR[1]) / 2, (YR[0] + YR[1]) / 2))
        for l in list(plane.background_lines) + list(plane.faded_lines):
            l.set_stroke(opacity=0.35)
        d, dx = 0.35, 0.45
        signs = VGroup(
            tex("+", X_COLOR, 64).move_to(P(XR[1], YR[1]) + np.array([-dx, -d, 0])),
            tex("-", Y_COLOR, 64).move_to(P(XR[0], YR[1]) + np.array([dx, -d, 0])),
            tex("+", X_COLOR, 64).move_to(P(XR[0], YR[0]) + np.array([dx, d, 0])),
            tex("-", Y_COLOR, 64).move_to(P(XR[1], YR[0]) + np.array([-dx, d, 0])),
        )
        dots = VGroup(*[Dot(P(x, y), radius=0.07, color=V_COLOR) for x, y in X])
        mean = Circle(radius=0.13, color=HIGHLIGHT, stroke_width=4).move_to(P(0, 0))
        xl = tex("x_1", INK_DIM).move_to(P(XR[1], 0) + np.array([-0.3, -0.3, 0]))
        yl = tex("x_2", INK_DIM).move_to(P(0, YR[1]) + np.array([0.3, -0.3, 0]))
        mean_lab = Tex("mean", font_size=MIN_FONT, color=HIGHLIGHT).move_to(P(-2.0, 2.2))
        mean_arrow = Arrow(mean_lab.get_bottom() + RIGHT * 0.3, mean.get_top() + LEFT * 0.08, buff=0.08,
                           color=HIGHLIGHT, stroke_width=4, tip_length=0.15)

        self.add(qs, plane, dots, mean, xl, yl, signs)
        self.wait(1.2)
        self.play(FadeIn(mean_lab), FadeIn(mean_arrow), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(mean_lab), FadeOut(mean_arrow), run_time=0.4)

        # right panel
        RX = 3.0
        LX = 1.35
        lab_p = tex(r"S_+ =", X_COLOR).move_to([LX, 1.6, 0]).align_to([LX, 0, 0], LEFT)
        lab_n = tex(r"S_- =", Y_COLOR).move_to([LX, 0.8, 0]).align_to([LX, 0, 0], LEFT)
        tp, tn = ValueTracker(0), ValueTracker(0)
        num_p = DecimalNumber(0, num_decimal_places=1, font_size=MIN_FONT, color=X_COLOR, include_sign=False)
        num_n = DecimalNumber(0, num_decimal_places=1, font_size=MIN_FONT, color=Y_COLOR, include_sign=True)
        num_p.add_updater(lambda m: m.set_value(tp.get_value() + 1e-9).next_to(lab_p, RIGHT, buff=0.15))
        num_n.add_updater(lambda m: m.set_value(tn.get_value() - 1e-9).next_to(lab_n, RIGHT, buff=0.15))
        self.add(lab_p, num_p)
        num_p.update(0); num_n.update(0)

        pos = [i for i in range(M) if PROD[i] > 0]
        neg = [i for i in range(M) if PROD[i] < 0]
        self.play(*[dots[i].animate.set_color(X_COLOR) for i in pos],
                  tp.animate.set_value(S_POS), run_time=2.2, rate_func=smooth)
        self.wait(0.6)
        self.play(FadeIn(lab_n), FadeIn(num_n), run_time=0.4)
        self.play(*[dots[i].animate.set_color(Y_COLOR) for i in neg],
                  tn.animate.set_value(S_NEG), run_time=1.8, rate_func=smooth)
        self.wait(0.8)

        c12 = tex(r"C_{12}=\tfrac{1}{40}(S_++S_-)", RESULT_COLOR).move_to([RX, -0.25, 0])

        def c12_val(v):
            t = tex(r"= %s" % (f"{v:.2f}".replace("-", "-")), RESULT_COLOR)
            return t.next_to(c12, DOWN, buff=0.25).align_to(c12, LEFT)

        c12v = c12_val(C[0, 1])
        self.play(Write(c12), run_time=1.0)
        self.wait(0.5)
        self.play(Write(c12v), run_time=0.7)
        self.wait(1.5)

        # contrast: flip x2 -> -x2
        flip = tex(r"x_2 \to -x_2", HIGHLIGHT).move_to([RX, 2.3, 0])
        self.play(FadeIn(flip), run_time=0.4)
        self.play(*[dots[i].animate.move_to(P(*XF[i])).set_color(sign_color(PROD_F[i])) for i in range(M)],
                  tp.animate.set_value(S_POS_F), tn.animate.set_value(S_NEG_F),
                  FadeOut(c12v), run_time=2.2, rate_func=smooth)
        c12v_f = c12_val(C12_F)
        self.play(Write(c12v_f), run_time=0.6)
        self.wait(1.6)
        self.play(*[dots[i].animate.move_to(P(*X[i])).set_color(sign_color(PROD[i])) for i in range(M)],
                  tp.animate.set_value(S_POS), tn.animate.set_value(S_NEG),
                  FadeOut(c12v_f), FadeOut(flip), run_time=2.0, rate_func=smooth)
        c12v = c12_val(C[0, 1])
        self.play(Write(c12v), run_time=0.5)
        self.wait(1.0)

        # the matrix
        num_p.clear_updaters(); num_n.clear_updaters()
        self.play(FadeOut(VGroup(lab_p, lab_n, num_p, num_n, c12, c12v)), run_time=0.5)
        ents = [tex("%.2f" % C[i, j], INK if i == j else RESULT_COLOR) for i in range(2) for j in range(2)]
        mat = MobjectMatrix([ents[:2], ents[2:]], h_buff=1.1, v_buff=0.8, bracket_h_buff=0.2)
        cl = tex("C=", INK)
        grp = VGroup(cl, mat).arrange(RIGHT, buff=0.2).move_to([RX, 1.5, 0])
        self.play(FadeIn(grp), run_time=0.7)
        self.wait(0.8)
        l1 = Tex("diagonal: variances", font_size=MIN_FONT, color=INK).move_to([RX, -0.3, 0])
        l2 = Tex("off-diagonal:", font_size=MIN_FONT, color=RESULT_COLOR)
        l3 = Tex("covariance", font_size=MIN_FONT, color=RESULT_COLOR)
        l2.next_to(l1, DOWN, buff=0.3)
        l3.next_to(l2, DOWN, buff=0.2)
        self.play(FadeIn(l1), run_time=0.5)
        self.wait(0.8)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.5)
        self.wait(2.0)
