"""Block 2.4: A = P D P^{-1} as three moves of the plane, carrying one vector through.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.13 (change of basis) and
ch.14 (eigenvectors), and Visual Kernel, "SEE Matrix" ch.2.
Same matrix as the deck: A = [[4, 1], [2, 3]].
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class EigenbasisChange(Scene):
    """x = (3,0) goes through P^-1, D, P and lands on A x = (12,6), the same point A gives directly."""

    def construct(self):
        U = 0.35
        plane = lin_plane(U)
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        P = np.array([[1.0, 1.0], [1.0, -2.0]])
        Pi = np.linalg.inv(P)
        D = np.diag([5.0, 2.0])
        assert np.allclose(P @ D @ Pi, A)
        x0 = np.array([3.0, 0.0])
        stages = [x0, Pi @ x0, D @ Pi @ x0, P @ D @ Pi @ x0]
        assert np.allclose(stages[1], [2, 1]) and np.allclose(stages[2], [10, 2])
        assert np.allclose(stages[3], [12, 6]) and np.allclose(stages[3], A @ x0)

        def sc(v):
            return np.array([v[0] * U, v[1] * U, 0.0])

        dots = disc_cloud(2.4, 0.4, 0.05)
        for d in dots:
            d.move_to(d.get_center() * U)
        ghost_pos = [d.get_center().copy() for d in dots]

        # eigenlines through the origin, long enough to stay on screen after every move
        l1 = Line(sc(-2.4 * np.array([1, 1])), sc(2.4 * np.array([1, 1])), color=V_COLOR, stroke_width=5)
        l2 = Line(sc(-1.2 * np.array([1, -2])), sc(1.2 * np.array([1, -2])), color=W_COLOR, stroke_width=5)

        xdot = Dot(sc(x0), radius=0.09, color=HIGHLIGHT)
        xarrow = always_redraw(lambda: Arrow(ORIGIN, xdot.get_center(), buff=0, color=HIGHLIGHT,
                                             stroke_width=6, max_tip_length_to_length_ratio=0.3,
                                             tip_length=0.18))

        eq = MathTex("A", "=", "P", "D", r"P^{-1}", font_size=MIN_FONT, color=INK)
        eq.to_corner(UL, buff=0.25)
        parts = {"P^{-1}": eq[4], "D": eq[3], "P": eq[2]}
        eq_a = eq[0]
        label_box(eq)

        def coord(s, colour=HIGHLIGHT):
            t = tex(s, colour)
            t.to_corner(DL, buff=0.25)
            label_box(t, opacity=1.0)
            t.set_z_index(10)
            return t

        cur = coord(r"\mathbf{x}=(3,\,0)")
        self.add(plane, dots, l1, l2, xarrow, xdot, eq, cur)
        self.wait(2)

        def step(name, M, nxt, caption):
            nonlocal cur
            part = parts[name]
            self.play(part.animate.set_color(HIGHLIGHT), run_time=0.4)
            self.play(move_dots(dots, M),
                      *[m.animate.apply_matrix(m2(*M.flatten())) for m in (l1, l2)],
                      xdot.animate.move_to(m2(*M.flatten()) @ xdot.get_center()), run_time=3.5)
            new = coord(nxt)
            self.play(FadeOut(cur), FadeIn(new), part.animate.set_color(INK), run_time=0.6)
            cur = new
            self.wait(1.4)

        step("P^{-1}", Pi, r"(2,\,1)=2\mathbf{v}_1+1\mathbf{v}_2", "")
        step("D", D, r"(10,\,2)=10\,\mathbf{v}_1+2\,\mathbf{v}_2", "")
        step("P", P, r"(12,\,6)=A\mathbf{x}", "")

        rings = VGroup(*[Circle(radius=0.06, color=INK, stroke_width=2).move_to(p) for p in ghost_pos])
        ring_x = Circle(radius=0.14, color=INK, stroke_width=3).move_to(sc(x0))
        new = coord(r"\text{apply }A\text{ directly}", INK)
        self.play(FadeOut(cur), FadeIn(new), FadeIn(rings), FadeIn(ring_x), eq_a.animate.set_color(HIGHLIGHT),
                  run_time=0.8)
        cur = new
        self.play(move_dots(rings, A), ring_x.animate.move_to(m2(*A.flatten()) @ ring_x.get_center()), run_time=3)
        new = coord(r"\text{same point } (12,\,6)", HIGHLIGHT)
        self.play(FadeOut(cur), FadeIn(new), eq_a.animate.set_color(INK), run_time=0.6)
        self.wait(2.5)
