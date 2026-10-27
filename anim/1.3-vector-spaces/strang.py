# Block 1.3, vector spaces and subspaces after Gilbert Strang, MIT 18.06
# lecture 5 "Transposes, Permutations, Spaces R^n" (second half). Strang
# draws these on the board; the scenes are authored here in house style.

import numpy as np

from shared.anim.house import *


def arrow(tip, color):
    return Arrow(ORIGIN, np.array([*tip, 0.0]), buff=0, stroke_width=5,
                 max_tip_length_to_length_ratio=0.25, color=color)


def tag(tex, color, at, direction, math=True):
    m = (MathTex if math else Tex)(tex, font_size=MIN_FONT, color=color)
    m.next_to(at, direction, buff=0.15)
    m.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
    return m


class QuadrantTest(Scene):
    """The quarter plane x >= 0, y >= 0: adding stays inside, scaling by -1 leaves."""

    def construct(self):
        plane = house_plane()
        quarter = Polygon([0, 0, 0], [5.2, 0, 0], [5.2, 3, 0], [0, 3, 0],
                          stroke_width=0, fill_color=V_COLOR, fill_opacity=0.15)
        title = Tex(r"Quarter plane: $x \ge 0,\ y \ge 0$", font_size=MIN_FONT, color=INK)
        title.to_corner(UL, buff=0.3).add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        v, w = np.array([2.0, 0.6]), np.array([0.8, 1.4])
        va, wa = arrow(v, V_COLOR), arrow(w, W_COLOR)
        vl = tag(r"\vec v", V_COLOR, va.get_end(), DR)
        wl = tag(r"\vec w", W_COLOR, wa.get_end(), LEFT)
        self.add(plane, quarter, va, wa, vl, wl, title)
        self.wait(1.5)

        # Add: tip to tail, the sum is still in the quarter.
        w_moved = wa.copy().shift([*v, 0])
        s = v + w
        sa = arrow(s, RESULT_COLOR)
        sl = tag(r"\vec v + \vec w", RESULT_COLOR, sa.get_end(), RIGHT)
        self.play(TransformFromCopy(wa, w_moved))
        self.play(GrowArrow(sa), Write(sl))
        ok = Tex(r"add: still inside", font_size=MIN_FONT, color=RESULT_COLOR)
        ok.to_corner(DR, buff=0.3).add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(FadeIn(ok))
        self.wait(1.2)
        self.play(FadeOut(VGroup(w_moved, sa, sl, ok)))

        # Scale by -1: the arrow flips into the opposite quarter.
        na = arrow(-v, RESULT_COLOR)
        nl = tag(r"-1\cdot\vec v", RESULT_COLOR, na.get_end(), DOWN)
        self.play(TransformFromCopy(va, na), run_time=1.3)
        self.play(Write(nl))
        bad = Tex(r"scale by $-1$: outside", font_size=MIN_FONT, color=Y_COLOR)
        bad.to_corner(DR, buff=0.3).add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(FadeIn(bad), quarter.animate.set_fill(Y_COLOR, opacity=0.18))
        self.wait(1)
        verdict = Tex(r"Not a vector space", font_size=MIN_FONT, color=Y_COLOR)
        verdict.next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        verdict.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(Write(verdict))
        self.wait(2.5)


class LineFromVector(Scene):
    """One vector in a subspace forces in every multiple of it: the whole line through 0."""

    def construct(self):
        plane = house_plane()
        v = np.array([2.0, 1.0, 0.0])
        va = arrow(v[:2], V_COLOR)
        vl = tag(r"\vec v", V_COLOR, va.get_end(), DR)
        self.add(plane, va, vl)
        self.wait(1.5)

        c = ValueTracker(1.0)
        cv = always_redraw(lambda: Arrow(
            ORIGIN, c.get_value() * v, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.25 / max(abs(c.get_value()), 0.3),
            color=RESULT_COLOR) if abs(c.get_value()) > 0.05 else Dot(ORIGIN, color=HIGHLIGHT, radius=0.1))
        readout = VGroup(MathTex(r"c =", font_size=MIN_FONT, color=INK),
                         DecimalNumber(1.0, num_decimal_places=1, include_sign=True,
                                       font_size=MIN_FONT, color=RESULT_COLOR))
        readout.arrange(RIGHT, buff=0.15).to_corner(UL, buff=0.3)
        readout[1].add_updater(lambda d: d.set_value(c.get_value()))
        label = MathTex(r"c\,\vec v", font_size=MIN_FONT, color=RESULT_COLOR)
        label.next_to(readout, DOWN, aligned_edge=LEFT, buff=0.2)
        bg = BackgroundRectangle(VGroup(readout, label), color=BG, fill_opacity=0.9, buff=0.12)
        trace = TracedPath(lambda: c.get_value() * v, stroke_color=RESULT_COLOR,
                           stroke_width=6, stroke_opacity=0.6)
        self.add(trace, cv, bg, readout, label)
        self.bring_to_front(va, vl)
        self.play(c.animate.set_value(2.4), run_time=1.5)
        self.play(c.animate.set_value(0.0), run_time=1.5)
        zero = tag(r"0\,\vec v = \vec 0", HIGHLIGHT, ORIGIN, DR)
        self.play(FadeIn(zero))
        self.wait(0.8)
        self.play(FadeOut(zero))
        self.play(c.animate.set_value(-2.4), run_time=2)
        self.play(c.animate.set_value(1.0), run_time=1.5)

        line = Line(-2.6 * v, 2.6 * v, color=RESULT_COLOR, stroke_width=6)
        self.play(Create(line), FadeOut(trace))
        note = Tex(r"the whole line through $\vec 0$", font_size=MIN_FONT, color=RESULT_COLOR)
        note.to_corner(DR, buff=0.3).add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.play(FadeIn(note))
        self.wait(2.5)


class SpaceAndSubspace(Scene):
    """Vector space: the plane, where sums and multiples stay in the plane.
    Subspace: a line through 0 inside it, where they stay on the line."""

    def construct(self):
        plane = house_plane()
        r2 = tag(r"\mathbb{R}^2", V_COLOR, [4.0, -2.3, 0], ORIGIN)
        self.add(plane, r2)
        self.wait(1.5)

        def header(text):
            h = Tex(text, font_size=MIN_FONT, color=INK).to_edge(UP, buff=0.15)
            return h.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # Vector space: the whole plane.
        head = header(r"\textbf{Vector space}: sums and multiples stay inside")
        v, w = np.array([1.6, -0.6]), np.array([-0.6, 1.3])
        va, wa = arrow(v, V_COLOR), arrow(w, W_COLOR)
        vl = tag(r"\vec v", V_COLOR, va.get_end(), DR)
        wl = tag(r"\vec w", W_COLOR, wa.get_end(), LEFT)
        self.play(FadeIn(head), GrowArrow(va), GrowArrow(wa), FadeIn(vl), FadeIn(wl))
        sa = arrow(v + w, RESULT_COLOR)
        sl = tag(r"\vec v + \vec w", RESULT_COLOR, sa.get_end(), RIGHT)
        self.play(GrowArrow(sa), FadeIn(sl))
        ma = arrow(-1.4 * v, RESULT_COLOR)
        ml = tag(r"-1.4\,\vec v", RESULT_COLOR, ma.get_end(), UP)
        self.play(GrowArrow(ma), FadeIn(ml))
        self.play(Indicate(r2, color=HIGHLIGHT))
        self.wait(1.5)

        # Subspace: a line through 0, inside the plane.
        d = np.array([2.0, 1.0])
        line = Line([*(-2.6 * d), 0], [*(2.6 * d), 0], color=X_COLOR, stroke_width=7)
        line_lab = tag(r"\text{line through } \vec 0", X_COLOR, [-3.4, -0.35, 0], ORIGIN)
        head2 = header(r"\textbf{Subspace}: a vector space inside a vector space")
        self.play(FadeOut(VGroup(va, wa, vl, wl, sa, sl, ma, ml)), Create(line), FadeIn(line_lab),
                  Transform(head, head2))
        a, b = 0.6 * d, 0.9 * d
        aa, ba = arrow(a, V_COLOR), arrow(b, W_COLOR)
        al = tag(r"\vec a", V_COLOR, aa.get_end(), UP)
        bl = tag(r"\vec b", W_COLOR, ba.get_end(), UP)
        self.play(GrowArrow(ba), FadeIn(bl))
        self.play(GrowArrow(aa), FadeIn(al))
        b_moved = ba.copy().shift([*a, 0])
        self.play(TransformFromCopy(ba, b_moved), FadeOut(bl))
        ca = arrow(a + b, RESULT_COLOR)
        cl = tag(r"\vec a + \vec b", RESULT_COLOR, ca.get_end(), UP)
        self.play(GrowArrow(ca), FadeIn(cl), FadeOut(b_moved))
        na = arrow(-1.5 * a, RESULT_COLOR)
        nl = tag(r"-1.5\,\vec a", RESULT_COLOR, na.get_end() + RIGHT * 0.6, DOWN)
        self.play(GrowArrow(na), FadeIn(nl))
        self.play(Indicate(line, color=HIGHLIGHT, scale_factor=1.0))
        self.wait(3)
