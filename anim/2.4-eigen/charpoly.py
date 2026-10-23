"""Block 2.4: eigenvalues are where A - lambda I squashes space.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.14 (eigenvectors and eigenvalues).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class DetHitsZero(Scene):
    """The parallelogram of A - lambda I collapses exactly at the roots of det(A - lambda I)."""

    def construct(self):
        U = 0.45
        O = np.array([-2.6, -0.1, 0.0])
        left = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8 * U, y_length=6 * U,
            background_line_style={"stroke_color": GRID, "stroke_width": 2, "stroke_opacity": 0.8},
            axis_config={"stroke_color": INK_DIM, "stroke_width": 3}, faded_line_ratio=1)
        left.move_to(O)

        lam = ValueTracker(0.0)

        def cols():
            l = lam.get_value()
            return np.array([3 - l, 0.0]), np.array([1.0, 2 - l])

        def pt(v):
            return O + np.array([v[0] * U, v[1] * U, 0.0])

        def para():
            c1, c2 = cols()
            poly = Polygon(pt([0, 0]), pt(c1), pt(c1 + c2), pt(c2), stroke_width=2,
                           stroke_color=RESULT_COLOR, fill_color=RESULT_COLOR, fill_opacity=0.35)
            return poly

        def arrow(c, colour):
            if np.linalg.norm(c) < 0.03:
                return VGroup()
            return Arrow(pt([0, 0]), pt(c), buff=0, color=colour, stroke_width=6,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.16)

        P = always_redraw(para)
        a1 = always_redraw(lambda: arrow(cols()[0], X_COLOR))
        a2 = always_redraw(lambda: arrow(cols()[1], Y_COLOR))

        axes = Axes(x_range=[0, 4, 1], y_range=[-2, 6, 1], x_length=4.2, y_length=3.4,
                    axis_config={"stroke_color": INK_DIM, "stroke_width": 3, "include_ticks": False,
                                 "include_tip": False})
        axes.move_to([2.7, -0.4, 0])
        p = lambda l: (3 - l) * (2 - l)
        curve = axes.plot(p, x_range=[0, 4], color=INK, stroke_width=5)
        dot = always_redraw(lambda: Dot(axes.c2p(lam.get_value(), p(lam.get_value())),
                                        radius=0.1, color=RESULT_COLOR))
        r2 = tex("2", INK_DIM).move_to(axes.c2p(2, 2.2))
        r3 = tex("3", INK_DIM).move_to(axes.c2p(3, 2.2))
        ticks = VGroup(*[DashedLine(axes.c2p(r, 0), axes.c2p(r, 1.0), color=INK_FAINT, stroke_width=2)
                         for r in (2, 3)])

        formula = tex(r"p(\lambda)=(3-\lambda)(2-\lambda)")
        formula.to_corner(UR, buff=0.25)
        label_box(formula)

        def lam_ro():
            lab = tex(r"\lambda=")
            num = DecimalNumber(lam.get_value(), num_decimal_places=2, font_size=MIN_FONT, color=INK)
            g = VGroup(lab, num).arrange(RIGHT, buff=0.12)
            g.to_corner(UL, buff=0.25)
            label_box(g)
            return g

        ro = always_redraw(lam_ro)
        tag = tex(r"A-\lambda I", INK_DIM)
        tag.to_corner(DL, buff=0.25)
        label_box(tag)

        self.add(left, P, a1, a2, axes, curve, ticks, r2, r3, dot, formula, ro, tag)
        self.wait(0.8)
        self.play(lam.animate.set_value(2.0), run_time=3.5, rate_func=smooth)
        self.play(Flash(dot, color=HIGHLIGHT, flash_radius=0.35), P.animate.set_stroke(HIGHLIGHT, width=5),
                  run_time=0.8)
        self.wait(0.6)
        self.play(P.animate.set_stroke(RESULT_COLOR, width=2), lam.animate.set_value(3.0), run_time=2.5)
        self.play(Flash(dot, color=HIGHLIGHT, flash_radius=0.35), P.animate.set_stroke(HIGHLIGHT, width=5),
                  run_time=0.8)
        self.wait(0.6)
        self.play(P.animate.set_stroke(RESULT_COLOR, width=2), lam.animate.set_value(4.0), run_time=2)
        self.wait(1)
