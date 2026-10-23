"""Block 4.1 clips for Acts 1, 2 and 4: shapes, the linear layer, autodiff.

Every number on screen is computed here from the formula being taught.
"""

from shared.anim.house import *
import numpy as np


def T(s, color=INK, size=MIN_FONT):
    return MathTex(s, color=color, font_size=size)


def fmt(v):
    return f"{v:g}"


def bracket(center, w, h, color=INK_DIM, arm=0.12):
    """Matrix brackets around a w x h box centred on `center`."""
    cx, cy, _ = center
    l, r, t, b = cx - w / 2, cx + w / 2, cy + h / 2, cy - h / 2
    left = VMobject(color=color, stroke_width=3).set_points_as_corners(
        [[l + arm, t, 0], [l, t, 0], [l, b, 0], [l + arm, b, 0]])
    right = VMobject(color=color, stroke_width=3).set_points_as_corners(
        [[r - arm, t, 0], [r, t, 0], [r, b, 0], [r - arm, b, 0]])
    return VGroup(left, right)


def grid_centers(center, rows, cols, cw, ch):
    cx, cy, _ = center
    return [[np.array([cx + (j - (cols - 1) / 2) * cw, cy - (i - (rows - 1) / 2) * ch, 0])
             for j in range(cols)] for i in range(rows)]


def node(name, pos, color, r=0.4, fill=BG):
    c = Circle(radius=r, color=color, stroke_width=3, fill_color=fill, fill_opacity=1).move_to(pos)
    t = T(name, color).move_to(pos)
    return VGroup(c, t)


def edge_between(a, b, color=INK_FAINT, width=3):
    ca, cb = a[0], b[0]
    d = cb.get_center() - ca.get_center()
    d = d / np.linalg.norm(d)
    return Line(ca.get_center() + d * ca.radius, cb.get_center() - d * cb.radius,
                color=color, stroke_width=width)


def flash(mob, color, width=7):
    return ShowPassingFlash(mob.copy().set_color(color).set_stroke(width=width), time_width=0.7)


# ---------------------------------------------------------------- scene 1

class CountThePairs(Scene):
    def construct(self):
        def f(x):
            return np.array([x[0] * x[1], x[1] + x[2] ** 2])

        def jac(x):
            return np.array([[x[1], x[0], 0.0], [0.0, 1.0, 2 * x[2]]])

        x0 = np.array([1.0, 2.0, 3.0])
        fx, J = f(x0), jac(x0)
        h = 1e-6  # the Jacobian must agree with finite differences
        for j in range(3):
            e = np.zeros(3); e[j] = h
            assert np.allclose((f(x0 + e) - f(x0 - e)) / (2 * h), J[:, j], atol=1e-5)

        header = T(r"f(x)=\bigl(x_1x_2,\;x_2+x_3^{2}\bigr)", INK).move_to(UP * 2.3)

        in_pos = [np.array([-3.4, y, 0]) for y in (0.9, 0.0, -0.9)]
        out_pos = [np.array([-1.2, y, 0]) for y in (0.45, -0.45)]
        in_dots = [Dot(p, radius=0.12, color=V_COLOR) for p in in_pos]
        out_dots = [Dot(p, radius=0.12, color=RESULT_COLOR) for p in out_pos]
        in_lbl = [T(rf"x_{j+1}={fmt(x0[j])}", V_COLOR).next_to(in_pos[j], LEFT, buff=0.15) for j in range(3)]
        out_lbl = [T(rf"f_{i+1}={fmt(fx[i])}", RESULT_COLOR).next_to(out_pos[i], RIGHT, buff=0.15) for i in range(2)]
        lines = {(i, j): Line(in_pos[j], out_pos[i], color=INK_FAINT, stroke_width=2.5)
                 for i in range(2) for j in range(3)}

        cw, ch = 1.05, 0.9
        gc = grid_centers(np.array([3.1, -0.05, 0]), 2, 3, cw, ch)
        gbr = bracket(np.array([3.1, -0.05, 0]), 3 * cw + 0.35, 2 * ch + 0.1)
        col_h = [T(rf"x_{j+1}", V_COLOR).move_to(gc[0][j] + UP * 0.95) for j in range(3)]
        row_h = [T(rf"f_{i+1}", RESULT_COLOR).move_to(np.array([0.8, gc[i][0][1], 0])) for i in range(2)]
        cells = {(i, j): T(fmt(J[i, j]), RESULT_COLOR).move_to(gc[i][j]) for i in range(2) for j in range(3)}

        def counter(k):
            return T(rf"\text{{pairs}}={k}", INK).move_to(np.array([-3.3, -2.3, 0]))

        cnt = counter(0)
        self.add(header, *in_dots, *out_dots, *in_lbl, *out_lbl, *lines.values(),
                 gbr, *col_h, *row_h, cnt)
        self.wait(2)

        k = 0
        for i in range(2):
            for j in range(3):
                k += 1
                new = counter(k)
                old, cnt = cnt, new
                self.play(flash(lines[(i, j)], HIGHLIGHT), run_time=0.45)
                self.play(FadeIn(cells[(i, j)], scale=1.4), FadeOut(old, run_time=0.2), FadeIn(new),
                          lines[(i, j)].animate.set_color(INK_DIM), run_time=0.5)
                self.wait(0.15)
        final = T(r"\text{pairs}=2\times3=6", HIGHLIGHT).move_to(np.array([-2.6, -2.3, 0]))
        self.play(FadeOut(cnt), FadeIn(final))
        cnt = final
        self.wait(2)

        # Collapse into the shape table.
        table_cw, table_ch = 0.95, 0.65
        cx_a, cx_b = -1.5, 2.2
        y1, y2 = 0.95, -0.95
        col_title = [T(r"n=1", INK_DIM).move_to(np.array([cx_a, 2.2, 0])),
                     T(r"n=3", INK_DIM).move_to(np.array([cx_b, 2.2, 0]))]
        row_title = [T(r"m=1", INK_DIM).move_to(np.array([-3.95, y1, 0])),
                     T(r"m=2", INK_DIM).move_to(np.array([-3.95, y2, 0]))]

        jc = grid_centers(np.array([cx_b, y2, 0]), 2, 3, table_cw, table_ch)
        jbr = bracket(np.array([cx_b, y2, 0]), 3 * table_cw + 0.2, 2 * table_ch + 0.1)
        jac_cells = VGroup(*[cells[(i, j)] for i in range(2) for j in range(3)])
        jac_lbl = T(r"\text{Jacobian}", RESULT_COLOR).move_to(np.array([cx_b, -1.95, 0]))

        fade = [header, *in_dots, *out_dots, *in_lbl, *out_lbl, *lines.values(), *col_h, *row_h, cnt]
        anims = [FadeOut(m) for m in fade] + [Transform(gbr, jbr)]
        anims += [cells[(i, j)].animate.move_to(jc[i][j]) for i in range(2) for j in range(3)]
        self.play(*anims, run_time=1.2)
        self.play(FadeIn(jac_lbl), *[FadeIn(m) for m in col_title + row_title])
        self.wait(1)

        def derived(label, text, idx, cen, color=RESULT_COLOR):
            rows = max(i for i, _ in idx) - min(i for i, _ in idx) + 1
            cols = max(j for _, j in idx) - min(j for _, j in idx) + 1
            pos = grid_centers(cen, rows, cols, table_cw, table_ch)
            nums, br = [], bracket(cen, cols * table_cw + 0.2, rows * table_ch + 0.1)
            lbl = T(text, color).move_to(cen + DOWN * (rows * table_ch / 2 + 0.38))
            r0, c0 = min(i for i, _ in idx), min(j for _, j in idx)
            anims = [FadeIn(br)]
            for (i, j) in idx:
                n = T(fmt(J[i, j]), color).move_to(pos[i - r0][j - c0])
                anims.append(TransformFromCopy(cells[(i, j)], n))
            self.play(*anims, FadeIn(lbl), run_time=1.0)
            self.wait(1.3)

        derived("g", r"\text{gradient}", [(0, 0), (0, 1), (0, 2)], np.array([cx_b, y1, 0]))
        derived("v", r"\text{velocity}", [(0, 1), (1, 1)], np.array([cx_a, y2, 0]))
        derived("s", r"\text{slope}", [(0, 1)], np.array([cx_a, y1, 0]))
        self.wait(2)


# ---------------------------------------------------------------- scene 2

class OuterProductLayer(Scene):
    def construct(self):
        W = np.array([[1.0, 0.0, 2.0], [-1.0, 3.0, 1.0]])
        x = np.array([2.0, 1.0, 3.0])
        delta = np.array([0.5, -1.0])
        z = W @ x
        gW = np.outer(delta, x)
        gx = W.T @ delta

        x_pos = [np.array([-3.5, y, 0]) for y in (1.45, 0.5, -0.45)]
        z_pos = [np.array([-1.5, y, 0]) for y in (0.95, 0.05)]
        xn = [node(fmt(x[j]), x_pos[j], V_COLOR, r=0.33) for j in range(3)]
        zn = [node(fmt(z[i]), z_pos[i], INK, r=0.33) for i in range(2)]
        xl = [T(rf"x_{j+1}", V_COLOR).next_to(x_pos[j], LEFT, buff=0.5) for j in range(3)]
        dl = [T(rf"\delta_{i+1}={fmt(delta[i])}", RESULT_COLOR).next_to(z_pos[i], RIGHT, buff=0.5) for i in range(2)]
        lines = {(i, j): Line(xn[j][0].get_center(), zn[i][0].get_center(), color=INK_FAINT, stroke_width=2.5)
                 for i in range(2) for j in range(3)}
        for (i, j), ln in lines.items():  # trim to the node outlines
            d = ln.get_vector() / ln.get_length()
            ln.put_start_and_end_on(x_pos[j] + d * 0.33, z_pos[i] - d * 0.33)

        cw, ch = 1.0, 0.9
        mc = np.array([3.1, 0.5, 0])
        gc = grid_centers(mc, 2, 3, cw, ch)
        wcells = [[T(fmt(W[i, j]), INK).move_to(gc[i][j]) for j in range(3)] for i in range(2)]
        wbr = bracket(mc, 3 * cw + 0.3, 2 * ch + 0.1)
        wlbl = T(r"W", INK).move_to(mc + UP * 1.2)

        self.add(*lines.values(), *xn, *zn, *xl, *dl, wbr, wlbl, *[c for r in wcells for c in r])
        self.wait(2)

        # Beat 1: nudge one weight, w_12.
        i0, j0 = 0, 1
        l1 = T(rf"z_1\text{{ moves by }}\epsilon\,x_2={fmt(x[j0])}\epsilon", INK).move_to(np.array([-0.9, -1.5, 0]))
        l2 = T(rf"L\text{{ moves by }}\epsilon\,\delta_1x_2={fmt(delta[i0] * x[j0])}\epsilon", RESULT_COLOR).move_to(np.array([-0.9, -2.2, 0]))
        box = SurroundingRectangle(wcells[i0][j0], color=HIGHLIGHT, buff=0.12, stroke_width=3)
        self.play(Create(box), lines[(i0, j0)].animate.set_color(HIGHLIGHT).set_stroke(width=6),
                  Indicate(xn[j0][1], color=HIGHLIGHT, scale_factor=1.3), run_time=1.0)
        self.play(FadeIn(l1), Indicate(zn[i0][1], color=HIGHLIGHT, scale_factor=1.3), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(l2), run_time=0.8)
        self.wait(2)

        # Beat 2: the whole gradient grid, delta_i x_j.
        gl = T(r"\partial L/\partial W", RESULT_COLOR).move_to(mc + UP * 1.2)
        gcells = [[T(fmt(gW[i, j]), RESULT_COLOR).move_to(gc[i][j]) for j in range(3)] for i in range(2)]
        self.play(*[FadeOut(m) for m in [box, l1, l2, wlbl] + [c for r in wcells for c in r]],
                  lines[(i0, j0)].animate.set_color(INK_FAINT).set_stroke(width=2.5),
                  FadeIn(gl), run_time=0.8)
        for i in range(2):
            for j in range(3):
                self.play(flash(lines[(i, j)], HIGHLIGHT), Indicate(xn[j][1], color=HIGHLIGHT, scale_factor=1.3),
                          Indicate(dl[i], color=HIGHLIGHT, scale_factor=1.1), run_time=0.5)
                self.play(FadeIn(gcells[i][j], scale=1.4), lines[(i, j)].animate.set_color(INK_DIM), run_time=0.4)
        f1 = MathTex(r"\frac{\partial L}{\partial W}=", r"\delta", r"x^{\top}", font_size=MIN_FONT)
        f1[0].set_color(RESULT_COLOR); f1[1].set_color(RESULT_COLOR); f1[2].set_color(V_COLOR)
        f1.move_to(np.array([-0.9, -1.85, 0]))
        self.play(FadeIn(f1))
        self.wait(2.5)

        # Beat 3: delta travels back along the same lines.
        self.play(FadeOut(f1), *[l.animate.set_color(INK_FAINT) for l in lines.values()], run_time=0.6)
        arith = MathTex(r"\partial L/\partial x_1=", rf"{fmt(delta[0])}\cdot{fmt(W[0,0])}+({fmt(delta[1])})({fmt(W[1,0])})={fmt(gx[0])}",
                        font_size=MIN_FONT, color=RESULT_COLOR).move_to(np.array([-0.9, -1.85, 0]))
        for j in range(3):
            dots = []
            for i in range(2):
                d = Dot(z_pos[i], radius=0.1, color=RESULT_COLOR)
                dots.append(d)
            self.add(*dots)
            newn = T(fmt(gx[j]), RESULT_COLOR).move_to(x_pos[j])
            self.play(*[d.animate.move_to(x_pos[j]) for d in dots],
                      *[lines[(i, j)].animate.set_color(RESULT_COLOR) for i in range(2)], run_time=0.9)
            self.remove(*dots)
            self.play(FadeOut(xn[j][1]), FadeIn(newn), xn[j][0].animate.set_stroke(color=RESULT_COLOR), run_time=0.4)
            if j == 0:
                self.play(FadeIn(arith))
                self.wait(1.5)
            self.play(*[lines[(i, j)].animate.set_color(INK_DIM) for i in range(2)], run_time=0.3)
        fa = MathTex(r"\frac{\partial L}{\partial W}=", r"\delta", r"x^{\top}", font_size=MIN_FONT)
        fa[0].set_color(RESULT_COLOR); fa[1].set_color(RESULT_COLOR); fa[2].set_color(V_COLOR)
        fb = MathTex(r"\frac{\partial L}{\partial x}=", r"W^{\top}", r"\delta", font_size=MIN_FONT)
        fb[0].set_color(RESULT_COLOR); fb[1].set_color(INK); fb[2].set_color(RESULT_COLOR)
        fa.move_to(np.array([-2.9, -1.85, 0])); fb.move_to(np.array([1.9, -1.85, 0]))
        self.play(FadeOut(arith))
        self.play(FadeIn(fa), FadeIn(fb))
        self.wait(2.5)


# ---------------------------------------------------------------- scene 3

class AutodiffWorkedGraph(Scene):
    def construct(self):
        xv, yv = 2.0, 3.0
        uv = xv + yv
        fv = uv * yv
        fbar = 1.0
        ubar = fbar * yv
        xbar = ubar * 1.0
        ycon1, ycon2 = fbar * uv, ubar * 1.0
        ybar = ycon1 + ycon2
        # check against f = xy + y^2
        assert fv == xv * yv + yv ** 2 and xbar == yv and ybar == xv + 2 * yv

        px, py, pu, pf = (np.array(p + (0,)) for p in [(-3.2, 1.2), (-3.2, -0.9), (-0.5, 1.2), (2.0, 0.1)])
        nx, ny = node("x", px, V_COLOR), node("y", py, V_COLOR)
        nu, nf = node("u", pu, INK), node("f", pf, INK)
        e_xu = edge_between(nx, nu)
        e_yu = edge_between(ny, nu)
        e_uf = edge_between(nu, nf)
        e_yf = edge_between(ny, nf)
        edges = [e_xu, e_yu, e_uf, e_yf]

        def above(n, s, color):
            return T(s, color).next_to(n[0], UP, buff=0.12)

        def below(n, s, color):
            return T(s, color).next_to(n[0], DOWN, buff=0.12)

        fx_, fy_ = above(nx, fmt(xv), V_COLOR), above(ny, fmt(yv), V_COLOR)
        fu_, ff_ = above(nu, fmt(uv), V_COLOR), above(nf, fmt(fv), V_COLOR)
        tag_f = T(r"\text{forward}", V_COLOR).move_to(np.array([3.4, 2.2, 0]))
        tag_b = T(r"\text{backward}", RESULT_COLOR).move_to(np.array([3.4, 2.2, 0]))
        fy_.next_to(ny[0], LEFT, buff=0.12)  # keep clear of the y -> u edge
        fx_.next_to(nx[0], LEFT, buff=0.12)

        self.add(*edges, nx, ny, nu, nf, fx_, fy_, tag_f)
        self.wait(2)

        def travel(edge, color, rev=False, t=0.7):
            p0, p1 = (edge.get_end(), edge.get_start()) if rev else (edge.get_start(), edge.get_end())
            d = Dot(p0, radius=0.1, color=color)
            self.add(d)
            return d, d.animate.move_to(p1)

        # forward pass
        d1, a1 = travel(e_xu, V_COLOR)
        d2, a2 = travel(e_yu, V_COLOR)
        self.play(a1, a2, run_time=0.8)
        self.remove(d1, d2)
        self.play(FadeIn(fu_), run_time=0.5)
        d1, a1 = travel(e_uf, V_COLOR)
        d2, a2 = travel(e_yf, V_COLOR)
        self.play(a1, a2, run_time=0.8)
        self.remove(d1, d2)
        self.play(FadeIn(ff_), run_time=0.5)
        self.wait(1.5)

        # seed
        self.play(FadeOut(tag_f), FadeIn(tag_b), *[e.animate.set_color(INK_FAINT) for e in edges])
        bf = below(nf, rf"\bar f={fmt(fbar)}", RESULT_COLOR)
        self.play(FadeIn(bf, scale=1.3), nf[0].animate.set_stroke(color=RESULT_COLOR))
        self.wait(1.5)

        def mid_label(edge, s, color, shift):
            return T(s, color).move_to(edge.get_center() + shift)

        l_uf = mid_label(e_uf, rf"\times y={fmt(yv)}", RESULT_COLOR, np.array([0.9, 0.6, 0]))
        l_yf = mid_label(e_yf, rf"\times u={fmt(uv)}", RESULT_COLOR, np.array([0.2, -0.6, 0]))
        l_xu = mid_label(e_xu, r"\times 1", RESULT_COLOR, UP * 0.45)
        l_yu = mid_label(e_yu, r"\times 1", RESULT_COLOR, np.array([0.75, -0.25, 0]))

        # f -> u
        d, a = travel(e_uf, RESULT_COLOR, rev=True)
        self.play(a, e_uf.animate.set_color(RESULT_COLOR), FadeIn(l_uf), run_time=1.0)
        self.remove(d)
        bu = below(nu, rf"\bar u={fmt(ubar)}", RESULT_COLOR).shift(RIGHT * 0.6)
        self.play(FadeIn(bu, scale=1.3), nu[0].animate.set_stroke(color=RESULT_COLOR))
        self.wait(1)

        # f -> y: contribution 5
        ysum = MathTex(r"\bar y=", fmt(ycon1), "+", fmt(ycon2), "=", fmt(ybar), font_size=MIN_FONT, color=RESULT_COLOR)
        ysum.move_to(np.array([-2.5, -1.8, 0]))
        ysum_bar = T(r"\bar y", RESULT_COLOR)
        d, a = travel(e_yf, RESULT_COLOR, rev=True)
        self.play(a, e_yf.animate.set_color(RESULT_COLOR), FadeIn(l_yf), run_time=1.0)
        self.remove(d)
        self.play(FadeIn(ysum[0:2], scale=1.3))
        self.wait(1)

        # u -> x
        d, a = travel(e_xu, RESULT_COLOR, rev=True)
        self.play(a, e_xu.animate.set_color(RESULT_COLOR), FadeIn(l_xu), run_time=0.9)
        self.remove(d)
        bx = T(rf"\bar x={fmt(xbar)}", RESULT_COLOR).next_to(nx[0], UP, buff=0.12)
        self.play(FadeIn(bx, scale=1.3), nx[0].animate.set_stroke(color=RESULT_COLOR))
        self.wait(1)

        # u -> y: contribution 3, then they add
        d, a = travel(e_yu, RESULT_COLOR, rev=True)
        self.play(a, e_yu.animate.set_color(RESULT_COLOR), FadeIn(l_yu), run_time=0.9)
        self.remove(d)
        self.play(FadeIn(ysum[2:4]), run_time=0.6)
        self.wait(1)
        self.play(FadeIn(ysum[4:]), ny[0].animate.set_stroke(color=RESULT_COLOR), run_time=0.8)
        self.play(Indicate(ysum[5], color=HIGHLIGHT, scale_factor=1.3), run_time=0.8)
        self.wait(1.5)

        # check against f = xy + y^2
        c0 = T(r"f=xy+y^{2}", INK).move_to(np.array([3.4, 2.2, 0]))
        def checked(s, y):
            m = MathTex(s, r"\;\checkmark", font_size=MIN_FONT, color=INK)
            m[1].set_color(HIGHLIGHT)
            return m.move_to(np.array([3.1, y, 0]))
        c1 = checked(rf"\partial f/\partial x={fmt(yv)}", -1.5)
        c2 = checked(rf"\partial f/\partial y={fmt(xv + 2 * yv)}", -2.3)
        self.play(FadeOut(tag_b), FadeIn(c0))
        self.wait(1)
        self.play(FadeIn(c1))
        self.play(FadeIn(c2))
        self.wait(2.5)


# ---------------------------------------------------------------- scene 4

class ForwardVsReverse(Scene):
    def construct(self):
        in_pos = [np.array([-3.9, y, 0]) for y in (1.3, 0.1, -1.1)]
        h_pos = [np.array([-1.6, y, 0]) for y in (0.7, -0.5)]
        l_pos = np.array([0.7, 0.1, 0])
        nin = [node(rf"x_{j+1}", in_pos[j], V_COLOR, r=0.42) for j in range(3)]
        nh = [node(rf"h_{i+1}", h_pos[i], INK, r=0.42) for i in range(2)]
        nl = node("L", l_pos, INK, r=0.42)
        e_ih = {(j, i): edge_between(nin[j], nh[i]) for j in range(3) for i in range(2)}
        e_hl = {i: edge_between(nh[i], nl) for i in range(2)}
        rows = [np.array([3.5, in_pos[j][1], 0]) for j in range(3)]

        def grad_lbl(j, color):
            return T(rf"\partial L/\partial x_{j+1}", color).move_to(rows[j])

        def counter(k, color):
            return T(rf"\text{{sweeps}}={k}", color).move_to(np.array([-3.0, -2.3, 0]))

        tag_f = T(r"\text{forward mode}", V_COLOR).move_to(np.array([-1.6, 2.3, 0]))
        tag_r = T(r"\text{reverse mode}", RESULT_COLOR).move_to(np.array([-1.6, 2.3, 0]))
        cnt = counter(0, V_COLOR)
        cur = [cnt]
        col = [V_COLOR]

        def swap(k):
            old = cur[0]
            new = counter(k, col[0])
            cur[0] = new
            return [FadeOut(old), FadeIn(new)]
        self.add(*e_ih.values(), *e_hl.values(), *nin, *nh, nl, tag_f, cnt)
        self.wait(2)

        # forward mode: one sweep per input
        results = []
        for j in range(3):
            self.play(Indicate(nin[j], color=HIGHLIGHT, scale_factor=1.2), run_time=0.4)
            self.play(*[flash(e_ih[(j, i)], V_COLOR) for i in range(2)], run_time=0.8)
            self.play(*[flash(e_hl[i], V_COLOR) for i in range(2)], run_time=0.8)
            g = grad_lbl(j, V_COLOR)
            results.append(g)
            self.play(FadeIn(g, scale=1.2), *swap(j + 1), run_time=0.6)
            self.wait(0.4)
        self.wait(1.5)

        # reverse mode: one sweep from L
        self.play(*[FadeOut(g) for g in results], FadeOut(tag_f), FadeOut(cur[0]), run_time=0.6)
        col[0] = RESULT_COLOR
        cnt = counter(0, RESULT_COLOR); cur[0] = cnt
        self.play(FadeIn(tag_r), FadeIn(cnt), run_time=0.6)
        self.play(Indicate(nl, color=HIGHLIGHT, scale_factor=1.2), run_time=0.4)
        self.play(*[flash(e_hl[i], RESULT_COLOR) for i in range(2)], run_time=0.8)
        self.play(*[flash(e_ih[k], RESULT_COLOR) for k in e_ih], run_time=0.9)
        rg = [grad_lbl(j, RESULT_COLOR) for j in range(3)]
        self.play(*[FadeIn(g, scale=1.2) for g in rg], *swap(1), run_time=0.6)
        self.wait(2.5)

        # scale it up
        everything = [*e_ih.values(), *e_hl.values(), *nin, *nh, nl, *rg, tag_r, cur[0]]
        self.play(*[FadeOut(m) for m in everything], run_time=0.8)
        l0 = T(r"10^{6}\text{ inputs, }1\text{ output}", INK).move_to(UP * 1.4)
        l1 = MathTex(r"\text{forward: }", r"10^{6}\text{ sweeps}", font_size=MIN_FONT)
        l1[0].set_color(INK_DIM); l1[1].set_color(V_COLOR)
        l2 = MathTex(r"\text{reverse: }", r"1\text{ sweep}", font_size=MIN_FONT)
        l2[0].set_color(INK_DIM); l2[1].set_color(RESULT_COLOR)
        l1.move_to(UP * 0.1); l2.move_to(DOWN * 0.9)
        l1.align_to(l2, LEFT) if False else None
        self.play(FadeIn(l0))
        self.wait(1)
        self.play(FadeIn(l1))
        self.wait(1)
        self.play(FadeIn(l2))
        self.wait(2.5)
