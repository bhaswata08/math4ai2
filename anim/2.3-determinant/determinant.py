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
        ghost_grid = ghost_plane(U)
        mat = corner_matrix([[3, 1], [0, 2]])

        square = Polygon([0, 0, 0], [U, 0, 0], [U, U, 0], [0, U, 0], color=RESULT_COLOR,
                         stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.3)
        i_hat, j_hat = basis_arrows(np.eye(2) * U)
        circle = Circle(radius=U, color=V_COLOR, stroke_width=4, fill_color=V_COLOR,
                        fill_opacity=0.25).move_to([-1.6 * U, -0.8 * U, 0])
        pi_lbl = tag(r"\pi").move_to(circle.get_center())
        area1 = label_box(tag(r"\text{area}=1", RESULT_COLOR).to_corner(UR, buff=0.25))

        self.add(ghost_grid, plane, square, circle, i_hat, j_hat, pi_lbl, mat, area1)
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
        ghost_grid = ghost_plane(U)
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
            arc = Arc(radius=0.7, start_angle=ai, angle=delta, color=INK, stroke_width=6)
            arc.add_tip(tip_length=0.22, tip_width=0.22)
            return arc

        arc = always_redraw(turn)
        self.add(ghost_grid, plane, ghost, F, i_hat, j_hat, arc, mat)
        self.wait(1.2)

        i2, j2 = basis_arrows(A * U)
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, F), Transform(i_hat, i2),
                  Transform(j_hat, j2), run_time=3.5)
        self.wait(0.4)
        flip = label_box(tag(r"\text{orientation flipped}").to_corner(UR, buff=0.25))
        area = label_box(tag(r"\text{area}\times3", RESULT_COLOR).next_to(flip, DOWN, buff=0.15, aligned_edge=RIGHT))
        det = label_box(tag(r"\det A=3\cdot(-1)-0\cdot0=-3").to_corner(DR, buff=0.4))
        self.play(FadeIn(area), FadeIn(flip), run_time=0.8)
        self.play(Write(det), run_time=1.2)
        self.wait(1.2)


class DetZero(Scene):
    """A = [[2,1],[4,2]]: det = 0. Everything lands on the line y = 2x."""

    def construct(self):
        U = 0.4
        A = np.array([[2.0, 1.0], [4.0, 2.0]])
        ghost_grid = ghost_plane(U)
        plane = lin_plane(U)
        mat = corner_matrix([[2, 1], [4, 2]])
        square = Polygon([0, 0, 0], [U, 0, 0], [U, U, 0], [0, U, 0], color=RESULT_COLOR,
                         stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.3)
        i_hat, j_hat = basis_arrows(np.eye(2) * U)
        # centred on the kernel direction (1, -2) so the image sits on the line through 0
        cloud = disc_cloud(radius=0.42, step=0.09, dot_radius=0.03).shift([0.45, -0.9, 0])
        area1 = label_box(tag(r"\text{area}=1", RESULT_COLOR).to_corner(UR, buff=0.25))

        self.add(ghost_grid, plane, cloud, square, i_hat, j_hat, mat, area1)
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
    """Why ad - bc: a (a+b) x (c+d) box minus six pieces, each kind in its own colour."""

    def construct(self):
        a, b, c, d = 4, 1, 2, 3
        W, H = a + b, c + d
        u = 0.6
        o = np.array([-4.2, -2.15, 0])

        def P(x, y):
            return o + u * np.array([x, y, 0])

        plane = house_plane(x_range=[-20, 20, 1], y_range=[-12, 12, 1],
                            x_length=40 * u, y_length=24 * u).shift(o)
        mat = corner_matrix([[a, b], [c, d]])
        para = Polygon(P(0, 0), P(a, c), P(a + b, c + d), P(b, d), color=RESULT_COLOR,
                       stroke_width=4, fill_color=RESULT_COLOR, fill_opacity=0.35)
        i_hat = Arrow(P(0, 0), P(a, c), buff=0, color=X_COLOR, stroke_width=6, tip_length=0.18)
        j_hat = Arrow(P(0, 0), P(b, d), buff=0, color=Y_COLOR, stroke_width=6, tip_length=0.18)

        q = tag(r"\text{area}=\,?", RESULT_COLOR).move_to([2.9, 1.9, 0])
        self.add(plane, para, i_hat, j_hat, mat, label_box(q))
        self.wait(1.5)

        box = Polygon(P(0, 0), P(W, 0), P(W, H), P(0, H), color=INK_DIM, stroke_width=4)
        lw = tag("a+b").next_to(P(0.7 * W, H), UP, buff=0.35)
        lh = tag("c+d").next_to(P(W, 0.25 * H), RIGHT, buff=0.75)
        box_area = W * H
        e1 = tag(rf"\text{{box}}={W}\cdot{H}={box_area}")
        ya = a * c
        yb = b * d
        yc = 2 * b * c
        e2 = tag(rf"-ac=-{a}\cdot{c}=-{ya}", X_COLOR)
        e3 = tag(rf"-bd=-{b}\cdot{d}=-{yb}", Y_COLOR)
        e4 = tag(rf"-2bc=-2\cdot{b}\cdot{c}=-{yc}", W_COLOR)
        det = box_area - ya - yb - yc
        assert det == a * d - b * c == 10
        e5 = tag(rf"{box_area}-{ya}-{yb}-{yc}={det}", RESULT_COLOR)
        e6 = tag(rf"=ad-bc={a*d}-{b*c}", RESULT_COLOR)
        eqs = VGroup(e1, e2, e3, e4, e5, e6).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        eqs.move_to([2.8, 0.55, 0]).align_to([0.5, 0, 0], LEFT)

        style = dict(stroke_width=2, fill_opacity=0.5)
        tris_ac = VGroup(Polygon(P(0, 0), P(a, 0), P(a, c), **style),
                         Polygon(P(W, H), P(b, H), P(b, d), **style)).set_color(X_COLOR)
        tris_bd = VGroup(Polygon(P(0, 0), P(b, d), P(0, d), **style),
                         Polygon(P(W, H), P(a, c), P(W, c), **style)).set_color(Y_COLOR)
        rects = VGroup(Polygon(P(a, 0), P(W, 0), P(W, c), P(a, c), **style),
                       Polygon(P(0, d), P(b, d), P(b, H), P(0, H), **style)).set_color(W_COLOR)
        for g in (tris_ac, tris_bd, rects):
            g.set_fill(opacity=0.5)

        self.play(Create(box), FadeIn(lw), FadeIn(lh), FadeOut(q), run_time=1.5)
        self.play(FadeIn(label_box(e1)), run_time=1.2)
        self.wait(1.5)
        for pieces, eq, away in ((tris_ac, e2, 0.2), (tris_bd, e3, 0.2), (rects, e4, 0.2)):
            self.play(FadeIn(pieces), FadeIn(label_box(eq)), run_time=1.2)
            self.wait(1.2)
            shifts = [pc.animate.shift(away * (pc.get_center() - P(W / 2, H / 2))) for pc in pieces]
            self.play(*shifts, run_time=0.8)
            self.wait(0.8)
        self.play(FadeIn(label_box(e5)), run_time=1.4)
        self.wait(1.5)
        self.play(FadeIn(label_box(e6)), run_time=1.2)
        self.play(*[pc.animate.set_fill(opacity=0.15).set_stroke(opacity=0.3)
                    for g in (tris_ac, tris_bd, rects) for pc in g], run_time=1)
        self.wait(2.0)


class CofactorWalk(Scene):
    """Cofactor expansion along row 1 of [[2,0,1],[1,3,2],[1,1,4]]: det = 18."""

    def construct(self):
        A = np.array([[2, 0, 1], [1, 3, 2], [1, 1, 4]])
        assert round(np.linalg.det(A)) == 18

        def minor(j):
            return np.delete(np.delete(A, 0, axis=0), j, axis=1)

        def det2(m):
            return int(m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0])

        signs = [1, -1, 1]
        minors = [minor(j) for j in range(3)]
        mdets = [det2(m) for m in minors]
        terms = [s * int(A[0, j]) * md for j, (s, md) in enumerate(zip(signs, mdets))]
        assert sum(terms) == 18 and mdets == [10, 2, -2]

        mat = matrix_tex(A.tolist(), font_size=56, col_colors=(None, None, None))
        mat.get_entries()  # 9 entries, row major
        mat.move_to([-3.0, 0.0, 0])
        ents = mat.get_entries()
        sign_tex = VGroup(*[
            MathTex("+" if s > 0 else r"\boldsymbol{-}", font_size=56, color=HIGHLIGHT).next_to(ents[j], UP, buff=0.55)
            for j, s in enumerate(signs)])
        rule = tag(r"\det A=a_{11}M_{11}-a_{12}M_{12}+a_{13}M_{13}").move_to([0, 2.4, 0])

        parts = [tag(r"\det A="),
                 tag(f"{terms[0]}", RESULT_COLOR),
                 tag(rf"-\,{abs(signs[1]) * int(A[0, 1]) * mdets[1]}", RESULT_COLOR),
                 tag(rf"+\,({terms[2]})", RESULT_COLOR),
                 tag(r"=18", RESULT_COLOR)]
        bottom = VGroup(*parts).arrange(RIGHT, buff=0.18).move_to([0, -2.35, 0])
        bottom[0].set_color(INK)

        self.add(mat, sign_tex, rule, parts[0])
        self.wait(2.0)

        def cross(j):
            rl = Line(ents[0].get_left() + LEFT * 0.25, ents[2].get_right() + RIGHT * 0.25,
                      color=HIGHLIGHT, stroke_width=4)
            cl = Line(ents[j].get_top() + UP * 0.3, ents[6 + j].get_bottom() + DOWN * 0.3,
                      color=HIGHLIGHT, stroke_width=4)
            return rl, cl

        def struck(j):
            return [ents[k] for k in range(9) if k // 3 == 0 or k % 3 == j]

        def survivors(j):
            return [ents[k] for k in range(9) if k // 3 != 0 and k % 3 != j]

        panel_x = 2.2
        for j in range(3):
            rl, cl = cross(j)
            self.play(Create(rl), Create(cl), *[e.animate.set_opacity(0.25) for e in struck(j)], run_time=1.2)
            mm = matrix_tex(minors[j].tolist(), col_colors=(None, None)).move_to([panel_x, 0.85, 0])
            lead = tag(f"M_{{1{j + 1}}}=", INK).next_to(mm, LEFT, buff=0.2)
            self.play(*[Indicate(e, color=HIGHLIGHT, scale_factor=1.15) for e in survivors(j)],
                      FadeIn(mm), FadeIn(lead), run_time=1.5)
            m = minors[j]
            e1 = tag(rf"{m[0,0]}\cdot{m[1,1]}-{m[0,1]}\cdot{m[1,0]}={mdets[j]}").move_to([panel_x + 0.2, -0.2, 0])
            self.play(FadeIn(e1), run_time=1.3)
            aj = int(A[0, j])
            sgn = "-" if signs[j] < 0 else ""
            mdtxt = f"({mdets[j]})" if mdets[j] < 0 else f"{mdets[j]}"
            e2 = tag(rf"{sgn}{aj}\cdot{mdtxt}={signs[j] * aj * mdets[j]}", RESULT_COLOR)
            if j == 1:
                e2 = tag(rf"-0\cdot{mdets[j]}=0", RESULT_COLOR)
            e2.next_to(e1, DOWN, buff=0.3).align_to(e1, LEFT)
            self.play(FadeIn(e2), run_time=1.2)
            extra = []
            if j == 1:
                note = tag(r"\text{a zero kills it}", INK_DIM).next_to(e2, DOWN, buff=0.3).align_to(e2, LEFT)
                extra.append(note)
                self.play(FadeIn(note), run_time=0.8)
            self.wait(0.8)
            self.play(FadeIn(parts[1 + j]), run_time=0.8)
            self.wait(1.0)
            self.play(FadeOut(VGroup(rl, cl, mm, lead, e1, e2, *extra)),
                      *[e.animate.set_opacity(1) for e in ents], run_time=0.8)
        self.play(FadeIn(parts[4]), run_time=1.0)
        self.wait(2.5)
