"""Block 2.4: repeated multiplication finds the top eigenvector.

Idea from Visual Kernel, "SEE Matrix" ch.2 and 3Blue1Brown,
Essence of Linear Algebra ch.14 (eigenvectors).
Same matrix as the deck: A = [[4, 1], [2, 3]], x0 = (3, 0) = 2 v1 + 1 v2.
"""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class PowerIteration(Scene):
    """A^k x0 = c1 5^k v1 + c2 2^k v2: the teal part grows faster, so the sum swings onto v1."""

    def construct(self):
        U = 0.4
        plane = lin_plane(U)
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        v1 = np.array([1.0, 1.0])
        v2 = np.array([1.0, -2.0])
        P = np.column_stack([v1, v2])
        x0 = np.array([3.0, 0.0])
        c = np.linalg.solve(P, x0)
        assert np.allclose(c, [2, 1])
        lam = (5.0, 2.0)

        def sc(v):
            return np.array([v[0] * U, v[1] * U, 0.0])

        def coeffs(k):
            return c[0] * lam[0] ** k, c[1] * lam[1] ** k

        for k in range(5):  # the closed form agrees with really multiplying by A
            xk = np.linalg.matrix_power(A, k) @ x0
            a, b = coeffs(k)
            assert np.allclose(xk, a * v1 + b * v2)

        def arr(v, colour, w=6):
            return Arrow(ORIGIN, sc(v), buff=0, color=colour, stroke_width=w,
                         max_tip_length_to_length_ratio=0.3, tip_length=0.18)

        # parts drawn divided by 5^k, so the teal part keeps its size
        def parts(k):
            a, b = coeffs(k)
            s = lam[0] ** k
            return a * v1 / s, b * v2 / s

        l1 = DashedLine(sc(-2.6 * v1), sc(2.6 * v1), color=V_COLOR, stroke_width=3)
        l2 = DashedLine(sc(-1.3 * v2), sc(1.3 * v2), color=W_COLOR, stroke_width=3)

        def row(k, active=True):
            a, b = coeffs(k)
            r = MathTex(rf"k={k}:", rf"{a:g}", r"\mathbf{v}_1", "+", rf"{b:g}", r"\mathbf{v}_2",
                        font_size=MIN_FONT, color=INK)
            r[1].set_color(V_COLOR)
            r[2].set_color(V_COLOR)
            r[4].set_color(W_COLOR)
            r[5].set_color(W_COLOR)
            return r

        rows = VGroup(*[row(k) for k in range(5)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.to_corner(UR, buff=0.15)
        rows.set_z_index(10)
        for r in rows:
            label_box(r)

        note = tex(r"\text{drawn at scale }5^{-k}", INK_DIM)
        note.to_corner(DL, buff=0.25)
        label_box(note)

        t1, t2 = parts(0)
        a1, a2 = arr(t1, V_COLOR), arr(t2, W_COLOR)
        a2.shift(sc(t1))
        s0 = arr(t1 + t2, RESULT_COLOR, 7)
        self.add(plane, l1, l2, a2, a1, s0, rows[0], note)
        self.wait(2.5)

        sum_arrow, ta, tb = s0, a1, a2
        for k in range(1, 5):
            t1, t2 = parts(k)
            n1, n2 = arr(t1, V_COLOR), arr(t2, W_COLOR)
            n2.shift(sc(t1))
            ns = arr(t1 + t2, RESULT_COLOR, 7)
            self.play(Transform(ta, n1), Transform(tb, n2), Transform(sum_arrow, ns),
                      FadeIn(rows[k]), *[r.animate.set_opacity(0.45) for r in rows[:k]], run_time=2.2)
            self.wait(1.8)

        # final: the closed form with the dominant term large and the other faded
        final = MathTex(r"A^{k}\mathbf{x}_0", "=", r"2\cdot5^{k}\,\mathbf{v}_1", "+",
                        r"1\cdot2^{k}\,\mathbf{v}_2", font_size=MIN_FONT, color=INK)
        final[2].set_color(V_COLOR)
        final[4].set_color(W_COLOR).set_opacity(0.5)
        final.to_edge(DOWN, buff=0.25)
        label_box(final)
        self.play(FadeOut(note), run_time=0.4)
        self.play(FadeIn(final), run_time=0.8)
        self.wait(3)
