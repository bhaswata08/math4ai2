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
        chain = MathTex(
            r"\frac{\partial C}{\partial w^{(L)}}", r"=",
            r"\frac{\partial z^{(L)}}{\partial w^{(L)}}", r"\quad\cdot\quad",
            r"\frac{\partial a^{(L)}}{\partial z^{(L)}}", r"\quad\cdot\quad",
            r"\frac{\partial C}{\partial a^{(L)}}", font_size=F)
        chain[0].set_color(INK)
        chain[2].set_color(A_COL)
        chain[4].set_color(S_COL)
        chain[6].set_color(D_COL)
        chain.move_to(np.array([0, 1.75, 0]))
        self.add(chain)
        self.wait(1.5)

        evals = [
            (2, r"a^{(L-1)}", A_COL),
            (4, r"\sigma'(z^{(L)})", S_COL),
            (6, r"2(a^{(L)} - y)", D_COL),
        ]
        shown = []
        for idx, s, col in evals:
            x = chain[idx].get_x()
            arr = Arrow(np.array([x, 1.05, 0]), np.array([x, 0.35, 0]), buff=0.05, color=col, stroke_width=3,
                        max_tip_length_to_length_ratio=0.25)
            ev = tex(s, col, size=F).move_to(np.array([x, -0.1, 0]))
            self.play(Create(arr), run_time=0.7)
            self.play(FadeIn(ev, shift=DOWN * 0.2), run_time=0.7)
            self.wait(0.7)
            shown.append(ev)

        final = MathTex(r"\frac{\partial C}{\partial w^{(L)}}", r"=", r"a^{(L-1)}", r"\cdot",
                        r"\sigma'(z^{(L)})", r"\cdot", r"2(a^{(L)} - y)", font_size=F + 2)
        final[0].set_color(INK)
        final[2].set_color(A_COL)
        final[4].set_color(S_COL)
        final[6].set_color(D_COL)
        final.move_to(np.array([0, -1.65, 0]))
        fbox = SurroundingRectangle(final, color=D_COL, buff=0.16, stroke_width=2.5)
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
        self.wait(1.5)

        reused = VGroup(eq[4], eq[5], eq[6])
        brace = Brace(reused, DOWN, buff=0.1, color=HIGHLIGHT)
        r_lbl = tex(r"\text{reused from layer } L", HIGHLIGHT).next_to(brace, DOWN, buff=0.12)
        self.play(Create(brace), FadeIn(r_lbl), run_time=1.0)
        self.wait(1.5)
        d_def = MathTex(r"\boldsymbol{\delta}^{(L)}", r"=", r"\frac{\partial C}{\partial z^{(L)}}", r"=",
                        r"\sigma'(z^{(L)})", r"\cdot", r"2(a^{(L)} - y)", font_size=F)
        d_def[0].set_color(D_COL)
        d_def[2].set_color(D_COL)
        d_def[4].set_color(S_COL)
        d_def[6].set_color(D_COL)
        d_def.move_to(np.array([0.0, -1.55, 0]))
        self.play(FadeOut(r_lbl), run_time=0.4)
        self.play(FadeIn(d_def), run_time=0.8)
        self.wait(2.5)

        # Pull the reused product out as delta^{(L)}.
        self.play(FadeOut(brace), FadeOut(d_def), FadeOut(eq), run_time=0.6)
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
        self.play(FadeIn(eq_a), FadeIn(eq_w), run_time=0.8)
        boxes = VGroup(SurroundingRectangle(eq_a[4], color=HIGHLIGHT, buff=0.1, stroke_width=3),
                       SurroundingRectangle(eq_w[4], color=HIGHLIGHT, buff=0.1, stroke_width=3))
        tw = tex(r"\text{one } \delta^{(L)}\text{, used twice}", HIGHLIGHT).move_to(np.array([0, -2.1, 0]))
        self.play(Create(boxes), FadeIn(tw), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(boxes), FadeOut(tw), run_time=0.4)

        # Backward sweep along the chain.
        cb = SurroundingRectangle(bc, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(cb), run_time=0.3)
        self.play(FadeOut(cb), run_time=0.2)
        prev, pts = bc, [n_l, n_l1, n_l2]
        for tgt in pts:
            pulse = Arrow(prev.get_left(), tgt.get_right(), buff=0.08, color=HIGHLIGHT, stroke_width=5,
                          max_tip_length_to_length_ratio=0.22)
            fl = SurroundingRectangle(tgt, color=HIGHLIGHT, buff=0.08, stroke_width=3)
            self.play(Create(pulse), run_time=0.35)
            self.play(Create(fl), FadeOut(pulse), run_time=0.3)
            self.play(FadeOut(fl), run_time=0.2)
            prev = tgt
        self.wait(0.3)

        # Next layer back: delta^{(L)} reaches every earlier weight.
        self.play(FadeOut(eq_a), FadeOut(eq_w), run_time=0.5)
        e1 = MathTex(r"\frac{\partial C}{\partial w^{(L-1)}}", r"=", r"a^{(L-2)}", r"\cdot",
                     r"\sigma'(z^{(L-1)})", r"\cdot", r"\frac{\partial C}{\partial a^{(L-1)}}", font_size=F)
        e2 = MathTex(r"=", r"a^{(L-2)}", r"\cdot", r"\sigma'(z^{(L-1)})", r"\cdot", r"w^{(L)}", r"\cdot",
                     r"\boldsymbol{\delta}^{(L)}", font_size=F)
        e1[0].set_color(D_COL); e1[2].set_color(A_COL); e1[4].set_color(S_COL); e1[6].set_color(D_COL)
        e2[1].set_color(A_COL); e2[3].set_color(S_COL); e2[5].set_color(A_COL); e2[7].set_color(D_COL)
        e1.move_to(np.array([0, -0.3, 0]))
        e2.next_to(e1, DOWN, buff=0.45).align_to(e1[1], LEFT)
        fb = SurroundingRectangle(VGroup(e1, e2), color=D_COL, buff=0.2, stroke_width=2.5)
        self.play(FadeIn(e1), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(e2), FadeIn(fb), run_time=0.8)
        self.wait(3.0)


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
