# Adapted from 3b1b/videos _2017/nn/part3.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0
#
# Colour scheme for this file: activations and weights (given quantities) teal,
# sigma' violet, derived quantities (delta, gradients, cost) amber.

from shared.anim.house import *
import numpy as np

F = MIN_FONT
A_COL = V_COLOR          # activations, weights, inputs
S_COL = W_COLOR          # sigma' factors
D_COL = RESULT_COLOR     # delta, gradients, cost


def tex(s, color=INK, size=F, bg=False):
    m = MathTex(s, font_size=size, color=color)
    if bg:
        m.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
    return m


def node(center, r=0.4, color=INK, sw=3.0):
    return Circle(radius=r, color=color, stroke_width=sw, fill_color=BG, fill_opacity=1.0).move_to(center)


def edge(a, b, color=INK_DIM, sw=3.0):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=sw, max_tip_length_to_length_ratio=0.22)


def box(center, w, h, color):
    return RoundedRectangle(corner_radius=0.1, width=w, height=h, color=color, stroke_width=2.5,
                            fill_color=BG, fill_opacity=1.0).move_to(center)


def sigma(z):
    return 1.0 / (1.0 + np.exp(-z))


class TinyNetwork(Scene):
    def construct(self):
        y0 = 1.6
        xs = [-3.7, -1.85, 0.0, 1.85]
        n0, n1, n2, n3 = [node(np.array([x, y0, 0]), color=c, sw=s) for x, c, s in
                          zip(xs, [INK_DIM, INK_DIM, INK, INK], [2.5, 2.5, 3.0, 3.0])]
        lbl_a0 = tex(r"a^{(0)}", INK_DIM).next_to(n0, UP, buff=0.14)
        lbl_a1 = tex(r"a^{(1)}", INK_DIM).next_to(n1, UP, buff=0.14)
        lbl_a2 = tex(r"a^{(L-1)}", A_COL).next_to(n2, UP, buff=0.14)
        lbl_a3 = tex(r"a^{(L)}", A_COL).next_to(n3, UP, buff=0.14)

        e0 = edge(n0.get_right(), n1.get_left(), INK_DIM)
        e1 = edge(n1.get_right(), n2.get_left(), INK_DIM)
        e2 = edge(n2.get_right(), n3.get_left(), A_COL, 3.5)
        w1 = tex(r"w^{(1)}", INK_DIM, bg=True).next_to(e0, DOWN, buff=0.12)
        w2 = tex(r"w^{(2)}", INK_DIM, bg=True).next_to(e1, DOWN, buff=0.12)
        wL = tex(r"w^{(L)}", A_COL, bg=True).next_to(e2, DOWN, buff=0.12)

        cost_box = box(np.array([3.75, y0, 0]), 1.2, 0.8, D_COL)
        cost_txt = tex(r"C", D_COL).move_to(cost_box)
        a_to_c = edge(n3.get_right(), cost_box.get_left(), D_COL)
        y_box = box(np.array([3.75, 0.4, 0]), 1.0, 0.7, A_COL)
        y_txt = tex(r"y", A_COL).move_to(y_box)
        y_to_c = Arrow(y_box.get_top(), cost_box.get_bottom(), buff=0.08, color=INK_DIM, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.3)

        early = VGroup(n0, n1, e0, e1, lbl_a0, lbl_a1, w1, w2)
        early.set_opacity(0.2)
        last = VGroup(n2, n3, e2, lbl_a2, lbl_a3, wL, cost_box, cost_txt, a_to_c, y_box, y_txt, y_to_c)
        self.add(early, last)
        self.wait(2.0)

        b_arrow = Arrow(np.array([1.85, 0.35, 0]), np.array([1.85, 1.15, 0]), buff=0.05, color=A_COL,
                        stroke_width=3, max_tip_length_to_length_ratio=0.25)
        b_lbl = tex(r"+\, b^{(L)}", A_COL, bg=True).next_to(b_arrow, DOWN, buff=0.08)
        self.play(Create(b_arrow), FadeIn(b_lbl), run_time=1.0)
        self.wait(1.0)

        eq_z = MathTex(r"z^{(L)}", r"=", r"w^{(L)}", r"a^{(L-1)}", r"+", r"b^{(L)}", font_size=F)
        eq_z[0].set_color(INK)
        for i in (2, 3, 5):
            eq_z[i].set_color(A_COL)
        eq_a = MathTex(r"a^{(L)}", r"=", r"\sigma(", r"z^{(L)}", r")", font_size=F)
        eq_a[0].set_color(A_COL)
        eq_c = MathTex(r"C", r"=", r"(", r"a^{(L)}", r"-", r"y", r")^2", font_size=F)
        eq_c[0].set_color(D_COL)
        eq_c[3].set_color(A_COL)
        eq_c[5].set_color(A_COL)
        VGroup(eq_z, eq_a).arrange(RIGHT, buff=0.8).move_to(np.array([0, -0.75, 0]))
        eq_c.move_to(np.array([0, -1.9, 0]))
        box_c = SurroundingRectangle(eq_c, color=D_COL, buff=0.16, stroke_width=2.5)

        self.play(FadeIn(eq_z), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(eq_a), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(eq_c), FadeIn(box_c), run_time=0.8)
        self.wait(3.0)


class DependencyTree(Scene):
    def construct(self):
        yp = 0.35
        bw = box(np.array([-3.6, yp, 0]), 1.4, 0.8, A_COL)
        tw = tex(r"w^{(L)}", A_COL).move_to(bw)
        bz = box(np.array([-1.2, yp, 0]), 1.3, 0.8, INK_DIM)
        tz = tex(r"z^{(L)}", INK).move_to(bz)
        ba = box(np.array([1.2, yp, 0]), 1.3, 0.8, A_COL)
        ta = tex(r"a^{(L)}", A_COL).move_to(ba)
        bc = box(np.array([3.6, yp, 0]), 1.3, 0.8, D_COL)
        tc = tex(r"C", D_COL).move_to(bc)
        by = box(np.array([3.6, -1.15, 0]), 1.3, 0.8, A_COL)
        ty = tex(r"y", A_COL).move_to(by)

        a_wz = edge(bw.get_right(), bz.get_left())
        a_za = edge(bz.get_right(), ba.get_left())
        a_ac = edge(ba.get_right(), bc.get_left())
        a_yc = Arrow(by.get_top(), bc.get_bottom(), buff=0.08, color=INK_DIM, stroke_width=3,
                     max_tip_length_to_length_ratio=0.3)
        tree = VGroup(bw, tw, bz, tz, ba, ta, bc, tc, by, ty, a_wz, a_za, a_ac, a_yc)
        self.add(tree)
        self.wait(1.5)

        def nudge(b, s, col):
            fl = SurroundingRectangle(b, color=HIGHLIGHT, buff=0.08, stroke_width=3)
            lab = tex(s, col, bg=True).next_to(b, UP, buff=0.14)
            return fl, lab

        fl, nw = nudge(bw, r"dw", A_COL)
        self.play(Create(fl), FadeIn(nw), run_time=0.6)
        self.play(FadeOut(fl), run_time=0.4)
        self.wait(0.4)

        steps = [
            (a_wz, bz, r"\frac{\partial z^{(L)}}{\partial w^{(L)}}", A_COL, r"dz", A_COL),
            (a_za, ba, r"\frac{\partial a^{(L)}}{\partial z^{(L)}}", S_COL, r"da", A_COL),
            (a_ac, bc, r"\frac{\partial C}{\partial a^{(L)}}", D_COL, r"dC", D_COL),
        ]
        for arr, tgt, fac, fcol, dn, dcol in steps:
            lf = tex(fac, fcol, size=F + 2, bg=True).next_to(arr, UP, buff=0.75)
            fl, nl = nudge(tgt, dn, dcol)
            self.play(arr.animate.set_color(fcol).set_stroke(width=4.5), FadeIn(lf), run_time=1.0)
            self.play(Create(fl), FadeIn(nl), run_time=0.5)
            self.play(FadeOut(fl), run_time=0.3)
            self.wait(0.7)

        flow = MathTex(r"dw", r"\;\longrightarrow\;", r"dz", r"\;\longrightarrow\;",
                       r"da", r"\;\longrightarrow\;", r"dC", font_size=F + 2)
        for i, c in enumerate([A_COL, INK_DIM, A_COL, INK_DIM, A_COL, INK_DIM, D_COL]):
            flow[i].set_color(c)
        flow.move_to(np.array([-0.9, -2.25, 0]))
        fbox = SurroundingRectangle(flow, color=D_COL, buff=0.14, stroke_width=2.5)
        self.play(FadeIn(flow), FadeIn(fbox), run_time=1.0)
        self.wait(3.0)


class ChainRuleProduct(Scene):
    def construct(self):
        # Left panel: the slice of the network the derivative runs through,
        # drawn top to bottom so each arrow sits level with the factor it
        # produces on the right. Every symbol in the formula is on screen.
        cx = -4.1
        lv = [1.95, 0.70, -0.55, -1.80]
        n_prev = node(np.array([cx, lv[0], 0]), r=0.33, color=A_COL)
        b_z = box(np.array([cx, lv[1], 0]), 0.9, 0.55, INK_DIM)
        n_last = node(np.array([cx, lv[2], 0]), r=0.33, color=A_COL)
        b_cost = box(np.array([cx, lv[3], 0]), 0.9, 0.55, D_COL)
        t_prev = tex(r"a^{(L-1)}", A_COL).next_to(n_prev, RIGHT, buff=0.18)
        t_z = tex(r"z^{(L)}", INK).move_to(b_z)
        t_last = tex(r"a^{(L)}", A_COL).next_to(n_last, RIGHT, buff=0.18)
        t_cost = tex(r"C", D_COL).move_to(b_cost)
        t_y = tex(r"y", A_COL).move_to(np.array([cx + 1.0, lv[3], 0]))

        a_wz = edge(n_prev.get_bottom(), b_z.get_top(), INK_DIM)
        a_za = edge(b_z.get_bottom(), n_last.get_top(), INK_DIM)
        a_ac = edge(n_last.get_bottom(), b_cost.get_top(), INK_DIM)
        a_yc = edge(t_y.get_left(), b_cost.get_right(), INK_DIM)
        l_w = tex(r"w^{(L)}", A_COL, bg=True).next_to(a_wz, RIGHT, buff=0.1)
        l_s = tex(r"\sigma", S_COL, bg=True).next_to(a_za, RIGHT, buff=0.1)

        net = VGroup(n_prev, b_z, n_last, b_cost, t_prev, t_z, t_last, t_cost, t_y,
                     a_wz, a_za, a_ac, a_yc, l_w, l_s)

        # Right panel: the same three steps as algebra.
        chain = MathTex(
            r"\frac{\partial C}{\partial w^{(L)}}", r"=",
            r"\frac{\partial z^{(L)}}{\partial w^{(L)}}", r"\;\cdot\;",
            r"\frac{\partial a^{(L)}}{\partial z^{(L)}}", r"\;\cdot\;",
            r"\frac{\partial C}{\partial a^{(L)}}", font_size=F)
        chain[0].set_color(INK)
        chain[2].set_color(A_COL)
        chain[4].set_color(S_COL)
        chain[6].set_color(D_COL)
        chain.move_to(np.array([1.45, 2.3, 0]))

        rows = []
        for num, den, val, col in [
            (r"\partial z^{(L)}", r"\partial w^{(L)}", r"a^{(L-1)}", A_COL),
            (r"\partial a^{(L)}", r"\partial z^{(L)}", r"\sigma'(z^{(L)})", S_COL),
            (r"\partial C", r"\partial a^{(L)}", r"2(a^{(L)} - y)", D_COL),
        ]:
            r = MathTex(rf"\frac{{{num}}}{{{den}}}", r"=", val, font_size=F, color=col)
            rows.append(r)
        # One row per network arrow, in the same order, flush with the chain.
        for r, y in zip(rows, [1.18, 0.08, -1.02]):
            r.move_to(np.array([chain.get_left()[0], y, 0]), aligned_edge=LEFT)

        final = MathTex(r"\frac{\partial C}{\partial w^{(L)}}", r"=", r"a^{(L-1)}", r"\cdot",
                        r"\sigma'(z^{(L)})", r"\cdot", r"2(a^{(L)} - y)", font_size=F)
        final[0].set_color(INK)
        final[2].set_color(A_COL)
        final[4].set_color(S_COL)
        final[6].set_color(D_COL)
        final.move_to(np.array([1.2, -2.18, 0]))
        fbox = SurroundingRectangle(final, color=D_COL, buff=0.14, stroke_width=2.5)

        self.add(net, chain)
        self.wait(1.5)

        for idx, row, arr, lbl, col in [
            (2, rows[0], a_wz, l_w, A_COL),
            (4, rows[1], a_za, l_s, S_COL),
            (6, rows[2], a_ac, None, D_COL),
        ]:
            self.play(Indicate(chain[idx], color=HIGHLIGHT, scale_factor=1.15),
                      arr.animate.set_color(col).set_stroke(width=5),
                      *([Indicate(lbl, color=HIGHLIGHT, scale_factor=1.15)] if lbl else []),
                      run_time=0.9)
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.8)

        self.play(FadeIn(final, shift=UP * 0.2), FadeIn(fbox), run_time=1.0)
        self.wait(3.5)


class GoDeeper(Scene):
    def construct(self):
        yn = 1.6
        xs = [-3.45, -1.15, 1.15]
        n_l2, n_l1, n_l = [node(np.array([x, yn, 0]), color=INK_DIM, sw=2.5) for x in xs]
        bc = box(np.array([3.45, yn, 0]), 1.2, 0.8, D_COL)
        tc = tex(r"C", D_COL).move_to(bc)
        lab_l2 = tex(r"a^{(L-2)}", A_COL).next_to(n_l2, UP, buff=0.12)
        lab_l1 = tex(r"a^{(L-1)}", A_COL).next_to(n_l1, UP, buff=0.12)
        lab_l = tex(r"a^{(L)}", A_COL).next_to(n_l, UP, buff=0.12)
        f1 = edge(n_l2.get_right(), n_l1.get_left())
        f2 = edge(n_l1.get_right(), n_l.get_left())
        f3 = edge(n_l.get_right(), bc.get_left(), D_COL)
        wl1 = tex(r"w^{(L-1)}", A_COL, bg=True).next_to(f1, DOWN, buff=0.1)
        wl = tex(r"w^{(L)}", A_COL, bg=True).next_to(f2, DOWN, buff=0.1)
        net = VGroup(n_l2, n_l1, n_l, bc, tc, lab_l2, lab_l1, lab_l, f1, f2, f3, wl1, wl)

        eq = MathTex(r"\frac{\partial C}{\partial a^{(L-1)}}", r"=", r"w^{(L)}", r"\cdot",
                     r"\sigma'(z^{(L)})", r"\cdot", r"2(a^{(L)} - y)", font_size=F + 2)
        eq[0].set_color(D_COL)
        eq[2].set_color(A_COL)
        eq[4].set_color(S_COL)
        eq[6].set_color(D_COL)
        eq.move_to(np.array([0, 0.1, 0]))
        self.add(net, eq)
        self.wait(2.5)

        reused = VGroup(eq[4], eq[5], eq[6])
        brace = Brace(reused, DOWN, buff=0.1, color=HIGHLIGHT)
        r_lbl = tex(r"\text{reused from layer } L", HIGHLIGHT).next_to(brace, DOWN, buff=0.12)
        self.play(Create(brace), FadeIn(r_lbl), run_time=1.4)
        self.wait(2.5)
        d_def = MathTex(r"\boldsymbol{\delta}^{(L)}", r"=", r"\frac{\partial C}{\partial z^{(L)}}", r"=",
                        r"\sigma'(z^{(L)})", r"\cdot", r"2(a^{(L)} - y)", font_size=F)
        d_def[0].set_color(D_COL)
        d_def[2].set_color(D_COL)
        d_def[4].set_color(S_COL)
        d_def[6].set_color(D_COL)
        d_def.move_to(np.array([0.0, -1.55, 0]))
        self.play(FadeOut(r_lbl), run_time=0.6)
        self.play(FadeIn(d_def), run_time=1.2)
        self.wait(3.0)

        # Pull the reused product out as delta^{(L)}.
        self.play(FadeOut(brace), FadeOut(d_def), FadeOut(eq), run_time=0.9)
        eq_a = MathTex(r"\frac{\partial C}{\partial a^{(L-1)}}", r"=", r"w^{(L)}", r"\cdot",
                       r"\boldsymbol{\delta}^{(L)}", font_size=F + 2)
        eq_w = MathTex(r"\frac{\partial C}{\partial w^{(L)}}", r"=", r"a^{(L-1)}", r"\cdot",
                       r"\boldsymbol{\delta}^{(L)}", font_size=F + 2)
        for e, c in ((eq_a, A_COL), (eq_w, A_COL)):
            e[0].set_color(D_COL)
            e[2].set_color(c)
            e[4].set_color(D_COL)
        VGroup(eq_a, eq_w).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(np.array([0, -0.5, 0]))
        eq_w.align_to(eq_a, LEFT)
        self.play(FadeIn(eq_a), FadeIn(eq_w), run_time=1.2)
        self.wait(1.2)
        boxes = VGroup(SurroundingRectangle(eq_a[4], color=HIGHLIGHT, buff=0.1, stroke_width=3),
                       SurroundingRectangle(eq_w[4], color=HIGHLIGHT, buff=0.1, stroke_width=3))
        tw = tex(r"\text{one } \delta^{(L)}\text{, used twice}", HIGHLIGHT).move_to(np.array([0, -2.1, 0]))
        self.play(Create(boxes), FadeIn(tw), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(boxes), FadeOut(tw), run_time=0.6)

        # Backward sweep along the chain, one node at a time so it can be
        # followed at talking speed.
        cb = SurroundingRectangle(bc, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(cb), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(cb), run_time=0.4)
        prev, pts = bc, [n_l, n_l1, n_l2]
        for tgt in pts:
            pulse = Arrow(prev.get_left(), tgt.get_right(), buff=0.08, color=HIGHLIGHT, stroke_width=5,
                          max_tip_length_to_length_ratio=0.22)
            fl = SurroundingRectangle(tgt, color=HIGHLIGHT, buff=0.08, stroke_width=3)
            self.play(Create(pulse), run_time=0.8)
            self.play(Create(fl), FadeOut(pulse), run_time=0.5)
            self.wait(0.35)
            self.play(FadeOut(fl), run_time=0.35)
            prev = tgt
        self.wait(0.8)

        # Next layer back: delta^{(L)} reaches every earlier weight.
        self.play(FadeOut(eq_a), FadeOut(eq_w), run_time=0.7)
        e1 = MathTex(r"\frac{\partial C}{\partial w^{(L-1)}}", r"=", r"a^{(L-2)}", r"\cdot",
                     r"\sigma'(z^{(L-1)})", r"\cdot", r"\frac{\partial C}{\partial a^{(L-1)}}", font_size=F)
        e2 = MathTex(r"=", r"a^{(L-2)}", r"\cdot", r"\sigma'(z^{(L-1)})", r"\cdot", r"w^{(L)}", r"\cdot",
                     r"\boldsymbol{\delta}^{(L)}", font_size=F)
        e1[0].set_color(D_COL); e1[2].set_color(A_COL); e1[4].set_color(S_COL); e1[6].set_color(D_COL)
        e2[1].set_color(A_COL); e2[3].set_color(S_COL); e2[5].set_color(A_COL); e2[7].set_color(D_COL)
        e1.move_to(np.array([0, -0.3, 0]))
        e2.next_to(e1, DOWN, buff=0.45).align_to(e1[1], LEFT)
        fb = SurroundingRectangle(VGroup(e1, e2), color=D_COL, buff=0.2, stroke_width=2.5)
        self.play(FadeIn(e1), run_time=1.2)
        self.wait(2.0)
        self.play(FadeIn(e2), FadeIn(fb), run_time=1.2)
        self.wait(3.5)


def rounded(v, nd):
    return f"{v:.{nd}f}"


class TinyNetworkNumbers(Scene):
    def construct(self):
        a_prev, w, b, y = 0.5, 2.0, -0.5, 1.0

        def forward(wv):
            z = wv * a_prev + b
            a = sigma(z)
            return z, a, (a - y) ** 2

        z, a, C = forward(w)
        sp = a * (1 - a)
        dCda = 2 * (a - y)
        grad = a_prev * sp * dCda
        z2, a2, C2 = forward(w + 0.01)
        dC = C2 - C
        f1 = lambda v: f"{v:.1f}"
        f3 = lambda v: f"{v:.3f}"
        f4 = lambda v: f"{v:.4f}"
        f5 = lambda v: f"{v:.5f}"

        yc = 1.1
        b0 = box(np.array([-4.0, yc, 0]), 1.7, 0.8, A_COL)
        t0 = tex(r"a^{(L-1)}", A_COL).move_to(b0)
        bz = box(np.array([-1.2, yc, 0]), 1.1, 0.8, INK_DIM)
        tz = tex(r"z", INK).move_to(bz)
        ba = box(np.array([1.3, yc, 0]), 1.1, 0.8, A_COL)
        ta = tex(r"a", A_COL).move_to(ba)
        bc = box(np.array([3.9, yc, 0]), 1.1, 0.8, D_COL)
        tc = tex(r"C", D_COL).move_to(bc)
        e1 = edge(b0.get_right(), bz.get_left())
        e2 = edge(bz.get_right(), ba.get_left())
        e3 = edge(ba.get_right(), bc.get_left())
        by = box(np.array([3.9, 2.3, 0]), 1.5, 0.7, A_COL)
        ty = tex(rf"y={f1(y)}".replace(".0", ""), A_COL).move_to(by)
        ey = Arrow(by.get_bottom(), bc.get_top(), buff=0.05, color=INK_DIM, stroke_width=3,
                   max_tip_length_to_length_ratio=0.35)
        bb = box(np.array([-0.9, 2.35, 0]), 2.0, 0.7, A_COL)
        tb = tex(rf"b={f1(b)}", A_COL).move_to(bb)
        eb = Arrow(np.array([-1.2, bb.get_bottom()[1], 0]), bz.get_top(), buff=0.05, color=INK_DIM,
                   stroke_width=3, max_tip_length_to_length_ratio=0.35)
        lw = tex(rf"w={f1(w)}".replace(".0", ""), A_COL).next_to(e1, UP, buff=0.12)
        ls = tex(r"\sigma", S_COL).next_to(e2, UP, buff=0.12)
        v0 = tex(f1(a_prev), A_COL).move_to(np.array([-4.0, 0.3, 0]))
        vz = tex(f1(z), INK).move_to(np.array([-1.2, 0.3, 0]))
        va = tex(f4(a), A_COL).move_to(np.array([1.3, 0.3, 0]))
        vc = tex(f4(C), D_COL).move_to(np.array([3.9, 0.3, 0]))

        self.add(b0, t0, bz, tz, ba, ta, bc, tc, e1, e2, e3, by, ty, ey, bb, tb, eb, lw, ls, v0)
        self.wait(2.0)

        def line(s, col=INK, yy=-1.0):
            return tex(s, col).move_to(np.array([0, yy, 0]))

        steps = [
            (vz, line(rf"z = w\,a^{{(L-1)}} + b = 2({f1(a_prev)}) - 0.5 = {f1(z)}")),
            (va, line(rf"a = \sigma(z) = \sigma({f1(z)}) = {f4(a)}")),
            (vc, line(rf"C = (a-y)^2 = ({f4(a)}-1)^2 = {f4(C)}", D_COL)),
        ]
        cur = None
        for v, ln in steps:
            if cur is not None:
                self.play(FadeOut(cur), run_time=0.3)
            self.play(FadeIn(ln), FadeIn(v), run_time=0.7)
            self.wait(1.5)
            cur = ln
        self.play(FadeOut(cur), FadeOut(VGroup(v0, vz, va, vc, lw, ls)), run_time=0.5)

        # Backward pass: a local factor on each edge.
        fr1 = tex(r"\frac{\partial z}{\partial w}", A_COL).next_to(e1, UP, buff=0.15)
        fr2 = tex(r"\sigma'(z)", S_COL).next_to(e2, UP, buff=0.12)
        fr3 = tex(r"\frac{\partial C}{\partial a}", D_COL).next_to(e3, UP, buff=0.15)
        n1 = tex(f1(a_prev), A_COL).move_to(np.array([e1.get_center()[0], 0.55, 0]))
        n2 = tex(f3(sp), S_COL).move_to(np.array([e2.get_center()[0], 0.55, 0]))
        n3 = tex(f3(dCda), D_COL).move_to(np.array([e3.get_center()[0], 0.55, 0]))
        for fr, n, col in ((fr1, n1, A_COL), (fr2, n2, S_COL), (fr3, n3, D_COL)):
            self.play(FadeIn(fr), FadeIn(n), run_time=0.8)
            self.wait(0.9)
        # Spell out where 0.235 comes from, then multiply.
        sp_line = line(rf"\sigma'(z) = a(1-a) = {f4(a)}\cdot{f4(1 - a)} = {f3(sp)}", S_COL, -0.9)
        self.play(FadeIn(sp_line), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(sp_line), run_time=0.3)
        prod = line(rf"\frac{{\partial C}}{{\partial w}} = {f1(a_prev)}\cdot{f3(sp)}\cdot({f3(dCda)}) = {f4(grad)}",
                    INK, -1.0)
        pbox = SurroundingRectangle(prod, color=D_COL, buff=0.14, stroke_width=2.5)
        self.play(FadeIn(prod), FadeIn(pbox), run_time=0.8)
        self.wait(2.2)

        # Numerical check.
        self.play(FadeOut(VGroup(fr1, fr2, fr3, n1, n2, n3)), prod.animate.move_to(np.array([0, -0.5, 0])),
                  pbox.animate.move_to(np.array([0, -0.5, 0])), run_time=0.6)
        l1 = tex(rf"w:\; 2.00 \to 2.01 \qquad C:\; {f5(C)} \to {f5(C2)}", INK).move_to(np.array([0, -1.5, 0]))
        l2 = tex(rf"\Delta C = {f5(dC)} \;\approx\; {f4(grad)}\times 0.01", D_COL).move_to(np.array([0, -2.35, 0]))
        cbox = SurroundingRectangle(l2, color=D_COL, buff=0.14, stroke_width=2.5)
        self.play(FadeIn(l1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(l2), FadeIn(cbox), run_time=0.8)
        self.wait(3.0)


class MatrixBackprop(Scene):
    def construct(self):
        a0 = np.array([1.0, 0.5])
        W1 = np.array([[1.0, -1.0], [0.5, 1.0], [-1.0, 0.5]])
        W2 = np.array([[2.0, -3.0, 1.0]])
        y = 1.0
        z1 = W1 @ a0
        a1 = sigma(z1)
        z2 = W2 @ a1
        a2 = sigma(z2)
        sp2 = a2 * (1 - a2)
        sp1 = a1 * (1 - a1)
        d2 = 2 * (a2 - y) * sp2                     # delta^(L), 1 entry
        u = W2.T @ d2                               # W^T delta
        d1 = u * sp1                                # delta^(L-1)
        dW = np.outer(d1, a0)

        f2 = lambda v: f"{v:.2f}"

        def vec(vals, col, nd=2):
            m = Matrix([[f"{v:.{nd}f}"] for v in np.ravel(vals)], v_buff=0.62, h_buff=1.0,
                       bracket_h_buff=0.15, bracket_v_buff=0.15,
                       element_to_mobject=MathTex, element_to_mobject_config={"font_size": F})
            for e in m.get_entries():
                e.set_color(col)
            m.get_brackets().set_color(INK_DIM)
            return m

        def mat(vals, col, nd=2, hb=1.35):
            rows = [[f"{v:.{nd}f}" for v in r] for r in np.atleast_2d(vals)]
            m = Matrix(rows, v_buff=0.62, h_buff=hb, bracket_h_buff=0.15, bracket_v_buff=0.15,
                       element_to_mobject=MathTex, element_to_mobject_config={"font_size": F})
            for e in m.get_entries():
                e.set_color(col)
            m.get_brackets().set_color(INK_DIM)
            return m

        # ---- Stage 0: forward values (frame one) ----
        c0 = vec(a0, A_COL).move_to(np.array([-3.5, -0.1, 0]))
        c1 = vec(a1, A_COL).move_to(np.array([0.0, -0.1, 0]))
        c2 = vec(a2, A_COL).move_to(np.array([3.5, -0.1, 0]))
        l0 = tex(r"a^{(L-2)}", A_COL).next_to(c0, UP, buff=0.35)
        l1 = tex(r"a^{(L-1)}", A_COL).next_to(c1, UP, buff=0.35)
        l2 = tex(r"a^{(L)}", A_COL).next_to(c2, UP, buff=0.35)
        ar1 = Arrow(c0.get_right() + RIGHT * 0.1, c1.get_left() + LEFT * 0.1, buff=0.05, color=INK_DIM,
                    stroke_width=3, max_tip_length_to_length_ratio=0.2)
        ar2 = Arrow(c1.get_right() + RIGHT * 0.1, c2.get_left() + LEFT * 0.1, buff=0.05, color=INK_DIM,
                    stroke_width=3, max_tip_length_to_length_ratio=0.2)
        wl1 = tex(r"W^{(L-1)}", A_COL).next_to(ar1, UP, buff=0.1)
        wl2 = tex(r"W^{(L)}", A_COL).next_to(ar2, UP, buff=0.1)
        yl = tex(rf"y = 1", A_COL).move_to(np.array([0, -2.1, 0]))
        stage0 = VGroup(c0, c1, c2, l0, l1, l2, ar1, ar2, wl1, wl2, yl)
        self.add(stage0)
        self.wait(3.0)
        self.play(FadeOut(stage0), run_time=0.5)

        # header helper
        # ---- Stage 1: delta^(L) ----
        h1 = MathTex(r"\boldsymbol\delta^{(L)}", "=", r"\nabla_{\mathbf a} C", r"\odot", r"\sigma'(\mathbf z^{(L)})",
                     font_size=F).move_to(np.array([0, 2.2, 0]))
        h1[0].set_color(D_COL); h1[2].set_color(D_COL); h1[4].set_color(S_COL)
        b1 = tex(rf"\boldsymbol\delta^{{(L)}} = 2(a^{{(L)}}-y)\,\sigma'(z^{{(L)}})", INK).move_to(np.array([0, 0.9, 0]))
        b1b = tex(rf"= 2({f2(a2[0])}-1)\cdot {f2(sp2[0])} = {f2(d2[0])}", D_COL)
        b1b.move_to(np.array([0, -0.3, 0]))
        dbox = SurroundingRectangle(b1b, color=D_COL, buff=0.16, stroke_width=2.5)
        self.play(FadeIn(h1), run_time=0.6)
        self.play(FadeIn(b1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeIn(b1b), FadeIn(dbox), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(VGroup(b1, b1b, dbox, h1)), run_time=0.5)

        # ---- Stage 2: step back through W^T ----
        h2 = MathTex(r"\boldsymbol\delta^{(L-1)}", "=", r"\big(", r"W^{(L)\top}\boldsymbol\delta^{(L)}", r"\big)",
                     r"\odot", r"\sigma'(\mathbf z^{(L-1)})", font_size=F).move_to(np.array([0, 2.2, 0]))
        h2[0].set_color(D_COL); h2[3].set_color(D_COL); h2[6].set_color(S_COL)
        h2[0].set_opacity(0.5); h2[6].set_opacity(0.5); h2[1].set_opacity(0.5); h2[5].set_opacity(0.5)
        Wrow = mat(W2, A_COL, nd=0).move_to(np.array([-3.2, 0.1, 0]))
        Wlab = tex(r"W^{(L)}", A_COL).next_to(Wrow, DOWN, buff=0.5)
        dsc = vec(d2, D_COL).move_to(np.array([0.2, 0.1, 0]))
        dlab = tex(r"\boldsymbol\delta^{(L)}", D_COL).next_to(dsc, DOWN, buff=0.5)
        self.play(FadeIn(h2), FadeIn(Wrow), FadeIn(Wlab), FadeIn(dsc), FadeIn(dlab), run_time=0.8)
        self.wait(1.4)
        Wcol = vec(W2.T, A_COL).move_to(np.array([-3.2, 0.1, 0]))
        Wlab_t = tex(r"W^{(L)\top}", A_COL).next_to(Wcol, DOWN, buff=0.5)
        tr_note = tex(r"\text{transpose}", HIGHLIGHT).move_to(np.array([-3.2, 2.2 - 0.0, 0]))
        tr_note.move_to(np.array([-3.2, -2.05, 0]))
        self.play(ReplacementTransform(Wrow, Wcol), ReplacementTransform(Wlab, Wlab_t),
                  FadeIn(tr_note), run_time=1.2)
        self.wait(1.3)
        self.play(FadeOut(tr_note), run_time=0.3)
        eq_s = tex(r"\times", INK).move_to(np.array([-1.35, 0.1, 0]))
        eq_e = tex(r"=", INK).move_to(np.array([1.75, 0.1, 0]))
        ucol = vec(u, D_COL).move_to(np.array([3.5, 0.1, 0]))
        ulab = tex(r"W^{(L)\top}\boldsymbol\delta^{(L)}", D_COL, size=F).next_to(ucol, DOWN, buff=0.5)
        ulab.set_x(min(3.5, 5 - 0.15 - ulab.width / 2))
        self.play(FadeIn(eq_s), FadeIn(eq_e), run_time=0.4)
        self.play(FadeIn(ucol), FadeIn(ulab), run_time=0.8)
        self.wait(1.6)

        # ---- Stage 3: element-wise product ----
        self.play(FadeOut(VGroup(Wcol, Wlab_t, dsc, dlab, eq_s, eq_e, ulab)), run_time=0.5)
        h3 = MathTex(r"\boldsymbol\delta^{(L-1)}", "=", r"\big(", r"W^{(L)\top}\boldsymbol\delta^{(L)}", r"\big)",
                     r"\odot", r"\sigma'(\mathbf z^{(L-1)})", font_size=F).move_to(np.array([0, 2.2, 0]))
        h3[0].set_color(D_COL); h3[3].set_color(D_COL); h3[6].set_color(S_COL)
        self.play(ReplacementTransform(h2, h3), run_time=0.4)
        self.play(ucol.animate.move_to(np.array([-3.4, 0.1, 0])), run_time=0.7)
        ulab2 = tex(r"W^{(L)\top}\boldsymbol\delta^{(L)}", D_COL).next_to(ucol, DOWN, buff=0.5)
        ulab2.set_x(max(ucol.get_x(), -5 + 0.15 + ulab2.width / 2))
        scol = vec(sp1, S_COL).move_to(np.array([0.2, 0.1, 0]))
        slab = tex(r"\sigma'(\mathbf z^{(L-1)})", S_COL).next_to(scol, DOWN, buff=0.5)
        dcol = vec(d1, D_COL).move_to(np.array([3.5, 0.1, 0]))
        dcol_entries = dcol.get_entries()
        hop = tex(r"\odot", INK).move_to(np.array([-1.6, 0.1, 0]))
        heq = tex(r"=", INK).move_to(np.array([1.85, 0.1, 0]))
        dlab2 = tex(r"\boldsymbol\delta^{(L-1)}", D_COL).next_to(dcol, DOWN, buff=0.5)
        self.play(FadeIn(ulab2), FadeIn(hop), FadeIn(scol), FadeIn(slab), FadeIn(heq),
                  FadeIn(dcol.get_brackets()), FadeIn(dlab2), run_time=0.8)
        self.wait(0.6)
        for i in range(3):
            rect = SurroundingRectangle(VGroup(ucol.get_entries()[i], scol.get_entries()[i]),
                                        color=HIGHLIGHT, buff=0.12, stroke_width=3)
            self.play(Create(rect), run_time=0.3)
            self.play(FadeIn(dcol_entries[i], shift=LEFT * 0.2), run_time=0.4)
            self.play(FadeOut(rect), run_time=0.2)
        self.wait(1.5)

        # ---- Stage 4: outer product ----
        self.play(FadeOut(VGroup(ucol, ulab2, hop, scol, slab, heq, dlab2)), run_time=0.5)
        h4 = MathTex(r"\frac{\partial C}{\partial W^{(L-1)}}", "=", r"\boldsymbol\delta^{(L-1)}",
                     r"\,\mathbf a^{(L-2)\top}", font_size=F).move_to(np.array([0, 2.15, 0]))
        h4[0].set_color(D_COL); h4[2].set_color(D_COL); h4[3].set_color(A_COL)
        self.play(FadeOut(h3), run_time=0.2)
        self.play(FadeIn(h4), dcol.animate.move_to(np.array([-3.5, 0.0, 0])), run_time=0.7)
        arow = mat(a0.reshape(1, 2), A_COL, nd=1, hb=1.0).move_to(np.array([-1.0, 0.0, 0]))
        dlab3 = tex(r"\boldsymbol\delta^{(L-1)}", D_COL).next_to(dcol, DOWN, buff=0.5)
        dlab3.set_x(max(dcol.get_x(), -5 + 0.15 + dlab3.width / 2))
        alab = tex(r"\mathbf a^{(L-2)\top}", A_COL).next_to(arow, DOWN, buff=0.5)
        # place the row at the vertical middle row of delta so the outer product reads as col x row
        grid = mat(dW, D_COL, hb=1.25).move_to(np.array([3.2, 0.0, 0]))
        geq = tex(r"=", INK).move_to(np.array([0.7, 0.0, 0]))
        glab = tex(r"\frac{\partial C}{\partial W^{(L-1)}}", D_COL).next_to(grid, DOWN, buff=0.4)
        self.play(FadeIn(arow), FadeIn(dlab3), FadeIn(alab), FadeIn(geq), FadeIn(grid.get_brackets()),
                  FadeIn(glab), run_time=0.8)
        self.wait(0.6)
        gents = grid.get_entries()
        for i in range(3):
            for j in range(2):
                r1 = SurroundingRectangle(dcol.get_entries()[i], color=HIGHLIGHT, buff=0.1, stroke_width=3)
                r2 = SurroundingRectangle(arow.get_entries()[j], color=HIGHLIGHT, buff=0.1, stroke_width=3)
                self.add(r1, r2)
                self.play(FadeIn(gents[i * 2 + j], scale=1.2), run_time=0.35)
                self.remove(r1, r2)
        self.wait(2.5)



# The three scenes below follow Mitesh Khapra, CS7015 lecture 4.4,
# "Backpropagation (Intuition)": the chain for a weight at the far end of a
# deep but thin network, the loss interrogating a wide network layer by
# layer, and the chain rule read back as that interrogation.


def fit(m, w=9.2):
    """Shrink a line only if it would run off the 10-unit frame."""
    if m.width > w:
        m.scale(w / m.width)
    return m


def keep_in_frame(m, margin=0.3):
    """Nudge a mobject back inside the frame if next_to pushed it out."""
    half = config.frame_width / 2 - margin
    if m.get_left()[0] < -half:
        m.shift(RIGHT * (-half - m.get_left()[0]))
    if m.get_right()[0] > half:
        m.shift(LEFT * (m.get_right()[0] - half))
    return m


class LongChainCompress(Scene):
    def construct(self):
        # Deep but thin, drawn left to right with the cost at the end. The
        # first edge is the subject: w^(1) is as far from C as a weight gets.
        yn = 1.75
        xs = [-4.0, -2.3, -0.6, 1.7]
        n_in, n_a1, n_a2, n_aL = [node(np.array([x, yn, 0]), r=0.26, color=c, sw=2.5)
                                  for x, c in zip(xs, [INK_FAINT, A_COL, INK_DIM, INK_DIM])]
        bc = box(np.array([3.5, yn, 0]), 1.0, 0.65, D_COL)
        tc = tex(r"C", D_COL).move_to(bc)
        l_in = tex(r"x", INK_FAINT).next_to(n_in, UP, buff=0.12)
        l_a1 = tex(r"a^{(1)}", A_COL).next_to(n_a1, UP, buff=0.12)
        l_a2 = tex(r"a^{(2)}", INK_DIM).next_to(n_a2, UP, buff=0.12)
        l_aL = tex(r"a^{(L)}", INK_DIM).next_to(n_aL, UP, buff=0.12)

        e1 = edge(n_in.get_right(), n_a1.get_left(), A_COL, sw=4.5)
        e2 = edge(n_a1.get_right(), n_a2.get_left(), INK_DIM)
        gap = VGroup(*[Dot(np.array([0.6 + i * 0.3, yn, 0]), radius=0.045, color=INK_FAINT)
                       for i in range(3)])
        e3 = edge(np.array([1.25, yn, 0]), n_aL.get_left(), INK_DIM)
        e4 = edge(n_aL.get_right(), bc.get_left(), D_COL)
        w1 = tex(r"w^{(1)}", A_COL, bg=True).next_to(e1, DOWN, buff=0.1)
        w2 = tex(r"w^{(2)}", INK_DIM, bg=True).next_to(e2, DOWN, buff=0.1)

        net = VGroup(n_in, n_a1, n_a2, n_aL, bc, tc, l_in, l_a1, l_a2, l_aL,
                     e1, e2, gap, e3, e4, w1, w2)

        # One factor per arrow, all the way back. The gap in the middle stands
        # for the layers the picture skips; it carries no multiplication dots
        # of its own, or the run of dots reads as one long ellipsis.
        chain = MathTex(
            r"\frac{\partial C}{\partial w^{(1)}}", r"=",
            r"\frac{\partial C}{\partial a^{(L)}}", r"\cdot",
            r"\frac{\partial a^{(L)}}{\partial z^{(L)}}", r"\;\cdots\;",
            r"\frac{\partial a^{(1)}}{\partial z^{(1)}}", r"\cdot",
            r"\frac{\partial z^{(1)}}{\partial w^{(1)}}", font_size=F)
        chain[0].set_color(D_COL)
        chain[8].set_color(A_COL)
        fit(chain).move_to(np.array([0, 0.3, 0]))

        self.add(net)
        self.wait(2.0)
        self.play(FadeIn(chain, shift=UP * 0.15), run_time=1.2)
        self.wait(3.0)

        tail = VGroup(*chain[2:7])
        brace = Brace(tail, DOWN, buff=0.12, color=HIGHLIGHT)
        b_lbl = MathTex(r"\text{all of this is just}", r"\;",
                        r"\frac{\partial C}{\partial a^{(1)}}",
                        font_size=F, color=HIGHLIGHT)
        keep_in_frame(b_lbl.next_to(brace, DOWN, buff=0.2))
        self.play(Create(brace), FadeIn(b_lbl), run_time=1.3)
        self.wait(3.0)

        # Collapse the tail. Two factors left: one already computed, one local.
        comp = MathTex(r"\frac{\partial C}{\partial w^{(1)}}", r"\;=\;",
                       r"\frac{\partial C}{\partial a^{(1)}}", r"\;\cdot\;",
                       r"\frac{\partial a^{(1)}}{\partial w^{(1)}}", font_size=F + 2)
        comp[0].set_color(D_COL)
        comp[2].set_color(D_COL)
        comp[4].set_color(A_COL)
        comp.move_to(np.array([0, 0.05, 0]))
        self.play(FadeOut(brace), FadeOut(b_lbl), FadeOut(chain), run_time=0.8)
        self.play(FadeIn(comp, scale=1.05), run_time=1.1)
        self.wait(1.2)

        hb = SurroundingRectangle(comp[2], color=HIGHLIGHT, buff=0.14, stroke_width=3)
        hl = tex(r"\text{computed once, on the way back}", HIGHLIGHT)
        fit(hl).move_to(np.array([0, -1.75, 0]))
        self.play(Create(hb), FadeIn(hl), run_time=1.2)
        self.wait(3.5)


class BlameSpreads(Scene):
    def construct(self):
        # A wide network. The question is not which neuron is wrong, it is how
        # far back the responsibility reaches: all the way, is the answer.
        cols_x = [-3.7, -1.7, 0.3, 2.3]
        ys3 = [0.8, -0.1, -1.0]
        ys2 = [0.45, -0.65]
        r = 0.22
        c_in = [node(np.array([cols_x[0], y, 0]), r=r, color=INK_FAINT, sw=2.5) for y in ys3]
        c_h1 = [node(np.array([cols_x[1], y, 0]), r=r, color=INK_DIM, sw=2.5) for y in ys3]
        c_h2 = [node(np.array([cols_x[2], y, 0]), r=r, color=INK_DIM, sw=2.5) for y in ys3]
        c_out = [node(np.array([cols_x[3], y, 0]), r=r, color=INK_DIM, sw=2.5) for y in ys2]
        x_lbls = VGroup(*[tex(rf"x_{i + 1}", INK_FAINT).next_to(n, LEFT, buff=0.16)
                          for i, n in enumerate(c_in)])

        def bundle(left, right):
            return VGroup(*[Line(a.get_right(), b.get_left(), color=INK_FAINT, stroke_width=1.6)
                            for a in left for b in right])

        b1, b2, b3 = bundle(c_in, c_h1), bundle(c_h1, c_h2), bundle(c_h2, c_out)
        # No background plate on these: a plate recolours with the label when
        # the blame reaches it and swallows the text.
        w1 = tex(r"W^{(1)}", A_COL).move_to(np.array([-2.7, 1.55, 0]))
        w2 = tex(r"W^{(2)}", A_COL).move_to(np.array([-0.7, 1.55, 0]))
        w3 = tex(r"W^{(3)}", A_COL).move_to(np.array([1.3, 1.55, 0]))

        bc = box(np.array([4.0, 1.55, 0]), 1.0, 0.62, D_COL)
        tc = tex(r"C", D_COL).move_to(bc)
        to_c = VGroup(*[Line(n.get_right(), bc.get_bottom(), color=INK_FAINT, stroke_width=1.6)
                        for n in c_out])

        net = VGroup(b1, b2, b3, to_c, *c_in, *c_h1, *c_h2, *c_out,
                     x_lbls, w1, w2, w3, bc, tc)
        self.add(net)

        say = fit(tex(r"\text{forward pass done}", INK_DIM)).move_to(np.array([0, -2.3, 0]))
        self.add(say)
        self.wait(1.5)

        def line(text, color=INK_DIM):
            nonlocal say
            new = fit(tex(rf"\text{{{text}}}", color)).move_to(np.array([0, -2.3, 0]))
            self.play(FadeOut(say), FadeIn(new), run_time=0.6)
            say = new

        # Stroke only: these circles are filled with the background colour so
        # the lines behind them are hidden, and set_color would fill them too.
        def light(mobs, width=3.2):
            return [m.animate.set_stroke(color=HIGHLIGHT, width=width) for m in mobs]

        line(r"and $C$ is not zero", D_COL)
        pulse = SurroundingRectangle(bc, color=D_COL, buff=0.1, stroke_width=3)
        self.play(Create(pulse), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(pulse), run_time=0.4)

        line(r"so ask the output layer what went wrong", HIGHLIGHT)
        self.play(*light(to_c, 2.6), run_time=0.8)
        self.play(*light(c_out), run_time=0.7)
        self.wait(1.5)

        for lbl, bun, col, text in [
            (w3, b3, c_h2, r"it blames $W^{(3)}$ and the layer under it"),
            (w2, b2, c_h1, r"which blames $W^{(2)}$ and the layer under it"),
            (w1, b1, None, r"which blames $W^{(1)}$, and we are at the input"),
        ]:
            line(text, HIGHLIGHT)
            self.play(lbl.animate.set_color(HIGHLIGHT), *light(bun, 2.4), run_time=0.9)
            if col is not None:
                self.play(*light(col), run_time=0.7)
            self.wait(1.4)

        line(r"every weight and every bias, in some amount", HIGHLIGHT)
        self.wait(3.5)


class TalkThroughTheChain(Scene):
    def construct(self):
        # The chain rule, read back as the conversation from the clip before.
        chain = MathTex(
            r"\frac{\partial C}{\partial w^{(1)}}", r"=",
            r"\frac{\partial C}{\partial a^{(L)}}", r"\cdot",
            r"\frac{\partial a^{(L)}}{\partial a^{(2)}}", r"\cdot",
            r"\frac{\partial a^{(2)}}{\partial a^{(1)}}", r"\cdot",
            r"\frac{\partial a^{(1)}}{\partial w^{(1)}}", font_size=F)
        chain[0].set_color(D_COL)
        fit(chain).move_to(np.array([0, 1.95, 0]))
        self.add(chain)
        self.wait(2.0)

        # The direct question, which has no answer.
        br0 = Brace(chain[0], DOWN, buff=0.12, color=INK_DIM)
        l0 = keep_in_frame(fit(tex(r"\text{ask the weight directly}", INK_DIM))
                           .next_to(br0, DOWN, buff=0.18))
        l0b = fit(tex(r"\text{the loss never sees } w^{(1)}", INK_FAINT)).move_to(
            np.array([0, -0.6, 0]))
        self.play(Create(br0), FadeIn(l0), run_time=1.0)
        self.wait(1.2)
        self.play(FadeIn(l0b), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(br0), FadeOut(l0), FadeOut(l0b), run_time=0.7)

        # One brace per factor, and a numbered line per brace. Both stay up, so
        # the last frame carries the whole conversation rather than four
        # unlabelled braces.
        steps = [
            (2, r"1.\ \text{ask the output layer}"),
            (4, r"2.\ \text{then the hidden layer below it}"),
            (6, r"3.\ \text{then the one below that}"),
            (8, r"4.\ \text{and now ask the weight}"),
        ]
        # Lay the four lines out together so the gaps are even, then reveal
        # them one at a time. Spacing one line at a time off its own height
        # leaves visibly uneven rows, since not every line has a descender.
        lines = [tex(t, HIGHLIGHT) for _, t in steps]
        block = VGroup(*lines).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        fit(block, 8.4).move_to(np.array([0, -0.95, 0]))
        block.shift(LEFT * (block.get_left()[0] + 4.35))

        prev = None
        for i, (idx, _) in enumerate(steps):
            ln = lines[i]
            br = Brace(chain[idx], DOWN, buff=0.12, color=HIGHLIGHT)
            num = tex(str(i + 1), HIGHLIGHT).next_to(br, DOWN, buff=0.1)
            anims = [Create(br), FadeIn(num), chain[idx].animate.set_color(HIGHLIGHT)]
            if prev is not None:
                pbr, pnum, pfac = prev
                anims += [pbr.animate.set_color(INK_FAINT), pnum.animate.set_color(INK_DIM),
                          pfac.animate.set_color(INK)]
            self.play(*anims, run_time=0.9)
            self.play(FadeIn(ln, shift=RIGHT * 0.15), run_time=0.6)
            self.wait(1.3)
            if prev is not None:
                self.play(lines[i - 1].animate.set_color(INK), run_time=0.3)
            prev = (br, num, chain[idx])

        # No closing line: the numbered list already is the closing line, and
        # a restatement under it only crowds the frame.
        pbr, pnum, pfac = prev
        self.play(pbr.animate.set_color(INK_FAINT), pnum.animate.set_color(INK_DIM),
                  pfac.animate.set_color(INK), lines[-1].animate.set_color(INK), run_time=0.7)
        self.wait(3.5)
