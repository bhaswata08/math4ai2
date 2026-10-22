# Adapted from 3b1b/videos _2016/eola/chapter2.py CoordinatesAsScalars, (c) 3Blue1Brown, CC BY-NC-SA 4.0
# Adapted from 3b1b/videos _2016/eola/chapter2.py ShowVaryingLinearCombinations, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np

from shared.anim.house import *


class BasisScalars(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Standard basis vectors
        i_coords = np.array([1.0, 0.0, 0.0])
        j_coords = np.array([0.0, 1.0, 0.0])

        i_vec = Arrow(
            ORIGIN,
            i_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=X_COLOR,
        )
        i_label = MathTex(r"\hat{\imath}", font_size=MIN_FONT, color=X_COLOR)
        i_label.next_to(i_vec.get_center(), UP, buff=0.18)
        i_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        j_vec = Arrow(
            ORIGIN,
            j_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=Y_COLOR,
        )
        j_label = MathTex(r"\hat{\jmath}", font_size=MIN_FONT, color=Y_COLOR)
        j_label.next_to(j_vec.get_center(), LEFT, buff=0.18)
        j_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Target vector coordinates [3, -2]
        coord_mat = IntegerMatrix(
            [[3], [-2]],
            element_to_mobject_config={"font_size": MIN_FONT},
        )
        coord_mat.get_brackets().set_color(INK)
        coord_mat.get_entries()[0].set_color(X_COLOR)
        coord_mat.get_entries()[1].set_color(Y_COLOR)
        coord_mat.to_corner(UL, buff=0.4)
        coord_mat.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # Frame 1 givens
        self.add(i_vec, i_label, j_vec, j_label, coord_mat)
        self.wait(1.5)

        # 1. Scale i_hat by 3
        i_ghost = i_vec.copy().fade(0.7)
        self.add(i_ghost)

        scaled_i_coords = np.array([3.0, 0.0, 0.0])
        scaled_i_vec = Arrow(
            ORIGIN,
            scaled_i_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=X_COLOR,
        )
        scaled_i_label = MathTex(r"3\hat{\imath}", font_size=MIN_FONT, color=X_COLOR)
        scaled_i_label.next_to(scaled_i_vec.get_center(), UP, buff=0.18)
        scaled_i_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(i_vec, scaled_i_vec),
            Transform(i_label, scaled_i_label),
            run_time=1.8,
        )
        self.wait(0.8)

        # 2. Scale j_hat by -2
        j_ghost = j_vec.copy().fade(0.7)
        self.add(j_ghost)

        scaled_j_coords = np.array([0.0, -2.0, 0.0])
        scaled_j_vec = Arrow(
            ORIGIN,
            scaled_j_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=Y_COLOR,
        )
        scaled_j_label = MathTex(r"-2\hat{\jmath}", font_size=MIN_FONT, color=Y_COLOR)
        scaled_j_label.next_to(scaled_j_vec.get_center(), LEFT, buff=0.18)
        scaled_j_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(j_vec, scaled_j_vec),
            Transform(j_label, scaled_j_label),
            run_time=1.8,
        )
        self.wait(0.8)

        # 3. Tip to tail: shift scaled j to tip of scaled i
        shifted_j_label = MathTex(r"-2\hat{\jmath}", font_size=MIN_FONT, color=Y_COLOR)
        shifted_j_label.next_to(np.array([3.0, -1.0, 0.0]), RIGHT, buff=0.18)
        shifted_j_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            j_vec.animate.shift(scaled_i_coords),
            Transform(j_label, shifted_j_label),
            run_time=2.0,
        )
        self.wait(0.8)

        # 4. Result vector [3, -2]
        res_coords = np.array([3.0, -2.0, 0.0])
        res_vec = Arrow(
            ORIGIN,
            res_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        # Formula at top-left: 3\hat{\imath} + (-2)\hat{\jmath} = [3, -2]^T
        lin_combo_eq = MathTex(
            r"3\hat{\imath} + (-2)\hat{\jmath}",
            font_size=MIN_FONT,
        )
        lin_combo_eq[0][:2].set_color(X_COLOR)
        lin_combo_eq[0][2].set_color(INK)
        lin_combo_eq[0][3:8].set_color(Y_COLOR)

        eq_full = VGroup(
            lin_combo_eq,
            MathTex(r"=", font_size=MIN_FONT, color=INK),
            coord_mat.copy(),
        ).arrange(RIGHT, buff=0.15)
        eq_full.to_corner(UL, buff=0.4)
        eq_full.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            GrowArrow(res_vec),
            FadeOut(coord_mat),
            FadeIn(eq_full),
            run_time=2.0,
        )
        self.wait(2.5)


class LinearCombinationVary(Scene):
    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Fixed vectors v = [1.5, 0.5], w = [-0.6, 1.2]
        v_coords = np.array([1.5, 0.5, 0.0])
        w_coords = np.array([-0.6, 1.2, 0.0])

        # Faded reference basis vectors at origin
        v_ghost = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        ).fade(0.65)
        v_ghost_label = MathTex(r"\vec{v}", font_size=MIN_FONT - 4, color=V_COLOR)
        v_ghost_label.fade(0.5).next_to(v_coords, DR, buff=0.12)
        v_ghost_label.add_background_rectangle(color=BG, opacity=0.8, buff=0.06)

        w_ghost = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        ).fade(0.65)
        w_ghost_label = MathTex(r"\vec{w}", font_size=MIN_FONT - 4, color=W_COLOR)
        w_ghost_label.fade(0.5).next_to(w_coords, UL, buff=0.12)
        w_ghost_label.add_background_rectangle(color=BG, opacity=0.8, buff=0.06)

        self.add(v_ghost, v_ghost_label, w_ghost, w_ghost_label)

        # ValueTrackers for scalars a and b
        a_tracker = ValueTracker(1.0)
        b_tracker = ValueTracker(1.0)

        # Live formula display using DecimalNumber (fast, no LaTeX recompilation per frame)
        bg_rect = Rectangle(
            width=3.8,
            height=0.8,
            color=BG,
            fill_color=BG,
            fill_opacity=0.9,
            stroke_color=GRID,
            stroke_width=1,
        )
        bg_rect.to_corner(UL, buff=0.4)

        a_num = DecimalNumber(1.0, num_decimal_places=1, font_size=MIN_FONT, color=V_COLOR)
        a_num.add_updater(lambda m: m.set_value(a_tracker.get_value()))

        v_sym = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        plus_glyph = MathTex("+", font_size=MIN_FONT, color=INK)
        minus_glyph = MathTex("-", font_size=MIN_FONT, color=INK)
        sign_glyph = plus_glyph.copy()

        b_num = DecimalNumber(1.0, num_decimal_places=1, font_size=MIN_FONT, color=W_COLOR)
        b_num.add_updater(lambda m: m.set_value(abs(b_tracker.get_value())))

        w_sym = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)

        def update_formula(m):
            b_val = b_tracker.get_value()
            if b_val < -1e-4:
                sign_glyph.become(minus_glyph)
            else:
                sign_glyph.become(plus_glyph)

            a_num.move_to(bg_rect.get_left() + RIGHT * 0.55)
            v_sym.next_to(a_num, RIGHT, buff=0.1)
            sign_glyph.next_to(v_sym, RIGHT, buff=0.12)
            b_num.next_to(sign_glyph, RIGHT, buff=0.12)
            w_sym.next_to(b_num, RIGHT, buff=0.1)

        formula_group = VGroup(bg_rect, a_num, v_sym, sign_glyph, b_num, w_sym)
        formula_group.add_updater(update_formula)

        # Dynamic arrow for a * v
        @always_redraw
        def dynamic_av():
            a = a_tracker.get_value()
            end = a * v_coords
            if np.linalg.norm(end) < 0.05:
                return VMobject()
            return Arrow(
                ORIGIN,
                end,
                buff=0,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.25,
                color=V_COLOR,
            )

        # Dynamic arrow for b * w (tip-to-tail from a*v)
        @always_redraw
        def dynamic_bw():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            start = a * v_coords
            end = start + b * w_coords
            if np.linalg.norm(end - start) < 0.05:
                return VMobject()
            return Arrow(
                start,
                end,
                buff=0,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.25,
                color=W_COLOR,
            )

        # Dynamic arrow for linear combination result a*v + b*w
        @always_redraw
        def dynamic_sum():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            end = a * v_coords + b * w_coords
            if np.linalg.norm(end) < 0.05:
                return Dot(ORIGIN, radius=0.08, color=RESULT_COLOR)
            return Arrow(
                ORIGIN,
                end,
                buff=0,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.25,
                color=RESULT_COLOR,
            )

        # Tip dot and traced path
        tip_dot = Dot(radius=0.09, color=RESULT_COLOR)
        tip_dot.add_updater(
            lambda d: d.move_to(
                a_tracker.get_value() * v_coords + b_tracker.get_value() * w_coords
            )
        )

        trace = TracedPath(
            tip_dot.get_center,
            stroke_color=RESULT_COLOR,
            stroke_width=3.5,
            stroke_opacity=0.6,
        )

        # Frame 1 givens
        self.add(dynamic_av, dynamic_bw, dynamic_sum, tip_dot, trace, formula_group)
        self.wait(1.2)

        # Animate sweeping through different combinations across the plane
        # Waypoint 1: quadrant 1
        self.play(
            a_tracker.animate.set_value(1.8),
            b_tracker.animate.set_value(0.4),
            run_time=2.2,
            rate_func=easeInOutCubic if hasattr(self, 'easeInOutCubic') else smooth,
        )
        self.wait(0.3)

        # Waypoint 2: upper region
        self.play(
            a_tracker.animate.set_value(0.4),
            b_tracker.animate.set_value(1.4),
            run_time=2.2,
            rate_func=smooth,
        )
        self.wait(0.3)

        # Waypoint 3: left/quadrant 2
        self.play(
            a_tracker.animate.set_value(-1.4),
            b_tracker.animate.set_value(0.9),
            run_time=2.4,
            rate_func=smooth,
        )
        self.wait(0.3)

        # Waypoint 4: bottom-left/quadrant 3
        self.play(
            a_tracker.animate.set_value(-0.9),
            b_tracker.animate.set_value(-1.2),
            run_time=2.4,
            rate_func=smooth,
        )
        self.wait(0.3)

        # Waypoint 5: bottom-right/quadrant 4
        self.play(
            a_tracker.animate.set_value(1.3),
            b_tracker.animate.set_value(-1.1),
            run_time=2.4,
            rate_func=smooth,
        )
        self.wait(0.3)

        # Waypoint 6: return to a balanced state
        self.play(
            a_tracker.animate.set_value(1.0),
            b_tracker.animate.set_value(0.6),
            run_time=2.0,
            rate_func=smooth,
        )

        # Summary note at bottom center with clear background
        summary = Tex("Linear combinations fill the 2D plane", font_size=MIN_FONT, color=INK)
        summary.to_edge(DOWN, buff=0.35)
        summary.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(FadeIn(summary, shift=0.1 * DOWN), run_time=1.2)
        self.wait(2.5)
