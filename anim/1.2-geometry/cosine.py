# Block 1.2 scenes, authored for this course in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class CosineAngle(Scene):
    r"""v and w with the angle \theta arc; v.w = ||v|| ||w|| cos \theta,

    rearranged to cos \theta = v.w / (||v|| ||w||);
    w swings through 0, 90, 180 degrees with cos \theta = 1, 0, -1 shown.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Fixed v along x-axis, length 2.6
        v_coords = np.array([2.6, 0.0, 0.0])
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

        # Swiveling w of length 2.0; initial at 45 degrees
        w0_coords = np.array([2.0 * np.cos(PI / 4), 2.0 * np.sin(PI / 4), 0.0])
        w_arr = Arrow(
            ORIGIN,
            w0_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w.next_to(w0_coords, UR, buff=0.15)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        arc = Arc(radius=0.6, start_angle=0, angle=PI / 4, color=HIGHLIGHT, stroke_width=3.5)
        l_theta = MathTex(r"\theta", font_size=MIN_FONT, color=HIGHLIGHT)
        l_theta.move_to(np.array([0.85, 0.35, 0.0]))
        l_theta.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        f1 = MathTex(r"\vec{v} \cdot \vec{w} = \|\vec{v}\| \|\vec{w}\| \cos\theta", font_size=MIN_FONT)
        f1.to_corner(UL, buff=0.35)
        f1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w, angle theta arc, formula
        self.add(v_arr, l_v, w_arr, l_w, arc, l_theta, f1)
        self.wait(1.5)

        # 2. Rearrange to cos theta
        f2 = MathTex(
            r"\cos\theta = \frac{\vec{v} \cdot \vec{w}}{\|\vec{v}\| \|\vec{w}\|}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        f2.to_corner(UL, buff=0.35)
        f2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(FadeOut(f1), FadeIn(f2), run_time=1.2)
        self.wait(0.6)

        # 3. Beat 1: w swings to 0 degrees (cos theta = 1)
        w1_coords = np.array([2.0, 0.0, 0.0])
        w1_arr = Arrow(
            ORIGIN,
            w1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w1 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w1.next_to(np.array([1.3, 0.0, 0.0]), UP, buff=0.15)
        l_w1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        r1 = MathTex(r"\theta = 0^\circ \implies \cos\theta = 1", font_size=MIN_FONT, color=RESULT_COLOR)
        r1.next_to(f2, DOWN, buff=0.25, aligned_edge=LEFT)
        r1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        r1_sub = Tex(r"Aligned", font_size=MIN_FONT - 2, color=INK_DIM)
        r1_sub.next_to(r1, DOWN, buff=0.15, aligned_edge=LEFT)
        r1_sub.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(w_arr, w1_arr),
            Transform(l_w, l_w1),
            FadeOut(arc),
            FadeOut(l_theta),
            Write(r1),
            Write(r1_sub),
            run_time=1.6,
        )
        self.wait(1.5)

        # 4. Beat 2: w swings to 90 degrees (cos theta = 0)
        w2_coords = np.array([0.0, 2.0, 0.0])
        w2_arr = Arrow(
            ORIGIN,
            w2_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w2 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w2.next_to(w2_coords, RIGHT, buff=0.18)
        l_w2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        elbow = VGroup(
            Line(np.array([0.25, 0.0, 0.0]), np.array([0.25, 0.25, 0.0])),
            Line(np.array([0.25, 0.25, 0.0]), np.array([0.0, 0.25, 0.0])),
        )
        elbow.set_stroke(color=HIGHLIGHT, width=2.5)

        r2 = MathTex(r"\theta = 90^\circ \implies \cos\theta = 0", font_size=MIN_FONT, color=HIGHLIGHT)
        r2.next_to(f2, DOWN, buff=0.25, aligned_edge=LEFT)
        r2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        r2_sub = Tex(r"Orthogonal", font_size=MIN_FONT - 2, color=INK_DIM)
        r2_sub.next_to(r2, DOWN, buff=0.15, aligned_edge=LEFT)
        r2_sub.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(w_arr, w2_arr),
            Transform(l_w, l_w2),
            Create(elbow),
            FadeOut(r1),
            FadeOut(r1_sub),
            FadeIn(r2),
            FadeIn(r2_sub),
            run_time=1.8,
        )
        self.wait(1.5)

        # 5. Beat 3: w swings to 180 degrees (cos theta = -1)
        w3_coords = np.array([-2.0, 0.0, 0.0])
        w3_arr = Arrow(
            ORIGIN,
            w3_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w3 = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w3.next_to(w3_coords, DOWN, buff=0.20)
        l_w3.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        semi_arc = Arc(radius=0.5, start_angle=0, angle=PI, color=Y_COLOR, stroke_width=3.5)

        r3 = MathTex(r"\theta = 180^\circ \implies \cos\theta = -1", font_size=MIN_FONT, color=Y_COLOR)
        r3.next_to(f2, DOWN, buff=0.25, aligned_edge=LEFT)
        r3.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        r3_sub = Tex(r"Opposite direction", font_size=MIN_FONT - 4, color=INK_DIM)
        r3_sub.next_to(r3, DOWN, buff=0.12, aligned_edge=LEFT)
        r3_sub.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(w_arr, w3_arr),
            Transform(l_w, l_w3),
            FadeOut(elbow),
            Create(semi_arc),
            FadeOut(r2),
            FadeOut(r2_sub),
            FadeIn(r3),
            FadeIn(r3_sub),
            run_time=1.8,
        )
        self.wait(2.5)


class CosineScaleInvariant(Scene):
    r"""w stretched to 3w; the dot product triples, cos \theta stays fixed.

    Then two "documents" as word-count vectors point the same way: cosine 1 despite different lengths.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Given v = [2.0, 0.0], w = [0.8, 0.6]
        # ||v|| = 2, ||w|| = 1.0, v . w = 1.6, cos theta = 0.8
        v_coords = np.array([2.0, 0.0, 0.0])
        w_coords = np.array([0.8, 0.6, 0.0])

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
        l_w.next_to(w_coords, UP, buff=0.15)
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        theta_val = np.arctan2(0.6, 0.8)
        arc = Arc(radius=0.5, start_angle=0, angle=theta_val, color=HIGHLIGHT, stroke_width=3)

        f_cos = MathTex(
            r"\cos\theta = \frac{\vec{v} \cdot \vec{w}}{\|\vec{v}\| \|\vec{w}\|}",
            font_size=MIN_FONT,
        )
        f_cos.to_corner(UL, buff=0.35)
        f_cos.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        val1 = MathTex(r"\vec{v} \cdot \vec{w} = 1.6 \implies \cos\theta = 0.8", font_size=MIN_FONT - 4, color=RESULT_COLOR)
        val1.next_to(f_cos, DOWN, buff=0.20, aligned_edge=LEFT)
        val1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w, arc, formulas
        self.add(v_arr, l_v, w_arr, l_w, arc, f_cos, val1)
        self.wait(1.5)

        # 2. Stretch w to 3w = [2.4, 1.8]
        w3_coords = np.array([2.4, 1.8, 0.0])
        w3_arr = Arrow(
            ORIGIN,
            w3_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w3 = MathTex(r"3\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        l_w3.next_to(w3_coords, UR, buff=0.15)
        l_w3.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        val2_1 = MathTex(
            r"\vec{v} \cdot (3\vec{w}) = 3(1.6) = 4.8",
            font_size=MIN_FONT - 4,
            color=RESULT_COLOR,
        )
        val2_1.next_to(f_cos, DOWN, buff=0.20, aligned_edge=LEFT)
        val2_1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        val2_2 = MathTex(
            r"\cos\theta = \frac{4.8}{2 \cdot 3} = 0.8",
            font_size=MIN_FONT - 4,
            color=RESULT_COLOR,
        )
        val2_2.next_to(val2_1, DOWN, buff=0.14, aligned_edge=LEFT)
        val2_2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        tag_scale = Tex(
            r"Lengths cancel\\$\implies \cos\theta$ invariant",
            font_size=MIN_FONT - 4,
            color=INK,
        )
        tag_scale.next_to(val2_2, DOWN, buff=0.18, aligned_edge=LEFT)
        tag_scale.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            Transform(w_arr, w3_arr),
            Transform(l_w, l_w3),
            FadeOut(val1),
            FadeIn(val2_1),
            FadeIn(val2_2),
            FadeIn(tag_scale),
            run_time=2.0,
        )
        self.wait(1.5)

        # 3. Beat 2: Document vectors
        self.play(
            FadeOut(v_arr),
            FadeOut(l_v),
            FadeOut(w_arr),
            FadeOut(l_w),
            FadeOut(arc),
            FadeOut(f_cos),
            FadeOut(val2_1),
            FadeOut(val2_2),
            FadeOut(tag_scale),
            run_time=0.8,
        )

        d1_coords = np.array([1.2, 0.9, 0.0])
        d2_coords = np.array([2.8, 2.1, 0.0])

        d1_arr = Arrow(
            ORIGIN,
            d1_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_d1 = Tex(r"Short article", font_size=MIN_FONT - 4, color=V_COLOR)
        l_d1.next_to(d1_coords, DR, buff=0.18)
        l_d1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        d2_arr = Arrow(
            ORIGIN,
            d2_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_d2 = Tex(r"Long article", font_size=MIN_FONT - 4, color=W_COLOR)
        l_d2.next_to(d2_coords, UR, buff=0.15)
        l_d2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        doc_title = Tex(r"Word count vectors:", font_size=MIN_FONT, color=INK_DIM)
        doc_title.to_corner(UL, buff=0.35)
        doc_title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        doc_sim = MathTex(r"\cos\theta = 1.0", font_size=MIN_FONT + 4, color=RESULT_COLOR)
        doc_sim.next_to(doc_title, DOWN, buff=0.22, aligned_edge=LEFT)
        doc_sim.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        doc_sub = Tex(r"Same topic, different length", font_size=MIN_FONT - 4, color=INK)
        doc_sub.next_to(doc_sim, DOWN, buff=0.18, aligned_edge=LEFT)
        doc_sub.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            GrowArrow(d1_arr),
            Write(l_d1),
            GrowArrow(d2_arr),
            Write(l_d2),
            Write(doc_title),
            Write(doc_sim),
            Write(doc_sub),
            run_time=2.0,
        )
        self.wait(2.5)
