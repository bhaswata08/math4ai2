"""Block 3.2: variance, covariance and the covariance matrix, drawn as areas.

Idea after Normalized Nerd, "Covariance Clearly Explained!"; rebuilt in house
style. Every number on screen is computed here. Division is by m, as in the deck.
"""

from shared.anim.house import *

PTS = np.array([(-4, -1), (-1, 4), (2, 0), (5, 5), (9, 4), (13, 6)], dtype=float)
M = len(PTS)
XB, YB = PTS.mean(0)
DX, DY = PTS[:, 0] - XB, PTS[:, 1] - YB
VAR_X, VAR_Y = (DX**2).mean(), (DY**2).mean()
COV = (DX * DY).mean()
assert (XB, YB) == (4.0, 3.0) and np.isclose(VAR_X, 100 / 3) and np.isclose(VAR_Y, 20 / 3)
assert np.isclose(COV, 67 / 6) and np.isclose(COV / np.sqrt(VAR_X * VAR_Y), 0.75, atol=0.005)

SC = 0.42                  # scene units per data unit, both axes
X0, Y0 = -4.5 * SC, -1.61  # scene position of data (0, 0)
XR, YR = (-6, 15), (-2, 7)


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def P(x, y):
    return np.array([X0 + SC * x, Y0 + SC * y, 0])


def fmt(v):
    return f"{v:.2f}"


def plane_axes(xt=(5, 10, 15), yt=(5,)):
    g = VGroup()
    g.add(Line(P(XR[0], 0), P(XR[1], 0), color=INK_DIM, stroke_width=3))
    g.add(Line(P(0, YR[0]), P(0, YR[1]), color=INK_DIM, stroke_width=3))
    for v in xt:
        g.add(Line(P(v, 0.0) + DOWN * 0.07, P(v, 0.0) + UP * 0.07, color=INK_DIM, stroke_width=3))
        g.add(tex(str(v), INK_DIM).move_to(P(v, 0) + DOWN * 0.3))
    for v in yt:
        g.add(Line(P(0, v) + LEFT * 0.07, P(0, v) + RIGHT * 0.07, color=INK_DIM, stroke_width=3))
        g.add(tex(str(v), INK_DIM).move_to(P(0, v) + LEFT * 0.27))
    g.add(tex("x", INK_DIM).move_to(P(XR[1], 0) + UP * 0.3 + LEFT * 0.1))
    g.add(tex("y", INK_DIM).move_to(P(0, YR[1]) + RIGHT * 0.3))
    return g


def mean_lines(color):
    v = DashedLine(P(XB, YR[0]), P(XB, YR[1]), color=color, stroke_width=3, dash_length=0.12)
    h = DashedLine(P(XR[0], YB), P(XR[1], YB), color=color, stroke_width=3, dash_length=0.12)
    return v, h


def dots_at(arr, color=V_COLOR):
    return VGroup(*[Dot(P(x, y), radius=0.08, color=color) for x, y in arr])


class Variance1D(Scene):
    def construct(self):
        s = 0.38
        ly = -2.0

        def Q(x):
            return np.array([(x - 4.5) * s, ly, 0])

        line = VGroup(Line(Q(-6), Q(15), color=INK_DIM, stroke_width=3))
        for v in (-5, 0, 5, 10, 15):
            line.add(Line(Q(v) + DOWN * 0.07, Q(v) + UP * 0.07, color=INK_DIM, stroke_width=3))
            if v != 5:
                line.add(tex(str(v), INK_DIM).move_to(Q(v) + DOWN * 0.4))
        xs = PTS[:, 0]
        dots = VGroup(*[Dot(Q(x), radius=0.09, color=V_COLOR) for x in xs])
        self.add(line, dots)
        self.wait(1.2)

        # mean
        mv = DashedLine(Q(XB), Q(XB) + UP * 9 * s, color=HIGHLIGHT, stroke_width=3, dash_length=0.12)
        mk = Line(Q(XB) + DOWN * 0.12, Q(XB) + UP * 0.12, color=HIGHLIGHT, stroke_width=5)
        ml = tex(r"\bar x=%d" % XB, HIGHLIGHT).move_to(Q(XB) + DOWN * 0.4)
        self.play(Create(mv), FadeIn(mk), FadeIn(ml), run_time=0.8)
        self.wait(1.0)
        self.play(mv.animate.set_color(INK_DIM), mk.animate.set_color(INK_DIM),
                  ml.animate.set_color(INK_DIM), run_time=0.4)

        # deviations: left side and right side are disjoint, stagger by size
        order = {}
        for side in (-1, 1):
            idx = sorted([i for i in range(M) if np.sign(DX[i]) == side], key=lambda i: -abs(DX[i]))
            for k, i in enumerate(idx):
                order[i] = k
        segs = []
        for i in range(M):
            y = ly + 0.16 + 0.11 * order[i]
            segs.append(Line([Q(XB)[0], y, 0], [Q(xs[i])[0], y, 0], color=X_COLOR, stroke_width=6))
        for sg in segs:
            self.play(Create(sg), run_time=0.35, rate_func=smooth)
        self.wait(0.8)

        # squares
        sq, lab = [], []
        for i in range(M):
            d = abs(DX[i])
            r = Rectangle(width=d * s, height=d * s, stroke_color=X_COLOR, stroke_width=2,
                          fill_color=X_COLOR, fill_opacity=0.17)
            r.move_to([(Q(xs[i])[0] + Q(XB)[0]) / 2, ly + d * s / 2, 0])
            sq.append(r)
            lab.append(tex("%g" % d, INK).move_to([r.get_center()[0], r.get_top()[1] + 0.25, 0]))
        for i in np.argsort(-abs(DX)):
            self.play(GrowFromEdge(sq[i], DOWN), FadeIn(lab[i]), run_time=0.55)
        self.wait(1.2)
        self.play(*[FadeOut(x) for x in segs], run_time=0.3)

        tot = (DX**2).sum()
        f = MathTex(r"\mathrm{Var}(x)=\textstyle\frac1m\sum_i(x_i-\bar x)^2=\frac{%d}{%d}=" % (tot, M),
                    font_size=MIN_FONT, color=INK)
        val = tex(fmt(VAR_X), RESULT_COLOR)
        g = VGroup(f, val).arrange(RIGHT, buff=0.12).move_to([0, 2.4, 0])
        self.play(Write(f), run_time=1.4)
        self.play(FadeIn(val), run_time=0.5)
        self.wait(2.0)


class TwoVariances(Scene):
    def construct(self):
        ax = plane_axes()
        mv, mh = mean_lines(INK_DIM)
        yl = tex(r"\bar y=%d" % YB, INK_DIM).move_to(P(13.6, YB - 0.75))
        xl = tex(r"\bar x=%d" % XB, INK_DIM).move_to(P(XB + 2.5, YR[0] + 0.3))
        dots = dots_at(PTS)
        mirror = PTS.copy()
        mirror[:, 1] = 2 * YB - PTS[:, 1]

        def trend(arr):
            a, b = np.polyfit(arr[:, 0], arr[:, 1], 1)
            return Line(P(-5, a * -5 + b), P(14, a * 14 + b), color=RESULT_COLOR, stroke_width=4)

        tr = trend(PTS)
        tr_m = trend(mirror)
        self.add(ax, mv, mh, xl, yl, dots)
        self.wait(1.2)

        def stats(arr):
            return arr[:, 0].var(), arr[:, 1].var()

        vx, vy = stats(PTS)
        lx = tex(r"\mathrm{Var}(x)=", X_COLOR)
        ly = tex(r"\mathrm{Var}(y)=", Y_COLOR)
        nx = tex(fmt(vx), RESULT_COLOR)
        ny = tex(fmt(vy), RESULT_COLOR)
        rowx = VGroup(lx, nx).arrange(RIGHT, buff=0.12)
        rowy = VGroup(ly, ny).arrange(RIGHT, buff=0.12)
        rowx.move_to([3.1, 2.4, 0]).align_to([4.7, 0, 0], RIGHT)
        rowy.move_to([3.1, 1.8, 0]).align_to([4.7, 0, 0], RIGHT)
        self.play(FadeIn(rowx), run_time=0.6)
        self.wait(0.8)
        self.play(FadeIn(rowy), run_time=0.6)
        self.wait(0.8)
        self.play(Create(tr), run_time=0.8)
        self.wait(1.2)

        cap = VGroup(Tex("same variances,", font_size=MIN_FONT, color=INK),
                     Tex("opposite trend", font_size=MIN_FONT, color=INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cap.move_to([-2.9, 2.1, 0]).align_to([-4.75, 0, 0], LEFT)

        def new_nums(arr):
            a, b = stats(arr)
            assert np.isclose(a, vx) and np.isclose(b, vy)
            return (tex(fmt(a), RESULT_COLOR).move_to(nx, aligned_edge=LEFT),
                    tex(fmt(b), RESULT_COLOR).move_to(ny, aligned_edge=LEFT))

        def flip(target, tline):
            self.play(*[d.animate.move_to(P(*p)) for d, p in zip(dots, target)],
                      Transform(tr, tline), run_time=2.2, rate_func=smooth)
            a, b = new_nums(target)
            self.play(Transform(nx, a), Transform(ny, b), run_time=0.01)
            self.play(Indicate(nx, color=HIGHLIGHT, scale_factor=1.15),
                      Indicate(ny, color=HIGHLIGHT, scale_factor=1.15), run_time=1.0)

        flip(mirror, tr_m)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(cap), run_time=0.3)
        flip(PTS, trend(PTS))
        self.wait(2.0)


class CovarianceRectangles(Scene):
    def construct(self):
        ax = plane_axes()
        mv, mh = mean_lines(HIGHLIGHT)
        xl = tex(r"\bar x=%d" % XB, INK_DIM).move_to(P(XB + 2.5, YR[0] + 0.3))
        yl = tex(r"\bar y=%d" % YB, INK_DIM).move_to(P(13.6, YB - 0.75))
        dots = dots_at(PTS)
        mdot = Dot(P(XB, YB), radius=0.1, color=HIGHLIGHT)
        self.add(ax, mv, mh, dots, mdot)
        self.wait(1.0)
        self.play(FadeIn(xl), FadeIn(yl), mv.animate.set_color(INK_DIM), mh.animate.set_color(INK_DIM),
                  mdot.animate.set_color(INK_DIM), run_time=0.6)
        self.wait(0.6)

        # label spots for rectangles too thin or too small for their number (data coords)
        beside = {0: (-2.2, 1.0), 3: (5.4, 5.55)}
        prods = DX * DY
        segs_prev = None
        rects, labs = [], []
        for i in range(M):
            x, y = PTS[i]
            first = i == 0
            sx = Line(P(XB, YB), P(x, YB), color=X_COLOR, stroke_width=7)
            sy = Line(P(XB, YB), P(XB, y), color=Y_COLOR, stroke_width=7)
            pos = prods[i] > 0
            col = RESULT_COLOR if pos else W_COLOR
            rect = Polygon(P(XB, YB), P(x, YB), P(x, y), P(XB, y), stroke_color=col, stroke_width=2,
                           fill_color=col, fill_opacity=0.35)
            val = prods[i]
            lab = tex(("+" if pos else "-") + "%g" % abs(val), INK)
            w, h = abs(x - XB) * SC, abs(y - YB) * SC
            if i in beside:
                lab.move_to(P(*beside[i]))
            else:
                lab.move_to(rect.get_center())
            fade = [FadeOut(segs_prev)] if segs_prev is not None else []
            self.play(*fade, Create(sx), Create(sy), run_time=1.2 if first else 0.55)
            self.play(FadeIn(rect), run_time=0.9 if first else 0.4)
            self.play(FadeIn(lab), run_time=0.5 if first else 0.25)
            self.wait(1.5 if first else 0.8)
            segs_prev = VGroup(sx, sy)
            rects.append(rect)
            labs.append(lab)
        self.play(FadeOut(segs_prev), run_time=0.3)
        self.wait(0.6)

        tot = int(round(prods.sum()))
        assert tot == 67
        f = MathTex(r"\mathrm{Cov}(x,y)=\textstyle\frac1m\sum_i(x_i-\bar x)(y_i-\bar y)=\frac{%d}{%d}=" % (tot, M),
                    font_size=MIN_FONT, color=INK)
        val = tex(fmt(COV), RESULT_COLOR)
        g = VGroup(f, val).arrange(RIGHT, buff=0.12).move_to([0, 2.42, 0])
        self.play(Write(f), run_time=1.6)
        self.play(FadeIn(val), run_time=0.5)
        self.wait(1.2)
        cap = Tex("more amber area than violet: positive covariance", font_size=MIN_FONT, color=INK)
        cap.move_to([0, 1.86, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(2.0)


class CovarianceMorph(Scene):
    def construct(self):
        s = 0.6
        cx, cy = -2.2, 0.0

        def Q(x, y):
            return np.array([cx + s * x, cy + s * y, 0])

        def inv(p):
            return (p[0] - cx) / s, (p[1] - cy) / s

        k = np.arange(9)
        x = k - 4.0
        A = np.c_[x, 0.15 * (-1.0) ** k]
        B = np.c_[x, 0.75 * x]
        noise = np.array([1.2, -1.4, 0.5, -0.6, 1.5, -1.0, 0.9, -0.4, 0.3])
        yc = 0.5 * x + 1.4 * noise
        yc -= yc.mean()
        C = np.c_[x, yc]
        D = np.c_[x, -0.75 * x]
        ang = np.arange(8) * np.pi / 4 + np.pi / 8
        E = np.vstack([2.6 * np.c_[np.cos(ang), np.sin(ang)], [0.0, 0.0]])
        # arrange E so each point travels a sensible distance: sort by x like the lines
        E = E[np.argsort(E[:, 0] + 0.01 * E[:, 1])]

        def rho_of(a):
            return np.corrcoef(a[:, 0], a[:, 1])[0, 1]

        assert np.isclose(rho_of(B), 1) and np.isclose(rho_of(D), -1) and abs(rho_of(E)) < 1e-9
        assert 0.6 < rho_of(C) < 0.8, rho_of(C)
        print("rho C", rho_of(C), "max y", abs(C[:, 1]).max())

        L = 4.1
        ax = VGroup(Line(Q(-L, 0), Q(L, 0), color=INK_DIM, stroke_width=3),
                    Line(Q(0, -L), Q(0, L), color=INK_DIM, stroke_width=3))
        for v in (-4, 4):
            ax.add(tex(str(v), INK_DIM).move_to(Q(v, 0) + DOWN * 0.62))
        ax.add(tex("4", INK_DIM).move_to(Q(0, 4) + LEFT * 0.27))
        ax.add(tex("-4", INK_DIM).move_to(Q(0, -4) + LEFT * 0.37))
        dots = VGroup(*[Dot(Q(*p), radius=0.12, color=V_COLOR) for p in A])

        def data():
            return np.array([inv(d.get_center()) for d in dots])

        def live(fn, col, row_y, label_tex, label_col, sign=False):
            lab = tex(label_tex, label_col).move_to([3.0, row_y, 0]).align_to([3.0, 0, 0], RIGHT)
            num = DecimalNumber(0, num_decimal_places=2, include_sign=sign, font_size=MIN_FONT, color=col)
            num.move_to([3.1, row_y, 0], aligned_edge=LEFT)

            def upd(m):
                m.set_value(round(float(fn(data())), 2) + 0.0)

            num.add_updater(upd)
            num.update(0)
            return lab, num

        def cov(a):
            return ((a[:, 0] - a[:, 0].mean()) * (a[:, 1] - a[:, 1].mean())).mean()

        def rho(a):
            return cov(a) / np.sqrt(a[:, 0].var() * a[:, 1].var())

        r1 = live(lambda a: a[:, 0].var(), X_COLOR, 1.9, r"\mathrm{Var}(x)=", X_COLOR)
        r2 = live(lambda a: a[:, 1].var(), Y_COLOR, 1.1, r"\mathrm{Var}(y)=", Y_COLOR)
        r3 = live(cov, INK, 0.3, r"\mathrm{Cov}(x,y)=", INK, True)
        r4 = live(rho, RESULT_COLOR, -0.7, r"\rho=", RESULT_COLOR, True)
        fr = MathTex(r"=\frac{\mathrm{Cov}(x,y)}{\sigma_x\,\sigma_y}", font_size=MIN_FONT, color=RESULT_COLOR)
        fr.move_to([3.6, -1.7, 0]).align_to([4.8, 0, 0], RIGHT)
        for n in (r1[1], r2[1], r3[1], r4[1]):
            n.update(0)
        self.add(ax, dots, *[m for r in (r1, r2, r3, r4) for m in r], fr)
        self.wait(1.5)
        for tgt in (B, C, D, E):
            self.play(*[d.animate.move_to(Q(*p)) for d, p in zip(dots, tgt)], run_time=2.2, rate_func=smooth)
            self.wait(2.0)
        self.wait(0.8)
