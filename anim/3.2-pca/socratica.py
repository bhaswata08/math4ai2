"""Block 3.2: covariance introduced the way Socratica does it in "Covariance Explained".

Storyline and visuals follow that video (Logan's three weeks, three scatter
shapes, two real return clouds, deviations above and below the mean, the 2x2
sign table, the formula read part by part); rebuilt in house style.
Return data: anim/3.2-pca/data/returns_2017_2018.csv (Yahoo Finance, adjusted close).
Every number on screen is computed here. Division is by m, as in the deck.
"""

from pathlib import Path

from shared.anim.house import *

STUDY = np.array([2, 5, 6], dtype=float)
SCORE = np.array([70, 90, 95], dtype=float)
SLEEP = np.array([8, 7, 6.5])

R = np.loadtxt(Path(__file__).parent / "data" / "returns_2017_2018.csv", delimiter=",",
               comments="#", usecols=(1, 2, 3, 4))
assert R.shape == (500, 4)


def cov(a, b):
    return ((a - a.mean()) * (b - b.mean())).mean()


COV_GM = cov(R[:, 0], R[:, 1])
COV_SV = cov(R[:, 2], R[:, 3])
assert COV_GM > 0 > COV_SV


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def txt(s, color=INK, size=MIN_FONT):
    return MathTex(r"\text{" + s + "}", font_size=size, color=color)


def panel(w, h, center):
    """Bottom-left axes of a w x h box; returns (axes group, point mapper from [0,1]^2)."""
    o = np.array(center) + np.array([-w / 2, -h / 2, 0])
    ax = VGroup(Line(o, o + RIGHT * w, color=INK_DIM, stroke_width=3),
                Line(o, o + UP * h, color=INK_DIM, stroke_width=3))
    return ax, lambda u, v: o + np.array([u * w, v * h, 0])


def norm01(a):
    return (a - a.min()) / (a.max() - a.min())


class LoganWeeks(Scene):
    def construct(self):
        cols = []
        for k in range(3):
            x = -3.3 + 3.3 * k
            head = txt(f"Week {k + 1}", INK).move_to([x, 2.4, 0])
            s1 = txt(f"studied {STUDY[k]:g} h", X_COLOR).move_to([x, 1.9, 0])
            s2 = txt(f"slept {SLEEP[k]:g} h", W_COLOR).move_to([x, 1.4, 0])
            base = np.array([x - 0.45, -2.6, 0])
            h = 3.2 * SCORE[k] / 100
            frame = Rectangle(width=0.55, height=3.2, color=INK_FAINT, stroke_width=2).move_to(base + UP * 1.6)
            bar = Rectangle(width=0.55, height=h, color=RESULT_COLOR, fill_opacity=0.85, stroke_width=0)
            bar.move_to(base + UP * h / 2)
            lab = txt(f"quiz {SCORE[k]:g}\\%", RESULT_COLOR).next_to(frame, RIGHT, buff=0.15).align_to(bar, UP)
            cols.append(VGroup(head, s1, s2, frame, bar, lab))
        self.add(cols[0][0], cols[0][1], cols[0][2], cols[0][3])
        for k, c in enumerate(cols):
            if k:
                self.play(FadeIn(c[0]), FadeIn(c[1]), FadeIn(c[2]), FadeIn(c[3]), run_time=0.7)
            self.play(GrowFromEdge(c[4], DOWN), FadeIn(c[5]), run_time=0.8)
            self.wait(0.8)
        self.wait(1.5)
        self.play(FadeOut(VGroup(*cols)))

        # the same numbers as lines over the weeks, each scaled to its own range
        charts = VGroup()
        specs = [(-2.5, STUDY, SCORE, "studied", "score", RESULT_COLOR, "rise together"),
                 (2.5, STUDY, SLEEP, "studied", "sleep", W_COLOR, "move opposite")]
        for cx, a, b, la, lb, cb, verdict in specs:
            ax, at = panel(3.6, 2.4, [cx, 0.15, 0])
            wk = VGroup(*[txt(f"wk {k + 1}", INK_DIM).move_to(at(k / 2, 0) + DOWN * 0.32) for k in range(3)])
            pa = [at(0.05 + 0.9 * k / 2, 0.08 + 0.84 * v) for k, v in enumerate(norm01(a))]
            pb = [at(0.05 + 0.9 * k / 2, 0.08 + 0.84 * v) for k, v in enumerate(norm01(b))]
            line_a = VMobject(color=X_COLOR, stroke_width=6).set_points_as_corners(pa)
            line_b = VMobject(color=cb, stroke_width=6).set_points_as_corners(pb)
            dots = VGroup(*[Dot(p, radius=0.07, color=X_COLOR) for p in pa],
                          *[Dot(p, radius=0.07, color=cb) for p in pb])
            key = VGroup(txt(la, X_COLOR), txt(lb, cb)).arrange(RIGHT, buff=0.45)
            key.next_to(ax, UP, buff=0.25)
            v = txt(verdict, INK).next_to(wk, DOWN, buff=0.25)
            charts.add(VGroup(ax, wk, key, line_a, line_b, dots, v))
        for c in charts:
            self.play(FadeIn(c[0]), FadeIn(c[1]), FadeIn(c[2]), run_time=0.7)
            self.play(Create(c[3]), Create(c[4]), FadeIn(c[5]), run_time=1.5)
            self.play(FadeIn(c[6]))
            self.wait(1.5)
        self.wait(2)


class ThreeShapes(Scene):
    def construct(self):
        rng = np.random.default_rng(3)
        u = rng.uniform(0.08, 0.92, 22)
        specs = [("positive", RESULT_COLOR, 0.1 + 0.8 * u + rng.normal(0, 0.07, 22)),
                 ("negative", W_COLOR, 0.9 - 0.8 * u + rng.normal(0, 0.07, 22)),
                 ("about 0", INK, rng.uniform(0.1, 0.9, 22))]
        axes = []
        for k, (name, col, v) in enumerate(specs):
            ax, at = panel(2.6, 2.6, [-3.3 + 3.3 * k, -0.45, 0])
            dots = VGroup(*[Dot(at(a, np.clip(b, 0.04, 0.96)), radius=0.06, color=col) for a, b in zip(u, v)])
            head = txt(name, col).next_to(ax, UP, buff=0.3)
            axes.append((ax, dots, head))
        self.add(*[a for a, _, _ in axes])
        for ax, dots, head in axes:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.05), run_time=1.4)
            self.wait(1)
        self.wait(2)


class ReturnClouds(Scene):
    def construct(self):
        specs = [(-2.6, 0, 1, "GOOG", "META", 5.0, 5.0, RESULT_COLOR, COV_GM),
                 (2.3, 2, 3, "SPY", "VIXY", 3.0, 12.0, W_COLOR, COV_SV)]
        title = txt("daily returns, 2017--2018: one dot per trading day", INK_DIM).to_edge(UP, buff=0.25)
        s = 1.5
        parts = []
        for cx, i, j, ni, nj, li, lj, col, c in specs:
            c0 = np.array([cx, -0.3, 0])
            ax = VGroup(Line(c0 + LEFT * s, c0 + RIGHT * s, color=INK_DIM, stroke_width=3),
                        Line(c0 + DOWN * s, c0 + UP * s, color=INK_DIM, stroke_width=3))
            keep = (np.abs(R[:, i]) < li) & (np.abs(R[:, j]) < lj)
            dots = VGroup(*[Dot(c0 + np.array([a / li * s, b / lj * s, 0]), radius=0.03, color=col)
                            for a, b in R[keep][:, [i, j]]])
            lx = txt(ni, INK_DIM).next_to(ax[0].get_end(), RIGHT, buff=0.12)
            ly = txt(nj, INK_DIM).next_to(ax[1].get_end(), UP, buff=0.08)
            sgn = 1 if c > 0 else -1
            band = Rectangle(width=2 * s * 1.3, height=0.75, stroke_width=0, fill_color=col, fill_opacity=0.18)
            band.rotate(sgn * PI / 4).move_to(c0)
            cv = tex(rf"\mathrm{{Cov}} = {c:+.2f}", col).next_to(ax, DOWN, buff=0.2)
            parts.append((ax, lx, ly, dots, band, cv))
        self.add(title, *[VGroup(p[0], p[1], p[2]) for p in parts])
        for ax, lx, ly, dots, band, cv in parts:
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.004), run_time=2)
            self.play(FadeIn(band), run_time=0.8)
            self.play(FadeIn(cv))
            self.wait(1.5)
        self.wait(2)


class DeviationSigns(Scene):
    def construct(self):
        BX = -3.6    # centre of the two strips
        DOTX = BX - 0.35
        BARX = BX - 0.8

        def strip(cy, name, col):
            box = Rectangle(width=2.5, height=1.6, color=INK_FAINT, stroke_width=2).move_to([BX, cy, 0])
            mean = DashedLine(box.get_left() + RIGHT * 0.1, box.get_right() + LEFT * 0.55,
                              color=INK_DIM, stroke_width=3, dash_length=0.1)
            ml = tex(r"\mu_" + name, INK_DIM).next_to(mean, RIGHT, buff=0.08)
            nm = tex(name, col).move_to(box.get_corner(UL) + np.array([0.25, -0.25, 0]))
            return VGroup(box, mean, ml, nm), cy

        gx, mx = strip(1.35, "x", X_COLOR)
        gy, my = strip(-0.75, "y", Y_COLOR)
        D = 0.5
        dx = Dot([DOTX, mx + D, 0], radius=0.11, color=X_COLOR)
        dy = Dot([DOTX, my + D, 0], radius=0.11, color=Y_COLOR)
        bx = Line([BARX, mx, 0], [BARX, mx + D, 0], color=X_COLOR, stroke_width=5)
        by = Line([BARX, my, 0], [BARX, my + D, 0], color=Y_COLOR, stroke_width=5)
        lx = tex(r"x_i-\mu_x", X_COLOR).move_to([BX + 0.5, mx - 0.48, 0])
        ly = tex(r"y_i-\mu_y", Y_COLOR).move_to([BX + 0.5, my - 0.48, 0])
        self.add(gx, gy, dx, dy)
        self.wait(0.5)
        self.play(Create(bx), Create(by), FadeIn(lx), FadeIn(ly))
        self.wait(1)

        # the 2x2 sign table
        cw, rh = 1.75, 0.62
        tl = np.array([-1.7, 2.55, 0])

        def cell(r, c):
            return tl + np.array([c * cw + cw / 2, -r * rh - rh / 2, 0])
        grid = VGroup()
        for r in range(4):
            grid.add(Line(tl + DOWN * r * rh, tl + DOWN * r * rh + RIGHT * 3 * cw, color=INK_FAINT, stroke_width=2))
        for c in range(4):
            grid.add(Line(tl + RIGHT * c * cw, tl + RIGHT * c * cw + DOWN * 3 * rh, color=INK_FAINT, stroke_width=2))
        heads = VGroup(txt("x above", X_COLOR).move_to(cell(1, 0)), txt("x below", X_COLOR).move_to(cell(2, 0)),
                       txt("y above", Y_COLOR).move_to(cell(0, 1)), txt("y below", Y_COLOR).move_to(cell(0, 2)))
        self.play(Create(grid), FadeIn(heads))
        signs = {(1, 1): "+", (1, 2): "-", (2, 1): "-", (2, 2): "+"}
        marks = {k: tex(v, RESULT_COLOR if v == "+" else W_COLOR, 56).move_to(cell(*k)) for k, v in signs.items()}

        # both above: + ; x above, y below: - ; both below: + ; x below, y above: -
        for k, ux, uy in [((1, 1), D, D), ((1, 2), D, -D), ((2, 2), -D, -D), ((2, 1), -D, D)]:
            ex, ey = mx + ux, my + uy
            self.play(dx.animate.move_to([DOTX, ex, 0]), dy.animate.move_to([DOTX, ey, 0]),
                      bx.animate.put_start_and_end_on([BARX, mx, 0], [BARX, ex, 0]),
                      by.animate.put_start_and_end_on([BARX, my, 0], [BARX, ey, 0]),
                      lx.animate.move_to([BX + 0.5, mx - np.sign(ux) * 0.48, 0]),
                      ly.animate.move_to([BX + 0.5, my - np.sign(uy) * 0.48, 0]), run_time=0.9)
            box = SurroundingRectangle(marks[k], color=HIGHLIGHT, buff=0.12)
            self.play(FadeIn(marks[k]), Create(box), run_time=0.6)
            self.play(FadeOut(box), run_time=0.3)
            self.wait(0.4)
        tog = txt("same side: $+$, together", RESULT_COLOR).next_to(grid, DOWN, buff=0.22).align_to(grid, LEFT)
        opp = txt("opposite sides: $-$, apart", W_COLOR).next_to(tog, DOWN, buff=0.12).align_to(grid, LEFT)
        self.play(FadeIn(tog), FadeIn(opp))
        self.wait(2)
        self.play(FadeOut(tog), FadeOut(opp))

        # the formula, read in three parts
        f = MathTex(r"\mathrm{Cov}(x,y)", r"=", r"\frac1m\sum_i", r"(x_i-\mu_x)", r"(y_i-\mu_y)",
                    font_size=MIN_FONT, color=INK)
        f[2].set_color(RESULT_COLOR)
        f[3].set_color(X_COLOR)
        f[4].set_color(Y_COLOR)
        f.move_to([1.15, -0.55, 0])
        self.play(FadeIn(f))
        # x deviation labelled above, the other two below, so no labels collide
        for part, word, col, d in [(f[3], "x deviation", X_COLOR, UP), (f[4], "y deviation", Y_COLOR, DOWN),
                                   (f[2], "average", RESULT_COLOR, DOWN)]:
            br = Brace(part, d, color=col, buff=0.05)
            w = txt(word, col).next_to(br, d, buff=0.05)
            self.play(GrowFromCenter(br), FadeIn(w), run_time=0.6)
        self.wait(2.5)
