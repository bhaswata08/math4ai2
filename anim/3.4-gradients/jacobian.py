# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (after 3Blue1Brown's Khan Academy Jacobian videos)

import numpy as np
from shared.anim.house import *

# Ensure xcolor is available for column-coloured matrices
tex_tmpl = TexTemplate()
tex_tmpl.add_to_preamble(r"\usepackage{xcolor}")


def F_map(p):
    """The 2D map F(x, y) = (x + sin(y)/2, y + sin(x)/2)."""
    x, y = p[0], p[1]
    return np.array([x + 0.5 * np.sin(y), y + 0.5 * np.sin(x), 0.0])


def J_map(x, y):
    """Jacobian of F_map at (x, y)."""
    return np.array([[1.0, 0.5 * np.cos(y)], [0.5 * np.cos(x), 1.0]])


def bg(m, op=0.9, buff=0.06):
    m.add_background_rectangle(color=BG, opacity=op, buff=buff)
    return m


def faint_and_warp_planes():
    faint = house_plane(
        x_range=[-6, 6, 1], y_range=[-4, 4, 1],
        background_line_style={"stroke_color": INK_FAINT, "stroke_width": 1.5, "stroke_opacity": 0.35},
        axis_config={"stroke_color": INK_FAINT, "stroke_width": 2, "stroke_opacity": 0.45},
    )
    warp = house_plane(x_range=[-6, 6, 1], y_range=[-4, 4, 1])
    warp.prepare_for_nonlinear_transform(num_inserted_curves=60)
    return faint, warp


class NonlinearWarp(Scene):
    def construct(self):
        faint, warp = faint_and_warp_planes()

        # A straight reference line: it must come out bent.
        a, b = np.array([-3.5, -1.8, 0.0]), np.array([3.5, 1.8, 0.0])
        line = Line(a, b, color=V_COLOR, stroke_width=7)
        line.insert_n_curves(60)
        line.set_z_index(5)
        straight = bg(MathTex(r"\text{a straight line}", font_size=MIN_FONT, color=V_COLOR))
        straight.move_to(np.array([-2.3, 2.1, 0.0])).set_z_index(10)
        bent = bg(MathTex(r"\text{comes out bent}", font_size=MIN_FONT, color=V_COLOR))
        bent.move_to(np.array([-2.0, 2.3, 0.0])).set_z_index(10)

        self.add(faint, warp, line, straight)
        self.wait(1.8)
        self.play(
            ApplyPointwiseFunction(F_map, warp),
            ApplyPointwiseFunction(F_map, line),
            run_time=4.5,
        )
        self.wait(0.8)
        self.play(FadeOut(straight), run_time=0.4)
        self.play(FadeIn(bent), run_time=0.6)
        self.wait(3.0)


class ZoomLocallyLinear(MovingCameraScene):
    def construct(self):
        p = np.array([1.0, 0.5, 0.0])
        F_p = F_map(p)
        delta = 0.20
        zoom_width = 2.0
        scale_fac = zoom_width / 10.0
        zoom_x = 10.0 / zoom_width

        faint, warp = faint_and_warp_planes()

        p_dot = Dot(p, radius=0.015, color=HIGHLIGHT).set_z_index(15)
        p_lbl = bg(MathTex(r"p", font_size=MIN_FONT, color=INK))
        p_lbl.next_to(p, UL, buff=0.12).set_z_index(15)

        xs = np.linspace(p[0] - 2 * delta, p[0] + 2 * delta, 5)
        ys = np.linspace(p[1] - 2 * delta, p[1] + 2 * delta, 5)
        lines = VGroup()
        for x in xs:
            l = Line(np.array([x, ys[0], 0]), np.array([x, ys[-1], 0]), stroke_color=GRID, stroke_width=2.5)
            l.insert_n_curves(25)
            lines.add(l)
        for y in ys:
            l = Line(np.array([xs[0], y, 0]), np.array([xs[-1], y, 0]), stroke_color=GRID, stroke_width=2.5)
            l.insert_n_curves(25)
            lines.add(l)
        box = Square(side_length=4 * delta, stroke_color=INK_DIM, stroke_width=2, fill_color=BG,
                     fill_opacity=0.25).move_to(p)
        box.insert_n_curves(40)
        patch = VGroup(box, lines).set_z_index(10)

        def arr(a, b, col):
            return Arrow(a, b, buff=0, color=col, stroke_width=5,
                         max_tip_length_to_length_ratio=0.3).set_z_index(12)

        e1, e2 = np.array([delta, 0, 0]), np.array([0, delta, 0])
        x_arrow = arr(p, p + e1, X_COLOR)
        y_arrow = arr(p, p + e2, Y_COLOR)
        F_p_dot = Dot(F_p, radius=0.015, color=HIGHLIGHT).set_z_index(15)
        t_x = arr(F_p, F_map(p + e1), X_COLOR)
        t_y = arr(F_p, F_map(p + e2), Y_COLOR)

        # Labels that live in the zoomed view (drawn small so they read at x5).
        def zlabel(tex, col, pos):
            m = MathTex(tex, font_size=MIN_FONT, color=col, tex_template=tex_tmpl)
            m.scale(scale_fac)
            m.add_background_rectangle(color=BG, opacity=0.9, buff=0.06 * scale_fac)
            m.move_to(pos).set_z_index(30)
            return m

        J = J_map(p[0], p[1])
        col1 = F_p + 0.5 * np.append(J[:, 0], 0) * delta * 2
        col2 = F_p + 0.5 * np.append(J[:, 1], 0) * delta * 2
        lbl1 = zlabel(r"\text{col } 1", X_COLOR, F_p + np.append(J[:, 0], 0) * delta + np.array([0.0, -0.17, 0.0]))
        lbl2 = zlabel(r"\text{col } 2", Y_COLOR, F_p + np.append(J[:, 1], 0) * delta + np.array([-0.12, 0.17, 0.0]))
        zoom_lbl = zlabel(rf"\text{{zoom }} \times {zoom_x:g}", INK, F_p + np.array([-0.62, 0.45, 0.0]))

        self.add(faint, warp, patch, p_dot, p_lbl, x_arrow, y_arrow)
        self.wait(1.5)
        self.play(FadeOut(p_lbl), run_time=0.3)
        self.play(
            ApplyPointwiseFunction(F_map, warp),
            ApplyPointwiseFunction(F_map, patch),
            Transform(p_dot, F_p_dot),
            Transform(x_arrow, t_x),
            Transform(y_arrow, t_y),
            run_time=3.5,
        )
        self.wait(1.0)
        self.play(self.camera.frame.animate.set(width=zoom_width).move_to(F_p), run_time=3.0)
        self.play(FadeIn(zoom_lbl), run_time=0.6)
        self.wait(1.2)
        self.play(FadeIn(lbl1), FadeIn(lbl2), run_time=1.0)
        self.wait(4.0)


class JacobianColumns(Scene):
    def construct(self):
        S = 2.3
        o = np.array([-3.6, -1.5, 0.0])
        p = (1.0, 0.5)
        J = J_map(*p)

        x_axis = Line(o + np.array([-0.2, 0, 0]), o + np.array([1.55 * S, 0, 0]), stroke_color=INK_DIM, stroke_width=2.5)
        y_axis = Line(o + np.array([0, -0.2, 0]), o + np.array([0, 1.4 * S, 0]), stroke_color=INK_DIM, stroke_width=2.5)
        tick_x = bg(MathTex(r"\Delta x", font_size=MIN_FONT, color=X_COLOR, tex_template=tex_tmpl))
        tick_x.next_to(o + np.array([S, 0, 0]), DOWN, buff=0.15)
        tick_y = bg(MathTex(r"\Delta y", font_size=MIN_FONT, color=Y_COLOR, tex_template=tex_tmpl))
        tick_y.next_to(o + np.array([0, S, 0]), LEFT, buff=0.15)
        square = Polygon(o, o + [S, 0, 0], o + [S, S, 0], o + [0, S, 0],
                         stroke_color=INK_FAINT, stroke_width=2, fill_opacity=0)
        ghost = VGroup(
            DashedLine(o, o + [S, 0, 0], color=INK_FAINT, stroke_width=2.5, dash_length=0.12),
            DashedLine(o, o + [0, S, 0], color=INK_FAINT, stroke_width=2.5, dash_length=0.12))

        def arr(v, col):
            return Arrow(o, o + v, buff=0, color=col, stroke_width=7,
                         max_tip_length_to_length_ratio=0.18).set_z_index(10)

        ax, ay = arr(np.array([S, 0, 0]), X_COLOR), arr(np.array([0, S, 0]), Y_COLOR)
        v1 = np.array([J[0, 0], J[1, 0], 0]) * S
        v2 = np.array([J[0, 1], J[1, 1], 0]) * S
        lx, ly = arr(v1, X_COLOR), arr(v2, Y_COLOR)
        para = Polygon(o, o + v1, o + v1 + v2, o + v2, stroke_color=RESULT_COLOR, stroke_width=3,
                       fill_color=RESULT_COLOR, fill_opacity=0.28).set_z_index(5)
        c1_lbl = bg(MathTex(r"\text{col } 1", font_size=MIN_FONT, color=X_COLOR, tex_template=tex_tmpl))
        c1_lbl.next_to(o + v1, RIGHT, buff=0.15)
        c2_lbl = bg(MathTex(r"\text{col } 2", font_size=MIN_FONT, color=Y_COLOR, tex_template=tex_tmpl))
        c2_lbl.next_to(o + v2, UP, buff=0.12)

        # J(p) written as two columns, numbers computed from J_map.
        def col_tex(c0, c1, colour):
            return MathTex(rf"\begin{{bmatrix}} {c0:.2f} \\[4pt] {c1:.2f} \end{{bmatrix}}".replace(".00", ""),
                           font_size=MIN_FONT, color=colour)

        jp = MathTex(r"J(p) =", font_size=MIN_FONT, color=INK)
        col1 = col_tex(J[0, 0], J[1, 0], X_COLOR)
        col2 = col_tex(J[0, 1], J[1, 1], Y_COLOR)
        row = VGroup(jp, col1, col2).arrange(RIGHT, buff=0.35).move_to(np.array([2.1, 0.7, 0.0]))
        note1 = bg(MathTex(r"\text{where } \Delta x \text{ lands}", font_size=MIN_FONT, color=X_COLOR))
        note1.next_to(row, DOWN, buff=0.6).align_to(row, LEFT)
        note2 = bg(MathTex(r"\text{where } \Delta y \text{ lands}", font_size=MIN_FONT, color=Y_COLOR))
        note2.next_to(note1, DOWN, buff=0.35).align_to(note1, LEFT)
        col1_lbl = MathTex(r"\text{col }1", font_size=MIN_FONT, color=X_COLOR)  # unused header kept off screen

        self.add(x_axis, y_axis, square, tick_x, tick_y, ax, ay, jp)
        self.wait(1.5)

        self.add(ghost)
        self.play(Transform(ax, lx), FadeOut(tick_x), run_time=1.5)
        self.play(FadeIn(c1_lbl), FadeIn(col1), run_time=0.8)
        self.play(FadeIn(note1), run_time=0.6)
        self.wait(2.0)
        self.play(Transform(ay, ly), FadeOut(tick_y), run_time=1.5)
        self.play(FadeIn(c2_lbl), FadeIn(col2), run_time=0.8)
        self.play(FadeIn(note2), run_time=0.6)
        self.wait(1.5)
        self.play(Transform(square, para), run_time=1.5)
        self.wait(3.5)


class JacobianRowsCols(Scene):
    def construct(self):
        # F(x, y, z) = (xy, yz) at (1, 2, 3)
        x0, y0, z0 = 1.0, 2.0, 3.0
        J = np.array([[y0, x0, 0.0], [0.0, z0, y0]])

        def num(v):
            return f"{v:g}"

        head = MathTex(r"F(x,y,z) = (xy,\ yz), \quad p = (1,2,3)", font_size=MIN_FONT, color=INK)
        head.move_to(np.array([0.0, 2.3, 0.0]))
        bg(head)

        sym = MathTex(r"J = \begin{bmatrix} y & x & 0 \\ 0 & z & y \end{bmatrix}", font_size=MIN_FONT + 4, color=INK)
        sym.move_to(np.array([-2.7, 0.1, 0.0]))
        ent = [[num(v) for v in r] for r in J]
        numm = MathTex(
            r"J(p) = \begin{bmatrix} " + " & ".join(ent[0]) + r" \\ " + " & ".join(ent[1]) + r" \end{bmatrix}",
            font_size=MIN_FONT + 4, color=INK)
        numm.move_to(sym.get_center())
        # find entry positions in the numeric matrix: last 6 glyph groups
        # (use bmatrix element boxes via a separate Matrix for exact rectangles)
        M = IntegerMatrix([[int(v) for v in r] for r in J], h_buff=1.1, v_buff=0.8,
                          element_to_mobject_config={"font_size": MIN_FONT + 4}).move_to(np.array([-1.7, 0.1, 0.0]))
        M.get_brackets().set_color(INK)
        jlab = MathTex(r"J =", font_size=MIN_FONT + 4, color=INK).next_to(M, LEFT, buff=0.25)
        entries = M.get_entries()

        row1 = SurroundingRectangle(VGroup(*entries[0:3]), color=RESULT_COLOR, buff=0.14, stroke_width=4)
        col2 = SurroundingRectangle(VGroup(entries[1], entries[4]), color=V_COLOR, buff=0.14, stroke_width=4)

        # mini plane for grad F1 = (y, x, 0) = (2, 1, 0); the z part is 0
        po = np.array([1.9, -0.6, 0.0])
        ax_x = Arrow(po + [-0.2, 0, 0], po + [2.4, 0, 0], buff=0, color=X_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        ax_y = Arrow(po + [0, -0.2, 0], po + [0, 1.9, 0], buff=0, color=Y_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        gx, gy = J[0, 0], J[0, 1]
        g_arrow = Arrow(po, po + np.array([gx, gy, 0]) * 0.9, buff=0, color=RESULT_COLOR, stroke_width=7,
                        max_tip_length_to_length_ratio=0.2)
        g_lbl = bg(MathTex(rf"\nabla F_1 = ({num(J[0,0])},\,{num(J[0,1])},\,{num(J[0,2])})", font_size=MIN_FONT, color=RESULT_COLOR))
        g_lbl.next_to(po + np.array([0.0, 2.1, 0.0]), RIGHT, buff=0.0).shift(LEFT * 0.4)
        plane = VGroup(ax_x, ax_y)

        row_lbl = bg(MathTex(r"\leftarrow \text{gradient of } F_i", font_size=MIN_FONT, color=RESULT_COLOR))
        row_lbl.next_to(row1, RIGHT, buff=0.3)

        brace = Brace(VGroup(entries[1], entries[4]), DOWN, color=V_COLOR, buff=0.2)
        col_lbl = bg(MathTex(r"\text{response to } x_j", font_size=MIN_FONT, color=V_COLOR))
        col_lbl.next_to(brace, DOWN, buff=0.12)

        d = 0.1
        resp = J[:, 1] * d
        n1 = MathTex(rf"\text{{nudge }} y \text{{ by }} {d:g}", font_size=MIN_FONT, color=Y_COLOR)
        n2 = MathTex(rf"F_1 \text{{ moves }} {resp[0]:g}", font_size=MIN_FONT, color=RESULT_COLOR)
        n3 = MathTex(rf"F_2 \text{{ moves }} {resp[1]:g}", font_size=MIN_FONT, color=RESULT_COLOR)
        nudge = VGroup(n1, n2, n3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(np.array([2.9, -0.75, 0.0]))
        bg(nudge)

        self.add(head, sym)
        self.wait(2.0)
        self.play(FadeOut(sym), run_time=0.4)
        self.play(FadeIn(jlab), FadeIn(M), run_time=0.8)
        self.wait(1.2)
        # row 1
        self.play(Create(row1), run_time=0.8)
        self.play(FadeIn(plane), run_time=0.6)
        self.play(GrowArrow(g_arrow), FadeIn(g_lbl), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(plane), FadeOut(g_arrow), FadeOut(g_lbl), run_time=0.6)
        self.play(FadeIn(row_lbl), run_time=0.8)
        self.wait(2.0)
        # column 2
        self.play(Create(col2), run_time=0.8)
        self.play(FadeIn(nudge), run_time=1.2)
        self.wait(2.5)
        self.play(GrowFromCenter(brace), FadeIn(col_lbl), run_time=1.0)
        self.wait(3.0)


class DetLocalArea(Scene):
    def construct(self):
        S = 1.6
        pts = [(1.0, 0.5, "1,\\,0.5"), (np.pi, 0.0, r"\pi,\,0")]
        centres = [-2.5, 2.5]

        def panel(cx, x, y, tag):
            J = J_map(x, y)
            o = np.array([cx - 0.9, -0.85, 0.0])
            sq = Polygon(o, o + [S, 0, 0], o + [S, S, 0], o + [0, S, 0], stroke_color=V_COLOR,
                         stroke_width=4, fill_color=V_COLOR, fill_opacity=0.25)
            v1 = np.array([J[0, 0], J[1, 0], 0]) * S
            v2 = np.array([J[0, 1], J[1, 1], 0]) * S
            para = Polygon(o, o + v1, o + v1 + v2, o + v2, stroke_color=RESULT_COLOR, stroke_width=4,
                           fill_color=RESULT_COLOR, fill_opacity=0.3)
            det = float(np.linalg.det(J))
            one = bg(MathTex("1", font_size=MIN_FONT, color=V_COLOR)).move_to(o + np.array([S / 2, S / 2, 0]))
            area = bg(MathTex(f"{det:.2f}", font_size=MIN_FONT, color=RESULT_COLOR)).move_to(
                o + (v1 + v2) / 2)
            head = MathTex(rf"p = ({tag})", font_size=MIN_FONT, color=INK).move_to(np.array([cx, 2.15, 0.0]))
            a, b, c, dd = J[0, 0], J[0, 1], J[1, 0], J[1, 1]
            def g(v):
                t = f"{round(v, 2):g}"
                return f"({t})" if v < 0 else t
            l1 = MathTex(rf"\det J = {g(a * dd)} - {g(b)}\cdot{g(c)}", font_size=MIN_FONT, color=INK).move_to(np.array([cx, -1.9, 0.0]))
            l2 = MathTex(rf"= {det:.2f}", font_size=MIN_FONT, color=RESULT_COLOR).move_to(np.array([cx, -2.45, 0.0]))
            ghost = sq.copy().set_fill(opacity=0).set_stroke(color=INK_FAINT, width=2.5)
            return dict(sq=sq, para=para, one=one, area=area, head=head, l1=l1, l2=l2, ghost=ghost, det=det)

        A = panel(centres[0], *pts[0])
        B = panel(centres[1], *pts[1])
        print(f"[DET] {A['det']:.4f} {B['det']:.4f}")

        self.add(A["head"], A["sq"], A["one"])
        self.wait(2.0)
        self.add(A["ghost"])
        self.play(Transform(A["sq"], A["para"]), FadeOut(A["one"]), run_time=2.0)
        self.play(FadeIn(A["area"]), run_time=0.6)
        self.play(FadeIn(A["l1"]), run_time=0.8)
        self.play(FadeIn(A["l2"]), run_time=0.6)
        self.wait(2.5)
        self.play(FadeIn(B["head"]), FadeIn(B["sq"]), FadeIn(B["one"]), run_time=1.0)
        self.wait(1.0)
        self.add(B["ghost"])
        self.play(Transform(B["sq"], B["para"]), FadeOut(B["one"]), run_time=2.0)
        self.play(FadeIn(B["area"]), run_time=0.6)
        self.play(FadeIn(B["l1"]), run_time=0.8)
        self.play(FadeIn(B["l2"]), run_time=0.6)
        self.wait(4.0)
