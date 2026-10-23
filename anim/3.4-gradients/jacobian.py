# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (after 3Blue1Brown's Khan Academy Jacobian videos)

import numpy as np
from shared.anim.house import *

# Ensure xcolor is available for column-colored matrices
tex_tmpl = TexTemplate()
tex_tmpl.add_to_preamble(r"\usepackage{xcolor}")


def F_map(p):
    """The 2D map F(x, y) = (x + sin(y)/2, y + sin(x)/2)."""
    x, y = p[0], p[1]
    return np.array([
        x + 0.5 * np.sin(y),
        y + 0.5 * np.sin(x),
        0.0,
    ])


class NonlinearWarp(Scene):
    def construct(self):
        # 1. Background faint reference grid (stays fixed behind)
        faint_plane = house_plane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_color": INK_FAINT, "stroke_width": 1.5, "stroke_opacity": 0.35},
            axis_config={"stroke_color": INK_FAINT, "stroke_width": 2, "stroke_opacity": 0.45},
        )

        # 2. Active warping plane
        warp_plane = house_plane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
        )
        warp_plane.prepare_for_nonlinear_transform(num_inserted_curves=60)

        # 3. Formula for the map F(x, y)
        formula = MathTex(
            r"F(x, y) = \left(x + \frac{1}{2}\sin(y),\; y + \frac{1}{2}\sin(x)\right)",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=INK,
        )
        formula.to_edge(UP, buff=0.40)
        formula.add_background_rectangle(color=BG, opacity=0.92, buff=0.12)
        formula.set_z_index(20)

        # 4. Caption describing the result
        caption = MathTex(
            r"\text{lines bend: not a linear map}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        caption.to_edge(DOWN, buff=0.40)
        caption.add_background_rectangle(color=BG, opacity=0.92, buff=0.12)
        caption.set_z_index(20)

        # First frame shows the givens
        self.add(faint_plane, warp_plane, formula)
        self.wait(1.5)

        # Apply F with apply_function
        self.play(
            ApplyPointwiseFunction(F_map, warp_plane),
            run_time=4.5,
        )
        self.wait(1.5)

        # Reveal caption
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=1.5)
        self.wait(5.0)


class ZoomLocallyLinear(MovingCameraScene):
    def construct(self):
        p = np.array([1.0, 0.5, 0.0])
        F_p = F_map(p)  # ≈ (1.2397, 0.9207, 0.0)
        delta = 0.20
        zoom_width = 2.8
        scale_fac = zoom_width / 10.0

        # Background faint grid
        faint_plane = house_plane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_color": INK_FAINT, "stroke_width": 1.5, "stroke_opacity": 0.35},
            axis_config={"stroke_color": INK_FAINT, "stroke_width": 2, "stroke_opacity": 0.45},
        )

        # Active grid
        warp_plane = house_plane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
        )
        warp_plane.prepare_for_nonlinear_transform(num_inserted_curves=60)

        # Formula at top of wide view
        formula = MathTex(
            r"F(x, y) = \left(x + \frac{1}{2}\sin(y),\; y + \frac{1}{2}\sin(x)\right)",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=INK,
        )
        formula.to_edge(UP, buff=0.35)
        formula.add_background_rectangle(color=BG, opacity=0.92, buff=0.12)
        formula.set_z_index(25)

        # Point p dot and label
        p_dot = Dot(p, radius=0.045, color=HIGHLIGHT)
        p_dot.set_z_index(15)
        p_lbl = MathTex(r"p = (1,\, 0.5)", tex_template=tex_tmpl, font_size=MIN_FONT, color=INK)
        p_lbl.next_to(p, UL, buff=0.15)
        p_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        p_lbl.set_z_index(15)

        # Construct little neighborhood grid around p (4x4 cells, 0.8 x 0.8)
        x_vals = np.linspace(p[0] - 2 * delta, p[0] + 2 * delta, 5)
        y_vals = np.linspace(p[1] - 2 * delta, p[1] + 2 * delta, 5)

        little_lines = VGroup()
        for x in x_vals:
            line = Line(
                np.array([x, y_vals[0], 0.0]),
                np.array([x, y_vals[-1], 0.0]),
                stroke_color=GRID,
                stroke_width=2.5,
            )
            line.insert_n_curves(25)
            little_lines.add(line)
        for y in y_vals:
            line = Line(
                np.array([x_vals[0], y, 0.0]),
                np.array([x_vals[-1], y, 0.0]),
                stroke_color=GRID,
                stroke_width=2.5,
            )
            line.insert_n_curves(25)
            little_lines.add(line)

        # Neighborhood bounding square
        box = Square(
            side_length=4 * delta,
            stroke_color=INK_DIM,
            stroke_width=2,
            stroke_opacity=0.8,
            fill_color=BG,
            fill_opacity=0.25,
        ).move_to(p)
        box.insert_n_curves(40)

        # Small basis arrows at p: x-step X_COLOR, y-step Y_COLOR
        x_arrow = Arrow(
            p,
            p + np.array([delta, 0.0, 0.0]),
            buff=0,
            color=X_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.30,
        )
        x_arrow.set_z_index(12)

        y_arrow = Arrow(
            p,
            p + np.array([0.0, delta, 0.0]),
            buff=0,
            color=Y_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.30,
        )
        y_arrow.set_z_index(12)

        little_patch = VGroup(box, little_lines)
        little_patch.set_z_index(10)

        # Transformed geometry targets
        F_p_dot = Dot(F_p, radius=0.045, color=HIGHLIGHT)
        F_p_dot.set_z_index(15)

        target_x_arrow = Arrow(
            F_p,
            F_map(p + np.array([delta, 0.0, 0.0])),
            buff=0,
            color=X_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.30,
        )
        target_x_arrow.set_z_index(12)

        target_y_arrow = Arrow(
            F_p,
            F_map(p + np.array([0.0, delta, 0.0])),
            buff=0,
            color=Y_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.30,
        )
        target_y_arrow.set_z_index(12)

        # First frame shows the givens
        self.add(faint_plane, warp_plane, little_patch, p_dot, p_lbl, x_arrow, y_arrow, formula)
        self.wait(1.5)

        # 1. Zoom the camera in on p BEFORE applying F
        self.play(
            FadeOut(p_lbl),
            FadeOut(formula),
            self.camera.frame.animate.set(width=zoom_width).move_to(p),
            run_time=2.2,
        )
        self.wait(1.8)

        # 2. Zoom out to wide view
        self.play(
            FadeIn(formula),
            self.camera.frame.animate.set(width=10.0).move_to(ORIGIN),
            run_time=2.0,
        )
        self.wait(0.5)

        # 3. Apply F globally
        self.play(
            ApplyPointwiseFunction(F_map, warp_plane),
            ApplyPointwiseFunction(F_map, little_patch),
            Transform(p_dot, F_p_dot),
            Transform(x_arrow, target_x_arrow),
            Transform(y_arrow, target_y_arrow),
            run_time=3.5,
        )
        self.wait(1.0)

        # 4. Zoom the camera in on F(p) AFTER applying F
        self.play(
            FadeOut(formula),
            self.camera.frame.animate.set(width=zoom_width).move_to(F_p),
            run_time=2.2,
        )

        # 5. Caption at the top of the zoomed view (completely clear of any lines)
        caption = MathTex(
            r"\text{zoomed in, } F \text{ looks linear}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        caption.scale(scale_fac)
        caption.move_to(self.camera.frame.get_top() + DOWN * 0.40 * scale_fac)
        caption.add_background_rectangle(color=BG, opacity=1.0, buff=0.12 * scale_fac)
        caption.set_z_index(30)

        self.play(FadeIn(caption, shift=DOWN * 0.1 * scale_fac), run_time=1.5)
        self.wait(4.0)


class JacobianColumns(Scene):
    def construct(self):
        # Scale for local coordinate plane on the left (fills ~50% width and ~60% height)
        S = 2.20
        origin_pt = np.array([-4.50, -1.50, 0.0])

        # Local axes on the left half
        local_x_axis = Line(
            origin_pt + np.array([-0.25, 0.0, 0.0]),
            origin_pt + np.array([1.50 * S, 0.0, 0.0]),
            stroke_color=INK_DIM,
            stroke_width=2.5,
        )
        local_y_axis = Line(
            origin_pt + np.array([0.0, -0.25, 0.0]),
            origin_pt + np.array([0.0, 1.35 * S, 0.0]),
            stroke_color=INK_DIM,
            stroke_width=2.5,
        )

        # Faint local grid lines
        grid_lines = VGroup()
        grid_lines.add(
            Line(
                origin_pt + np.array([S, -0.20, 0.0]),
                origin_pt + np.array([S, 1.32 * S, 0.0]),
                stroke_color=GRID,
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
        )
        grid_lines.add(
            Line(
                origin_pt + np.array([-0.20, S, 0.0]),
                origin_pt + np.array([1.45 * S, S, 0.0]),
                stroke_color=GRID,
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
        )

        # Axis ticks / labels
        tick_x = MathTex(r"\Delta x", tex_template=tex_tmpl, font_size=MIN_FONT, color=X_COLOR)
        tick_x.next_to(origin_pt + np.array([S, 0.0, 0.0]), DOWN, buff=0.15)
        tick_x.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        tick_y = MathTex(r"\Delta y", tex_template=tex_tmpl, font_size=MIN_FONT, color=Y_COLOR)
        tick_y.next_to(origin_pt + np.array([0.0, S, 0.0]), LEFT, buff=0.15)
        tick_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.06)

        # Initial unit square before transformation
        initial_square = Polygon(
            origin_pt,
            origin_pt + np.array([S, 0.0, 0.0]),
            origin_pt + np.array([S, S, 0.0]),
            origin_pt + np.array([0.0, S, 0.0]),
            stroke_color=INK_FAINT,
            stroke_width=1.5,
            stroke_opacity=0.5,
            fill_color=BG,
            fill_opacity=0.0,
        )

        # Ghost lines of the initial basis vectors
        ghost_x = DashedLine(
            origin_pt,
            origin_pt + np.array([S, 0.0, 0.0]),
            color=INK_FAINT,
            stroke_width=2.5,
            dash_length=0.12,
        )
        ghost_y = DashedLine(
            origin_pt,
            origin_pt + np.array([0.0, S, 0.0]),
            color=INK_FAINT,
            stroke_width=2.5,
            dash_length=0.12,
        )

        # Initial basis arrows at p
        arrow_x = Arrow(
            origin_pt,
            origin_pt + np.array([S, 0.0, 0.0]),
            buff=0,
            color=X_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow_x.set_z_index(10)

        arrow_y = Arrow(
            origin_pt,
            origin_pt + np.array([0.0, S, 0.0]),
            buff=0,
            color=Y_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow_y.set_z_index(10)

        # Landed arrow targets:
        # Col 1: (1, cos(1)/2) ≈ (1, 0.270)
        # Col 2: (cos(0.5)/2, 1) ≈ (0.439, 1)
        v1 = np.array([1.0 * S, (np.cos(1.0) / 2.0) * S, 0.0])
        v2 = np.array([(np.cos(0.5) / 2.0) * S, 1.0 * S, 0.0])

        landed_arrow_x = Arrow(
            origin_pt,
            origin_pt + v1,
            buff=0,
            color=X_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        landed_arrow_x.set_z_index(10)

        landed_arrow_y = Arrow(
            origin_pt,
            origin_pt + v2,
            buff=0,
            color=Y_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.18,
        )
        landed_arrow_y.set_z_index(10)

        # Transformed parallelogram
        parallelogram = Polygon(
            origin_pt,
            origin_pt + v1,
            origin_pt + v1 + v2,
            origin_pt + v2,
            stroke_color=RESULT_COLOR,
            stroke_width=3,
            fill_color=RESULT_COLOR,
            fill_opacity=0.30,
        )
        parallelogram.set_z_index(5)

        # RIGHT SIDE: Mathematical formulas centered in the right half
        right_x = (2.15 - 0.30)

        # 1. Symbolic Jacobian matrix with colored columns (inline partials)
        formula_sym = MathTex(
            r"J = \begin{bmatrix} "
            r"{\color[HTML]{8bd17c} \partial F_1/\partial x} & {\color[HTML]{e8798a} \partial F_1/\partial y} \\[6pt] "
            r"{\color[HTML]{8bd17c} \partial F_2/\partial x} & {\color[HTML]{e8798a} \partial F_2/\partial y} "
            r"\end{bmatrix}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=INK,
        )
        formula_sym.move_to(np.array([right_x + 0.20, 1.35, 0.0]))
        formula_sym.add_background_rectangle(color=BG, opacity=0.92, buff=0.10)
        formula_sym.set_z_index(20)

        # 2. Evaluated at p: inline cosines so glyphs stay >= MIN_FONT
        line_exact = MathTex(
            r"J(p) = \begin{bmatrix} "
            r"{\color[HTML]{8bd17c} 1} & {\color[HTML]{e8798a} \cos(0.5)/2} \\[6pt] "
            r"{\color[HTML]{8bd17c} \cos(1)/2} & {\color[HTML]{e8798a} 1} "
            r"\end{bmatrix}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=INK,
        )
        line_exact.move_to(np.array([right_x, 1.35, 0.0]))
        line_exact.add_background_rectangle(color=BG, opacity=0.92, buff=0.10)
        line_exact.set_z_index(20)

        # 3. Decimal values aligned with the exact matrix columns
        line_num = MathTex(
            r"\approx \begin{bmatrix} "
            r"{\color[HTML]{8bd17c} 1} & {\color[HTML]{e8798a} 0.44} \\[4pt] "
            r"{\color[HTML]{8bd17c} 0.27} & {\color[HTML]{e8798a} 1} "
            r"\end{bmatrix}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=INK,
        )
        line_num.move_to(np.array([right_x + 0.32, 0.05, 0.0]))
        line_num.add_background_rectangle(color=BG, opacity=0.92, buff=0.10)
        line_num.set_z_index(20)

        # 4. Determinant & local area scaling (final lines of right column)
        det_lbl = MathTex(
            r"\det J(p) \approx 0.88",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        det_lbl.move_to(np.array([right_x + 0.35, -1.05, 0.0]))
        det_lbl.add_background_rectangle(color=BG, opacity=0.92, buff=0.10)
        det_lbl.set_z_index(20)

        scaling_lbl = MathTex(
            r"\text{local area scaling}",
            tex_template=tex_tmpl,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        scaling_lbl.move_to(np.array([right_x + 0.35, -1.65, 0.0]))
        scaling_lbl.add_background_rectangle(color=BG, opacity=0.92, buff=0.10)
        scaling_lbl.set_z_index(20)

        # First frame shows the givens: local axes, unit square, initial basis arrows
        self.add(
            local_x_axis,
            local_y_axis,
            grid_lines,
            initial_square,
            arrow_x,
            arrow_y,
            tick_x,
            tick_y,
        )
        self.wait(1.2)

        # Show arrows landing and square shearing into parallelogram
        self.add(ghost_x, ghost_y)
        self.play(
            Transform(arrow_x, landed_arrow_x),
            Transform(arrow_y, landed_arrow_y),
            Transform(initial_square, parallelogram),
            FadeOut(tick_x),
            FadeOut(tick_y),
            run_time=2.0,
        )
        self.wait(1.6)

        # Step 1: Symbolic Jacobian J with colored columns
        self.play(FadeIn(formula_sym, shift=LEFT * 0.15), run_time=1.5)
        self.wait(5.2)

        # Step 2: Transform symbolic J to evaluated J(p) with inline cosines
        self.play(FadeTransform(formula_sym, line_exact), run_time=1.4)
        self.wait(0.4)

        # Step 3: Decimal numbers matrix
        self.play(FadeIn(line_num, shift=UP * 0.15), run_time=1.2)
        self.wait(3.5)

        # Step 4: Determinant & local area scaling
        self.play(
            FadeIn(det_lbl, shift=UP * 0.10),
            FadeIn(scaling_lbl, shift=UP * 0.10),
            run_time=1.4,
        )
        self.wait(2.6)
