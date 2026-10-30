"""Block 3.2, Act 4: drop the least important principal component of a 3D cloud and see what is lost.

Setup after Khapra, CS7015 Lec 6.5 (PCA: Interpretation 2, reconstruction error),
drawn the way the user asked: data in 3D, the three principal components beside it,
ditch p3, show the reconstruction loss as the segment from each point to the p1-p2 plane.
The cloud is thicker than ThreeToTwo's (lambda_3 = 0.5, not 0.1) so the loss is visible.
Every number on screen is computed here. Division is by m, as in the deck.
"""

from shared.anim.house import *
from shared.anim.linmap import label_box

M_PTS = 40
LAMS = np.array([4.0, 1.5, 0.5])
rng = np.random.default_rng(11)
_Z = rng.standard_normal((M_PTS, 3))
_Z -= _Z.mean(0)
_ev, _eV = np.linalg.eigh(_Z.T @ _Z / M_PTS)
_Z = _Z @ _eV @ np.diag(_ev ** -0.5) @ _eV.T          # exactly identity covariance


def _rot(ax, a):
    c, s = np.cos(a), np.sin(a)
    i, j = [(1, 2), (2, 0), (0, 1)][ax]
    R = np.eye(3)
    R[i, i], R[i, j], R[j, i], R[j, j] = c, -s, s, c
    return R


Q = _rot(2, np.radians(35)) @ _rot(0, np.radians(50)) @ _rot(1, np.radians(-20))
X = (_Z * np.sqrt(LAMS)) @ Q.T                         # rows x_i^T, centred
C = X.T @ X / M_PTS
_w, _V = np.linalg.eigh(C)
_o = np.argsort(_w)[::-1]
EIG, P = _w[_o], _V[:, _o]                             # columns p1, p2, p3
if P[2, 0] < 0:
    P[:, 0] *= -1
if P[2, 1] < 0:
    P[:, 1] *= -1
P[:, 2] = np.cross(P[:, 0], P[:, 1])
assert np.allclose(EIG, LAMS)
A = X @ P                                              # coordinates alpha_ij


def recon_without(k):
    """Points rebuilt from every component except p_k, and the mean squared loss."""
    keep = [j for j in range(3) if j != k]
    R = A[:, keep] @ P[:, keep].T
    loss = ((X - R) ** 2).sum(1).mean()
    assert np.isclose(loss, EIG[k])                    # the loss is the dropped eigenvalue
    return R, loss


S = 0.75                                               # scene units per data unit
COLS = [RESULT_COLOR, W_COLOR, X_COLOR]


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def view(el, az):
    """phi, theta, gamma for a camera `el` radians above the p1-p2 plane at azimuth `az` from p1,
    rolled so p3 points up the screen."""
    d = np.cos(el) * (np.cos(az) * P[:, 0] + np.sin(az) * P[:, 1]) + np.sin(el) * P[:, 2]
    phi, th = np.arccos(d[2]), np.arctan2(d[1], d[0])
    r = np.array([-np.sin(th), np.cos(th), 0])
    u = np.array([-np.cos(phi) * np.cos(th), -np.cos(phi) * np.sin(th), np.sin(phi)])
    return phi, th, np.arctan2(P[:, 2] @ r, P[:, 2] @ u)


def turn(scene, el, az, run_time):
    phi, th, gam = view(el, az)
    th0 = scene.camera.get_theta()
    th += 2 * np.pi * np.round((th0 - th) / (2 * np.pi))
    scene.move_camera(phi=phi, theta=th, gamma=gam, run_time=run_time)


def build():
    pts = X * S
    dots = VGroup(*[Dot3D(p, radius=0.05, color=V_COLOR) for p in pts])
    lens = np.maximum(np.sqrt(EIG) * S * 1.6, 0.75)
    arrows = [Arrow3D(ORIGIN, P[:, k] * lens[k], color=COLS[k], thickness=0.02, height=0.22,
                      base_radius=0.06) for k in range(3)]
    labs = [tex(rf"\mathbf p_{k + 1}", COLS[k]).move_to(P[:, k] * (lens[k] + 0.45)) for k in range(3)]
    return pts, dots, arrows, labs


def plane_of(k, pts_rec):
    """Rectangle in the plane of the two components other than p_k, holding every rebuilt point."""
    a, b = [j for j in range(3) if j != k]
    ra = np.abs(A[:, a]).max() * S + 0.15
    rb = np.abs(A[:, b]).max() * S + 0.15
    corners = [P[:, a] * sa * ra + P[:, b] * sb * rb for sa, sb in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    return Polygon(*corners, fill_color=INK_FAINT, fill_opacity=0.16,
                   stroke_color=INK_DIM, stroke_width=2, stroke_opacity=0.6)


def lam_row():
    row = VGroup(*[tex(rf"\lambda_{k + 1}={EIG[k]:.1f}", COLS[k]) for k in range(3)]).arrange(RIGHT, buff=0.45)
    row.to_corner(UL, buff=0.2)
    return label_box(row, opacity=0.9, buff=0.1)


class DropThird(ThreeDScene):
    def construct(self):
        pts, dots, arrows, labs = build()
        rec, loss = recon_without(2)
        phi0, th0, g0 = view(np.radians(28), np.radians(55))
        self.set_camera_orientation(phi=phi0, theta=th0, gamma=g0)
        self.add(dots)
        self.wait(1)

        # the three principal components, longest first
        row = lam_row()
        self.add_fixed_in_frame_mobjects(row)
        self.remove(row)
        for k in range(3):
            self.play(FadeIn(arrows[k]), FadeIn(labs[k]), run_time=0.7)
            self.add_fixed_orientation_mobjects(labs[k])
        self.play(FadeIn(row), run_time=0.6)
        turn(self, np.radians(28), np.radians(125), 4)          # slow turn so the depth reads
        self.wait(0.5)

        # ditch p3: keep the p1-p2 plane
        ditch = tex(r"\text{ditch } \mathbf p_3", X_COLOR)
        ditch.to_corner(UR, buff=0.2)
        label_box(ditch, opacity=0.9, buff=0.1)
        self.add_fixed_in_frame_mobjects(ditch)
        self.remove(ditch)
        self.play(FadeIn(ditch), arrows[2].animate.set_opacity(0.25), labs[2].animate.set_opacity(0.35))
        plane = plane_of(2, rec)
        self.play(FadeIn(plane), run_time=0.8)
        turn(self, np.radians(9), np.radians(90), 2.5)          # nearly edge-on: p1 across, p3 up
        self.wait(0.8)

        # each point falls onto the plane; the drop is what we lose
        recs = rec * S
        segs = VGroup(*[Line(a, b, color=Y_COLOR, stroke_width=4) for a, b in zip(pts, recs)])
        ghosts = VGroup(*[Dot3D(p, radius=0.04, color=V_COLOR).set_opacity(0.3) for p in pts])
        self.add(ghosts)
        self.play(Create(segs), run_time=1.2)
        self.play(*[d.animate.move_to(q) for d, q in zip(dots, recs)], run_time=1.6)
        self.wait(0.6)

        lossl = tex(rf"\text{{loss}} = \frac1m\sum_i \|\mathbf x_i - \hat{{\mathbf x}}_i\|^2 = {loss:.1f} = \lambda_3",
                    Y_COLOR)
        lossl.to_edge(DOWN, buff=0.2)
        label_box(lossl, opacity=0.9, buff=0.1)
        assert lossl.width < 9.6, lossl.width
        self.add_fixed_in_frame_mobjects(lossl)
        self.remove(lossl)
        self.play(FadeIn(lossl))
        self.wait(3)


class DropEach(ThreeDScene):
    def construct(self):
        pts, dots, arrows, labs = build()
        phi0, th0, g0 = view(np.radians(28), np.radians(55))
        self.set_camera_orientation(phi=phi0, theta=th0, gamma=g0)
        self.add(dots, *arrows, *labs)
        for l in labs:
            self.add_fixed_orientation_mobjects(l)
        row = lam_row()
        self.add_fixed_in_frame_mobjects(row)

        # scoreboard on the right: one line per choice
        lines = [tex(rf"\text{{ditch }}\mathbf p_{k + 1}:\ \text{{lose }} {EIG[k]:.1f}", COLS[k]) for k in range(3)]
        board = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(DR, buff=0.25)
        label_box(board, opacity=0.9, buff=0.12)
        self.wait(1)

        shown = []
        for k in range(3):
            rec, loss = recon_without(k)
            recs = rec * S
            plane = plane_of(k, rec)
            segs = VGroup(*[Line(a, b, color=Y_COLOR, stroke_width=4) for a, b in zip(pts, recs)])
            self.play(arrows[k].animate.set_opacity(0.25), labs[k].animate.set_opacity(0.35), FadeIn(plane),
                      run_time=0.7)
            self.play(Create(segs), run_time=1.2)
            self.add_fixed_in_frame_mobjects(lines[k])
            self.remove(lines[k])
            self.play(FadeIn(lines[k]), run_time=0.5)
            shown.append(lines[k])
            self.wait(1.5)
            self.play(FadeOut(segs), FadeOut(plane), arrows[k].animate.set_opacity(1),
                      labs[k].animate.set_opacity(1), run_time=0.6)
        best = SurroundingRectangle(lines[2], color=HIGHLIGHT, buff=0.08)
        self.add_fixed_in_frame_mobjects(best)
        self.remove(best)
        self.play(Create(best))
        self.wait(2.5)
