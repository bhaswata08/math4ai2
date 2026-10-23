# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np

LABEL_BG = dict(color=BG, opacity=0.85, buff=0.08)


# Shared curves. A convex parabola and a tilted double well.
def f_par(x):
    return 0.75 * x * x - 1.3


def df_par(x):
    return 1.5 * x


def f_non(x):
    return 0.25 * x ** 4 - x * x + 0.35 * x


def df_non(x):
    return x ** 3 - 2 * x + 0.35


# The two minima of the double well, from the real derivative.
_roots = np.sort(np.roots([1.0, 0.0, -2.0, 0.35]).real)
X_GLOBAL, X_HUMP, X_LOCAL = _roots[0], _roots[1], _roots[2]
XR = (-2.4, 2.4)


class Plot:
    """Hand-drawn axes with the x axis along the bottom and the y axis at the left."""

    def __init__(self, yr, width=8.4, height=4.3, centre=(-0.15, -0.3)):
        self.ax = Axes(x_range=[XR[0], XR[1], 1], y_range=[yr[0], yr[1], 1],
                       x_length=width, y_length=height, tips=False)
        self.ax.move_to([centre[0], centre[1], 0])
        self.c2p = self.ax.c2p
        o = self.c2p(XR[0], yr[0])
        xe = self.c2p(XR[1], yr[0])
        ye = self.c2p(XR[0], yr[1])
        self.axes = VGroup(
            Line(o, xe, color=INK_DIM, stroke_width=3),
            Line(o, ye, color=INK_DIM, stroke_width=3),
        )
        self.xl = MathTex("x", font_size=44, color=INK_DIM).next_to(xe, RIGHT, buff=0.2)
        self.yl = MathTex("f", font_size=44, color=INK_DIM).next_to(ye, UP, buff=0.12)
        self.group = VGroup(self.axes, self.xl, self.yl)

    def curve(self, f, color=V_COLOR, x0=XR[0], x1=XR[1]):
        return ParametricFunction(lambda t: self.c2p(t, f(t)), t_range=[x0, x1], color=color,
                                  stroke_width=6)


def flow(df, x0, lr, T, n=400):
    xs = [x0]
    dt = T / n
    for _ in range(n):
        xs.append(xs[-1] - lr * df(xs[-1]) * dt)
    return np.array(xs)


# =============================================================================
# SCENE 1: ChordTest
# =============================================================================
class ChordTest(Scene):
    def construct(self):
        P = Plot((-1.6, 3.6))
        self.add(P.group)

        fs = [f_par]  # the curve the chord currently rides on

        ta, tb = ValueTracker(-1.8), ValueTracker(0.9)

        def chord():
            a, b = ta.get_value(), tb.get_value()
            return Line(P.c2p(a, fs[0](a)), P.c2p(b, fs[0](b)), color=RESULT_COLOR, stroke_width=6)

        def dots():
            a, b = ta.get_value(), tb.get_value()
            return VGroup(*[Dot(P.c2p(x, fs[0](x)), radius=0.11, color=RESULT_COLOR) for x in (a, b)])

        def gap(color, op, sign):
            # fill only where sign * (curve - chord) > 0: sign -1 = chord above, +1 = chord below
            def make():
                a, b = ta.get_value(), tb.get_value()
                f = fs[0]
                xs = np.linspace(a, b, 240)
                ch_y = lambda x: f(a) + (f(b) - f(a)) * (x - a) / (b - a)
                ok = [sign * (f(x) - ch_y(x)) > 1e-9 for x in xs]
                g = VGroup()
                i = 0
                while i < len(xs):
                    if not ok[i]:
                        i += 1
                        continue
                    j = i
                    while j + 1 < len(xs) and ok[j + 1]:
                        j += 1
                    if j > i:
                        seg = xs[i:j + 1]
                        top = [P.c2p(x, f(x)) for x in seg]
                        bot = [P.c2p(x, ch_y(x)) for x in seg[::-1]]
                        g.add(Polygon(*top, *bot, stroke_width=0, fill_color=color, fill_opacity=op))
                    i = j + 1
                if len(g) == 0:
                    g.add(Dot(P.c2p(a, f(a)), radius=0.001, fill_opacity=0))
                return g
            return make

        # --- beat 1: convex parabola
        curve1 = P.curve(f_par)
        lab1 = MathTex(r"\text{convex}", font_size=52, color=V_COLOR).move_to([0.2, 2.35, 0])
        ch = always_redraw(chord)
        dt = always_redraw(dots)
        gp = always_redraw(gap(RESULT_COLOR, 0.22, -1))
        self.add(curve1, gp, ch, dt, lab1)
        self.wait(2.0)
        for a, b in [(-2.1, -0.4), (-0.9, 2.1), (-1.5, 1.6)]:
            self.play(ta.animate.set_value(a), tb.animate.set_value(b), run_time=1.2)
            self.wait(0.4)
        self.wait(0.4)

        # --- beat 2: double well
        self.play(FadeOut(ch), FadeOut(dt), FadeOut(gp), FadeOut(lab1), run_time=0.5)
        curve2 = P.curve(f_non)
        fs[0] = f_non
        ta.set_value(-1.35)
        tb.set_value(1.0)
        lab2 = MathTex(r"\text{not convex}", font_size=52, color=INK).move_to([0.2, 2.35, 0])
        self.play(ReplacementTransform(curve1, curve2), run_time=1.2)
        gp = always_redraw(gap(HIGHLIGHT, 0.5, +1))
        ch = always_redraw(chord)
        dt = always_redraw(dots)
        self.play(FadeIn(gp), FadeIn(ch), FadeIn(dt), FadeIn(lab2), run_time=0.7)
        self.wait(1.6)
        for a, b in [(-1.7, 0.5), (-1.0, 1.7)]:
            self.play(ta.animate.set_value(a), tb.animate.set_value(b), run_time=1.3)
            self.wait(0.7)
        self.wait(1.1)


# =============================================================================
# SCENE 2: ConvexSets
# =============================================================================
class ConvexSets(Scene):
    def construct(self):
        CL = np.array([-2.5, 0.0, 0.0])
        CR = np.array([2.5, 0.0, 0.0])
        R_DISC = 1.5
        R_IN, R_OUT, A0, A1 = 0.75, 1.65, np.radians(60), np.radians(300)

        disc = Circle(radius=R_DISC, color=W_COLOR, stroke_width=4, fill_color=W_COLOR,
                      fill_opacity=0.35).move_to(CL)
        sector = AnnularSector(inner_radius=R_IN, outer_radius=R_OUT, angle=A1 - A0,
                               start_angle=A0, color=W_COLOR, stroke_width=4,
                               fill_color=W_COLOR, fill_opacity=0.35).move_to(CR)
        # AnnularSector centres on its own bounding box; pin the ring centre back to CR.
        sector.shift(CR - sector.get_arc_center())

        def in_disc(q):
            return np.linalg.norm(q - CL) <= R_DISC + 1e-9

        def in_sector(q):
            v = q - CR
            r = np.hypot(v[0], v[1])
            ang = np.arctan2(v[1], v[0]) % (2 * np.pi)
            return R_IN - 1e-9 <= r <= R_OUT + 1e-9 and A0 - 1e-9 <= ang <= A1 + 1e-9

        t1 = MathTex(r"\text{convex set}", font_size=48, color=INK).move_to([-2.5, -2.3, 0])
        t2 = MathTex(r"\text{not convex}", font_size=48, color=INK).move_to([2.5, -2.3, 0])

        def pt_disc(ang, r):
            return CL + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        def pt_sec(ang, r):
            return CR + r * np.array([np.cos(ang), np.sin(ang), 0.0])

        # tracker drives both panels: u in [0,1] interpolates the two end points
        ua, ub = ValueTracker(0.0), ValueTracker(0.0)
        discA = [(np.radians(200), 1.3), (np.radians(40), 1.4), (np.radians(110), 1.2), (np.radians(260), 1.4)]
        discB = [(np.radians(20), 1.3), (np.radians(250), 1.35), (np.radians(330), 1.4), (np.radians(70), 1.0)]
        secA = [(np.radians(90), 1.2), (np.radians(105), 1.2), (np.radians(80), 1.2), (np.radians(115), 1.2)]
        secB = [(np.radians(270), 1.2), (np.radians(255), 1.2), (np.radians(280), 1.2), (np.radians(245), 1.2)]

        def lerp_pts(lst, mk, u):
            k = min(int(u), len(lst) - 2)
            f = u - k
            a0, r0 = lst[k]
            a1, r1 = lst[k + 1]
            return mk(a0 + (a1 - a0) * f, r0 + (r1 - r0) * f)

        def seg_panel(lstA, lstB, mk, inside, u_tr):
            def make():
                u = u_tr.get_value()
                p, q = lerp_pts(lstA, mk, u), lerp_pts(lstB, mk, u)
                ts = np.linspace(0, 1, 241)
                pts = [p + (q - p) * t for t in ts]
                ok = [inside(z) for z in pts]
                g = VGroup()
                i = 0
                while i < len(ts) - 1:
                    j = i
                    while j < len(ts) - 1 and ok[j] == ok[i]:
                        j += 1
                    col = RESULT_COLOR if ok[i] else HIGHLIGHT
                    if j > i:
                        g.add(Line(pts[i], pts[j], color=col, stroke_width=7))
                    i = j
                g.add(Dot(p, radius=0.11, color=RESULT_COLOR), Dot(q, radius=0.11, color=RESULT_COLOR))
                return g
            return make

        segL = always_redraw(seg_panel(discA, discB, pt_disc, in_disc, ua))
        segR = always_redraw(seg_panel(secA, secB, pt_sec, in_sector, ub))
        self.add(disc, sector, segL, segR, t1, t2)
        self.wait(2.0)
        self.play(ua.animate.set_value(3.0), run_time=5.0, rate_func=linear)
        self.wait(1.0)
        self.play(ub.animate.set_value(3.0), run_time=5.0, rate_func=linear)
        self.wait(2.0)


# =============================================================================
# SCENE 3: ConvexStarts
# =============================================================================
def starts_scene(scene, f, df, yr, starts, lr, label_top, labels_after):
    P = Plot(yr)
    curve = P.curve(f)
    balls = VGroup(*[Dot(radius=0.14, color=RESULT_COLOR).move_to(P.c2p(x, f(x))) for x in starts])
    trails = VGroup(*[TracedPath(b.get_center, stroke_color=RESULT_COLOR, stroke_width=3,
                                 stroke_opacity=0.35) for b in balls])
    scene.add(P.group, curve, trails, balls, label_top)
    scene.wait(2.5)
    paths = [flow(df, x, lr, 7.0) for x in starts]
    n = len(paths[0]) - 1

    def upd(mob, alpha):
        k = int(round(alpha * n))
        for b, path in zip(mob, paths):
            b.move_to(P.c2p(path[k], f(path[k])))
    scene.play(UpdateFromAlphaFunc(balls, upd, run_time=7.0, rate_func=linear))
    return P, curve, paths


class ConvexStarts(Scene):
    def construct(self):
        lab = MathTex(r"\text{convex}", font_size=52, color=V_COLOR).move_to([0.2, 2.35, 0])
        P, curve, paths = starts_scene(self, f_par, df_par, (-1.6, 3.6), [-2.2, 0.6, 2.2], 0.9, lab, None)
        self.wait(0.5)
        cap = MathTex(r"\text{every local minimum is global}", font_size=48, color=INK).move_to([0.2, 2.35, 0])
        self.play(FadeOut(lab), run_time=0.4)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(3.5)


class NonConvexStarts(Scene):
    def construct(self):
        lab = MathTex(r"\text{not convex}", font_size=52, color=INK).move_to([0.2, 2.35, 0])
        P, curve, paths = starts_scene(self, f_non, df_non, (-3.0, 3.6), [-2.2, 0.6, 2.2], 0.45, lab, None)
        glob = MathTex(r"\text{global}", font_size=48, color=RESULT_COLOR)
        glob.move_to(P.c2p(X_GLOBAL, f_non(X_GLOBAL)) + DOWN * 0.55)
        loc = MathTex(r"\text{local}", font_size=48, color=INK_DIM)
        loc.move_to(P.c2p(X_LOCAL, f_non(X_LOCAL)) + DOWN * 0.55)
        self.wait(0.5)
        self.play(FadeIn(glob), FadeIn(loc), run_time=0.8)
        self.wait(3.5)


# =============================================================================
# SCENE 5: ActiveVsInactive
# =============================================================================
def project_disc(p):
    n = np.linalg.norm(p)
    return p if n <= 1.0 else p / n


def projected_gradient(c, x0=(0.0, 0.0), eta=0.12, steps=70):
    """Projected gradient descent on f = |x - c|^2 over the unit disc. Returns every iterate."""
    c = np.array(c, dtype=float)
    x = np.array(x0, dtype=float)
    xs = [x.copy()]
    for _ in range(steps):
        x = project_disc(x - eta * 2.0 * (x - c))
        xs.append(x.copy())
    return np.array(xs)


class ActiveVsInactive(Scene):
    def construct(self):
        S = 1.2
        cases = {
            "A": dict(c=(2.0, 1.0), origin=np.array([-2.55, -0.58, 0.0])),
            "B": dict(c=(0.3, 0.2), origin=np.array([3.0, -0.58, 0.0])),
        }
        for k in cases.values():
            k["path"] = projected_gradient(k["c"])
            k["opt"] = k["path"][-1]

        def sp(k, v):
            return k["origin"] + S * np.array([v[0], v[1], 0.0])

        panels, dots, trails, caps = {}, {}, {}, {}
        for name, k in cases.items():
            disc = Circle(radius=S, color=W_COLOR, stroke_width=4, fill_color=W_COLOR,
                          fill_opacity=0.35).move_to(k["origin"])
            c = np.array(k["c"])
            d = np.linalg.norm(k["path"][-1] - c)  # distance from the optimum to the centre
            rings = VGroup(*[Circle(radius=S * r, color=V_COLOR, stroke_width=3, stroke_opacity=0.7)
                             .move_to(sp(k, c)) for r in ([d] if name == "A" else [0.25, 0.5])])
            cdot = Dot(sp(k, c), radius=0.07, color=V_COLOR)
            dot = Dot(sp(k, k["path"][0]), radius=0.12, color=INK)
            trail = TracedPath(dot.get_center, stroke_color=INK, stroke_width=3, stroke_opacity=0.7)
            cap = MathTex(r"\mathbf c = (%g,\ %g)" % k["c"], font_size=42, color=V_COLOR)
            cap.move_to([k["origin"][0], 2.42, 0.0])
            gl = MathTex(r"g \le 0", font_size=42, color=INK_DIM).move_to(k["origin"] + np.array([0.0, -0.55, 0.0]))
            panels[name] = VGroup(disc, rings, cdot, gl)
            dots[name], trails[name], caps[name] = dot, trail, cap
            k["cap"] = cap

        self.add(*panels.values(), *trails.values(), *dots.values(), *caps.values())
        self.wait(2.5)

        def run(name, T):
            path = cases[name]["path"]
            n = len(path) - 1
            k = cases[name]

            def upd(mob, alpha):
                mob.move_to(sp(k, path[int(round(alpha * n))]))
            return UpdateFromAlphaFunc(dots[name], upd, run_time=T, rate_func=linear)

        # --- part A: centre outside the disc, constraint active
        kA = cases["A"]
        self.play(run("A", 3.5))
        self.wait(0.5)
        p = kA["opt"]
        cA = np.array(kA["c"])
        grad_f = 2.0 * (p - cA)          # gradient of f at the optimum
        grad_g = 2.0 * p                 # gradient of g = x^2 + y^2 - 1
        lam = -float(np.dot(grad_f, grad_g) / np.dot(grad_g, grad_g))   # grad f = -lam grad g
        assert abs(np.linalg.norm(p) - 1.0) < 1e-6 and lam > 0
        assert np.allclose(grad_f, -lam * grad_g, atol=1e-4)
        K = 0.4
        u = p / np.linalg.norm(p)
        nrm = np.array([-u[1], u[0], 0.0])
        u = np.append(u, 0.0)
        off = 0.14
        start = sp(kA, p)
        a_f = Arrow(start + off * nrm * 1.0, start + off * nrm + K * np.append(-grad_f, 0.0),
                    buff=0, color=RESULT_COLOR, stroke_width=7, max_tip_length_to_length_ratio=0.3)
        a_g = Arrow(start - off * nrm, start - off * nrm + K * np.append(grad_g, 0.0),
                    buff=0, color=W_COLOR, stroke_width=7, max_tip_length_to_length_ratio=0.3)
        lf = MathTex(r"-\nabla f", font_size=44, color=RESULT_COLOR).move_to(a_f.get_end() + nrm * 0.62 + u * 0.1)
        lg = MathTex(r"\nabla g", font_size=44, color=W_COLOR).move_to(a_g.get_end() - nrm * 0.58 + u * 0.1)
        self.play(GrowArrow(a_f), GrowArrow(a_g), FadeIn(lf), FadeIn(lg), run_time=1.2)
        self.wait(1.3)
        resA = MathTex(r"\text{active: } \lambda = %.2f > 0" % lam, font_size=42, color=INK)
        resA.move_to(kA["origin"] + np.array([0.0, -1.85, 0.0]))
        self.play(FadeIn(resA), run_time=0.6)
        self.wait(2.5)

        # --- part B: centre inside the disc, constraint inactive
        kB = cases["B"]
        self.play(run("B", 3.5))
        self.wait(0.5)
        assert np.linalg.norm(kB["opt"]) < 1.0 - 1e-3
        resB = MathTex(r"\text{inactive: } \lambda = 0", font_size=42, color=INK)
        resB.move_to(kB["origin"] + np.array([0.0, -1.85, 0.0]))
        self.play(FadeIn(resB), run_time=0.6)
        self.wait(3.5)
