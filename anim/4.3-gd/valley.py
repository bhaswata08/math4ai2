# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np

# The valley L = 0.5 w1^2 + 4 w2^2, gradient (w1, 8 w2), Hessian diag(1, 8).
CURV = np.array([1.0, 8.0])
START = np.array([-3.5, 1.2])
LAMBDA_MAX = float(CURV.max())


def grad(w):
    return CURV * w


def gd_path(eta, n):
    w = START.copy()
    pts = [w.copy()]
    for _ in range(n):
        w = w - eta * grad(w)
        pts.append(w.copy())
    return pts


def momentum_path(eta, beta, n):
    w = START.copy()
    v = np.zeros(2)
    pts, vels = [w.copy()], []
    for _ in range(n):
        v = beta * v - eta * grad(w)
        w = w + v
        pts.append(w.copy())
        vels.append(v.copy())
    return pts, vels


def steps_to_reach(pts, tol=0.1):
    """First step k after which |w| < tol and stays there."""
    norms = [np.linalg.norm(p) for p in pts]
    for k in range(len(norms)):
        if all(n < tol for n in norms[k:]):
            return k
    return None


def valley_axes():
    """Plane with equal unit lengths, spanning the frame; room above for a text row."""
    ax = Axes(
        x_range=[-4.6, 4.6, 1.0],
        y_range=[-2.0, 2.0, 1.0],
        x_length=9.2,
        y_length=4.0,
        axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
        tips=False,
    ).move_to(np.array([0.0, -0.4, 0.0]))
    return ax


def valley_contours(ax):
    out = VGroup()
    for lvl in [0.5, 1.5, 3.0, 5.0, 8.0]:
        a, b = np.sqrt(2.0 * lvl), np.sqrt(lvl / 4.0)
        ell = Ellipse(width=2 * a * ax.x_axis.unit_size, height=2 * b * ax.y_axis.unit_size,
                      stroke_color=V_COLOR, stroke_width=1.5, stroke_opacity=0.55, fill_opacity=0)
        out.add(ell.move_to(ax.c2p(0, 0)))
    return out


def axis_ticks(ax):
    """Number labels on both axes, placed off the contour lines."""
    g = VGroup()
    for v in (-4, 4):
        t = MathTex(f"{v}", font_size=MIN_FONT, color=INK_DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
        g.add(t.add_background_rectangle(color=BG, opacity=0.9, buff=0.05))
    for v in (-2, 2):
        g.add(MathTex(f"{v}", font_size=MIN_FONT, color=INK_DIM).next_to(ax.c2p(0, v), RIGHT, buff=0.1))
    return g


def top_row(parts, y=2.4):
    """parts: list of (tex, colour). Arranged in one row at the top of the frame."""
    row = VGroup(*[MathTex(t, font_size=MIN_FONT, color=c) for t, c in parts]).arrange(RIGHT, buff=0.55)
    return row.move_to(np.array([0.0, y, 0.0]))


def trail(ax, pts, color, opacity=1.0):
    g = VGroup()
    for i in range(len(pts) - 1):
        g.add(Line(ax.c2p(*pts[i]), ax.c2p(*pts[i + 1]), color=color, stroke_width=4, stroke_opacity=opacity))
    for p in pts:
        g.add(Dot(ax.c2p(*p), radius=0.05, color=color, fill_opacity=opacity))
    return g


class ValleyThreeRates(Scene):
    def construct(self):
        ax = valley_axes()
        lbl_w1 = MathTex("w_1", font_size=MIN_FONT, color=X_COLOR).next_to(ax.c2p(4.6, 0), UP, buff=0.1).shift(LEFT * 0.35)
        lbl_w2 = MathTex("w_2", font_size=MIN_FONT, color=Y_COLOR).next_to(ax.c2p(0, 2.0), RIGHT, buff=0.1).shift(DOWN * 0.1 + RIGHT * 0.9)
        contours = valley_contours(ax)
        ticks = axis_ticks(ax)
        ball = Dot(ax.c2p(*START), radius=0.1, color=RESULT_COLOR)
        grad_tex = MathTex(r"L = \tfrac12 w_1^2 + 4 w_2^2", font_size=MIN_FONT, color=V_COLOR).move_to(np.array([0.0, 2.4, 0.0]))

        self.add(ax, contours, ticks, lbl_w1, lbl_w2, ball, grad_tex)
        self.wait(1.6)

        runs = [(0.05, 20, 0.2), (0.22, 12, 0.4), (0.27, 4, 0.8)]
        trails = []
        prev_row = grad_tex
        for ri, (eta, n, rt) in enumerate(runs):
            pts = gd_path(eta, n)
            f1, f2 = 1.0 - eta, 1.0 - LAMBDA_MAX * eta
            row = top_row([
                (rf"\eta = {eta:.2f}", INK),
                (rf"(1-\eta) = {f1:.2f}", X_COLOR),
                (rf"(1-8\eta) = {f2:.2f}", Y_COLOR),
            ])
            if ri == 0:
                self.play(FadeOut(prev_row), run_time=0.3)
            else:
                dim = trails[-1]
                self.play(FadeOut(prev_row), dim.animate.set_opacity(0.3), ball.animate.move_to(ax.c2p(*START)), run_time=0.8)
            self.play(FadeIn(row), run_time=0.4)
            prev_row = row
            self.wait(1.0)
            tr = VGroup()
            self.add(tr)
            for i in range(n):
                seg = Line(ax.c2p(*pts[i]), ax.c2p(*pts[i + 1]), color=RESULT_COLOR, stroke_width=4)
                self.play(Create(seg), ball.animate.move_to(ax.c2p(*pts[i + 1])), run_time=rt, rate_func=linear)
                tr.add(seg, Dot(ax.c2p(*pts[i + 1]), radius=0.05, color=RESULT_COLOR))
            trails.append(tr)
            self.wait(1.8 if ri else 1.5)

        bound = top_row([(rf"\eta < 2/\lambda_{{\max}} = 2/{LAMBDA_MAX:.0f} = {2.0 / LAMBDA_MAX:.2f}", HIGHLIGHT)])
        self.play(FadeOut(prev_row), run_time=0.3)
        self.play(trails[0].animate.set_opacity(0.55), trails[1].animate.set_opacity(0.55), ball.animate.move_to(ax.c2p(*START)), run_time=0.8)
        self.play(FadeIn(bound), run_time=0.4)
        self.wait(3.0)


class MomentumVsPlain(Scene):
    def construct(self):
        eta, beta = 0.22, 0.3
        n_plain, n_mom = 40, 20
        plain = gd_path(eta, n_plain)
        mom, vels = momentum_path(eta, beta, n_mom)
        k_plain = steps_to_reach(plain)
        k_mom = steps_to_reach(mom)
        assert k_plain is not None and k_mom is not None and k_mom < k_plain

        ax = valley_axes()
        lbl_w1 = MathTex("w_1", font_size=MIN_FONT, color=X_COLOR).next_to(ax.c2p(4.6, 0), UP, buff=0.1).shift(LEFT * 0.35)
        lbl_w2 = MathTex("w_2", font_size=MIN_FONT, color=Y_COLOR).next_to(ax.c2p(0, 2.0), RIGHT, buff=0.1).shift(DOWN * 0.1 + RIGHT * 0.9)
        contours = valley_contours(ax)
        ticks = axis_ticks(ax)
        ball = Dot(ax.c2p(*START), radius=0.1, color=RESULT_COLOR)
        row_plain = top_row([(rf"\text{{plain GD}},\ \eta = {eta}", RESULT_COLOR)])

        self.add(ax, contours, ticks, lbl_w1, lbl_w2, ball, row_plain)
        self.wait(1.6)

        # plain gradient descent
        tr_plain = VGroup()
        self.add(tr_plain)
        for i in range(k_plain):
            seg = Line(ax.c2p(*plain[i]), ax.c2p(*plain[i + 1]), color=RESULT_COLOR, stroke_width=4)
            self.play(Create(seg), ball.animate.move_to(ax.c2p(*plain[i + 1])), run_time=0.1, rate_func=linear)
            tr_plain.add(seg, Dot(ax.c2p(*plain[i + 1]), radius=0.04, color=RESULT_COLOR))
        cnt_plain = top_row([(rf"\text{{plain GD}}:\ {k_plain}\ \text{{steps}}", RESULT_COLOR)])
        self.play(FadeOut(row_plain), run_time=0.3)
        self.play(FadeIn(cnt_plain), run_time=0.4)
        self.wait(1.8)

        # heavy ball
        row_mom = top_row([
            (rf"v \leftarrow {beta}\,v - \eta\nabla L", W_COLOR),
            (r"\mathbf w \leftarrow \mathbf w + v", W_COLOR),
        ], y=2.4)
        # two stacked lines would need more room, so the update rule is shown across one row
        self.play(FadeOut(cnt_plain), tr_plain.animate.set_opacity(0.3), ball.animate.set_color(W_COLOR).move_to(ax.c2p(*START)), run_time=0.8)
        self.play(FadeIn(row_mom), run_time=0.4)
        self.wait(1.5)

        tr_mom = VGroup()
        self.add(tr_mom)
        n_show = 5
        shown = VGroup()
        for i in range(k_mom):
            p0, p1 = mom[i], mom[i + 1]
            seg = Line(ax.c2p(*p0), ax.c2p(*p1), color=W_COLOR, stroke_width=4)
            if i < n_show:
                v = vels[i]
                corner = ax.c2p(p0[0] + v[0], p0[1])
                a_x = Arrow(ax.c2p(*p0), corner, buff=0, stroke_width=5, color=X_COLOR, max_tip_length_to_length_ratio=0.3) if abs(v[0]) > 0.05 else VGroup()
                a_y = Arrow(corner, ax.c2p(*p1), buff=0, stroke_width=5, color=Y_COLOR, max_tip_length_to_length_ratio=0.3) if abs(v[1]) > 0.05 else VGroup()
                a_v = Arrow(ax.c2p(*p0), ax.c2p(*p1), buff=0, stroke_width=5, color=HIGHLIGHT, max_tip_length_to_length_ratio=0.2)
                self.play(Create(seg), ball.animate.move_to(ax.c2p(*p1)),
                          FadeIn(a_x), FadeIn(a_y), GrowArrow(a_v), run_time=0.9)
                shown.add(a_x, a_y, a_v)
                self.wait(0.5)
            else:
                self.play(Create(seg), ball.animate.move_to(ax.c2p(*p1)), run_time=0.22, rate_func=linear)
            tr_mom.add(seg, Dot(ax.c2p(*p1), radius=0.04, color=W_COLOR))
            if i == n_show - 1:
                msg = top_row([(r"w_1\ \text{kicks add up}", X_COLOR), (r"w_2\ \text{kicks cancel}", Y_COLOR)])
                self.play(FadeOut(row_mom), run_time=0.3)
                self.play(FadeIn(msg), run_time=0.4)
                self.wait(2.2)
                self.play(FadeOut(shown), run_time=0.4)
        end = top_row([
            (rf"\text{{plain}}:\ {k_plain}", RESULT_COLOR),
            (rf"\text{{momentum}}:\ {k_mom}\ \text{{steps}}", W_COLOR),
        ])
        self.play(FadeOut(msg), tr_plain.animate.set_opacity(0.8), run_time=0.4)
        self.play(FadeIn(end), run_time=0.4)
        self.wait(3.0)
