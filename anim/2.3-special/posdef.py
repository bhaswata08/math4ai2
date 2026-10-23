"""Block 2.3: positive definite matrices and the forms x^T A x.

Idea from Visual Kernel, "SEE Matrix" ch.1 (special matrices) and
3Blue1Brown, Essence of Linear Algebra ch.7 (dot products and angles).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class QuadraticForms(ThreeDScene):
    """The surface z = x^T A x for a positive definite, semi-definite and indefinite A."""

    def construct(self):
        a = ValueTracker(2.0)
        b = ValueTracker(1.0)
        R = 1.5
        ZS = 0.4  # z is drawn at half height (display only)

        def surf():
            sa, sb = a.get_value(), b.get_value()
            s = Surface(lambda u, v: np.array([u, v, ZS * (sa * u * u + sb * v * v) - 0.3]),
                        u_range=[-R, R], v_range=[-R, R], resolution=(24, 24),
                        fill_color=V_COLOR, fill_opacity=0.7,
                        stroke_color=INK, stroke_width=0.6, stroke_opacity=0.5)
            return s

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-1.5, 2.5, 1],
                          x_length=4, y_length=4, z_length=4,
                          axis_config={"stroke_color": INK_DIM, "stroke_width": 2, "include_ticks": False,
                                       "include_tip": False})
        axes.shift(-axes.c2p(0, 0, 0) + np.array([0, 0, -0.3]))
        surface = always_redraw(surf)

        def valley():
            sb = b.get_value()
            return ParametricFunction(lambda t: np.array([0, t, ZS * sb * t * t - 0.3]),
                                      t_range=[-R, R], color=RESULT_COLOR, stroke_width=7)

        valley_line = always_redraw(valley)

        def mat(av, bv):
            m = matrix_tex([[av, 0], [0, bv]], col_colors=(None, None))
            m.to_corner(UL, buff=0.25)
            label_box(m)
            return m

        form = tex(r"z=\mathbf{x}^{T}A\,\mathbf{x}")
        form.to_corner(UR, buff=0.25)
        label_box(form)
        m1 = mat(2, 1)
        t1 = tex(r"\text{positive definite}")
        t1.to_edge(DOWN, buff=0.25)
        label_box(t1)

        self.set_camera_orientation(phi=42 * DEGREES, theta=-50 * DEGREES, zoom=0.8)
        self.add(axes, surface, valley_line)
        self.add_fixed_in_frame_mobjects(m1, form, t1)
        self.wait(1.5)
        self.begin_ambient_camera_rotation(rate=0.1)

        # PSD: diag(1, 0)
        m2_ = mat(1, 0)
        t2 = tex(r"\text{positive semi-definite}")
        t2.to_edge(DOWN, buff=0.25)
        label_box(t2)
        self.add_fixed_in_frame_mobjects(m2_, t2)
        self.remove(m2_, t2)
        self.play(FadeOut(m1), FadeOut(t1), run_time=0.4)
        self.play(a.animate.set_value(1.0), b.animate.set_value(0.0),
                  FadeIn(m2_, run_time=1), FadeIn(t2, run_time=1), run_time=3)
        self.wait(2)

        # indefinite: diag(1, -1)
        m3 = mat(1, -1)
        t3 = tex(r"\text{indefinite}")
        t3.to_edge(DOWN, buff=0.25)
        label_box(t3)
        self.add_fixed_in_frame_mobjects(m3, t3)
        self.remove(m3, t3)
        self.play(FadeOut(m2_), FadeOut(t2), run_time=0.4)
        self.play(b.animate.set_value(-1.0),
                  FadeIn(m3, run_time=1), FadeIn(t3, run_time=1), run_time=3)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()


class PDAngle(Scene):
    """For a positive definite A, A x never turns more than 90 degrees from x."""

    def construct(self):
        U = 0.7
        XL = 1.5
        plane = lin_plane(U)
        self.add(plane)

        def build(M, mat_rows, tag_s):
            return M, mat_rows, tag_s

        Apd = np.array([[2.0, 1.0], [1.0, 2.0]])
        Ain = np.array([[1.0, 0.0], [0.0, -1.0]])
        state = {"A": Apd}
        th = ValueTracker(0.0)

        def xvec():
            t = th.get_value()
            return XL * np.array([np.cos(t), np.sin(t)])

        def x_arrow():
            v = xvec()
            return Arrow(ORIGIN, [v[0] * U, v[1] * U, 0], buff=0, color=V_COLOR, stroke_width=6,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.18)

        def ax_arrow():
            v = state["A"] @ xvec()
            return Arrow(ORIGIN, [v[0] * U, v[1] * U, 0], buff=0, color=RESULT_COLOR, stroke_width=6,
                         max_tip_length_to_length_ratio=0.2, tip_length=0.18)

        def value():
            v = xvec()
            return float(v @ state["A"] @ v)

        def arc():
            v = xvec()
            w = state["A"] @ v
            a0 = np.arctan2(v[1], v[0])
            d = np.arctan2(w[1], w[0]) - a0
            d = (d + np.pi) % (2 * np.pi) - np.pi
            col = HIGHLIGHT if value() < 0 else INK
            if abs(d) < 1e-3:
                return VGroup()
            return Arc(radius=0.7, start_angle=a0, angle=d, color=col, stroke_width=5)

        xa = always_redraw(x_arrow)
        axa = always_redraw(ax_arrow)
        ar = always_redraw(arc)

        def readout():
            val = value()
            col = HIGHLIGHT if val < 0 else INK
            lab = tex(r"\mathbf{x}^{T}A\,\mathbf{x}=", color=col)
            num = DecimalNumber(val, num_decimal_places=2, font_size=MIN_FONT, color=col)
            g = VGroup(lab, num).arrange(RIGHT, buff=0.12)
            g.to_corner(DR, buff=0.25)
            bg = label_box(g)
            return g

        ro = always_redraw(readout)

        def angle_ro():
            v = xvec()
            w = state["A"] @ v
            ang = np.degrees(np.arccos(np.clip(v @ w / (np.linalg.norm(w) * np.linalg.norm(v)), -1, 1)))
            col = HIGHLIGHT if ang >= 90 else INK
            g = tex(r"\text{angle}=" + f"{ang:.0f}" + r"^{\circ}", color=col)
            g.next_to(ro, UP, aligned_edge=RIGHT, buff=0.2)
            label_box(g)
            return g

        ang_ro = always_redraw(angle_ro)

        mat1 = matrix_tex([[2, 1], [1, 2]], col_colors=(None, None))
        mat1.to_corner(UL, buff=0.25)
        label_box(mat1)
        tag1 = tex(r"\text{positive definite}")
        tag1.move_to([-0.6, 2.35, 0])
        label_box(tag1)

        xa.set_z_index(3)
        ar.set_z_index(2)
        self.add(mat1, tag1, axa, ar, xa, ro, ang_ro)
        self.wait(0.8)
        self.play(th.animate.set_value(2 * PI), run_time=7, rate_func=linear)
        self.wait(0.4)

        # contrast: indefinite
        th.set_value(0.0)
        state["A"] = Ain
        mat2 = matrix_tex([[1, 0], [0, -1]], col_colors=(None, None))
        mat2.to_corner(UL, buff=0.25)
        label_box(mat2)
        tag2 = tex(r"\text{indefinite}")
        tag2.move_to([-0.6, 2.35, 0])
        label_box(tag2)
        self.play(FadeTransform(mat1, mat2), FadeTransform(tag1, tag2), run_time=1)
        self.play(th.animate.set_value(2 * PI), run_time=7, rate_func=linear)
        self.wait(1)
