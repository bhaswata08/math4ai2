# JennysGrid: adapted from 3b1b/videos _2016/eola/chapter9.py JennysGrid and ShowOriginOfGrid, (c) 3Blue1Brown, CC BY-NC-SA 4.0
# TranslateFromJenny: adapted from 3b1b/videos _2016/eola/chapter9.py TranslateFromJenny, (c) 3Blue1Brown, CC BY-NC-SA 4.0
# TranslateToJenny: authored for this course (the reverse direction)

import numpy as np

from shared.anim.house import *

B1 = np.array([2.0, 1.0, 0.0])
B2 = np.array([-1.0, 1.0, 0.0])
HALF_W, HALF_H = 5.0, 5.625 / 2
JENNY = W_COLOR


def _clip(p, d):
    """Clip the line p + t d to the frame rectangle; return endpoints or None."""
    lo, hi = -1e9, 1e9
    for k, half in ((0, HALF_W), (1, HALF_H)):
        if abs(d[k]) < 1e-9:
            if abs(p[k]) > half:
                return None
            continue
        t1, t2 = (-half - p[k]) / d[k], (half - p[k]) / d[k]
        lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
    if lo >= hi:
        return None
    return p + lo * d, p + hi * d


def jenny_grid(origin=ORIGIN, scale=1.0):
    """Lines a*b1 + t*b2 and b*b2 + t*b1, clipped to the frame."""
    lines = VGroup()
    for n in range(-14, 15):
        for base, direction in ((B1, B2), (B2, B1)):
            seg = _clip(origin + n * scale * base, direction)
            if seg:
                lines.add(Line(seg[0], seg[1], stroke_color=JENNY,
                               stroke_width=2.5, stroke_opacity=0.5))
    return lines


def scaled_plane(origin, scale):
    plane = house_plane(x_range=[-24, 24, 1], y_range=[-14, 14, 1])
    plane.scale(scale, about_point=ORIGIN).shift(origin)
    return plane


def arrow(end, color, start=ORIGIN, width=6):
    return Arrow(start, end, buff=0, stroke_width=width,
                 max_tip_length_to_length_ratio=0.25, color=color).set_z_index(2)


def tag(mob, color=INK, pad=0.08):
    mob.set_color(color)
    mob.add_background_rectangle(color=BG, opacity=0.92, buff=pad)
    return mob.set_z_index(5)


def label(tex, color, **place):
    m = MathTex(tex, font_size=MIN_FONT)
    m.set_color(color)
    return tag(m)


def column(a, b, ca, cb):
    m = Matrix([[a], [b]], v_buff=0.6,
               element_to_mobject_config={"font_size": MIN_FONT})
    m.get_brackets().set_color(INK)
    m.get_entries()[0].set_color(ca)
    m.get_entries()[1].set_color(cb)
    return m


def card(*mobs, buff=0.15, edge=INK_FAINT, align=ORIGIN):
    g = VGroup(*mobs).arrange(DOWN, buff=0.15, aligned_edge=align)
    rect = RoundedRectangle(corner_radius=0.1, width=g.width + 2 * buff,
                            height=g.height + 2 * buff, fill_color=BG,
                            fill_opacity=0.95, stroke_color=edge, stroke_width=2)
    rect.move_to(g)
    return VGroup(rect, g).set_z_index(5)


def heading(l1, l2, color):
    return VGroup(Tex(l1, font_size=MIN_FONT, color=color),
                  Tex(l2, font_size=MIN_FONT, color=color)).arrange(DOWN, buff=0.05)


def caption(text):
    t = Tex(text, font_size=MIN_FONT, color=INK)
    c = card(t, buff=0.12)
    c.to_edge(DOWN, buff=0.32)
    return c


class JennysGrid(Scene):
    def construct(self):
        plane = house_plane()
        jg = jenny_grid()
        i_hat, j_hat = arrow(RIGHT, X_COLOR), arrow(UP, Y_COLOR)
        b1, b2 = arrow(B1, V_COLOR), arrow(B2, W_COLOR)
        i_l = label(r"\hat{\imath}", X_COLOR).next_to(i_hat, DOWN, buff=0.12).shift(RIGHT * 0.1)
        j_l = label(r"\hat{\jmath}", Y_COLOR).move_to(UP * 0.8 + RIGHT * 0.45)
        b1_l = label(r"\vec{b}_1", V_COLOR).next_to(b1.get_end(), RIGHT, buff=0.12)
        b2_l = label(r"\vec{b}_2", W_COLOR).move_to(np.array([-1.6, 0.5, 0]))

        sw_ours = Line(LEFT * 0.3, RIGHT * 0.3, color=GRID, stroke_width=4)
        sw_her = Line(LEFT * 0.3, RIGHT * 0.3, color=JENNY, stroke_width=4)
        legend = card(
            VGroup(sw_ours, Tex("ours", font_size=MIN_FONT, color=INK)).arrange(RIGHT, buff=0.2),
            VGroup(sw_her, Tex("Jennifer's", font_size=MIN_FONT, color=JENNY)).arrange(RIGHT, buff=0.2),
            align=LEFT,
        )
        legend.to_corner(UL, buff=0.32)

        origin_dot = Dot(ORIGIN, color=HIGHLIGHT, radius=0.1)

        cap = caption("same origin, two grids")
        self.add(plane, jg, i_hat, j_hat, b1, b2, i_l, j_l, b1_l, b2_l, legend, origin_dot, cap)
        self.wait(2.5)

        cap2 = caption("our first steps")
        self.play(FadeOut(cap), FadeIn(cap2), Indicate(i_hat, color=HIGHLIGHT),
                  Indicate(j_hat, color=HIGHLIGHT), run_time=1.5)
        self.wait(1)
        cap3 = caption("Jennifer's first steps")
        self.play(FadeOut(cap2), FadeIn(cap3), Indicate(b1, color=HIGHLIGHT),
                  Indicate(b2, color=HIGHLIGHT), run_time=1.5)
        self.wait(1)
        # her grid points: a*b1 + b*b2 for small integers
        pts = VGroup(*[
            Dot(a * B1 + b * B2, radius=0.06, color=JENNY).set_z_index(1)
            for a in range(-4, 5) for b in range(-4, 5)
            if abs((a * B1 + b * B2)[0]) < 4.7 and abs((a * B1 + b * B2)[1]) < 2.5
            and not (a == 0 and b == 0)
        ])
        cap4 = caption("her lattice points")
        self.play(FadeOut(cap3), FadeIn(cap4), FadeIn(pts), run_time=1.5)
        self.wait(3)


def hcard(l1, l2, color, col):
    """Wide card: two-line heading left, column vector right."""
    return card(VGroup(heading(l1, l2, color), col).arrange(RIGHT, buff=0.35))


class TranslateFromJenny(Scene):
    def construct(self):
        S, O = 0.8, np.array([-1.2, 0.7, 0.0])
        P = lambda v: O + S * np.asarray(v, dtype=float)
        plane = scaled_plane(O, S)
        jg = jenny_grid(O, S)
        b1, b2 = arrow(P(B1), V_COLOR, start=O), arrow(P(B2), W_COLOR, start=O)
        b1_l = label(r"\vec{b}_1", V_COLOR).next_to(b1.get_end(), RIGHT, buff=0.1)
        b2_l = label(r"\vec{b}_2", W_COLOR).next_to(b2.get_end(), UP, buff=0.1)
        origin_dot = Dot(O, color=HIGHLIGHT, radius=0.08).set_z_index(3)

        her = card(heading("Jennifer's", "coordinates", JENNY),
                   column("-1", "2", V_COLOR, W_COLOR))
        her.to_corner(UR, buff=0.32)
        self.add(plane, jg, b1, b2, b1_l, b2_l, her, origin_dot)
        self.wait(2.5)

        # first step: -1 * b1
        s1 = arrow(P(-B1), V_COLOR, start=O)
        s1_l = label(r"-1\cdot\vec{b}_1", V_COLOR).move_to(P(-B1) + np.array([1.0, -0.38, 0]))
        self.play(GrowArrow(s1), FadeIn(s1_l), run_time=1.8)
        self.wait(1.2)

        # second step from the tip: 2 * b2
        tip = -B1 + 2 * B2
        s2 = arrow(P(tip), W_COLOR, start=P(-B1))
        s2_l = label(r"2\cdot\vec{b}_2", W_COLOR).move_to(P(-B1) + np.array([-1.0, -0.38, 0]))
        self.play(GrowArrow(s2), FadeIn(s2_l), run_time=1.8)
        self.wait(1.2)

        # the tip on our grid
        res = arrow(P(tip), RESULT_COLOR, start=O, width=7)
        dx = DashedLine(P(tip), np.array([P(tip)[0], O[1], 0]), color=X_COLOR, stroke_width=5)
        dy = DashedLine(P(tip), np.array([O[0], P(tip)[1], 0]), color=Y_COLOR, stroke_width=5)
        ours = hcard("our", "coordinates", INK_DIM, column("-4", "1", X_COLOR, Y_COLOR))
        ours.to_corner(DL, buff=0.32)
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(b1_l), FadeOut(b2_l),
                  GrowArrow(res), run_time=1.5)
        self.play(Create(dx), Create(dy), run_time=1.2)
        self.play(FadeIn(ours), run_time=1)
        self.wait(4)


class TranslateToJenny(Scene):
    def construct(self):
        S, O = 0.9, np.array([-3.3, 0.2, 0.0])
        P = lambda v: O + S * np.asarray(v, dtype=float)
        plane = scaled_plane(O, S)
        jg = jenny_grid(O, S)
        target = np.array([3.0, 2.0, 0.0])
        b1, b2 = arrow(P(B1), V_COLOR, start=O), arrow(P(B2), W_COLOR, start=O)
        b1_l = label(r"\vec{b}_1", V_COLOR).next_to(P(B1), DOWN + RIGHT, buff=0.05)
        b2_l = label(r"\vec{b}_2", W_COLOR).next_to(P(B2), UP, buff=0.1)
        tgt = arrow(P(target), RESULT_COLOR, start=O, width=7)
        origin_dot = Dot(O, color=HIGHLIGHT, radius=0.08).set_z_index(3)

        ours = card(heading("our", "coordinates", INK_DIM),
                    column("3", "2", X_COLOR, Y_COLOR))
        ours.to_corner(UR, buff=0.32)

        def stage(*mobs):
            return VGroup(*mobs).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        s1 = VGroup(MathTex(r"a\,\vec{b}_1 + b\,\vec{b}_2 =", font_size=MIN_FONT, color=INK),
                    column("3", "2", X_COLOR, Y_COLOR)).arrange(RIGHT, buff=0.3)
        s2 = stage(MathTex(r"2a - b = 3", font_size=MIN_FONT, color=INK),
                   MathTex(r"a + b = 2", font_size=MIN_FONT, color=INK))
        s3 = stage(MathTex(r"a = 5/3", font_size=MIN_FONT, color=V_COLOR),
                   MathTex(r"b = 1/3", font_size=MIN_FONT, color=W_COLOR))
        hers = VGroup(heading("Jennifer's", "coordinates", JENNY),
                      column("5/3", "1/3", V_COLOR, W_COLOR)
                      ).arrange(RIGHT, buff=0.35)
        slot = RoundedRectangle(corner_radius=0.1, width=5.4, height=1.6,
                                fill_color=BG, fill_opacity=0.95,
                                stroke_color=INK_FAINT, stroke_width=2).set_z_index(5)
        slot.to_corner(DL, buff=0.32)
        for m in (s1, s2, s3, hers):
            m.move_to(slot).set_z_index(6)

        self.add(plane, jg, b1, b2, b1_l, b2_l, tgt, ours, slot, s1, origin_dot)
        self.wait(2.5)

        self.play(FadeOut(s1), FadeIn(s2), run_time=1)
        self.wait(2.2)
        self.play(FadeOut(s2), FadeIn(s3), run_time=1)
        self.wait(1.2)

        # stretch b1 to (5/3) b1, then (1/3) b2 from its tip
        a_end = (5 / 3) * B1
        b1_big = arrow(P(a_end), V_COLOR, start=O)
        b1_big_l = label(r"\frac{5}{3}\vec{b}_1", V_COLOR).move_to(P(a_end * 0.6) + np.array([0.5, -0.5, 0]))
        b2_small = arrow(P(a_end + B2 / 3), W_COLOR, start=P(a_end), width=6)
        b2_small_l = label(r"\frac{1}{3}\vec{b}_2", W_COLOR).next_to(P(a_end), RIGHT, buff=0.12)
        self.play(Transform(b1, b1_big), FadeOut(b1_l), FadeIn(b1_big_l),
                  tgt.animate.set_opacity(0.4), run_time=1.8)
        self.play(Transform(b2, b2_small), FadeOut(b2_l), FadeIn(b2_small_l), run_time=1.8)
        self.play(FadeOut(s3), FadeIn(hers), run_time=1)
        self.wait(4)
