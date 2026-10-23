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


class LevelSetsDefinite(Scene):
    """The level curve x^T A x = 1 for a positive definite, an indefinite and a semi-definite A.

    The matrices are not the ones in the practice problems on the slide.
    """

    def construct(self):
        A1 = np.array([[2.0, 1.0], [1.0, 2.0]])
        A2 = np.array([[1.0, 3.0], [3.0, 1.0]])
        A3 = np.array([[4.0, 2.0], [2.0, 1.0]])
        dets = [np.linalg.det(A) for A in (A1, A2, A3)]
        assert np.allclose(dets, [3, -8, 0])

        U = 1.2
        CEN = np.array([2.3, 0.0, 0.0])
        RNG = 2.0

        plane = house_plane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4 * U, y_length=4 * U)
        plane.move_to(CEN)
        for ax in (plane.x_axis, plane.y_axis):
            ax.add_numbers(x_values=[-2, -1, 1, 2], font_size=MIN_FONT, excluding=[0]) if ax is plane.x_axis \
                else ax.add_numbers(x_values=[-2, -1, 1, 2], font_size=MIN_FONT, excluding=[0])
        for ax in (plane.x_axis, plane.y_axis):
            for n in ax.numbers:
                n.set_color(INK_DIM)
                label_box(n, opacity=0.9, buff=0.04)

        sv = ValueTracker(0.0)   # 0..1 goes A1 -> A2, 1..2 goes A2 -> A3

        def cur_A():
            s = sv.get_value()
            if s <= 1:
                return (1 - s) * A1 + s * A2
            return (2 - s) * A2 + (s - 1) * A3

        def curve_for(A, col=RESULT_COLOR, width=7, unit=U, centre=CEN, rng=RNG):
            f = lambda x, y: A[0, 0] * x * x + 2 * A[0, 1] * x * y + A[1, 1] * y * y - 1
            c = ImplicitFunction(f, x_range=(-rng, rng), y_range=(-rng, rng), color=col, stroke_width=width,
                                 min_depth=6, max_quads=3000)
            c.scale(unit, about_point=ORIGIN).shift(centre)
            return c

        curve = always_redraw(lambda: curve_for(cur_A()))

        # left panel: live matrix and determinant
        LX = -2.55

        def mat_readout():
            A = cur_A()
            ents = VGroup()
            for (i, j, px, py) in [(0, 0, -0.7, 0.42), (0, 1, 0.7, 0.42), (1, 0, -0.7, -0.42), (1, 1, 0.7, -0.42)]:
                v = A[i, j] if abs(A[i, j]) > 0.05 else 0.0
                ents.add(DecimalNumber(v, num_decimal_places=1, font_size=MIN_FONT, color=INK)
                         .move_to([LX + px, 1.7 + py, 0]))
            return ents

        brk = VGroup(MathTex(r"\Bigg[", font_size=MIN_FONT * 1.5, color=INK).move_to([LX - 1.3, 1.7, 0]),
                     MathTex(r"\Bigg]", font_size=MIN_FONT * 1.5, color=INK).move_to([LX + 1.3, 1.7, 0]))
        a_lab = tex(r"A=", INK).move_to([LX - 1.95, 1.7, 0])
        ents = always_redraw(mat_readout)

        def det_readout():
            A = cur_A()
            d = float(np.linalg.det(A))
            if abs(d) < 0.05:
                d = 0.0
            g = VGroup(tex(r"\det A=", INK),
                       DecimalNumber(d, num_decimal_places=1, font_size=MIN_FONT + 8, color=RESULT_COLOR))
            g.arrange(RIGHT, buff=0.15).move_to([LX, -0.15, 0])
            return g

        det = always_redraw(det_readout)
        form = tex(r"\mathbf{x}^{T}A\,\mathbf{x}=1", INK).move_to([LX, 2.55 - 0.0, 0])
        form.move_to([LX, 0.45, 0])

        def tag(s1, s2):
            g = VGroup(tex(s1, INK), tex(s2, INK_DIM)).arrange(DOWN, buff=0.2).move_to([LX, -1.4, 0])
            return g

        t1 = tag(r"\text{positive definite}", r"\text{closed curve}")
        t2 = tag(r"\text{indefinite}", r"\text{two branches}")
        t3 = tag(r"\text{semi-definite}", r"\text{two lines}")
        for t in (t1, t2, t3):
            assert t.width < 4.6, t.width

        self.add(plane, curve, brk, a_lab, ents, det, form, t1)
        self.wait(2.5)
        self.play(FadeOut(t1), run_time=0.4)
        self.play(sv.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.play(FadeIn(t2), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(t2), run_time=0.4)
        self.play(sv.animate.set_value(2.0), run_time=4, rate_func=smooth)
        self.play(FadeIn(t3), run_time=0.5)
        self.wait(2)

        # final: three panels
        curve.clear_updaters()
        ents.clear_updaters()
        det.clear_updaters()
        self.play(*[FadeOut(m) for m in (plane, curve, brk, a_lab, ents, det, form, t3)], run_time=0.6)
        u2, rng2 = 0.62, 2.0
        outs = []
        for k, (A, name) in enumerate([(A1, r"\text{positive definite}"), (A2, r"\text{indefinite}"),
                                       (A3, r"\text{semi-definite}")]):
            cx = -3.2 + 3.2 * k
            pl = house_plane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4 * u2, y_length=4 * u2)
            pl.move_to([cx, 0.85, 0])
            cv = curve_for(A, unit=u2, centre=np.array([cx, 0.85, 0]), rng=rng2, width=6)
            d = float(np.linalg.det(A))
            dl = tex(r"\det A=" + f"{d:.0f}", RESULT_COLOR).move_to([cx, -0.9, 0])
            tg = tex(name, INK, 40)
            if tg.width > 3.1:
                tg.scale(3.1 / tg.width)
            tg.move_to([cx, -1.7, 0])
            outs.append(VGroup(pl, cv, dl, tg))
        self.play(*[FadeIn(o) for o in outs], run_time=1.2)
        self.wait(2.5)
