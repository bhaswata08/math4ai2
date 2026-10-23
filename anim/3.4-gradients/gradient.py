# Original work for Mathematics for AI, CC BY-NC-SA 4.0

from functools import reduce

from shared.anim.house import *
import numpy as np

# Worked function for the surface clips: f(x, y) = x^2 + 3xy at p = (1, 2).
PX, PY = 1.0, 2.0


def f3(x, y):
    return x * x + 3.0 * x * y


def fx3(x, y):
    return 2.0 * x + 3.0 * y


def fy3(x, y):
    return 3.0 * x


def hud(tex, y, color=INK, x=2.95, size=MIN_FONT):
    """A line of text pinned to the screen (never hidden behind the surface)."""
    m = MathTex(tex, font_size=size, color=color)
    m.move_to(np.array([x, y, 0.0]))
    m.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)
    return m


def screen_to_world(phi, theta, vec):
    """World vector that appears as screen vector `vec` at this camera angle."""
    rot = reduce(np.dot, [rotation_about_z(-theta - 90 * DEGREES), rotation_matrix(-phi, RIGHT)])
    return np.dot(np.array(vec, dtype=float), rot)


class SurfaceScene(ThreeDScene):
    """Shared set-up: the surface z = x^2 + 3xy over [0,3]^2, floor grid, axes."""

    PHI = 68 * DEGREES
    THETA = -52 * DEGREES
    SHIFT = np.array([-1.9, -0.35, 0.0])  # where the box centre sits on screen

    def build_world(self):
        L = 3.3
        axes = ThreeDAxes(
            x_range=[0, 3, 1], y_range=[0, 3, 1], z_range=[0, 36, 12],
            x_length=L, y_length=L, z_length=2.3,
            axis_config={"stroke_width": 2.5, "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.z_axis.set_color(INK_DIM)
        axes.shift(-axes.c2p(1.5, 1.5, 0.0) + np.dot(self.SHIFT, self.camera.get_rotation_matrix()))
        self.axes = axes
        c2p = axes.c2p

        surface = Surface(
            lambda u, v: c2p(u, v, f3(u, v)),
            u_range=[0, 3], v_range=[0, 3], resolution=(18, 18),
            stroke_color=INK_FAINT, stroke_width=0.5, stroke_opacity=0.45,
        )
        for face in surface.submobjects:
            face.set_fill(color=INK_DIM, opacity=0.16 if (face.u_index + face.v_index) % 2 == 0 else 0.30)
        self.surface = surface

        grid = VGroup()
        for i in range(4):
            grid.add(Line(c2p(i, 0, 0), c2p(i, 3, 0), stroke_color=INK_FAINT, stroke_width=1.5, stroke_opacity=0.55))
            grid.add(Line(c2p(0, i, 0), c2p(3, i, 0), stroke_color=INK_FAINT, stroke_width=1.5, stroke_opacity=0.55))
        self.grid = grid

        # Axis letters and tick numbers, kept upright and on the visible edges.
        labels = VGroup()
        for v in (1, 2, 3):
            t = MathTex(str(v), font_size=MIN_FONT, color=X_COLOR)
            t.move_to(c2p(v, -0.45, 0))
            labels.add(t)
            t = MathTex(str(v), font_size=MIN_FONT, color=Y_COLOR)
            t.move_to(c2p(3.45, v, 0))
            labels.add(t)
        for ch, col, pos in (("x", X_COLOR, (3.35, -0.55, 0)), ("y", Y_COLOR, (3.45, 3.5, 0))):
            t = MathTex(ch, font_size=MIN_FONT, color=col)
            t.move_to(c2p(*pos))
            labels.add(t)
        for m in labels:
            m.add_background_rectangle(color=BG, opacity=0.75, buff=0.04)
        self.labels = labels

        z0 = f3(PX, PY)
        self.P = c2p(PX, PY, z0)
        self.P_floor = c2p(PX, PY, 0)
        self.dot_p = Dot3D(point=self.P, radius=0.10, color=RESULT_COLOR)
        self.dot_floor = Dot3D(point=self.P_floor, radius=0.07, color=RESULT_COLOR)
        self.drop = DashedLine(self.P, self.P_floor, color=INK_DIM, stroke_width=3)

    def orient(self):
        self.set_camera_orientation(phi=self.PHI, theta=self.THETA)

    def add_world(self, floor_dot=True):
        self.add(self.axes, self.grid, self.surface, self.drop, self.dot_p)
        if floor_dot:
            self.add(self.dot_floor)
        self.add_fixed_orientation_mobjects(*self.labels)

    def arrow(self, a, b, color, w=0.055):
        return Arrow3D(a, b, color=color, thickness=w, height=0.30, base_radius=0.12)


# =============================================================================
# SCENE 1: GradientOnSurface
# =============================================================================
class GradientOnSurface(SurfaceScene):
    """Partials at the point, stacked into the gradient, on the same surface as
    the worked example. Arrows start at p itself, at the height of p."""

    def construct(self):
        self.orient()
        self.build_world()
        c2p = self.axes.c2p
        c = 0.2  # arrows drawn at 0.15x length so they fit on the surface
        gx, gy = fx3(PX, PY), fy3(PX, PY)
        z0 = f3(PX, PY)

        a = self.P
        b = c2p(PX + c * gx, PY, z0)
        d = c2p(PX + c * gx, PY + c * gy, z0)
        arr_x = self.arrow(a, b, X_COLOR)
        arr_y = self.arrow(b, d, Y_COLOR)
        arr_g = self.arrow(a, d, RESULT_COLOR, 0.07)
        tip_up = c2p(PX + c * gx, PY + c * gy, z0 + c * (gx * gx + gy * gy))
        arr_up = self.arrow(a, tip_up, RESULT_COLOR, 0.07)
        drop_tip = DashedLine(d, tip_up, color=INK_DIM, stroke_width=3)

        h_f = hud(r"f(x,y) = x^2 + 3xy", 2.2, V_COLOR)
        h_p = hud(r"p = (1,\,2)", 1.4, RESULT_COLOR)
        h_x = hud(r"\partial f/\partial x", 0.45, X_COLOR)
        h_y = hud(r"\partial f/\partial y", -0.35, Y_COLOR)
        h_g = hud(r"\nabla f = \text{their sum}", -1.25, RESULT_COLOR)
        h_u = hud(r"\text{points uphill}", -2.05, RESULT_COLOR)

        self.camera.add_fixed_in_frame_mobjects(h_x, h_y, h_g, h_u)
        self.add_world()
        self.add_fixed_in_frame_mobjects(h_f, h_p)
        self.wait(2.0)

        self.play(Create(arr_x), FadeIn(h_x), run_time=1.6)
        self.wait(1.2)
        self.play(Create(arr_y), FadeIn(h_y), run_time=1.6)
        self.wait(1.2)
        self.play(Create(arr_g), FadeIn(h_g), run_time=1.6)
        self.wait(1.5)
        self.play(Create(arr_up), Create(drop_tip), FadeIn(h_u), run_time=1.8)
        self.wait(1.5)
        self.begin_ambient_camera_rotation(rate=0.03)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()
        self.wait(2.0)


# =============================================================================
# SCENE 2: WorkedGradient
# =============================================================================
class WorkedGradient(SurfaceScene):
    """f = x^2 + 3xy at (1, 2): slice y=2 gives slope 8, slice x=1 gives
    slope 3, stack them into grad f = (8, 3), length sqrt(73)."""

    def construct(self):
        self.orient()
        self.build_world()
        c2p = self.axes.c2p
        z0 = f3(PX, PY)
        gx, gy = fx3(PX, PY), fy3(PX, PY)
        mag = float(np.hypot(gx, gy))
        c = 0.2

        # --- slice y = 2 -------------------------------------------------
        wall_y = Surface(lambda u, v: c2p(u, PY, v), u_range=[0, 3], v_range=[0, 36],
                         resolution=(2, 2), fill_color=INK, fill_opacity=0.10,
                         stroke_color=INK_FAINT, stroke_width=1.5, stroke_opacity=0.6)
        curve_x = ParametricFunction(lambda t: c2p(t, PY, f3(t, PY)), t_range=[0, 3],
                                     color=V_COLOR, stroke_width=8)
        tan_x = Line(c2p(0.3, PY, z0 + gx * (0.3 - PX)), c2p(2.2, PY, z0 + gx * (2.2 - PX)),
                     color=RESULT_COLOR, stroke_width=7)
        run_x = Line(c2p(PX, PY, z0), c2p(PX + 1, PY, z0), color=X_COLOR, stroke_width=6)
        rise_x = Line(c2p(PX + 1, PY, z0), c2p(PX + 1, PY, z0 + gx), color=X_COLOR, stroke_width=6)

        # --- slice x = 1 -------------------------------------------------
        wall_x = Surface(lambda u, v: c2p(PX, u, v), u_range=[0, 3], v_range=[0, 36],
                         resolution=(2, 2), fill_color=INK, fill_opacity=0.10,
                         stroke_color=INK_FAINT, stroke_width=1.5, stroke_opacity=0.6)
        curve_y = ParametricFunction(lambda t: c2p(PX, t, f3(PX, t)), t_range=[0, 3],
                                     color=V_COLOR, stroke_width=8)
        run_y = Line(c2p(PX, PY, z0), c2p(PX, PY + 1, z0), color=Y_COLOR, stroke_width=6)
        rise_y = Line(c2p(PX, PY + 1, z0), c2p(PX, PY + 1, z0 + gy), color=Y_COLOR, stroke_width=6)

        # --- stacked gradient on the floor ------------------------------
        fl = c2p(PX, PY, 0)
        t1 = c2p(PX + c * gx, PY, 0)
        t2 = c2p(PX + c * gx, PY + c * gy, 0)
        arr_x = Arrow(fl, t1, buff=0, color=X_COLOR, stroke_width=9, max_tip_length_to_length_ratio=0.2)
        arr_y = Arrow(t1, t2, buff=0, color=Y_COLOR, stroke_width=9, max_tip_length_to_length_ratio=0.3)
        arr_g = Arrow(fl, t2, buff=0, color=RESULT_COLOR, stroke_width=11, max_tip_length_to_length_ratio=0.12)
        for a_ in (arr_x, arr_y, arr_g):
            a_.set_shade_in_3d(True)
        # contour f = 7 through p, and a right-angle marker
        cont = ParametricFunction(
            lambda t: c2p(t, (z0 - t * t) / (3 * t), 0), t_range=[0.76, 2.6],
            color=INK, stroke_width=5)
        tdir = np.array([gy, -gx]) / mag     # tangent of the contour in (x, y)
        gdir = np.array([gx, gy]) / mag
        s = 0.22
        pts = [c2p(PX + s * tdir[0], PY + s * tdir[1], 0),
               c2p(PX + s * (tdir[0] + gdir[0]), PY + s * (tdir[1] + gdir[1]), 0),
               c2p(PX + s * gdir[0], PY + s * gdir[1], 0)]
        box = VMobject(color=HIGHLIGHT, stroke_width=4).set_points_as_corners(pts)

        # --- HUD ---------------------------------------------------------
        h_f = hud(r"f = x^2 + 3xy", 2.3, V_COLOR)
        h_p = hud(r"p = (1,\,2)", 1.6, RESULT_COLOR)   # replaced below
        h_slice_y = hud(rf"\text{{slice }} y = {PY:g}", 1.6, Y_COLOR)
        h_slice_x = hud(rf"\text{{slice }} x = {PX:g}", 1.6, X_COLOR)
        h_c_x = hud(rf"f(x,{PY:g}) = x^2 + {3 * PY:g}x", 0.85, V_COLOR)
        h_c_y = hud(rf"f({PX:g},y) = {PX * PX:g} + {3 * PX:g}y", 0.85, V_COLOR)
        h_rr_x = hud(rf"\text{{run }} 1,\ \text{{rise }} {gx:g}", 0.1, X_COLOR)
        h_rr_y = hud(rf"\text{{run }} 1,\ \text{{rise }} {gy:g}", 0.1, Y_COLOR)
        h_dx = hud(rf"\partial f/\partial x = 2x + 3y = {gx:g}", -0.85, X_COLOR)
        h_dy = hud(rf"\partial f/\partial y = 3x = {gy:g}", -1.6, Y_COLOR)
        h_gr = hud(rf"\nabla f = ({gx:g},\ {gy:g})", 0.1, RESULT_COLOR)
        h_mg = hud(rf"|\nabla f| = \sqrt{{{gx * gx + gy * gy:g}}} \approx {mag:.2f}", -0.65, RESULT_COLOR)
        h_ct = hud(r"\text{contour } f = 7 \perp \nabla f", -1.4, INK)
        h_sc = hud(r"\text{arrows at } 0.2\times", -2.1, INK_DIM)
        self.camera.add_fixed_in_frame_mobjects(
            h_slice_y, h_slice_x, h_c_x, h_c_y, h_rr_x, h_rr_y, h_dx, h_dy,
            h_gr, h_mg, h_ct, h_sc)

        h_p = hud(r"p = (1,\,2),\ f = 7", 1.6, RESULT_COLOR)
        self.add_world()
        self.add_fixed_in_frame_mobjects(h_f, h_p)
        self.wait(2.0)

        # Step 1: slice y = 2, slope in x
        self.play(FadeOut(h_p), FadeIn(wall_y), FadeIn(h_slice_y), run_time=1.2)
        self.play(Create(curve_x), FadeIn(h_c_x), run_time=1.6)
        self.wait(0.8)
        self.play(Create(tan_x), run_time=1.2)
        self.play(Create(run_x), Create(rise_x), FadeIn(h_rr_x), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(h_dx), run_time=1.0)
        self.wait(1.4)

        # Step 2: slice x = 1, slope in y
        self.play(
            FadeOut(wall_y), FadeOut(curve_x), FadeOut(tan_x), FadeOut(run_x), FadeOut(rise_x),
            FadeOut(h_slice_y), FadeOut(h_c_x), FadeOut(h_rr_x),
            run_time=1.0)
        self.play(FadeIn(wall_x), FadeIn(h_slice_x), run_time=1.0)
        self.play(Create(curve_y), FadeIn(h_c_y), run_time=1.4)
        self.wait(0.6)
        self.play(Create(run_y), Create(rise_y), FadeIn(h_rr_y), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(h_dy), run_time=1.0)
        self.wait(1.4)

        # Step 3: top view, stack the two slopes
        self.play(
            FadeOut(wall_x), FadeOut(curve_y), FadeOut(run_y), FadeOut(rise_y),
            FadeOut(h_slice_x), FadeOut(h_c_y), FadeOut(h_rr_y),
            FadeOut(self.drop), FadeOut(self.dot_p),
            self.surface.animate.set_fill(opacity=0.05).set_stroke(opacity=0.12),
            run_time=1.4)
        self.move_camera(
            phi=0.0001, theta=-90 * DEGREES,
            added_anims=[h_dx.animate.move_to(np.array([2.95, 1.6, 0.0])), h_dy.animate.move_to(np.array([2.95, 0.85, 0.0]))],
            run_time=2.6)
        self.wait(0.6)
        self.play(Create(arr_x), run_time=1.0)
        self.play(Create(arr_y), run_time=1.0)
        self.wait(0.5)
        self.play(Create(arr_g), FadeIn(h_gr), run_time=1.4)
        self.wait(0.8)
        self.play(FadeIn(h_mg), run_time=1.0)
        self.wait(1.0)
        self.play(Create(cont), Create(box), FadeIn(h_ct), FadeIn(h_sc), run_time=1.6)
        self.wait(3.0)


# =============================================================================
# SCENE 3: PerpToContours  f(x, y) = x^2 + 4y^2
# =============================================================================
def f_el(x, y):
    return x * x + 4.0 * y * y


def grad_el(x, y):
    return np.array([2.0 * x, 8.0 * y])


class PerpToContours(Scene):
    def construct(self):
        U = 1.2                       # screen units per unit of x, y
        origin = np.array([-1.2, -0.5, 0.0])

        def to_screen(x, y):
            return origin + U * np.array([x, y, 0.0])

        axes = VGroup(
            Line(to_screen(-3.8, 0), to_screen(3.6, 0), stroke_color=X_COLOR, stroke_width=2.5),
            Line(to_screen(0, -1.7), to_screen(0, 1.7), stroke_color=Y_COLOR, stroke_width=2.5),
        )
        lbl_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR).move_to(to_screen(3.5, -0.35))
        lbl_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR).move_to(to_screen(0.4, 1.55))

        levels = [1, 4, 9]
        contours = VGroup()
        for c in levels:
            a, b = np.sqrt(c), np.sqrt(c) / 2.0
            e = ParametricFunction(lambda t, a=a, b=b: to_screen(a * np.cos(t), b * np.sin(t)),
                                   t_range=[0, TAU], color=INK_DIM, stroke_width=3.5)
            contours.add(e)
        level_lbls = VGroup()
        for c in levels:
            a, b = np.sqrt(c), np.sqrt(c) / 2.0
            m = MathTex(f"f={c}", font_size=MIN_FONT, color=INK_DIM)
            m.move_to(to_screen(-0.75, b * np.sqrt(1 - (0.75 / a) ** 2)) + np.array([0.0, 0.3, 0.0]))
            m.add_background_rectangle(color=BG, opacity=0.9, buff=0.04)
            level_lbls.add(m)
        # f=1 label would sit inside the small ellipse; keep it, it is small enough.

        def point_at(deg):
            t = np.radians(deg)
            return 2.0 * np.cos(t), 1.0 * np.sin(t)    # on f = 4

        def probe(deg, with_len=False):
            x, y = point_at(deg)
            assert abs(f_el(x, y) - 4.0) < 1e-9
            g = grad_el(x, y)
            mag = float(np.hypot(*g))
            gd = g / mag
            td = np.array([-gd[1], gd[0]])
            p = to_screen(x, y)
            gv = np.array([gd[0], gd[1], 0.0]) * 0.2 * mag      # arrows at 0.2x length
            arrow = Arrow(p, p + gv, buff=0, color=RESULT_COLOR, stroke_width=7,
                          max_tip_length_to_length_ratio=0.25)
            tangent = Line(p - 0.9 * np.array([td[0], td[1], 0]), p + 0.9 * np.array([td[0], td[1], 0]),
                           color=INK, stroke_width=4)
            s = 0.2
            corners = [p + s * np.array([td[0], td[1], 0]),
                       p + s * np.array([td[0] + gd[0], td[1] + gd[1], 0]),
                       p + s * np.array([gd[0], gd[1], 0])]
            box = VMobject(color=HIGHLIGHT, stroke_width=4).set_points_as_corners(corners)
            grp = VGroup(tangent, arrow, box)
            lab = None
            if with_len:
                lab = MathTex(rf"|\nabla f| = {mag:g}", font_size=MIN_FONT, color=RESULT_COLOR)
                lab.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
            return grp, mag, lab

        dot = Dot(to_screen(*point_at(0)), radius=0.1, color=V_COLOR).set_z_index(10)
        note = MathTex(r"\text{walk along } f = 4", font_size=MIN_FONT, color=V_COLOR)
        note.move_to(np.array([3.0, 2.2, 0.0]))
        note.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

        self.add(axes, lbl_x, lbl_y, contours, level_lbls, dot, note)
        self.wait(1.5)

        def walk(a0, a1):
            return ParametricFunction(
                lambda t: to_screen(2.0 * np.cos(t), np.sin(t)),
                t_range=[np.radians(a0), np.radians(a1) + (TAU if a1 < a0 else 0)])

        cur = None
        prev = 0
        for deg in (0, 50, 130, 310):
            if deg != 0:
                self.play(MoveAlongPath(dot, walk(prev, deg)), run_time=1.4, rate_func=smooth)
            grp, _, _ = probe(deg)
            if cur is not None:
                self.play(FadeOut(cur), run_time=0.4)
            self.play(Create(grp[0]), GrowArrow(grp[1]), Create(grp[2]), run_time=1.2)
            cur = grp
            prev = deg
            self.wait(1.5)

        # Compare a wide-spaced spot with a tight-spaced spot
        self.play(FadeOut(cur), FadeOut(note), run_time=0.5)
        self.play(MoveAlongPath(dot, walk(prev, 0)), run_time=1.2)
        g0, m0, l0 = probe(0, True)
        self.play(Create(g0[0]), GrowArrow(g0[1]), Create(g0[2]), run_time=1.0)
        l0.next_to(g0[1].get_end(), RIGHT, buff=0.12)
        self.play(FadeIn(l0), run_time=0.6)
        self.wait(1.0)
        self.play(MoveAlongPath(dot, walk(0, 90)), run_time=1.3)
        g1, m1, l1 = probe(90, True)
        self.play(Create(g1[0]), GrowArrow(g1[1]), Create(g1[2]), run_time=1.0)
        l1.next_to(g1[1].get_end(), RIGHT, buff=0.15)
        self.play(FadeIn(l1), run_time=0.6)
        self.wait(1.0)
        tight = MathTex(r"\text{tighter} \to \text{longer}", font_size=MIN_FONT, color=RESULT_COLOR)
        tight.move_to(np.array([3.3, -1.9, 0.0])).add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
        self.play(FadeIn(tight), run_time=0.8)
        self.wait(2.5)


# =============================================================================
# SCENE 4: DirectionalDerivative  (projection of grad f onto u)
# =============================================================================
class DirectionalDerivative(Scene):
    def construct(self):
        G = np.array([2.0, 1.5])               # grad f at p, drawn at true length
        gmag = float(np.hypot(*G))             # 2.5
        alpha = float(np.arctan2(G[1], G[0]))
        p = np.array([-1.6, -0.3, 0.0])

        def vec(ang, length=1.0):
            return length * np.array([np.cos(ang), np.sin(ang), 0.0])

        circle = Circle(radius=1.0, color=INK_FAINT, stroke_width=3).move_to(p)
        p_dot = Dot(p, radius=0.09, color=RESULT_COLOR).set_z_index(10)
        grad_arrow = Arrow(p, p + np.append(G, 0), buff=0, color=RESULT_COLOR, stroke_width=7,
                           max_tip_length_to_length_ratio=0.15).set_z_index(3)
        grad_lbl = MathTex(r"\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        grad_lbl.move_to(p + np.append(G, 0) + np.array([0.15, 0.35, 0.0]))
        grad_lbl.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
        unit_note = MathTex(r"|\mathbf{u}| = 1", font_size=MIN_FONT, color=INK_DIM)
        unit_note.move_to(p + np.array([-0.7, -1.55, 0.0]))

        th = ValueTracker(0.0)

        def ang():
            return alpha + th.get_value()

        def dval():
            return gmag * np.cos(th.get_value())

        def u_arrow():
            return Arrow(p, p + vec(ang()), buff=0, color=W_COLOR, stroke_width=7,
                         max_tip_length_to_length_ratio=0.3).set_z_index(6)

        def u_line():
            return DashedLine(p - vec(ang(), 2.0), p + vec(ang(), 2.0), color=INK_FAINT, stroke_width=2.5)

        def shadow():
            d = dval()
            s = p + vec(ang(), d)
            seg = Line(p, s, color=RESULT_COLOR, stroke_width=14, stroke_opacity=0.9).set_z_index(2) \
                if abs(d) > 0.02 else VGroup()
            drop = DashedLine(p + np.append(G, 0), s, color=INK_DIM, stroke_width=3) \
                if np.linalg.norm(p + np.append(G, 0) - s) > 0.05 else VGroup()
            return VGroup(seg, drop)

        def u_lbl():
            a = ang()
            m = MathTex(r"\mathbf{u}", font_size=MIN_FONT, color=W_COLOR)
            m.move_to(p + vec(a, 0.55) + vec(a - PI / 2, 0.5))
            m.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
            return m

        u_arr = always_redraw(u_arrow)
        u_ln = always_redraw(u_line)
        shd = always_redraw(shadow)
        u_l = always_redraw(u_lbl)

        # contour tangent (shown only at 90 degrees)
        tang_dir = vec(alpha + PI / 2)
        tangent = Line(p - 1.6 * tang_dir, p + 1.6 * tang_dir, color=INK, stroke_width=4)
        tang_lbl = MathTex(r"\text{contour: slope } 0", font_size=MIN_FONT, color=INK)
        tang_lbl.move_to(np.array([-2.9, 1.8, 0.0]))
        tang_lbl.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

        # readout and plot on the right
        rx = 2.95
        readout = MathTex(r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u} =", font_size=MIN_FONT, color=INK)
        readout.move_to(np.array([rx, 2.2, 0.0]))
        num = DecimalNumber(gmag, num_decimal_places=2, include_sign=False, font_size=MIN_FONT, color=RESULT_COLOR)
        num.add_updater(lambda d: d.set_value(dval()).move_to(np.array([rx, 1.55, 0.0])))
        theta_lbl = MathTex(r"\theta = ", font_size=MIN_FONT, color=W_COLOR).move_to(np.array([2.2, 0.85, 0.0]))
        theta_num = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=MIN_FONT, color=W_COLOR)
        theta_num.add_updater(lambda d: d.set_value(np.degrees(th.get_value())).next_to(theta_lbl, RIGHT, buff=0.15))

        num.update()
        theta_num.update()

        plot = Axes(x_range=[0, TAU, PI], y_range=[-gmag, gmag, 1], x_length=3.1, y_length=1.9,
                    axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5, "include_ticks": False},
                    tips=False).move_to(np.array([3.1, -1.0, 0.0]))
        curve_full = plot.plot(lambda t: gmag * np.cos(t), x_range=[0, TAU], color=INK_FAINT, stroke_width=3)
        t_lbls = VGroup(*[
            MathTex(s_, font_size=MIN_FONT, color=INK_DIM).next_to(plot.c2p(v, 0), DOWN, buff=0.45 if v else 0.45)
            for s_, v in (("0", 0), (r"\pi", PI), (r"2\pi", TAU))])
        # put the labels below the lowest point of the curve so they never sit on it
        for m_ in t_lbls:
            m_.set_y(plot.c2p(0, -gmag)[1] - 0.3)
        y_lbl = MathTex(r"D_{\mathbf{u}} f", font_size=MIN_FONT, color=RESULT_COLOR).next_to(plot.y_axis.get_top(), LEFT, buff=0.1)
        x_lbl = MathTex(r"\theta", font_size=MIN_FONT, color=W_COLOR).next_to(plot.x_axis.get_end(), UP, buff=0.12)
        trace = always_redraw(lambda: plot.plot(
            lambda t: gmag * np.cos(t), x_range=[0, max(th.get_value(), 0.01)],
            color=RESULT_COLOR, stroke_width=5))
        mover = always_redraw(lambda: Dot(plot.c2p(th.get_value(), dval()), radius=0.1, color=W_COLOR).set_z_index(8))

        def frozen(angle, label):
            d = Dot(plot.c2p(angle, gmag * np.cos(angle)), radius=0.12, color=HIGHLIGHT).set_z_index(9)
            t = MathTex(label, font_size=MIN_FONT, color=HIGHLIGHT)
            off = {0: (0.55, 0.05), 1: (0.0, 0.4), 2: (0.0, 0.5)}[int(round(angle / (PI / 2))) if angle < PI else 2]
            t.move_to(d.get_center() + np.array([off[0], off[1], 0.0]))
            t.add_background_rectangle(color=BG, opacity=0.9, buff=0.04)
            return VGroup(d, t)

        self.add(circle, u_ln, shd, grad_arrow, grad_lbl, u_arr, u_l, p_dot, unit_note,
                 readout, num, theta_lbl, theta_num, plot, curve_full, t_lbls, y_lbl, x_lbl, trace, mover)

        steep = MathTex(r"\text{steepest}", font_size=MIN_FONT, color=RESULT_COLOR)
        steep.move_to(np.array([-2.5, 1.0, 0.0]))
        steep.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
        down = MathTex(r"\text{steepest descent}", font_size=MIN_FONT, color=RESULT_COLOR)
        down.move_to(np.array([-2.2, 1.0, 0.0]))
        down.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

        # 0 degrees: along the gradient
        self.wait(1.0)
        self.play(FadeIn(steep), FadeIn(frozen(0, f"{gmag:.1f}")), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(steep), run_time=0.4)
        # 90 degrees
        self.play(th.animate.set_value(PI / 2), run_time=3.5, rate_func=smooth)
        self.play(Create(tangent), FadeIn(tang_lbl), FadeIn(frozen(PI / 2, "0")), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(tangent), FadeOut(tang_lbl), run_time=0.4)
        # 180 degrees
        self.play(th.animate.set_value(PI), run_time=3.5, rate_func=smooth)
        self.play(FadeIn(down), FadeIn(frozen(PI, f"-{gmag:.1f}")), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(down), run_time=0.4)
        # rest of the turn
        self.play(th.animate.set_value(TAU), run_time=4.0, rate_func=smooth)
        self.wait(2.0)


def f_func(x, y):
    """Smooth asymmetric hill with peak at (0.5, -0.3) of height 2.0."""
    return 2.0 * np.exp(-((x - 0.5) ** 2 + 2.0 * (y + 0.3) ** 2) / 2.5)


def grad_func(x, y):
    """Analytical gradient of f_func."""
    val = f_func(x, y)
    df_dx = val * (-2.0 * (x - 0.5) / 2.5)
    df_dy = val * (-4.0 * (y + 0.3) / 2.5)
    return np.array([df_dx, df_dy])



# =============================================================================
# SCENE 5: SteepestAscent (2D)
# =============================================================================
class SteepestAscent(Scene):
    def construct(self):
        # Left ~55% of frame width (5.425 units), ~83% of frame height (4.65 units)
        scale = 1.6
        x_min, x_max = -1.25, 2.25
        y_min, y_max = -1.8, 1.2

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([-1.85, 0.0, 0.0]))
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)

        lbl_x = MathTex("x", font_size=MIN_FONT, color=X_COLOR)
        lbl_x.next_to(axes.x_axis.get_end(), DL, buff=0.10)
        lbl_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y = MathTex("y", font_size=MIN_FONT, color=Y_COLOR)
        lbl_y.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Elliptical contour lines
        peak_pos = axes.c2p(0.5, -0.3)
        levels = [0.65, 0.90, 1.15, 1.40, 1.65, 1.85]
        opacities = [0.06, 0.11, 0.16, 0.22, 0.28, 0.35]

        contour_mobs = []
        for lvl, opac in zip(levels, opacities):
            a = np.sqrt(2.5 * np.log(2.0 / lvl))
            b = a / np.sqrt(2.0)
            ell = Ellipse(
                width=2.0 * a * scale,
                height=2.0 * b * scale,
                stroke_color=INK_DIM,
                stroke_width=1.5,
                fill_color=V_COLOR,
                fill_opacity=opac,
            ).move_to(peak_pos)
            contour_mobs.append(ell)

        contours_group = VGroup(*contour_mobs)
        peak_dot = Dot(peak_pos, radius=0.07, color=V_COLOR)
        peak_lbl = MathTex(r"\text{peak}", font_size=MIN_FONT, color=V_COLOR)
        peak_lbl.next_to(peak_pos, UP, buff=0.22)
        peak_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Exactly two lines in the right column, centered at x = 3.10 (clear of all edges)
        right_x = 2.9
        c_ascent = MathTex(r"\text{ascent: follow } +\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        c_ascent.move_to(np.array([right_x, 2.05, 0.0]))
        c_ascent.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c_descent = MathTex(r"\text{descent: follow } -\nabla f", font_size=MIN_FONT, color=W_COLOR)
        c_descent.move_to(np.array([right_x, -0.55, 0.0]))
        c_descent.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        c_rule = MathTex(r"\mathbf{x}_{k+1} = \mathbf{x}_k + 0.4\,\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        c_rule.move_to(np.array([right_x, 1.25, 0.0]))
        c_rule.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        c_shrink = MathTex(r"\text{steps get shorter}", font_size=MIN_FONT, color=INK_DIM)
        c_shrink.move_to(np.array([right_x, 0.45, 0.0]))
        c_shrink.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        c_rule2 = MathTex(r"\mathbf{w}_{k+1} = \mathbf{w}_k - 0.32\,\nabla f", font_size=MIN_FONT, color=W_COLOR)
        c_rule2.move_to(np.array([right_x, -1.35, 0.0]))
        c_rule2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # -------------------------------------------------------------
        # Part 1: Steepest Ascent to peak
        # -------------------------------------------------------------
        p_start = np.array([-1.0, -1.2])
        dot_start = Dot(axes.c2p(*p_start), radius=0.08, color=RESULT_COLOR)
        lbl_start = MathTex(r"\mathbf{x}_0", font_size=MIN_FONT, color=RESULT_COLOR)
        lbl_start.next_to(axes.c2p(*p_start), RIGHT, buff=0.15)
        lbl_start.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Calculate ascent trajectory
        ascent_pts = [p_start]
        lr = 0.40
        curr = p_start.copy()
        for _ in range(6):
            g = grad_func(curr[0], curr[1])
            curr = curr + lr * g
            ascent_pts.append(curr.copy())

        ascent_arrows = []
        for i in range(len(ascent_pts) - 1):
            p1 = axes.c2p(*ascent_pts[i])
            p2 = axes.c2p(*ascent_pts[i + 1])
            arr = Arrow(
                p1, p2,
                buff=0,
                stroke_width=4.5,
                max_tip_length_to_length_ratio=0.30,
                color=RESULT_COLOR,
            )
            ascent_arrows.append(arr)

        flash_peak = Dot(peak_pos, radius=0.18, color=HIGHLIGHT)

        # -------------------------------------------------------------
        # Part 2: Contrast with Steepest Descent
        # -------------------------------------------------------------
        q_start = np.array([1.1, -0.6])
        dot_q = Dot(axes.c2p(*q_start), radius=0.08, color=W_COLOR)
        lbl_q = MathTex(r"\mathbf{w}_0", font_size=MIN_FONT, color=W_COLOR)
        lbl_q.next_to(axes.c2p(*q_start), UR, buff=0.10)
        lbl_q.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        descent_pts = [q_start]
        curr_d = q_start.copy()
        for _ in range(3):
            g = grad_func(curr_d[0], curr_d[1])
            curr_d = curr_d - 0.32 * g
            descent_pts.append(curr_d.copy())

        descent_arrows = []
        for i in range(len(descent_pts) - 1):
            q1 = axes.c2p(*descent_pts[i])
            q2 = axes.c2p(*descent_pts[i + 1])
            arr = Arrow(
                q1, q2,
                buff=0,
                stroke_width=4.5,
                max_tip_length_to_length_ratio=0.30,
                color=W_COLOR,
            )
            descent_arrows.append(arr)

        # 1. First frame: givens present
        self.add(
            axes, lbl_x, lbl_y, contours_group, peak_dot, peak_lbl,
            dot_start, lbl_start, c_ascent, c_rule,
        )
        self.wait(1.5)

        # 2. Draw steepest ascent steps one by one
        for arr in ascent_arrows:
            self.play(GrowArrow(arr), run_time=0.45)
        self.wait(0.5)
        self.play(FadeIn(c_shrink), run_time=0.8)

        # Flash peak
        self.play(FadeIn(flash_peak, run_time=0.25))
        self.play(FadeOut(flash_peak, run_time=0.25))
        self.wait(0.8)

        # 3. Contrast with steepest descent
        self.play(FadeIn(dot_q), Write(lbl_q), FadeIn(c_descent), FadeIn(c_rule2), run_time=1.0)
        self.wait(0.4)

        for arr in descent_arrows:
            self.play(GrowArrow(arr), run_time=0.45)
        self.wait(4.0)
