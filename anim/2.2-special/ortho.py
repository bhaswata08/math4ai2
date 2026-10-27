"""Block 2.3: an orthogonal matrix. Q^T Q = I read as dot products, and Q^T undoes Q."""

from shared.anim.house import *
from shared.anim.linmap import *

U = 1.2                      # scene units per grid unit
CENTRE = np.array([-2.5, 0.0, 0.0])
RIGHT_X = 2.45               # centre of the right-hand panel


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def rot(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def arrow_to(p, color):
    return Arrow(CENTRE, CENTRE + np.array([p[0] * U, p[1] * U, 0]), buff=0, color=color, stroke_width=7,
                 max_tip_length_to_length_ratio=0.25, tip_length=0.2)


def dot_matrix(entries, colors):
    """A 2x2 bracketed grid whose entries are given as lists of TeX parts."""
    cells = []
    for i in range(2):
        for j in range(2):
            parts = entries[i][j]
            m = MathTex(*parts, font_size=MIN_FONT, color=INK)
            for k, c in enumerate(colors[i][j]):
                m[k].set_color(c)
            cells.append(m)
    xs = [-0.95, 0.95]
    ys = [0.5, -0.5]
    for n, c in enumerate(cells):
        c.move_to([xs[n % 2], ys[n // 2], 0])
    br = VGroup(MathTex(r"\Bigg[", font_size=MIN_FONT * 1.5, color=INK).move_to([-1.85, 0, 0]),
                MathTex(r"\Bigg]", font_size=MIN_FONT * 1.5, color=INK).move_to([1.85, 0, 0]))
    return cells, br


class OrthoColumnsTranspose(Scene):
    """Q^T Q = I: entry (i,j) is column i dot column j; then Q^T undoes the turn."""

    def construct(self):
        # Q = (sqrt2/2) [[1, 1], [-1, 1]] is the rotation by -45 degrees (clockwise).
        s = np.sqrt(2) / 2
        Q = s * np.array([[1.0, 1.0], [-1.0, 1.0]])
        assert np.allclose(Q, rot(-np.pi / 4))
        q1, q2 = Q[:, 0], Q[:, 1]
        gram = Q.T @ Q
        assert np.allclose(gram, np.eye(2))

        plane = house_plane(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=4 * U, y_length=4 * U)
        plane.move_to(CENTRE)

        th = ValueTracker(0.0)

        def corners():
            R = rot(th.get_value())
            return [R @ np.array(c) for c in [(0, 0), (1, 0), (1, 1), (0, 1)]]

        def square():
            pts = [CENTRE + np.array([p[0] * U, p[1] * U, 0]) for p in corners()]
            return Polygon(*pts, color=INK_DIM, stroke_width=3, fill_color=INK_DIM, fill_opacity=0.18)

        def blend(a, b):
            return interpolate_color(ManimColor(a), ManimColor(b), min(abs(th.get_value()) / (np.pi / 4), 1))

        def arrows():
            R = rot(th.get_value())
            return VGroup(arrow_to(R[:, 0], blend(X_COLOR, V_COLOR)), arrow_to(R[:, 1], blend(Y_COLOR, W_COLOR)))

        sq = always_redraw(square)
        arr = always_redraw(arrows)

        # Right panel. Q as factor times a plain matrix; its columns are coloured.
        def q_matrix(M, name):
            fac = tex(r"\tfrac{\sqrt2}{2}")
            mat = matrix_tex([[f"{int(round(M[0, 0] / s))}", f"{int(round(M[0, 1] / s))}"],
                              [f"{int(round(M[1, 0] / s))}", f"{int(round(M[1, 1] / s))}"]],
                             col_colors=(V_COLOR, W_COLOR)) if name == "Q" else \
                matrix_tex([[f"{int(round(M[0, 0] / s))}", f"{int(round(M[0, 1] / s))}"],
                            [f"{int(round(M[1, 0] / s))}", f"{int(round(M[1, 1] / s))}"]],
                           col_colors=(None, None))
            nm = tex(name + "=")
            g = VGroup(nm, fac, mat).arrange(RIGHT, buff=0.15)
            g.move_to([RIGHT_X, 2.0, 0])
            return g

        QM = q_matrix(Q, "Q")
        QTM = q_matrix(Q.T, r"Q^{T}")

        self.add(plane, sq, arr, QM)
        self.wait(1.0)

        # 1. apply Q
        self.play(th.animate.set_value(-np.pi / 4), run_time=2.5)

        l1 = tex(r"\mathbf{q}_1", V_COLOR)
        l2 = tex(r"\mathbf{q}_2", W_COLOR)
        l1.move_to(CENTRE + np.array([q1[0] * U + 0.05, q1[1] * U - 0.4, 0]))
        l2.move_to(CENTRE + np.array([q2[0] * U + 0.05, q2[1] * U + 0.4, 0]))
        for l in (l1, l2):
            label_box(l)
        n1 = tex(r"|\mathbf{q}_1|=" + f"{np.linalg.norm(q1):g}", RESULT_COLOR)
        n2 = tex(r"|\mathbf{q}_2|=" + f"{np.linalg.norm(q2):g}", RESULT_COLOR)
        n1.move_to([RIGHT_X, 0.6, 0])
        n2.move_to([RIGHT_X, -0.1, 0])
        right = RightAngle(Line(CENTRE, CENTRE + np.array([q1[0], q1[1], 0])),
                           Line(CENTRE, CENTRE + np.array([q2[0], q2[1], 0])),
                           length=0.3, color=HIGHLIGHT, quadrant=(1, 1), stroke_width=5)
        ang = tex(r"90^{\circ}", HIGHLIGHT)
        ang.move_to(CENTRE + np.array([U * 0.95, 0, 0]))
        label_box(ang)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.8)
        self.play(Create(right), FadeIn(ang), run_time=1)
        self.wait(1.2)
        self.play(FadeIn(n1), run_time=0.7)
        self.play(FadeIn(n2), run_time=0.7)
        self.wait(1.0)

        # 2. Q^T Q as a grid of dot products
        self.play(FadeOut(n1), FadeOut(n2), run_time=0.5)
        title = tex(r"Q^{T}Q", INK).move_to([RIGHT_X, 0.75, 0])
        names = [[("q_1", r"\!\cdot\!", "q_1"), ("q_1", r"\!\cdot\!", "q_2")],
                 [("q_2", r"\!\cdot\!", "q_1"), ("q_2", r"\!\cdot\!", "q_2")]]
        cols = [[(V_COLOR, INK, V_COLOR), (V_COLOR, INK, W_COLOR)],
                [(W_COLOR, INK, V_COLOR), (W_COLOR, INK, W_COLOR)]]
        cells, br = dot_matrix(names, cols)
        grid = VGroup(*cells, br)
        grid.scale(0.97).move_to([RIGHT_X, -0.7, 0])
        self.play(FadeIn(title), FadeIn(grid), run_time=0.9)
        self.wait(1)

        qs = [q1, q2]
        arrows_now = arr
        filled = []
        for n, cell in enumerate(cells):
            i, j = n // 2, n % 2
            val = float(qs[i] @ qs[j])
            assert abs(val - gram[i, j]) < 1e-9
            num = tex(f"{val + 0.0:.0f}", RESULT_COLOR)
            num.move_to(cell)
            ring = SurroundingRectangle(cell, color=HIGHLIGHT, buff=0.1, stroke_width=4)
            hl = [arrows_now[0]] if i == j == 0 else [arrows_now[1]] if i == j == 1 else [arrows_now[0], arrows_now[1]]
            self.play(Create(ring), *[Indicate(h, color=HIGHLIGHT, scale_factor=1.15) for h in hl], run_time=0.9)
            self.play(FadeOut(cell), FadeOut(ring), run_time=0.3)
            self.play(FadeIn(num), run_time=0.4)
            filled.append(num)
            self.wait(0.2)

        eq_title = tex(r"Q^{T}Q=I", INK).move_to([RIGHT_X, 0.75, 0])
        self.play(FadeOut(title), run_time=0.3)
        self.play(FadeIn(eq_title), run_time=0.5)
        self.wait(1.6)

        # 3. Q^T undoes Q
        self.play(FadeOut(eq_title), FadeOut(br), *[FadeOut(f) for f in filled],
                  FadeOut(l1), FadeOut(l2), FadeOut(right), FadeOut(ang), run_time=0.8)
        self.play(FadeOut(QM), run_time=0.3)
        self.play(FadeIn(QTM), run_time=0.5)
        inv = tex(r"Q^{-1}=Q^{T}", RESULT_COLOR).move_to([RIGHT_X, 0.3, 0])
        self.wait(0.2)
        self.play(th.animate.set_value(0.0), run_time=3)
        self.play(FadeIn(inv), run_time=0.8)
        self.wait(1.2)
        fin = tex(r"Q^{T}Q=I", INK).move_to([RIGHT_X, -1.0, 0])
        self.play(FadeIn(fin), run_time=0.8)
        self.wait(1.6)
