"""Block 2.4: composition and decomposition shown on four panels of F.

Remakes two card sequences of Visual Kernel, "SEE Matrix" ch.2 (03:56-04:25),
which use third-party art, with the F of SpectralNegative instead.

ComposeF: read right to left. F is scaled in x by 2.5, then in y by 0.6, then
reflected; the left panel applies the product diag(-2.5, 0.6) in one go and
lands on the same F.

DecomposeF: the left panel applies M = A3 A2 A1 in one go. The other panels
start as "?" and then show the simple moves that build it, right to left:
scale, reflect, shear. The last one lands on the same F as M.
"""

from shared.anim.house import *
from shared.anim.linmap import *


# F as three boxes (stem, middle bar, top bar), corner at the origin; same F as SpectralNegative.
F_PARTS = [
    ([(0, 0), (0.3, 0), (0.3, 1.1), (0, 1.1)], INK_DIM),
    ([(0.3, 0.6), (0.8, 0.6), (0.8, 0.85), (0.3, 0.85)], INK_DIM),
    ([(0, 1.1), (1.0, 1.1), (1.0, 1.35), (0, 1.35)], RESULT_COLOR),
]
F_OUTLINE = [(0, 0), (0.3, 0), (0.3, 0.6), (0.8, 0.6), (0.8, 0.85), (0.3, 0.85),
             (0.3, 1.1), (1.0, 1.1), (1.0, 1.35), (0, 1.35)]

SIDE = 2.25    # panel width in scene units
HALF = 3       # each panel shows -3..3 in both directions
U = SIDE / (2 * HALF)
GAP = 0.22
CY = 0.6       # panel centre height


def panel_x(i):
    return (i - 1.5) * (SIDE + GAP)


class Panel:
    """A framed square with a static grid and an F that a matrix moves."""

    def __init__(self, i, scene):
        self.c = np.array([panel_x(i), CY, 0.0])
        frame = Square(SIDE, color=INK, stroke_width=3).move_to(self.c)
        lines = VGroup()
        for k in range(-HALF, HALF + 1):
            col = INK_DIM if k == 0 else GRID
            w = 2 if k == 0 else 1.5
            lines.add(Line(self.c + U * np.array([k, -HALF, 0]), self.c + U * np.array([k, HALF, 0]),
                           color=col, stroke_width=w))
            lines.add(Line(self.c + U * np.array([-HALF, k, 0]), self.c + U * np.array([HALF, k, 0]),
                           color=col, stroke_width=w))
        self.box = VGroup(lines, frame)
        self.scene = scene
        self.f = None

    def make_f(self, M):
        parts = VGroup(*[Polygon(*[np.array([x, y, 0.0]) for x, y in pts], color=c,
                                 stroke_width=2, fill_color=c, fill_opacity=0.9)
                         for pts, c in F_PARTS])
        base = [p.points.copy() for p in parts]
        tr = ValueTracker(0)
        state = {"A": np.asarray(M, float), "B": np.asarray(M, float)}

        def upd(_=None):
            t = tr.get_value()
            Mt = (1 - t) * state["A"] + t * state["B"]
            for p, b in zip(parts, base):
                pts = b.copy()
                pts[:, :2] = b[:, :2] @ Mt.T * U
                pts += self.c
                p.set_points(pts)

        for p in parts:
            p.add_updater(upd)
        upd()
        parts.set_z_index(3)
        self.f, self.tr, self.state = parts, tr, state
        # every stage must stay inside the frame
        return parts

    def move(self, M_to, run=2.2):
        self.state["B"] = np.asarray(M_to, float)
        self.tr.set_value(0)
        self.scene.play(self.tr.animate.set_value(1), run_time=run, rate_func=smooth)
        self.state["A"] = self.state["B"]
        self.tr.set_value(0)

    def outline(self, M):
        return Polygon(*[self.c + U * np.array([*(np.asarray(M) @ np.array([x, y])), 0])
                         for x, y in F_OUTLINE],
                       color=HIGHLIGHT, stroke_width=3, fill_opacity=0).set_z_index(5)


def fits(M):
    pts = np.array(F_OUTLINE) @ np.asarray(M).T
    assert np.abs(pts).max() < HALF - 0.1, (M, np.abs(pts).max())


def caption(i, M, name):
    """Matrix under panel i, then a short name under the matrix."""
    mat = matrix_tex(M, col_colors=(None, None), fmt="{:g}")
    mat.next_to([panel_x(i), CY - SIDE / 2, 0], DOWN, buff=0.16)
    word = Tex(name, font_size=MIN_FONT, color=INK_DIM)
    word.next_to(mat, DOWN, buff=0.12)
    assert mat.width < SIDE + GAP and word.width < SIDE + GAP, name
    assert word.get_bottom()[1] > -2.8125 + 0.1, name
    return mat, word


class ComposeF(Scene):
    """Right to left: scale x by 2.5, scale y by 0.6, reflect; the left panel does all three at once."""

    def construct(self):
        A1 = np.diag([2.5, 1.0])
        A2 = np.diag([1.0, 0.6])
        A3 = np.diag([-1.0, 1.0])
        C = A3 @ A2 @ A1
        assert np.allclose(C, np.diag([-2.5, 0.6]))
        for M in (A1, A2 @ A1, C):
            fits(M)

        P = [Panel(i, self) for i in range(4)]
        self.add(*[p.box for p in P])
        caps = [caption(0, C, "together"), caption(1, A3, "reflect"),
                caption(2, A2, "scale $y$"), caption(3, A1, "scale $x$")]
        self.wait(0.8)

        # right to left, each panel picks up where the previous one stopped
        steps = [(3, np.eye(2), A1), (2, A1, A2 @ A1), (1, A2 @ A1, C)]
        for i, start, end in steps:
            self.play(FadeIn(P[i].make_f(start)), FadeIn(caps[i][0]), FadeIn(caps[i][1]), run_time=0.6)
            self.wait(0.3)
            P[i].move(end)
            self.wait(0.6)

        self.play(FadeIn(P[0].make_f(np.eye(2))), FadeIn(caps[0][0]), FadeIn(caps[0][1]), run_time=0.6)
        self.wait(0.4)
        P[0].move(C, run=2.6)
        g0, g1 = P[0].outline(C), P[1].outline(C)
        self.play(Create(g0), Create(g1), run_time=1.0)
        self.wait(2.5)


class DecomposeF(Scene):
    """M in one go on the left; then the simple moves that build it: scale, reflect, shear."""

    def construct(self):
        A1 = np.diag([1.5, 1.2])
        A2 = np.diag([-1.0, 1.0])
        A3 = np.array([[1.0, 0.8], [0.0, 1.0]])
        M = A3 @ A2 @ A1
        assert np.allclose(M, [[-1.5, 0.96], [0.0, 1.2]])
        for X in (A1, A2 @ A1, M):
            fits(X)

        P = [Panel(i, self) for i in range(4)]
        self.add(*[p.box for p in P])
        cM = caption(0, M, "$M$")
        self.play(FadeIn(P[0].make_f(np.eye(2))), FadeIn(cM[0]), FadeIn(cM[1]), run_time=0.6)
        self.wait(0.4)
        P[0].move(M, run=2.6)

        names = {3: (A1, "$A_1$: scale"), 2: (A2, "$A_2$: reflect"), 1: (A3, "$A_3$: shear")}
        qs = {}
        for i in (1, 2, 3):
            q = MathTex("?", font_size=2 * MIN_FONT, color=INK_DIM).move_to(P[i].c)
            qs[i] = q
        self.play(*[FadeIn(q) for q in qs.values()], run_time=0.6)
        self.wait(1.5)

        steps = [(3, np.eye(2), A1), (2, A1, A2 @ A1), (1, A2 @ A1, M)]
        for i, start, end in steps:
            mat, word = caption(i, *names[i])
            self.play(FadeOut(qs[i]), FadeIn(P[i].make_f(start)), FadeIn(mat), FadeIn(word),
                      run_time=0.6)
            self.wait(0.3)
            P[i].move(end)
            self.wait(0.6)

        g0, g1 = P[0].outline(M), P[1].outline(M)
        self.play(Create(g0), Create(g1), run_time=1.0)
        self.wait(2.5)
