# Original work for Mathematics for AI, CC BY-NC-SA 4.0
# (after Trefor Bazett, "Lagrange Multipliers | Geometric Meaning & Full
# Example")

from shared.anim.house import *
import numpy as np

# =============================================================================
# The running example for Acts 1 and 2
#
#     maximise / minimise   f(x, y) = xy + 1        a saddle
#     subject to            g(x, y) = x^2 + y^2 - 1 = 0   the unit circle
#
# On the circle, x = cos t and y = sin t, so f = 1 + sin(2t)/2: highs of 1.5
# at t = 45 and 225 degrees, lows of 0.5 at t = 135 and 315 degrees.
# =============================================================================
R2 = 1.0 / np.sqrt(2.0)
MAXES = [np.array([R2, R2]), np.array([-R2, -R2])]
MINS = [np.array([R2, -R2]), np.array([-R2, R2])]


def f(x, y):
    return x * y + 1.0


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


# =============================================================================
# SCENE 1: SaddleOnCircle
# The problem: the saddle has no highest point, but above the circle it does.
# =============================================================================
R_DISC = 1.6      # the saddle is drawn on a round patch, so it has a clean rim
Z_FLOOR = -0.6    # the domain plane sits under the lowest point of the patch


class SaddleOnCircle(ThreeDScene):
    def construct(self):
        # The four marked points sit on the two diagonals. At 22.5 degrees off
        # both diagonals no two of them share a line of sight, so none hides
        # another (at -45 or -90 degrees two of them would coincide on screen).
        self.set_camera_orientation(phi=62 * DEGREES, theta=-67.5 * DEGREES)
        self.camera.rotation_matrix = self.camera.generate_rotation_matrix()
        scr = lambda p: self.camera.project_point(np.array(p, dtype=float))

        ax = ThreeDAxes(
            x_range=[-1.9, 1.9, 1.0], y_range=[-1.9, 1.9, 1.0], z_range=[Z_FLOOR, 2.6, 1.0],
            x_length=5.0, y_length=5.0, z_length=2.7,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                         "include_ticks": False, "include_tip": False},
        )
        ax.shift(LEFT * 1.4 + DOWN * 0.55)
        # The x and y axes are drawn in the floor plane, under the surface.
        # (Shifting ax.x_axis itself would move what ax.c2p maps to.)
        floor_x = Line(ax.c2p(-1.9, 0, Z_FLOOR), ax.c2p(1.9, 0, Z_FLOOR), color=X_COLOR, stroke_width=2)
        floor_y = Line(ax.c2p(0, -1.9, Z_FLOOR), ax.c2p(0, 1.9, Z_FLOOR), color=Y_COLOR, stroke_width=2)

        def pt(s, ang):
            x, y = R_DISC * s * np.cos(ang), R_DISC * s * np.sin(ang)
            return ax.c2p(x, y, f(x, y))

        surf = Surface(pt, u_range=[0.001, 1.0], v_range=[0, TAU], resolution=(10, 32),
                       stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.35)
        for face in surf.submobjects:
            face.set_fill(color=V_COLOR, opacity=0.30 if (face.u_index + face.v_index) % 2 == 0 else 0.48)

        lbl_x = tex("x", X_COLOR).move_to(scr(ax.c2p(1.9, 0, Z_FLOOR)) + RIGHT * 0.25)
        # The far end of the y axis is hidden under the surface (which draws over
        # fixed labels), so y is labelled on the open near end of its axis.
        lbl_y = tex("y", Y_COLOR).move_to(scr(ax.c2p(0, -1.6, Z_FLOOR)) + LEFT * 0.3)
        title_f = tex(r"f(x, y) = xy + 1", V_COLOR).to_corner(UR, buff=0.3)
        self.add(floor_x, floor_y, ax.z_axis, surf)
        self.add_fixed_in_frame_mobjects(lbl_x, lbl_y, title_f)
        self.wait(1.0)

        # ---- the constraint, drawn in the floor
        floor_circle = ParametricFunction(lambda t: ax.c2p(np.cos(t), np.sin(t), Z_FLOOR),
                                          t_range=[0, TAU], color=W_COLOR, stroke_width=5)
        title_g = tex(r"x^2 + y^2 = 1", W_COLOR).next_to(title_f, DOWN, buff=0.2, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(title_g)
        self.play(Create(floor_circle), FadeIn(title_g), run_time=1.5)
        self.wait(0.5)

        # ---- lift the circle onto the surface
        ts = np.linspace(0, TAU, 13)[:-1]
        risers = VGroup(*[DashedLine(ax.c2p(np.cos(t), np.sin(t), Z_FLOOR),
                                     ax.c2p(np.cos(t), np.sin(t), f(np.cos(t), np.sin(t))),
                                     color=W_COLOR, stroke_width=2, stroke_opacity=0.6, dash_length=0.08)
                          for t in ts])
        lifted = ParametricFunction(lambda t: ax.c2p(np.cos(t), np.sin(t), f(np.cos(t), np.sin(t)) + 0.03),
                                    t_range=[0, TAU], color=W_COLOR, stroke_width=6)
        self.play(LaggedStart(*[Create(r) for r in risers], lag_ratio=0.08), run_time=1.5)
        self.play(Create(lifted), run_time=2.0)
        self.play(FadeOut(risers), run_time=0.6)

        # ---- walk the lifted curve with a live value of f
        tr = ValueTracker(0.0)
        walker = Dot3D(radius=0.08, color=HIGHLIGHT)
        walker.add_updater(lambda d: d.move_to(ax.c2p(np.cos(tr.get_value()), np.sin(tr.get_value()),
                                                      f(np.cos(tr.get_value()), np.sin(tr.get_value())) + 0.03)))
        read_lbl = tex(r"f =", INK)
        read_val = DecimalNumber(1.0, num_decimal_places=2, font_size=MIN_FONT, color=HIGHLIGHT)
        VGroup(read_lbl, read_val).arrange(RIGHT, buff=0.15).next_to(title_g, DOWN, buff=0.45, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(read_lbl, read_val)

        def refresh(m):
            t = tr.get_value()
            m.set_value(f(np.cos(t), np.sin(t)))
            m.next_to(read_lbl, RIGHT, buff=0.15)
            # set_value rebuilds the digits, which drops them out of the
            # fixed-in-frame set, so pin them again
            self.add_fixed_in_frame_mobjects(m)
        read_val.add_updater(refresh)
        self.add(walker)
        self.play(tr.animate.set_value(TAU), run_time=6.0, rate_func=linear)
        read_val.clear_updaters()
        self.play(FadeOut(walker), FadeOut(read_lbl), FadeOut(read_val), run_time=0.5)

        # ---- mark the two highs and the two lows, on the curve and in the floor
        def mark(w, color):
            top = ax.c2p(w[0], w[1], f(*w) + 0.03)
            bot = ax.c2p(w[0], w[1], Z_FLOOR)
            return VGroup(Dot3D(top, radius=0.09, color=color), Dot3D(bot, radius=0.07, color=color),
                          DashedLine(bot, top, color=color, stroke_width=3, dash_length=0.08))

        highs = VGroup(*[mark(w, RESULT_COLOR) for w in MAXES])
        lows = VGroup(*[mark(w, Y_COLOR) for w in MINS])
        hi_txt = tex(r"\text{highest: } f = 1.5", RESULT_COLOR)
        lo_txt = tex(r"\text{lowest: } f = 0.5", Y_COLOR)
        VGroup(hi_txt, lo_txt).arrange(DOWN, aligned_edge=RIGHT, buff=0.2).next_to(title_g, DOWN, buff=0.45, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(hi_txt)
        self.play(FadeIn(highs), FadeIn(hi_txt), run_time=1.0)
        self.wait(0.8)
        self.add_fixed_in_frame_mobjects(lo_txt)
        self.play(FadeIn(lows), FadeIn(lo_txt), run_time=1.0)
        self.wait(3.0)


# =============================================================================
# SCENE 2: LevelCurvesTouch
# Why the gradients line up: raise the level of f until its level curve only
# just touches the circle. There the two curves share a tangent line, so their
# normals, grad f and grad g, lie along one line.
# =============================================================================
U = 1.12          # screen units per unit of x and y
BOX = 1.95        # half-width of the plotted domain
GS = 0.55         # screen arrow length per unit of gradient, in plot units


class LevelCurvesTouch(Scene):
    def construct(self):
        ax = Axes(x_range=[-BOX, BOX, 1.0], y_range=[-BOX, BOX, 1.0],
                  x_length=2 * BOX * U, y_length=2 * BOX * U,
                  axis_config={"stroke_color": INK_DIM, "stroke_width": 2, "include_ticks": False},
                  tips=False).move_to(LEFT * 2.65)
        ax.x_axis.set_color(X_COLOR)
        ax.y_axis.set_color(Y_COLOR)
        lbl_x = tex("x", X_COLOR).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        lbl_y = tex("y", Y_COLOR).next_to(ax.y_axis.get_end(), RIGHT, buff=0.1)
        circle = ParametricFunction(lambda t: ax.c2p(np.cos(t), np.sin(t)), t_range=[0, TAU],
                                    color=W_COLOR, stroke_width=5)

        col_x = -0.05  # left edge of the text column

        def place(m, y):
            m.move_to(np.array([col_x + m.width / 2, y, 0]))
            return m

        def level_curve(c, color=V_COLOR, width=4, opacity=1.0):
            """The level curve xy + 1 = c, i.e. y = k / x with k = c - 1."""
            k = c - 1.0
            g = VGroup()
            if abs(k) < 1e-3:
                return g
            x0 = abs(k) / BOX
            for sx in (1, -1):
                sy = sx if k > 0 else -sx
                g.add(ParametricFunction(lambda x, sx=sx, sy=sy: ax.c2p(sx * x, sy * abs(k) / x),
                                         t_range=[x0, BOX], color=color, stroke_width=width,
                                         stroke_opacity=opacity))
            return g

        def crossings(c):
            """Where xy + 1 = c meets the circle: (x + y)^2 = 1 + 2k, (x - y)^2 = 1 - 2k."""
            k = c - 1.0
            if abs(k) > 0.5 + 1e-9:
                return []
            s, d = np.sqrt(max(1 + 2 * k, 0)), np.sqrt(max(1 - 2 * k, 0))
            pts = {(round((a + b) / 2, 6), round((a - b) / 2, 6)) for a in (s, -s) for b in (d, -d)}
            return [np.array(p) for p in pts]

        # faint family of level curves for context, labelled by their value
        family = VGroup(*[level_curve(c, opacity=0.28, width=2.5) for c in (0.0, 0.5, 1.5, 2.0, 2.5)])
        given_f = place(tex(r"f(x, y) = xy + 1", V_COLOR), 2.35)
        given_g = place(tex(r"x^2 + y^2 = 1", W_COLOR), 1.75)
        self.add(ax, lbl_x, lbl_y, family, circle, given_f, given_g)
        self.wait(1.0)

        # ---- one live level curve, and where it meets the circle
        c_tr = ValueTracker(1.25)
        live = always_redraw(lambda: level_curve(c_tr.get_value(), color=HIGHLIGHT, width=5))
        dots = always_redraw(lambda: VGroup(*[Dot(ax.c2p(*p), radius=0.08, color=HIGHLIGHT)
                                              for p in crossings(c_tr.get_value())]))
        c_lbl = tex(r"c =", INK)
        c_val = DecimalNumber(1.25, num_decimal_places=2, font_size=MIN_FONT, color=HIGHLIGHT)
        lvl_row = place(tex(r"\text{level curve } xy + 1 = c", INK), 1.0)
        c_row = place(VGroup(c_lbl, c_val).arrange(RIGHT, buff=0.15), 0.4)
        c_val.add_updater(lambda m: m.set_value(c_tr.get_value()).next_to(c_lbl, RIGHT, buff=0.15))

        say = place(tex(r"\text{crosses: } f \text{ still changes}", INK_DIM), -0.25)
        self.play(FadeIn(lvl_row), FadeIn(c_row), Create(live), FadeIn(dots), FadeIn(say), run_time=1.2)
        self.add(live, dots, c_val)
        self.wait(1.2)

        # raise the level: the four crossings slide together in pairs
        self.play(c_tr.animate.set_value(1.5), run_time=3.0, rate_func=smooth)
        say_touch = place(tex(r"\text{only touches: } f = 1.5", RESULT_COLOR), -0.25)
        self.play(ReplacementTransform(say, say_touch), run_time=0.6)
        self.wait(0.6)
        # one step higher and the level never meets the circle
        say_miss = place(tex(r"\text{misses: no allowed point}", INK_DIM), -0.25)
        self.play(c_tr.animate.set_value(1.75), ReplacementTransform(say_touch, say_miss), run_time=1.4)
        self.wait(0.6)
        say_touch = place(tex(r"\text{only touches: } f = 1.5", RESULT_COLOR), -0.25)
        self.play(c_tr.animate.set_value(1.5), ReplacementTransform(say_miss, say_touch), run_time=1.2)
        c_val.clear_updaters()
        self.remove(live, dots)
        live = level_curve(1.5, color=HIGHLIGHT, width=5)
        self.add(live)

        # ---- shared tangent line at both touching points
        def tangent(w):
            d = np.array([-w[1], w[0]])
            return Line(ax.c2p(*(w - 0.85 * d)), ax.c2p(*(w + 0.85 * d)), color=INK, stroke_width=4)

        tangents = VGroup(*[tangent(w) for w in MAXES])
        touch = VGroup(*[Dot(ax.c2p(*w), radius=0.09, color=RESULT_COLOR) for w in MAXES])
        say_tan = place(tex(r"\text{one shared tangent line}", INK), -0.85)
        self.play(Create(tangents), FadeIn(touch), FadeIn(say_tan), run_time=1.2)
        self.wait(1.0)

        # ---- the two gradients, both perpendicular to that line
        def arrows(w, lam_sign):
            gf = np.array([w[1], w[0]])            # grad f = (y, x)
            gg = 2.0 * w                            # grad g = (2x, 2y)
            a_g = Arrow(ax.c2p(*w), ax.c2p(*(w + GS * gg)), buff=0, color=W_COLOR,
                        stroke_width=6, max_tip_length_to_length_ratio=0.25)
            a_f = Arrow(ax.c2p(*w), ax.c2p(*(w + GS * gf)), buff=0, color=RESULT_COLOR,
                        stroke_width=7, max_tip_length_to_length_ratio=0.35)
            return a_g, a_f

        grads = [arrows(w, 1) for w in MAXES]
        lbl_gg = tex(r"\nabla g", W_COLOR).next_to(grads[0][0].get_end(), UR, buff=0.05)
        # grad f is short and sits inside the level curve near the top point,
        # so it is labelled at the lower-left touching point, below its tip
        lbl_gf = tex(r"\nabla f", RESULT_COLOR).next_to(grads[1][1].get_end(), RIGHT, buff=0.3).shift(DOWN * 0.3)
        self.play(*[GrowArrow(a) for a, _ in grads], FadeIn(lbl_gg), run_time=1.0)
        self.play(*[GrowArrow(b) for _, b in grads], FadeIn(lbl_gf), run_time=1.0)
        rule = place(MathTex(r"\nabla f", r"= \lambda\,", r"\nabla g", r", \quad \lambda = \tfrac12", font_size=MIN_FONT, color=INK), -1.5)
        rule[0].set_color(RESULT_COLOR)
        rule[2].set_color(W_COLOR)
        self.play(FadeIn(rule), run_time=0.8)
        self.wait(2.0)

        # ---- the lows: lower the level until it touches on the other diagonal
        # dim the max case: stroke only on the open curves, or they fill in
        hi_lines = VGroup(live, tangents)
        hi_marks = VGroup(touch, *[m for pair in grads for m in pair], lbl_gg, lbl_gf)
        self.play(hi_lines.animate.set_stroke(opacity=0.25), hi_marks.animate.set_opacity(0.25),
                  FadeOut(say_touch), FadeOut(say_tan), FadeOut(rule), run_time=0.8)
        c_tr.set_value(1.5)
        live_lo = always_redraw(lambda: level_curve(c_tr.get_value(), color=HIGHLIGHT, width=5))
        c_val.add_updater(lambda m: m.set_value(c_tr.get_value()).next_to(c_lbl, RIGHT, buff=0.15))
        self.add(live_lo)
        self.play(c_tr.animate.set_value(0.5), run_time=3.0, rate_func=smooth)
        c_val.clear_updaters()
        self.remove(live_lo)
        self.add(level_curve(0.5, color=HIGHLIGHT, width=5))

        lo_touch = VGroup(*[Dot(ax.c2p(*w), radius=0.09, color=Y_COLOR) for w in MINS])
        lo_tan = VGroup(*[tangent(w) for w in MINS])
        lo_grads = [arrows(w, -1) for w in MINS]
        say_lo = place(tex(r"\text{only touches: } f = 0.5", Y_COLOR), -0.25)
        self.play(FadeIn(lo_touch), Create(lo_tan), FadeIn(say_lo), run_time=1.0)
        self.play(*[GrowArrow(a) for pair in lo_grads for a in pair], run_time=1.2)
        say_opp = place(tex(r"\text{same line, opposite way}", INK), -0.85)
        rule_lo = place(MathTex(r"\nabla f", r"= \lambda\,", r"\nabla g", r", \quad \lambda = -\tfrac12", font_size=MIN_FONT, color=INK), -1.5)
        rule_lo[0].set_color(RESULT_COLOR)
        rule_lo[2].set_color(W_COLOR)
        self.play(FadeIn(say_opp), FadeIn(rule_lo), run_time=0.8)
        self.wait(3.0)
