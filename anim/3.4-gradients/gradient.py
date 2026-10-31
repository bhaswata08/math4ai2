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


def ellipse_axes(c):
    """Semi-axes of the contour f_el = c."""
    return np.sqrt(c), np.sqrt(c) / 2.0


class PerpToContours(ThreeDScene):
    """The bowl z = x^2 + 4y^2, its level rings, and the same rings pushed down
    to the floor as a contour map. The gradient is a vector in the input plane,
    so every arrow is drawn on the floor. The camera flattens to a top view for
    the tight-versus-wide comparison, where the right angle reads true."""

    PHI = 58 * DEGREES
    THETA = -50 * DEGREES
    LEVELS = (1, 4, 9)
    ARROW = 0.16      # floor arrows drawn at 0.16x the gradient's length

    def construct(self):
        self.set_camera_orientation(phi=self.PHI, theta=self.THETA)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-1.8, 1.8, 1], z_range=[0, 18, 6],
            x_length=6.0, y_length=3.6, z_length=2.8,
            axis_config={"stroke_width": 2.5, "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.z_axis.set_opacity(0.0)   # the bowl reads its own height; the axis only clutters
        axes.shift(IN * 1.2)           # drop the bowl to the middle of the frame
        c2p = axes.c2p

        surface = Surface(
            lambda u, v: c2p(u, v, f_el(u, v)),
            u_range=[-3, 3], v_range=[-1.5, 1.5], resolution=(24, 12),
            stroke_color=INK_FAINT, stroke_width=0.8, stroke_opacity=0.5,
        )
        for face in surface.submobjects:
            face.set_fill(color=INK_DIM,
                          opacity=0.09 if (face.u_index + face.v_index) % 2 == 0 else 0.18)

        def ellipse(c, z, color, width):
            a, b = ellipse_axes(c)
            return ParametricFunction(
                lambda t, a=a, b=b: c2p(a * np.cos(t), b * np.sin(t), z),
                t_range=[0, TAU], color=color, stroke_width=width)

        # Level rings cut on the bowl, and the same rings on the floor.
        rings = VGroup(*[ellipse(c, c, V_COLOR if c == 4 else INK_DIM, 6 if c == 4 else 4)
                         for c in self.LEVELS])
        floor = VGroup(*[ellipse(c, 0, V_COLOR if c == 4 else INK_FAINT, 5 if c == 4 else 3.5)
                         for c in self.LEVELS])
        floor.set_z_index(3)

        def level_label(c, z, deg, out):
            """Label the contour f = c, placed just outside it at this angle."""
            a, b = ellipse_axes(c)
            t = np.radians(deg)
            m = MathTex(f"f={c}", font_size=MIN_FONT, color=V_COLOR if c == 4 else INK_DIM)
            m.move_to(c2p((a + out) * np.cos(t), (b + out * 0.5) * np.sin(t), z))
            m.add_background_rectangle(color=BG, opacity=0.85, buff=0.05)
            return m

        # On the bowl the labels sit off the back-left end of each ring, where
        # the rings own heights separate them; on the flat map they fan out
        # along the upper-left, one angle per level.
        FLAT_DEG = {1: 155, 4: 140, 9: 118}
        ring_lbls = VGroup(*[level_label(c, c, 180, 0.5) for c in self.LEVELS])

        ax_lbls = VGroup()
        for ch, col, pos in (("x", X_COLOR, (3.35, -0.4, 0)), ("y", Y_COLOR, (-0.4, 1.95, 0))):
            m = MathTex(ch, font_size=MIN_FONT, color=col).move_to(c2p(*pos))
            m.add_background_rectangle(color=BG, opacity=0.8, buff=0.04)
            ax_lbls.add(m)

        h_f = hud(r"f(x,y) = x^2 + 4y^2", 2.45, V_COLOR, x=-2.9)
        h_w = hud(r"\text{walk along } f = 4", 2.45, V_COLOR, x=3.0)

        # ---- the floor probe: tangent, gradient arrow, right-angle square ----
        def probe(deg):
            t = np.radians(deg)
            x, y = 2.0 * np.cos(t), np.sin(t)
            g = grad_el(x, y)
            mag = float(np.hypot(*g))
            gd = g / mag
            td = np.array([-gd[1], gd[0]])
            p = c2p(x, y, 0)
            tip = c2p(x + self.ARROW * g[0], y + self.ARROW * g[1], 0)
            arrow = Arrow(p, tip, buff=0, color=RESULT_COLOR, stroke_width=7,
                          max_tip_length_to_length_ratio=0.28)
            e = 1.0
            tangent = Line(c2p(x - e * td[0], y - e * td[1], 0),
                           c2p(x + e * td[0], y + e * td[1], 0),
                           color=INK, stroke_width=4)
            s = 0.30
            corners = [c2p(x + s * td[0], y + s * td[1], 0),
                       c2p(x + s * (td[0] + gd[0]), y + s * (td[1] + gd[1]), 0),
                       c2p(x + s * gd[0], y + s * gd[1], 0)]
            box = VMobject(color=HIGHLIGHT, stroke_width=4).set_points_as_corners(corners)
            grp = VGroup(tangent, arrow, box)
            grp.set_z_index(6)
            return grp, mag

        def walk(a0, a1, z):
            lo = np.radians(a0)
            hi = np.radians(a1) + (TAU if a1 <= a0 else 0.0)
            return ParametricFunction(
                lambda t: c2p(2.0 * np.cos(t), np.sin(t), z), t_range=[lo, hi])

        # ---- open on the bowl with its rings already cut -------------------
        self.add(axes, surface, rings)
        self.add_fixed_orientation_mobjects(*ring_lbls)
        self.add_fixed_in_frame_mobjects(h_f)
        self.wait(2.0)

        # ---- push the rings down: that is the contour map -------------------
        self.play(*[TransformFromCopy(r, fl) for r, fl in zip(rings, floor)], run_time=2.0)
        self.wait(1.2)

        # ---- walk the f = 4 ring, read the gradient on the floor ------------
        dot = Dot3D(c2p(2, 0, 4), radius=0.10, color=V_COLOR)
        shadow = Dot3D(c2p(2, 0, 0), radius=0.07, color=V_COLOR)
        shadow.set_z_index(8)
        drop = always_redraw(lambda: DashedLine(dot.get_center(), shadow.get_center(),
                                                color=INK_DIM, stroke_width=3))
        self.add(dot, shadow, drop)
        self.add_fixed_in_frame_mobjects(h_w)
        self.wait(0.8)

        cur = None
        prev = 0
        for deg in (0, 50, 130):
            if deg != prev:
                self.play(MoveAlongPath(dot, walk(prev, deg, 4.0)),
                          MoveAlongPath(shadow, walk(prev, deg, 0.0)),
                          run_time=1.4, rate_func=smooth)
            grp, _ = probe(deg)
            if cur is not None:
                self.play(FadeOut(cur), run_time=0.4)
            self.play(Create(grp[0]), GrowArrow(grp[1]), Create(grp[2]), run_time=1.2)
            cur = grp
            prev = deg
            self.wait(1.4)

        # ---- drop the bowl away and flatten to the map ----------------------
        self.remove(drop)
        self.play(FadeOut(cur), FadeOut(surface), FadeOut(rings), FadeOut(ring_lbls),
                  FadeOut(dot), FadeOut(h_w), run_time=1.0)
        self.move_camera(phi=0.0, theta=-90 * DEGREES, run_time=2.0)

        floor_lbls = VGroup(*[level_label(c, 0, FLAT_DEG[c], 0.35) for c in self.LEVELS])
        floor_lbls.set_z_index(9)
        # The axis letters only earn their place once the map is flat; in the
        # tilted view the +y end sits inside the bowl.
        self.add_fixed_orientation_mobjects(*floor_lbls, *ax_lbls)
        self.wait(1.0)

        # ---- wide contours give a short arrow, tight ones a long arrow ------
        self.play(MoveAlongPath(shadow, walk(prev, 360, 0.0)), run_time=1.3)
        g0, m0 = probe(0)
        self.play(Create(g0[0]), GrowArrow(g0[1]), Create(g0[2]), run_time=1.0)
        l0 = MathTex(rf"|\nabla f| = {m0:g}", font_size=MIN_FONT, color=RESULT_COLOR)
        l0.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
        l0.next_to(g0[1].get_end(), RIGHT, buff=0.15)
        self.add_fixed_orientation_mobjects(l0)
        self.wait(1.2)

        self.play(MoveAlongPath(shadow, walk(0, 90, 0.0)), run_time=1.3)
        g1, m1 = probe(90)
        self.play(Create(g1[0]), GrowArrow(g1[1]), Create(g1[2]), run_time=1.0)
        l1 = MathTex(rf"|\nabla f| = {m1:g}", font_size=MIN_FONT, color=RESULT_COLOR)
        l1.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)
        l1.next_to(g1[1].get_end(), RIGHT, buff=0.15)
        self.add_fixed_orientation_mobjects(l1)
        self.wait(1.2)

        tight = hud(r"\text{tighter} \to \text{longer}", -2.45, RESULT_COLOR, x=3.0)
        self.add_fixed_in_frame_mobjects(tight)
        self.wait(2.5)


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
# SCENE 4: DirectionalDerivative  (the slope of the hill along u)
# =============================================================================
# The same hill the ascent clip climbs, f_func, read at one point on its flank.
# On the flank due west of the peak, so grad f runs along +x and always
# projects across the screen rather than down it.
PD = np.array([-0.9, -0.3])


class DirectionalDerivative(ThreeDScene):
    """Turn a unit vector u on the floor and watch two things move together:
    the shadow of grad f on u, down on the map, and the tilt of the hill along
    u, up on the surface. They are the same number, D_u f."""

    PHI = 62 * DEGREES
    THETA = -130 * DEGREES  # camera on p's side, so the point is never behind the dome
    SHIFT = np.array([-1.95, 0.15, 0.0])   # a true screen offset, see the transpose below
    XR = (-2.1, 2.25)
    YR = (-1.8, 1.4)

    def construct(self):
        self.set_camera_orientation(phi=self.PHI, theta=self.THETA)
        S = 0.95                                   # screen units per unit of x, y and z
        x_min, x_max = self.XR
        y_min, y_max = self.YR

        axes = ThreeDAxes(
            x_range=[x_min, x_max, 1.0], y_range=[y_min, y_max, 1.0], z_range=[0, 2.4, 1.0],
            x_length=(x_max - x_min) * S, y_length=(y_max - y_min) * S, z_length=2.4 * S,
            axis_config={"stroke_width": 2.0, "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.z_axis.set_opacity(0.0)
        # SHIFT is where the hill should sit on screen, so it has to be sent
        # back through the inverse of the camera rotation, not through the
        # rotation itself.
        axes.shift(np.dot(self.SHIFT, self.camera.get_rotation_matrix().T))
        c2p = axes.c2p

        surface = Surface(
            lambda u, v: c2p(u, v, f_func(u, v)),
            u_range=[x_min, x_max], v_range=[y_min, y_max], resolution=(28, 26),
            stroke_color=INK_FAINT, stroke_width=0.8, stroke_opacity=0.5,
        )
        for face in surface.submobjects:
            face.set_fill(color=INK_DIM,
                          opacity=0.08 if (face.u_index + face.v_index) % 2 == 0 else 0.17)

        FP = float(f_func(*PD))                    # the hill's height at p
        G = grad_func(*PD)
        GM = float(np.hypot(*G))
        AL = float(np.arctan2(G[1], G[0]))

        def flat(v):
            return c2p(PD[0] + v[0], PD[1] + v[1], 0.0)

        P3 = c2p(PD[0], PD[1], FP)
        P0 = flat(np.zeros(2))
        drop = DashedLine(P3, P0, color=INK_FAINT, stroke_width=2.5)
        dot_p = Dot3D(P3, radius=0.09, color=RESULT_COLOR).set_z_index(20)
        dot_f = Dot3D(P0, radius=0.06, color=RESULT_COLOR).set_z_index(11)

        circle = ParametricFunction(lambda t: flat(np.array([np.cos(t), np.sin(t)])),
                                    t_range=[0, TAU], color=INK_FAINT,
                                    stroke_width=3).set_z_index(10)
        grad_arrow = Arrow3D(P0, flat(G), color=RESULT_COLOR, thickness=0.030,
                             height=0.22, base_radius=0.085).set_z_index(14)
        grad_lbl = MathTex(r"\nabla f", font_size=MIN_FONT, color=RESULT_COLOR)
        grad_lbl.move_to(flat(G * 1.0 + np.array([0.34, -0.2])))
        grad_lbl.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

        # The contour ring through p, cut on the hill. Only the near arc is
        # drawn: manim cannot hide the far half behind the dome, and a full
        # ring then reads as a hoop floating above the surface.
        a_c = np.sqrt(2.5 * np.log(2.0 / FP))
        b_c = a_c / np.sqrt(2.0)
        t_near = self.THETA
        ring = ParametricFunction(
            lambda t: c2p(0.5 + a_c * np.cos(t), -0.3 + b_c * np.sin(t), FP),
            t_range=[t_near - 1.75, t_near + 1.75], color=INK,
            stroke_width=5).set_z_index(16)

        th = ValueTracker(0.0)

        def ang():
            return AL + th.get_value()

        def uvec():
            a = ang()
            return np.array([np.cos(a), np.sin(a)])

        def dval():
            return GM * np.cos(th.get_value())

        def u_arrow():
            return Arrow3D(P0, flat(uvec()), color=W_COLOR, thickness=0.030,
                           height=0.2, base_radius=0.08).set_z_index(15)

        def u_line():
            d = uvec()
            return DashedLine(flat(-1.4 * d), flat(1.4 * d),
                              color=INK_FAINT, stroke_width=2.5).set_z_index(9)

        def shade():
            d = dval()
            foot = uvec() * d
            seg = Line(P0, flat(foot), color=RESULT_COLOR, stroke_width=13,
                       stroke_opacity=0.9).set_z_index(12) if abs(d) > 0.03 else VGroup()
            tie = DashedLine(flat(G), flat(foot), color=INK_DIM,
                             stroke_width=2.5).set_z_index(12) \
                if float(np.linalg.norm(G - foot)) > 0.05 else VGroup()
            return VGroup(seg, tie)

        def slice_curve():
            d = uvec()
            return ParametricFunction(
                lambda t: c2p(PD[0] + t * d[0], PD[1] + t * d[1],
                              f_func(PD[0] + t * d[0], PD[1] + t * d[1])),
                t_range=[-1.0, 1.0], color=V_COLOR, stroke_width=6).set_z_index(17)

        def tangent():
            d, m, e = uvec(), dval(), 0.7
            return Line(c2p(PD[0] - e * d[0], PD[1] - e * d[1], FP - e * m),
                        c2p(PD[0] + e * d[0], PD[1] + e * d[1], FP + e * m),
                        color=RESULT_COLOR, stroke_width=7).set_z_index(18)

        u_arr = always_redraw(u_arrow)
        u_ln = always_redraw(u_line)
        shd = always_redraw(shade)
        sl = always_redraw(slice_curve)
        tg = always_redraw(tangent)

        u_lbl = MathTex(r"\mathbf{u}", font_size=MIN_FONT, color=W_COLOR)
        u_lbl.add_background_rectangle(color=BG, opacity=0.9, buff=0.05)

        def place_u(m):
            d = uvec()
            m.move_to(flat(1.05 * d + 0.42 * np.array([-d[1], d[0]])))

        u_lbl.add_updater(place_u)
        place_u(u_lbl)

        # ---- the right column: the rule, the reading, the cosine ------------
        rx = 3.1
        h_def = hud(r"D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}", 2.4, INK, x=rx)
        h_unit = hud(r"|\mathbf{u}| = 1", 1.72, INK_DIM, x=rx)

        plot = Axes(x_range=[0, TAU, PI], y_range=[-GM, GM, 1], x_length=2.6, y_length=1.5,
                    axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5,
                                 "include_ticks": False}, tips=False)
        plot.move_to(np.array([rx, -1.55, 0.0]))
        curve_full = plot.plot(lambda t: GM * np.cos(t), x_range=[0, TAU],
                               color=INK_FAINT, stroke_width=3)
        t_lbls = VGroup(*[MathTex(s_, font_size=MIN_FONT, color=INK_DIM).move_to(
            np.array([plot.c2p(v, 0)[0], plot.c2p(0, -GM)[1] - 0.34, 0.0]))
            for s_, v in (("0", 0), (r"\pi", PI), (r"2\pi", TAU))])
        y_lbl = MathTex(r"D_{\mathbf{u}} f", font_size=MIN_FONT, color=RESULT_COLOR)
        y_lbl.next_to(plot.y_axis.get_top(), LEFT, buff=0.1)
        x_lbl = MathTex(r"\theta", font_size=MIN_FONT, color=W_COLOR)
        x_lbl.next_to(plot.x_axis.get_end(), UP, buff=0.12)

        # Both are single VMobjects, so become() never swaps their families and
        # the fixed-in-frame flag survives every redraw.
        trace = always_redraw(lambda: plot.plot(
            lambda t: GM * np.cos(t), x_range=[0, max(th.get_value(), 0.01)],
            color=RESULT_COLOR, stroke_width=5))
        mover = always_redraw(lambda: Dot(plot.c2p(th.get_value(), dval()),
                                          radius=0.09, color=W_COLOR))

        self.add(axes, surface, circle, u_ln, shd, grad_arrow, u_arr, drop, sl, tg,
                 dot_f, dot_p)
        self.add_fixed_orientation_mobjects(grad_lbl, u_lbl)
        self.add_fixed_in_frame_mobjects(h_def, h_unit, plot, curve_full, t_lbls,
                                         y_lbl, x_lbl, trace, mover)

        def stop(deg, tex, colour):
            # Two short lines, never one long one: a single line runs off the
            # right edge of the frame.
            a = hud(rf"\theta = {deg}^\circ", 1.05, colour, x=rx)
            b = hud(tex, 0.38, colour, x=rx)
            d = Dot(plot.c2p(np.radians(deg), GM * np.cos(np.radians(deg))),
                    radius=0.11, color=HIGHLIGHT)
            self.add_fixed_in_frame_mobjects(a, b, d)
            return VGroup(a, b)

        def note(tex, colour):
            m = hud(tex, 2.4, colour, x=-3.05)
            self.add_fixed_in_frame_mobjects(m)
            return m

        # theta = 0: straight up the hill
        self.wait(1.2)
        r0 = stop(0, rf"D_{{\mathbf{{u}}}} f = {GM:.2f}", RESULT_COLOR)
        n0 = note(r"\text{steepest climb}", RESULT_COLOR)
        self.wait(2.4)
        self.play(FadeOut(n0), FadeOut(r0), run_time=0.4)

        # theta = 90: along the contour, the hill is level
        self.play(th.animate.set_value(PI / 2), run_time=3.5, rate_func=smooth)
        r1 = stop(90, r"D_{\mathbf{u}} f = 0", INK)
        n1 = note(r"\text{contour: slope } 0", INK)
        self.play(Create(ring), run_time=1.0)
        self.wait(2.4)
        self.play(FadeOut(n1), FadeOut(r1), FadeOut(ring), run_time=0.4)

        # theta = 180: straight down
        self.play(th.animate.set_value(PI), run_time=3.5, rate_func=smooth)
        r2 = stop(180, rf"D_{{\mathbf{{u}}}} f = -{GM:.2f}", W_COLOR)
        n2 = note(r"\text{steepest descent}", W_COLOR)
        self.wait(2.4)
        self.play(FadeOut(n2), FadeOut(r2), run_time=0.4)

        # finish the turn
        self.play(th.animate.set_value(TAU), run_time=4.0, rate_func=smooth)
        self.wait(2.0)


# =============================================================================
# SCENE 5: SteepestAscent  (the hill itself, climbed)
# =============================================================================
class SteepestAscent(ThreeDScene):
    """The hill f_func as a surface, its contour map on the floor underneath,
    and the ascent rule walked up the hillside: each amber arrow is one step of
    x_{k+1} = x_k + 0.4 grad f, with its shadow on the map below. The violet
    arrows run the same rule with the sign flipped and go downhill."""

    PHI = 62 * DEGREES
    THETA = -70 * DEGREES   # -50 sends the descent arrows straight down the screen
    SHIFT = np.array([-1.8, -1.6, 0.0])     # where the hill sits on screen
    LEVELS = (0.65, 0.90, 1.15, 1.40, 1.65, 1.85)
    PEAK = (0.5, -0.3)

    def construct(self):
        self.set_camera_orientation(phi=self.PHI, theta=self.THETA)
        x_min, x_max = -1.25, 2.9
        y_min, y_max = -1.8, 1.2
        S = 1.05                                  # screen units per unit of x, y

        axes = ThreeDAxes(
            x_range=[x_min, x_max, 1.0], y_range=[y_min, y_max, 1.0], z_range=[0, 2.4, 1.0],
            x_length=(x_max - x_min) * S, y_length=(y_max - y_min) * S, z_length=2.2 * 1.2,
            axis_config={"stroke_width": 2.5, "include_ticks": False, "include_tip": False},
        )
        axes.x_axis.set_color(X_COLOR)
        axes.y_axis.set_color(Y_COLOR)
        axes.z_axis.set_opacity(0.0)
        axes.shift(np.dot(self.SHIFT, self.camera.get_rotation_matrix()))
        c2p = axes.c2p

        surface = Surface(
            lambda u, v: c2p(u, v, f_func(u, v)),
            u_range=[x_min, x_max], v_range=[y_min, y_max], resolution=(28, 24),
            stroke_color=INK_FAINT, stroke_width=0.8, stroke_opacity=0.5,
        )
        for face in surface.submobjects:
            face.set_fill(color=INK_DIM,
                          opacity=0.07 if (face.u_index + face.v_index) % 2 == 0 else 0.15)

        # The contour map, on the floor under the hill.
        contours = VGroup()
        for lvl in self.LEVELS:
            a = np.sqrt(2.5 * np.log(2.0 / lvl))
            b = a / np.sqrt(2.0)
            contours.add(ParametricFunction(
                lambda t, a=a, b=b: c2p(self.PEAK[0] + a * np.cos(t),
                                        self.PEAK[1] + b * np.sin(t), 0.0),
                t_range=[0, TAU], color=INK_DIM, stroke_width=2.5))
        contours.set_z_index(2)

        summit = c2p(*self.PEAK, f_func(*self.PEAK))
        peak_dot = Dot3D(summit, radius=0.09, color=V_COLOR)
        peak_pin = DashedLine(summit, c2p(*self.PEAK, 0.0), color=INK_FAINT, stroke_width=2.5)
        peak_lbl = MathTex(r"\text{peak}", font_size=MIN_FONT, color=V_COLOR)
        peak_lbl.move_to(summit + np.array([0.0, 0.45, 0.0]))
        peak_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        ax_lbls = VGroup()
        for ch, col, pos in (("x", X_COLOR, (x_max + 0.28, 0.0, 0.0)),
                             ("y", Y_COLOR, (0.0, y_max + 0.32, 0.0))):
            m = MathTex(ch, font_size=MIN_FONT, color=col).move_to(c2p(*pos))
            m.add_background_rectangle(color=BG, opacity=0.8, buff=0.04)
            ax_lbls.add(m)

        def march(start, lr, n):
            """n steps of x <- x + lr * grad f from start."""
            pts = [np.array(start, dtype=float)]
            for _ in range(n):
                pts.append(pts[-1] + lr * grad_func(*pts[-1]))
            return pts

        def climb(p, q, color):
            """One step, drawn on the hillside, with its shadow on the map."""
            a, b = c2p(p[0], p[1], f_func(*p)), c2p(q[0], q[1], f_func(*q))
            L = float(np.linalg.norm(b - a))
            arr = Arrow3D(a, b, color=color, thickness=0.036,
                          height=min(0.26, 0.55 * L), base_radius=min(0.095, 0.22 * L))
            arr.set_z_index(7)
            sh = DashedLine(c2p(p[0], p[1], 0.0), c2p(q[0], q[1], 0.0),
                            color=color, stroke_width=3).set_opacity(0.45)
            sh.set_z_index(4)
            return arr, sh

        def marker(p, color, tex, shift):
            d = Dot3D(c2p(p[0], p[1], f_func(*p)), radius=0.08, color=color).set_z_index(9)
            s = Dot3D(c2p(p[0], p[1], 0.0), radius=0.055, color=color).set_z_index(5)
            s.set_opacity(0.55)
            m = MathTex(tex, font_size=MIN_FONT, color=color)
            m.move_to(d.get_center() + shift)
            m.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)
            return d, s, m

        up = march((-1.0, -1.2), 0.40, 6)
        # Due east of the peak, so every descent step runs along +x and
        # reads as a step across the screen, not a drop through the hill.
        down = march((1.6, -0.3), -0.32, 3)

        d0, s0, l0 = marker(up[0], RESULT_COLOR, r"\mathbf{x}_0", np.array([0.45, 0.1, 0.0]))
        dq, sq, lq = marker(down[0], W_COLOR, r"\mathbf{w}_0", np.array([0.45, 0.2, 0.0]))

        rx = 2.85
        h_asc = hud(r"\text{ascent: follow } +\nabla f", 2.35, RESULT_COLOR, x=rx)
        h_rule = hud(r"\mathbf{x}_{k+1} = \mathbf{x}_k + 0.4\,\nabla f", 1.55, RESULT_COLOR, x=rx)
        h_short = hud(r"\text{steps get shorter}", 0.75, INK_DIM, x=rx)
        h_desc = hud(r"\text{descent: follow } -\nabla f", -0.45, W_COLOR, x=rx)
        h_rule2 = hud(r"\mathbf{w}_{k+1} = \mathbf{w}_k - 0.32\,\nabla f", -1.25, W_COLOR, x=rx)

        # ---- open on the hill with its map and the starting point ----------
        self.add(axes, surface, contours, peak_pin, peak_dot, d0, s0)
        self.add_fixed_orientation_mobjects(peak_lbl, l0, *ax_lbls)
        self.add_fixed_in_frame_mobjects(h_asc, h_rule)
        self.wait(1.8)

        # ---- climb ---------------------------------------------------------
        for p, q in zip(up, up[1:]):
            arr, sh = climb(p, q, RESULT_COLOR)
            self.play(Create(arr), Create(sh), run_time=0.5)
        self.wait(0.5)
        self.add_fixed_in_frame_mobjects(h_short)
        self.wait(1.2)

        flash = Dot3D(summit, radius=0.18, color=HIGHLIGHT)
        self.play(FadeIn(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.3)
        self.wait(0.8)

        # ---- the same rule with the sign flipped runs downhill -------------
        self.add(dq, sq)
        self.add_fixed_orientation_mobjects(lq)
        self.add_fixed_in_frame_mobjects(h_desc, h_rule2)
        self.wait(0.8)
        for p, q in zip(down, down[1:]):
            arr, sh = climb(p, q, W_COLOR)
            self.play(Create(arr), Create(sh), run_time=0.5)
        self.wait(1.2)

        self.begin_ambient_camera_rotation(rate=0.035)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)
