"""Block 2.3: projection onto a unit vector. P = u u^T, P^2 = P, many inputs share one output."""

from shared.anim.house import *
from shared.anim.linmap import *

U = 1.1
ORG = np.array([-3.8, -1.15, 0.0])   # scene position of the plane origin
PX = 2.45                             # centre of the right-hand panel


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def P2S(p):
    return ORG + np.array([p[0] * U, p[1] * U, 0.0])


def arrow(p, color, w=7):
    return Arrow(ORG, P2S(p), buff=0, color=color, stroke_width=w,
                 max_tip_length_to_length_ratio=0.25, tip_length=0.2)


class ProjectionBuild(Scene):
    def construct(self):
        u = np.array([1.0, 2.0]) / np.sqrt(5)
        x1 = np.array([2.0, 1.0])
        P = np.outer(u, u)
        p = P @ x1
        d = np.array([2.0, -1.0])               # direction of the fibre (perpendicular to u)
        assert abs(u @ d) < 1e-12
        s_ = (x1 - p)[0] / d[0]
        x2 = p + 1.0 * d
        x3 = p - s_ * d                         # mirror of x1 across p
        assert np.allclose(P @ x2, p) and np.allclose(P @ x3, p)
        assert np.allclose(P @ P, P)
        dot = float(u @ x1)

        plane = house_plane(x_range=[-1, 3, 1], y_range=[-1, 3, 1], x_length=4 * U, y_length=4 * U)
        plane.move_to(ORG + np.array([1.0 * U, 1.0 * U, 0]))
        line = Line(P2S(np.array([-0.5, -1.0])), P2S(np.array([1.5, 3.0])), color=INK_DIM, stroke_width=4)

        au = arrow(u, V_COLOR)
        ax1 = arrow(x1, W_COLOR)
        lu = tex(r"\mathbf{u}", V_COLOR).move_to(P2S(u) + np.array([-0.35, 0.1, 0]))
        lx = tex(r"\mathbf{x}", W_COLOR).move_to(P2S(x1) + np.array([0.3, 0.2, 0]))
        for l in (lu, lx):
            label_box(l)

        def panel_defs():
            g = VGroup(
                tex(r"\mathbf{u}=\tfrac{1}{\sqrt5}\begin{bmatrix}1\\2\end{bmatrix}", V_COLOR),
                tex(r"\mathbf{x}=\begin{bmatrix}2\\1\end{bmatrix}", W_COLOR),
            ).arrange(DOWN, buff=0.5)
            return g.move_to([PX, 0.9, 0])

        defs = panel_defs()
        self.add(plane, line, au, ax1, lu, lx, defs)
        self.wait(1.05)

        # 1. the drop and the foot
        foot = P2S(p)
        drop = DashedLine(P2S(x1), foot, color=HIGHLIGHT, stroke_width=5, dash_length=0.12)
        ra = RightAngle(Line(foot, P2S(x1)), Line(foot, P2S(u * 2)), length=0.22, color=HIGHLIGHT, stroke_width=4)
        ap = arrow(p, RESULT_COLOR, 8)
        lp = tex(r"\mathbf{p}", RESULT_COLOR).move_to(foot + np.array([0.35, -0.3, 0]))
        label_box(lp)
        self.play(Create(drop), run_time=1.2)
        self.play(Create(ra), run_time=0.5)
        self.play(GrowArrow(ap), FadeIn(lp), run_time=1.2)
        self.wait(0.7)

        # 2. the numbers
        n1 = tex(r"\mathbf{u}\cdot\mathbf{x}=" + f"{dot:.2f}", INK)
        n2 = tex(r"\mathbf{p}=(\mathbf{u}\cdot\mathbf{x})\,\mathbf{u}", RESULT_COLOR)
        n3 = tex(r"\mathbf{p}=\begin{bmatrix}" + f"{p[0]:.1f}" + r"\\" + f"{p[1]:.1f}" + r"\end{bmatrix}", RESULT_COLOR)
        g = VGroup(n1, n2, n3).arrange(DOWN, buff=0.4).move_to([PX, 0.4, 0])
        self.play(FadeOut(defs), run_time=0.4)
        self.play(FadeIn(n1), run_time=0.8)
        self.wait(0.56)
        self.play(FadeIn(n2), FadeIn(n3), run_time=0.8)
        self.wait(1.05)

        # 3. regroup: p = u (u^T x) = (u u^T) x, and build the matrix
        self.play(FadeOut(g), run_time=0.4)
        a1 = tex(r"\mathbf{p}=\mathbf{u}\,(\mathbf{u}^{T}\mathbf{x})", RESULT_COLOR).move_to([PX, 1.6, 0])
        a2 = tex(r"\;=(\mathbf{u}\mathbf{u}^{T})\,\mathbf{x}", RESULT_COLOR).move_to([PX + 0.15, 0.85, 0])
        self.play(FadeIn(a1), run_time=0.6)
        self.play(FadeIn(a2), run_time=0.6)
        self.wait(1.05)
        self.play(FadeOut(a1), FadeOut(a2), run_time=0.4)

        ttl = tex(r"P=\mathbf{u}\mathbf{u}^{T}", V_COLOR).move_to([PX, 1.75, 0])
        names = [[r"u_1u_1", r"u_1u_2"], [r"u_2u_1", r"u_2u_2"]]
        cells = VGroup()
        pos = [[(-0.95, 0.45), (0.95, 0.45)], [(-0.95, -0.45), (0.95, -0.45)]]
        for i in range(2):
            for j in range(2):
                cells.add(tex(names[i][j], V_COLOR).move_to([PX + pos[i][j][0], 0.5 + pos[i][j][1], 0]))
        brs = VGroup(MathTex(r"\Bigg[", font_size=MIN_FONT * 1.5, color=INK).move_to([PX - 1.85, 0.5, 0]),
                     MathTex(r"\Bigg]", font_size=MIN_FONT * 1.5, color=INK).move_to([PX + 1.85, 0.5, 0]))
        self.play(FadeIn(ttl), FadeIn(cells), FadeIn(brs), run_time=1)
        self.wait(0.7)
        nums = VGroup()
        for n in range(4):
            i, j = n // 2, n % 2
            val = P[i, j]
            num = tex(f"{val:.1f}", RESULT_COLOR).move_to(cells[n])
            self.play(FadeOut(cells[n]), FadeIn(num), run_time=0.4)
            nums.add(num)
            self.wait(0.35)
        self.wait(0.7)

        # 4. apply P: x slides to p. Apply again: p stays.
        self.play(FadeOut(ttl), run_time=0.3)
        pm_lab = tex(r"P=", RESULT_COLOR).move_to([PX - 2.55, 0.5, 0])
        self.play(FadeIn(pm_lab), run_time=0.3)
        self.wait(0.3)
        self.play(FadeOut(drop), FadeOut(ra), FadeOut(ap), FadeOut(lx), run_time=0.4)
        self.play(Transform(ax1, arrow(p, RESULT_COLOR, 8)), run_time=1.8)
        self.wait(0.56)
        t1 = tex(r"P\mathbf{x}=\mathbf{p}", RESULT_COLOR).move_to([PX, -0.75, 0])
        self.play(FadeIn(t1), run_time=0.6)
        self.play(Indicate(ax1, color=HIGHLIGHT, scale_factor=1.0), run_time=1)
        t2 = tex(r"P\mathbf{p}=\mathbf{p}\quad(P^{2}=P)", RESULT_COLOR).move_to([PX, -1.65, 0])
        self.play(FadeIn(t2), run_time=0.8)
        self.wait(0.84)

        # 5. many inputs, one output
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(lp), run_time=0.4)
        fibre = DashedLine(P2S(p - 0.8 * d), P2S(p + 1.2 * d), color=HIGHLIGHT, stroke_width=5, dash_length=0.14)
        fibre.set_z_index(1)
        b2, b3, b1 = arrow(x2, W_COLOR), arrow(x3, W_COLOR), arrow(x1, W_COLOR)
        l2 = tex(r"\mathbf{x}_2", W_COLOR).move_to(P2S(x2) + np.array([0.45, 0.1, 0]))
        l3 = tex(r"\mathbf{x}_3", W_COLOR).move_to(P2S(x3) + np.array([-0.45, 0.2, 0]))
        l1 = tex(r"\mathbf{x}_1", W_COLOR).move_to(P2S(x1) + np.array([0.45, 0.25, 0]))
        for l in (l1, l2, l3):
            label_box(l)
        self.play(Create(fibre), run_time=1.2)
        self.play(FadeOut(ax1), run_time=0.01)
        self.play(*[GrowArrow(a) for a in (b1, b2, b3)], FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=1.5)
        self.wait(0.84)
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(l3), run_time=0.3)
        ap2 = arrow(p, RESULT_COLOR, 8)
        self.play(Transform(b1, arrow(p, RESULT_COLOR, 8)), Transform(b2, arrow(p, RESULT_COLOR, 8)),
                  Transform(b3, arrow(p, RESULT_COLOR, 8)), run_time=2.2)
        self.wait(0.42)
        t3 = tex(r"P\mathbf{x}_1=P\mathbf{x}_2=P\mathbf{x}_3", RESULT_COLOR, 40).move_to([PX, -0.85, 0])
        t4 = tex(r"\det P=0:\ \text{no way back}", INK).move_to([PX, -1.8, 0])
        self.play(FadeIn(t3), run_time=0.8)
        self.play(FadeIn(t4), run_time=0.8)
        self.wait(1.4)
