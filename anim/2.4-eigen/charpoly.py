"""Block 2.4: eigenvectors keep their line; eigenvalues are where A - lambda I squashes space.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.14 (eigenvectors and eigenvalues).
Both scenes use the deck's matrix A = [[4, 1], [2, 3]] (eigenvalues 5 and 2,
eigenvectors (1, 1) and (1, -2)).
"""

from shared.anim.house import *
from shared.anim.linmap import *

A = np.array([[4.0, 1.0], [2.0, 3.0]])
EVALS, EVECS = np.linalg.eig(A)
_o = np.argsort(EVALS)[::-1]
LAM1, LAM2 = EVALS[_o]
V1 = np.array([1.0, 1.0])
V2 = np.array([1.0, -2.0])
assert np.allclose(A @ V1, LAM1 * V1) and np.allclose(A @ V2, LAM2 * V2)
assert np.isclose(LAM1, 5) and np.isclose(LAM2, 2)


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def arrow3(start, end, colour, width=6, tip=0.16):
    if np.linalg.norm(np.asarray(end) - np.asarray(start)) < 0.03:
        return VGroup()
    return Arrow(start, end, buff=0, color=colour, stroke_width=width,
                 max_tip_length_to_length_ratio=0.35, tip_length=tip)


class EigenLines(Scene):
    """A turns almost every arrow off its line; (1,1) and (1,-2) only stretch."""

    def construct(self):
        U = 0.5
        plane = lin_plane(U)

        def sc(v):
            return np.array([v[0] * U, v[1] * U, 0.0])

        R = 1.2
        eig_angles = [np.degrees(np.arctan2(V1[1], V1[0])), np.degrees(np.arctan2(V2[1], V2[0]))]
        generic = [36.0 * k for k in range(10)]
        vecs = []
        for a in generic:
            vecs.append(R * np.array([np.cos(np.radians(a)), np.sin(np.radians(a))]))
        v1 = R * V1 / np.linalg.norm(V1)
        v2 = R * V2 / np.linalg.norm(V2)
        # the generic arrows keep a clear angular gap to both eigen-directions
        for a in generic:
            for e in eig_angles:
                assert abs(((a - e + 180) % 360) - 180) > 8, (a, e)
        vecs_all = vecs + [v1, v2]

        t = ValueTracker(0.0)  # 0 = identity, 1 = A, so arrows move along the true linear path

        def img(v, s):
            return (np.eye(2) + s * (A - np.eye(2))) @ v

        ghosts = VGroup(*[arrow3(ORIGIN, sc(v), INK_DIM, width=4, tip=0.13) for v in vecs])
        g1 = arrow3(ORIGIN, sc(v1), INK_DIM, width=4, tip=0.13)
        g2 = arrow3(ORIGIN, sc(v2), INK_DIM, width=4, tip=0.13)

        def mover(v, colour=RESULT_COLOR):
            return always_redraw(lambda: arrow3(ORIGIN, sc(img(v, t.get_value())), colour, width=5, tip=0.14))

        movers = [mover(v) for v in vecs]
        m1, m2 = mover(v1), mover(v2)

        L = 2.7
        d1 = DashedLine(sc(-V1 / np.linalg.norm(V1) * L / U * 0.98), sc(V1 / np.linalg.norm(V1) * L / U * 0.98),
                        color=V_COLOR, stroke_width=3)
        k2 = 2.65 / abs(V2[1])
        d2 = DashedLine(sc(-V2 * k2), sc(V2 * k2), color=W_COLOR, stroke_width=3)

        self.add(plane, ghosts, g1, g2)
        self.wait(1.5)

        # step 1: apply A to every arrow
        self.add(*movers, m1, m2)
        self.play(t.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.remove(*movers, m1, m2)  # freeze: always_redraw would reset any later fade
        finals = VGroup(*[arrow3(ORIGIN, sc(A @ v), RESULT_COLOR, width=4, tip=0.13) for v in vecs])
        self.add(finals)
        self.wait(1.5)

        # step 2: the two lines
        self.play(Create(d1), Create(d2), g1.animate.set_color(V_COLOR), g2.animate.set_color(W_COLOR),
                  run_time=1.5)
        self.add(g1, g2)
        self.wait(1.5)

        # step 3: replay just the two eigenvectors, labelled with their stretch
        others = VGroup(ghosts, finals)
        self.play(others.animate.set_opacity(0.12), run_time=1)
        s = ValueTracker(1.0)

        def img_s(v):
            return arrow3(ORIGIN, sc(img(v, s.get_value())), RESULT_COLOR, width=6, tip=0.16)

        n1 = always_redraw(lambda: img_s(v1))
        n2 = always_redraw(lambda: img_s(v2))
        self.add(n1, n2, g1, g2)
        self.play(s.animate.set_value(0.0), run_time=1.2)
        lab1 = tex(r"\times 5", RESULT_COLOR)
        lab2 = tex(r"\times 2", RESULT_COLOR)
        lab1.move_to(sc(A @ v1) + np.array([0.55, -0.55, 0]))
        lab2.move_to(sc(A @ v2) + np.array([0.7, 0.0, 0]))
        label_box(lab1)
        label_box(lab2)
        self.play(s.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.5)
        self.wait(1)

        e1 = MathTex(r"A\mathbf{v}_1", "=", "5", r"\mathbf{v}_1", font_size=MIN_FONT, color=INK)
        e1[0].set_color(RESULT_COLOR)
        e1[2].set_color(RESULT_COLOR)
        e1[3].set_color(V_COLOR)
        e1.to_corner(UL, buff=0.25)
        e2 = MathTex(r"A\mathbf{v}_2", "=", "2", r"\mathbf{v}_2", font_size=MIN_FONT, color=INK)
        e2[0].set_color(RESULT_COLOR)
        e2[2].set_color(RESULT_COLOR)
        e2[3].set_color(W_COLOR)
        e2.to_corner(DR, buff=0.25)
        label_box(e1)
        label_box(e2)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.8)
        self.wait(2.5)


class DetHitsZero(Scene):
    """The parallelogram of A - lambda I collapses exactly at the roots of det(A - lambda I)."""

    def construct(self):
        U = 0.5
        O = np.array([-2.6, -0.1, 0.0])
        left = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], x_length=8 * U, y_length=8 * U,
            background_line_style={"stroke_color": GRID, "stroke_width": 2, "stroke_opacity": 0.8},
            axis_config={"stroke_color": INK_DIM, "stroke_width": 3}, faded_line_ratio=1)
        left.move_to(O)

        lam = ValueTracker(0.0)

        def cols():
            l = lam.get_value()
            M = A - l * np.eye(2)
            return M[:, 0], M[:, 1]

        def det_now():
            c1, c2 = cols()
            return c1[0] * c2[1] - c1[1] * c2[0]

        def pt(v):
            return O + np.array([v[0] * U, v[1] * U, 0.0])

        def para():
            c1, c2 = cols()
            return Polygon(pt([0, 0]), pt(c1), pt(c1 + c2), pt(c2), stroke_width=2,
                           stroke_color=RESULT_COLOR, fill_color=RESULT_COLOR, fill_opacity=0.35)

        def arrow(c, colour):
            if np.linalg.norm(c) < 0.03:
                return VGroup()
            return Arrow(pt([0, 0]), pt(c), buff=0, color=colour, stroke_width=6,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.16)

        P = always_redraw(para)
        a1 = always_redraw(lambda: arrow(cols()[0], X_COLOR))
        a2 = always_redraw(lambda: arrow(cols()[1], Y_COLOR))

        # right-hand plot of p(lambda) = det(A - lambda I)
        XMAX = 6
        axes = Axes(x_range=[0, XMAX, 1], y_range=[-3, 11, 1], x_length=3.6, y_length=3.0,
                    axis_config={"stroke_color": INK_DIM, "stroke_width": 3, "include_ticks": False,
                                 "include_tip": False})
        axes.move_to([2.55, -0.55, 0])
        p = lambda l: (4 - l) * (3 - l) - 2.0
        assert np.isclose(p(2), 0) and np.isclose(p(5), 0) and np.isclose(p(0), 10)
        curve = axes.plot(p, x_range=[0, XMAX], color=INK, stroke_width=5)
        zero_line = DashedLine(axes.c2p(0, 0), axes.c2p(XMAX, 0), color=INK_FAINT, stroke_width=2)
        dot = always_redraw(lambda: Dot(axes.c2p(lam.get_value(), p(lam.get_value())),
                                        radius=0.1, color=RESULT_COLOR))
        xt = VGroup(*[tex(str(k), INK_DIM).scale(0.8).move_to(axes.c2p(k, 0) + DOWN * 0.0) for k in (0, 2, 5)])
        for k, m in zip((0, 2, 5), xt):
            m.move_to(axes.c2p(k, -3.0) + DOWN * 0.3 + UP * 0.0)
        yt = VGroup(tex("10", INK_DIM).scale(0.8).next_to(axes.c2p(0, 10), LEFT, buff=0.1),
                    tex("0", INK_DIM).scale(0.8).next_to(axes.c2p(0, 0), LEFT, buff=0.1))
        # lambda axis label
        lam_ax = tex(r"\lambda", INK_DIM).next_to(axes.c2p(XMAX, -3.0), DOWN, buff=0.1).shift(LEFT * 0.0)
        lam_ax.move_to(axes.c2p(XMAX, -3.0) + np.array([0.1, -0.3, 0]))

        formula = tex(r"p(\lambda)=(5-\lambda)(2-\lambda)")
        formula.to_corner(UR, buff=0.25)
        label_box(formula)

        def lam_ro():
            lab = tex(r"\lambda=")
            num = DecimalNumber(lam.get_value(), num_decimal_places=2, font_size=MIN_FONT, color=INK)
            g = VGroup(lab, num).arrange(RIGHT, buff=0.12)
            g.to_corner(UL, buff=0.25)
            label_box(g)
            return g

        def det_ro():
            d = det_now()
            near = abs(d) < 0.005
            lab = tex(r"\det=", HIGHLIGHT if near else INK)
            num = DecimalNumber(0.0 if near else d, num_decimal_places=2, font_size=MIN_FONT,
                                color=HIGHLIGHT if near else INK)
            g = VGroup(lab, num).arrange(RIGHT, buff=0.12)
            g.next_to(formula, DOWN, buff=0.15, aligned_edge=RIGHT)
            label_box(g)
            return g

        ro = always_redraw(lam_ro)
        dro = always_redraw(det_ro)
        tag = tex(r"A-\lambda I", INK_DIM)
        tag.to_corner(DL, buff=0.25)
        label_box(tag)

        self.add(left, P, a1, a2, axes, zero_line, curve, xt, yt, lam_ax, dot, formula, ro, dro, tag)
        self.wait(1.2)

        def root(r):
            d = Dot(axes.c2p(r, 0), radius=0.1, color=HIGHLIGHT)
            return d

        roots = []
        for r in (2.0, 5.0):
            self.play(lam.animate.set_value(r), run_time=4, rate_func=smooth)
            rd = root(r)
            roots.append(rd)
            self.play(Flash(dot, color=HIGHLIGHT, flash_radius=0.35), FadeIn(rd),
                      P.animate.set_stroke(HIGHLIGHT, width=5), run_time=0.8)
            self.wait(1.4)
            if r == 2.0:
                self.play(P.animate.set_stroke(RESULT_COLOR, width=2), run_time=0.4)

        # payoff at lambda = 5: the kernel vector is sent to zero
        M5 = A - 5 * np.eye(2)
        s = ValueTracker(0.0)
        v = np.array([1.0, 1.0])
        kv = always_redraw(lambda: arrow((np.eye(2) + s.get_value() * (M5 - np.eye(2))) @ v, V_COLOR))
        kv_lab = tex(r"\mathbf{v}_1", V_COLOR)
        kv_lab.move_to(pt(v) + np.array([0.35, 0.3, 0]))
        label_box(kv_lab)
        self.play(FadeOut(tag), FadeIn(kv), FadeIn(kv_lab), run_time=0.8)
        self.wait(1)
        self.play(s.animate.set_value(1.0), FadeOut(kv_lab), run_time=2.5, rate_func=smooth)
        end = MathTex(r"(A-5I)", r"\mathbf{v}_1", "=", r"\mathbf{0}", font_size=MIN_FONT, color=INK)
        end[1].set_color(V_COLOR)
        end.to_corner(DL, buff=0.25)
        label_box(end)
        self.play(FadeIn(end), run_time=0.6)
        self.wait(2.5)
