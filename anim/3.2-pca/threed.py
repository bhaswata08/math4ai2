"""Block 3.2: a flat 3D cloud, the three eigenvectors of C, projection onto the top-2 plane."""

from shared.anim.house import *
from shared.anim.linmap import label_box

# ---- data: 80 centred points, exact covariance, tilted frame --------------------------------
M_PTS = 80
LAMS = np.array([4.0, 1.5, 0.1])
rng = np.random.default_rng(7)
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
if np.dot(np.cross(P[:, 0], P[:, 1]), P[:, 2]) < 0:    # right-handed: p1 x p2 = p3
    P[:, 2] *= -1
if P[2, 0] < 0:                                        # p1 and p2 both turn the same way
    P[:, 0] *= -1; P[:, 1] *= -1
P[:, 2] = np.cross(P[:, 0], P[:, 1])
SHARE = EIG[:2].sum() / EIG.sum()
ALPHA = X @ P[:, :2]                                   # (m, 2) = X P_2
PROJ = ALPHA @ P[:, :2].T                              # points on the plane, in R^3
S = 0.42                                               # world units per data unit
assert np.allclose(np.diag(P.T @ C @ P), EIG)


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def view_angles(el, az):
    """phi, theta for a camera `el` radians above the p1-p2 plane, at azimuth `az` within it."""
    d = np.cos(el) * (np.cos(az) * P[:, 0] + np.sin(az) * P[:, 1]) + np.sin(el) * P[:, 2]
    return np.arccos(d[2]), np.arctan2(d[1], d[0])


def cam_for_view(d, p1):
    """phi, theta, gamma so the camera sits along d and p1 points right on screen."""
    phi = np.arccos(d[2])
    th = np.arctan2(d[1], d[0])
    r = np.array([-np.sin(th), np.cos(th), 0])
    u = np.array([-np.cos(phi) * np.cos(th), -np.cos(phi) * np.sin(th), np.sin(phi)])
    a = np.arctan2(p1 @ u, p1 @ r)
    return phi, th, -a


class ThreeToTwo(ThreeDScene):
    def construct(self):
        pts = X * S
        proj = PROJ * S
        dots = VGroup(*[Dot3D(p, radius=0.045, color=V_COLOR) for p in pts])
        axes = VGroup(
            Line([-2.6, 0, 0], [2.6, 0, 0], color=INK_DIM, stroke_width=3),
            Line([0, -2.6, 0], [0, 2.6, 0], color=INK_DIM, stroke_width=3),
            Line([0, 0, -1.6], [0, 0, 1.6], color=INK_DIM, stroke_width=3))
        axlab = [tex(n, INK_DIM).move_to(v) for n, v in
                 (("x", [2.9, 0, 0]), ("y", [0, 2.9, 0]), ("z", [0, 0, 1.95]))]

        cols = [RESULT_COLOR, W_COLOR, INK_FAINT]
        lens = np.sqrt(EIG) * S * 1.5
        lens[2] = 0.5                      # p3 would be a stub at true scale; drawn longer
        arrows = [Arrow3D(ORIGIN, P[:, k] * lens[k], color=cols[k], thickness=0.02, height=0.22,
                          base_radius=0.06) for k in range(3)]
        plab = [tex(rf"\mathbf{{p}}_{k + 1}", cols[k] if k < 2 else INK_DIM)
                .move_to(P[:, k] * (lens[k] + (0.65 if k == 0 else 0.5))) for k in range(3)]

        # plane spanned by p1, p2, wide enough to hold every projected point
        a1 = np.abs(ALPHA[:, 0]).max() * S + 0.1
        a2 = np.abs(ALPHA[:, 1]).max() * S + 0.1
        corners = [P[:, 0] * s1 * a1 + P[:, 1] * s2 * a2 for s1, s2 in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
        plane = Polygon(*corners, fill_color=RESULT_COLOR, fill_opacity=0.18,
                        stroke_color=RESULT_COLOR, stroke_width=2, stroke_opacity=0.7)

        lam_row = VGroup(
            tex(rf"\lambda_1={EIG[0]:.1f}", RESULT_COLOR),
            tex(rf"\lambda_2={EIG[1]:.1f}", W_COLOR),
            tex(rf"\lambda_3={EIG[2]:.1f}", INK_DIM)).arrange(RIGHT, buff=0.5)
        lam_row.to_corner(UL, buff=0.2)
        xp = tex(r"X P_2\ \ (80\times 2)", INK)
        xp.to_corner(UL, buff=0.2)
        share = tex(rf"\frac{{\lambda_1+\lambda_2}}{{\lambda_1+\lambda_2+\lambda_3}}={100 * SHARE:.1f}\%\ \text{{kept}}")
        share.to_edge(DOWN, buff=0.2)
        for m in (lam_row, xp, share):
            label_box(m, opacity=0.9, buff=0.1)
        assert share.width < 9.5, share.width

        el = np.radians(22)
        az0 = np.radians(-40)
        phi0, th0 = view_angles(el, az0)
        self.set_camera_orientation(phi=phi0, theta=th0)
        self.add(axes, dots)
        self.add_fixed_orientation_mobjects(*axlab)
        self.add_fixed_in_frame_mobjects(lam_row)
        self.wait(1.5)

        # eigenvectors, with a slow ambient turn so the flatness reads
        for k in range(3):
            self.play(FadeIn(arrows[k]), FadeIn(plab[k]), run_time=0.7)
            self.add_fixed_orientation_mobjects(plab[k])
        cur = th0
        for az in np.radians(np.linspace(-40, 120, 7)[1:]):      # slow turn about p3
            ph, th = view_angles(el, az)
            th += 2 * np.pi * np.round((cur - th) / (2 * np.pi))
            self.move_camera(phi=ph, theta=th, run_time=0.9, rate_func=linear)
            cur = th
        self.wait(0.5)

        # plane of p1, p2
        self.play(FadeIn(plane), run_time=1.0)
        self.wait(1.2)
        segs = VGroup(*[Line(a, b, color=W_COLOR, stroke_width=2) for a, b in zip(pts, proj)])
        self.play(Create(segs), run_time=1.2)
        self.wait(0.5)
        self.play(*[d.animate.move_to(q) for d, q in zip(dots, proj)], run_time=1.8)
        self.wait(0.8)

        # look straight down p3
        self.play(FadeOut(segs), FadeOut(VGroup(axes, arrows[2])), *[FadeOut(l) for l in axlab + [plab[2]]],
                  run_time=0.6)
        phi, th, gam = cam_for_view(P[:, 2], P[:, 0])
        self.move_camera(phi=phi, theta=th, gamma=gam, run_time=3.5)
        self.wait(0.8)
        self.play(FadeOut(lam_row), run_time=0.3)
        self.add_fixed_in_frame_mobjects(xp, share)
        self.play(FadeIn(xp), FadeIn(share), run_time=0.8)
        self.wait(2.0)
