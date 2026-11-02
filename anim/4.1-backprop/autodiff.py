"""Block 4.1 clips for Acts 1, 2 and 4: shapes, the linear layer, autodiff.

Every number on screen is computed here from the formula being taught.
"""

from shared.anim.house import *
from types import SimpleNamespace
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
        out_pos = [np.array([-1.65, y, 0]) for y in (0.45, -0.45)]
        in_dots = [Dot(p, radius=0.12, color=V_COLOR) for p in in_pos]
        out_dots = [Dot(p, radius=0.12, color=RESULT_COLOR) for p in out_pos]
        in_lbl = [T(rf"x_{j+1}={fmt(x0[j])}", V_COLOR).next_to(in_pos[j], LEFT, buff=0.15) for j in range(3)]
        out_lbl = [T(rf"f_{i+1}={fmt(fx[i])}", RESULT_COLOR).next_to(out_pos[i], RIGHT, buff=0.15) for i in range(2)]
        lines = {(i, j): Line(in_pos[j], out_pos[i], color=INK_FAINT, stroke_width=2.5)
                 for i in range(2) for j in range(3)}

        # Name every slot before filling it, so the shape reads from the first
        # frame. A stacked fraction keeps a name inside one cell; the cell is
        # sized from the name rather than from the number that replaces it.
        slot = {(i, j): T(rf"\frac{{\partial f_{i+1}}}{{\partial x_{j+1}}}", INK_DIM, 52)
                for i in range(2) for j in range(3)}
        cw = max(m.width for m in slot.values()) + 0.24
        ch = max(m.height for m in slot.values()) + 0.3
        gcen = np.array([0, -0.05, 0])
        gw = 3 * cw + 0.35
        gc = grid_centers(gcen, 2, 3, cw, ch)
        gbr = bracket(gcen, gw, 2 * ch + 0.1)
        for (i, j), m in slot.items():
            m.move_to(gc[i][j])
        col_h = [T(rf"x_{j+1}", V_COLOR).move_to(gc[0][j] + UP * (ch / 2 + 0.55)) for j in range(3)]
        row_h = [T(rf"f_{i+1}", RESULT_COLOR).move_to(
            np.array([gcen[0] - gw / 2 - 0.35, gc[i][0][1], 0])) for i in range(2)]

        # The network and the grid are sized by their own contents, so let them
        # share the frame instead of pinning either to a guessed x.
        net = VGroup(*in_dots, *out_dots, *in_lbl, *out_lbl, *lines.values())
        grid = VGroup(gbr, *col_h, *row_h, *slot.values())
        VGroup(net, grid).arrange(RIGHT, buff=0.5).move_to(np.array([0, -0.05, 0]))
        cells = {(i, j): T(fmt(J[i, j]), RESULT_COLOR).move_to(slot[(i, j)].get_center())
                 for i in range(2) for j in range(3)}

        def counter(k):
            return T(rf"\text{{pairs}}={k}", INK).move_to(np.array([-3.3, -2.3, 0]))

        cnt = counter(0)
        self.add(header, *in_dots, *out_dots, *in_lbl, *out_lbl, *lines.values(),
                 gbr, *col_h, *row_h, *slot.values(), cnt)
        self.wait(2)

        k = 0
        for i in range(2):
            for j in range(3):
                k += 1
                new = counter(k)
                old, cnt = cnt, new
                self.play(flash(lines[(i, j)], HIGHLIGHT), run_time=0.45)
                self.play(FadeIn(cells[(i, j)], scale=1.4), FadeOut(slot[(i, j)]),
                          FadeOut(old, run_time=0.2), FadeIn(new),
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
        jac_lbl = VGroup(T(r"\text{Jacobian}", RESULT_COLOR), T(r"J_f", INK_DIM, 34)) \
            .arrange(RIGHT, buff=0.25).move_to(np.array([cx_b, -1.95, 0]))

        fade = [header, *in_dots, *out_dots, *in_lbl, *out_lbl, *lines.values(), *col_h, *row_h, cnt]
        anims = [FadeOut(m) for m in fade] + [Transform(gbr, jbr)]
        anims += [cells[(i, j)].animate.move_to(jc[i][j]) for i in range(2) for j in range(3)]
        self.play(*anims, run_time=1.2)
        self.play(FadeIn(jac_lbl), *[FadeIn(m) for m in col_title + row_title])
        self.wait(1)

        # Each case is the Jacobian restricted: a row, a column, or one entry.
        # The name alone does not say which, so carry the symbol beside it.
        def derived(sym, text, idx, cen, color=RESULT_COLOR):
            rows = max(i for i, _ in idx) - min(i for i, _ in idx) + 1
            cols = max(j for _, j in idx) - min(j for _, j in idx) + 1
            pos = grid_centers(cen, rows, cols, table_cw, table_ch)
            nums, br = [], bracket(cen, cols * table_cw + 0.2, rows * table_ch + 0.1)
            lbl = VGroup(T(text, color), T(sym, INK_DIM, 34)).arrange(RIGHT, buff=0.25)
            lbl.move_to(cen + DOWN * (rows * table_ch / 2 + 0.42))
            r0, c0 = min(i for i, _ in idx), min(j for _, j in idx)
            anims = [FadeIn(br)]
            for (i, j) in idx:
                n = T(fmt(J[i, j]), color).move_to(pos[i - r0][j - c0])
                anims.append(TransformFromCopy(cells[(i, j)], n))
            self.play(*anims, FadeIn(lbl), run_time=1.0)
            self.wait(1.3)

        # Row 1 of J is the gradient of f_1, lying on its side.
        derived(r"\nabla f_1^{\top}", r"\text{gradient}", [(0, 0), (0, 1), (0, 2)],
                np.array([cx_b, y1, 0]))
        derived(r"\partial f/\partial x_2", r"\text{velocity}", [(0, 1), (1, 1)],
                np.array([cx_a, y2, 0]))
        derived(r"\partial f_1/\partial x_2", r"\text{slope}", [(0, 1)],
                np.array([cx_a, y1, 0]))
        self.wait(2)


# ---------------------------------------------------------------- scene 2
# Two clips, one picture. Part 1 derives a single entry of dL/dW by hand;
# part 2 opens on part 1's last frame, fills the rest of the grid and sends
# delta back to x. Both build the stage with _layer_stage, so the geometry is
# identical and the second clip reads as the first one resuming.

W_L = np.array([[1.0, 0.0, 2.0], [-1.0, 3.0, 1.0]])
X_L = np.array([2.0, 1.0, 3.0])
D_L = np.array([0.5, -1.0])
I0, J0 = 0, 2            # the entry part 1 works through by hand
MC = np.array([3.1, 0.8, 0])
CW, CH = 1.0, 0.9


def _layer_stage():
    """The linear-layer picture: inputs, outputs, the deltas and W."""
    W, x, delta = W_L, X_L, D_L
    s = SimpleNamespace(W=W, x=x, delta=delta, z=W @ x,
                        gW=np.outer(delta, x), gx=W.T @ delta)

    # The diagram sits in the top half; the derivation needs four lines
    # below it, and the house frame is only 5.625 units tall.
    s.x_pos = [np.array([-3.5, y, 0]) for y in (1.75, 0.8, -0.15)]
    s.z_pos = [np.array([-1.5, y, 0]) for y in (1.25, 0.35)]
    s.xn = [node(fmt(x[j]), s.x_pos[j], V_COLOR, r=0.33) for j in range(3)]
    s.zn = [node(fmt(s.z[i]), s.z_pos[i], INK, r=0.33) for i in range(2)]
    s.xl = [T(rf"x_{j+1}", V_COLOR).next_to(s.x_pos[j], LEFT, buff=0.5) for j in range(3)]
    s.dl = [T(rf"\delta_{i+1}={fmt(delta[i])}", RESULT_COLOR).next_to(s.z_pos[i], RIGHT, buff=0.5)
            for i in range(2)]
    s.lines = {(i, j): Line(s.x_pos[j], s.z_pos[i], color=INK_FAINT, stroke_width=2.5)
               for i in range(2) for j in range(3)}
    for (i, j), ln in s.lines.items():  # trim to the node outlines
        d = ln.get_vector() / ln.get_length()
        ln.put_start_and_end_on(s.x_pos[j] + d * 0.33, s.z_pos[i] - d * 0.33)

    s.gc = grid_centers(MC, 2, 3, CW, CH)
    s.wcells = [[T(fmt(W[i, j]), INK).move_to(s.gc[i][j]) for j in range(3)] for i in range(2)]
    s.wbr = bracket(MC, 3 * CW + 0.3, 2 * CH + 0.1)
    s.wlbl = T(r"W", INK).move_to(MC + DOWN * 1.4)  # below: the column labels own the top
    # Row i of W feeds z_i, column j carries x_j. Without these the boxed
    # entry is just one of six numbers.
    s.wcol = [T(rf"x_{j+1}", V_COLOR, size=34).move_to(np.array([s.gc[0][j][0], MC[1] + 1.2, 0]))
              for j in range(3)]
    s.wrow = [T(rf"z_{i+1}", INK_DIM, size=34).move_to(np.array([MC[0] - 2.1, s.gc[i][0][1], 0]))
              for i in range(2)]
    s.statics = [*s.lines.values(), *s.xn, *s.zn, *s.xl, *s.dl, s.wbr, s.wlbl,
                 *s.wcol, *s.wrow, *[c for r in s.wcells for c in r]]
    return s


def _worked_entry(s):
    """The four lines of part 1's derivation, and the box round the weight."""
    wname = rf"w_{{{I0+1}{J0+1}}}"
    terms = "+".join(rf"w_{{{I0+1}{j+1}}}x_{j+1}" for j in range(J0))
    l0 = MathTex(rf"z_{I0+1}={terms}+", rf"{wname}x_{J0+1}", font_size=MIN_FONT, color=INK)
    l0[1].set_color(HIGHLIGHT)
    l1 = T(rf"\text{{nudge }} {wname} \text{{ by }} \epsilon:"
           rf"\quad z_{I0+1} \text{{ moves by }} x_{J0+1}\epsilon={fmt(s.x[J0])}\epsilon", HIGHLIGHT)
    l2 = T(rf"\text{{so }} L \text{{ moves by }} \delta_{I0+1}x_{J0+1}\epsilon"
           rf"={fmt(s.delta[I0] * s.x[J0])}\epsilon", RESULT_COLOR)
    l3 = T(rf"\partial L/\partial {wname}=\delta_{I0+1}x_{J0+1}={fmt(s.gW[I0, J0])}", RESULT_COLOR)
    for m, y in zip((l0, l1, l2, l3), (-0.9, -1.45, -2.0, -2.55)):
        m.move_to(np.array([-0.3, y, 0]))
    box = SurroundingRectangle(s.wcells[I0][J0], color=HIGHLIGHT, buff=0.12, stroke_width=3)
    return [l0, l1, l2, l3], box


class OuterProductLayer(Scene):
    """Part 1: what delta means, and one entry of dL/dW worked by hand."""

    def construct(self):
        s = _layer_stage()
        self.add(*s.statics)
        self.wait(1.5)

        # Beat 0: say what delta means before anything uses it.
        d1 = T(r"\delta_i=\partial L/\partial z_i", RESULT_COLOR).move_to(np.array([0, -1.25, 0]))
        d2 = T(r"\text{move } z_i \text{ a little: } L \text{ moves } \delta_i \text{ times as much}",
               INK).move_to(np.array([0, -2.0, 0]))
        self.play(FadeIn(d1), *[Indicate(m, color=HIGHLIGHT, scale_factor=1.1) for m in s.dl], run_time=1.0)
        self.play(FadeIn(d2), run_time=0.8)
        self.wait(3)
        self.play(FadeOut(d1), FadeOut(d2), run_time=0.5)

        # Beat 1: nudge one weight by epsilon and follow the nudge to L.
        (l0, l1, l2, l3), box = _worked_entry(s)
        self.play(FadeIn(l0), run_time=0.8)
        self.wait(1.5)
        self.play(Create(box), s.lines[(I0, J0)].animate.set_color(HIGHLIGHT).set_stroke(width=6),
                  Indicate(s.xn[J0][1], color=HIGHLIGHT, scale_factor=1.3), run_time=1.0)
        self.play(FadeIn(l1), Indicate(s.zn[I0][1], color=HIGHLIGHT, scale_factor=1.3), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(l2), Indicate(s.dl[I0], color=HIGHLIGHT, scale_factor=1.1), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(l3), run_time=0.8)
        self.wait(2.5)


class OuterProductBackward(Scene):
    """Part 2: the same entry for every weight, then delta back to x.

    Opens on part 1's last frame so the two clips join without a jump.
    """

    def construct(self):
        s = _layer_stage()
        worked, box = _worked_entry(s)
        s.lines[(I0, J0)].set_color(HIGHLIGHT).set_stroke(width=6)
        self.add(*s.statics, *worked, box)
        self.wait(2)

        # Beat 2: the same product for every pair, which is the whole grid.
        gl = T(r"\partial L/\partial W", RESULT_COLOR).move_to(MC + DOWN * 1.4)
        gcells = [[T(fmt(s.gW[i, j]), RESULT_COLOR).move_to(s.gc[i][j]) for j in range(3)]
                  for i in range(2)]
        self.play(*[FadeOut(m) for m in [box, *worked, s.wlbl] + [c for r in s.wcells for c in r]],
                  s.lines[(I0, J0)].animate.set_color(INK_FAINT).set_stroke(width=2.5),
                  FadeIn(gl), run_time=0.8)
        for i in range(2):
            for j in range(3):
                self.play(flash(s.lines[(i, j)], HIGHLIGHT),
                          Indicate(s.xn[j][1], color=HIGHLIGHT, scale_factor=1.3),
                          Indicate(s.dl[i], color=HIGHLIGHT, scale_factor=1.1), run_time=0.5)
                self.play(FadeIn(gcells[i][j], scale=1.4),
                          s.lines[(i, j)].animate.set_color(INK_DIM), run_time=0.4)
        f1 = MathTex(r"\frac{\partial L}{\partial W}=", r"\delta", r"x^{\top}", font_size=MIN_FONT)
        f1[0].set_color(RESULT_COLOR); f1[1].set_color(RESULT_COLOR); f1[2].set_color(V_COLOR)
        f1.move_to(np.array([-0.9, -1.85, 0]))
        self.play(FadeIn(f1))
        self.wait(2.5)

        # Beat 3: delta travels back along the same lines.
        self.play(FadeOut(f1), *[l.animate.set_color(INK_FAINT) for l in s.lines.values()], run_time=0.6)
        arith = MathTex(r"\partial L/\partial x_1=",
                        rf"{fmt(s.delta[0])}\cdot{fmt(s.W[0,0])}+({fmt(s.delta[1])})({fmt(s.W[1,0])})={fmt(s.gx[0])}",
                        font_size=MIN_FONT, color=RESULT_COLOR).move_to(np.array([-0.9, -1.85, 0]))
        for j in range(3):
            dots = [Dot(s.z_pos[i], radius=0.1, color=RESULT_COLOR) for i in range(2)]
            self.add(*dots)
            newn = T(fmt(s.gx[j]), RESULT_COLOR).move_to(s.x_pos[j])
            self.play(*[d.animate.move_to(s.x_pos[j]) for d in dots],
                      *[s.lines[(i, j)].animate.set_color(RESULT_COLOR) for i in range(2)], run_time=0.9)
            self.remove(*dots)
            self.play(FadeOut(s.xn[j][1]), FadeIn(newn),
                      s.xn[j][0].animate.set_stroke(color=RESULT_COLOR), run_time=0.4)
            if j == 0:
                self.play(FadeIn(arith))
                self.wait(1.5)
            self.play(*[s.lines[(i, j)].animate.set_color(INK_DIM) for i in range(2)], run_time=0.3)
        fa = MathTex(r"\frac{\partial L}{\partial W}=", r"\delta", r"x^{\top}", font_size=MIN_FONT)
        fa[0].set_color(RESULT_COLOR); fa[1].set_color(RESULT_COLOR); fa[2].set_color(V_COLOR)
        fb = MathTex(r"\frac{\partial L}{\partial x}=", r"W^{\top}", r"\delta", font_size=MIN_FONT)
        fb[0].set_color(RESULT_COLOR); fb[1].set_color(INK); fb[2].set_color(RESULT_COLOR)
        fa.move_to(np.array([-2.9, -1.85, 0])); fb.move_to(np.array([1.9, -1.85, 0]))
        self.play(FadeOut(arith))
        self.play(FadeIn(fa), FadeIn(fb))
        self.wait(2.5)


# ---------------------------------------------------------------- act 4
# One running example carries the whole act, after ArchQuant, "Automatic
# Differentiation Explained with Example": decompose f into elementary
# operations, then run the chain rule over them forwards (tangent mode) and
# backwards (adjoint mode).
#
#     f(a, b) = b sin a + b^2 = r
#     w0 = sin a      w1 = b w0      w2 = b^2      r = w1 + w2

A0, B0 = 0.5, 2.0


def num(v):
    """Three decimals, so a column of values lines up on the point."""
    return f"{v:.3f}"


def primal_trace(a, b):
    w0 = np.sin(a)
    w1 = b * w0
    w2 = b ** 2
    return w0, w1, w2, w1 + w2


def tangent_trace(a, b, adot, bdot):
    """The tangent of every primal, for the seed (adot, bdot)."""
    w0, _, _, _ = primal_trace(a, b)
    t0 = np.cos(a) * adot
    t1 = b * t0 + bdot * w0
    t2 = 2 * b * bdot
    return t0, t1, t2, t1 + t2


def adjoint_trace(a, b):
    """The six accumulations of the reverse sweep, in the order they happen."""
    w0, _, _, _ = primal_trace(a, b)
    rbar = 1.0
    w1bar = rbar                 # r = w1 + w2
    w2bar = rbar
    bbar_1 = 2 * b * w2bar       # w2 = b^2
    w0bar = b * w1bar            # w1 = b w0, the w0 half
    bbar_2 = bbar_1 + w0 * w1bar # w1 = b w0, the b half: b's second contribution
    abar = w0bar * np.cos(a)     # w0 = sin a
    return w1bar, w2bar, bbar_1, w0bar, bbar_2, abar


def fd(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


def _check():
    """Every number the act shows, against central finite differences."""
    a, b = A0, B0
    F = lambda s, t: t * np.sin(s) + t ** 2
    assert np.isclose(primal_trace(a, b)[3], F(a, b))
    assert np.isclose(tangent_trace(a, b, 1.0, 0.0)[3], fd(lambda s: F(s, b), a))
    assert np.isclose(tangent_trace(a, b, 0.0, 1.0)[3], fd(lambda t: F(a, t), b))
    _, _, _, _, bbar, abar = adjoint_trace(a, b)
    assert np.isclose(abar, fd(lambda s: F(s, b), a))
    assert np.isclose(bbar, fd(lambda t: F(a, t), b))


_check()


def col(mobs, x, edge=LEFT):
    """Align a stack of rows on a column at world x."""
    for m in mobs:
        m.shift(RIGHT * (x - m.get_edge_center(edge)[0]))
    return mobs


# ---------------------------------------------------------------- scene 3

class DecomposeToPrimals(Scene):
    """f is a chain of elementary operations, and the chain rule is a product
    of three factors that can be multiplied from either end."""

    def construct(self):
        a, b = A0, B0
        w0, w1, w2, r = primal_trace(a, b)

        head = MathTex(r"f(a,b)=", r"b", r"\sin a", r"+", r"b^{2}", r"=", r"r",
                       font_size=MIN_FONT, color=INK)
        head[1].set_color(W_COLOR)
        head[2].set_color(V_COLOR)
        head[4].set_color(W_COLOR)
        head[6].set_color(RESULT_COLOR)
        head.move_to(UP * 2.4)

        steps = [r"w_0=\sin a", r"w_1=b\,w_0", r"w_2=b^{2}", r"r=w_1+w_2"]
        rows = VGroup(*[T(s, INK) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        rows.move_to(np.array([-2.9, -0.2, 0]))
        rows[3][0].set_color(RESULT_COLOR)
        vals = [T(rf"={num(v)}", INK_DIM, 36) for v in (w0, w1, w2, r)]
        for v, m in zip(vals, rows):
            v.next_to(rows, RIGHT, buff=0.3).set_y(m.get_y())

        # Frame one carries the function and its decomposition, because the
        # slide shows it before the clip plays. The values and the chain rule
        # are what get built.
        self.add(head, *rows)
        self.wait(1.5)
        for m, v in zip(rows, vals):
            self.play(Indicate(m, color=HIGHLIGHT, scale_factor=1.1),
                      FadeIn(v), run_time=0.6)
        self.wait(1.5)

        chain = MathTex(r"\frac{\partial r}{\partial a}", "=",
                        r"\frac{\partial r}{\partial w_1}",
                        r"\frac{\partial w_1}{\partial w_0}",
                        r"\frac{\partial w_0}{\partial a}",
                        font_size=MIN_FONT, color=INK)
        chain[0].set_color(RESULT_COLOR)
        chain.move_to(np.array([1.9, 0.75, 0]))

        self.play(FadeIn(chain[0:2]), run_time=0.6)
        for k, src in ((2, 3), (3, 1), (4, 0)):
            self.play(Indicate(rows[src], color=HIGHLIGHT, scale_factor=1.12),
                      FadeIn(chain[k], scale=1.3), run_time=0.7)
        self.wait(1.8)

        # The same product, multiplied from either end.
        fwd = T(r"\text{forward (tangent)}", V_COLOR, 36)
        rev = T(r"\text{reverse (adjoint)}", RESULT_COLOR, 36)
        a_f = Arrow(chain[4].get_bottom() + DOWN * 0.3, chain[2].get_bottom() + DOWN * 0.3,
                    color=V_COLOR, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.12)
        a_r = Arrow(chain[2].get_bottom() + DOWN * 1.6, chain[4].get_bottom() + DOWN * 1.6,
                    color=RESULT_COLOR, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.12)
        fwd.next_to(a_f, DOWN, buff=0.12)
        rev.next_to(a_r, DOWN, buff=0.12)

        self.play(GrowArrow(a_f), FadeIn(fwd), run_time=0.8)
        self.wait(1.4)
        self.play(GrowArrow(a_r), FadeIn(rev), run_time=0.8)
        self.wait(2.2)


# ---------------------------------------------------------------- scene 4

class ForwardTangentTrace(Scene):
    """Primals down the left, tangents down the right, computed in parallel.
    The seed picks which input the sweep differentiates with respect to."""

    def construct(self):
        a, b = A0, B0
        w0, w1, w2, r = primal_trace(a, b)
        t = tangent_trace(a, b, 1.0, 0.0)
        t2 = tangent_trace(a, b, 0.0, 1.0)

        head = T(r"f(a,b)=b\sin a+b^{2}=r", INK, 36).move_to(np.array([-2.6, 2.4, 0]))
        seed = MathTex(r"\text{seed: }", r"\dot a=1", r",\;", r"\dot b=0",
                       font_size=36, color=RESULT_COLOR).move_to(np.array([2.5, 2.4, 0]))

        h_p = T(r"\text{primal}", V_COLOR, 36)
        h_t = T(r"\text{tangent}", RESULT_COLOR, 36)

        pr = [r"w_0=\sin a", r"w_1=b\,w_0", r"w_2=b^{2}", r"r=w_1+w_2"]
        tg = [r"\dot w_0=\cos a\,\dot a", r"\dot w_1=b\,\dot w_0+\dot b\,w_0",
              r"\dot w_2=2b\,\dot b", r"\dot r=\dot w_1+\dot w_2"]
        pv = [w0, w1, w2, r]

        ys = [1.15, 0.35, -0.45, -1.25]
        p_rows = [T(s, INK, 36) for s in pr]
        p_vals = [T(rf"={num(v)}", INK_DIM, 36) for v in pv]
        t_rows = [T(s, INK, 36) for s in tg]
        t_vals = [T(rf"={num(v)}", RESULT_COLOR, 36) for v in t]

        col(p_rows, -4.8)
        col(p_vals, -2.2)
        col(t_rows, -0.65)
        col(t_vals, 2.45)
        for i, y in enumerate(ys):
            for m in (p_rows[i], p_vals[i], t_rows[i], t_vals[i]):
                m.set_y(y)
        h_p.move_to(np.array([-3.6, 1.95, 0]))
        h_t.move_to(np.array([0.9, 1.95, 0]))
        rule = Line(np.array([-4.9, 1.65, 0]), np.array([3.9, 1.65, 0]),
                    color=INK_FAINT, stroke_width=2)
        div = Line(np.array([-1.0, 1.65, 0]), np.array([-1.0, -1.7, 0]),
                   color=INK_FAINT, stroke_width=2)

        # The program is a given, so frame one already shows the primal column.
        # Only the derivative work is animated.
        self.add(head, seed, h_p, h_t, rule, div, *p_rows)
        self.wait(1.5)
        for i in range(4):
            self.play(FadeIn(p_vals[i]), run_time=0.35)
            self.play(FadeIn(t_rows[i], shift=RIGHT * 0.2), FadeIn(t_vals[i]), run_time=0.45)
            self.wait(0.25)

        box = SurroundingRectangle(VGroup(t_rows[3], t_vals[3]), color=HIGHLIGHT,
                                   buff=0.14, stroke_width=3)
        got = T(rf"\partial r/\partial a=b\cos a={num(t[3])}", HIGHLIGHT, 36)
        got.move_to(np.array([0.3, -2.25, 0]))
        self.play(Create(box), FadeIn(got), run_time=0.9)
        self.wait(2.2)

        # Same machine, other seed: one sweep buys one input's derivative.
        seed2 = MathTex(r"\text{seed: }", r"\dot a=0", r",\;", r"\dot b=1",
                        font_size=36, color=RESULT_COLOR).move_to(seed.get_center())
        t_vals2 = [T(rf"={num(v)}", RESULT_COLOR, 36) for v in t2]
        col(t_vals2, 2.45)
        for i, y in enumerate(ys):
            t_vals2[i].set_y(y)
        got2 = T(rf"\partial r/\partial b=\sin a+2b={num(t2[3])}", HIGHLIGHT, 36)
        got2.move_to(got.get_center())

        self.play(FadeOut(box), FadeOut(got), run_time=0.4)
        self.play(FadeOut(seed), FadeIn(seed2), run_time=0.6)
        self.play(*[FadeOut(m) for m in t_vals], run_time=0.3)
        for i in range(4):
            self.play(FadeIn(t_vals2[i]), run_time=0.3)
        box2 = SurroundingRectangle(VGroup(t_rows[3], t_vals2[3]), color=HIGHLIGHT,
                                    buff=0.14, stroke_width=3)
        self.play(Create(box2), FadeIn(got2), run_time=0.9)
        self.wait(1.6)

        cost = T(r"\text{one sweep per input}", INK_DIM, 36).move_to(np.array([0.3, -2.25, 0]))
        self.play(FadeOut(got2), FadeIn(cost), run_time=0.7)
        self.wait(2.2)


# ---------------------------------------------------------------- scene 5

class ReverseAdjointTape(Scene):
    """Forward once to fill the tape, then back up it accumulating adjoints.
    b appears twice in f, so b-bar is a sum of two contributions."""

    def construct(self):
        a, b = A0, B0
        w0, w1, w2, r = primal_trace(a, b)
        w1b, w2b, bb1, w0b, bb2, ab = adjoint_trace(a, b)

        head = T(r"f(a,b)=b\sin a+b^{2}=r", INK, 36).move_to(np.array([-2.6, 2.4, 0]))
        seed = MathTex(r"\text{seed: }", r"\bar r=1", font_size=36,
                       color=RESULT_COLOR).move_to(np.array([3.6, 2.4, 0]))

        pr = [r"w_0=\sin a", r"w_1=b\,w_0", r"w_2=b^{2}", r"r=w_1+w_2"]
        p_rows = [T(s, INK, 36) for s in pr]
        p_vals = [T(rf"={num(v)}", INK_DIM, 36) for v in (w0, w1, w2, r)]
        col(p_rows, -4.5)
        col(p_vals, -2.2)
        pys = [1.15, 0.45, -0.25, -0.95]
        for i, y in enumerate(pys):
            p_rows[i].set_y(y)
            p_vals[i].set_y(y)

        down = Arrow(np.array([-4.8, 1.45, 0]), np.array([-4.8, -1.25, 0]),
                     color=V_COLOR, stroke_width=5, buff=0,
                     max_tip_length_to_length_ratio=0.1)
        tag_f = T(r"\text{forward}", V_COLOR, 36).move_to(np.array([-3.3, 1.95, 0]))
        self.add(head, tag_f, down, *p_rows)
        self.wait(1.2)
        for i in range(4):
            self.play(FadeIn(p_vals[i]), run_time=0.35)
        tape = T(r"\text{stored on the tape}", INK_FAINT, 32).move_to(np.array([-3.1, -1.8, 0]))
        tape_box = SurroundingRectangle(VGroup(*p_vals), color=INK_FAINT, buff=0.16,
                                        stroke_width=2)
        self.play(Create(tape_box), FadeIn(tape), run_time=0.8)
        self.wait(1.8)

        # Turn around.
        up = Arrow(np.array([-0.75, -1.55, 0]), np.array([-0.75, 2.0, 0]),
                   color=RESULT_COLOR, stroke_width=5, buff=0,
                   max_tip_length_to_length_ratio=0.08)
        tag_r = T(r"\text{reverse}", RESULT_COLOR, 36).move_to(np.array([1.0, 2.4, 0]))
        self.play(FadeIn(seed), run_time=0.5)
        self.play(GrowArrow(up), FadeIn(tag_r), run_time=0.9)
        self.wait(0.8)

        # The six accumulations, bottom of the trace to the top.
        acc = [(r"\bar w_1\mathrel{+}=\bar r", w1b, False),
               (r"\bar w_2\mathrel{+}=\bar r", w2b, False),
               (r"\bar b\mathrel{+}=2b\,\bar w_2", bb1, True),
               (r"\bar w_0\mathrel{+}=b\,\bar w_1", w0b, False),
               (r"\bar b\mathrel{+}=w_0\,\bar w_1", bb2 - bb1, True),
               (r"\bar a\mathrel{+}=\bar w_0\cos a", ab, False)]
        ays = [1.5, 0.98, 0.46, -0.06, -0.58, -1.10]
        rows, vals = [], []
        for s, v, _ in acc:
            rows.append(T(s, INK, 36))
            vals.append(T(rf"={num(v)}", RESULT_COLOR, 36))
        col(rows, -0.25)
        col(vals, 2.8)
        for i, y in enumerate(ays):
            rows[i].set_y(y)
            vals[i].set_y(y)

        for i, (_, _, is_b) in enumerate(acc):
            if is_b:
                self.play(FadeIn(rows[i], shift=RIGHT * 0.2), FadeIn(vals[i]),
                          Flash(rows[i].get_left() + LEFT * 0.12, color=HIGHLIGHT,
                                line_length=0.12, num_lines=8, flash_radius=0.3),
                          run_time=0.75)
                self.wait(0.5)
            else:
                self.play(FadeIn(rows[i], shift=RIGHT * 0.2), FadeIn(vals[i]), run_time=0.55)
                self.wait(0.15)
        self.wait(1.0)

        # b got two contributions. That plus sign is the whole of the reverse rule.
        bsum = MathTex(r"\bar b=", num(bb1), "+", num(bb2 - bb1), "=", num(bb2),
                       font_size=36, color=HIGHLIGHT).move_to(np.array([1.3, -2.1, 0]))
        self.play(Indicate(rows[2], color=HIGHLIGHT, scale_factor=1.1),
                  Indicate(rows[4], color=HIGHLIGHT, scale_factor=1.1), run_time=0.9)
        self.play(FadeIn(bsum), run_time=0.7)
        self.wait(1.8)

        out = MathTex(rf"\bar a={num(ab)}", r",\quad", rf"\bar b={num(bb2)}",
                      font_size=MIN_FONT, color=RESULT_COLOR)
        out.move_to(np.array([1.3, -2.2, 0]))
        box = SurroundingRectangle(out, color=HIGHLIGHT, buff=0.16, stroke_width=3)
        both = T(r"\text{both, in one sweep}", HIGHLIGHT, 32).move_to(np.array([-3.1, -2.35, 0]))
        self.play(FadeOut(bsum), FadeIn(out), run_time=0.6)
        self.play(Create(box), FadeIn(both), run_time=0.8)
        self.wait(2.5)


# ---------------------------------------------------------------- scene 6

class JacobianSeeds(Scene):
    """Four inputs, two outputs. Forward mode seeds an input and fills a
    column; reverse mode seeds an output and fills a row."""

    def construct(self):
        a, b, c, d = 0.5, 2.0, 1.5, 0.25

        def f(v):
            return np.array([v[1] * np.sin(v[0]) + v[1] ** 2, 2 * v[2] * v[3] + v[0]])

        x0 = np.array([a, b, c, d])
        J = np.array([[b * np.cos(a), np.sin(a) + 2 * b, 0.0, 0.0],
                      [1.0, 0.0, 2 * d, 2 * c]])
        h = 1e-6
        for j in range(4):
            e = np.zeros(4); e[j] = h
            assert np.allclose((f(x0 + e) - f(x0 - e)) / (2 * h), J[:, j], atol=1e-6)

        head = MathTex(r"f(a,b,c,d)=\bigl(b\sin a+b^{2},\;2cd+a\bigr)",
                       font_size=36, color=INK).move_to(UP * 2.4)

        names = ["a", "b", "c", "d"]
        in_pos = [np.array([-3.5, y, 0]) for y in (1.25, 0.45, -0.35, -1.15)]
        out_pos = [np.array([-1.6, y, 0]) for y in (0.85, -0.75)]
        nin = [node(names[j], in_pos[j], V_COLOR, r=0.3) for j in range(4)]
        nout = [node(rf"r_{i}", out_pos[i], RESULT_COLOR, r=0.3) for i in range(2)]
        lines = {(i, j): Line(in_pos[j], out_pos[i], color=INK_FAINT, stroke_width=2)
                 for i in range(2) for j in range(4)}
        for (i, j), ln in lines.items():
            dvec = ln.get_vector() / ln.get_length()
            ln.put_start_and_end_on(in_pos[j] + dvec * 0.3, out_pos[i] - dvec * 0.3)

        cw, ch = 1.05, 0.95
        mc = np.array([2.45, 0.05, 0])
        gc = grid_centers(mc, 2, 4, cw, ch)
        br = bracket(mc, 4 * cw + 0.3, 2 * ch + 0.1)
        jl = T(r"J_f", INK).move_to(mc + UP * 1.35)
        cells = {(i, j): T(num(J[i, j]), RESULT_COLOR, 36).move_to(gc[i][j])
                 for i in range(2) for j in range(4)}

        tag_f = T(r"\text{forward mode}", V_COLOR, 36).move_to(np.array([-3.0, 2.05, 0]))
        tag_r = T(r"\text{reverse mode}", RESULT_COLOR, 36).move_to(np.array([-3.0, 2.05, 0]))

        def counter(k, color):
            return T(rf"\text{{sweeps}}={k}", color, 36).move_to(np.array([-2.9, -2.2, 0]))

        cnt = counter(0, V_COLOR)
        self.add(head, *lines.values(), *nin, *nout, br, jl, tag_f, cnt)
        self.wait(1.8)

        # Forward: seed one input, get one column.
        for j in range(4):
            seed = T(rf"\dot {names[j]}=1", HIGHLIGHT, 32).next_to(nin[j], LEFT, buff=0.2)
            self.play(FadeIn(seed), Indicate(nin[j], color=HIGHLIGHT, scale_factor=1.2),
                      run_time=0.45)
            self.play(*[flash(lines[(i, j)], V_COLOR) for i in range(2)], run_time=0.6)
            new = counter(j + 1, V_COLOR)
            self.play(*[FadeIn(cells[(i, j)], scale=1.3) for i in range(2)],
                      FadeOut(cnt), FadeIn(new), FadeOut(seed), run_time=0.5)
            cnt = new
            self.wait(0.2)
        colbox = SurroundingRectangle(VGroup(cells[(0, 0)], cells[(1, 0)]), color=V_COLOR,
                                      buff=0.14, stroke_width=3)
        colnote = T(r"\text{one seed, one column}", V_COLOR, 32).move_to(np.array([2.45, -1.9, 0]))
        self.play(Create(colbox), FadeIn(colnote), run_time=0.8)
        self.wait(2.0)

        # Reverse: seed one output, get one row.
        self.play(*[FadeOut(cells[k]) for k in cells], FadeOut(colbox), FadeOut(colnote),
                  FadeOut(tag_f), FadeOut(cnt), run_time=0.6)
        cnt = counter(0, RESULT_COLOR)
        self.play(FadeIn(tag_r), FadeIn(cnt), run_time=0.5)
        for i in range(2):
            seed = T(rf"\bar r_{i}=1", HIGHLIGHT, 32).next_to(nout[i], RIGHT, buff=0.2)
            self.play(FadeIn(seed), Indicate(nout[i], color=HIGHLIGHT, scale_factor=1.2),
                      run_time=0.45)
            self.play(*[flash(lines[(i, j)], RESULT_COLOR) for j in range(4)], run_time=0.7)
            new = counter(i + 1, RESULT_COLOR)
            self.play(*[FadeIn(cells[(i, j)], scale=1.3) for j in range(4)],
                      FadeOut(cnt), FadeIn(new), FadeOut(seed), run_time=0.5)
            cnt = new
            self.wait(0.3)
        rowbox = SurroundingRectangle(VGroup(*[cells[(0, j)] for j in range(4)]),
                                      color=RESULT_COLOR, buff=0.14, stroke_width=3)
        rownote = T(r"\text{one seed, one row}", RESULT_COLOR, 32).move_to(np.array([2.45, -1.9, 0]))
        self.play(Create(rowbox), FadeIn(rownote), run_time=0.8)
        self.wait(2.2)

        # The shape machine learning is actually in.
        everything = [head, *lines.values(), *nin, *nout, br, jl, tag_r, cnt, rowbox,
                      rownote, *cells.values()]
        self.play(*[FadeOut(m) for m in everything], run_time=0.8)
        l0 = T(r"10^{6}\text{ parameters},\;1\text{ loss}", INK).move_to(UP * 1.4)
        l1 = MathTex(r"\text{forward: }", r"10^{6}\text{ sweeps}", font_size=MIN_FONT)
        l1[0].set_color(INK_DIM); l1[1].set_color(V_COLOR)
        l2 = MathTex(r"\text{reverse: }", r"1\text{ sweep}", font_size=MIN_FONT)
        l2[0].set_color(INK_DIM); l2[1].set_color(RESULT_COLOR)
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(DOWN * 0.5)
        self.play(FadeIn(l0))
        self.wait(1.0)
        self.play(FadeIn(l1))
        self.wait(1.0)
        self.play(FadeIn(l2))
        self.wait(2.5)
