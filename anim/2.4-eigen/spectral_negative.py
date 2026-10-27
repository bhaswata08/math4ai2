"""Block 2.4: a negative eigenvalue flips its eigen-direction.

S = Q Lambda Q^T acts as three moves: Q^T turns the eigenvectors onto the
axes, Lambda scales (and here flips) along them, Q turns back. A gold
ghost of F under S applied in one go lands on the same F. The grid stays
still; only F, the eigenvector arrows and their span lines move.

F has an amber top bar (the q2 colour) so the flip is visible: the bar
crosses the q1 line during the Lambda step and ends on the other side.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.14 (eigenvectors) and
Visual Kernel, "SEE Matrix" (spectral theorem). Matrix: S = [[-1, -2], [-2, -1.8]].
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def rot(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


# F as three boxes (stem, middle bar, top bar) in a 1 x 1.35 cell, corner at origin.
F_PARTS = [
    ("stem", [(0, 0), (0.3, 0), (0.3, 1.1), (0, 1.1)], INK_DIM),
    ("mid", [(0.3, 0.6), (0.8, 0.6), (0.8, 0.85), (0.3, 0.85)], INK_DIM),
    ("top", [(0, 1.1), (1.0, 1.1), (1.0, 1.35), (0, 1.35)], RESULT_COLOR),
]
F_OUTLINE = [(0, 0), (0.3, 0), (0.3, 0.6), (0.8, 0.6), (0.8, 0.85), (0.3, 0.85),
             (0.3, 1.1), (1.0, 1.1), (1.0, 1.35), (0, 1.35)]


class SpectralNegative(Scene):
    """F goes through Q^T (rotate), Lambda = diag(0.64, -3.44) (shrink, stretch and flip), Q (rotate back)."""

    def construct(self):
        U = 0.42
        S_F = 2.4
        S = np.array([[-1.0, -2.0], [-2.0, -1.8]])
        lam, vec = np.linalg.eigh(S)
        order = np.argsort(-lam)
        lam, vec = lam[order], vec[:, order]
        q1 = vec[:, 0] * (1 if vec[0, 0] > 0 else -1)
        q2 = np.array([-q1[1], q1[0]])
        assert abs(abs(q2 @ vec[:, 1]) - 1) < 1e-9
        Q = np.column_stack([q1, q2])
        Lam = np.diag(lam)
        assert abs(np.linalg.det(Q) - 1) < 1e-9 and np.allclose(Q @ Lam @ Q.T, S)
        assert lam[0] > 0 > lam[1]
        theta = np.arctan2(Q.T[1, 0], Q.T[0, 0])  # Q^T turns by +theta

        def p3(v):
            return np.array([v[0] * U, v[1] * U, 0.0])

        plane = lin_plane(U)   # static background grid

        CEN = 5.6   # distance of the F along q1

        def fpt(x, y):
            """F lies on its side in the eigenframe: spine along q1, bars pointing along +q2,
            the amber top bar at the near end. Cell centred on the q1 line."""
            lu = (-y + 0.675) * S_F
            lv = (x - 0.5) * S_F
            w = Q @ np.array([CEN + lu, lv])
            return np.array([w[0], w[1], 0.0])

        def f_part(pts, color):
            poly = Polygon(*[fpt(x, y) for x, y in pts],
                           color=color, stroke_width=2, fill_color=color, fill_opacity=0.9)
            return poly

        parts_f = VGroup(*[f_part(p, c) for _n, p, c in F_PARTS])
        world = [(m, m.points.copy()) for m in parts_f]
        state = {"M": np.eye(2), "f": lambda t: np.eye(2)}
        tr = ValueTracker(0)

        def T():
            return state["f"](tr.get_value()) @ state["M"]

        def apply_world(_=None):
            Tm = T()
            for m, base in world:
                pts = base.copy()
                pts[:, :2] = base[:, :2] @ Tm.T * U
                m.set_points(pts)

        for m, _b in world:
            m.add_updater(apply_world)
        parts_f.set_z_index(3)
        apply_world()

        # S F must stay on screen with margin at every stage
        allp = np.vstack([b[:, :2] for _m, b in world])
        for M in (np.eye(2), Q.T, Lam @ Q.T, S):
            ext = np.abs(allp @ M.T * U).max(axis=0)
            assert ext[0] < 4.6 and ext[1] < 2.5, (M, ext)

        L = 1.2
        R_SPAN = 2.0   # span lines stop here so they never reach the caption or equation corners

        def arrow(q, color):
            def build():
                tip = T() @ (L * q)
                if np.linalg.norm(tip) * U < 0.06:
                    return Dot(ORIGIN, radius=0.05, color=color)
                return Arrow(ORIGIN, p3(tip), buff=0, color=color, stroke_width=6,
                             max_tip_length_to_length_ratio=0.35, tip_length=0.16)
            return build

        def span(q, color):
            def build():
                d = T() @ q
                d = d / max(np.linalg.norm(d), 1e-9)
                return DashedLine(ORIGIN - R_SPAN * np.array([d[0], d[1], 0]),
                                  R_SPAN * np.array([d[0], d[1], 0]), color=color, stroke_width=3,
                                  dash_length=0.12, stroke_opacity=0.9)
            return build

        def label(name, q, color, side):
            """Placed off the arrow tip on the bisector between the arrow's own line and
            the perpendicular one, so neither dashed line passes through it."""
            def build():
                tip = T() @ (L * q)
                d = tip / max(np.linalg.norm(tip), 1e-9)
                perp = np.array([-d[1], d[0]]) * side
                v = tip * U + 0.42 * d + 0.42 * perp
                t = tex(name, color)
                label_box(t, opacity=0.9, buff=0.05)
                t.move_to([v[0], v[1], 0])
                t.set_z_index(6)
                return t
            return build

        sp1 = always_redraw(span(q1, V_COLOR))
        sp2 = always_redraw(span(q2, RESULT_COLOR))
        ar1 = always_redraw(arrow(q1, V_COLOR))
        ar2 = always_redraw(arrow(q2, RESULT_COLOR))
        lb1 = always_redraw(label(r"\mathbf{q}_1", q1, V_COLOR, +1))
        lb2 = always_redraw(label(r"\mathbf{q}_2", q2, RESULT_COLOR, +1))
        for m in (sp1, sp2):
            m.set_z_index(2)
        for m in (ar1, ar2):
            m.set_z_index(5)
        plane.set_z_index(0)

        eq = MathTex("S", "=", "Q", r"\Lambda", r"Q^{T}", font_size=MIN_FONT, color=INK)
        eq.to_corner(UL, buff=0.25)
        parts = {"Q^T": eq[4], "L": eq[3], "Q": eq[2], "S": eq[0]}
        label_box(eq, opacity=0.95)
        eq.set_z_index(10)

        def caption(s, colour=INK):
            t = tex(s, colour)
            t.to_corner(DL, buff=0.25)
            label_box(t, opacity=1.0)
            t.set_z_index(10)
            return t

        cur = caption(r"\lambda_1=0.64,\ \lambda_2=-3.44")
        self.add(plane, sp1, sp2, parts_f, ar1, ar2, lb1, lb2, eq, cur)
        self.wait(2.5)

        def step(part, f, M_new, text, run=3.5, hold=1.6):
            nonlocal cur
            self.play(part.animate.set_color(HIGHLIGHT), run_time=0.4)
            new = caption(text)
            self.remove(cur)
            self.add(new)
            cur = new
            state["f"] = f
            self.play(tr.animate.set_value(1), run_time=run, rate_func=smooth)
            state["M"] = M_new
            state["f"] = lambda t: np.eye(2)
            tr.set_value(0)
            self.play(part.animate.set_color(INK), run_time=0.4)
            self.wait(hold)

        step(parts["Q^T"], lambda t: rot(t * theta), Q.T, r"\text{rotate: }\mathbf{q}_i\to\text{axes}")
        # Lambda: linear blend of the diagonal, so y passes through zero thickness
        step(parts["L"], lambda t: np.diag([(1 - t) + t * lam[0], (1 - t) + t * lam[1]]),
             Lam @ Q.T, r"x\times 0.64,\ y\times(-3.44)", run=6.0, hold=2.2)
        step(parts["Q"], lambda t: rot(-t * theta), Q @ Lam @ Q.T, r"\text{rotate back}")
        assert np.allclose(state["M"], S)

        # ghost outline of F, then S applied to it in one go
        gbase = Polygon(*[fpt(x, y) for x, y in F_OUTLINE]).points.copy()
        ghost = Polygon(*[fpt(x, y) * U for x, y in F_OUTLINE],
                        color=HIGHLIGHT, stroke_width=6, fill_opacity=0)
        ghost.set_z_index(4)
        gt = ValueTracker(0)

        def gup(_):
            Mg = (1 - gt.get_value()) * np.eye(2) + gt.get_value() * S
            pts = gbase.copy()
            pts[:, :2] = gbase[:, :2] @ Mg.T * U
            ghost.set_points(pts)

        ghost.add_updater(gup)
        new = caption(r"S\text{ in one go (gold)}", HIGHLIGHT)
        self.remove(cur)
        self.add(new)
        self.play(FadeIn(ghost), parts["S"].animate.set_color(HIGHLIGHT), run_time=0.8)
        cur = new
        self.wait(0.6)
        self.play(gt.animate.set_value(1), run_time=3.5, rate_func=smooth)
        new = caption(r"\text{same }F\text{, flipped}", HIGHLIGHT)
        self.remove(cur)
        self.add(new)
        self.play(parts["S"].animate.set_color(INK), run_time=0.6)
        self.wait(3)
