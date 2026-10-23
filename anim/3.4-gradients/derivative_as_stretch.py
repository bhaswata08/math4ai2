# Adapted from 3b1b/videos _2018/alt_calc.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *


class GraphVsTransform(Scene):
    def construct(self):
        # -------------------------------------------------------------
        # Left side: The graph view of f(x) = x^2 (~4 units tall, centered)
        # -------------------------------------------------------------
        left_center_x = -2.50

        axes = Axes(
            x_range=[0, 2.2, 1],
            y_range=[0, 4.2, 1],
            x_length=3.6,
            y_length=3.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.2,
                "include_ticks": True,
                "tick_size": 0.08,
            },
            tips=False,
        ).move_to(np.array([left_center_x, -0.05, 0.0]))

        # Coordinate labels with background rectangles
        lbl_x1 = MathTex("1", font_size=MIN_FONT, color=INK_DIM)
        lbl_x1.next_to(axes.c2p(1, 0), DOWN, buff=0.15)
        lbl_x1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_x2 = MathTex("2", font_size=MIN_FONT, color=INK_DIM)
        lbl_x2.next_to(axes.c2p(2, 0), DOWN, buff=0.15)
        lbl_x2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y1 = MathTex("1", font_size=MIN_FONT, color=INK_DIM)
        lbl_y1.next_to(axes.c2p(0, 1), LEFT, buff=0.15)
        lbl_y1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y4 = MathTex("4", font_size=MIN_FONT, color=INK_DIM)
        lbl_y4.next_to(axes.c2p(0, 4), LEFT, buff=0.15)
        lbl_y4.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        curve = axes.plot(lambda x: x**2, x_range=[0, 2.02], color=V_COLOR, stroke_width=3.5)
        curve_lbl = MathTex(r"f(x) = x^2", font_size=MIN_FONT, color=V_COLOR)
        curve_lbl.move_to(axes.c2p(1.10, 3.40))
        curve_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        pt_1 = axes.c2p(1, 1)
        dot_1 = Dot(pt_1, radius=0.08, color=RESULT_COLOR)
        dot_1.set_z_index(5)

        dash_v = DashedLine(axes.c2p(1, 0), pt_1, color=INK_FAINT, stroke_width=1.8)
        dash_h = DashedLine(axes.c2p(0, 1), pt_1, color=INK_FAINT, stroke_width=1.8)

        # Tangent line at x = 1 (slope = 2)
        tangent = axes.plot(lambda x: 2 * x - 1, x_range=[0.45, 1.80], color=RESULT_COLOR, stroke_width=3.5)
        tangent.set_z_index(4)

        slope_lbl = MathTex(r"\text{slope} = 2", font_size=MIN_FONT, color=RESULT_COLOR)
        slope_lbl.move_to(axes.c2p(0.62, 2.3))
        slope_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # -------------------------------------------------------------
        # Right side: The transformation view (~4.5 units wide, centered)
        # -------------------------------------------------------------
        right_center_x = 2.45
        in_y = 0.85
        out_y = -1.95

        in_line = NumberLine(
            x_range=[0, 2.2, 0.5],
            length=4.4,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([right_center_x, in_y, 0.0]))

        in_tag = MathTex(r"x", font_size=MIN_FONT + 2, color=V_COLOR)
        in_tag.next_to(in_line, LEFT, buff=0.20)
        in_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        in_nums = VGroup()
        for val in [0, 1, 2]:
            lbl = MathTex(str(val), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(in_line.n2p(val), UP, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            in_nums.add(lbl)

        out_line = NumberLine(
            x_range=[0, 4.4, 1.0],
            length=4.4,
            color=INK_DIM,
            stroke_width=2.2,
            include_ticks=True,
            tick_size=0.08,
        ).move_to(np.array([right_center_x, out_y, 0.0]))

        out_tag = MathTex(r"x^2", font_size=MIN_FONT + 2, color=RESULT_COLOR)
        out_tag.next_to(out_line, LEFT, buff=0.20)
        out_tag.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        out_nums = VGroup()
        for val in [0, 1, 2, 3, 4]:
            lbl = MathTex(str(val), font_size=MIN_FONT, color=INK_DIM)
            lbl.next_to(out_line.n2p(val), DOWN, buff=0.15)
            lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
            out_nums.add(lbl)

        # Input dots
        x_vals = np.linspace(0.0, 2.0, 11)
        ghost_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.065, color=V_COLOR).set_opacity(0.35)
            for x in x_vals
        ])

        moving_dots = VGroup(*[
            Dot(in_line.n2p(x), radius=0.075, color=V_COLOR)
            for x in x_vals
        ])
        moving_dots.set_z_index(5)

        # Frame 0: All givens visible!
        self.add(
            axes, lbl_x1, lbl_x2, lbl_y1, lbl_y4, curve, curve_lbl,
            dash_v, dash_h, dot_1,
            in_line, in_tag, in_nums, out_line, out_tag, out_nums,
            moving_dots
        )
        self.wait(1.0)

        # 1. Left side: tangent line and slope
        self.play(Create(tangent), FadeIn(slope_lbl), run_time=1.5)
        self.wait(0.6)

        # 2. Right side: ghost dots appear, moving dots flow along arcs to output line
        self.add(ghost_dots)
        self.bring_to_front(moving_dots)
        move_anims = [
            dot.animate(path_arc=-0.35).move_to(out_line.n2p(x**2)).set_color(RESULT_COLOR)
            for dot, x in zip(moving_dots, x_vals)
        ]
        self.play(LaggedStart(*move_anims, lag_ratio=0.12, run_time=3.5))
        self.wait(0.8)

        # 3. Momentary highlight at x = 1 (on tangent, graph dot, and output dot at 1)
        dot_1_out = moving_dots[5]  # x = 1.0 is index 5
        self.play(
            tangent.animate.set_color(HIGHLIGHT),
            dot_1_out.animate.set_color(HIGHLIGHT).scale(1.3),
            dot_1.animate.set_color(HIGHLIGHT).scale(1.3),
            run_time=0.4,
        )
        self.play(
            tangent.animate.set_color(RESULT_COLOR),
            dot_1_out.animate.set_color(RESULT_COLOR).scale(1 / 1.3),
            dot_1.animate.set_color(RESULT_COLOR).scale(1 / 1.3),
            run_time=0.4,
        )
        # x = 1 maps to 1: link the graph dot to the output dot
        link = DashedLine(pt_1, out_line.n2p(1), color=HIGHLIGHT, stroke_width=2.5)
        self.play(Create(link), run_time=1.2)
        self.wait(4.0)


def _fmt(v):
    """Tick text for a number: 2 decimals at most, no trailing zeros."""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _bg(m, opacity=0.85):
    m.add_background_rectangle(color=BG, opacity=opacity, buff=0.08)
    return m


def _zoom_line(values, center_val, center_x, y, scale, label_dir, label_vals, pad=0.05):
    """A number line at a fixed scale (screen units per number unit), shifted
    so that center_val sits at center_x, with ticks and labels at label_vals."""
    lo, hi = min(values) - pad, max(values) + pad
    line = NumberLine(
        x_range=[lo, hi, 1], length=(hi - lo) * scale,
        color=INK_DIM, stroke_width=2.2, include_ticks=False,
    )
    line.shift(np.array([center_x - line.n2p(center_val)[0], y - line.n2p(center_val)[1], 0.0]))
    ticks = VGroup(*[line.get_tick(v, 0.08) for v in label_vals])
    ticks.set_color(INK_DIM)
    nums = VGroup()
    for v in label_vals:
        lbl = MathTex(_fmt(v), font_size=MIN_FONT, color=INK_DIM)
        lbl.next_to(line.n2p(v), label_dir, buff=0.15)
        nums.add(_bg(lbl))
    return line, VGroup(ticks, nums)


class ZoomStretch(Scene):
    def construct(self):
        f = lambda x: x ** 2
        S = 6.5               # screen units per number unit, same on both lines
        center_x = 0.40
        in_y, out_y = 0.55, -1.15
        readout_y = 2.15
        h = 0.10              # the nudge shown by the braces
        ks = [-2, -1, 0, 1, 2]

        in_tag = _bg(MathTex(r"x", font_size=MIN_FONT, color=V_COLOR).move_to(np.array([-4.35, in_y, 0.0])))
        out_tag = _bg(MathTex(r"x^2", font_size=MIN_FONT, color=RESULT_COLOR).move_to(np.array([-4.35, out_y, 0.0])))

        def build(x0):
            xs = [x0 + k * h / 2 for k in ks]
            ys = [f(x) for x in xs]
            in_line, in_lab = _zoom_line(xs, x0, center_x, in_y, S, UP, [x0 - h, x0, x0 + h])
            out_line, out_lab = _zoom_line(ys, f(x0), center_x, out_y, S, DOWN, [f(x0 - h), f(x0), f(x0 + h)])
            dots = VGroup(*[Dot(in_line.n2p(x), radius=0.075, color=V_COLOR) for x in xs])
            dots.set_z_index(5)
            ghosts = VGroup(*[Dot(in_line.n2p(x), radius=0.065, color=V_COLOR).set_opacity(0.35) for x in xs])
            land = [out_line.n2p(y) for y in ys]
            # braces: input gap x0 -> x0+h, output gap f(x0) -> f(x0+h)
            gap_in = f(x0 + h) - f(x0)
            b_in = Brace(Line(in_line.n2p(x0), in_line.n2p(x0 + h)), DOWN, buff=0.1, color=INK_DIM)
            t_in = _bg(MathTex(_fmt(h), font_size=MIN_FONT, color=V_COLOR).next_to(b_in, DOWN, buff=0.08))
            b_out = Brace(Line(out_line.n2p(f(x0)), out_line.n2p(f(x0 + h))), UP, buff=0.1, color=INK_DIM)
            t_out = _bg(MathTex(_fmt(gap_in), font_size=MIN_FONT, color=RESULT_COLOR).next_to(b_out, UP, buff=0.08))
            ratio = gap_in / h
            shown = round(ratio)
            read = MathTex(
                rf"\frac{{{_fmt(gap_in)}}}{{{_fmt(h)}}} \approx {shown} = f'({_fmt(x0)}) \cdot 1"
                if False else rf"{_fmt(gap_in)} / {_fmt(h)} \approx {shown} \approx f'({_fmt(x0)}) = {_fmt(2 * x0)}",
                font_size=MIN_FONT + 2, color=RESULT_COLOR,
            ).move_to(np.array([center_x, readout_y, 0.0]))
            _bg(read)
            return dict(in_line=in_line, in_lab=in_lab, out_line=out_line, out_lab=out_lab, dots=dots,
                        ghosts=ghosts, land=land, braces=VGroup(b_in, t_in, b_out, t_out), read=read, x0=x0)

        def intro_text(x0):
            return _bg(MathTex(rf"\text{{near }} x = {_fmt(x0)}", font_size=MIN_FONT + 2, color=INK_DIM)
                       .move_to(np.array([center_x, readout_y, 0.0])))

        hold = [3.0, 3.5]
        prev = None
        for i, x0 in enumerate([1.0, 3.0]):
            st = build(x0)
            intro = intro_text(x0)
            group_in = VGroup(st["in_line"], st["in_lab"], st["out_line"], st["out_lab"], st["dots"], intro)
            if prev is None:
                self.add(in_tag, out_tag, group_in)
                self.wait(1.2)
            else:
                self.play(FadeOut(prev), run_time=0.6)
                self.wait(0.2)
                self.play(FadeIn(group_in), run_time=0.8)
                self.wait(1.0)
            self.add(st["ghosts"])
            self.bring_to_front(st["dots"])
            self.play(
                *[d.animate(path_arc=-0.25).move_to(p).set_color(RESULT_COLOR) for d, p in zip(st["dots"], st["land"])],
                run_time=2.2,
            )
            self.wait(0.6)
            self.play(FadeIn(st["braces"]), run_time=1.0)
            self.wait(1.0)
            self.play(FadeOut(intro), run_time=0.3)
            self.play(FadeIn(st["read"]), run_time=0.6)
            self.wait(hold[i])
            prev = VGroup(st["in_line"], st["in_lab"], st["out_line"], st["out_lab"], st["dots"],
                          st["ghosts"], st["braces"], st["read"])
        self.wait(1.0)


class NegativeStretch(Scene):
    def construct(self):
        f = lambda x: x ** 2
        S = 10.67
        center_x = 0.40
        in_y, out_y = 0.45, -0.85

        readout = _bg(MathTex(r"f'(-1) = -2", font_size=MIN_FONT + 4, color=RESULT_COLOR).move_to(np.array([center_x, 2.2, 0.0])))

        in_tag = _bg(MathTex(r"x", font_size=MIN_FONT, color=V_COLOR).move_to(np.array([-4.35, in_y, 0.0])))
        out_tag = _bg(MathTex(r"x^2", font_size=MIN_FONT, color=RESULT_COLOR).move_to(np.array([-4.35, out_y, 0.0])))

        xs = np.linspace(-1.10, -0.90, 5)
        ys = [f(x) for x in xs]
        in_line, in_lab = _zoom_line(list(xs), -1.0, center_x, in_y, S, UP, [-1.1, -1.0, -0.9])
        out_line, out_lab = _zoom_line(ys, 1.0, center_x, out_y, S, DOWN, [f(-0.9), 1.0, f(-1.1)])

        dot_colors = [interpolate_color(ManimColor(X_COLOR), ManimColor(Y_COLOR), i / 4) for i in range(5)]
        input_dots = VGroup(*[Dot(in_line.n2p(x), radius=0.08, color=c) for x, c in zip(xs, dot_colors)])
        input_dots.set_z_index(5)
        ghost_dots = VGroup(*[Dot(in_line.n2p(x), radius=0.07, color=c).set_opacity(0.35)
                              for x, c in zip(xs, dot_colors)])
        land = [out_line.n2p(y) for y in ys]

        in_dist = abs(in_line.n2p(xs[-1])[0] - in_line.n2p(xs[0])[0])
        out_dist = abs(out_line.n2p(ys[-1])[0] - out_line.n2p(ys[0])[0])
        assert abs(out_dist / in_dist - 2.0) / 2.0 < 0.10, out_dist / in_dist

        arrow_in = Arrow(np.array([in_line.n2p(xs[0])[0], 1.55, 0.0]), np.array([in_line.n2p(xs[-1])[0], 1.55, 0.0]),
                         color=INK, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        arrow_in_lbl = _bg(MathTex(r"\text{original order}", font_size=MIN_FONT, color=INK).next_to(arrow_in, RIGHT, buff=0.2))

        arrow_out = Arrow(np.array([out_line.n2p(ys[0])[0], -1.85, 0.0]), np.array([out_line.n2p(ys[-1])[0], -1.85, 0.0]),
                          color=RESULT_COLOR, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        arrow_out_lbl = _bg(MathTex(r"\text{order reversed}", font_size=MIN_FONT, color=RESULT_COLOR).next_to(arrow_out, DOWN, buff=0.1))

        self.add(readout, in_tag, out_tag, in_line, in_lab, out_line, out_lab, input_dots, arrow_in, arrow_in_lbl)
        self.wait(1.5)

        self.add(ghost_dots)
        self.bring_to_front(input_dots)
        self.play(*[d.animate(path_arc=-0.25).move_to(p) for d, p in zip(input_dots, land)], run_time=3.0)
        self.wait(1.0)

        self.play(Create(arrow_out), FadeIn(arrow_out_lbl), run_time=1.5)
        self.wait(1.5)
        self.play(input_dots.animate.scale(1.25), run_time=0.4)
        self.play(input_dots.animate.scale(1 / 1.25), run_time=0.4)
        self.wait(2.0)
