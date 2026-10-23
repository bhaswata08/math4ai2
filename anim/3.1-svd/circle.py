"""Block 3.1: the SVD as rotate, stretch, rotate of the unit circle.

A = [[3, 0], [4, 5]] = U Sigma V^T, with V and U both rotations.
Idea from 3Blue1Brown-style SVD pictures and Visual Kernel's "SEE Matrix".
"""

from shared.anim.house import *
from shared.anim.linmap import *

A = np.array([[3.0, 0.0], [4.0, 5.0]])
S1, S2 = 3 * np.sqrt(5), np.sqrt(5)
V = np.array([[1.0, -1.0], [1.0, 1.0]]) / np.sqrt(2)   # columns v1=(1,1)/r2, v2=(-1,1)/r2
U = np.array([[1.0, -3.0], [3.0, 1.0]]) / np.sqrt(10)  # columns u1=(1,3)/r10, u2=(-3,1)/r10
SIG = np.diag([S1, S2])
assert np.allclose(U @ SIG @ V.T, A)
assert np.isclose(np.linalg.det(V), 1) and np.isclose(np.linalg.det(U), 1)

SC = 0.38  # scene units per plane unit: the ellipse (half height 6.4) must fit in 2.66


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def rot(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


def pt(M, v):
    w = M @ np.asarray(v, dtype=float)
    return np.array([w[0], w[1], 0.0]) * SC


def circle_pts(M, n=120):
    return [pt(M, (np.cos(t), np.sin(t))) for t in np.linspace(0, 2 * np.pi, n + 1)]


FR = [None]


def KK():
    """Frame width / 10: scale for strokes so lines keep their on-screen width while zooming."""
    return FR[0].width / 10 if FR[0] is not None else 1.0


def fix_strokes(plane):
    def up(m):
        k = KK()
        for l in m.background_lines:
            l.set_stroke(width=2 * k)
        for l in m.faded_lines:
            l.set_stroke(width=2 * k)
        for a in (m.x_axis, m.y_axis):
            a.set_stroke(width=3 * k)
    plane.add_updater(up)
    up(plane)


def arrow(M, v, color):
    return Arrow(ORIGIN, pt(M, v), buff=0, color=color, stroke_width=6 * KK(),
                 tip_length=0.13, max_tip_length_to_length_ratio=0.4)


def right_mark(a, b, color=INK):
    return RightAngle(Line(ORIGIN, a), Line(ORIGIN, b), length=0.2, color=color, stroke_width=3,
                      quadrant=(1, 1))


MARK = -0.35  # angle (rad) of the asymmetric marker radius

ZOOM = 1.3 / SC          # start zoomed so the unit circle has radius 1.3 on screen
K0 = 1 / ZOOM            # frame width / 10 at the start


def pin(frame, mob):
    """Keep mob at a fixed place and on-screen size while the camera frame zooms.
    mob must be laid out in the default (unzoomed) frame when pin is called."""
    rel = mob.get_center().copy()
    mob._k = 1.0

    def up(m):
        k = frame.width / 10
        m.scale(k / m._k)
        m._k = k
        m.move_to(frame.get_center() + k * rel)

    mob.add_updater(up)
    up(mob)
    return mob


def header(frame, color_parts=True):
    parts = [tex("A"), tex("="), tex("U"), tex(r"\Sigma"), tex(r"V^T")]
    row = VGroup(*parts).arrange(RIGHT, buff=0.14)
    row.to_corner(UL, buff=0.3)
    bg = BackgroundRectangle(row, color=BG, fill_opacity=0.85, buff=0.1)
    grp = VGroup(bg, row)
    return grp, parts


def corner_label(frame, s, anchor_group=None, corner=UL, below=None):
    t = tex(s)
    if below is None:
        t.to_corner(corner, buff=0.3)
    else:
        t.move_to(below + RIGHT * t.width / 2 + DOWN * (t.height / 2 + 0.2))
    return VGroup(BackgroundRectangle(t, color=BG, fill_opacity=0.85, buff=0.1), t)


def v_labels():
    out = []
    for i, col in enumerate((V_COLOR, W_COLOR)):
        v = V[:, i]
        l = tex(r"\mathbf v_%d" % (i + 1), col).scale(K0)
        l.move_to(np.array([v[0], v[1], 0]) * (SC + 0.5 * K0))
        out.append(l)
    return out


class SVDCircleSteps(MovingCameraScene):
    """V^T rotates, Sigma stretches, U rotates: the circle lands on A's ellipse."""

    def construct(self):
        frame = self.camera.frame
        FR[0] = frame
        plane = lin_plane(SC)
        fix_strokes(plane)
        th = np.arctan2(3, 1)

        def M_of(p):
            R1 = rot(-np.pi / 4)
            if p <= 1:
                return rot(-np.pi / 4 * p)
            if p <= 2:
                f = p - 1
                return np.diag([1 + (S1 - 1) * f, 1 + (S2 - 1) * f]) @ R1
            return rot(th * (p - 2)) @ SIG @ R1

        tr = ValueTracker(0)

        def body():
            p = tr.get_value()
            M = M_of(p)
            f = float(np.clip(p - 1, 0, 1))
            amber = interpolate_color(ManimColor(INK_DIM), ManimColor(RESULT_COLOR), f)
            c1 = interpolate_color(ManimColor(V_COLOR), ManimColor(RESULT_COLOR), f)
            c2 = interpolate_color(ManimColor(W_COLOR), ManimColor(RESULT_COLOR), f)
            shape = VMobject(stroke_color=amber, stroke_width=5 * KK(), fill_color=amber, fill_opacity=0.12)
            shape.set_points_as_corners(circle_pts(M))
            q = pt(M, (np.cos(MARK), np.sin(MARK)))
            return VGroup(shape, Line(ORIGIN, q, color=INK, stroke_width=4 * KK()),
                          Dot(q, radius=0.05 * KK(), color=INK), arrow(M, V[:, 0], c1), arrow(M, V[:, 1], c2))

        frame.set_width(10 * K0)
        plane.update(0)
        fig = always_redraw(body)
        head, parts = header(frame)
        lv1, lv2 = v_labels()
        HEAD_DL = head[0].get_corner(DL).copy()
        pin(frame, head)

        head.update(0)
        self.add(plane, fig, head, lv1, lv2)
        self.wait(1.2)
        self.play(FadeOut(lv1), FadeOut(lv2), run_time=0.4)

        steps = [(4, r"V^T:\ \text{rotate}"), (3, r"\Sigma:\ \text{stretch}"), (2, r"U:\ \text{rotate}")]
        for k, (idx, cap) in enumerate(steps):
            t = pin(frame, corner_label(frame, cap, below=HEAD_DL))
            parts[idx].set_color(HIGHLIGHT)
            self.add(t)
            self.wait(0.4)
            if k == 1:
                self.play(tr.animate.set_value(k + 1), frame.animate.set_width(10),
                          run_time=3.5, rate_func=smooth)
            else:
                self.play(tr.animate.set_value(k + 1), run_time=3, rate_func=smooth)
            parts[idx].set_color(INK)
            self.remove(t)

        tip1 = pt(A, V[:, 0])
        tip2 = pt(A, V[:, 1])
        l1 = label_box(tex(r"\sigma_1 \mathbf u_1", RESULT_COLOR))
        l1.next_to(tip1, RIGHT, buff=0.75).shift(DOWN * 0.1)
        l2 = label_box(tex(r"\sigma_2 \mathbf u_2", RESULT_COLOR))
        l2.next_to(tip2, LEFT, buff=0.45)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.wait(0.8)

        g = ValueTracker(0)

        def ghost():
            M = (1 - g.get_value()) * np.eye(2) + g.get_value() * A
            s = VMobject(stroke_color=INK, stroke_width=3)
            s.set_points_as_corners(circle_pts(M))
            return DashedVMobject(s, num_dashes=60, dashed_ratio=0.5)

        gh = always_redraw(ghost)
        t = pin(frame, corner_label(frame, r"A\ \text{directly}", below=HEAD_DL))
        parts[0].set_color(HIGHLIGHT)
        self.add(t, gh)
        self.wait(0.4)
        self.play(g.animate.set_value(1), run_time=3, rate_func=smooth)
        parts[0].set_color(INK)
        self.remove(t)
        t2 = pin(frame, corner_label(frame, r"\text{same ellipse}", below=HEAD_DL))
        self.add(t2)
        self.wait(1.4)


class SingularPairs(MovingCameraScene):
    """A sends the perpendicular pair v1, v2 to the perpendicular pair sigma1 u1, sigma2 u2."""

    def construct(self):
        frame = self.camera.frame
        FR[0] = frame
        plane = lin_plane(SC)
        fix_strokes(plane)
        tr = ValueTracker(0)

        def M_now():
            t = tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        circ = VMobject(stroke_color=INK_DIM, stroke_width=5, fill_color=INK_DIM, fill_opacity=0.12)
        circ.set_points_as_corners(circle_pts(np.eye(2)))
        circ.add_updater(lambda m: m.set_stroke(width=5 * KK()))

        def arrows():
            t = tr.get_value()
            M = M_now()
            c1 = interpolate_color(ManimColor(V_COLOR), ManimColor(RESULT_COLOR), t)
            c2 = interpolate_color(ManimColor(W_COLOR), ManimColor(RESULT_COLOR), t)
            return VGroup(arrow(M, V[:, 0], c1), arrow(M, V[:, 1], c2))

        frame.set_width(10 * K0)
        plane.update(0)
        circ.update(0)
        arr = always_redraw(arrows)
        lv1, lv2 = v_labels()
        v1, v2 = V[:, 0], V[:, 1]
        mark0 = RightAngle(Line(ORIGIN, pt(np.eye(2), v1)), Line(ORIGIN, pt(np.eye(2), v2)),
                           length=0.12, color=INK, stroke_width=3, quadrant=(1, 1))

        mark0.add_updater(lambda m: m.set_stroke(width=3 * KK()))
        mark0.update(0)
        cap1 = pin(frame, corner_label(frame, r"\text{perpendicular in}"))
        self.add(plane, circ, arr, lv1, lv2, mark0, cap1)
        self.wait(1.4)

        cap2 = pin(frame, corner_label(frame, r"\text{apply }A"))
        self.play(FadeOut(lv1), FadeOut(lv2), FadeOut(mark0), FadeOut(cap1), run_time=0.5)
        self.remove(cap1)
        self.add(cap2)
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, circ), tr.animate.set_value(1),
                  frame.animate.set_width(10), run_time=4.5, rate_func=smooth)

        w1, w2 = pt(A, v1), pt(A, v2)
        mark1 = RightAngle(Line(ORIGIN, w1), Line(ORIGIN, w2), length=0.22, color=INK,
                           stroke_width=3, quadrant=(1, 1))
        self.remove(cap2)
        cap3 = pin(frame, corner_label(frame, r"\text{perpendicular out}"))
        self.add(cap3)
        self.play(FadeIn(mark1), run_time=0.6)

        n1 = label_box(tex(r"|A\mathbf v_1| = 3\sqrt5", RESULT_COLOR))
        n1.next_to(w1, RIGHT, buff=0.75).shift(DOWN * 0.1)
        n2 = label_box(tex(r"|A\mathbf v_2| = \sqrt5", RESULT_COLOR))
        n2.next_to(w2, LEFT, buff=0.45)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.7)
        self.wait(0.8)
        eq = label_box(tex(r"A\mathbf v_i = \sigma_i \mathbf u_i", INK))
        eq.to_corner(DR, buff=0.2)
        self.play(FadeIn(eq), run_time=0.7)
        self.wait(1.3)
