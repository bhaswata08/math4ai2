"""Block 2.3: four shears of the same unit square. The area never changes."""

from shared.anim.house import *
from shared.anim.linmap import *


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


class ShearFour(Scene):
    def construct(self):
        U = 1.1
        CEN = np.array([1.6, -0.3, 0.0])
        plane = house_plane(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=6 * U, y_length=4 * U)
        plane.move_to(CEN)
        # keep the grid inside the frame: the plane is 7.5 x 5 units
        shears = [([[1, 1], [0, 1]], "right"), ([[1, -1], [0, 1]], "left"),
                  ([[1, 0], [1, 1]], "up"), ([[1, 0], [-1, 1]], "down")]
        t = ValueTracker(0.0)
        state = {"M": np.eye(2)}

        def Mt():
            return np.eye(2) + t.get_value() * (state["M"] - np.eye(2))

        def P(p):
            return CEN + np.array([p[0] * U, p[1] * U, 0.0])

        def square():
            M = Mt()
            pts = [P(M @ np.array(c)) for c in [(0, 0), (1, 0), (1, 1), (0, 1)]]
            return Polygon(*pts, color=RESULT_COLOR, stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.25)

        def arrows():
            M = Mt()
            return VGroup(
                Arrow(P([0, 0]), P(M[:, 0]), buff=0, color=X_COLOR, stroke_width=7,
                      max_tip_length_to_length_ratio=0.25, tip_length=0.2),
                Arrow(P([0, 0]), P(M[:, 1]), buff=0, color=Y_COLOR, stroke_width=7,
                      max_tip_length_to_length_ratio=0.25, tip_length=0.2))

        sq = always_redraw(square)
        ar = always_redraw(arrows)
        area = tex(r"\text{area}=1", RESULT_COLOR).move_to([-3.2, -1.9, 0])
        self.add(plane, sq, ar, area)

        def mat_for(M):
            m = matrix_tex(M, col_colors=(X_COLOR, Y_COLOR))
            return m.move_to([-3.2, 1.5, 0])

        cur = mat_for([[1, 0], [0, 1]])
        self.add(cur)
        self.wait(1.2)
        for M, _ in shears:
            Mn = np.array(M, dtype=float)
            assert abs(np.linalg.det(Mn) - 1) < 1e-12
            new = mat_for(M)
            self.play(FadeOut(cur), run_time=0.3)
            state["M"] = Mn
            self.play(FadeIn(new), run_time=0.3)
            cur = new
            self.play(t.animate.set_value(1.0), run_time=2.0)
            self.wait(1.4)
            self.play(FadeOut(cur), run_time=0.2)
            cur = mat_for([[1, 0], [0, 1]])
            self.play(t.animate.set_value(0.0), FadeIn(cur), run_time=1.2)
        self.wait(1.0)
