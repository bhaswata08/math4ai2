# BasisDefinition: authored for this course, from the definition in 3b1b _2016/eola/chapter2.py TechnicalDefinitionOfBasis, (c) 3Blue1Brown, CC BY-NC-SA 4.0
# SameVectorTwoBases: adapted from 3b1b _2016/eola/chapter2.py WhatIfWeChoseADifferentBasis, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *

HX, HY = 5.0, 5.625 / 2  # half frame
B1 = np.array([2.0, 1.0, 0.0])
B2 = np.array([-1.0, 1.0, 0.0])


def clip_segment(p, d, hx=HX, hy=HY):
    """Part of the line p + t d inside the frame box, as (start, end) or None."""
    t0, t1 = -1e3, 1e3
    for k, h in ((0, hx), (1, hy)):
        if abs(d[k]) < 1e-9:
            if abs(p[k]) > h:
                return None
            continue
        a, b = (-h - p[k]) / d[k], (h - p[k]) / d[k]
        t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
    if t0 >= t1:
        return None
    return p + t0 * d, p + t1 * d


def skew_grid(b1, b2, color=W_COLOR, opacity=0.45, n=12):
    """Lines a*b1 + t*b2 and t*b1 + b*b2 for integer a, b, clipped to the frame."""
    lines = VGroup()
    for i in range(-n, n + 1):
        for p, d in ((i * b1, b2), (i * b2, b1)):
            seg = clip_segment(p, d)
            if seg:
                lines.add(Line(*seg, stroke_color=color, stroke_width=2.5,
                               stroke_opacity=opacity))
    return lines


def vec(v, color, width=7):
    return Arrow(ORIGIN, v, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.25)


def lab(tex, at, direction, color):
    m = MathTex(tex, font_size=MIN_FONT, color=color)
    m.next_to(at, direction, buff=0.12)
    m.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)
    return m


def card(*lines, pos=None, **kw):
    """Text on a background card. Each line is a Tex string."""
    rows = VGroup(*[Tex(s, font_size=MIN_FONT, color=INK) for s in lines])
    rows.arrange(DOWN, buff=0.12)
    box = RoundedRectangle(corner_radius=0.1, width=rows.width + 0.4,
                           height=rows.height + 0.3, fill_color=BG,
                           fill_opacity=0.95, stroke_color=INK_FAINT,
                           stroke_width=2)
    box.move_to(rows)
    g = VGroup(box, rows)
    if pos is not None:
        g.move_to(pos)
    return g


class BasisDefinition(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        def caption(*lines):
            c = card(*lines)
            c.to_edge(DOWN, buff=0.35)
            return c

        def verdict(text):
            c = card(text)
            c.to_corner(UL, buff=0.35)
            return c

        # Frame 1: givens, the standard basis and the definition
        i_arr, j_arr = vec(RIGHT, X_COLOR), vec(UP, Y_COLOR)
        i_lab = lab(r"\hat\imath", RIGHT, DR, X_COLOR)
        j_lab = lab(r"\hat\jmath", UP, UL, Y_COLOR)
        cap = caption(r"A basis: linearly independent vectors", r"that span the space")
        self.add(i_arr, j_arr, i_lab, j_lab, cap)
        self.wait(2.5)

        # 1. standard basis
        cap2 = caption(r"$\hat\imath,\hat\jmath$ are independent", r"and span the plane")
        v1 = verdict("a basis")
        self.play(FadeOut(cap), FadeIn(cap2), FadeIn(v1), run_time=0.8)
        self.wait(2)

        # 2. b1, b2 with skewed grid
        b1, b2 = vec(B1, V_COLOR), vec(B2, W_COLOR)
        b1l = lab(r"\vec b_1", B1, DR, V_COLOR)
        b2l = lab(r"\vec b_2", B2, UL, W_COLOR)
        grid = skew_grid(B1, B2)
        cap3 = caption(r"$\vec b_1,\vec b_2$ are independent too:", r"their combinations fill the plane")
        self.play(FadeOut(VGroup(i_arr, j_arr, i_lab, j_lab, cap2, v1)),
                  plane.animate.set_opacity(0.35),
                  FadeIn(grid), FadeIn(VGroup(b1, b2, b1l, b2l)),
                  FadeIn(cap3), run_time=1.5)
        v2 = verdict("a basis")
        self.play(FadeIn(v2), run_time=0.4)
        self.wait(3)

        # 3. parallel pair
        P2 = 0.5 * B1
        p2 = vec(P2, W_COLOR)
        p2l = lab(r"\vec b_2", P2, DR, W_COLOR)
        b1l_up = lab(r"\vec b_1", B1, UL, V_COLOR)
        line = Line(*clip_segment(ORIGIN, B1), stroke_color=INK_DIM, stroke_width=4,
                    stroke_opacity=0.8)
        cap4 = caption(r"Parallel vectors: the span is", r"only a line")
        v3 = verdict("not a basis")
        self.play(FadeOut(VGroup(grid, b2, b2l, b1l, cap3, v2)),
                  plane.animate.set_opacity(1),
                  FadeIn(line), FadeIn(p2), FadeIn(p2l), FadeIn(b1l_up),
                  FadeIn(cap4), FadeIn(v3), run_time=1.5)
        self.add(b1, p2)  # keep b1 under p2 ordering stable
        self.wait(3)

        # 4. three vectors in the plane
        T = B1 + B2
        b2n, b2nl = vec(B2, W_COLOR), lab(r"\vec b_2", B2, UL, W_COLOR)
        b3, b3l = vec(T, RESULT_COLOR), lab(r"\vec b_3", T, RIGHT, RESULT_COLOR)
        b1l2 = lab(r"\vec b_1", B1, DR, V_COLOR)
        cap5 = caption(r"Three vectors span the plane, but", r"one is redundant: $\vec b_3=\vec b_1+\vec b_2$")
        v4 = verdict("not a basis")
        self.play(FadeOut(VGroup(line, p2, p2l, b1l_up, cap4, v3)),
                  FadeIn(VGroup(b2n, b2nl, b3, b3l, b1l2, cap5, v4)), run_time=1.5)
        self.wait(3.5)


class SameVectorTwoBases(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)
        X = np.array([3.0, 2.0, 0.0])

        def caption(*lines):
            c = card(*lines)
            c.to_edge(DOWN, buff=0.35)
            return c

        x_arr = vec(X, RESULT_COLOR, 8)
        x_lab = lab(r"\vec x", X, UR, RESULT_COLOR)

        # Frame 1: arrow, standard basis, coordinates
        i_arr, j_arr = vec(RIGHT, X_COLOR), vec(UP, Y_COLOR)
        i_lab = lab(r"\hat\imath", RIGHT, DR, X_COLOR)
        j_lab = lab(r"\hat\jmath", UP, UL, Y_COLOR)
        cap = caption(r"In $\hat\imath,\hat\jmath$ coordinates: $(3,\,2)$")
        self.add(x_arr, x_lab, i_arr, j_arr, i_lab, j_lab, cap)
        self.wait(1.5)

        # 3 i-hat then 2 j-hat
        s1 = Line(ORIGIN, 3 * RIGHT, stroke_color=X_COLOR, stroke_width=8)
        s2 = Line(3 * RIGHT, X, stroke_color=Y_COLOR, stroke_width=8)
        cap2 = caption(r"$\vec x = 3\,\hat\imath + 2\,\hat\jmath$")
        self.play(FadeOut(cap), FadeIn(cap2), Create(s1), run_time=1.2)
        self.play(Create(s2), run_time=1.2)
        self.wait(1.5)

        # switch to the b1, b2 grid
        b1, b2 = vec(B1, V_COLOR), vec(B2, W_COLOR)
        b1l = lab(r"\vec b_1", B1, DR, V_COLOR)
        b2l = lab(r"\vec b_2", B2, UL, W_COLOR)
        grid = skew_grid(B1, B2)
        cap3 = caption(r"Same arrow, new grid: $\vec b_1,\vec b_2$")
        self.play(FadeOut(VGroup(i_arr, j_arr, i_lab, j_lab, s1, s2, cap2)),
                  plane.animate.set_opacity(0.3),
                  FadeIn(grid), FadeIn(VGroup(b1, b2, b1l, b2l, cap3)),
                  run_time=1.5)
        self.wait(1)
        self.bring_to_front(x_arr)
        t1 = Line(ORIGIN, B1 * 5 / 3, stroke_color=V_COLOR, stroke_width=8)
        t2 = Line(B1 * 5 / 3, X, stroke_color=W_COLOR, stroke_width=8)
        cap4 = caption(r"$\vec x = \tfrac53\,\vec b_1 + \tfrac13\,\vec b_2$")
        self.play(FadeOut(cap3), FadeIn(cap4), Create(t1), run_time=1.2)
        self.play(Create(t2), run_time=1.2)
        self.wait(1.2)
        cap5 = caption(r"In $\vec b_1,\vec b_2$ coordinates: $(\tfrac53,\,\tfrac13)$")
        self.play(FadeOut(cap4), FadeIn(cap5), run_time=0.8)
        self.wait(2.5)
