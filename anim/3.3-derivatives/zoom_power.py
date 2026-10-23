# Original work for Mathematics for AI (zoom idea after 3b1b EoC ch. 3, cube picture after EoC ch. 3
# NudgeSideLengthOfCube), (c) 3Blue1Brown ideas, CC BY-NC-SA 4.0

from shared.anim.house import *


# ---------------------------------------------------------------- ZoomIn
class ZoomIn(Scene):
    """Local linearity: zoom into y = x^2 at x = 1 until it is its tangent line."""

    def construct(self):
        S = 2.15                      # half-size of the square view in scene units
        C = np.array([-2.15, -0.1, 0.0])
        f = lambda x: x * x
        x0 = 1.0
        y0 = f(x0)
        slope = 2 * x0

        w = ValueTracker(1.0)         # half-width of the window in data units
        dx = ValueTracker(0.0)        # nudge shown (0 = hidden)

        def to_screen(x, y):
            ww = w.get_value()
            return C + np.array([(x - x0) / ww * S, (y - y0) / ww * S, 0.0])

        def clipped(points):
            pts = [p for p in points if abs(p[0] - C[0]) <= S and abs(p[1] - C[1]) <= S]
            return pts

        def curve():
            ww = w.get_value()
            us = np.linspace(-1, 1, 500)
            pts = clipped([to_screen(x0 + u * ww, f(x0 + u * ww)) for u in us])
            m = VMobject(stroke_color=V_COLOR, stroke_width=5)
            m.set_points_as_corners(pts if len(pts) > 1 else [C, C + 0.01 * RIGHT])
            return m

        def tangent():
            ww = w.get_value()
            us = np.linspace(-1, 1, 200)
            pts = clipped([to_screen(x0 + u * ww, y0 + slope * u * ww) for u in us])
            m = VMobject(stroke_color=RESULT_COLOR, stroke_width=3)
            m.set_points_as_corners(pts if len(pts) > 1 else [C, C + 0.01 * RIGHT])
            return m

        frame = Square(side_length=2 * S, stroke_color=INK_FAINT, stroke_width=2).move_to(C)
        curve_m = always_redraw(curve)
        tan_m = always_redraw(tangent)
        P = Dot(C, color=RESULT_COLOR, radius=0.09).set_z_index(5)
        p_lbl = MathTex(r"P", font_size=MIN_FONT, color=RESULT_COLOR)
        p_lbl.next_to(P, DOWN + RIGHT, buff=0.15)

        # Nudge triangle (only when dx > 0)
        def nudge_group():
            d = dx.get_value()
            if d <= 0:
                return VGroup()
            a = to_screen(x0, y0)
            b = to_screen(x0 + d, y0)
            q = to_screen(x0 + d, f(x0 + d))
            t = to_screen(x0 + d, y0 + slope * d)
            g = VGroup(
                Line(a, b, color=X_COLOR, stroke_width=4),
                Line(b, q, color=Y_COLOR, stroke_width=4),
                Dot(q, color=V_COLOR, radius=0.07),
                Dot(t, color=RESULT_COLOR, radius=0.07),
            )
            return g
        nudge_m = always_redraw(nudge_group)

        # Readouts, right column
        def row(label, fn, color, places=2, prefix=""):
            lab = MathTex(label, font_size=MIN_FONT, color=color)
            num = DecimalNumber(fn(), num_decimal_places=places, font_size=MIN_FONT, color=color)
            num.next_to(lab, RIGHT, buff=0.15)
            num.add_updater(lambda m: m.set_value(fn()))
            num.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.15))
            return VGroup(lab, num), num

        zoom_row, zoom_num = row(r"\text{zoom}\ \times", lambda: 1.0 / w.get_value(), INK, places=0)
        lo_row, _ = row(r"x\ \text{from}", lambda: x0 - w.get_value(), X_COLOR, places=3)
        hi_row, _ = row(r"x\ \text{to}\ \ ", lambda: x0 + w.get_value(), X_COLOR, places=3)
        # slope of the chord from P to the right edge of the window
        sl_row, _ = row(r"\text{slope}\ ", lambda: (f(x0 + w.get_value()) - y0) / w.get_value(), RESULT_COLOR, places=3)
        panel = VGroup(zoom_row, lo_row, hi_row, sl_row).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        panel.move_to(np.array([2.85, 0.35, 0.0]))
        panel.set_x(2.95)
        fx = MathTex(r"f(x)=x^2,\ \ x=1", font_size=MIN_FONT, color=V_COLOR)
        fx.move_to(np.array([2.9, 2.3, 0.0]))

        for m in panel.get_family():
            m.update(0)
        self.add(frame, curve_m, tan_m, nudge_m, P, p_lbl, fx, panel)
        self.wait(1.5)

        for target in (1 / 3, 0.1, 0.03, 0.01):
            self.play(w.animate.set_value(target), run_time=1.8, rate_func=smooth)
            self.wait(1.2)
        note = MathTex(r"\text{straight line, slope} \to 2", font_size=MIN_FONT, color=INK)
        note.move_to(np.array([2.9, -1.75, 0.0]))
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.5)

        # Step 2: put a nudge on it and compare df with 2 dx
        self.play(FadeOut(note), FadeOut(panel), run_time=0.6)
        self.play(w.animate.set_value(0.5), run_time=2.0)

        def card(d):
            df = f(x0 + d) - y0
            lines = VGroup(
                MathTex(rf"dx = {d:g}", font_size=MIN_FONT, color=X_COLOR),
                MathTex(rf"df = {df:.4g}", font_size=MIN_FONT, color=Y_COLOR),
                MathTex(rf"2\,dx = {slope * d:.4g}", font_size=MIN_FONT, color=RESULT_COLOR),
                MathTex(rf"dx^2 = {d * d:.4g}", font_size=MIN_FONT, color=INK_DIM),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            lines.move_to(np.array([2.95, 0.3, 0.0])).set_x(2.95)
            return lines

        c1 = card(0.2)
        dx.set_value(0.2)
        self.play(FadeIn(c1), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(c1), run_time=0.4)
        self.play(w.animate.set_value(0.05), dx.animate.set_value(0.02), run_time=2.0)
        c2 = card(0.02)
        self.play(FadeIn(c2), run_time=0.8)
        self.wait(1.8)
        fin = MathTex(r"df \approx f'(1)\,dx,\ \ f'(1)=2", font_size=MIN_FONT, color=RESULT_COLOR)
        fin.move_to(np.array([2.5, -2.0, 0.0]))
        self.play(FadeIn(fin), run_time=0.8)
        self.wait(2.0)


# ---------------------------------------------------------------- PowerRule
def _box_faces(x0, x1, y0, y1, z0, z1, proj, fill, op, stroke=BG):
    """Front (y=y0), right (x=x1) and top (z=z1) faces of an axis-aligned box."""
    P = lambda a, b, c: proj(a, b, c)
    faces = [
        [P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)],
        [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)],
        [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)],
    ]
    shades = [1.0, 0.8, 1.2]
    g = VGroup()
    for f_, s in zip(faces, shades):
        g.add(Polygon(*f_, stroke_color=stroke, stroke_width=1.5,
                      fill_color=interpolate_color(ManimColor(BG), ManimColor(fill), min(1.0, op * s * 0.9)),
                      fill_opacity=1.0))
    return g


class PowerRule(Scene):
    """(x+dx)^3 as three factors, then the cube picture. Ends on n x^(n-1) dx."""

    def construct(self):
        # ---- phase 1: which factor gives the dx?
        head = MathTex(r"(x+dx)^3 = (x+dx)(x+dx)(x+dx)", font_size=MIN_FONT, color=INK)
        head.move_to(UP * 2.25)

        def term(parts, colors, tail, tail_color):
            tex = MathTex(*parts, tail, font_size=MIN_FONT)
            for p, c in zip(tex[:len(parts)], colors):
                p.set_color(c)
            tex[-1].set_color(tail_color)
            return tex

        X, D, I = V_COLOR, X_COLOR, INK_DIM
        r0 = term([r"x", r"\cdot", r"x", r"\cdot", r"x"], [X, I, X, I, X], r"=\ x^3", V_COLOR)
        r1 = term([r"dx", r"\cdot", r"x", r"\cdot", r"x"], [D, I, X, I, X], r"=\ x^2\,dx", RESULT_COLOR)
        r2 = term([r"x", r"\cdot", r"dx", r"\cdot", r"x"], [X, I, D, I, X], r"=\ x^2\,dx", RESULT_COLOR)
        r3 = term([r"x", r"\cdot", r"x", r"\cdot", r"dx"], [X, I, X, I, D], r"=\ x^2\,dx", RESULT_COLOR)
        rows = VGroup(r0, r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to(np.array([-1.3, 0.55, 0.0]))
        lab0 = MathTex(r"\text{no } dx", font_size=MIN_FONT, color=INK_DIM).next_to(rows, RIGHT, buff=0.5).align_to(r0, UP)
        labs = VGroup(*[MathTex(rf"\text{{factor {k}}}", font_size=MIN_FONT, color=INK_DIM)
                        for k in (1, 2, 3)])
        for lab, r in zip(labs, (r1, r2, r3)):
            lab.next_to(rows, RIGHT, buff=0.5).set_y(r.get_y())
        lab0.set_y(r0.get_y())
        brace = Brace(VGroup(r1, r2, r3), RIGHT, buff=0.1)
        brace.shift(RIGHT * 1.9)
        three = MathTex(r"3\ \text{ways}", r"\Rightarrow\ 3x^2\,dx", font_size=MIN_FONT, color=RESULT_COLOR)
        three.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        three.next_to(brace, RIGHT, buff=0.15)
        rest = MathTex(r"\text{two or more } dx:\ 3x\,dx^2+dx^3\ \text{(tiny)}", font_size=MIN_FONT, color=INK_FAINT)
        rest.move_to(DOWN * 2.1)

        self.add(head)
        self.wait(1.2)
        self.play(FadeIn(r0), FadeIn(lab0), run_time=0.8)
        self.wait(1.5)
        for r, lab in zip((r1, r2, r3), labs):
            self.play(FadeIn(r), FadeIn(lab), run_time=0.7)
            self.wait(0.6)
        self.play(Create(brace), FadeIn(three), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(rest), run_time=0.8)
        self.wait(1.2)

        # ---- phase 2: the same three ways are the three slabs of a cube
        self.play(*[FadeOut(m) for m in (head, rows, lab0, labs, brace, three, rest)], run_time=0.8)

        unit = 1.75                     # scene units per x (x = 1)
        dxt = ValueTracker(0.45)
        ox = np.array([-4.2, -2.1, 0.0])
        kx, ky = 0.55, 0.38             # oblique depth shift per unit y

        def proj(a, b, c):
            return ox + np.array([unit * (a + kx * b), unit * (c + ky * b), 0.0])

        def cube():
            d = dxt.get_value()
            x = 1.0
            cuts = [(0, x), (x, x + d)]
            boxes = []
            for i, (xa, xb) in enumerate(cuts):
                for j, (ya, yb) in enumerate(cuts):
                    for k, (za, zb) in enumerate(cuts):
                        n = i + j + k
                        if n == 0:
                            fill, op = V_COLOR, 0.45
                        elif n == 1:
                            fill, op = RESULT_COLOR, 0.8
                        else:
                            fill, op = INK_FAINT, 0.6
                        boxes.append(((xa, xb, ya, yb, za, zb), fill, op))
            boxes.sort(key=lambda b: b[0][0] - b[0][2] + b[0][4])
            g = VGroup()
            for (xa, xb, ya, yb, za, zb), fill, op in boxes:
                g.add(_box_faces(xa, xb, ya, yb, za, zb, proj, fill, op))
            return g

        cube_m = always_redraw(cube)

        def num_row(label, fn, color, places):
            lab = MathTex(label, font_size=MIN_FONT, color=color)
            num = DecimalNumber(fn(), num_decimal_places=places, font_size=MIN_FONT, color=color)
            num.next_to(lab, RIGHT, buff=0.15)
            num.add_updater(lambda m: m.set_value(fn()))
            num.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.15))
            return VGroup(lab, num)

        d_ = lambda: dxt.get_value()
        r_dx = num_row(r"dx =", d_, X_COLOR, 2)
        r_sl = num_row(r"3x^2dx =", lambda: 3 * d_(), RESULT_COLOR, 3)
        r_lo = num_row(r"\text{left over} =", lambda: 3 * d_() ** 2 + d_() ** 3, INK_DIM, 3)
        r_ra = num_row(r"\text{ratio} =", lambda: (3 * d_() ** 2 + d_() ** 3) / (3 * d_()), INK, 3)
        panel = VGroup(r_dx, r_sl, r_lo, r_ra).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        panel.move_to(np.array([2.9, -0.45, 0.0])).set_x(2.9)

        slab_tag = MathTex(r"\text{3 slabs, each } x^2\,dx", font_size=MIN_FONT, color=RESULT_COLOR)
        slab_tag.move_to(np.array([2.9, 2.3, 0.0]))
        edge_tag = MathTex(r"\text{edges, corner: grey}", font_size=MIN_FONT, color=INK_FAINT)
        edge_tag.move_to(np.array([2.9, 1.6, 0.0]))
        xlab = MathTex(r"x", font_size=MIN_FONT, color=V_COLOR).move_to(proj(0.5, 0, 0) + DOWN * 0.38)

        self.add(cube_m, xlab)
        self.play(FadeIn(slab_tag), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(edge_tag), run_time=0.8)
        self.wait(1.5)
        self.play(FadeIn(panel), run_time=0.8)
        self.wait(1.0)
        for v in (0.25, 0.1, 0.04):
            self.play(dxt.animate.set_value(v), run_time=1.4)
            self.wait(1.0)
        self.play(FadeOut(panel), FadeOut(slab_tag), FadeOut(edge_tag), run_time=0.7)
        fin = MathTex(r"d(x^3) = 3x^2\,dx", font_size=MIN_FONT + 6, color=RESULT_COLOR)
        gen = MathTex(r"d(x^n) = n\,x^{n-1}\,dx", font_size=MIN_FONT + 6, color=RESULT_COLOR)
        why = VGroup(MathTex(r"n\ \text{ways to pick the factor}", font_size=MIN_FONT, color=INK_DIM), MathTex(r"\text{that gives } dx", font_size=MIN_FONT, color=INK_DIM)).arrange(DOWN, buff=0.15)
        VGroup(fin, gen, why).arrange(DOWN, buff=0.5).move_to(np.array([2.2, 0.2, 0.0]))
        self.play(Write(fin), run_time=1.0)
        self.wait(1.2)
        self.play(FadeIn(gen), FadeIn(why), run_time=1.0)
        self.wait(2.2)


# ---------------------------------------------------------------- NoTangent
class NoTangent(Scene):
    """|x| at 0: the slope from the right is +1, from the left is -1."""

    def construct(self):
        axes = Axes(
            x_range=[-2, 2, 1], y_range=[-1, 2, 1], x_length=5.4, y_length=3.6,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 2.5, "include_tip": False},
        ).move_to(np.array([-1.8, -0.25, 0]))
        axes.add_coordinates(font_size=MIN_FONT)
        for ax in axes.get_axes():
            for n in getattr(ax, "numbers", []):
                n.set_color(INK_DIM)
        graph = axes.plot(lambda x: abs(x), x_range=[-2, 2], color=INK, stroke_width=4)
        line_r = axes.plot(lambda x: x, x_range=[-1, 2], color=V_COLOR, stroke_width=3)
        line_l = axes.plot(lambda x: -x, x_range=[-2, 1], color=W_COLOR, stroke_width=3)
        h = ValueTracker(1.0)
        dot_r = always_redraw(lambda: Dot(axes.c2p(h.get_value(), h.get_value()), color=V_COLOR, radius=0.09))
        dot_l = always_redraw(lambda: Dot(axes.c2p(-h.get_value(), h.get_value()), color=W_COLOR, radius=0.09))
        origin = Dot(axes.c2p(0, 0), color=RESULT_COLOR, radius=0.09)
        f = abs
        sr = lambda: (f(h.get_value()) - f(0)) / h.get_value()
        sl = lambda: (f(-h.get_value()) - f(0)) / (-h.get_value())

        def row(label, fn, color, places, sign):
            lab = MathTex(label, font_size=MIN_FONT, color=color)
            num = DecimalNumber(fn(), num_decimal_places=places, include_sign=sign, font_size=MIN_FONT, color=color)
            num.next_to(lab, RIGHT, buff=0.15)
            num.add_updater(lambda m: m.set_value(fn()))
            num.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.15))
            return VGroup(lab, num)

        panel = VGroup(
            row(r"h =", lambda: h.get_value(), X_COLOR, 2, False),
            row(r"\text{right}", sr, V_COLOR, 2, True),
            row(r"\text{left}", sl, W_COLOR, 2, True),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(np.array([3.0, 1.0, 0.0])).set_x(3.0)
        fx = MathTex(r"f(x)=|x|", font_size=MIN_FONT, color=INK).move_to(np.array([3.0, 2.4, 0.0]))

        for m in panel.get_family():
            m.update(0)
        self.add(axes, graph, line_r, line_l, origin, dot_r, dot_l, panel, fx)
        self.wait(1.5)
        for v in (0.5, 0.1):
            self.play(h.animate.set_value(v), run_time=2.0)
            self.wait(1.3)
        verdict = VGroup(MathTex(r"\text{two slopes,}", font_size=MIN_FONT, color=RESULT_COLOR), MathTex(r"\text{no tangent}", font_size=MIN_FONT, color=RESULT_COLOR)).arrange(DOWN, buff=0.15)
        verdict.move_to(np.array([3.0, -0.7, 0.0]))
        self.play(FadeIn(verdict), run_time=0.8)
        self.wait(1.5)
        # contrast with x^2
        g = lambda x: x * x
        hh = 0.1
        cmp0 = MathTex(r"x^2\ \text{at } h=0.1:", font_size=MIN_FONT, color=INK_DIM)
        cmp1 = MathTex(rf"{g(hh)/hh:+.2f}\ \text{{and}}\ {g(-hh)/(-hh):+.2f}", font_size=MIN_FONT, color=INK_DIM)
        cmp2 = MathTex(r"\text{both shrink to } 0", font_size=MIN_FONT, color=INK_DIM)
        VGroup(cmp0, cmp1, cmp2).arrange(DOWN, buff=0.15).move_to(np.array([3.0, -2.0, 0.0]))
        self.play(FadeIn(cmp0), FadeIn(cmp1), FadeIn(cmp2), run_time=0.8)
        self.wait(2.2)


# ---------------------------------------------------------------- SpeedGraph
def _s(t):
    tau = np.clip(t / 8.0, 0.0, 1.0)
    return 100.0 * (10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5)


def _v(t):
    """ds/dt of _s, worked out by hand: 100 * (30 tau^2 - 60 tau^3 + 30 tau^4) / 8."""
    tau = np.clip(t / 8.0, 0.0, 1.0)
    return 100.0 * (30 * tau**2 - 60 * tau**3 + 30 * tau**4) / 8.0


class SpeedGraph(Scene):
    """Speed drawn as a function: slope of s(t) traces v(t)."""

    def construct(self):
        ax_cfg = {"stroke_color": INK_DIM, "stroke_width": 2.5, "include_tip": False}
        top = Axes(x_range=[0, 8.001, 2], y_range=[0, 100.001, 50], x_length=6.4, y_length=1.8,
                   axis_config=ax_cfg).move_to(np.array([-0.5, 1.45, 0]))
        bot = Axes(x_range=[0, 8.001, 2], y_range=[0, 30.001, 15], x_length=6.4, y_length=1.8,
                   axis_config=ax_cfg).move_to(np.array([-0.5, -1.1, 0]))
        top.add_coordinates(font_size=MIN_FONT)
        bot.add_coordinates(font_size=MIN_FONT)
        for ax in (top, bot):
            for a in ax.get_axes():
                for n in getattr(a, "numbers", []):
                    n.set_color(INK_DIM)
        # no time numbers on the top axes (shared time axis)
        for n in getattr(top.x_axis, "numbers", []):
            n.set_opacity(0)
        s_lab = MathTex(r"s", font_size=MIN_FONT, color=V_COLOR).next_to(top.c2p(0, 100), RIGHT, buff=0.2)
        v_lab = MathTex(r"v", font_size=MIN_FONT, color=RESULT_COLOR).next_to(bot.c2p(0, 30), RIGHT, buff=0.2)
        t_lab = MathTex(r"t", font_size=MIN_FONT, color=X_COLOR).next_to(bot.c2p(8, 0), RIGHT, buff=0.15)
        s_curve = top.plot(_s, x_range=[0, 8], color=V_COLOR, stroke_width=4)
        t = ValueTracker(0.0)
        t.set_value(0.0)

        def tangent():
            tt = t.get_value()
            sl = _v(tt)
            a, b = max(0, tt - 1.2), min(8, tt + 1.2)
            return Line(top.c2p(a, _s(tt) + sl * (a - tt)), top.c2p(b, _s(tt) + sl * (b - tt)),
                        color=RESULT_COLOR, stroke_width=4)
        tan = always_redraw(tangent)
        dot_s = always_redraw(lambda: Dot(top.c2p(t.get_value(), _s(t.get_value())), color=RESULT_COLOR, radius=0.08))
        v_trace = always_redraw(lambda: bot.plot(_v, x_range=[0, max(0.01, t.get_value())],
                                                 color=RESULT_COLOR, stroke_width=4))
        dot_v = always_redraw(lambda: Dot(bot.c2p(t.get_value(), _v(t.get_value())), color=RESULT_COLOR, radius=0.08))
        guide = always_redraw(lambda: DashedLine(top.c2p(t.get_value(), 0), bot.c2p(t.get_value(), _v(t.get_value())),
                                                 color=INK_FAINT, stroke_width=2))
        read = always_redraw(lambda: MathTex(rf"v = {_v(t.get_value()):.1f}\ \text{{m/s}}",
                                             font_size=MIN_FONT, color=RESULT_COLOR
                                             ).move_to(np.array([-2.0, 2.2, 0])))
        self.add(top, bot, s_lab, v_lab, t_lab, s_curve, tan, dot_s, v_trace, dot_v, guide, read)
        self.wait(1.5)
        self.play(t.animate.set_value(8.0), run_time=10.0, rate_func=linear)
        self.wait(0.5)
        peak = MathTex(rf"\text{{fastest at }} t=4:\ {_v(4):.1f}\ \text{{m/s}}", font_size=MIN_FONT, color=INK)
        peak.move_to(np.array([2.1, -2.62, 0])) if False else None
        note = MathTex(r"v(t) = \text{slope of } s(t)", font_size=MIN_FONT, color=INK)
        note.move_to(np.array([-0.5, 0.15, 0]))
        self.play(FadeOut(read), run_time=0.4)
        self.play(FadeIn(note), run_time=0.8)
        top_peak = Dot(bot.c2p(4, _v(4)), color=HIGHLIGHT, radius=0.1)
        self.play(FadeIn(top_peak), run_time=0.6)
        self.wait(2.2)
