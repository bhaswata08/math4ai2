# Block 1.2 scenes, authored for this course in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class ProjectionFormula(Scene):
    r"""v and w, the line through v, w dropped perpendicular onto it, the shadow proj_v w (RESULT_COLOR);

    formula proj_v w = (v.w / v.v) v built in steps; right angle mark at the foot.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Givens: v = [3, 1], w = [1, 2]
        # v . w = 3*1 + 1*2 = 5
        # v . v = 3^2 + 1^2 = 10
        # proj = (5/10) v = 0.5 * [3, 1] = [1.5, 0.5]
        v_coords = np.array([3.0, 1.0, 0.0])
        w_coords = np.array([1.0, 2.0, 0.0])
        proj_coords = np.array([1.5, 0.5, 0.0])

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_coords, DR, buff=0.18)
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
        l_w.next_to(w_coords, UL, buff=0.18)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        c_v = MathTex(r"\begin{bmatrix} 3 \\ 1 \end{bmatrix}", font_size=MIN_FONT, color=V_COLOR)
        c_v.next_to(v_coords, UR, buff=0.12)
        c_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)
        c_w = MathTex(r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}", font_size=MIN_FONT, color=W_COLOR)
        c_w.next_to(w_coords, RIGHT, buff=0.25)
        c_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.06)

        # 1. Frame one shows givens: plane, v, w, labels and coordinates
        self.add(v_arr, l_v, c_v, w_arr, l_w, c_w)
        self.wait(1.5)

        # 2. Line through v
        u_v = v_coords / np.linalg.norm(v_coords)
        line_v = Line(-1.8 * u_v, 4.2 * u_v, color=INK_DIM, stroke_width=2.5)
        self.play(Create(line_v), run_time=1.2)
        self.wait(0.4)

        # 3. Dashed drop line from w perpendicular to line through v
        drop_line = DashedLine(
            w_coords,
            proj_coords,
            color=INK_DIM,
            stroke_width=3,
            dash_length=0.08,
        )

        # Right angle mark at foot [1.5, 0.5]
        u_n = (w_coords - proj_coords) / np.linalg.norm(w_coords - proj_coords)
        s = 0.22
        p1 = proj_coords - s * u_v
        p2 = proj_coords - s * u_v + s * u_n
        p3 = proj_coords + s * u_n
        elbow = VGroup(
            Line(p1, p2, stroke_width=2.5, color=HIGHLIGHT),
            Line(p2, p3, stroke_width=2.5, color=HIGHLIGHT),
        )

        self.play(Create(drop_line), Create(elbow), run_time=1.2)
        self.wait(0.4)

        # 4. Projection vector along v
        proj_arr = Arrow(
            ORIGIN,
            proj_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_proj = MathTex(r"\text{proj}_{\vec{v}}\vec{w}", font_size=MIN_FONT - 4, color=RESULT_COLOR)
        l_proj.next_to(proj_coords, DR, buff=0.2)
        l_proj.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(GrowArrow(proj_arr), Write(l_proj), run_time=1.2)
        self.wait(0.8)

        # 5. Formula built in steps on the left
        # Direction times magnitude, as formulas only: the coordinates at the
        # tips are the givens, the slide after this works the numbers.
        eq1 = MathTex(r"\hat{v} = \frac{\vec{v}}{\|\vec{v}\|}", font_size=MIN_FONT, color=V_COLOR)
        note1 = Tex("direction", font_size=MIN_FONT, color=INK_DIM)
        step1 = VGroup(eq1, note1).arrange(RIGHT, buff=0.35)
        step1.to_corner(UL, buff=0.3)
        step1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        eq2 = MathTex(r"\hat{v} \cdot \vec{w} = \|\vec{w}\| \cos\theta", font_size=MIN_FONT)
        note2 = Tex("shadow length", font_size=MIN_FONT, color=INK_DIM)
        step2 = VGroup(eq2, note2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        step2.next_to(step1, DOWN, buff=0.3, aligned_edge=LEFT)
        step2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        step3 = MathTex(
            r"\text{proj}_{\vec{v}}\vec{w} = \hat{v}\,(\hat{v} \cdot \vec{w})",
            font_size=MIN_FONT + 4,
            color=RESULT_COLOR,
        )
        step3.next_to(step2, DOWN, buff=0.35, aligned_edge=LEFT)
        step3.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Background rectangles skew aligned_edge, so pin every line to one margin.
        for m in (step1, step2, step3):
            m.to_edge(LEFT, buff=0.3)

        self.play(Write(step1), run_time=1.2)
        self.wait(0.6)
        self.play(Write(step2), run_time=1.4)
        self.wait(0.6)
        self.play(Write(step3), run_time=1.4)
        self.wait(3.0)
