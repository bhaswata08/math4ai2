# Shared 3D bowl loss surface helpers for Block 4.3 (and 4.2 reference style)
# Every loss picture in Block 4.3 shows the loss as a 3D surface, never as a contour map.

from shared.anim.house import *
import numpy as np

# -----------------------------------------------------------------------------
# Elliptical bowl: L = 0.5 w1^2 + 4 w2^2, Hessian diag(1, 8)
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


def bowl_surface(ax, l_max=L_MAX):
    """The elliptical bowl out to L = l_max, so the rim is a level set."""
    def pt(s, ang):
        lvl = l_max * s * s
        w1 = np.sqrt(2.0 * lvl) * np.cos(ang)
        w2 = np.sqrt(lvl / 4.0) * np.sin(ang)
        return ax.c2p(w1, w2, lvl)

    surf = Surface(pt, u_range=[0.001, 1.0], v_range=[0, TAU], resolution=(10, 28),
                   stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3)
    for face in surf.submobjects:
        face.set_fill(color=V_COLOR, opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60)
    return surf


def on_bowl(ax, w, lift=LIFT, loss_fn=LOSS):
    """The point of the surface above w, floated clear of the mesh."""
    return ax.c2p(w[0], w[1], loss_fn(w) + lift)


def top_row(parts, y=2.4):
    """parts: list of (tex, colour). Arranged in one row at the top of the frame."""
    row = VGroup(*[MathTex(t, font_size=MIN_FONT, color=c) for t, c in parts]).arrange(RIGHT, buff=0.55)
    return row.move_to(np.array([0.0, y, 0.0]))


def trail(ax, pts, color, opacity=1.0, lift=LIFT):
    g = VGroup()
    for i in range(len(pts) - 1):
        g.add(Line(on_bowl(ax, pts[i], lift=lift), on_bowl(ax, pts[i + 1], lift=lift),
                   color=color, stroke_width=4, stroke_opacity=opacity))
    for p in pts:
        g.add(Dot3D(on_bowl(ax, p, lift=lift), radius=0.05, color=color, fill_opacity=opacity))
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


# -----------------------------------------------------------------------------
# Circular isotropic bowl: L = 0.5 (w1^2 + w2^2) (for NoiseBallSchedule side-by-side)
# -----------------------------------------------------------------------------
def circular_bowl_axes(cx, cy=0.6):
    ax = ThreeDAxes(
        x_range=[-2.4, 2.4, 1.0], y_range=[-2.4, 2.4, 1.0], z_range=[0.0, 3.5, 1.0],
        x_length=3.4, y_length=2.4, z_length=1.5,
        axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                     "include_ticks": False, "include_tip": False},
    )
    ax.x_axis.set_color(X_COLOR)
    ax.y_axis.set_color(Y_COLOR)
    ax.shift(np.array([cx, cy, 0.0]))
    return ax


def circular_bowl_surface(ax, l_max=2.5):
    """Circular paraboloid mesh out to L = l_max."""
    def pt(s, ang):
        lvl = l_max * s * s
        r = np.sqrt(2.0 * lvl)
        w1 = r * np.cos(ang)
        w2 = r * np.sin(ang)
        return ax.c2p(w1, w2, lvl)

    surf = Surface(pt, u_range=[0.001, 1.0], v_range=[0, TAU], resolution=(8, 24),
                   stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3)
    for face in surf.submobjects:
        face.set_fill(color=V_COLOR, opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60)
    return surf


def on_circular_bowl(ax, w, lift=0.15):
    lvl = 0.5 * (w[0] ** 2 + w[1] ** 2)
    return ax.c2p(w[0], w[1], lvl + lift)
