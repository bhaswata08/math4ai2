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


# -----------------------------------------------------------------------------
# The bowl, drawn as a surface. Every scene in this deck shows the loss as a
# 3D surface, never as a contour map.
# -----------------------------------------------------------------------------
L_MAX = 12.0     # the surface is drawn out to this level set
LIFT = 0.45      # how far a path floats above the mesh, in loss units


def LOSS(w):
    return 0.5 * w[0] ** 2 + 4.0 * w[1] ** 2


def bowl_axes():
    """Loss surface axes: w1 wide, w2 narrow, L up. Room above for a text row."""
    ax = ThreeDAxes(
        x_range=[-5.2, 5.2, 1.0], y_range=[-2.0, 2.0, 1.0], z_range=[0.0, 20.0, 5.0],
        x_length=7.4, y_length=3.4, z_length=2.8,
        axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                     "include_ticks": False, "include_tip": False},
    )
    ax.x_axis.set_color(X_COLOR)
    ax.y_axis.set_color(Y_COLOR)
    ax.shift(DOWN * 0.95)
    return ax


def bowl_surface(ax):
    """The elliptical bowl out to L = L_MAX, so the rim is a level set."""
    def pt(s, ang):
        lvl = L_MAX * s * s
        w1 = np.sqrt(2.0 * lvl) * np.cos(ang)
        w2 = np.sqrt(lvl / 4.0) * np.sin(ang)
        return ax.c2p(w1, w2, lvl)

    surf = Surface(pt, u_range=[0.001, 1.0], v_range=[0, TAU], resolution=(10, 28),
                   stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3)
    for face in surf.submobjects:
        face.set_fill(color=V_COLOR, opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60)
    return surf


def on_bowl(ax, w, lift=LIFT):
    """The point of the surface above w, floated clear of the mesh."""
    return ax.c2p(w[0], w[1], LOSS(w) + lift)


def top_row(parts, y=2.4):
    """parts: list of (tex, colour). Arranged in one row at the top of the frame."""
    row = VGroup(*[MathTex(t, font_size=MIN_FONT, color=c) for t, c in parts]).arrange(RIGHT, buff=0.55)
    return row.move_to(np.array([0.0, y, 0.0]))


def trail(ax, pts, color, opacity=1.0):
    g = VGroup()
    for i in range(len(pts) - 1):
        g.add(Line(on_bowl(ax, pts[i]), on_bowl(ax, pts[i + 1]),
                   color=color, stroke_width=4, stroke_opacity=opacity))
    for p in pts:
        g.add(Dot3D(on_bowl(ax, p), radius=0.05, color=color, fill_opacity=opacity))
    return g


class BowlScene(ThreeDScene):
    """Shared framing: one camera, one surface, labels fixed in the frame."""

    def setup_bowl(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-68 * DEGREES)
        ax = bowl_axes()
        self.camera.rotation_matrix = self.camera.generate_rotation_matrix()
        scr = lambda p: self.camera.project_point(np.array(p, dtype=float))

        lbl_w1 = MathTex("w_1", font_size=MIN_FONT, color=X_COLOR).move_to(scr(ax.c2p(5.2, 0, 0)) + RIGHT * 0.3)
        lbl_w2 = MathTex("w_2", font_size=MIN_FONT, color=Y_COLOR).move_to(scr(ax.c2p(0, -2.0, 0)) + DOWN * 0.35 + LEFT * 0.2)
        labels = VGroup(lbl_w1, lbl_w2)
        self.camera.add_fixed_in_frame_mobjects(labels)

        surf = bowl_surface(ax)
        self.add(ax, surf, labels)
        return ax, surf

    def fixed(self, *mobs):
        self.camera.add_fixed_in_frame_mobjects(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs


class ValleyThreeRates(BowlScene):
    def construct(self):
        ax, surf = self.setup_bowl()
        ball = Dot3D(on_bowl(ax, START), radius=0.1, color=RESULT_COLOR)
        head = self.fixed(MathTex(r"L = \tfrac12 w_1^2 + 4 w_2^2", font_size=MIN_FONT,
                                  color=V_COLOR).move_to(np.array([0.0, 2.4, 0.0])))

        self.add(ball, head)
        self.wait(1.6)

        # three steps of the diverging run: the fourth would climb out of the frame
        runs = [(0.05, 20, 0.2), (0.22, 12, 0.4), (0.27, 3, 0.8)]
        trails = []
        prev_row = head
        for ri, (eta, n, rt) in enumerate(runs):
            pts = gd_path(eta, n)
            f1, f2 = 1.0 - eta, 1.0 - LAMBDA_MAX * eta
            row = self.fixed(top_row([
                (rf"\eta = {eta:.2f}", INK),
                (rf"(1-\eta) = {f1:.2f}", X_COLOR),
                (rf"(1-8\eta) = {f2:.2f}", Y_COLOR),
            ]))
            if ri == 0:
                self.play(FadeOut(prev_row), run_time=0.3)
            else:
                dim = trails[-1]
                self.play(FadeOut(prev_row), dim.animate.set_opacity(0.3),
                          ball.animate.move_to(on_bowl(ax, START)), run_time=0.8)
            self.play(FadeIn(row), run_time=0.4)
            prev_row = row
            self.wait(1.0)
            tr = VGroup()
            self.add(tr)
            for i in range(n):
                seg = Line(on_bowl(ax, pts[i]), on_bowl(ax, pts[i + 1]), color=RESULT_COLOR, stroke_width=4)
                self.play(Create(seg), ball.animate.move_to(on_bowl(ax, pts[i + 1])), run_time=rt, rate_func=linear)
                tr.add(seg, Dot3D(on_bowl(ax, pts[i + 1]), radius=0.05, color=RESULT_COLOR))
            trails.append(tr)
            self.wait(1.8 if ri else 1.5)

        bound = self.fixed(top_row([(rf"\eta < 2/\lambda_{{\max}} = 2/{LAMBDA_MAX:.0f} = {2.0 / LAMBDA_MAX:.2f}", HIGHLIGHT)]))
        self.play(FadeOut(prev_row), run_time=0.3)
        self.play(trails[0].animate.set_opacity(0.55), trails[1].animate.set_opacity(0.55),
                  ball.animate.move_to(on_bowl(ax, START)), run_time=0.8)
        self.play(FadeIn(bound), run_time=0.4)
        self.wait(3.0)


class MomentumVsPlain(BowlScene):
    def construct(self):
        eta, beta = 0.22, 0.3
        n_plain, n_mom = 40, 20
        plain = gd_path(eta, n_plain)
        mom, vels = momentum_path(eta, beta, n_mom)
        k_plain = steps_to_reach(plain)
        k_mom = steps_to_reach(mom)
        assert k_plain is not None and k_mom is not None and k_mom < k_plain

        ax, surf = self.setup_bowl()
        ball = Dot3D(on_bowl(ax, START), radius=0.1, color=RESULT_COLOR)
        row_plain = self.fixed(top_row([(rf"\text{{plain GD}},\ \eta = {eta}", RESULT_COLOR)]))

        self.add(ball, row_plain)
        self.wait(1.6)

        # plain gradient descent
        tr_plain = VGroup()
        self.add(tr_plain)
        for i in range(k_plain):
            seg = Line(on_bowl(ax, plain[i]), on_bowl(ax, plain[i + 1]), color=RESULT_COLOR, stroke_width=4)
            self.play(Create(seg), ball.animate.move_to(on_bowl(ax, plain[i + 1])), run_time=0.1, rate_func=linear)
            tr_plain.add(seg, Dot3D(on_bowl(ax, plain[i + 1]), radius=0.04, color=RESULT_COLOR))
        cnt_plain = self.fixed(top_row([(rf"\text{{plain GD}}:\ {k_plain}\ \text{{steps}}", RESULT_COLOR)]))
        self.play(FadeOut(row_plain), run_time=0.3)
        self.play(FadeIn(cnt_plain), run_time=0.4)
        self.wait(1.8)

        # heavy ball
        row_mom = self.fixed(top_row([
            (rf"v \leftarrow {beta}\,v - \eta\nabla L", W_COLOR),
            (r"\mathbf w \leftarrow \mathbf w + v", W_COLOR),
        ], y=2.4))
        # two stacked lines would need more room, so the update rule is shown across one row
        self.play(FadeOut(cnt_plain), tr_plain.animate.set_opacity(0.3),
                  ball.animate.set_color(W_COLOR).move_to(on_bowl(ax, START)), run_time=0.8)
        self.play(FadeIn(row_mom), run_time=0.4)
        self.wait(1.5)

        tr_mom = VGroup()
        self.add(tr_mom)
        n_show = 5
        shown = VGroup()
        for i in range(k_mom):
            p0, p1 = mom[i], mom[i + 1]
            seg = Line(on_bowl(ax, p0), on_bowl(ax, p1), color=W_COLOR, stroke_width=4)
            if i < n_show:
                v = vels[i]
                corner = np.array([p0[0] + v[0], p0[1]])
                a_x = (Arrow3D(on_bowl(ax, p0), on_bowl(ax, corner), thickness=0.012,
                               base_radius=0.05, color=X_COLOR) if abs(v[0]) > 0.05 else VGroup())
                a_y = (Arrow3D(on_bowl(ax, corner), on_bowl(ax, p1), thickness=0.012,
                               base_radius=0.05, color=Y_COLOR) if abs(v[1]) > 0.05 else VGroup())
                a_v = Arrow3D(on_bowl(ax, p0), on_bowl(ax, p1), thickness=0.012,
                              base_radius=0.05, color=HIGHLIGHT)
                self.play(Create(seg), ball.animate.move_to(on_bowl(ax, p1)),
                          FadeIn(a_x), FadeIn(a_y), FadeIn(a_v), run_time=0.9)
                shown.add(a_x, a_y, a_v)
                self.wait(0.5)
            else:
                self.play(Create(seg), ball.animate.move_to(on_bowl(ax, p1)), run_time=0.22, rate_func=linear)
            tr_mom.add(seg, Dot3D(on_bowl(ax, p1), radius=0.04, color=W_COLOR))
            if i == n_show - 1:
                msg = self.fixed(top_row([(r"w_1\ \text{kicks add up}", X_COLOR),
                                          (r"w_2\ \text{kicks cancel}", Y_COLOR)]))
                self.play(FadeOut(row_mom), run_time=0.3)
                self.play(FadeIn(msg), run_time=0.4)
                self.wait(2.2)
                self.play(FadeOut(shown), run_time=0.4)
        end = self.fixed(top_row([
            (rf"\text{{plain}}:\ {k_plain}", RESULT_COLOR),
            (rf"\text{{momentum}}:\ {k_mom}\ \text{{steps}}", W_COLOR),
        ]))
        self.play(FadeOut(msg), tr_plain.animate.set_opacity(0.8), run_time=0.4)
        self.play(FadeIn(end), run_time=0.4)
        self.wait(3.0)
