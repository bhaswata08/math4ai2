# Original work for Mathematics for AI, CC BY-NC-SA 4.0
# (after Brian Douglas, MATLAB Tech Talk "Constrained Optimization: Intuition
# behind the Lagrangian")

from shared.anim.house import *
import numpy as np

LABEL_BG = dict(color=BG, opacity=0.85, buff=0.08)


def bg(m):
    m.add_background_rectangle(**LABEL_BG)
    return m


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


# =============================================================================
# The running example, shared by all four scenes
#
#     minimise   J(x1, x2) = x1^2 + x2^2        a bowl
#     subject to c(x1, x2) = x1 + x2 + 3 = 0    a line in the x1-x2 plane
#
# The bowl is drawn on a round patch of radius R, so it ends on a clean rim and
# has no corner spikes. On the constraint line, writing s for signed distance
# from the line's closest point to the origin, J = |foot|^2 + s^2: a parabola
# whose minimum is exactly the answer. The chord ends on the rim, by choice of
# the s range.
# =============================================================================
R = 3.3                                    # radius of the plotted patch
ZMAX = R * R                               # the bowl is drawn up to its rim
# Azimuth is a compromise. Looking straight down the constraint normal (1,1)
# lays the chord flat across the picture but squashes grad c to a stub, which
# is the one arrow scene 2 needs to be readable. At -100 degrees the chord
# still keeps 82% of its length across the screen and the normal keeps 57%.
PHI, THETA = 64 * DEGREES, -100 * DEGREES
D = np.array([1.0, -1.0]) / np.sqrt(2.0)   # unit vector along the constraint
GSCALE = 0.75                              # plot units drawn per unit gradient


def J(x, y):
    return x * x + y * y


def foot(t=0.0):
    """Point of the line x1 + x2 + 3 = t closest to the origin."""
    return np.array([-(3.0 - t) / 2, -(3.0 - t) / 2])


def jstar(t=0.0):
    """Best value of J on that line: the height of the parabola's vertex."""
    f = foot(t)
    return float(J(f[0], f[1]))


def half_chord(t=0.0):
    """How far along the line we can go before leaving the drawn patch."""
    return float(np.sqrt(R * R - jstar(t)))


def on_line(s, t=0.0):
    """The point s along the constraint line, in x1-x2 coordinates."""
    return foot(t) + D * s


def make_axes(shift=LEFT * 2.0 + UP * 0.35):
    """A frame for c2p only. The axes stay hidden: drawn, they run straight
    through the bowl and through the constraint line, and green and rose are
    already spoken for here."""
    axes = ThreeDAxes(
        x_range=[-R, R, 1.5], y_range=[-R, R, 1.5], z_range=[0, ZMAX, 5],
        x_length=4.3, y_length=4.3, z_length=2.5,
        axis_config={"stroke_color": INK_DIM, "stroke_width": 1.5,
                     "include_ticks": False, "include_tip": False},
    )
    axes.set_opacity(0)
    axes.shift(shift)
    return axes


def bowl(axes):
    """The checkered teal surface, built in polar coordinates for a round rim."""
    surf = Surface(
        lambda u, v: axes.c2p(u * np.cos(v), u * np.sin(v), u * u),
        u_range=[1e-3, R], v_range=[0, TAU], resolution=(10, 32),
        stroke_color=V_COLOR, stroke_width=0.4, stroke_opacity=0.3,
    )
    for face in surf.submobjects:
        face.set_fill(color=V_COLOR,
                      opacity=0.40 if (face.u_index + face.v_index) % 2 == 0 else 0.60)
    return surf


def floor_line(axes, t=0.0, **kw):
    h = half_chord(t)
    a, b = on_line(-h, t), on_line(h, t)
    style = dict(color=W_COLOR, stroke_width=5)
    style.update(kw)
    return Line(axes.c2p(a[0], a[1], 0), axes.c2p(b[0], b[1], 0), **style)


def slice_curve(axes, t=0.0, **kw):
    """Where the constraint sheet meets the bowl: a parabola lying on the surface."""
    h = half_chord(t)
    style = dict(color=RESULT_COLOR, stroke_width=6)
    style.update(kw)
    return ParametricFunction(
        lambda s: axes.c2p(*on_line(s, t), jstar(t) + s * s),
        t_range=[-h, h, 0.05], **style,
    )


def sheet(axes, t=0.0):
    """A translucent vertical wall standing on the constraint line."""
    h = half_chord(t)
    return Surface(
        lambda u, v: axes.c2p(*on_line(u, t), v),
        u_range=[-h, h], v_range=[0, ZMAX], resolution=(1, 1),
        fill_color=W_COLOR, fill_opacity=0.22,
        stroke_color=W_COLOR, stroke_width=2.5, stroke_opacity=0.8,
    )


def ring(axes, rho, **kw):
    """A level curve of J, drawn on the surface rather than flattened into a map."""
    style = dict(color=INK_DIM, stroke_width=4)
    style.update(kw)
    return ParametricFunction(
        lambda a: axes.c2p(rho * np.cos(a), rho * np.sin(a), rho * rho),
        t_range=[0, TAU, 0.05], **style,
    )


def hud(scene, *mobs):
    """Pin a label to the frame, and refuse to render one that leaves it. The
    column beside the bowl is narrow, and a line that grew by a word used to
    run off the slide unnoticed."""
    for m in mobs:
        assert m.get_right()[0] <= 4.85, f"HUD line runs off the right: {m}"
        assert m.get_left()[0] >= -5.0, f"HUD line runs off the left: {m}"
        assert m.get_top()[1] <= 2.78, f"HUD line runs off the top: {m}"
        assert m.get_bottom()[1] >= -2.78, f"HUD line runs off the bottom: {m}"
    scene.camera.add_fixed_in_frame_mobjects(*mobs)
    return mobs


def column(m, y, x0=-0.45):
    """Left-align a HUD line in the column to the right of the bowl."""
    m.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
    return m


def live_number(scene, label, value_fn, color=RESULT_COLOR, size=48):
    """A readout that tracks a tracker and stays pinned to the frame.

    set_value rebuilds a DecimalNumber's digits, and the new digits are not
    on the camera's fixed-in-frame list, so in a ThreeDScene a plain updater
    leaves the number smeared across the floor. Re-pin and re-place it on
    every frame instead.
    """
    num = DecimalNumber(value_fn(), num_decimal_places=2, font_size=size, color=color)
    num.next_to(label, RIGHT, buff=0.22)

    def tick(m):
        m.set_value(value_fn())
        m.next_to(label, RIGHT, buff=0.22)
        scene.add_fixed_in_frame_mobjects(m)

    num.add_updater(tick)
    return num


def clamp_to_frame(m, pad=0.12):
    """Nudge a label that was placed from a projected 3D point back inside the
    frame. The arrow tips sit near the bottom-left corner, so their labels land
    just off screen if they are placed by offset alone."""
    dx = min(0.0, 4.85 - pad - m.get_right()[0]) - min(0.0, m.get_left()[0] + 5.0 - pad)
    dy = min(0.0, 2.75 - pad - m.get_top()[1]) - min(0.0, m.get_bottom()[1] + 2.81 - pad)
    return m.shift(np.array([dx, dy, 0.0]))


def stack(y, *lines, size=42, color=INK, gap=0.12):
    """Two or three short HUD lines, left-aligned under each other. The column
    is 5.3 units wide, so a sentence is split rather than shrunk below the
    font floor."""
    g = VGroup(*[MathTex(s, font_size=size, color=color) for s in lines])
    g.arrange(DOWN, buff=gap, aligned_edge=LEFT)
    return column(g, y)


# =============================================================================
# SCENE 1: ConstrainedSlice
# What the constrained problem is: the bowl, the wall, and the curve they share.
# =============================================================================
class ConstrainedSlice(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=PHI, theta=THETA)
        axes = make_axes()
        surf = bowl(axes)
        free_dot = Dot3D(axes.c2p(0, 0, 0), radius=0.08, color=RESULT_COLOR)

        title = column(tex(r"J = x_1^2 + x_2^2", V_COLOR, 46), 2.3)
        free = column(tex(r"\text{free minimum: }(0,0)", INK_DIM, 40), 1.6)
        hud(self, title, free)
        self.add(axes, surf, free_dot, title, free)
        self.wait(2.5)

        # The constraint arrives: first the line of allowed points, then the
        # wall. The free minimum goes grey: it is still there, just not allowed.
        line = floor_line(axes)
        c_lab = column(tex(r"x_1 + x_2 + 3 = 0", W_COLOR, 46), 0.7)
        hud(self, c_lab)
        self.play(FadeOut(free), free_dot.animate.set_color(INK_FAINT),
                  Create(line), FadeIn(c_lab), run_time=1.6)
        self.wait(1.2)

        wall = sheet(axes)
        self.play(FadeIn(wall), run_time=1.4)
        self.wait(0.8)

        # The problem is the curve where the wall meets the bowl.
        curve = slice_curve(axes)
        cut = column(tex(r"\text{the allowed curve}", RESULT_COLOR, 42), -0.1)
        hud(self, cut)
        self.play(Create(curve), FadeIn(cut), run_time=2.2)
        self.wait(1.2)

        # Walk it, and watch the height.
        h = half_chord()
        s = ValueTracker(-h)

        def pos():
            return axes.c2p(*on_line(s.get_value()), jstar() + s.get_value() ** 2)

        walker = Dot3D(pos(), radius=0.1, color=HIGHLIGHT)
        walker.add_updater(lambda m: m.move_to(pos()))
        read_lab = column(tex(r"J =", INK, 48), -1.1)
        read_num = live_number(self, read_lab,
                               lambda: jstar() + s.get_value() ** 2)
        hud(self, read_lab, read_num)
        self.add(walker, read_lab, read_num)
        self.wait(1.0)
        self.play(s.animate.set_value(h), run_time=4.5, rate_func=linear)
        self.wait(0.6)
        self.play(s.animate.set_value(0.0), run_time=2.6, rate_func=smooth)
        read_num.clear_updaters()
        self.wait(0.8)

        # The answer, checked against the algebra.
        x1, x2 = foot()
        assert np.allclose([x1, x2], [-1.5, -1.5])
        assert abs(jstar() - 4.5) < 1e-12
        ans = stack(-2.0, rf"x_1 = x_2 = {x1:.1f}", rf"J = {jstar():.1f}",
                    size=46, color=RESULT_COLOR)
        hud(self, ans)
        self.play(Flash(pos(), color=HIGHLIGHT, flash_radius=0.4, line_length=0.18),
                  FadeIn(ans), run_time=1.0)
        self.wait(3.0)


# =============================================================================
# SCENE 2: LevelOnTheCurve
# Why the gradients line up: at the lowest allowed point the constraint curve
# stops crossing level curves and merely touches one.
# =============================================================================
class LevelOnTheCurve(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=PHI, theta=THETA)
        axes = make_axes()
        surf = bowl(axes)
        wall = sheet(axes)
        line = floor_line(axes)
        curve = slice_curve(axes)
        rho = ValueTracker(3.0)

        def level():
            return ring(axes, rho.get_value())

        lv = always_redraw(level)

        def mark(sign):
            def make():
                r = rho.get_value()
                s = sign * np.sqrt(max(r * r - jstar(), 0.0))
                return Dot3D(axes.c2p(*on_line(s), jstar() + s * s),
                             radius=0.09, color=HIGHLIGHT)
            return always_redraw(make)

        m1, m2 = mark(+1), mark(-1)

        title = column(tex(r"\text{a level curve of } J", INK_DIM, 42), 2.3)
        note = stack(1.4, r"\text{it crosses:}", r"J \text{ is still changing}",
                     size=42, color=HIGHLIGHT)
        hud(self, title, note)
        self.add(axes, surf, wall, line, curve, lv, m1, m2, title, note)
        self.wait(3.0)

        # Shrink the level curve: the two crossings slide together and merge.
        touch = np.sqrt(jstar())
        assert abs(touch**2 - 4.5) < 1e-12
        self.play(rho.animate.set_value(touch), run_time=4.0, rate_func=smooth)
        note2 = stack(1.4, r"\text{it touches:}", r"J \text{ has stopped changing}",
                      size=42, color=RESULT_COLOR)
        hud(self, note2)
        self.play(FadeOut(note), FadeIn(note2), run_time=0.8)
        self.wait(2.5)

        # Drop to the floor and compare the two gradients at that point.
        x1, x2 = foot()
        gJ = np.array([2 * x1, 2 * x2])
        gc = np.array([1.0, 1.0])
        assert np.allclose(gJ, [-3.0, -3.0])
        assert np.allclose(gJ, -3.0 * gc)

        top = axes.c2p(x1, x2, jstar())
        base = axes.c2p(x1, x2, 0)
        drop = DashedLine(top, base, color=INK_FAINT, stroke_width=2.5, dash_length=0.08)
        foot_dot = Dot3D(base, radius=0.09, color=RESULT_COLOR)

        def arrow(vec, color):
            tip = axes.c2p(x1 + GSCALE * vec[0], x2 + GSCALE * vec[1], 0)
            return Arrow3D(base, tip, color=color, thickness=0.012,
                           height=0.22, base_radius=0.07)

        a_J = arrow(gJ, RESULT_COLOR)
        a_c = arrow(gc, W_COLOR)

        self.camera.rotation_matrix = self.camera.generate_rotation_matrix()
        scr = lambda p: self.camera.project_point(np.array(p, dtype=float))
        lab_J = clamp_to_frame(bg(tex(r"\nabla J", RESULT_COLOR, 44)).move_to(
            scr(axes.c2p(x1 + GSCALE * gJ[0], x2 + GSCALE * gJ[1], 0)) + LEFT * 0.55))
        lab_c = clamp_to_frame(bg(tex(r"\nabla c", W_COLOR, 44)).move_to(
            scr(axes.c2p(x1 + GSCALE * gc[0], x2 + GSCALE * gc[1], 0))
            + RIGHT * 0.55 + UP * 0.3))
        hud(self, lab_J, lab_c)

        self.play(FadeOut(title), Create(drop), FadeIn(foot_dot), run_time=1.2)
        self.play(FadeIn(a_c), FadeIn(lab_c), run_time=1.0)
        self.wait(1.0)
        self.play(FadeIn(a_J), FadeIn(lab_J), run_time=1.0)
        self.wait(2.0)

        same = stack(-0.4, r"\text{same line,}", r"\text{different length}",
                     size=40, color=INK_DIM)
        eq = column(tex(r"\nabla J = -3\,\nabla c", RESULT_COLOR, 50), -1.8)
        hud(self, same, eq)
        self.play(FadeIn(same), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(eq), run_time=0.9)
        self.wait(3.0)


# =============================================================================
# SCENE 3: LagrangeSystem
# The algebra, on its own. No function plot here, so the frame stays flat.
# =============================================================================
def colour_parts(m, spec):
    for i, col in spec.items():
        m[i].set_color(col)
    return m


class LagrangeSystem(Scene):
    def construct(self):
        FS = 48

        def row(m, y, x0=-4.4):
            m.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
            return m

        lag = row(MathTex(r"\mathcal{L}(x_1, x_2, \lambda)", r"=",
                          r"x_1^2 + x_2^2", r"+", r"\lambda", r"\,(x_1 + x_2 + 3)",
                          font_size=FS), 2.2)
        colour_parts(lag, {2: V_COLOR, 4: RESULT_COLOR, 5: W_COLOR})
        obj_tag = MathTex(r"\text{objective}", font_size=38, color=V_COLOR)
        con_tag = MathTex(r"\text{constraint}", font_size=38, color=W_COLOR)
        obj_tag.next_to(lag[2], UP, buff=0.22)
        con_tag.next_to(lag[5], UP, buff=0.22)

        self.add(lag)
        self.wait(1.5)
        self.play(FadeIn(obj_tag), FadeIn(con_tag), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(obj_tag), FadeOut(con_tag), run_time=0.5)

        # Set every partial derivative to zero. The partials are written with a
        # slash, not a built-up fraction: three stacked fractions do not fit the
        # frame height once the solve is added underneath.
        e1 = row(MathTex(r"\partial\mathcal{L}/\partial x_1", r"=",
                         r"2x_1 + \lambda = 0", font_size=FS, color=X_COLOR), 1.1)
        e2 = row(MathTex(r"\partial\mathcal{L}/\partial x_2", r"=",
                         r"2x_2 + \lambda = 0", font_size=FS, color=Y_COLOR), 0.25)
        e3 = row(MathTex(r"\partial\mathcal{L}/\partial \lambda", r"=",
                         r"x_1 + x_2 + 3 = 0", font_size=FS, color=W_COLOR), -0.6)
        brace = Brace(VGroup(e1, e2, e3), RIGHT, color=INK_DIM)
        count = MathTex(r"\text{3 equations,}\\ \text{3 unknowns}", font_size=40,
                        color=INK_DIM)
        count.next_to(brace, RIGHT, buff=0.3)
        back = MathTex(r"\text{the }\lambda\text{ row hands}\\ \text{the constraint back}",
                       font_size=38, color=W_COLOR)
        back.next_to(count, DOWN, buff=0.7).align_to(count, LEFT)

        self.play(FadeIn(e1), run_time=0.8)
        self.wait(0.9)
        self.play(FadeIn(e2), run_time=0.8)
        self.wait(0.9)
        self.play(FadeIn(e3), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(brace), FadeIn(count), run_time=0.9)
        self.wait(1.4)
        self.play(FadeIn(back), run_time=0.8)
        self.wait(2.2)

        # Solve it, and check the solve against numpy.
        A = np.array([[2.0, 0.0, 1.0], [0.0, 2.0, 1.0], [1.0, 1.0, 0.0]])
        b = np.array([0.0, 0.0, -3.0])
        x1, x2, lam = np.linalg.solve(A, b)
        assert np.allclose([x1, x2, lam], [-1.5, -1.5, 3.0])
        assert abs(J(x1, x2) - 4.5) < 1e-12

        self.play(FadeOut(brace, count, back, lag), run_time=0.6)
        self.play(VGroup(e1, e2, e3).animate.shift(UP * 1.0), run_time=0.8)

        s1 = row(MathTex(r"\text{first two rows: } x_1 = x_2 = -\lambda/2",
                         font_size=FS), -0.5)
        s2 = row(MathTex(r"\text{put that in the third: } -\lambda + 3 = 0",
                         font_size=FS), -1.4)
        s3 = row(MathTex(rf"\lambda = {lam:.0f}, \quad x_1 = x_2 = {x1:.1f},"
                         rf" \quad J = {J(x1, x2):.1f}",
                         font_size=FS + 4, color=RESULT_COLOR), -2.4)
        self.play(FadeIn(s1), run_time=0.9)
        self.wait(1.6)
        self.play(FadeIn(s2), run_time=0.9)
        self.wait(1.6)
        self.play(FadeIn(s3), run_time=1.0)
        self.wait(3.0)


# =============================================================================
# SCENE 4: ShadowPrice
# What lambda is worth: slide the constraint and watch the best value move.
# =============================================================================
class ShadowPrice(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=PHI, theta=THETA)
        axes = make_axes()
        surf = bowl(axes)
        t = ValueTracker(0.0)

        wall = always_redraw(lambda: sheet(axes, t.get_value()))
        line = always_redraw(lambda: floor_line(axes, t.get_value()))
        curve = always_redraw(lambda: slice_curve(axes, t.get_value()))
        best = always_redraw(lambda: Dot3D(
            axes.c2p(*foot(t.get_value()), jstar(t.get_value())),
            radius=0.1, color=HIGHLIGHT))

        c_lab = column(tex(r"x_1 + x_2 + 3 = t", W_COLOR, 44), 2.3)
        t_lab = column(tex(r"t =", INK, 48), 1.5)
        t_num = live_number(self, t_lab, t.get_value, color=W_COLOR)
        j_lab = column(tex(r"J^* =", INK, 48), 0.7)
        j_num = live_number(self, j_lab, lambda: jstar(t.get_value()))
        hud(self, c_lab, t_lab, t_num, j_lab, j_num)

        self.add(axes, surf, wall, line, curve, best,
                 c_lab, t_lab, t_num, j_lab, j_num)
        self.wait(2.5)

        # Relax the constraint, then put it back.
        assert abs(jstar(1.0) - 2.0) < 1e-12
        self.play(t.animate.set_value(1.0), run_time=5.0, rate_func=smooth)
        self.wait(1.5)
        self.play(t.animate.set_value(0.0), run_time=3.0, rate_func=smooth)
        t_num.clear_updaters()
        j_num.clear_updaters()
        self.wait(1.0)

        # The rate, by central difference, next to the multiplier it matches.
        h = 1e-6
        rate = (jstar(h) - jstar(-h)) / (2 * h)
        assert abs(rate + 3.0) < 1e-6
        f1 = column(tex(r"J^*(t) = \tfrac{(3-t)^2}{2}", INK, 44), -0.6)
        f2 = column(tex(rf"\left.\frac{{dJ^*}}{{dt}}\right|_{{t=0}}"
                        rf" = {rate:.0f} = -\lambda", RESULT_COLOR, 46), -1.9)
        hud(self, f1, f2)
        self.play(FadeIn(f1), run_time=0.9)
        self.wait(1.8)
        self.play(FadeIn(f2), run_time=0.9)
        self.wait(3.5)
