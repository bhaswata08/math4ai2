"""Block 2.3: eigenvectors by sweeping a unit vector round the circle."""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class EigenSweep(Scene):
    """A unit vector x turns once round. Ax traces an ellipse and lies on x's line only twice."""

    def construct(self):
        U = 0.8
        CEN = np.array([1.9, 0.0, 0.0])
        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        vals, vecs = np.linalg.eigh(A)
        assert np.allclose(vals, [1, 3])

        def P(p):
            return CEN + np.array([p[0] * U, p[1] * U, 0.0])

        plane = house_plane(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6 * U, y_length=6 * U)
        plane.move_to(CEN)
        circ = Circle(radius=U, color=INK_FAINT, stroke_width=3).move_to(CEN)
        th = ValueTracker(0.0)

        def xv():
            t = th.get_value()
            return np.array([np.cos(t), np.sin(t)])

        def arr(p, color, w=7, tip=0.2):
            return Arrow(CEN, P(p), buff=0, color=color, stroke_width=w,
                         max_tip_length_to_length_ratio=0.25, tip_length=tip)

        xa = always_redraw(lambda: arr(xv(), W_COLOR, 8))
        axa = always_redraw(lambda: arr(A @ xv(), RESULT_COLOR, 8))
        line = always_redraw(lambda: DashedLine(P(-3.2 * xv()), P(3.2 * xv()), color=HIGHLIGHT,
                                                stroke_width=3, dash_length=0.12))
        trail = always_redraw(lambda: ParametricFunction(
            lambda t: P(A @ np.array([np.cos(t), np.sin(t)])), t_range=[0, max(th.get_value(), 1e-3)],
            color=RESULT_COLOR, stroke_width=3, stroke_opacity=0.7))

        def angle_deg():
            x, y = xv(), A @ xv()
            c = x @ y / np.linalg.norm(y)
            return float(np.degrees(np.arccos(np.clip(c, -1, 1))))

        def ang_ro():
            a = angle_deg()
            if a < 0.5:
                a = 0.0
            g = VGroup(tex(r"\text{angle}=", INK), DecimalNumber(a, num_decimal_places=0, font_size=MIN_FONT, color=INK),
                       tex(r"^{\circ}", INK)).arrange(RIGHT, buff=0.1)
            g[2].shift(UP * 0.05)
            return g.move_to([-3.2, -0.1, 0])

        ro = always_redraw(ang_ro)
        mat = matrix_tex([[2, 1], [1, 2]], col_colors=(None, None)).to_corner(UL, buff=0.25)
        lx = tex(r"\mathbf{x}", W_COLOR).move_to([-4.2, 0.95, 0]) if False else None
        key = VGroup(tex(r"\mathbf{x}", W_COLOR), tex(r"A\mathbf{x}", RESULT_COLOR)).arrange(RIGHT, buff=0.7)
        key.move_to([-3.2, 0.6, 0])

        self.add(plane, circ, line, trail, xa, axa, mat, key, ro)
        xa.set_z_index(4)
        axa.set_z_index(3)
        self.wait(1.5)
        self.play(th.animate.set_value(np.pi / 4), run_time=3.5, rate_func=linear)
        l3 = tex(r"A\mathbf{x}=3\,\mathbf{x}", HIGHLIGHT).move_to([-3.0, -1.3, 0])
        self.play(FadeIn(l3), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(l3), run_time=0.4)
        self.play(th.animate.set_value(3 * np.pi / 4), run_time=3.5, rate_func=linear)
        l1 = tex(r"A\mathbf{x}=1\,\mathbf{x}", HIGHLIGHT).move_to([-3.0, -1.3, 0])
        self.play(FadeIn(l1), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(l1), run_time=0.4)
        self.play(th.animate.set_value(2 * np.pi), run_time=5, rate_func=linear)
        self.wait(0.5)

        # the two lines that stayed put
        for d in (vecs[:, 1], vecs[:, 0]):
            pass
        ln3 = Line(P(-3.2 * vecs[:, 1]), P(3.2 * vecs[:, 1]), color=V_COLOR, stroke_width=5)
        ln1 = Line(P(-3.2 * vecs[:, 0]), P(3.2 * vecs[:, 0]), color=V_COLOR, stroke_width=5)
        for l in (ln3, ln1):
            l.set_z_index(2)
        t3 = tex(r"\lambda=3", V_COLOR).move_to(P(2.3 * vecs[:, 1]) + np.array([0.55, 0.35, 0]))
        t1 = tex(r"\lambda=1", V_COLOR).move_to(P(1.7 * vecs[:, 0] * np.array([-1, 1])) + np.array([-0.2, 0.0, 0]))
        t1.move_to(P(np.array([-2.3, 0.7])))
        t3.move_to(P(np.array([2.1, 2.1])) + np.array([0.0, 0.45, 0]))
        for t in (t1, t3):
            label_box(t)
        eq = tex(r"A\mathbf{v}=\lambda\mathbf{v}", INK).move_to([-3.2, -1.3, 0])
        self.play(FadeOut(line), FadeOut(xa), FadeOut(axa), FadeOut(ro), FadeOut(key), run_time=0.5)
        self.play(Create(ln3), Create(ln1), run_time=1.2)
        self.play(FadeIn(t3), FadeIn(t1), FadeIn(eq), run_time=0.8)
        self.wait(2.5)
