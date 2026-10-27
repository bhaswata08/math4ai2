"""Block 3.2: rotate the basis; C_hat = P^T C P is diagonal exactly at the eigenvectors of C."""

from pathlib import Path

from shared.anim.house import *

X = np.loadtxt(Path(__file__).parent / "data" / "cloud2d.csv", delimiter=",", comments="#")
M = len(X)
C = X.T @ X / M
assert np.allclose(C, [[3.25, 1.5], [1.5, 1.0]], atol=1e-6)
W, V = np.linalg.eigh(C)                     # ascending
v1 = V[:, 1] * np.sign(V[0, 1])
TH_EIG = float(np.arctan2(v1[1], v1[0]))
assert np.isclose(TH_EIG, np.arctan2(1, 2)) and np.allclose(W[::-1], [4, 0.25])

SC = 0.65
ORG = np.array([-1.8, 0.1, 0])
XR, YR = (-4.7, 3.7), (-3.2, 3.2)
L = 2.8


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def P(x, y):
    return ORG + np.array([x * SC, y * SC, 0])


def Pmat(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def Chat(t):
    Pm = Pmat(t)
    return Pm.T @ C @ Pm


def clean(v):
    return float(v) + 0.0 if abs(v) > 5e-3 else 0.0


class Decorrelate(Scene):
    def construct(self):
        plane = house_plane(x_range=[XR[0], XR[1], 1], y_range=[YR[0], YR[1], 1],
                            x_length=(XR[1] - XR[0]) * SC, y_length=(YR[1] - YR[0]) * SC)
        plane.move_to(P((XR[0] + XR[1]) / 2, (YR[0] + YR[1]) / 2))
        for l in list(plane.background_lines) + list(plane.faded_lines):
            l.set_stroke(opacity=0.35)
        dots = VGroup(*[Dot(P(x, y), radius=0.065, color=V_COLOR) for x, y in X])
        xl = tex("x_1", INK_DIM).move_to(P(3.3, 0.85))
        yl = tex("x_2", INK_DIM).move_to(P(1.2, 2.9))

        th = ValueTracker(0.0)

        def basis():
            t = th.get_value()
            out = VGroup()
            for k, col in enumerate((RESULT_COLOR, W_COLOR)):
                d = Pmat(t)[:, k]
                ext = Line(P(-L * d[0], -L * d[1]), P(L * d[0], L * d[1]), color=col, stroke_width=3,
                           stroke_opacity=0.35)
                arr = Arrow(P(0, 0), P(L * d[0], L * d[1]), buff=0, color=col, stroke_width=7,
                            tip_length=0.2, max_tip_length_to_length_ratio=0.3)
                lab = tex(r"\mathbf p_%d" % (k + 1), col)
                o = -Pmat(t)[:, 1 - k] * (0.8 if k == 0 else 0.9)
                lab.move_to(P((L + 0.5) * d[0] + o[0], (L + 0.5) * d[1] + o[1]))
                out.add(ext, arr, VGroup(BackgroundRectangle(lab, color=BG, fill_opacity=0.9, buff=0.04), lab))
            return out

        bas = always_redraw(basis)

        # right panel: the live matrix
        RX = 3.0
        anchors = {(0, 0): [RX - 0.55, 1.9, 0], (0, 1): [RX + 0.75, 1.9, 0],
                   (1, 0): [RX - 0.55, 1.15, 0], (1, 1): [RX + 0.75, 1.15, 0]}
        entries = {}
        for (i, j), a in anchors.items():
            off = i != j
            n = DecimalNumber(0, num_decimal_places=2, include_sign=off, font_size=MIN_FONT,
                              color=RESULT_COLOR if off else INK)

            def up(m, i=i, j=j, a=a):
                m.set_value(clean(Chat(th.get_value())[i, j]))
                m.move_to(a)
            n.add_updater(up)
            up(n)
            entries[(i, j)] = n
        lb = tex(r"\hat C = P^T C P =", INK).move_to([RX - 2.15, 1.52, 0])
        # brackets around the entries
        br = VGroup(
            Line([RX - 1.3, 2.3, 0], [RX - 1.45, 2.3, 0]), Line([RX - 1.45, 2.3, 0], [RX - 1.45, 0.75, 0]),
            Line([RX - 1.45, 0.75, 0], [RX - 1.3, 0.75, 0]),
            Line([RX + 1.4, 2.3, 0], [RX + 1.55, 2.3, 0]), Line([RX + 1.55, 2.3, 0], [RX + 1.55, 0.75, 0]),
            Line([RX + 1.55, 0.75, 0], [RX + 1.4, 0.75, 0]),
        ).set_stroke(INK, 3)
        # fit the header to the left of the matrix: use shorter label
        lb = tex(r"\hat C =", INK).move_to([RX - 1.95, 1.52, 0])
        br.shift(LEFT * 0.0)

        # theta readout under the plane
        th_lab = tex(r"\theta =", INK).move_to([-3.2, -2.4, 0])
        th_num = DecimalNumber(0, num_decimal_places=1, font_size=MIN_FONT, color=INK, unit=r"^\circ")
        th_num.add_updater(lambda m: m.set_value(np.degrees(th.get_value())).next_to(th_lab, RIGHT, buff=0.15))
        th_num.update(0)

        # graph of the off-diagonal entry against theta
        ax = Axes(x_range=[0, 60, 30], y_range=[-2, 2, 1], x_length=2.8, y_length=1.9,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 3, "include_tip": False},
                  x_axis_config={"numbers_to_include": [0, 30, 60], "font_size": MIN_FONT, "decimal_number_config": {"num_decimal_places": 0, "color": INK_DIM}},
                  y_axis_config={"numbers_to_include": [-1, 1], "font_size": MIN_FONT, "decimal_number_config": {"num_decimal_places": 0, "color": INK_DIM}})
        ax.move_to([RX - 0.1, -1.15, 0])
        curve = ax.plot(lambda d: Chat(np.radians(d))[0, 1], x_range=[0, 60], color=RESULT_COLOR, stroke_width=4)
        gl = tex(r"\hat C_{12}", RESULT_COLOR).next_to(ax.c2p(0, 2), RIGHT, buff=0.15)
        gx = tex(r"\theta^\circ", INK_DIM).next_to(ax.c2p(60, 0), UP, buff=0.12).shift(LEFT * 0.1)
        gdot = always_redraw(lambda: Dot(ax.c2p(np.degrees(th.get_value()), Chat(th.get_value())[0, 1]),
                                         radius=0.09, color=HIGHLIGHT))
        graph = VGroup(ax, curve, gl, gx)

        self.add(plane, dots, xl, yl, bas, lb, br, *entries.values(), th_lab, th_num, graph, gdot)
        self.wait(2.0)
        self.play(FadeOut(xl), FadeOut(yl), run_time=0.4)
        self.play(th.animate.set_value(np.radians(60)), run_time=6.5, rate_func=linear)
        self.wait(0.8)
        self.play(th.animate.set_value(TH_EIG), run_time=3.0, rate_func=smooth)
        self.wait(0.5)

        # settle: freeze the numbers at the exact values
        for n in entries.values():
            n.clear_updaters()
        th_num.clear_updaters()
        zeros = []
        for (i, j) in ((0, 1), (1, 0)):
            z = DecimalNumber(0, num_decimal_places=2, font_size=MIN_FONT, color=RESULT_COLOR)
            z.move_to(anchors[(i, j)])
            zeros.append(z)
        self.play(*[Transform(entries[k], z) for k, z in zip(((0, 1), (1, 0)), zeros)], run_time=0.3)
        self.play(*[Flash(entries[k], color=HIGHLIGHT, flash_radius=0.45, line_length=0.18) for k in ((0, 1), (1, 0))],
                  *[entries[k].animate.set_color(HIGHLIGHT) for k in ((0, 1), (1, 0))], run_time=0.8)
        self.play(*[entries[k].animate.set_color(RESULT_COLOR) for k in ((0, 1), (1, 0))], run_time=0.4)
        self.wait(1.2)

        # the eigenvectors
        e1 = tex(r"\mathbf p_1=\tfrac{1}{\sqrt5}(2,\,1)", RESULT_COLOR)
        e2 = tex(r"\mathbf p_2=\tfrac{1}{\sqrt5}(-1,\,2)", W_COLOR)
        e1.move_to([RX + 0.1, -0.5, 0])
        e2.next_to(e1, DOWN, buff=0.45).align_to(e1, LEFT)
        self.play(FadeOut(VGroup(graph, gdot)), run_time=0.5)
        self.play(FadeIn(e1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(e2), run_time=0.7)
        self.wait(2.0)
