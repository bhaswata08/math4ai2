"""Block 2.4: diagonalization A = P D P^-1, shown the way Visual Kernel shows
the spectral decomposition S = Q Lambda Q^T.

Same sequence as the video (ch.2, 09:36-14:13): the statement with a label
under each factor, the factors in matrix form, P e_i = v_i, the numbers for
one matrix, then the matrix acting on a shape in one go and as three moves,
in 2D and in 3D. The difference from the spectral case is the point: P is
not a rotation, so the move onto the axes also stretches and shears.

2D: A = [[4, 1], [2, 3]], v1 = (1, 1) with 5, v2 = (-1, 2) with 2.
v2 is -1 times the (1, -2) of Act 3, so det P = 3 > 0 and no step flips
the plane (the same choice as making Q a rotation).
3D: P has columns (1,1,0), (0,1,1), (1,0,1), D = diag(3, -1, 2),
so A = (1/2) [[5, 1, -1], [4, 2, -4], [3, -3, 1]].

Visual layout after Visual Kernel, "SEE Matrix" ch.2 (spectral decomposition).
"""

from shared.anim.house import *
from shared.anim.linmap import *

V1_COLOR, V2_COLOR, V3_COLOR = V_COLOR, W_COLOR, RESULT_COLOR
LAM_COLOR = Y_COLOR

A2 = np.array([[4.0, 1.0], [2.0, 3.0]])
P2 = np.array([[1.0, -1.0], [1.0, 2.0]])
D2 = np.diag([5.0, 2.0])
P2i = np.linalg.inv(P2)
assert np.allclose(P2 @ D2 @ P2i, A2) and np.allclose(3 * P2i, [[2, 1], [-1, 1]])

P3 = np.array([[1.0, 0.0, 1.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]])
D3 = np.diag([3.0, -1.0, 2.0])
P3i = np.linalg.inv(P3)
A3 = P3 @ D3 @ P3i
assert np.linalg.det(P3) > 0 and not np.allclose(A3, A3.T)
assert np.allclose(2 * A3, [[5, 1, -1], [4, 2, -4], [3, -3, 1]])


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def words(s, color=INK, size=MIN_FONT):
    return Tex(s, font_size=size, color=color)


def blend_ok(F, n=50):
    """The straight-line path from I to F never squashes space flat."""
    k = F.shape[0]
    return all(np.linalg.det((1 - t) * np.eye(k) + t * F) > 1e-3 for t in np.linspace(0, 1, n))


def fmt(x):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:g}"


# ------------------------------------------------------------------ algebra


class DiagStatement(Scene):
    """A = P D P^-1 built right to left, labelled as invertible / diagonal / invertible, then as moves."""

    def construct(self):
        eq = MathTex("A", "=", "P", "D", "P^{-1}", font_size=96, color=INK).shift(UP * 1.4)
        self.add(eq[0])
        self.wait(0.8)
        self.play(FadeIn(eq[1]), run_time=0.5)
        for k in (4, 3, 2):
            self.play(FadeIn(eq[k], shift=0.15 * DOWN), run_time=0.6)
        self.wait(0.6)

        xs = [-3.3, 0.0, 3.3]
        facs = [eq[2], eq[3], eq[4]]
        lines = VGroup(*[Line(f.get_bottom() + 0.1 * DOWN, np.array([x, -0.15, 0]), color=INK_DIM, stroke_width=3)
                         for f, x in zip(facs, xs)])

        def lab(lines_, x, color=INK):
            g = VGroup(*[words(s, color) for s in lines_]).arrange(DOWN, buff=0.12)
            g.move_to(np.array([x, -0.35, 0]), aligned_edge=UP)
            return g

        names = VGroup(lab(["invertible"], xs[0]), lab(["diagonal"], xs[1]), lab(["invertible"], xs[2]))
        self.play(Create(lines), run_time=0.8)
        self.play(FadeIn(names), run_time=0.8)
        self.wait(2.2)

        moves = VGroup(lab(["axes", r"$\to$ eigenvectors"], xs[0], V1_COLOR),
                       lab(["stretch", "the axes"], xs[1], LAM_COLOR),
                       lab(["eigenvectors", r"$\to$ axes"], xs[2], V1_COLOR))
        self.play(ReplacementTransform(names, moves), run_time=1.0)
        self.wait(1.5)

        cmp = tex(r"S=Q\Lambda Q^T:\ \text{rotation, stretch, rotation}", INK_DIM)
        cmp.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cmp), run_time=0.8)
        self.wait(3)


def col_matrix(names, colors, rows=3):
    """[ | | ; v1 v2 ; | | ]: eigenvector columns drawn the way the video draws them."""
    mid = rows // 2
    data = [[(names[j] if i == mid else r"\vert") for j in range(len(names))] for i in range(rows)]
    m = Matrix(data, element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
               h_buff=1.0, v_buff=0.55, bracket_h_buff=0.15)
    m.get_brackets().set_color(INK)
    for j, col in enumerate(m.get_columns()):
        col.set_color(colors[j])
    return m


def diag_matrix(n):
    data = [[(rf"\lambda_{i + 1}" if i == j else "0") for j in range(n)] for i in range(n)]
    m = Matrix(data, element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
               h_buff=0.85 if n == 3 else 1.0, v_buff=0.55 if n == 3 else 0.75, bracket_h_buff=0.15)
    m.get_brackets().set_color(INK)
    for i in range(n):
        for j in range(n):
            m.get_entries()[i * n + j].set_color(LAM_COLOR if i == j else INK_FAINT)
    return m


def box_matrix(name, rows):
    data = [[r"\phantom{0}"] for _ in range(rows)]
    data[rows // 2] = [name]
    m = Matrix(data, element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
               v_buff=0.55 if rows == 3 else 0.75, bracket_h_buff=0.25)
    m.get_brackets().set_color(INK)
    return m


class DiagMatrixForm(Scene):
    """[A] = [v1 v2][lambda1 lambda2][P^-1], labelled; then the 3x3 version."""

    def construct(self):
        top = MathTex("A", "=", "P", "D", "P^{-1}", font_size=56, color=INK).to_edge(UP, buff=0.25)
        self.add(top)
        self.wait(0.6)

        def build(n):
            Am = box_matrix("A", n if n == 3 else 2)
            Pm = col_matrix([rf"\mathbf{{v}}_{i + 1}" for i in range(n)], [V1_COLOR, V2_COLOR, V3_COLOR][:n],
                            rows=3)
            Dm = diag_matrix(n)
            Pim = box_matrix("P^{-1}", n if n == 3 else 2)
            eqs = tex("=")
            row = VGroup(Am, eqs, Pm, Dm, Pim).arrange(RIGHT, buff=0.18 if n == 3 else 0.5).move_to(UP * 0.2)
            assert row.width < 9.6, row.width
            return row

        def labels(row, n):
            Am, _e, Pm, Dm, Pim = row
            specs = [(Am, [f"{n} by {n}"], INK_DIM), (Pm, ["eigenvectors", "of $A$"], V1_COLOR),
                     (Dm, ["eigenvalues,", "same order"], LAM_COLOR), (Pim, ["inverse", "of $P$"], INK_DIM)]
            out = VGroup()
            for mob, ls, c in specs:
                g = VGroup(*[words(s, c) for s in ls]).arrange(DOWN, buff=0.08)
                g.next_to(mob, DOWN, buff=0.22)
                out.add(g)
            return out

        r2 = build(2)
        Am, eqs, Pm, Dm, Pim = r2
        l2 = labels(r2, 2)
        self.add(Am, l2[0])
        self.wait(0.6)
        self.play(FadeIn(eqs), run_time=0.4)
        self.play(top[2].animate.set_color(HIGHLIGHT), FadeIn(Pm.get_brackets()), run_time=0.5)
        for col in Pm.get_columns():
            self.play(FadeIn(col, shift=0.2 * DOWN), run_time=0.6)
        self.play(FadeIn(l2[1]), top[2].animate.set_color(INK), run_time=0.6)
        self.wait(0.8)
        self.play(top[3].animate.set_color(HIGHLIGHT), FadeIn(Dm), run_time=0.8)
        self.play(FadeIn(l2[2]), top[3].animate.set_color(INK), run_time=0.6)
        self.wait(0.8)
        self.play(top[4].animate.set_color(HIGHLIGHT), FadeIn(Pim), run_time=0.8)
        self.play(FadeIn(l2[3]), top[4].animate.set_color(INK), run_time=0.6)
        self.wait(2.5)

        r3 = build(3)
        l3 = labels(r3, 3)
        self.play(FadeOut(r2), FadeOut(l2), run_time=0.7)
        self.play(FadeIn(r3), FadeIn(l3), run_time=1.0)
        self.wait(3)


class DiagPe(Scene):
    """P (1,0) = v1 and P (0,1) = v2, then the arrow diagram for P and for P^-1."""

    def construct(self):
        top = MathTex("A", "=", "P", "D", "P^{-1}", font_size=56, color=INK).to_edge(UP, buff=0.25)
        self.add(top)

        def Pmat():
            return matrix_tex(P2, col_colors=(V1_COLOR, V2_COLOR))

        def vec(v, color=INK):
            return matrix_tex([[fmt(x)] for x in v], col_colors=(color,))

        tagP = tex("P", INK).scale(1.2)
        frame = SurroundingRectangle(tagP, color=HIGHLIGHT, buff=0.12)
        tag = VGroup(tagP, frame).move_to([-4.2, 0.9, 0])

        rows = VGroup()
        for e, v, c, name in (((1, 0), (1, 1), V1_COLOR, r"=\mathbf{v}_1"), ((0, 1), (-1, 2), V2_COLOR, r"=\mathbf{v}_2")):
            Pm, em, eqm, vm, nm = Pmat(), vec(e), tex("="), vec(v, c), tex(name, c)
            rows.add(VGroup(Pm, em, eqm, vm, nm).arrange(RIGHT, buff=0.18))
        rows.arrange(DOWN, buff=0.35).move_to([0.4, -0.35, 0])
        assert rows.height < 4.4

        self.add(tag)
        self.wait(0.6)
        for r, j in zip(rows, (0, 1)):
            Pm, em, eqm, vm, nm = r
            self.play(FadeIn(Pm), FadeIn(em), run_time=0.7)
            box = SurroundingRectangle(Pm.get_columns()[j], color=HIGHLIGHT, buff=0.08)
            self.play(Create(box), run_time=0.5)
            self.play(FadeIn(eqm), TransformFromCopy(Pm.get_columns()[j], vm.get_entries()),
                      FadeIn(vm.get_brackets()), run_time=1.0)
            self.play(FadeIn(nm), FadeOut(box), run_time=0.6)
            self.wait(1.0)
        note = tex(r"\text{a matrix times }\mathbf{e}_i\text{ is its column } i", INK_DIM).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(rows), FadeOut(note), run_time=0.7)

        # arrow diagram: e_i -> v_i under P, then back under P^-1
        def icon(d, color):
            d = np.array([d[0], d[1], 0.0])
            d = d / np.linalg.norm(d) * 0.9
            return Arrow(-d / 2, d / 2, buff=0, color=color, stroke_width=7,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.2)

        def diagram(src, dst):
            g = VGroup()
            for y, (s, sc), (d, dc) in zip((0.75, -0.75), src, dst):
                a, b = icon(s, sc), icon(d, dc)
                a.move_to([-1.8, y, 0])
                b.move_to([1.8, y, 0])
                hop = CurvedArrow(np.array([-0.9, y + 0.05, 0]), np.array([0.9, y + 0.05, 0]),
                                  angle=-TAU / 5, color=INK, stroke_width=5, tip_length=0.2)
                g.add(VGroup(a, hop, b))
            return g

        fwd = diagram([((1, 0), X_COLOR), ((0, 1), Y_COLOR)], [((1, 1), V1_COLOR), ((-1, 2), V2_COLOR)])
        fwd.shift(DOWN * 0.3)
        names = VGroup(tex(r"\mathbf{e}_1", X_COLOR).next_to(fwd[0][0], LEFT, buff=0.3),
                       tex(r"\mathbf{v}_1", V1_COLOR).next_to(fwd[0][2], RIGHT, buff=0.3),
                       tex(r"\mathbf{e}_2", Y_COLOR).next_to(fwd[1][0], LEFT, buff=0.3),
                       tex(r"\mathbf{v}_2", V2_COLOR).next_to(fwd[1][2], RIGHT, buff=0.3))
        cap = tex(r"P\text{ sends }\mathbf{e}_i\text{ to the eigenvector }\mathbf{v}_i")
        cap.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(fwd), FadeIn(names), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(3)

        tagPi = tex("P^{-1}", INK).scale(1.2).move_to(tagP)
        frame2 = SurroundingRectangle(tagPi, color=HIGHLIGHT, buff=0.12)
        back = diagram([((1, 1), V1_COLOR), ((-1, 2), V2_COLOR)], [((1, 0), X_COLOR), ((0, 1), Y_COLOR)])
        back.shift(DOWN * 0.3)
        names2 = VGroup(tex(r"\mathbf{v}_1", V1_COLOR).next_to(back[0][0], LEFT, buff=0.3),
                        tex(r"\mathbf{e}_1", X_COLOR).next_to(back[0][2], RIGHT, buff=0.3),
                        tex(r"\mathbf{v}_2", V2_COLOR).next_to(back[1][0], LEFT, buff=0.3),
                        tex(r"\mathbf{e}_2", Y_COLOR).next_to(back[1][2], RIGHT, buff=0.3))
        cap2 = tex(r"P^{-1}\text{ sends }\mathbf{v}_i\text{ back to }\mathbf{e}_i").to_edge(DOWN, buff=0.25)
        self.play(ReplacementTransform(tagP, tagPi), ReplacementTransform(frame, frame2),
                  ReplacementTransform(fwd, back), ReplacementTransform(names, names2),
                  FadeOut(cap), FadeIn(cap2), run_time=1.2)
        self.wait(3.5)


class DiagNumeric(Scene):
    """[[4,1],[2,3]] = P D P^-1 in numbers, built like the video's numeric slide."""

    def construct(self):
        Am = matrix_tex(A2, col_colors=(None, None))
        eqm = tex("=")
        Pm = matrix_tex(P2, col_colors=(V1_COLOR, V2_COLOR))
        Dm = matrix_tex(D2, col_colors=(None, None))
        for k in (0, 3):
            Dm.get_entries()[k].set_color(LAM_COLOR)
        third = tex(r"\tfrac13")
        Pim = matrix_tex(3 * P2i, col_colors=(None, None))
        Pig = VGroup(third, Pim).arrange(RIGHT, buff=0.1)
        row = VGroup(Am, eqm, Pm, Dm, Pig).arrange(RIGHT, buff=0.2).move_to(UP * 0.3)
        assert row.width < 9.6
        labs = VGroup(*[tex(s, c).next_to(m, DOWN, buff=0.3) for s, c, m in
                        (("A", INK, Am), ("P", V1_COLOR, Pm), ("D", LAM_COLOR, Dm), ("P^{-1}", INK, Pim))])
        self.add(Am, labs[0])
        self.wait(0.8)
        self.play(FadeIn(eqm), run_time=0.4)
        for m, l in ((Pig, labs[3]), (Dm, labs[2]), (Pm, labs[1])):
            self.play(FadeIn(m), FadeIn(l), run_time=0.8)
            self.wait(0.4)
        notes = VGroup(tex(r"\text{columns of }P:\ \mathbf{v}_1=(1,1),\ \mathbf{v}_2=(-1,2)", INK_DIM),
                       tex(r"\text{diagonal of }D:\ \lambda_1=5,\ \lambda_2=2", INK_DIM)).arrange(DOWN, buff=0.15)
        notes.next_to(labs, DOWN, buff=0.45)
        self.play(FadeIn(notes), run_time=0.8)
        self.wait(4)


# ------------------------------------------------------------------ 2D pictures

U2 = 0.34
RECT = [(-1.5, -0.9), (0.0, -0.9), (0.0, 0.9), (-1.5, 0.9)], [(0.0, -0.9), (1.5, -0.9), (1.5, 0.9), (0.0, 0.9)]
L2 = 1.0   # eigen arrows are drawn as L2 * v
RECT_FILLS = ("#e9d36a", "#b9a64a")


def p3(v, U=U2):
    return np.array([v[0] * U, v[1] * U, 0.0])


class _World2D:
    """A shape, eigen arrows and span lines that follow T(t) = blend(t) @ M on a still grid."""

    def __init__(self, scene, arrows=True):
        self.state = {"M": np.eye(2), "F": np.eye(2)}
        self.tr = ValueTracker(0)
        self.parts = VGroup(*[Polygon(*[p3(p) for p in pts], color=c, stroke_width=2,
                                      fill_color=c, fill_opacity=0.85) for pts, c in zip(RECT, RECT_FILLS)])
        self.base = [m.points.copy() / U2 for m in self.parts]
        for m in self.parts:
            m.add_updater(lambda _m: self.apply())
        self.parts.set_z_index(3)
        self.extra = VGroup()
        if arrows:
            for v, c, name in (((1, 1), V1_COLOR, r"\mathbf{v}_1"), ((-1, 2), V2_COLOR, r"\mathbf{v}_2")):
                v = np.array(v, dtype=float)
                sp = always_redraw(self._span(v, c))
                ar = always_redraw(self._arrow(v, c))
                lb = always_redraw(self._label(v, c, name))
                sp.set_z_index(2)
                ar.set_z_index(5)
                lb.set_z_index(6)
                self.extra.add(sp, ar, lb)
        self.apply()

    def T(self):
        t = self.tr.get_value()
        return ((1 - t) * np.eye(2) + t * self.state["F"]) @ self.state["M"]

    def apply(self):
        Tm = self.T()
        for m, b in zip(self.parts, self.base):
            pts = b.copy()
            pts[:, :2] = b[:, :2] @ Tm.T * U2
            m.set_points(pts)

    def _span(self, v, c):
        def build():
            d = self.T() @ v
            d = d / max(np.linalg.norm(d), 1e-9)
            d3 = np.array([d[0], d[1], 0])
            return DashedLine(-2.6 * d3, 2.6 * d3, color=c, stroke_width=3, dash_length=0.12, stroke_opacity=0.8)
        return build

    def _arrow(self, v, c):
        def build():
            tip = self.T() @ (L2 * v)
            if np.linalg.norm(tip) * U2 < 0.06:
                return Dot(ORIGIN, radius=0.05, color=c)
            return Arrow(ORIGIN, p3(tip), buff=0, color=c, stroke_width=7,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.17)
        return build

    def _label(self, v, c, name):
        def build():
            tip = self.T() @ (L2 * v)
            d = tip / max(np.linalg.norm(tip), 1e-9)
            perp = np.array([-d[1], d[0]])
            w = tip * U2 + 0.38 * d + 0.38 * perp
            t = tex(name, c)
            label_box(t, opacity=0.9, buff=0.05)
            t.move_to([w[0], w[1], 0])
            return t
        return build

    def run(self, scene, F, run_time=3.0):
        assert blend_ok(F), F
        self.state["F"] = F
        scene.play(self.tr.animate.set_value(1), run_time=run_time, rate_func=smooth)
        self.state["M"] = F @ self.state["M"]
        self.state["F"] = np.eye(2)
        self.tr.set_value(0)


def _caption(s, colour=INK):
    t = tex(s, colour)
    t.to_corner(DL, buff=0.25)
    label_box(t, opacity=1.0)
    t.set_z_index(10)
    return t


def _check_fits():
    corners = np.array([p for pts in RECT for p in pts])
    for M in (np.eye(2), P2i, np.diag([5, 1]) @ P2i, D2 @ P2i, A2):
        ext = np.abs(corners @ M.T * U2).max(axis=0)
        assert ext[0] < 4.6 and ext[1] < 2.45, (M, ext)


_check_fits()


class Diag2DFull(Scene):
    """A moves the rectangle in one go."""

    def construct(self):
        plane = lin_plane(U2)
        w = _World2D(self, arrows=False)
        eq = tex(r"A=\begin{bmatrix}4&1\\2&3\end{bmatrix}").to_corner(UL, buff=0.25)
        label_box(eq, opacity=1.0)
        eq.set_z_index(10)
        self.add(plane, w.parts, eq)
        self.wait(1.5)
        w.run(self, A2, run_time=3.5)
        self.wait(3)


class Diag2DSteps(Scene):
    """P^-1 puts the eigenvectors on the axes, D scales x by 5 then y by 2, P puts them back."""

    def construct(self):
        plane = lin_plane(U2)
        w = _World2D(self)
        eq = MathTex("A", "=", "P", "D", "P^{-1}", font_size=MIN_FONT, color=INK).to_corner(UL, buff=0.25)
        fA, fP, fD, fPi = eq[0], eq[2], eq[3], eq[4]
        label_box(eq, opacity=0.95)
        eq.set_z_index(10)
        cur = _caption(r"\lambda_1=5,\ \lambda_2=2")
        self.add(plane, w.parts, w.extra, eq, cur)
        self.wait(2)

        def step(part, F, text, run=3.0, hold=1.3):
            nonlocal cur
            self.play(part.animate.set_color(HIGHLIGHT), run_time=0.4)
            new = _caption(text)
            self.remove(cur)
            self.add(new)
            cur = new
            w.run(self, F, run)
            self.play(part.animate.set_color(INK), run_time=0.3)
            self.wait(hold)

        step(fPi, P2i, r"P^{-1}:\ \text{eigenvectors}\to\text{axes}")
        step(fD, np.diag([5.0, 1.0]), r"D:\ \text{scale }x\text{ by }5", run=2.5, hold=0.6)
        step(fD, np.diag([1.0, 2.0]), r"D:\ \text{scale }y\text{ by }2", run=2.0, hold=0.6)
        step(fP, P2, r"P:\ \text{axes}\to\text{eigenvectors}")
        assert np.allclose(w.state["M"], A2)

        ghost = VGroup(*[Polygon(*[p3(A2 @ np.array(p)) for p in pts], color=HIGHLIGHT, stroke_width=5,
                                 fill_opacity=0) for pts in RECT])
        ghost.set_z_index(7)
        new = _caption(r"A\text{ in one go (gold): the same shape}", HIGHLIGHT)
        self.remove(cur)
        self.add(new)
        self.play(Create(ghost), fA.animate.set_color(HIGHLIGHT), run_time=1.5)
        self.wait(3)


class DiagPGrid(Scene):
    """P carries the grid and e1, e2 onto v1, v2. Lengths and the right angle both change."""

    def construct(self):
        U = 0.6
        ghost = ghost_plane(U, opacity=0.35)
        plane = lin_plane(U)
        e1 = Arrow(ORIGIN, [U, 0, 0], buff=0, color=X_COLOR, stroke_width=7,
                   max_tip_length_to_length_ratio=0.3, tip_length=0.18)
        e2 = Arrow(ORIGIN, [0, U, 0], buff=0, color=Y_COLOR, stroke_width=7,
                   max_tip_length_to_length_ratio=0.3, tip_length=0.18)
        lines = VGroup(*[DashedLine(-2.5 * d / np.linalg.norm(d), 2.5 * d / np.linalg.norm(d), color=c,
                                    stroke_width=3, dash_length=0.12)
                         for d, c in ((np.array([1, 1, 0.0]), V1_COLOR), (np.array([-1, 2, 0.0]), V2_COLOR))])
        lab1 = label_box(tex(r"\mathbf{e}_1", X_COLOR), buff=0.05).move_to([U + 0.3, -0.3, 0])
        lab2 = label_box(tex(r"\mathbf{e}_2", Y_COLOR), buff=0.05).move_to([-0.35, U + 0.2, 0])
        cap = _caption(r"\text{the grid before }P")
        eq = MathTex("P", "=", r"\begin{bmatrix}1&-1\\1&2\end{bmatrix}", font_size=MIN_FONT,
                     color=INK).to_corner(UL, buff=0.25)
        fP = eq[0]
        label_box(eq, opacity=0.95)
        eq.set_z_index(10)
        for m in (e1, e2):
            m.set_z_index(5)
        self.add(ghost, plane, lines, e1, e2, lab1, lab2, eq, cap)
        self.wait(2)

        M = m2(*P2.flatten())
        assert blend_ok(P2)
        v1 = Arrow(ORIGIN, p3((1, 1), U), buff=0, color=V1_COLOR, stroke_width=7,
                   max_tip_length_to_length_ratio=0.3, tip_length=0.18)
        v2 = Arrow(ORIGIN, p3((-1, 2), U), buff=0, color=V2_COLOR, stroke_width=7,
                   max_tip_length_to_length_ratio=0.3, tip_length=0.18)
        nl1 = label_box(tex(r"\mathbf{v}_1", V1_COLOR), buff=0.05).move_to(p3((1, 1), U) + np.array([0.45, -0.1, 0]))
        nl2 = label_box(tex(r"\mathbf{v}_2", V2_COLOR), buff=0.05).move_to(p3((-1, 2), U) + np.array([-0.45, 0.0, 0]))
        new = _caption(r"P:\ \mathbf{e}_1\to\mathbf{v}_1,\ \ \mathbf{e}_2\to\mathbf{v}_2")
        self.play(fP.animate.set_color(HIGHLIGHT), FadeOut(cap), FadeIn(new), run_time=0.5)
        cap = new
        self.play(ApplyMatrix(M, plane), ReplacementTransform(e1, v1), ReplacementTransform(e2, v2),
                  ReplacementTransform(lab1, nl1), ReplacementTransform(lab2, nl2), run_time=3.5)
        self.play(fP.animate.set_color(INK), run_time=0.3)
        self.wait(1.5)
        new = _caption(r"\text{not a rotation: lengths and the right angle change}")
        self.play(FadeOut(cap), FadeIn(new), run_time=0.6)
        self.wait(3.5)


# ------------------------------------------------------------------ 3D pictures

U3 = 0.85
CUBE_COLORS = (V_COLOR, W_COLOR, RESULT_COLOR, X_COLOR, Y_COLOR, HIGHLIGHT)


def cube_faces():
    h = 0.5
    c = [np.array([x, y, z]) for x in (-h, h) for y in (-h, h) for z in (-h, h)]
    idx = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
    return [[c[i] for i in f] for f in idx]


def matrix_tex3(M):
    rows = [[fmt(x) for x in r] for r in M]
    m = Matrix(rows, element_to_mobject=lambda e: MathTex(e, font_size=MIN_FONT, color=INK),
               h_buff=0.95, v_buff=0.6, bracket_h_buff=0.12)
    m.get_brackets().set_color(INK)
    return m


class _World3D:
    def __init__(self, arrows=True):
        self.state = {"M": np.eye(3), "F": np.eye(3)}
        self.tr = ValueTracker(0)
        self.faces = VGroup()
        self.base = []
        for f, c in zip(cube_faces(), CUBE_COLORS):
            poly = Polygon(*[p * U3 for p in f], color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.55)
            self.faces.add(poly)
            self.base.append(poly.points.copy() / U3)
        for m in self.faces:
            m.add_updater(lambda _m: self.apply())
        self.arrows = VGroup()
        if arrows:
            for j, c in enumerate((V1_COLOR, V2_COLOR, V3_COLOR)):
                v = P3[:, j] * 1.0
                line = Line(ORIGIN, v * U3, color=c, stroke_width=8)
                tip = Dot3D(v * U3, radius=0.07, color=c)
                line.add_updater(self._line_up(v))
                tip.add_updater(self._tip_up(v))
                self.arrows.add(line, tip)
        self.apply()

    def T(self):
        t = self.tr.get_value()
        return ((1 - t) * np.eye(3) + t * self.state["F"]) @ self.state["M"]

    def apply(self):
        Tm = self.T()
        for m, b in zip(self.faces, self.base):
            m.set_points(b @ Tm.T * U3)

    def _line_up(self, v):
        def up(m):
            end = self.T() @ v * U3
            if np.linalg.norm(end) < 1e-3:
                end = end + np.array([1e-3, 0, 0])
            m.put_start_and_end_on(ORIGIN, end)
        return up

    def _tip_up(self, v):
        def up(m):
            m.move_to(self.T() @ v * U3)
        return up

    def run(self, scene, F, run_time=3.0, check=True):
        # a diagonal step may pass through zero on purpose (a negative eigenvalue flips)
        assert not check or blend_ok(F) or np.allclose(F, np.diag(np.diag(F))), F
        self.state["F"] = F
        scene.play(self.tr.animate.set_value(1), run_time=run_time, rate_func=smooth)
        self.state["M"] = F @ self.state["M"]
        self.state["F"] = np.eye(3)
        self.tr.set_value(0)


def _axes3():
    ax = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-3, 3, 1],
                    x_length=8 * U3, y_length=8 * U3, z_length=6 * U3,
                    axis_config={"stroke_color": INK_FAINT, "stroke_width": 2, "include_ticks": False,
                                 "include_tip": False})
    return ax


def _check_fits3():
    pts = np.array([p for f in cube_faces() for p in f])
    for M in (np.eye(3), P3i, D3 @ P3i, A3):
        assert np.abs(pts @ M.T * U3).max() < 2.4, M


_check_fits3()


class Diag3DFull(ThreeDScene):
    """A 3x3 non-symmetric A deforms the cube in one go."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        ax = _axes3()
        w = _World3D(arrows=False)
        eqA = VGroup(tex(r"A=\tfrac12"), matrix_tex3(2 * A3)).arrange(RIGHT, buff=0.15)
        eqA.scale(1.0).to_corner(UL, buff=0.2)
        label_box(eqA, opacity=0.95)
        self.add_fixed_in_frame_mobjects(eqA)
        self.add(ax, w.faces)
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(1.5)
        w.run(self, A3, run_time=4.0, check=False)  # det A < 0: the cube passes through flat
        self.wait(4)


class Diag3DSteps(ThreeDScene):
    """P^-1 puts v1, v2, v3 on the axes, D scales x, y (flips), z one at a time, P puts them back."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        ax = _axes3()
        w = _World3D()
        eq = MathTex("A", "=", "P", "D", "P^{-1}", font_size=MIN_FONT, color=INK).to_corner(UL, buff=0.25)
        fA, fP, fD, fPi = eq[0], eq[2], eq[3], eq[4]
        label_box(eq, opacity=0.95)
        self.add_fixed_in_frame_mobjects(eq)
        state = {"cap": None}

        def caption(s, colour=INK):
            t = tex(s, colour).to_corner(DL, buff=0.25)
            label_box(t, opacity=1.0)
            if state["cap"] is not None:
                self.remove(state["cap"])
            self.add_fixed_in_frame_mobjects(t)
            state["cap"] = t

        caption(r"\mathbf{v}_1,\mathbf{v}_2,\mathbf{v}_3:\ \text{teal, violet, amber}")
        self.add(ax, w.faces, w.arrows)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(2.5)

        lam = np.diag(D3)

        def step(part, F, text, run=3.0, hold=1.2):
            part.set_color(HIGHLIGHT)
            caption(text)
            w.run(self, F, run)
            part.set_color(INK)
            self.wait(hold)

        step(fPi, P3i, r"P^{-1}:\ \text{eigenvectors}\to\text{axes}")
        for k, axis in enumerate("xyz"):
            F = np.eye(3)
            F[k, k] = lam[k]
            step(fD, F, rf"D:\ \text{{scale }}{axis}\text{{ by }}{fmt(lam[k])}", run=2.5, hold=0.6)
        step(fP, P3, r"P:\ \text{axes}\to\text{eigenvectors}")
        assert np.allclose(w.state["M"], A3)

        h = 0.5
        corners = [np.array([x, y, z]) for x in (-h, h) for y in (-h, h) for z in (-h, h)]
        edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if np.sum(np.abs(corners[a] - corners[b])) == 1]
        ghost = VGroup(*[Line(A3 @ corners[a] * U3, A3 @ corners[b] * U3, color=HIGHLIGHT, stroke_width=4)
                         for a, b in edges])
        caption(r"A\text{ in one go (gold): the same box}", HIGHLIGHT)
        fA.set_color(HIGHLIGHT)
        self.play(Create(ghost), run_time=1.5)
        self.wait(3.5)
