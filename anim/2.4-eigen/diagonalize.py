"""Block 2.4: A = P D P^{-1} as three moves of the plane.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.13 (change of basis) and
ch.14 (eigenvectors), and Visual Kernel, "SEE Matrix" ch.2.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class EigenbasisChange(Scene):
    """A = P D P^{-1}: eigenvectors onto the axes, stretch, back. Same cloud as applying A."""

    def construct(self):
        U = 0.6
        plane = lin_plane(U)
        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        P = np.array([[1.0, 1.0], [0.0, -1.0]])
        Pi = np.linalg.inv(P)
        D = np.diag([3.0, 2.0])
        assert np.allclose(P @ D @ Pi, A)

        dots = disc_cloud(1.6, 0.25, 0.05)
        for d in dots:  # plane coordinates -> scene, keeping dot size
            d.move_to(d.get_center() * U)
        ghost_pos = [d.get_center().copy() for d in dots]

        L = 2.2
        l1 = Line(np.array([-L, 0, 0]) * U, np.array([L, 0, 0]) * U, color=V_COLOR, stroke_width=5)
        l2 = Line(np.array([-1.5, 1.5, 0]) * U, np.array([1.5, -1.5, 0]) * U, color=W_COLOR, stroke_width=5)

        eq = MathTex("A", "=", "P", "D", r"P^{-1}", font_size=MIN_FONT, color=INK)
        eq.to_corner(UL, buff=0.25)
        parts = {"P^{-1}": eq[4], "D": eq[3], "P": eq[2]}
        eq_a = eq[0]
        label_box(eq)

        self.add(plane, dots, l1, l2, eq)
        self.wait(1)

        def tagm(s):
            t = tex(s)
            t.to_edge(DOWN, buff=0.25)
            label_box(t)
            return t

        def step(name, M, tag_s):
            part = parts[name]
            t = tagm(tag_s)
            self.play(part.animate.set_color(HIGHLIGHT), FadeIn(t), run_time=0.5)
            mobs = [l1, l2]
            self.play(move_dots(dots, M), *[m.animate.apply_matrix(m2(*M.flatten())) for m in mobs],
                      run_time=3)
            self.play(part.animate.set_color(INK), FadeOut(t), run_time=0.5)

        step("P^{-1}", Pi, r"\text{eigenvectors onto the axes}")
        step("D", D, r"\text{stretch by 3 and 2}")
        step("P", P, r"\text{axes back to eigenvectors}")

        rings = VGroup(*[Circle(radius=0.06, color=INK, stroke_width=2).move_to(p) for p in ghost_pos])
        t = tagm(r"\text{apply }A\text{ directly}")
        self.play(FadeIn(rings), FadeIn(t), eq_a.animate.set_color(HIGHLIGHT), run_time=0.8)
        self.play(move_dots(rings, A), run_time=3)
        self.play(eq_a.animate.set_color(INK), run_time=0.4)
        t2 = tagm(r"\text{same cloud}")
        self.play(FadeTransform(t, t2), run_time=0.6)
        self.wait(1.2)
