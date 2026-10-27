# Block 1.3, polynomials as a vector space. Storyline and visuals rebuilt
# from Quantum Sense, "Maths of Quantum Mechanics" ch. 3 "Why do we need a
# Hilbert Space?" (youtube.com/watch?v=_kJUUxjJ_FY, 2:00-5:12). No source was
# published, so the scenes are authored here, in plain notation (no bra-ket).

import math

import numpy as np

from shared.anim.house import *

POLY_COLOR = V_COLOR      # the polynomial space and its members
FUNC_COLOR = INK_DIM      # the larger space of all functions
SUB_COLOR = RESULT_COLOR  # degree <= 2, the subspace inside polynomials


def mt(tex, color=INK, size=MIN_FONT):
    return MathTex(tex, font_size=size, color=color)


def label(text, color=INK_DIM, size=MIN_FONT):
    return Tex(text, font_size=size, color=color)


class PolynomialSpace(Scene):
    """Polynomials add and scale like arrows do."""

    def construct(self):
        title = label("polynomials").to_edge(UP, buff=0.3)
        spots = [
            (r"2 + x - 0.45x^4", [-3.0, 1.3]),
            (r"x^3 + 3.1x^2", [2.9, 1.5]),
            (r"-2.3 - x^2", [-3.3, -0.4]),
            (r"5x^6", [3.4, -0.2]),
            (r"3 + 0.2x^2 - 99x^5", [-3.45, -2.3]),
            (r"x - 7", [3.3, -2.3]),
        ]
        crowd = VGroup(*[mt(t, INK_DIM).move_to([x, y, 0]) for t, (x, y) in spots])
        self.add(title, crowd)
        self.wait(1.5)

        p = mt(r"p = 1 + 2x", POLY_COLOR)
        q = mt(r"q = 3 - x^2", W_COLOR)
        VGroup(p, q).arrange(DOWN, buff=0.35).move_to(UP * 0.6)
        self.play(crowd.animate.set_opacity(0.18), FadeIn(p, shift=UP * 0.2), FadeIn(q, shift=UP * 0.2))
        self.wait(1)

        add = mt(r"p + q = 4 + 2x - x^2", RESULT_COLOR).next_to(q, DOWN, buff=0.55)
        self.play(Write(add))
        self.wait(0.8)
        scale = mt(r"2p = 2 + 4x", RESULT_COLOR).next_to(add, DOWN, buff=0.3)
        self.play(Write(scale))
        self.wait(0.8)

        verdict = label(r"still polynomials", HIGHLIGHT).next_to(scale, DOWN, buff=0.4)
        self.play(FadeIn(verdict), Indicate(add, color=HIGHLIGHT), Indicate(scale, color=HIGHLIGHT))
        self.wait(1)
        self.play(verdict.animate.set_color(RESULT_COLOR))

        zero = mt(r"\text{zero vector: } 0", INK).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(zero))
        self.wait(2)


class PolynomialCoordinates(Scene):
    """1, x, x^2, ... are the building blocks; the scalars on them are the coordinates."""

    def construct(self):
        blocks = mt(r"1,\; x,\; x^2,\; x^3,\; x^4,\; x^5,\; \dots", POLY_COLOR).to_edge(UP, buff=0.45)
        cap = label("building blocks").next_to(blocks, DOWN, buff=0.15)
        poly = mt(r"3 + 0.2x^2 - 99x^5").move_to(UP * 0.35)
        self.add(blocks, cap, poly)
        self.wait(1.5)

        # Same polynomial, every block written out with its scalar.
        parts = [r"3", r"\cdot 1", r"+", r"0", r"\cdot x", r"+", r"0.2", r"\cdot x^2",
                 r"+", r"0", r"\cdot x^3", r"+", r"0", r"\cdot x^4", r"-", r"99", r"\cdot x^5"]
        full = MathTex(*parts, font_size=MIN_FONT, color=INK).move_to(DOWN * 0.6)
        for i in (0, 3, 6, 9, 12, 15):
            full[i].set_color(RESULT_COLOR)
        for i in (1, 4, 7, 10, 13, 16):
            full[i].set_color(POLY_COLOR)
        self.play(TransformFromCopy(poly, full), run_time=1.5)
        self.wait(1.5)

        coords = mt(r"(3,\; 0,\; 0.2,\; 0,\; 0,\; -99)", RESULT_COLOR).move_to(DOWN * 1.9)
        arrow = Arrow(full.get_bottom(), coords.get_top(), buff=0.1, color=INK_DIM, stroke_width=4)
        scalars = VGroup(*[full[i] for i in (0, 3, 6, 9, 12, 15)])
        self.play(GrowArrow(arrow), TransformFromCopy(scalars, coords), run_time=1.5)
        self.wait(1)

        note = label(r"a polynomial is a list of scalars", HIGHLIGHT).move_to(DOWN * 2.55)
        self.play(coords.animate.shift(UP * 0.15), FadeIn(note))
        self.wait(2.5)


def exp_partial(n):
    def f(x):
        return sum(x**k / math.factorial(k) for k in range(n + 1))
    return f


class ExpFromPolynomials(Scene):
    """Add one block at a time: every step is a polynomial, and they close in on e^x."""

    def construct(self):
        axes = Axes(
            x_range=[-3, 2.5, 1], y_range=[-1, 7, 1],
            x_length=4.6, y_length=4.6,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 3, "include_ticks": True},
            tips=False,
        ).move_to(RIGHT * 2.5 + DOWN * 0.1)
        target = axes.plot(np.exp, x_range=[-3, np.log(7)], color=W_COLOR, stroke_width=4)
        target = DashedVMobject(target, num_dashes=40)
        target.set_stroke(opacity=0.7)
        e_label = mt(r"e^x", W_COLOR).next_to(axes.c2p(1.5, 6.3), LEFT, buff=0.25)

        terms = [r"p(x) = 1", r"+\, x", r"+\, x^2/2", r"+\, x^3/6",
                 r"+\, x^4/24", r"+\, x^5/120", r"+\, x^6/720", r"+\, \dots"]
        rows = [[0, 1], [2, 3], [4, 5], [6, 7]]
        tex = [mt(t, POLY_COLOR) for t in terms]
        lines = VGroup(*[VGroup(*[tex[i] for i in r]).arrange(RIGHT, buff=0.2) for r in rows])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.35).shift(UP * 0.3)
        lines[1:].shift(RIGHT * 0.95)

        def curve(n):
            f = exp_partial(n)
            xs = np.linspace(-3, 2.5, 200)
            ok = [x for x in xs if -1 <= f(x) <= 7]
            return axes.plot(f, x_range=[min(ok), max(ok)], color=RESULT_COLOR, stroke_width=5)

        count = mt(r"\text{degree } 0", INK_DIM).to_corner(DL, buff=0.35)
        cur = curve(0)
        self.add(axes, target, e_label, tex[0], cur, count)
        self.wait(1.5)

        for n in range(1, 7):
            new_count = mt(rf"\text{{degree }} {n}", INK_DIM).move_to(count, aligned_edge=LEFT)
            self.play(
                FadeIn(tex[n], shift=LEFT * 0.2),
                Transform(cur, curve(n)),
                Transform(count, new_count),
                run_time=1.1 if n < 4 else 0.8,
            )
            self.wait(0.6 if n < 4 else 0.3)
        self.play(FadeIn(tex[7]))
        self.wait(0.8)

        note = label(r"each step: a polynomial", RESULT_COLOR).move_to(count, aligned_edge=LEFT)
        self.play(FadeOut(count), FadeIn(note), Indicate(e_label, color=HIGHLIGHT))
        self.wait(2.5)


class PolynomialSubspace(Scene):
    """Spaces inside spaces: degree <= 2 inside polynomials inside all functions.
    The partial sums of e^x walk out of the inner box, stay inside polynomials,
    and pile up at its wall; their limit e^x is just outside."""

    def construct(self):
        funcs = RoundedRectangle(width=9.6, height=5.2, corner_radius=0.3,
                                 stroke_color=FUNC_COLOR, stroke_width=3)
        polys = RoundedRectangle(width=6.6, height=3.6, corner_radius=0.3,
                                 stroke_color=POLY_COLOR, stroke_width=3,
                                 fill_color=POLY_COLOR, fill_opacity=0.08).move_to(LEFT * 1.3 + DOWN * 0.35)
        sub = RoundedRectangle(width=2.6, height=2.3, corner_radius=0.25,
                               stroke_color=SUB_COLOR, stroke_width=3,
                               fill_color=SUB_COLOR, fill_opacity=0.08)
        sub.move_to(polys.get_left() + RIGHT * 1.55 + DOWN * 0.3)
        f_lab = label("all functions", FUNC_COLOR).next_to(funcs.get_corner(UL), DR, buff=0.18)
        p_lab = label("polynomials", POLY_COLOR).next_to(polys.get_corner(UL), DR, buff=0.15)
        s_lab = label(r"degree $\le 2$", SUB_COLOR).next_to(sub.get_top(), DOWN, buff=0.12)
        self.add(funcs, polys, sub, f_lab, p_lab, s_lab)
        self.wait(1.5)

        # Partial sums of e^x as dots on one row, closing in on the wall of polys.
        wall = polys.get_right()[0]
        y = sub.get_center()[1] - 0.35
        # Degrees 0, 1, 2 sit inside the inner box; from degree 3 on they leave it.
        left = sub.get_left()[0]
        far = sub.get_right()[0] + 0.55
        xs = [left + 0.4, left + 1.25, left + 2.1] + [wall - (wall - far) * 0.6**k for k in range(12)]
        dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=RESULT_COLOR) for x in xs])
        names = [mt(r"1", RESULT_COLOR), mt(r"1+x", RESULT_COLOR)]
        names[0].next_to(dots[0], DOWN, buff=0.15)
        names[1].next_to(dots[1], UP, buff=0.15)

        self.play(FadeIn(dots[0], scale=2), FadeIn(names[0]))
        self.play(FadeIn(dots[1], scale=2), FadeIn(names[1]))
        self.play(FadeIn(dots[2], scale=2))
        self.wait(0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots[3:]], lag_ratio=0.5), run_time=3)
        self.wait(0.5)

        e_dot = Dot([wall + 0.22, y, 0], radius=0.09, color=W_COLOR)
        e_lab = mt(r"e^x", W_COLOR).next_to(e_dot, RIGHT, buff=0.18)
        sin_dot = Dot(funcs.get_right() + LEFT * 1.1 + UP * 1.2, radius=0.09, color=W_COLOR)
        sin_lab = mt(r"\sin x", W_COLOR).next_to(sin_dot, DOWN, buff=0.15)
        self.play(FadeIn(e_dot, scale=2), Write(e_lab))
        self.play(Flash(e_dot, color=HIGHLIGHT))
        self.play(FadeIn(sin_dot, scale=2), Write(sin_lab))
        self.wait(3)
