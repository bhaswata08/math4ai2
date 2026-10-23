# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


def bg(m, buff=0.08):
    m.add_background_rectangle(color=BG, opacity=0.85, buff=buff)
    return m


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def coef(c, power):
    """'3\\,t^2' style term with the coefficient computed, never typed."""
    c = float(c)
    if abs(c - round(c)) < 1e-9:
        c = int(round(c))
    return f"{c}\\,t^{power}" if power != 1 else f"{c}\\,t"


# The deck's worked example (slide "f(x,y) = x^3 + 2xy - y^2").
def F(x, y):
    return x**3 + 2 * x * y - y**2


def GRAD(x, y):
    return np.array([3 * x**2 + 2 * y, 2 * x - 2 * y])


def HESS(x, y):
    return np.array([[6 * x, 2.0], [2.0, -2.0]])


# =============================================================================
# SCENE 1: QuadraticAlongDirection (ThreeDScene)
# =============================================================================
class QuadraticAlongDirection(ThreeDScene):
    def construct(self):
        px, py = 1.0, 1.0
        z0 = F(px, py)
        g = GRAD(px, py)
        H = HESS(px, py)
        assert z0 == 2 and list(g) == [5, 0] and H.tolist() == [[6, 2], [2, -2]]

        theta = -80 * DEGREES
        phi = 62 * DEGREES
        self.set_camera_orientation(phi=phi, theta=theta)
        right = np.array([-np.sin(theta), np.cos(theta), 0.0])

        axes = ThreeDAxes(
            x_range=[0, 2, 1], y_range=[0, 2, 1], z_range=[-4, 12, 4],
            x_length=3.6, y_length=3.0, z_length=2.5,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                         "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        # box centre to origin, then slide the whole scene left on screen
        centre = axes.c2p(1, 1, 4)
        axes.shift(-centre - 2.2 * right + DOWN * 0.1)

        def P(x, y, z=None, lift=0.0):
            return axes.c2p(x, y, (F(x, y) if z is None else z) + lift)

        surface = Surface(
            lambda u, v: P(u, v), u_range=[0, 2], v_range=[0, 2], resolution=(16, 16),
            stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3,
        )
        for face in surface.submobjects:
            face.set_fill(color=V_COLOR, opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.55)

        # labels and the marker for p are fixed-in-frame at the projected screen position,
        # so they are drawn on top and can never end up behind a sheet
        self.camera.rotation_matrix = self.camera.generate_rotation_matrix()

        def scr(pt):
            return self.camera.project_point(np.array(pt, dtype=float))

        p_dot = Dot(scr(P(px, py)), radius=0.09, color=INK).set_stroke(BG, 2)
        lab_x = tex("x", X_COLOR).move_to(scr(axes.c2p(2.0, 0, -4)) + DOWN * 0.4 + RIGHT * 0.3)
        lab_y = tex("y", Y_COLOR).move_to(scr(axes.c2p(0, 2.0, -4)) + LEFT * 0.4 + UP * 0.1)
        lab_f = tex("f", INK_DIM).move_to(scr(axes.c2p(0, 0, 12)) + UP * 0.35)
        lab_p = tex(r"\mathbf p", INK).move_to(scr(P(px, py)) + UP * 0.38 + LEFT * 0.3)

        # fixed-in-frame text
        head = VGroup(
            tex(r"f(x,y)=x^3+2xy-y^2", V_COLOR),
            tex(r"\mathbf p=(1,1)", INK),
        ).arrange(RIGHT, buff=0.5).to_corner(UL, buff=0.2)
        head = bg(head)

        def slice_curve(direction, color):
            d = np.array(direction)
            return ParametricFunction(
                lambda t: P(px + d[0] * t, py + d[1] * t, lift=0.25),
                t_range=[-1, 1], color=color, stroke_width=7,
            )

        # ---- right-hand panel: the 1D picture along the chosen direction ----
        def panel(direction, y_range, nums):
            d = np.array(direction)
            ax = Axes(
                x_range=[-1, 1, 1], y_range=y_range + [1],
                x_length=3.3, y_length=1.9,
                axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5,
                             "include_tip": False, "include_ticks": False,
                             "font_size": MIN_FONT},
                x_axis_config={"numbers_to_include": [-1, 1]},
                y_axis_config={"numbers_to_include": nums},
            ).move_to(RIGHT * 2.95 + UP * 1.2)
            for ax_ in ax.get_axes():
                for n in ax_.numbers:
                    n.set_color(INK_DIM)
            true = ax.plot(lambda t: F(px + d[0] * t, py + d[1] * t), x_range=[-1, 1], color=V_COLOR, stroke_width=4)
            lin = ax.plot(lambda t: z0 + g @ (d * t), x_range=[-1, 1], color=HIGHLIGHT, stroke_width=4)
            quad = ax.plot(lambda t: z0 + g @ (d * t) + 0.5 * (d * t) @ H @ (d * t),
                           x_range=[-1, 1], color=RESULT_COLOR, stroke_width=4)
            return ax, true, lin, quad

        def rows(hlabel, hcolor, direction):
            d = np.array(direction, dtype=float)
            slope = g @ d
            curv = 0.5 * d @ H @ d
            r0 = tex(hlabel, hcolor)
            r1 = tex(rf"\nabla f\cdot\mathbf h={coef(slope,1)}" if slope else r"\nabla f\cdot\mathbf h=0", HIGHLIGHT)
            r2 = tex(rf"\tfrac12\mathbf h^{{\top}}H\mathbf h={coef(curv,2)}", RESULT_COLOR)
            r0 = VGroup(r0, tex(r"f(\mathbf p+\mathbf h)", V_COLOR)).arrange(RIGHT, buff=0.35)
            grp = VGroup(r0, r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            grp.move_to(RIGHT * 2.95 + DOWN * 1.45)
            grp.align_to(RIGHT * 1.0, LEFT)
            return grp

        self.camera.add_fixed_in_frame_mobjects(head, p_dot, lab_x, lab_y, lab_f, lab_p)
        self.add(axes, surface, p_dot, head, lab_x, lab_y, lab_f, lab_p)
        self.wait(1.6)

        # ---- step 1: slice along x ----
        cx = slice_curve((1, 0), X_COLOR)
        ax1, tr1, li1, qu1 = panel((1, 0), [-1, 11], [0, 5, 10])
        rw1 = rows(r"\mathbf h=(t,0)", X_COLOR, (1, 0))
        self.camera.add_fixed_in_frame_mobjects(ax1, tr1, li1, qu1, rw1)
        for m in (ax1, tr1, li1, qu1, rw1):
            self.remove(m)
        self.play(Create(cx), run_time=1.5)
        self.play(FadeIn(ax1), FadeIn(rw1[0]), Create(tr1), run_time=1.5)
        self.wait(0.8)
        self.play(Create(li1), FadeIn(rw1[1]), run_time=1.5)
        self.wait(1.2)
        self.play(Create(qu1), FadeIn(rw1[2]), run_time=1.5)
        self.wait(1.8)

        # ---- step 2: slice along y ----
        self.play(*[FadeOut(m) for m in (cx, ax1, tr1, li1, qu1, rw1)], run_time=0.8)
        cy = slice_curve((0, 1), Y_COLOR)
        ax2, tr2, li2, qu2 = panel((0, 1), [0, 3], [1, 2, 3])
        rw2 = rows(r"\mathbf h=(0,t)", Y_COLOR, (0, 1))
        self.camera.add_fixed_in_frame_mobjects(ax2, tr2, li2, qu2, rw2)
        for m in (ax2, tr2, li2, qu2, rw2):
            self.remove(m)
        self.play(Create(cy), run_time=1.2)
        self.play(FadeIn(ax2), FadeIn(rw2[0]), Create(tr2), run_time=1.2)
        self.play(Create(li2), FadeIn(rw2[1]), run_time=1.2)
        self.wait(0.8)
        self.play(Create(qu2), FadeIn(rw2[2]), run_time=1.2)
        self.wait(1.8)

        # ---- step 3: the whole tangent plane, bent into the quadratic ----
        self.play(*[FadeOut(m) for m in (cy, ax2, tr2, li2, qu2, rw2)], run_time=0.8)
        r = 0.75
        ul = [px - r, px + r]
        vl = [py - r, py + r]

        def sheet(fn, color, op):
            s = Surface(lambda u, v: P(u, v, fn(u, v)), u_range=ul, v_range=vl, resolution=(10, 10),
                        stroke_color=color, stroke_width=0.6, stroke_opacity=0.6)
            for face in s.submobjects:
                face.set_fill(color=color, opacity=op)
            return s

        def plane_fn(u, v):
            return z0 + g @ np.array([u - px, v - py])

        def quad_fn(u, v):
            h = np.array([u - px, v - py])
            return z0 + g @ h + 0.5 * h @ H @ h

        plane = sheet(plane_fn, HIGHLIGHT, 0.8)
        bowl = sheet(quad_fn, RESULT_COLOR, 0.8)

        Hm = Matrix([[f"{int(H[0,0])}", f"{int(H[0,1])}"], [f"{int(H[1,0])}", f"{int(H[1,1])}"]],
                    element_to_mobject=lambda t: MathTex(t, font_size=MIN_FONT), h_buff=0.9, v_buff=0.6)
        Hlab = tex("H=")
        Hrow = VGroup(Hlab, Hm).arrange(RIGHT, buff=0.2).move_to(RIGHT * 3.2 + UP * 1.7)
        t1 = tex(r"f(\mathbf p)+\nabla f^{\top}\mathbf h", HIGHLIGHT)
        t1n = tex(rf"={int(z0)}+{int(g[0])}h_1", HIGHLIGHT)
        t2 = tex(r"+\tfrac12\mathbf h^{\top}H\mathbf h", RESULT_COLOR)
        t2n = tex(r"=3h_1^2+2h_1h_2-h_2^2", RESULT_COLOR)
        # numbers from H: 1/2 h^T H h = (H00/2) h1^2 + H01 h1 h2 + (H11/2) h2^2
        assert (H[0, 0] / 2, H[0, 1], H[1, 1] / 2) == (3, 2, -1)
        side = VGroup(t1, t1n, t2, t2n).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        side.move_to(RIGHT * 2.95 + DOWN * 0.55).align_to(RIGHT * 0.95, LEFT)
        self.camera.add_fixed_in_frame_mobjects(Hrow, t1, t1n, t2, t2n)
        for m in (Hrow, t1, t1n, t2, t2n):
            self.remove(m)

        self.play(surface.animate.set_opacity(0.18), run_time=0.6)
        self.play(FadeIn(plane), FadeIn(t1), run_time=1.5)
        self.play(FadeIn(t1n), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(Hrow), run_time=0.8)
        self.play(Transform(plane, bowl), FadeIn(t2), run_time=2.0)
        self.play(FadeIn(t2n), run_time=0.8)
        self.wait(4.0)


# =============================================================================
# SCENE 2: CriticalPoints (ThreeDScene): fixed camera, same view for all three
# =============================================================================
class CriticalPoints(ThreeDScene):
    def construct(self):
        theta, phi = -65 * DEGREES, 66 * DEGREES
        self.set_camera_orientation(phi=phi, theta=theta)
        s = 0.5
        R = 1.1
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 1.0], y_range=[-1.5, 1.5, 1.0], z_range=[-1.5, 1.5, 1.0],
            x_length=4.6, y_length=4.6, z_length=2.5,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                         "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.shift(DOWN * 0.15)

        self.camera.rotation_matrix = self.camera.generate_rotation_matrix()
        scr = lambda pt: self.camera.project_point(np.array(pt, dtype=float))
        lab_x = tex("x", X_COLOR).move_to(scr(axes.c2p(1.6, 0, 0)) + RIGHT * 0.25 + DOWN * 0.1)
        lab_y = tex("y", Y_COLOR).move_to(scr(axes.c2p(0, -1.9, 0)) + LEFT * 0.3 + DOWN * 0.2)

        def make_surface(fn):
            surf = Surface(lambda u, v: axes.c2p(u, v, fn(u, v)), u_range=[-R, R], v_range=[-R, R],
                           resolution=(16, 16), stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3)
            for face in surf.submobjects:
                face.set_fill(color=V_COLOR, opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60)
            return surf

        def curves(a, b):
            cx = ParametricFunction(lambda t: axes.c2p(t, 0, a * t**2 + 0.04), t_range=[-R, R],
                                    color=X_COLOR, stroke_width=6)
            cy = ParametricFunction(lambda t: axes.c2p(0, t, b * t**2 + 0.04), t_range=[-R, R],
                                    color=Y_COLOR, stroke_width=6)
            return VGroup(cx, cy)

        cases = {
            "min": (s, s, "minimum"),
            "max": (-s, -s, "maximum"),
            "saddle": (s, -s, "saddle"),
        }
        surfs = {k: make_surface(lambda u, v, a=a, b=b: a * u**2 + b * v**2) for k, (a, b, _) in cases.items()}
        crvs = {k: curves(a, b) for k, (a, b, _) in cases.items()}

        def card(key):
            a, b, name = cases[key]
            h1, h2 = 2 * a, 2 * b  # H = diag(2a, 2b), eigenvalues are its entries
            sg = lambda v: ">0" if v > 0 else "<0"
            m = tex(rf"\text{{{name}: }}H=\mathrm{{diag}}({h1:g},{h2:g}),\ \lambda_1{sg(h1)},\ \lambda_2{sg(h2)}")
            return bg(m).to_corner(UL, buff=0.2)

        cards = {k: card(k) for k in cases}
        self.camera.add_fixed_in_frame_mobjects(*cards.values())
        for k in ("max", "saddle"):
            self.remove(cards[k])

        origin_dot = Dot3D(point=axes.c2p(0, 0, 0.04), radius=0.07, color=RESULT_COLOR)
        self.add(axes, surfs["min"], crvs["min"], origin_dot, cards["min"])
        self.camera.add_fixed_in_frame_mobjects(lab_x, lab_y)
        self.add(lab_x, lab_y)
        self.wait(3.0)
        for prev, nxt in (("min", "max"), ("max", "saddle")):
            self.play(FadeOut(cards[prev]), run_time=0.4)
            self.play(Transform(surfs["min"], surfs[nxt]), Transform(crvs["min"], crvs[nxt]), run_time=1.8)
            self.play(FadeIn(cards[nxt]), run_time=0.6)
            self.wait(3.0)
        self.wait(1.0)


# =============================================================================
# SCENE 3: CurvatureAllDirections (2D): f = xy, curvature u^T H u = sin 2theta
# =============================================================================
class CurvatureAllDirections(Scene):
    def construct(self):
        H = np.array([[0.0, 1.0], [1.0, 0.0]])  # Hessian of f = xy
        evals, evecs = np.linalg.eigh(H)       # ascending: -1, +1
        lam_dn, lam_up = evals
        v_dn, v_up = evecs[:, 0], evecs[:, 1]
        assert abs(lam_up - 1) < 1e-9 and abs(lam_dn + 1) < 1e-9

        title = bg(tex(r"f(x,y)=xy,\quad H=\begin{bmatrix}0&1\\1&0\end{bmatrix}", V_COLOR)).to_edge(UP, buff=0.2)

        # left: contour map
        L = 1.7
        mp = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=2 * L, y_length=2 * L,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2, "include_ticks": False,
                               "include_tip": False}).move_to(LEFT * 2.8 + DOWN * 0.45)
        xl = tex("x", X_COLOR).next_to(mp.c2p(2, 0), DOWN, buff=0.05).shift(LEFT * 0.1)
        yl = tex("y", Y_COLOR).next_to(mp.c2p(0, 2), RIGHT, buff=0.08)
        contours = VGroup()
        for c in [0.5, 1.5, -0.5, -1.5]:
            x0 = max(abs(c) / 1.95, 0.2)
            for sgn in (1, -1):
                xr = [x0, 1.95] if sgn > 0 else [-1.95, -x0]
                contours.add(mp.plot(lambda x, c=c: c / x, x_range=xr, color=INK_FAINT, stroke_width=2))
        circle = Circle(radius=L * 0.55, color=INK_FAINT, stroke_width=2).move_to(mp.c2p(0, 0))
        ur = L * 0.55  # screen length of the unit vector

        th = ValueTracker(0.0)

        def u_vec(a):
            return np.array([np.cos(a), np.sin(a)])

        def arrow(a, color):
            o = mp.c2p(0, 0)
            return Arrow(o, o + ur * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=color,
                         stroke_width=7, max_tip_length_to_length_ratio=0.25)

        u_arrow = always_redraw(lambda: arrow(th.get_value(), W_COLOR))
        u_lab = always_redraw(lambda: tex(r"\mathbf u", W_COLOR).move_to(
            mp.c2p(0, 0) + (ur + 0.38) * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])))

        def curv(a):
            u = u_vec(a)
            return float(u @ H @ u)

        # right: plot of curvature against theta
        pl = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[-1, 1, 1], x_length=4.0, y_length=1.8,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5, "include_tip": False,
                               "include_ticks": False}).move_to(RIGHT * 2.6 + UP * 0.3)
        ticks = VGroup()
        for val, lab in [(PI, r"\pi"), (2 * PI, r"2\pi")]:
            ticks.add(tex(lab, INK_DIM).next_to(pl.c2p(val, 0), DOWN, buff=0.1))
        for val, lab in [(1, "1"), (-1, "-1")]:
            ticks.add(tex(lab, INK_DIM).next_to(pl.c2p(0, val), LEFT, buff=0.1))
        th_lab = tex(r"\theta", INK_DIM).next_to(pl.c2p(2 * PI, 0), UP, buff=0.05).shift(LEFT * 0.15)
        full = pl.plot(lambda a: curv(a), x_range=[0, 2 * PI], color=INK_FAINT, stroke_width=3)
        drawn = always_redraw(lambda: pl.plot(lambda a: curv(a), x_range=[0, max(th.get_value() % (2 * PI) if th.get_value() < 2 * PI else 2 * PI, 0.001)],
                                              color=RESULT_COLOR, stroke_width=5))
        dot = always_redraw(lambda: Dot(pl.c2p(th.get_value() % (2 * PI), curv(th.get_value())), radius=0.1, color=HIGHLIGHT))

        read_lab = tex(r"\mathbf u^{\top}H\,\mathbf u=", RESULT_COLOR)
        read_num = DecimalNumber(0.0, num_decimal_places=2, include_sign=True, font_size=MIN_FONT, color=RESULT_COLOR)
        read = VGroup(read_lab, read_num).arrange(RIGHT, buff=0.15).move_to(RIGHT * 2.6 + DOWN * 1.35)
        read_num.add_updater(lambda m: m.set_value(curv(th.get_value())).next_to(read_lab, RIGHT, buff=0.15))
        read2 = tex(r"=\sin 2\theta", INK_DIM).next_to(read, DOWN, buff=0.12).align_to(read, LEFT)

        self.add(title, mp, xl, yl, contours, circle, u_arrow, u_lab, pl, ticks, th_lab, full, drawn, dot, read, read2)
        self.wait(2.0)

        # step 1: u makes one full turn
        self.play(th.animate.set_value(2 * PI), run_time=8.0, rate_func=linear)
        self.wait(0.8)

        # step 2: freeze at the extremes
        notes = VGroup()

        def freeze(a, color, vec_note, plot_note, pos):
            arr = arrow(a, color)
            mk = Dot(pl.c2p(a % (2 * PI), curv(a)), radius=0.1, color=color)
            note = tex(plot_note, color).move_to(pos)
            vn = tex(vec_note, color)
            return arr, mk, note

        base = 2 * PI
        # 45 degrees: curves up the most
        self.play(th.animate.set_value(base + PI / 4), run_time=1.5)
        a1, m1, n1 = freeze(PI / 4, X_COLOR, "", rf"\lambda_1=+{lam_up:.0f}", pl.c2p(PI / 4, 1) + RIGHT * 1.0 + UP * 0.12)
        self.add(a1, m1)
        self.play(FadeIn(n1), run_time=0.6)
        self.wait(1.5)
        self.play(th.animate.set_value(base + 3 * PI / 4), run_time=1.5)
        a2, m2, n2 = freeze(3 * PI / 4, Y_COLOR, "", rf"\lambda_2={lam_dn:.0f}", pl.c2p(3 * PI / 4, -1) + RIGHT * 1.0 + DOWN * 0.12)
        self.add(a2, m2)
        self.play(FadeIn(n2), run_time=0.6)
        self.wait(1.5)
        self.play(th.animate.set_value(2 * base), run_time=1.5)
        n3 = tex("0", INK_DIM).move_to(pl.c2p(0, 0) + DOWN * 0.35 + RIGHT * 0.3)
        m3 = Dot(pl.c2p(0, 0), radius=0.1, color=INK_DIM)
        self.add(m3)
        self.play(FadeIn(n3), run_time=0.6)
        self.wait(1.5)

        # step 3: the statement
        self.play(FadeOut(u_arrow), FadeOut(u_lab), run_time=0.4)
        a1e = arrow(PI / 4, X_COLOR)
        a2e = arrow(3 * PI / 4, Y_COLOR)
        self.add(a1e, a2e)
        self.remove(a1, a2)
        final = bg(tex(r"\lambda_{\max},\lambda_{\min}\ =\ \text{extremes of }\mathbf u^{\top}H\,\mathbf u,\ \text{at the eigenvectors}", HIGHLIGHT, 38))
        final.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(final), run_time=1.0)
        self.wait(4.0)


# =============================================================================
# SCENE 4: CriticalPointsNumbers (2D): f = x^3 + 2xy - y^2
# =============================================================================
class CriticalPointsNumbers(Scene):
    def construct(self):
        # critical points from the real equations: 3x^2+2y=0, 2x-2y=0 -> y=x, 3x^2+2x=0
        xs = np.roots([3, 2, 0])
        pts = sorted([(float(x.real), float(x.real)) for x in xs], key=lambda p: -p[0])
        assert len(pts) == 2 and abs(pts[1][0] + 2 / 3) < 1e-9
        for (x, y) in pts:
            assert np.allclose(GRAD(x, y), 0)

        title = bg(tex(r"f=x^3+2xy-y^2,\quad \nabla f=\mathbf 0\ \text{at}\ (0,0),\ (-\tfrac23,-\tfrac23)", V_COLOR, 38)).to_edge(UP, buff=0.15)

        lo, hi = -1.5, 1.0
        S = 3.8
        mp = Axes(x_range=[lo, hi, 1], y_range=[lo, hi, 1], x_length=S, y_length=S,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2, "include_tip": False,
                               "include_ticks": True, "tick_size": 0.05}).move_to(LEFT * 3.0 + DOWN * 0.4)
        mp.x_axis.add_labels({-1: MathTex("-1", font_size=MIN_FONT), 1: MathTex("1", font_size=MIN_FONT)})
        mp.y_axis.add_labels({-1: MathTex("-1", font_size=MIN_FONT), 1: MathTex("1", font_size=MIN_FONT)})
        for ax_ in mp.get_axes():
            for m in ax_.labels:
                m.set_color(INK_DIM)
        xl = tex("x", X_COLOR).next_to(mp.c2p(hi, 0), UP, buff=0.05).shift(LEFT * 0.12)
        yl = tex("y", Y_COLOR).next_to(mp.c2p(0, hi), RIGHT, buff=0.08)

        contours = VGroup()
        for c in [-2.0, -1.0, -0.4, 0.0, 0.1]:
            try:
                cv = mp.plot_implicit_curve(lambda x, y, c=c: F(x, y) - c, color=INK_FAINT, stroke_width=2)
                contours.add(cv)
            except Exception as e:  # pragma: no cover
                print("contour fail", c, e)

        # gradient field: short amber arrows
        field = VGroup()
        for gx in np.linspace(-1.3, 0.8, 6):
            for gy in np.linspace(-1.3, 0.8, 6):
                gv = GRAD(gx, gy)
                n = np.linalg.norm(gv)
                if n < 1e-6:
                    continue
                ln = 0.3
                o = mp.c2p(gx, gy)
                dirv = np.array([gv[0], gv[1], 0]) / n
                field.add(Arrow(o - dirv * ln / 2, o + dirv * ln / 2, buff=0, color=RESULT_COLOR, stroke_width=3,
                                max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20))

        dots = [Dot(mp.c2p(*p), radius=0.1, color=HIGHLIGHT).set_z_index(5) for p in pts]
        rings = [Circle(radius=0.2, color=HIGHLIGHT, stroke_width=3).move_to(d) for d in dots]

        def eigen_block(p, name, y_c):
            Hn = HESS(*p)
            ev, vec = np.linalg.eigh(Hn)
            ev, vec = ev[::-1], vec[:, ::-1]  # descending
            Hn_str = [[f"{Hn[i,j]:.0f}" for j in range(2)] for i in range(2)]
            m = Matrix(Hn_str, element_to_mobject=lambda t: MathTex(t, font_size=MIN_FONT), h_buff=0.85, v_buff=0.55)
            if ev[1] > 0:
                kind, kc = "minimum", V_COLOR
            elif ev[0] < 0:
                kind, kc = "maximum", V_COLOR
            else:
                kind, kc = "saddle", V_COLOR
            col = lambda v: X_COLOR if v > 0 else Y_COLOR
            r1 = VGroup(tex(name + r"\ \Rightarrow"), tex(r"\text{" + kind + "}", HIGHLIGHT)).arrange(RIGHT, buff=0.2)
            lams = VGroup(
                tex(rf"\lambda_1={ev[0]:.2f}", col(ev[0])),
                tex(rf"\lambda_2={ev[1]:.2f}", col(ev[1])),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            r2 = VGroup(tex("H="), m, lams).arrange(RIGHT, buff=0.2)
            blk = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            blk.move_to(RIGHT * 2.45 + UP * y_c)
            blk.align_to(RIGHT * -0.95, LEFT)
            # eigen-direction arrows on the map
            arrs = VGroup()
            for k in range(2):
                o = mp.c2p(*p)
                d = np.array([vec[0, k], vec[1, k], 0.0])
                d = d * 0.55
                # keep direction readable on the map: map axes share the same scale
                arrs.add(Arrow(o - d, o + d, buff=0, color=col(ev[k]), stroke_width=6,
                               max_tip_length_to_length_ratio=0.2).set_z_index(4))
            return blk, arrs, ev

        blkA, arrA, evA = eigen_block(pts[0], "(0,0)", 0.95)
        blkB, arrB, evB = eigen_block(pts[1], r"(-\tfrac23,-\tfrac23)", -1.2)
        assert abs(evA[0] - (-1 + np.sqrt(5))) < 1e-9 and abs(evB[1] - (-3 - np.sqrt(5))) < 1e-9

        self.add(title, mp, xl, yl, contours, field)
        self.play(FadeIn(VGroup(*dots)), *[Create(r) for r in rings], run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(field), run_time=0.8)
        self.play(FadeIn(blkA), Create(arrA), run_time=1.5)
        self.wait(4.0)
        self.play(FadeIn(blkB), Create(arrB), run_time=1.5)
        self.wait(5.0)


# =============================================================================
# SCENE 4: Convexity (2D)
# =============================================================================
class Convexity(Scene):
    def construct(self):
        caption_def = bg(tex(r"f(t\,a + (1-t)\,b) \le t\,f(a) + (1-t)\,f(b)")).move_to(UP * 2.3)
        caption_min = bg(
            tex(r"\text{convex} \Rightarrow \text{every local minimum is global}", RESULT_COLOR)
        ).move_to(UP * 2.3)

        axes = Axes(
            x_range=[-2.3, 2.3, 1],
            y_range=[0, 3.2, 1],
            x_length=7.4,
            y_length=3.9,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
                "include_tip": False,
            },
        ).move_to(DOWN * 0.5)
        x_label = bg(tex("x", X_COLOR)).next_to(axes.c2p(2.3, 0), RIGHT, buff=0.08)
        f_label = bg(tex("f", INK_DIM)).next_to(axes.c2p(0, 3.2), LEFT, buff=0.1)

        def f_conv(x):
            return 0.3 * x**2 + 0.04 * x**4 + 0.3

        def g_non(x):
            return 0.22 * x**4 - 1.1 * x**2 + 0.2 * x + 2.5

        m = ValueTracker(0.0)  # 0 = convex function, 1 = two-basin function

        def F(x):
            k = m.get_value()
            return (1 - k) * f_conv(x) + k * g_non(x)

        curve = always_redraw(
            lambda: axes.plot(F, x_range=[-2.2, 2.2], color=V_COLOR, stroke_width=4)
        )

        a_val = ValueTracker(-1.8)
        b_val = ValueTracker(1.8)

        def chord_color():
            return interpolate_color(ManimColor(RESULT_COLOR), ManimColor(Y_COLOR), m.get_value())

        def pa():
            return axes.c2p(a_val.get_value(), F(a_val.get_value()))

        def pb():
            return axes.c2p(b_val.get_value(), F(b_val.get_value()))

        chord = always_redraw(lambda: Line(pa(), pb(), color=chord_color(), stroke_width=5))
        dots = always_redraw(
            lambda: VGroup(
                Dot(pa(), radius=0.09, color=chord_color()),
                Dot(pb(), radius=0.09, color=chord_color()),
            )
        )

        lab_pos = axes.c2p(1.5, 2.95)
        label_conv = bg(tex(r"\text{convex}", V_COLOR)).move_to(lab_pos)
        label_non = bg(tex(r"\text{non-convex}", V_COLOR)).move_to(lab_pos)

        # the single minimum of the convex bowl
        dot_min = Dot(axes.c2p(0, f_conv(0)), radius=0.1, color=RESULT_COLOR)
        lab_min = bg(tex(r"\text{only minimum}", RESULT_COLOR)).next_to(dot_min, UP, buff=0.3).shift(RIGHT * 1.1)

        self.add(axes, x_label, f_label, curve, label_conv, chord, dots, caption_def)
        self.wait(1.5)

        self.play(a_val.animate.set_value(-0.8), b_val.animate.set_value(2.0), run_time=2.2)
        self.play(a_val.animate.set_value(-2.0), b_val.animate.set_value(0.6), run_time=2.2)
        self.play(a_val.animate.set_value(-1.6), b_val.animate.set_value(1.6), run_time=1.6)
        self.wait(0.6)

        self.play(FadeOut(label_conv), run_time=0.4)
        self.play(m.animate.set_value(1.0), run_time=2.5)
        self.play(FadeIn(label_non), run_time=0.5)
        self.wait(2.0)

        self.play(FadeOut(chord), FadeOut(dots), FadeOut(label_non), FadeOut(caption_def), run_time=0.8)
        self.play(m.animate.set_value(0.0), run_time=2.0)
        self.play(FadeIn(label_conv), FadeIn(dot_min), FadeIn(lab_min), FadeIn(caption_min), run_time=1.2)
        self.wait(4.0)


# =============================================================================
# SCENE 5: ConvexAlongEveryLine (2D): chord test in each direction
# =============================================================================
class ConvexAlongEveryLine(Scene):
    def construct(self):
        def panel(cx, ylo, yhi, ticks):
            ax = Axes(x_range=[-1.5, 1.5, 1], y_range=[ylo, yhi, 1], x_length=3.6, y_length=2.0,
                      axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5, "include_tip": False,
                                   "include_ticks": False}).move_to(RIGHT * cx + DOWN * 0.35)
            return ax

        def build(Hd, cases):
            """cases: list of (cx, label, colour, coefficient of t^2)."""
            grp = VGroup()
            out = []
            for cx, name, ncol, c in cases:
                ax = panel(cx, -2.3, 2.3, None)
                curve = ax.plot(lambda t, c=c: c * t * t, x_range=[-1.4, 1.4], color=V_COLOR, stroke_width=4)
                ta, tb = -1.1, 1.1
                A = ax.c2p(ta, c * ta * ta)
                B = ax.c2p(tb, c * tb * tb)
                chord = Line(A, B, color=RESULT_COLOR, stroke_width=5)
                da, db = Dot(A, radius=0.09, color=RESULT_COLOR), Dot(B, radius=0.09, color=RESULT_COLOR)
                # chord height vs curve height at the midpoint tells above/below
                mid_chord = c * ta * ta  # symmetric endpoints: chord is flat at c*1.21
                above = mid_chord >= 0
                verdict = tex(r"\text{chord above}" if above else r"\text{chord below}", X_COLOR if above else Y_COLOR)
                verdict.next_to(ax, DOWN, buff=0.25)
                lab = tex(name, ncol).next_to(ax, UP, buff=0.15)
                out.append((ax, curve, chord, VGroup(da, db), verdict, lab, above))
            return out

        def header(fx, Hd):
            return bg(tex(rf"f={fx},\quad H=\mathrm{{diag}}({Hd[0]:g},{Hd[1]:g})", V_COLOR)).to_edge(UP, buff=0.2)

        def run_case(fx, Hd, last):
            c1, c2 = Hd[0] / 2, Hd[1] / 2  # f(t,0)=c1 t^2, f(0,t)=c2 t^2
            hd = header(fx, Hd)
            items = build(Hd, [(-2.55, r"\mathbf h=(t,0)", X_COLOR, c1), (2.55, r"\mathbf h=(0,t)", Y_COLOR, c2)])
            return hd, items

        # ---- f = x^2 - y^2 ----
        hd, items = run_case("x^2-y^2", (2, -2), False)
        (ax1, cu1, ch1, dt1, v1, l1, ab1), (ax2, cu2, ch2, dt2, v2, l2, ab2) = items
        assert ab1 and not ab2
        self.add(hd, ax1, cu1, l1, ax2, cu2, l2)
        self.wait(1.5)
        self.play(Create(ch1), FadeIn(dt1), run_time=1.0)
        self.play(FadeIn(v1), run_time=0.6)
        self.wait(1.5)
        self.play(Create(ch2), FadeIn(dt2), run_time=1.0)
        self.play(FadeIn(v2), run_time=0.6)
        self.wait(1.2)
        verdict_a = bg(tex(r"\text{one direction fails}\Rightarrow\text{not convex}", Y_COLOR)).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(verdict_a), run_time=0.8)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in (hd, ax1, cu1, l1, ch1, dt1, v1, ax2, cu2, l2, ch2, dt2, v2, verdict_a)], run_time=0.8)

        # ---- f = x^2 + y^2 ----
        hd, items = run_case("x^2+y^2", (2, 2), True)
        (ax1, cu1, ch1, dt1, v1, l1, ab1), (ax2, cu2, ch2, dt2, v2, l2, ab2) = items
        assert ab1 and ab2
        self.add(hd, ax1, cu1, l1, ax2, cu2, l2)
        self.wait(1.0)
        self.play(Create(ch1), FadeIn(dt1), Create(ch2), FadeIn(dt2), run_time=1.2)
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.6)
        verdict_b = bg(tex(r"\text{every direction passes}\Rightarrow\text{convex},\ H\succeq 0", X_COLOR)).to_edge(DOWN, buff=0.15)
        self.wait(1.2)
        self.play(FadeIn(verdict_b), run_time=0.8)
        self.wait(3.5)
