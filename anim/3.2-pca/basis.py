"""Block 3.2: one centred cloud, two bases; coordinates in a basis are dot products.

Data: anim/3.2-pca/data/cloud2d.csv (40 points, mean 0).
p1 = (2,1)/sqrt5, p2 = (-1,2)/sqrt5 are the eigenvectors of C = X^T X / m.
Storyline after Khapra, CS7015 Lecture 6 (change of basis); scenes rebuilt in Manim.
"""

from pathlib import Path

from shared.anim.house import *

X = np.loadtxt(Path(__file__).parent / "data" / "cloud2d.csv", delimiter=",", comments="#")
M, N = X.shape
assert (M, N) == (40, 2) and np.allclose(X.mean(axis=0), 0, atol=1e-5)
C = X.T @ X / M
EVALS, EVECS = np.linalg.eigh(C)
EVALS, EVECS = EVALS[::-1], EVECS[:, ::-1]
P1, P2 = EVECS[:, 0].copy(), EVECS[:, 1].copy()
if P1[0] < 0:
    P1 = -P1
if P2[1] < 0:
    P2 = -P2
PM = np.column_stack([P1, P2])
assert np.allclose(P1, np.array([2, 1]) / np.sqrt(5)) and np.allclose(P2, np.array([-1, 2]) / np.sqrt(5))
XHAT = X @ PM
VAR_X, VAR_Y = (X ** 2).mean(axis=0)
VAR_1, VAR_2 = (XHAT ** 2).mean(axis=0)


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def num(v):
    return f"{v:.2f}"


def grid_plane(S, O):
    p = house_plane(x_range=[-12, 12, 1], y_range=[-8, 8, 1], x_length=24 * S, y_length=16 * S)
    p.shift(O)
    return p


def dots_for(S, O, pts, color=V_COLOR, radius=0.045):
    return VGroup(*[Dot(O + S * np.array([a, b, 0.0]), radius=radius, color=color) for a, b in pts])


class NewBasis(Scene):
    def construct(self):
        S = 0.6
        O = np.array([0.0, 0.2, 0.0])
        theta = np.arctan2(1, 2)

        plane = grid_plane(S, O)
        xl = tex("x", X_COLOR).move_to(O + np.array([4.55, 0.3, 0]))
        yl = tex("y", Y_COLOR).move_to(O + np.array([0.3, 2.3, 0]))
        dots = dots_for(S, O, X)
        self.add(plane, xl, yl, dots)
        self.wait(1)

        # spread along x
        gx = dots_for(S, O, [(a, 0) for a in X[:, 0]], X_COLOR, 0.04)
        vx = tex(r"\mathrm{Var}(x)=" + num(VAR_X), X_COLOR).move_to([-2.4, -2.35, 0])
        self.play(AnimationGroup(*[TransformFromCopy(d, g) for d, g in zip(dots, gx)], lag_ratio=0.01),
                  run_time=1.3)
        self.play(FadeIn(vx))
        self.wait(1.5)
        # spread along y
        gy = dots_for(S, O, [(0, b) for b in X[:, 1]], Y_COLOR, 0.04)
        vy = tex(r"\mathrm{Var}(y)=" + num(VAR_Y), Y_COLOR).move_to([2.4, -2.35, 0])
        self.play(AnimationGroup(*[TransformFromCopy(d, g) for d, g in zip(dots, gy)], lag_ratio=0.01),
                  run_time=1.3)
        self.play(FadeIn(vy))
        self.wait(1.5)
        self.play(FadeOut(VGroup(gx, gy, vx, vy)))

        # the new basis
        a1 = Arrow(O, O + S * np.array([*P1, 0]), buff=0, color=RESULT_COLOR, stroke_width=7, tip_length=0.2)
        a2 = Arrow(O, O + S * np.array([*P2, 0]), buff=0, color=W_COLOR, stroke_width=7, tip_length=0.2)
        self.play(GrowArrow(a1), GrowArrow(a2))
        L1, L2 = 4.2, 1.9
        long1 = Arrow(O - L1 * np.array([*P1, 0]), O + L1 * np.array([*P1, 0]), buff=0, color=RESULT_COLOR,
                      stroke_width=5, tip_length=0.2)
        long2 = Arrow(O - L2 * np.array([*P2, 0]), O + L2 * np.array([*P2, 0]), buff=0, color=W_COLOR,
                      stroke_width=5, tip_length=0.2)
        self.play(Transform(a1, long1), Transform(a2, long2))
        d1, d2 = np.array([*P1, 0]), np.array([*P2, 0])
        l1 = tex(r"\mathbf p_1", RESULT_COLOR)
        l2 = tex(r"\mathbf p_2", W_COLOR)

        def follow(lab, arr):
            def up(m):
                e = arr.get_end() - arr.get_start()
                m.move_to(arr.get_end() + e / np.linalg.norm(e) * 0.4)
            lab.add_updater(up)
            up(lab)
        follow(l1, a1)
        follow(l2, a2)
        self.play(FadeIn(l1), FadeIn(l2))
        self.wait(1)

        # rotate so p1 is horizontal
        self.play(FadeOut(VGroup(plane, xl, yl)))
        self.play(Rotate(VGroup(dots, a1, a2), angle=-theta, about_point=O), run_time=2.5)
        self.wait(1)

        # spread along p1, p2
        g1 = dots_for(S, O, [(a, 0) for a in XHAT[:, 0]], RESULT_COLOR, 0.06)
        g2 = dots_for(S, O, [(0, b) for b in XHAT[:, 1]], W_COLOR, 0.06)
        v1 = tex(r"\mathrm{Var}(\alpha_1)=" + num(VAR_1), RESULT_COLOR).move_to([-2.4, -2.35, 0])
        v2 = tex(r"\mathrm{Var}(\alpha_2)=" + num(VAR_2), W_COLOR).move_to([2.4, -2.35, 0])
        self.play(a1.animate.set_stroke(width=2.5), a2.animate.set_stroke(width=2.5), run_time=0.5)
        self.play(AnimationGroup(*[TransformFromCopy(d, g) for d, g in zip(dots, g1)], lag_ratio=0.01),
                  run_time=1.3)
        self.play(FadeIn(v1))
        self.wait(1.5)
        self.play(AnimationGroup(*[TransformFromCopy(d, g) for d, g in zip(dots, g2)], lag_ratio=0.01),
                  run_time=1.3)
        self.play(FadeIn(v2))
        self.wait(2)


class CoordinatesXP(Scene):
    def construct(self):
        S = 0.62
        O = np.array([-2.0, 0.0, 0.0])
        px = 1.5  # left edge of the right-hand panel
        d1, d2 = np.array([*P1, 0]), np.array([*P2, 0])
        # a point with both coordinates visible: largest |alpha_2| among |alpha_1| > 1.5
        cand = [k for k in range(M) if abs(XHAT[k, 0]) > 1.5]
        i = max(cand, key=lambda k: abs(XHAT[k, 1]))
        xi = X[i]
        a1, a2 = XHAT[i]
        assert np.isclose(a1, xi @ P1) and np.isclose(a2, xi @ P2)

        L1, L2 = 2.9, 2.2
        line1 = Arrow(O - L1 * d1, O + L1 * d1, buff=0, color=RESULT_COLOR, stroke_width=4, tip_length=0.2)
        line2 = Arrow(O - L2 * d2, O + L2 * d2, buff=0, color=W_COLOR, stroke_width=4, tip_length=0.2)
        l1 = tex(r"\mathbf p_1", RESULT_COLOR).move_to(O + (L1 * d1) + d1 * 0.4)
        l2 = tex(r"\mathbf p_2", W_COLOR).move_to(O + (L2 * d2) + d2 * 0.4)
        dots = dots_for(S, O, X, radius=0.05)
        self.add(line1, line2, l1, l2, dots)
        self.wait(1)

        # one point
        pos = O + S * np.array([*xi, 0])
        big = Dot(pos, radius=0.1, color=HIGHLIGHT)
        self.play(FadeIn(big, scale=3), dots[i].animate.set_opacity(0), run_time=0.8)
        self.wait(0.5)
        self.play(big.animate.set_color(V_COLOR))
        lab_x = tex(r"\mathbf x_i", V_COLOR).move_to(pos + np.array([0.3, -0.38, 0]))
        self.play(FadeIn(lab_x))

        f1 = O + S * a1 * d1
        f2 = O + S * a2 * d2
        dl1 = DashedLine(pos, f1, color=RESULT_COLOR, stroke_width=4, dash_length=0.08)
        dl2 = DashedLine(pos, f2, color=W_COLOR, stroke_width=4, dash_length=0.08)
        self.play(Create(dl1))
        self.play(FadeIn(Dot(f1, radius=0.07, color=RESULT_COLOR)))
        t1 = VGroup(tex(r"\alpha_{i1}=\mathbf x_i^T\mathbf p_1", RESULT_COLOR),
                    tex(f"={num(a1)}", RESULT_COLOR)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t1.move_to([px, 1.65, 0], aligned_edge=LEFT)
        self.play(FadeIn(t1))
        self.wait(1.5)
        self.play(Create(dl2))
        self.play(FadeIn(Dot(f2, radius=0.07, color=W_COLOR)))
        t2 = VGroup(tex(r"\alpha_{i2}=\mathbf x_i^T\mathbf p_2", W_COLOR),
                    tex(f"={num(a2)}", W_COLOR)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t2.move_to([px, 0.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(t2))
        self.wait(1.5)

        # x_i = alpha_i1 p_1 + alpha_i2 p_2, tip to tail
        v1 = Arrow(O, f1, buff=0, color=RESULT_COLOR, stroke_width=9, tip_length=0.2)
        v2 = Arrow(f1, pos, buff=0, color=W_COLOR, stroke_width=7, tip_length=0.2)
        self.play(GrowArrow(v1))
        self.play(GrowArrow(v2))
        dec = VGroup(tex(r"\mathbf x_i=\alpha_{i1}\mathbf p_1", INK),
                     tex(r"\qquad+\alpha_{i2}\mathbf p_2", INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        dec.move_to([px, -1.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(dec))
        self.wait(2)

