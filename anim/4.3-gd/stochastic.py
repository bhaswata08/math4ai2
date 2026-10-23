# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (mini-batch layout after 3b1b/videos _2017/nn/part3.py)
# Stochastic part of the gradient-descent block: why a mini-batch gradient is
# noisy, three paths on one bowl, loss curves per update and per epoch, and a
# shrinking step size.

from shared.anim.house import *
import numpy as np


# =============================================================================
# Shared data: linear regression with N = 64 and Hessian diag(1, 8)
# =============================================================================
N_PTS = 64


def bowl_data():
    rng = np.random.default_rng(42)
    x_raw = rng.standard_normal(N_PTS)
    x = (x_raw - np.mean(x_raw)) / np.std(x_raw) * np.sqrt(0.125)
    y = rng.standard_normal(N_PTS) * 0.02
    return x, y


def bowl_grad(w, idx, x, y):
    diff = w[0] * x[idx] + w[1] - y[idx]
    return np.array([8.0 * np.mean(diff * x[idx]), 8.0 * np.mean(diff)])


def bowl_loss(w):
    return 0.5 * w[0] ** 2 + 4.0 * w[1] ** 2


def run_variant(kind, n_updates, eta, w_start):
    """kind: 'batch' (B=64), 'mini' (B=16), 'sgd' (B=1). Returns the path."""
    x, y = bowl_data()
    seeds = {"batch": 0, "mini": 101, "sgd": 202}
    rng = np.random.default_rng(seeds[kind])
    w = np.array(w_start, dtype=float)
    path = [w.copy()]
    for _ in range(n_updates):
        if kind == "batch":
            idx = np.arange(N_PTS)
        elif kind == "mini":
            idx = rng.choice(N_PTS, size=16, replace=False)
        else:
            idx = np.array([rng.choice(N_PTS)])
        w = w - eta * bowl_grad(w, idx, x, y)
        path.append(w.copy())
    return np.array(path)


def bowl_contours(axes, levels):
    """Full ellipses of L = w1^2/2 + 4 w2^2 in axes coordinates (never cropped)."""
    mobs = []
    opacities = np.linspace(0.05, 0.22, len(levels))
    for lvl, opac in zip(levels, opacities):
        a = np.sqrt(2.0 * lvl)
        b = np.sqrt(lvl / 4.0)
        sx = abs(axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0])
        sy = abs(axes.c2p(0, 1)[1] - axes.c2p(0, 0)[1])
        mobs.append(Ellipse(width=2 * a * sx, height=2 * b * sy,
                            stroke_color=INK_DIM, stroke_width=1.5,
                            fill_color=V_COLOR, fill_opacity=opac
                            ).move_to(axes.c2p(0, 0)))
    return VGroup(*mobs)


def legend_row(label, color, dashed=False, width=0.5):
    if dashed:
        line = DashedLine(ORIGIN, RIGHT * width, color=color, stroke_width=4, dash_length=0.1)
    else:
        line = Line(ORIGIN, RIGHT * width, color=color, stroke_width=4)
    txt = MathTex(label, font_size=MIN_FONT, color=color)
    return VGroup(line, txt).arrange(RIGHT, buff=0.15)


# =============================================================================
# SCENE: WhyNoise
# =============================================================================
class WhyNoise(Scene):
    def construct(self):
        # ---- data: 24 points around y = x + 0.5, fixed seed
        n = 24
        rng = np.random.default_rng(1)
        px = np.clip(rng.standard_normal(n) * 0.8, -1.8, 1.8)
        py = 1.0 * px + 0.5 + 0.4 * rng.standard_normal(n)
        w = np.array([0.4, -0.2])          # current slope and intercept
        res = w[0] * px + w[1] - py          # residual of every point
        G = np.stack([res * px, res], axis=1)   # single-point gradients
        g_full = G.mean(axis=0)

        # typical error of a batch gradient, over many random batches
        rr = np.random.default_rng(7)
        err1 = np.sqrt(np.mean(np.sum((G - g_full) ** 2, axis=1)))
        err8 = np.sqrt(np.mean([np.sum((G[rr.choice(n, 8, replace=False)].mean(0) - g_full) ** 2)
                                for _ in range(4000)]))

        # which points to show
        ang = np.arctan2(G[:, 1], G[:, 0]) - np.arctan2(g_full[1], g_full[0])
        ang = (ang + np.pi) % (2 * np.pi) - np.pi
        i_a = int(np.argmax(ang)); i_b = int(np.argmin(ang))
        i_c = int(np.argmax(np.linalg.norm(G, axis=1)))
        singles = [i_a, i_b] + ([i_c] if i_c not in (i_a, i_b) else [])
        batch8 = np.random.default_rng(3).choice(n, 8, replace=False)
        g_b8 = G[batch8].mean(axis=0)

        # ---- left: scatter and line
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-2.8, 3.2, 1], x_length=4.4, y_length=4.2,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
                  tips=False).move_to(np.array([-2.6, 0.4, 0]))
        lx = MathTex(r"x", font_size=MIN_FONT, color=INK_DIM).next_to(ax.x_axis.get_end(), UP, buff=0.1)
        ly = MathTex(r"y", font_size=MIN_FONT, color=INK_DIM).next_to(ax.y_axis.get_end(), RIGHT, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(px[i], py[i]), radius=0.07, color=V_COLOR) for i in range(n)])
        line = Line(ax.c2p(-2.2, w[0] * -2.2 + w[1]), ax.c2p(2.2, w[0] * 2.2 + w[1]),
                    color=INK, stroke_width=4)

        # ---- right: gradient panel
        gr = 1.9
        gx = Axes(x_range=[-gr, gr, 1], y_range=[-gr, gr, 1], x_length=4.2, y_length=4.2,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
                  tips=False).move_to(np.array([2.6, 0.4, 0]))
        glx = MathTex(r"g_1", font_size=MIN_FONT, color=INK_DIM).next_to(gx.x_axis.get_end(), UP, buff=0.1)
        gly = MathTex(r"g_2", font_size=MIN_FONT, color=INK_DIM).next_to(gx.y_axis.get_end(), RIGHT, buff=0.1)
        ticks = VGroup()
        for v in (-1, 1):
            for axis_i, pos in ((0, gx.c2p(v, 0)), (1, gx.c2p(0, v))):
                t = MathTex(str(v), font_size=MIN_FONT, color=INK_DIM)
                t.next_to(pos, DOWN if axis_i == 0 else LEFT, buff=0.08)
                t.add_background_rectangle(color=BG, opacity=0.85, buff=0.03)
                ticks.add(t, Line(pos + (UP if axis_i == 0 else RIGHT) * 0.06,
                                  pos - (UP if axis_i == 0 else RIGHT) * 0.06,
                                  color=INK_DIM, stroke_width=2))

        def garrow(g, color, width=6, dashed=False):
            end = gx.c2p(g[0], g[1])
            if dashed:
                a = DashedLine(gx.c2p(0, 0), end, color=color, stroke_width=width, dash_length=0.12)
                a.add_tip(tip_length=0.2, tip_width=0.2)
                return a
            return Arrow(gx.c2p(0, 0), end, buff=0, color=color, stroke_width=width,
                         tip_length=0.2, max_tip_length_to_length_ratio=0.5)

        full_arrow = garrow(g_full, RESULT_COLOR, 8)

        # ---- legend and statistic strip
        lg_full = legend_row(r"\nabla L", RESULT_COLOR)
        lg_one = legend_row(r"B{=}1", W_COLOR)
        lg_eight = legend_row(r"B{=}8", RESULT_COLOR, dashed=True)
        lg_mean = legend_row(r"\text{mean of 24}", INK, dashed=True)
        legend = VGroup(lg_full, lg_one, lg_eight).arrange(RIGHT, buff=0.7).move_to(np.array([0.0, -2.0, 0]))
        stat = MathTex(r"\text{error: }", r"B{=}1", r"\to", f"{err1:.2f}", r",\;", r"B{=}8", r"\to", f"{err8:.2f}",
                       font_size=MIN_FONT, color=INK_DIM)
        stat[1].set_color(W_COLOR); stat[3].set_color(W_COLOR)
        stat[5].set_color(RESULT_COLOR); stat[7].set_color(RESULT_COLOR)
        stat.move_to(np.array([0.0, -2.5, 0]))

        print('maxnorm',np.abs(G).max(0),g_full)
        self.add(ax, lx, ly, dots, line, gx, glx, gly, ticks, full_arrow, lg_full)
        self.wait(2.0)

        # ---- single points
        faint = []
        first = True
        for i in singles:
            ring = Circle(radius=0.17, color=W_COLOR, stroke_width=4).move_to(ax.c2p(px[i], py[i]))
            foot = ax.c2p(px[i], w[0] * px[i] + w[1])
            resid = DashedLine(ax.c2p(px[i], py[i]), foot, color=W_COLOR, stroke_width=4, dash_length=0.08)
            arr = garrow(G[i], W_COLOR, 6)
            self.play(dots[i].animate.set_color(W_COLOR), Create(ring), Create(resid), run_time=0.7)
            anims = [GrowArrow(arr)]
            if first:
                anims.append(FadeIn(lg_one))
                first = False
            self.play(*anims, run_time=0.9)
            self.wait(1.2)
            self.play(FadeOut(ring), FadeOut(resid), dots[i].animate.set_color(V_COLOR),
                      arr.animate.set_opacity(0.3), run_time=0.5)
            faint.append(arr)

        # ---- batch of 8
        rings = VGroup(*[Circle(radius=0.17, color=W_COLOR, stroke_width=4).move_to(ax.c2p(px[i], py[i]))
                         for i in batch8])
        self.play(*[dots[i].animate.set_color(W_COLOR) for i in batch8], Create(rings), run_time=0.8)
        thin = VGroup(*[garrow(G[i], W_COLOR, 3) for i in batch8]).set_opacity(0.6)
        self.play(*[GrowArrow(a) for a in thin], run_time=1.0)
        self.wait(0.8)
        mean_arrow = garrow(g_b8, RESULT_COLOR, 7, dashed=True)
        self.play(FadeOut(thin), Create(mean_arrow), FadeIn(lg_eight), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(rings), *[dots[i].animate.set_color(V_COLOR) for i in batch8], run_time=0.5)
        # unbiasedness: all 24 single-point arrows, their mean is the full gradient
        allarr = VGroup(*[garrow(G[i], W_COLOR, 3) for i in range(n)]).set_opacity(0.5)
        self.play(FadeOut(mean_arrow), *[a.animate.set_opacity(0) for a in faint], run_time=0.5)
        self.play(*[GrowArrow(a) for a in allarr], run_time=1.0)
        self.wait(0.8)
        mean_all = garrow(G.mean(axis=0), INK, 5, dashed=True)
        lg_mean.move_to(legend.get_center())
        self.play(FadeOut(allarr), FadeOut(legend), Create(mean_all), FadeIn(lg_mean), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(mean_all), FadeOut(lg_mean), run_time=0.4)
        self.play(FadeIn(legend), *[a.animate.set_opacity(0.3) for a in faint], FadeIn(mean_arrow), run_time=0.5)
        self.play(FadeIn(stat), run_time=0.6)
        self.wait(2.5)


# =============================================================================
# SCENE: BatchVsSGD
# =============================================================================
class BatchVsSGD(Scene):
    def construct(self):
        scale = 1.0
        axes = Axes(
            x_range=[-4.8, 4.8, 1.0], y_range=[-1.7, 1.7, 1.0],
            x_length=9.6 * scale, y_length=3.4 * scale,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
            tips=False,
        ).move_to(np.array([0.0, -0.85, 0.0]))

        lbl_w1 = MathTex(r"w_1", font_size=MIN_FONT, color=INK_DIM)
        lbl_w1.next_to(axes.x_axis.get_end(), UP, buff=0.08)
        lbl_w2 = MathTex(r"w_2", font_size=MIN_FONT, color=INK_DIM)
        lbl_w2.next_to(axes.y_axis.get_end(), RIGHT, buff=0.1)

        contours = bowl_contours(axes, [0.4, 1.2, 2.5, 4.5, 7.0, 9.5])
        min_dot = Dot(axes.c2p(0, 0), radius=0.07, color=V_COLOR)

        w_start = np.array([-3.5, 1.2])
        n_updates = 40
        eta = 0.05
        path_b = run_variant("batch", n_updates, eta, w_start)
        path_mb = run_variant("mini", n_updates, eta, w_start)
        path_sgd = run_variant("sgd", n_updates, eta, w_start)
        for p in (path_b, path_mb, path_sgd):
            assert abs(p[:, 0]).max() < 4.6 and abs(p[:, 1]).max() < 1.6

        # legend with updates per epoch (N = 64, B = 16)
        legend = VGroup(
            legend_row(r"\text{Batch: } 1", RESULT_COLOR),
            legend_row(r"\text{Mini-batch: } N/B = 4", W_COLOR),
            legend_row(r"\text{SGD: } N = 64", Y_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        hdr = MathTex(r"\text{updates per epoch}", font_size=MIN_FONT, color=INK_DIM)
        legend = VGroup(hdr, legend).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        legend.move_to(np.array([-4.8 + legend.width / 2, 1.75, 0]))
        legend.shift(UP * 0)

        start_dot = Dot(axes.c2p(*w_start), radius=0.09, color=INK)
        lbl_w0 = MathTex(r"\mathbf{w}_0", font_size=MIN_FONT, color=INK)
        lbl_w0.next_to(axes.c2p(*w_start), LEFT, buff=0.28)

        dot_b = Dot(axes.c2p(*w_start), radius=0.09, color=RESULT_COLOR)
        dot_mb = Dot(axes.c2p(*w_start), radius=0.08, color=W_COLOR)
        dot_sgd = Dot(axes.c2p(*w_start), radius=0.08, color=Y_COLOR)

        self.add(contours, axes, lbl_w1, lbl_w2, min_dot, start_dot, lbl_w0, legend)
        self.wait(1.5)

        segs = VGroup()
        self.add(segs)
        for k in range(n_updates):
            new = []
            # draw order: SGD, mini-batch, then batch on top
            for path, col, wd in ((path_sgd, Y_COLOR, 3.5), (path_mb, W_COLOR, 3.5), (path_b, RESULT_COLOR, 4.5)):
                new.append(Line(axes.c2p(*path[k]), axes.c2p(*path[k + 1]), color=col, stroke_width=wd))
            segs.add(*new)
            dot_sgd.move_to(axes.c2p(*path_sgd[k + 1]))
            dot_mb.move_to(axes.c2p(*path_mb[k + 1]))
            dot_b.move_to(axes.c2p(*path_b[k + 1]))
            self.add(dot_sgd, dot_mb, dot_b)
            self.wait(0.2)
        self.wait(2.5)


# =============================================================================
# SCENE: LossCurves
# =============================================================================
def mavg(v, win):
    v = np.asarray(v)
    out = np.empty_like(v)
    for i in range(len(v)):
        lo = max(0, i - win // 2); hi = min(len(v), i + win // 2 + 1)
        out[i] = v[lo:hi].mean()
    out[0] = v[0]
    return out


class LossCurves(Scene):
    def construct(self):
        w_start = np.array([-3.5, 1.2])
        eta = 0.05
        n_upd = 48
        n_zoom_epochs = 4
        L = {k: np.array([bowl_loss(w) for w in run_variant(k, max(n_upd, n_zoom_epochs * u), eta, w_start)])
             for k, u in (("batch", 1), ("mini", 4), ("sgd", 64))}
        upe = {"batch": 1, "mini": 4, "sgd": 64}
        cols = {"batch": RESULT_COLOR, "mini": W_COLOR, "sgd": Y_COLOR}

        def build_axes(xmax, step):
            a = Axes(x_range=[0, xmax, step], y_range=[0, 12, 4], x_length=8.4, y_length=2.9,
                     axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": True,
                                  "tick_size": 0.06},
                     tips=False).move_to(np.array([0.2, 0.55, 0]))
            return a

        def numbers(a, xmax, step):
            g = VGroup()
            for v in np.arange(0, xmax + 1e-9, step):
                t = MathTex(f"{v:g}", font_size=MIN_FONT, color=INK_DIM)
                t.next_to(a.c2p(v, 0), DOWN, buff=0.1)
                g.add(t)
            for v in (0, 4, 8, 12):
                t = MathTex(f"{v}", font_size=MIN_FONT, color=INK_DIM)
                t.next_to(a.c2p(0, v), LEFT, buff=0.1)
                g.add(t)
            return g

        axes = build_axes(48, 12)
        nums = numbers(axes, 48, 12)
        lbl_y = MathTex(r"L", font_size=MIN_FONT, color=INK_DIM).next_to(axes.y_axis.get_end(), UP, buff=0.18)
        lbl_x_upd = MathTex(r"\text{updates } k", font_size=MIN_FONT, color=INK_DIM)
        lbl_x_upd.next_to(axes.x_axis, DOWN, buff=0.62)
        lbl_x_ep = MathTex(r"\text{epochs } (k \text{ updates} \div \text{updates per epoch})", font_size=MIN_FONT, color=INK_DIM)
        lbl_x_ep.next_to(axes.x_axis, DOWN, buff=0.62)

        def pts(a, xs, ys):
            return [a.c2p(x, min(y, 12.0)) for x, y in zip(xs, ys)]

        def make_curve(a, xs, ys, color, width, opacity=1.0):
            m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
            m.set_points_as_corners(pts(a, xs, ys))
            return m

        k_ax = np.arange(n_upd + 1)
        sm = {"batch": L["batch"][: n_upd + 1], "mini": L["mini"][: n_upd + 1],
              "sgd": mavg(L["sgd"][: n_upd + 1], 5)}
        raw_sgd = L["sgd"][: n_upd + 1]

        def curve_for(key, f, raw=False):
            ys = raw_sgd if raw else sm[key]
            return make_curve(axes, k_ax / f, ys, cols[key], 2.5 if raw else 4.5, 0.35 if raw else 1.0)

        cb = curve_for("batch", 1)
        cm = curve_for("mini", 1)
        cs = curve_for("sgd", 1)
        cr = curve_for("sgd", 1, raw=True)

        legend = VGroup(
            legend_row(r"\text{Batch: } 1", RESULT_COLOR),
            legend_row(r"\text{Mini-batch: } 4", W_COLOR),
            legend_row(r"\text{SGD: } 64", Y_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        hdr = MathTex(r"\text{updates per epoch}", font_size=MIN_FONT, color=INK_DIM)
        legend = VGroup(hdr, legend).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.move_to(np.array([3.7 - legend.width / 2, 1.5, 0]))

        cap1 = MathTex(r"\text{per update, batch GD descends most smoothly}", font_size=MIN_FONT, color=RESULT_COLOR)
        cap1.move_to(np.array([0.0, -2.45, 0]))

        self.add(axes, nums, lbl_y, lbl_x_upd, cr, cs, cm, cb, legend, cap1)
        self.wait(3.5)

        # ---- squeeze: epochs = updates / updates-per-epoch (log-spaced interpolation)
        self.play(FadeOut(lbl_x_upd), FadeOut(cap1), run_time=0.4)
        self.play(FadeIn(lbl_x_ep), run_time=0.5)
        tr = ValueTracker(0)

        def upd(mob, key, raw=False):
            def f(m):
                fac = upe[key] ** tr.get_value()
                new = curve_for(key, fac, raw)
                m.set_points(new.get_points())
            mob.add_updater(f)
        for mob, key, raw in ((cb, "batch", False), (cm, "mini", False), (cs, "sgd", False), (cr, "sgd", True)):
            upd(mob, key, raw)
        self.play(tr.animate.set_value(1.0), run_time=4.5, rate_func=smooth)
        for mob in (cb, cm, cs, cr):
            mob.clear_updaters()
        cap2 = MathTex(r"\text{per epoch, SGD is fastest}", font_size=MIN_FONT, color=RESULT_COLOR)
        cap2.move_to(np.array([0.0, -2.45, 0]))
        self.play(FadeIn(cap2), run_time=0.5)
        self.wait(3.0)

        # ---- zoom to the first 4 epochs
        self.play(FadeOut(VGroup(axes, nums, cb, cm, cs, cr, lbl_x_ep, cap2)), run_time=0.5)
        axes2 = build_axes(4, 1)
        nums2 = numbers(axes2, 4, 1)
        xs = {k: np.arange(len(L[k])) / upe[k] for k in L}
        cb2 = make_curve(axes2, xs["batch"][:5], L["batch"][:5], cols["batch"], 4.5)
        cm2 = make_curve(axes2, xs["mini"][:17], L["mini"][:17], cols["mini"], 4.5)
        cs2 = make_curve(axes2, xs["sgd"][:257], mavg(L["sgd"][:257], 9), cols["sgd"], 4.5)
        cr2 = make_curve(axes2, xs["sgd"][:257], L["sgd"][:257], cols["sgd"], 2.5, 0.35)
        lbl_zoom = MathTex(r"\text{epochs (zoom on the first 4)}", font_size=MIN_FONT, color=INK_DIM)
        lbl_zoom.next_to(axes2.x_axis, DOWN, buff=0.62)
        cap3 = MathTex(r"\text{SGD is down within one epoch}", font_size=MIN_FONT, color=RESULT_COLOR)
        cap3.move_to(np.array([0.0, -2.45, 0]))
        self.play(FadeIn(axes2), FadeIn(nums2), FadeIn(lbl_zoom), run_time=0.5)
        self.play(FadeIn(cr2), FadeIn(cs2), FadeIn(cm2), FadeIn(cb2), FadeIn(cap3), run_time=0.8)
        self.wait(5.0)


# =============================================================================
# SCENE: NoiseBallSchedule
# =============================================================================
class NoiseBallSchedule(Scene):
    def construct(self):
        # Per-example loss l_i(w) = 0.5 |w - a_i|^2, so L has its minimum at mean(a_i) = 0.
        n_pts = 64
        rng = np.random.default_rng(5)
        a = rng.standard_normal((n_pts, 2)) * 0.9
        a = a - a.mean(axis=0)
        K = 200
        eta0 = 0.30
        w0 = np.array([1.5, 1.1])

        def sgd(schedule):
            r = np.random.default_rng(11)
            w = w0.copy()
            P = [w.copy()]
            for k in range(K):
                eta = schedule(k)
                i = r.integers(n_pts)
                w = w - eta * (w - a[i])
                P.append(w.copy())
            return np.array(P)

        const = lambda k: eta0
        decay = lambda k: eta0 / (1.0 + k / 50.0)
        P_c, P_d = sgd(const), sgd(decay)
        # ball radius in the second half, from the real runs
        r_c = np.sqrt(np.mean(np.sum(P_c[100:] ** 2, axis=1)))
        r_d = np.sqrt(np.mean(np.sum(P_d[-20:] ** 2, axis=1)))
        print("noise ball rms radius const %.3f, decay (last 20 steps) %.3f" % (r_c, r_d))

        def panel(cx):
            ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1], x_length=3.4, y_length=3.4,
                      axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
                      tips=False).move_to(np.array([cx, 0.45, 0]))
            rings = VGroup(*[Circle(radius=r * ax.x_length / 4.4, stroke_color=INK_DIM, stroke_width=1.5,
                                    fill_color=V_COLOR, fill_opacity=op).move_to(ax.c2p(0, 0))
                             for r, op in ((2.0, 0.05), (1.5, 0.08), (1.0, 0.12), (0.5, 0.18))])
            return ax, rings

        ax_l, ring_l = panel(-2.6)
        ax_r, ring_r = panel(2.6)
        mins = VGroup(Dot(ax_l.c2p(0, 0), radius=0.06, color=V_COLOR), Dot(ax_r.c2p(0, 0), radius=0.06, color=V_COLOR))
        starts = VGroup(Dot(ax_l.c2p(*w0), radius=0.08, color=INK), Dot(ax_r.c2p(*w0), radius=0.08, color=INK))

        # eta curves under each bowl
        def eta_axes(cx):
            return Axes(x_range=[0, K, 100], y_range=[0, 0.3, 0.1], x_length=3.6, y_length=0.8,
                        axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
                        tips=False).move_to(np.array([cx, -1.75, 0]))
        ea_l, ea_r = eta_axes(-2.6), eta_axes(2.6)
        ks = np.arange(K + 1)
        eta_l = ea_l.plot_line_graph(ks, [const(k) for k in ks], line_color=INK, add_vertex_dots=False, stroke_width=4)
        eta_r = ea_r.plot_line_graph(ks, [decay(k) for k in ks], line_color=INK, add_vertex_dots=False, stroke_width=4)
        eta_sym = [MathTex(r"\eta", font_size=MIN_FONT, color=INK_DIM).next_to(e.y_axis.get_end(), UP, buff=0.05)
                   for e in (ea_l, ea_r)]
        k_sym = [MathTex(r"k", font_size=MIN_FONT, color=INK_DIM).next_to(e.x_axis.get_end(), RIGHT, buff=0.1)
                 for e in (ea_l, ea_r)]

        # live eta readout beside each curve's title
        def readout(cx, f):
            d = DecimalNumber(f(0), num_decimal_places=2, font_size=MIN_FONT, color=INK)
            d.move_to(np.array([cx, -2.5, 0]))
            return d
        ro_l, ro_r = readout(-2.1, const), readout(2.9, decay)
        ro_l_sym = MathTex(r"\eta_k =", font_size=MIN_FONT, color=INK_DIM).next_to(ro_l, LEFT, buff=0.12)
        ro_r_sym = MathTex(r"\eta_k =", font_size=MIN_FONT, color=INK_DIM).next_to(ro_r, LEFT, buff=0.12)

        t_l = MathTex(r"\text{constant } \eta = 0.30", font_size=MIN_FONT, color=INK).move_to(np.array([-2.6, 2.45, 0]))
        t_r = MathTex(r"\eta_k = 0.30/(1 + k/50)", font_size=MIN_FONT, color=INK).move_to(np.array([2.6, 2.45, 0]))
        self.add(t_l, t_r, ring_l, ring_r, ax_l, ax_r, mins, starts, ea_l, ea_r, eta_l, eta_r, *eta_sym, *k_sym,
                 ro_l, ro_r, ro_l_sym, ro_r_sym)
        self.wait(1.5)

        tr = ValueTracker(0)
        trace_l = VMobject(stroke_color=RESULT_COLOR, stroke_width=3, fill_opacity=0)
        trace_r = VMobject(stroke_color=RESULT_COLOR, stroke_width=3, fill_opacity=0)
        dot_l = Dot(ax_l.c2p(*w0), radius=0.09, color=RESULT_COLOR)
        dot_r = Dot(ax_r.c2p(*w0), radius=0.09, color=RESULT_COLOR)
        mk_l = Dot(ea_l.c2p(0, const(0)), radius=0.07, color=RESULT_COLOR)
        mk_r = Dot(ea_r.c2p(0, decay(0)), radius=0.07, color=RESULT_COLOR)

        def refresh(_):
            k = int(round(tr.get_value()))
            for tm, ax, P in ((trace_l, ax_l, P_c), (trace_r, ax_r, P_d)):
                tm.set_points_as_corners([ax.c2p(*p) for p in P[: k + 1]] if k > 0 else
                                         [ax.c2p(*P[0]), ax.c2p(*P[0])])
            dot_l.move_to(ax_l.c2p(*P_c[k])); dot_r.move_to(ax_r.c2p(*P_d[k]))
            mk_l.move_to(ea_l.c2p(k, const(k))); mk_r.move_to(ea_r.c2p(k, decay(k)))
        trace_l.add_updater(refresh)
        def live(f, anchor):
            return always_redraw(lambda: DecimalNumber(f(int(round(tr.get_value()))), num_decimal_places=2,
                                                       font_size=MIN_FONT, color=INK).move_to(anchor))
        a_l, a_r = ro_l.get_center(), ro_r.get_center()
        self.remove(ro_l, ro_r)
        ro_l, ro_r = live(const, a_l), live(decay, a_r)
        self.add(trace_l, trace_r, dot_l, dot_r, mk_l, mk_r, ro_l, ro_r)
        self.play(tr.animate.set_value(K), run_time=9.0, rate_func=linear)
        trace_l.clear_updaters()
        self.wait(2.5)
