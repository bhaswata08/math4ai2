"""Block 3.2, Act 2: new coordinates are dot products, X-hat = XP, and centring survives.

SumCollapse   dot both sides of x_i = sum_j alpha_ij p_j with p_k; every term but j = k dies.
RowTimesP     one point: the row x_i^T times P, entry k is x_i^T p_k.
StackRows     all m points: row i of X times P is row i of X-hat.
CentredStays  the real cloud (cloud2d.csv) turned into the p basis; column means stay 0.
"""

from pathlib import Path

from shared.anim.house import *

X = np.loadtxt(Path(__file__).parent / "data" / "cloud2d.csv", delimiter=",", comments="#")
M, N = X.shape
assert (M, N) == (40, 2) and np.allclose(X.mean(axis=0), 0, atol=1e-5)
P1 = np.array([2.0, 1.0]) / np.sqrt(5)
P2 = np.array([-1.0, 2.0]) / np.sqrt(5)
PM = np.column_stack([P1, P2])
XHAT = X @ PM
assert np.allclose(XHAT.mean(axis=0), 0, atol=1e-5)

P_COLORS = [RESULT_COLOR, W_COLOR, Y_COLOR]  # p_1, p_2, p_n


def tex(*s, color=INK, size=MIN_FONT):
    return MathTex(*s, font_size=size, color=color)


class SumCollapse(Scene):
    def construct(self):
        top = tex(r"\mathbf x_i", "=", r"\alpha_{i1}\mathbf p_1", "+", r"\alpha_{i2}\mathbf p_2",
                  "+", r"\cdots", "+", r"\alpha_{in}\mathbf p_n", size=48)
        top[0].set_color(V_COLOR)
        top.to_edge(UP, buff=0.45)
        rule = tex(r"\mathbf p_j^T\mathbf p_k=\begin{cases}1 & j=k\\ 0 & j\ne k\end{cases}", color=INK_DIM)
        rule.to_corner(DR, buff=0.4)
        self.add(top, rule)
        self.wait(1)

        # take the dot product of both sides with p_2 (k = 2)
        dot = tex(r"\text{dot both sides with } \mathbf p_2", color=HIGHLIGHT)
        dot.next_to(top, DOWN, buff=0.4)
        self.play(FadeIn(dot))
        self.wait(1)
        mid = tex(r"\mathbf x_i^T\mathbf p_2", "=",
                  r"\alpha_{i1}", r"\,\mathbf p_1^T\mathbf p_2", "+",
                  r"\alpha_{i2}", r"\,\mathbf p_2^T\mathbf p_2", "+", r"\cdots", "+",
                  r"\alpha_{in}", r"\,\mathbf p_n^T\mathbf p_2")
        mid[0].set_color(V_COLOR)
        mid.next_to(dot, DOWN, buff=0.45)
        self.play(TransformMatchingShapes(top.copy(), mid), run_time=1.5)
        self.wait(1.5)

        # each p_j^T p_2 is 0 or 1
        mid2 = tex(r"\mathbf x_i^T\mathbf p_2", "=",
                   r"\alpha_{i1}", r"\cdot 0", "+",
                   r"\alpha_{i2}", r"\cdot 1", "+", r"\cdots", "+",
                   r"\alpha_{in}", r"\cdot 0")
        mid2[0].set_color(V_COLOR)
        mid2[6].set_color(HIGHLIGHT)
        mid2.move_to(mid)
        self.play(Indicate(rule, color=HIGHLIGHT), run_time=1)
        self.play(Transform(mid, mid2), run_time=1.5)
        self.wait(1)

        # the zero terms vanish
        dead = VGroup(mid[2], mid[3], mid[8], mid[10], mid[11])
        self.play(dead.animate.set_opacity(0.3), run_time=0.8)
        crosses = VGroup(*[Line(g.get_corner(DL), g.get_corner(UR), color=INK_FAINT, stroke_width=4)
                           for g in (VGroup(mid[2], mid[3]), VGroup(mid[10], mid[11]))])
        self.play(Create(crosses), run_time=0.8)
        self.wait(1)

        res = tex(r"\mathbf x_i^T\mathbf p_2", "=", r"\alpha_{i2}", size=48)
        res[0].set_color(V_COLOR)
        res[2].set_color(RESULT_COLOR)
        res.next_to(mid, DOWN, buff=0.6).set_x(-1.6)
        self.play(TransformFromCopy(VGroup(mid[0], mid[1]), VGroup(res[0], res[1])),
                  TransformFromCopy(mid[5], res[2]), run_time=1.2)
        self.wait(1.5)

        # any k works the same way
        gen = tex(r"\alpha_{ik}", "=", r"\mathbf x_i^T\mathbf p_k", size=56)
        gen[0].set_color(RESULT_COLOR)
        gen[2].set_color(V_COLOR)
        gen.move_to(res).shift(DOWN * 0.15).set_x(-1.6)
        box = SurroundingRectangle(gen, color=HIGHLIGHT, buff=0.18, corner_radius=0.08)
        self.play(ReplacementTransform(res, gen), run_time=1.2)
        self.play(Create(box))
        self.wait(2.5)


def column_block(labels, colors, h=2.4, w=0.55, gap=0.25):
    """Matrix drawn as coloured vertical bars, one per column, with brackets."""
    bars = VGroup()
    for lab, col in zip(labels, colors):
        if lab is None:
            bars.add(tex(r"\cdots", color=INK_DIM))
            continue
        bar = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=col,
                               stroke_width=4, fill_color=col, fill_opacity=0.18)
        t = tex(lab, color=col).move_to(bar)
        bars.add(VGroup(bar, t))
    bars.arrange(RIGHT, buff=gap)
    return bars


def row_bar(lab, col, w, h=0.55):
    bar = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=col,
                           stroke_width=4, fill_color=col, fill_opacity=0.18)
    t = tex(lab, color=col).move_to(bar)
    return VGroup(bar, t)


def brackets(mob, buff=0.12):
    l = tex(r"\big[", size=40).stretch_to_fit_height(mob.height + 0.3).next_to(mob, LEFT, buff=buff)
    r = tex(r"\big]", size=40).stretch_to_fit_height(mob.height + 0.3).next_to(mob, RIGHT, buff=buff)
    return VGroup(l, r)


class RowTimesP(Scene):
    def construct(self):
        xrow = row_bar(r"\mathbf x_i^T", V_COLOR, w=1.7)
        P = column_block([r"\mathbf p_1", r"\mathbf p_2", None, r"\mathbf p_n"],
                         [P_COLORS[0], P_COLORS[1], None, P_COLORS[2]], h=2.2, w=0.55, gap=0.18)
        P_br = brackets(P)
        eq = tex("=")
        out_cells = VGroup(*[tex(s, color=RESULT_COLOR) for s in
                             (r"\alpha_{i1}", r"\alpha_{i2}", r"\cdots", r"\alpha_{in}")])
        out_cells.arrange(RIGHT, buff=0.3)
        out_cells[2].set_color(INK_DIM)
        out_br = brackets(out_cells)
        row = VGroup(xrow, VGroup(P, P_br), eq, VGroup(out_cells, out_br)).arrange(RIGHT, buff=0.35)
        row.move_to(UP * 0.55)
        sz = VGroup(*[tex(t, color=INK_DIM).next_to(g, DOWN, buff=0.2)
                      for t, g in zip((r"1\times n", r"n\times n", r"1\times n"), (xrow, P_br, out_br))])
        for t in sz:
            t.set_y(P_br.get_bottom()[1] - 0.4)
        self.add(xrow, P, P_br, eq, out_br)
        self.wait(1)

        # entry k of the product is row x_i^T against column p_k
        cols = [0, 1, 3]
        cells = [0, 1, 3]
        notes = [r"\mathbf x_i^T\mathbf p_1", r"\mathbf x_i^T\mathbf p_2", r"\mathbf x_i^T\mathbf p_n"]
        for c, e, note, pc in zip(cols, cells, notes, P_COLORS):
            hl_r = xrow[0].copy().set_stroke(HIGHLIGHT, 6).set_fill(opacity=0)
            hl_c = P[c][0].copy().set_stroke(HIGHLIGHT, 6).set_fill(opacity=0)
            lab = tex(note, "=", out_cells[e].get_tex_string(), color=INK)
            lab[0].set_color(pc)
            lab[2].set_color(RESULT_COLOR)
            lab.to_edge(DOWN, buff=0.35)
            self.play(Create(hl_r), Create(hl_c), run_time=0.6)
            self.play(TransformFromCopy(VGroup(xrow[1], P[c][1]), out_cells[e]), FadeIn(lab), run_time=1)
            self.wait(1)
            self.play(FadeOut(hl_r), FadeOut(hl_c), FadeOut(lab), run_time=0.5)
            if c == 1:
                self.play(FadeIn(out_cells[2]), run_time=0.4)
        self.play(FadeIn(sz), run_time=0.8)
        self.wait(1)
        res = tex(r"[\alpha_{i1},\dots,\alpha_{in}]", "=", r"\mathbf x_i^T", "P")
        res[0].set_color(RESULT_COLOR)
        res[2].set_color(V_COLOR)
        res.to_edge(DOWN, buff=0.3)
        self.play(Write(res))
        self.wait(2.5)


class StackRows(Scene):
    def construct(self):
        rw = 1.9
        labs = [r"\mathbf x_1^T", r"\mathbf x_2^T", None, r"\mathbf x_m^T"]
        hlabs = [r"\alpha_{11}\ \cdots\ \alpha_{1n}", r"\alpha_{21}\ \cdots\ \alpha_{2n}", None,
                 r"\alpha_{m1}\ \cdots\ \alpha_{mn}"]

        def stack(ls, col, w):
            g = VGroup()
            for s in ls:
                g.add(tex(r"\vdots", color=INK_DIM) if s is None else row_bar(s, col, w=w, h=0.5))
            return g.arrange(DOWN, buff=0.18)

        Xs = stack(labs, V_COLOR, rw)
        P = column_block([r"\mathbf p_1", None, r"\mathbf p_n"], [P_COLORS[0], None, P_COLORS[2]],
                         h=Xs.height, w=0.55)
        Hs = stack(hlabs, RESULT_COLOR, 2.6)
        eq = tex("=")
        Xh = tex(r"\hat X")
        Xn = tex("X", color=V_COLOR)
        Pn = tex("P")
        body = VGroup(Hs, eq.copy(), Xs, P).arrange(RIGHT, buff=0.4)
        Hs, eq_mid, Xs, P = body
        body.move_to(UP * 0.25)
        brs = VGroup(brackets(Hs), brackets(Xs), brackets(P))
        names = VGroup(Xh.next_to(brs[0], UP, buff=0.12), Xn.next_to(brs[1], UP, buff=0.12),
                       Pn.next_to(brs[2], UP, buff=0.12))
        sz = VGroup(*[tex(s, color=INK_DIM).next_to(b, DOWN, buff=0.15)
                      for s, b in zip((r"m\times n", r"m\times n", r"n\times n"), brs)])
        for t in sz:
            t.set_y(sz[0].get_y())
        Xs_full = VGroup(Xs, brs[1], names[1])
        self.add(Xs_full, P, brs[2], names[2], eq_mid, brs[0], names[0])
        self.wait(1)

        for r in (0, 1, 3):
            hl = Xs[r][0].copy().set_stroke(HIGHLIGHT, 6).set_fill(opacity=0)
            hlP = SurroundingRectangle(P, color=HIGHLIGHT, buff=0.06, stroke_width=4)
            self.play(Create(hl), Create(hlP), run_time=0.5)
            self.play(TransformFromCopy(VGroup(Xs[r], P), Hs[r]), run_time=1)
            self.play(FadeOut(hl), FadeOut(hlP), run_time=0.4)
            if r == 1:
                self.play(FadeIn(Hs[2]), run_time=0.3)
        self.play(FadeIn(sz))
        self.wait(1)

        # a single entry of X-hat
        cell = Hs[1][1]
        ring = SurroundingRectangle(Hs[1], color=HIGHLIGHT, buff=0.05)
        note = tex(r"\text{row } i \text{ of } \hat X", "=", r"\mathbf x_i^T", "P", color=INK)
        note[2].set_color(V_COLOR)
        note.to_edge(DOWN, buff=0.25)
        self.play(Create(ring), FadeIn(note))
        self.wait(2.5)


class CentredStays(Scene):
    def construct(self):
        S = 0.5
        O = np.array([-2.2, 0.0, 0.0])
        ax = house_plane(x_range=[-7, 7, 1], y_range=[-5, 5, 1], x_length=14 * S, y_length=10 * S)
        ax.shift(O)
        th = np.arctan2(P1[1], P1[0])
        cloud = VGroup(*[Dot(O + S * np.array([a, b, 0.0]), radius=0.05, color=V_COLOR) for a, b in X])
        d1, d2 = np.array([*P1, 0]), np.array([*P2, 0])
        a1 = Arrow(O, O + 2.0 * d1, buff=0, color=RESULT_COLOR, stroke_width=5, tip_length=0.2)
        a2 = Arrow(O, O + 1.5 * d2, buff=0, color=W_COLOR, stroke_width=5, tip_length=0.2)
        l1 = tex(r"\mathbf p_1", color=RESULT_COLOR).move_to(O + 2.45 * d1)
        l2 = tex(r"\mathbf p_2", color=W_COLOR).move_to(O + 1.95 * d2)
        l1.add_updater(lambda m: m.move_to(a1.get_end() + 0.4 * normalize(a1.get_end() - O)))
        l2.add_updater(lambda m: m.move_to(a2.get_end() + 0.4 * normalize(a2.get_end() - O)))
        frame = VGroup(cloud, a1, a2)

        def col_means():
            pts = np.array([(d.get_center() - O)[:2] / S for d in cloud])
            return pts.mean(axis=0)

        mean_dot = always_redraw(lambda: Cross(scale_factor=0.14, stroke_color=HIGHLIGHT, stroke_width=5)
                                 .move_to(O + S * np.array([*col_means(), 0])))
        px = 2.6
        head = tex(r"\text{column means}", color=INK).move_to([px, 1.75, 0])
        m1 = DecimalNumber(0, num_decimal_places=2, font_size=MIN_FONT, color=HIGHLIGHT)
        m2 = DecimalNumber(0, num_decimal_places=2, font_size=MIN_FONT, color=HIGHLIGHT)
        m1.add_updater(lambda m: m.set_value(abs(round(col_means()[0], 2))))
        m2.add_updater(lambda m: m.set_value(abs(round(col_means()[1], 2))))
        lbl1 = tex(r"\text{col 1:}", color=INK_DIM)
        lbl2 = tex(r"\text{col 2:}", color=INK_DIM)
        r1 = VGroup(lbl1, m1).arrange(RIGHT, buff=0.2)
        r2 = VGroup(lbl2, m2).arrange(RIGHT, buff=0.2)
        reads = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.3)
        m1.add_updater(lambda m: m.next_to(lbl1, RIGHT, buff=0.2))
        m2.add_updater(lambda m: m.next_to(lbl2, RIGHT, buff=0.2))
        tag = tex(r"X", color=V_COLOR).next_to(head, UP, buff=0.3)
        # one point, whose coordinates do change
        i = int(np.argmax(np.abs(X[:, 0])))
        big = Dot(cloud[i].get_center(), radius=0.09, color=INK)
        big.add_updater(lambda m: m.move_to(cloud[i].get_center()))
        pt_lab = tex(r"\text{one point:}", color=INK_DIM)
        pt_lab.next_to(reads, DOWN, buff=0.45).align_to(reads, LEFT)
        pt_val = always_redraw(lambda: tex(
            "(%.2f,\\ %.2f)" % tuple((cloud[i].get_center() - O)[:2] / S), color=INK)
            .next_to(pt_lab, DOWN, buff=0.12).align_to(pt_lab, LEFT))
        self.add(ax, frame, l1, l2, mean_dot, big, head, reads, tag, pt_lab, pt_val)
        self.wait(2)

        # turn the data into p coordinates: p1 onto the first axis, p2 onto the second
        tag2 = tex(r"\hat X = XP", color=RESULT_COLOR).move_to(tag)
        self.play(Rotate(frame, angle=-th, about_point=O), Transform(tag, tag2), run_time=4)
        assert np.allclose(np.array([(d.get_center() - O)[:2] / S for d in cloud]), XHAT, atol=1e-3)
        self.wait(1)
        self.play(Indicate(reads, color=HIGHLIGHT, scale_factor=1.1))
        why = VGroup(tex(r"\text{mean of } X\mathbf p_k", color=INK),
                     tex(r"=\mathbf 0^T\mathbf p_k=0", color=INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        why.next_to(reads, DOWN, buff=0.45).align_to(reads, LEFT)
        self.play(FadeOut(pt_lab), FadeOut(pt_val), FadeIn(why))
        self.wait(3)
