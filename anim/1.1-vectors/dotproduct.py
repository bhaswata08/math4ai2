# Adapted from 3b1b/videos _2016/eola/chapter7.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

import numpy as np
from shared.anim.house import *


class DotNumerically(Scene):
    """Adapted from ShowNumericalDotProduct / TwoDDotProductExample."""

    def construct(self):
        # [1, 2] . [3, 4] = 1*3 + 2*4 = 3 + 8 = 11
        # No plane needed; the equation fills the frame at a large size.
        # First pair: X_COLOR, second pair: Y_COLOR.

        m1 = IntegerMatrix([[1], [2]], element_to_mobject_config={"font_size": 48})
        m1.get_brackets().set_color(INK)
        m1.get_entries()[0].set_color(X_COLOR)
        m1.get_entries()[1].set_color(Y_COLOR)

        dot_sym = MathTex(r"\cdot", font_size=56, color=INK)

        m2 = IntegerMatrix([[3], [4]], element_to_mobject_config={"font_size": 48})
        m2.get_brackets().set_color(INK)
        m2.get_entries()[0].set_color(X_COLOR)
        m2.get_entries()[1].set_color(Y_COLOR)

        givens = VGroup(m1, dot_sym, m2).arrange(RIGHT, buff=0.2)
        givens.move_to(ORIGIN)

        # 1. Frame one shows the givens
        self.add(givens)
        self.wait(1.5)

        # Shift givens left to make room for evaluation
        target_pos = np.array([-3.2, 0.0, 0.0])
        self.play(givens.animate.move_to(target_pos), run_time=1.2)
        self.wait(0.5)

        # 2. Pair matching entries with subtle arcs
        arc_x = CurvedArrow(
            m1.get_entries()[0].get_top() + 0.08 * UP,
            m2.get_entries()[0].get_top() + 0.08 * UP,
            angle=-TAU / 4,
            color=X_COLOR,
            stroke_width=3,
        )
        arc_y = CurvedArrow(
            m1.get_entries()[1].get_bottom() + 0.08 * DOWN,
            m2.get_entries()[1].get_bottom() + 0.08 * DOWN,
            angle=TAU / 4,
            color=Y_COLOR,
            stroke_width=3,
        )
        self.play(Create(arc_x), Create(arc_y), run_time=1.0)
        self.wait(0.5)

        # 3. Write: = 1*3 + 2*4
        step1 = MathTex(
            r"=",
            r"1",
            r"\cdot",
            r"3",
            r"+",
            r"2",
            r"\cdot",
            r"4",
            font_size=48,
        )
        step1[0].set_color(INK)
        step1[1].set_color(X_COLOR)
        step1[2].set_color(INK)
        step1[3].set_color(X_COLOR)
        step1[4].set_color(INK)
        step1[5].set_color(Y_COLOR)
        step1[6].set_color(INK)
        step1[7].set_color(Y_COLOR)
        step1.next_to(givens, RIGHT, buff=0.25)

        self.play(Write(step1), run_time=1.5)
        self.play(FadeOut(arc_x), FadeOut(arc_y), run_time=0.6)
        self.wait(0.8)

        # 4. Write: = 3 + 8
        step2 = MathTex(
            r"=",
            r"3",
            r"+",
            r"8",
            font_size=48,
        )
        step2[0].set_color(INK)
        step2[1].set_color(X_COLOR)
        step2[2].set_color(INK)
        step2[3].set_color(Y_COLOR)
        step2.next_to(step1, RIGHT, buff=0.25)

        self.play(Write(step2), run_time=1.2)
        self.wait(0.8)

        # 5. Write: = 11
        step3 = MathTex(
            r"=",
            r"11",
            font_size=52,
        )
        step3[0].set_color(INK)
        step3[1].set_color(RESULT_COLOR)
        step3.next_to(step2, RIGHT, buff=0.25)

        self.play(Write(step3), run_time=1.0)
        self.wait(2.5)


class DotNumerically4D(Scene):
    """Adapted from FourDDotProductExample."""

    def construct(self):
        # [6, 2, 8, 3] . [1, 8, 5, 3] = 6 + 16 + 40 + 9 = 71
        # Pair colours: X_COLOR, Y_COLOR, W_COLOR, HIGHLIGHT

        colors = [X_COLOR, Y_COLOR, W_COLOR, HIGHLIGHT]
        v1_vals = [6, 2, 8, 3]
        v2_vals = [1, 8, 5, 3]

        m1 = IntegerMatrix([[x] for x in v1_vals], element_to_mobject_config={"font_size": 42})
        m1.get_brackets().set_color(INK)
        for entry, col in zip(m1.get_entries(), colors):
            entry.set_color(col)

        dot_sym = MathTex(r"\cdot", font_size=52, color=INK)

        m2 = IntegerMatrix([[x] for x in v2_vals], element_to_mobject_config={"font_size": 42})
        m2.get_brackets().set_color(INK)
        for entry, col in zip(m2.get_entries(), colors):
            entry.set_color(col)

        givens = VGroup(m1, dot_sym, m2).arrange(RIGHT, buff=0.2)
        givens.move_to(np.array([-3.2, 0.0, 0.0]))

        # 1. Frame one shows the givens
        self.add(givens)
        self.wait(1.5)

        # Rule works in any dimension tag
        title = Tex("The same rule works in any dimension", font_size=MIN_FONT, color=INK_DIM)
        title.to_edge(UP, buff=0.35)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # Line 1: = 6*1 + 2*8 + 8*5 + 3*3
        l1 = MathTex(
            r"=",
            r"6\cdot 1",
            r"+",
            r"2\cdot 8",
            r"+",
            r"8\cdot 5",
            r"+",
            r"3\cdot 3",
            font_size=42,
        )
        l1[0].set_color(INK)
        l1[1].set_color(X_COLOR)
        l1[2].set_color(INK)
        l1[3].set_color(Y_COLOR)
        l1[4].set_color(INK)
        l1[5].set_color(W_COLOR)
        l1[6].set_color(INK)
        l1[7].set_color(HIGHLIGHT)
        l1.move_to(np.array([0.9, 0.85, 0.0]))

        self.play(Write(l1), run_time=1.8)
        self.wait(0.8)

        # Line 2: = 6 + 16 + 40 + 9 (aligned to left of l1)
        l2 = MathTex(
            r"=",
            r"6",
            r"+",
            r"16",
            r"+",
            r"40",
            r"+",
            r"9",
            font_size=42,
        )
        l2[0].set_color(INK)
        l2[1].set_color(X_COLOR)
        l2[2].set_color(INK)
        l2[3].set_color(Y_COLOR)
        l2[4].set_color(INK)
        l2[5].set_color(W_COLOR)
        l2[6].set_color(INK)
        l2[7].set_color(HIGHLIGHT)
        l2.next_to(l1, DOWN, buff=0.55, aligned_edge=LEFT)

        self.play(Write(l2), run_time=1.5)
        self.wait(0.8)

        # Line 3: = 71 (aligned to left of l1)
        l3 = MathTex(
            r"=",
            r"71",
            font_size=50,
        )
        l3[0].set_color(INK)
        l3[1].set_color(RESULT_COLOR)
        l3.next_to(l2, DOWN, buff=0.55, aligned_edge=LEFT)

        self.play(Write(l3), run_time=1.0)
        self.wait(2.5)


class DotGeometric(Scene):
    """Adapted from GeometricInterpretation."""

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Upstream vectors: v = [4, 1], w = [2, -1]
        # Both satisfy |x| <= 4.7 and |y| <= 2.5
        v_coords = np.array([4.0, 1.0, 0.0])
        w_coords = np.array([2.0, -1.0, 0.0])

        v_len_sq = np.dot(v_coords, v_coords)  # 17.0
        dot_prod = np.dot(v_coords, w_coords)  # 7.0
        proj_coords = (dot_prod / v_len_sq) * v_coords  # (28/17, 7/17, 0)

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_coords, UR, buff=0.15)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w_arr = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w_coords, DR, buff=0.15)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w
        self.add(v_arr, l_v, w_arr, l_w)
        self.wait(1.5)

        # 2. Line through v
        u_v = v_coords / np.linalg.norm(v_coords)
        line_v = Line(-2.2 * u_v, 4.4 * u_v, color=INK_DIM, stroke_width=2.5)
        self.play(Create(line_v), run_time=1.5)
        self.wait(0.5)

        # 3. Dashed drop line from w to line through v
        drop_line = DashedLine(
            w_coords,
            proj_coords,
            color=INK_DIM,
            stroke_width=3,
            dash_length=0.08,
        )
        self.play(Create(drop_line), run_time=1.2)
        self.wait(0.5)

        # 4. Projection vector along v
        proj_arr = Arrow(
            ORIGIN,
            proj_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_proj = MathTex(r"\text{proj}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_proj.move_to(np.array([1.25, 0.85, 0.0]))
        l_proj.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(GrowArrow(proj_arr), Write(l_proj), run_time=1.3)
        self.wait(0.8)

        # 5. Formula: length of projection x length of v
        formula = MathTex(
            r"\vec{v} \cdot \vec{w} =",
            r"(\text{length of projection})",
            r"\times",
            r"(\text{length of }\vec{v})",
            font_size=MIN_FONT,
        )
        formula[0].set_color(INK)
        formula[1].set_color(RESULT_COLOR)
        formula[2].set_color(INK)
        formula[3].set_color(V_COLOR)
        formula.to_edge(UP, buff=0.35)
        formula.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(Write(formula), run_time=2.0)
        self.wait(2.5)


class DotNegative(Scene):
    """Adapted from GeometricInterpretationNegative."""

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Upstream vectors: v = [3, 1], w = [-1, -2]
        # v . w = -5 < 0; projection lands on the opposite side of origin
        v_coords = np.array([3.0, 1.0, 0.0])
        w_coords = np.array([-1.0, -2.0, 0.0])

        v_len_sq = np.dot(v_coords, v_coords)  # 10.0
        dot_prod = np.dot(v_coords, w_coords)  # -5.0
        proj_coords = (dot_prod / v_len_sq) * v_coords  # (-1.5, -0.5, 0.0)

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_coords, UR, buff=0.15)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w_arr = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w_coords, DL, buff=0.15)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w
        self.add(v_arr, l_v, w_arr, l_w)
        self.wait(1.5)

        # 2. Line through v extending backwards
        u_v = v_coords / np.linalg.norm(v_coords)
        line_v = Line(-2.5 * u_v, 3.5 * u_v, color=INK_DIM, stroke_width=2.5)
        self.play(Create(line_v), run_time=1.5)
        self.wait(0.5)

        # 3. Dashed drop line from w to opposite side of line through v
        drop_line = DashedLine(
            w_coords,
            proj_coords,
            color=INK_DIM,
            stroke_width=3,
            dash_length=0.08,
        )
        self.play(Create(drop_line), run_time=1.2)
        self.wait(0.5)

        # 4. Projection vector pointing opposite to v
        proj_arr = Arrow(
            ORIGIN,
            proj_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        # Position label clearly above x-axis to maintain > 0.15 clearance
        l_proj = MathTex(r"\text{proj}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_proj.move_to(np.array([-1.2, 0.65, 0.0]))
        l_proj.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(GrowArrow(proj_arr), Write(l_proj), run_time=1.3)
        self.wait(0.8)

        # 5. Formula showing negative sign
        formula = MathTex(
            r"\vec{v} \cdot \vec{w} =",
            r"-",
            r"(\text{length of projection})",
            r"\times",
            r"(\text{length of }\vec{v})",
            font_size=MIN_FONT,
        )
        formula[0].set_color(INK)
        formula[1].set_color(HIGHLIGHT)
        formula[2].set_color(RESULT_COLOR)
        formula[3].set_color(INK)
        formula[4].set_color(V_COLOR)
        formula.to_edge(UP, buff=0.35)
        formula.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        note = Tex(
            r"Opposite side $\implies \vec{v}\cdot\vec{w} < 0$",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        note.next_to(formula, DOWN, buff=0.2)
        note.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(formula), run_time=2.0)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(2.5)


class DotSign(Scene):
    """Adapted from ShowQualitativeDotProductValues."""

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Fixed v along x-axis for crystal-clear sign visualization
        v_coords = np.array([2.0, 0.0, 0.0])
        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.move_to(np.array([2.25, 0.45, 0.0]))
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Beat 1: w1 at acute angle (v.w > 0)
        w1_coords = np.array([1.2, 1.0, 0.0])
        w_arr = Arrow(
            ORIGIN,
            w1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w1_coords, UR, buff=0.18)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w1
        self.add(v_arr, l_v, w_arr, l_w)
        self.wait(1.5)

        # Reference line along v extending backwards
        line_v = Line(np.array([-2.2, 0.0, 0.0]), np.array([2.5, 0.0, 0.0]), color=INK_DIM, stroke_width=2.5)
        self.play(Create(line_v), run_time=1.0)

        # --- Beat 1: Acute angle, v.w > 0 ---
        proj1_coords = np.array([1.2, 0.0, 0.0])
        drop1 = DashedLine(w1_coords, proj1_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj1 = Arrow(
            ORIGIN,
            proj1_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        sign1 = MathTex(r"\vec{v} \cdot \vec{w} > 0", font_size=MIN_FONT + 6, color=INK)
        sign1.set_color_by_tex(">", X_COLOR)
        sign1.to_edge(UP, buff=0.35)
        sign1.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(Create(drop1), GrowArrow(proj1), Write(sign1), run_time=1.5)
        self.wait(1.8)

        # --- Beat 2: Perpendicular, v.w = 0 ---
        w2_coords = np.array([0.0, 1.3, 0.0])
        w2_arr = Arrow(
            ORIGIN,
            w2_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w2 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w2.next_to(w2_coords, LEFT, buff=0.22)
        l_w2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        drop2 = DashedLine(w2_coords, ORIGIN, color=INK_DIM, stroke_width=3, dash_length=0.08)
        zero_dot = Dot(ORIGIN, radius=0.1, color=RESULT_COLOR)

        sign2 = MathTex(r"\vec{v} \cdot \vec{w} = 0", font_size=MIN_FONT + 6, color=INK)
        sign2.set_color_by_tex("=", HIGHLIGHT)
        sign2.to_edge(UP, buff=0.35)
        sign2.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            Transform(w_arr, w2_arr),
            Transform(l_w, l_w2),
            Transform(drop1, drop2),
            Transform(proj1, zero_dot),
            Transform(sign1, sign2),
            run_time=2.0,
        )
        self.wait(1.8)

        # --- Beat 3: Opposite, v.w < 0 ---
        w3_coords = np.array([-1.2, 1.0, 0.0])
        w3_arr = Arrow(
            ORIGIN,
            w3_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w3 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w3.next_to(w3_coords, UL, buff=0.18)
        l_w3.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        proj3_coords = np.array([-1.2, 0.0, 0.0])
        drop3 = DashedLine(w3_coords, proj3_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj3 = Arrow(
            ORIGIN,
            proj3_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        sign3 = MathTex(r"\vec{v} \cdot \vec{w} < 0", font_size=MIN_FONT + 6, color=INK)
        sign3.set_color_by_tex("<", Y_COLOR)
        sign3.to_edge(UP, buff=0.35)
        sign3.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)

        self.play(
            Transform(w_arr, w3_arr),
            Transform(l_w, l_w3),
            Transform(drop1, drop3),
            Transform(proj1, proj3),
            Transform(sign1, sign3),
            run_time=2.0,
        )
        self.wait(2.5)


class DotSymmetric(Scene):
    """Adapted from SymmetricVAndW."""

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Equal length vectors symmetric across line y = x:
        # Upstream used [3, 1] and [1, 3], which exceeded the frame (|y| <= 2.5).
        # We rescale to v = [1.4, 0.35] and w = [0.35, 1.4], both norm sqrt(2.08) ~= 1.44.
        v_coords = np.array([1.4, 0.35, 0.0])
        w_coords = np.array([0.35, 1.4, 0.0])

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_coords, UP, buff=0.18)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        w_arr = Arrow(
            ORIGIN,
            w_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w_coords, RIGHT, buff=0.18)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title = MathTex(
            r"\vec{v} \cdot \vec{w} = \vec{w} \cdot \vec{v}",
            font_size=MIN_FONT + 4,
        )
        title.set_color_by_tex(r"\vec{v}", V_COLOR)
        title.set_color_by_tex(r"\vec{w}", W_COLOR)
        title.to_edge(UP, buff=0.3)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        # 1. Frame one shows givens: plane, v, w, and symmetry title
        self.add(v_arr, l_v, w_arr, l_w, title)
        self.wait(1.5)

        # 2. Line of symmetry y = x
        sym_line = DashedLine(
            np.array([-2.2, -2.2, 0.0]),
            np.array([2.0, 2.0, 0.0]),
            color=INK_DIM,
            stroke_width=2.5,
            dash_length=0.12,
        )
        sym_label = Tex("Line of symmetry", font_size=MIN_FONT, color=INK_DIM)
        sym_label.next_to(np.array([-1.2, -1.2, 0.0]), DR, buff=0.2)
        sym_label.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(sym_line), Write(sym_label), run_time=1.5)
        self.wait(1.0)

        # 3. Projections when vectors have equal length
        dot_val = np.dot(v_coords, w_coords)  # 1.4*0.35 + 0.35*1.4 = 0.98
        proj_w_coords = (dot_val / np.dot(v_coords, v_coords)) * v_coords
        drop_w = DashedLine(w_coords, proj_w_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj_w = Arrow(
            ORIGIN,
            proj_w_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        proj_v_coords = (dot_val / np.dot(w_coords, w_coords)) * w_coords
        drop_v = DashedLine(v_coords, proj_v_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj_v = Arrow(
            ORIGIN,
            proj_v_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        equal_step1 = Tex(r"Equal lengths", font_size=MIN_FONT, color=RESULT_COLOR)
        equal_step2 = Tex(r"$\implies$ equal projections", font_size=MIN_FONT, color=RESULT_COLOR)
        equal_note = VGroup(equal_step1, equal_step2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        equal_note.move_to(np.array([-2.7, 1.2, 0.0]))
        equal_note.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Create(drop_w),
            GrowArrow(proj_w),
            Create(drop_v),
            GrowArrow(proj_v),
            Write(equal_note),
            run_time=2.0,
        )
        self.wait(2.0)

        # 4. Fade projections to prepare for scaling
        self.play(
            FadeOut(drop_w),
            FadeOut(proj_w),
            FadeOut(drop_v),
            FadeOut(proj_v),
            FadeOut(equal_note),
            FadeOut(sym_label),
            FadeOut(sym_line),
            run_time=1.0,
        )

        # 5. Scale v by 2: v -> 2v = [2.8, 0.7, 0.0] (stays inside |x| <= 4.7, |y| <= 2.5)
        v2_coords = 2.0 * v_coords
        v2_arr = Arrow(
            ORIGIN,
            v2_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v2 = MathTex(r"2\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v2.next_to(v2_coords, UP, buff=0.18)
        l_v2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Concise proof steps placed cleanly in quadrant 3 (clears all axes)
        scale_title = Tex(r"Scale $\vec{v}$ by 2:", font_size=MIN_FONT, color=RESULT_COLOR)
        scale_step1 = MathTex(r"(2\vec{v})\cdot\vec{w} = 2(\vec{v}\cdot\vec{w})", font_size=MIN_FONT, color=INK)
        scale_step2 = MathTex(r"\vec{w}\cdot(2\vec{v}) = 2(\vec{w}\cdot\vec{v})", font_size=MIN_FONT, color=INK)
        proof_box = VGroup(scale_title, scale_step1, scale_step2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        proof_box.move_to(np.array([-2.5, -1.2, 0.0]))
        proof_box.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Transform(v_arr, v2_arr),
            Transform(l_v, l_v2),
            Write(proof_box),
            run_time=2.0,
        )
        self.wait(2.5)
