"""Block 2.2: the determinant as an area factor, its sign, zero, and ad - bc.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.6 (the determinant).
"""

from shared.anim.house import *
from shared.anim.linmap import *


def corner_matrix(rows, prefix=None):
    mat = matrix_tex(rows)
    if prefix is not None:
        mat = VGroup(MathTex(prefix, font_size=MIN_FONT, color=INK), mat).arrange(RIGHT, buff=0.15)
    mat.to_corner(UL, buff=0.25)
    return label_box(mat)


def tag(tex, color=INK):
    return MathTex(tex, font_size=MIN_FONT, color=color)


class DetArea(Scene):
    """A = [[3,1],[0,2]] multiplies every area by 3*2 - 1*0 = 6."""

    def construct(self):
        U = 0.5
        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        plane = lin_plane(U)
        mat = corner_matrix([[3, 1], [0, 2]])

        square = Polygon([0, 0, 0], [U, 0, 0], [U, U, 0], [0, U, 0], color=RESULT_COLOR,
                         stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.3)
        i_hat, j_hat = basis_arrows(np.eye(2) * U)
        circle = Circle(radius=U, color=V_COLOR, stroke_width=4, fill_color=V_COLOR,
                        fill_opacity=0.25).move_to([-1.6 * U, -0.8 * U, 0])
        pi_lbl = tag(r"\pi").move_to(circle.get_center())
        area1 = label_box(tag(r"\text{area}=1", RESULT_COLOR).to_corner(UR, buff=0.25))

        self.add(plane, square, circle, i_hat, j_hat, pi_lbl, mat, area1)
        self.wait(1.5)

        i2, j2 = basis_arrows(A * U)
        area6 = label_box(tag(r"\text{area}=6", RESULT_COLOR).to_corner(UR, buff=0.25))
        c_after = A @ circle.get_center()[:2]
        six_pi = tag(r"6\pi").move_to([c_after[0], c_after[1], 0])
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, square), ApplyMatrix(A, circle),
                  Transform(i_hat, i2), Transform(j_hat, j2),
                  ReplacementTransform(pi_lbl, six_pi), run_time=3)
        self.play(ReplacementTransform(area1, area6), run_time=0.6)
        every = label_box(tag(r"\text{every area}\times6").to_corner(DL, buff=0.25))
        self.play(FadeIn(every), run_time=0.6)
        det = label_box(tag(r"\det A=3\cdot2-1\cdot0=6").to_corner(DR, buff=0.25))
        self.play(Write(det), run_time=1.2)
        self.wait(2.0)


class DetNegative(Scene):
    """A = [[3,0],[0,-1]]: det = -3. Area x3, and the F is mirrored."""

    def construct(self):
        U = 0.5
        A = np.array([[3.0, 0.0], [0.0, -1.0]])
        plane = lin_plane(U)
        mat = corner_matrix([[3, 0], [0, -1]])
        t = np.array([-1.2, 0.5, 0])
        F = f_marker(scale=1.0).shift(t)
        ghost = f_marker(scale=1.0).shift(t)
        ghost.set_fill(opacity=0).set_stroke(INK_FAINT, width=2)
        i_hat, j_hat = basis_arrows(np.eye(2) * U)

        def turn():
            a = i_hat.get_vector()
            b = j_hat.get_vector()
            ai, aj = np.arctan2(a[1], a[0]), np.arctan2(b[1], b[0])
            delta = (aj - ai + PI) % TAU - PI
            if abs(delta) < 0.05 or np.linalg.norm(a) < 0.1 or np.linalg.norm(b) < 0.1:
                return VMobject()
            arc = Arc(radius=0.4, start_angle=ai, angle=delta, color=INK, stroke_width=4)
            arc.add_tip(tip_length=0.14, tip_width=0.14)
            return arc

        arc = always_redraw(turn)
        self.add(plane, ghost, F, i_hat, j_hat, arc, mat)
        self.wait(1.2)

        i2, j2 = basis_arrows(A * U)
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, F), Transform(i_hat, i2),
                  Transform(j_hat, j2), run_time=3.5)
        self.wait(0.4)
        flip = label_box(tag(r"\text{orientation flipped}").to_corner(UR, buff=0.25))
        area = label_box(tag(r"\text{area}\times3", RESULT_COLOR).next_to(flip, DOWN, buff=0.15, aligned_edge=RIGHT))
        det = label_box(tag(r"\det A=3\cdot(-1)-0\cdot0=-3").to_corner(DR, buff=0.25))
        self.play(FadeIn(area), FadeIn(flip), run_time=0.8)
        self.play(Write(det), run_time=1.2)
        self.wait(1.2)


class DetZero(Scene):
    """A = [[2,1],[4,2]]: det = 0. Everything lands on the line y = 2x."""

    def construct(self):
        U = 0.4
        A = np.array([[2.0, 1.0], [4.0, 2.0]])
        plane = lin_plane(U)
        mat = corner_matrix([[2, 1], [4, 2]])
        square = Polygon([0, 0, 0], [U, 0, 0], [U, U, 0], [0, U, 0], color=RESULT_COLOR,
                         stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.3)
        i_hat, j_hat = basis_arrows(np.eye(2) * U)
        # centred on the kernel direction (1, -2) so the image sits on the line through 0
        cloud = disc_cloud(radius=0.42, step=0.09, dot_radius=0.03).shift([0.45, -0.9, 0])
        area1 = label_box(tag(r"\text{area}=1", RESULT_COLOR).to_corner(UR, buff=0.25))

        self.add(plane, cloud, square, i_hat, j_hat, mat, area1)
        self.wait(1)

        i2, j2 = basis_arrows(A * U)
        area0 = label_box(tag(r"\text{area}=0", RESULT_COLOR).to_corner(UR, buff=0.25))
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, square), move_dots(cloud, A),
                  Transform(i_hat, i2), Transform(j_hat, j2), run_time=3.5)
        self.play(ReplacementTransform(area1, area0), run_time=0.6)
        line = label_box(tag(r"\text{all on the line }y=2x").to_corner(DL, buff=0.25))
        det = label_box(tag(r"\det A=2\cdot2-1\cdot4=0").to_corner(DR, buff=0.25))
        self.play(FadeIn(line), run_time=0.6)
        self.play(Write(det), run_time=1.2)
        self.wait(1.5)


class DetFormula(Scene):
    """Why ad - bc: the (a+b)x(c+d) box minus the pieces around the parallelogram."""

    def construct(self):
        u = 0.65
        o = np.array([-3.9, -1.9, 0])

        def P(x, y):
            return o + u * np.array([x, y, 0])

        plane = house_plane(x_range=[-20, 20, 1], y_range=[-12, 12, 1],
                            x_length=40 * u, y_length=24 * u).shift(o)
        mat = corner_matrix([[3, 1], [1, 2]])
        para = Polygon(P(0, 0), P(3, 1), P(4, 3), P(1, 2), color=RESULT_COLOR,
                       stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.3)
        i_hat = Arrow(P(0, 0), P(3, 1), buff=0, color=X_COLOR, stroke_width=6, tip_length=0.18)
        j_hat = Arrow(P(0, 0), P(1, 2), buff=0, color=Y_COLOR, stroke_width=6, tip_length=0.18)
        vals = tag(r"a=3,\ b=1,\ c=1,\ d=2").to_corner(UR, buff=0.25)


        box = Polygon(P(0, 0), P(4, 0), P(4, 3), P(0, 3), color=INK_DIM, stroke_width=4)
        la = tag("a", X_COLOR).next_to(P(1.5, 0), DOWN, buff=0.12)
        lb = tag("b", Y_COLOR).next_to(P(3.5, 0), DOWN, buff=0.12)
        lc = tag("c", X_COLOR).next_to(P(4, 0.5), RIGHT, buff=0.15)
        ld = tag("d", Y_COLOR).next_to(P(4, 2), RIGHT, buff=0.15)
        e1 = tag(r"(a+b)(c+d)=4\cdot3=12")
        e2 = MathTex(r"-ac", r"\;-bd", r"\;-2bc", font_size=MIN_FONT, color=INK)
        e3 = tag(r"=\,12-3-2-2")
        e4 = tag(r"\det=ad-bc=6-1=5", RESULT_COLOR)
        eqs = VGroup(e1, e2, e3, e4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        eqs.next_to(vals, DOWN, buff=0.35).align_to(vals, RIGHT)
        e4.shift(DOWN * 0.1)
        back = BackgroundRectangle(VGroup(vals, eqs), color=BG, fill_opacity=0.88, buff=0.15)
        self.add(plane, back, para, i_hat, j_hat, mat, vals)
        self.wait(1)

        piece_style = dict(stroke_width=2, stroke_color=INK_DIM, fill_color=INK_FAINT, fill_opacity=0.45)
        tris_ac = VGroup(Polygon(P(0, 0), P(3, 0), P(3, 1), **piece_style),
                         Polygon(P(4, 3), P(1, 3), P(1, 2), **piece_style))
        tris_bd = VGroup(Polygon(P(0, 0), P(1, 2), P(0, 2), **piece_style),
                         Polygon(P(4, 3), P(3, 1), P(4, 1), **piece_style))
        rects = VGroup(Polygon(P(3, 0), P(4, 0), P(4, 1), P(3, 1), **piece_style),
                       Polygon(P(0, 2), P(1, 2), P(1, 3), P(0, 3), **piece_style))

        self.play(Create(box), FadeIn(VGroup(la, lb, lc, ld)), run_time=1.2)
        self.play(Write(e1), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(tris_ac), run_time=0.8)
        self.play(Write(e2[0]), run_time=0.6)
        self.play(FadeIn(tris_bd), Write(e2[1]), run_time=0.8)
        self.play(FadeIn(rects), Write(e2[2]), run_time=0.8)
        self.play(Write(e3), run_time=1)
        self.play(Write(e4), run_time=1.2)
        self.wait(1.5)
