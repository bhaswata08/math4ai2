# Block 1.2 scenes, authored for this course in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class NormPythagoras(Scene):
    """v = [3, 2] on the plane, legs 3 (X_COLOR) and 2 (Y_COLOR), right angle mark,

    ||v|| = sqrt(3^2 + 2^2) = sqrt(13) ~ 3.61; then the same rule written for n entries.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        v_coords = np.array([3.0, 2.0, 0.0])

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.move_to(np.array([1.25, 1.45, 0.0]))
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows the givens: plane, vector v
        self.add(v_arr, l_v)
        self.wait(1.5)

        # 2. Draw horizontal leg (3, X_COLOR) and vertical leg (2, Y_COLOR)
        x_leg = Line(ORIGIN, np.array([3.0, 0.0, 0.0]), stroke_width=5, color=X_COLOR)
        l_x = MathTex(r"3", font_size=MIN_FONT, color=X_COLOR)
        l_x.next_to(np.array([1.5, 0.0, 0.0]), DOWN, buff=0.2)
        l_x.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        y_leg = Line(np.array([3.0, 0.0, 0.0]), v_coords, stroke_width=5, color=Y_COLOR)
        l_y = MathTex(r"2", font_size=MIN_FONT, color=Y_COLOR)
        l_y.next_to(np.array([3.0, 1.0, 0.0]), RIGHT, buff=0.2)
        l_y.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        ra_h = Line(np.array([2.75, 0.0, 0.0]), np.array([2.75, 0.25, 0.0]), stroke_width=2.5, color=INK_DIM)
        ra_v = Line(np.array([2.75, 0.25, 0.0]), np.array([3.0, 0.25, 0.0]), stroke_width=2.5, color=INK_DIM)
        right_angle = VGroup(ra_h, ra_v)

        self.play(Create(x_leg), Write(l_x), run_time=1.0)
        self.play(Create(y_leg), Write(l_y), run_time=1.0)
        self.play(Create(right_angle), run_time=0.6)
        self.wait(0.6)

        # 3. Pythagorean formula
        step1 = MathTex(
            r"\|\vec{v}\|",
            r"=",
            r"\sqrt{",
            r"3",
            r"^2 + ",
            r"2",
            r"^2}",
            font_size=MIN_FONT,
        )
        step1[0].set_color(RESULT_COLOR)
        step1[1].set_color(INK)
        step1[2].set_color(INK)
        step1[3].set_color(X_COLOR)
        step1[4].set_color(INK)
        step1[5].set_color(Y_COLOR)
        step1[6].set_color(INK)
        step1.move_to(np.array([-2.9, 1.8, 0.0]))
        step1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(step1), run_time=1.4)
        self.wait(0.5)

        step2 = MathTex(
            r"= \sqrt{9 + 4} = \sqrt{13} \approx 3.61",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        step2.next_to(step1, DOWN, buff=0.22, aligned_edge=LEFT)
        step2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(step2), run_time=1.4)
        self.wait(1.0)

        # 4. Same rule in n dimensions
        gen_title = Tex(r"In $n$ dimensions:", font_size=MIN_FONT, color=INK_DIM)
        gen_title.next_to(step2, DOWN, buff=0.45, aligned_edge=LEFT)
        gen_title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        gen_rule = MathTex(
            r"\|\vec{v}\|_2 = \sqrt{\sum_{i=1}^n v_i^2}",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        gen_rule.next_to(gen_title, DOWN, buff=0.2, aligned_edge=LEFT)
        gen_rule.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(gen_title), run_time=0.8)
        self.play(Write(gen_rule), run_time=1.4)
        self.wait(2.5)


class NormManhattan(Scene):
    """From the origin to [3, 2] along grid streets (L1 = |3| + |2| = 5, RESULT_COLOR path)

    versus the straight line (L2 = sqrt(13) ~ 3.61, V_COLOR); then L_infty = max(|3|, |2|) = 3.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        v_coords = np.array([3.0, 2.0, 0.0])

        v_arr = Arrow(
            ORIGIN,
            v_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_v = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        l_v.next_to(v_arr.point_from_proportion(0.65), UL, buff=0.2)
        l_v.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        l2_box = MathTex(
            r"\|\vec{v}\|_2 = \sqrt{13} \approx 3.61",
            font_size=MIN_FONT,
            color=V_COLOR,
        )
        l2_box.move_to(np.array([-2.8, 1.8, 0.0]))
        l2_box.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, vector v, L2 baseline
        self.add(v_arr, l_v, l2_box)
        self.wait(1.5)

        # 2. Manhattan path along grid streets
        m_path_x = Line(ORIGIN, np.array([3.0, 0.0, 0.0]), stroke_width=6, color=RESULT_COLOR)
        m_path_y = Line(np.array([3.0, 0.0, 0.0]), v_coords, stroke_width=6, color=RESULT_COLOR)

        m_dot = Dot(ORIGIN, radius=0.12, color=HIGHLIGHT)

        l1_box = MathTex(
            r"\|\vec{v}\|_1 = 3 + 2 = 5",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        l1_box.next_to(l2_box, DOWN, buff=0.35, aligned_edge=LEFT)
        l1_box.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(FadeIn(m_dot), run_time=0.4)
        self.play(
            Create(m_path_x),
            m_dot.animate.move_to(np.array([3.0, 0.0, 0.0])),
            run_time=1.2,
        )
        self.play(
            Create(m_path_y),
            m_dot.animate.move_to(v_coords),
            Write(l1_box),
            run_time=1.2,
        )
        self.play(FadeOut(m_dot), run_time=0.4)
        self.wait(1.0)

        # 3. L_infty (max norm)
        linf_box = MathTex(
            r"\|\vec{v}\|_\infty = \max(3, 2) = 3",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        linf_box.next_to(l1_box, DOWN, buff=0.35, aligned_edge=LEFT)
        linf_box.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Highlight max component (horizontal 3)
        max_line = Line(ORIGIN, np.array([3.0, 0.0, 0.0]), stroke_width=8, color=HIGHLIGHT)

        self.play(Create(max_line), Write(linf_box), run_time=1.2)
        self.wait(1.0)

        # 4. Final comparison
        comp = MathTex(
            r"\|\vec{v}\|_\infty \le \|\vec{v}\|_2 \le \|\vec{v}\|_1 \quad (3 < 3.61 < 5)",
            font_size=MIN_FONT,
            color=INK,
        )
        comp.to_edge(DOWN, buff=0.35)
        comp.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(comp), run_time=1.2)
        self.wait(2.5)


class UnitBalls(Scene):
    """Every vector of length 1 under each norm, traced as tips:

    L2 circle, L1 diamond, L_infty square, morphing between them, each labelled with its formula.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Unit radius = 1.0 (touches grid intersections at (+-1, 0), (0, +-1), (+-1, +-1))
        # Initial: L2 unit circle
        circle = Circle(radius=1.0, color=V_COLOR, stroke_width=5)

        u_vec = Arrow(
            ORIGIN,
            np.array([1.0, 0.0, 0.0]),
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_u = MathTex(r"\vec{u}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_u.next_to(u_vec.get_end(), UR, buff=0.15)
        l_u.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title = Tex(r"Unit balls: $\{\vec{u} : \|\vec{u}\| = 1\}$", font_size=MIN_FONT, color=INK_DIM)
        title.to_edge(UP, buff=0.35)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        f_circle = MathTex(
            r"L_2:\; \sqrt{x^2 + y^2} = 1",
            font_size=MIN_FONT,
            color=V_COLOR,
        )
        f_circle.move_to(np.array([-2.8, 0.0, 0.0]))
        f_circle.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, L2 circle, initial vector u, title, formula
        self.add(plane, circle, u_vec, l_u, title, f_circle)
        self.wait(1.5)

        # 2. Vector tip sweeps around circle
        self.play(
            Rotate(u_vec, angle=PI / 2, about_point=ORIGIN),
            l_u.animate.move_to(np.array([0.3, 1.25, 0.0])),
            run_time=1.4,
        )
        self.wait(0.6)

        # 3. Morph to L1 diamond
        diamond = Polygon(
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([-1.0, 0.0, 0.0]),
            np.array([0.0, -1.0, 0.0]),
            color=X_COLOR,
            stroke_width=5,
        )
        f_diamond = MathTex(
            r"L_1:\; |x| + |y| = 1",
            font_size=MIN_FONT,
            color=X_COLOR,
        )
        f_diamond.move_to(np.array([-2.8, 0.0, 0.0]))
        f_diamond.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        u_vec_d = Arrow(
            ORIGIN,
            np.array([0.5, 0.5, 0.0]),
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        self.play(
            Transform(circle, diamond),
            Transform(u_vec, u_vec_d),
            l_u.animate.move_to(np.array([0.75, 0.75, 0.0])),
            FadeOut(f_circle),
            FadeIn(f_diamond),
            run_time=1.8,
        )
        self.wait(1.0)

        # 4. Morph to L_infty square
        square = Square(side_length=2.0, color=W_COLOR, stroke_width=5)
        f_square = MathTex(
            r"L_\infty:\; \max(|x|, |y|) = 1",
            font_size=MIN_FONT,
            color=W_COLOR,
        )
        f_square.move_to(np.array([-2.8, 0.0, 0.0]))
        f_square.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        u_vec_sq = Arrow(
            ORIGIN,
            np.array([1.0, 1.0, 0.0]),
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )

        self.play(
            Transform(circle, square),
            Transform(u_vec, u_vec_sq),
            l_u.animate.move_to(np.array([1.3, 1.25, 0.0])),
            FadeOut(f_diamond),
            FadeIn(f_square),
            run_time=1.8,
        )
        self.wait(1.0)

        # 5. Final resting state: show all three shapes nested with legend at right
        final_square = Square(side_length=2.0, color=W_COLOR, stroke_width=3.5)
        final_circle = Circle(radius=1.0, color=V_COLOR, stroke_width=3.5)
        final_diamond = Polygon(
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([-1.0, 0.0, 0.0]),
            np.array([0.0, -1.0, 0.0]),
            color=X_COLOR,
            stroke_width=3.5,
        )

        tag_l1 = MathTex(r"L_1\text{ diamond}", font_size=MIN_FONT - 4, color=X_COLOR)
        tag_l2 = MathTex(r"L_2\text{ circle}", font_size=MIN_FONT - 4, color=V_COLOR)
        tag_linf = MathTex(r"L_\infty\text{ square}", font_size=MIN_FONT - 4, color=W_COLOR)
        legend = VGroup(tag_linf, tag_l2, tag_l1).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend.move_to(np.array([2.9, 0.0, 0.0]))
        legend.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(
            FadeOut(circle),
            FadeOut(u_vec),
            FadeOut(l_u),
            FadeOut(f_square),
            Create(final_square),
            Create(final_circle),
            Create(final_diamond),
            FadeIn(legend),
            run_time=2.0,
        )
        self.wait(2.5)


class Normalize(Scene):
    r"""Five vectors of different lengths; each divided by its own length

    shrinks or stretches onto the unit circle; caption \hat{v} = v / ||v||.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Unit circle
        unit_circle = Circle(radius=1.0, stroke_color=INK_DIM, stroke_width=2.5)

        # Five vectors of different lengths, chosen so none point into upper-left caption area:
        # v1: long in Q1 (length ~2.6)
        # v2: long in shallow Q2 (length ~2.24, y stays below 0.5)
        # v3: long in Q3 (length ~2.28)
        # v4: long in Q4 (length ~2.28)
        # v5: SHORT in Q1 (length 0.5 < 1 -> stretches onto unit circle)
        raw_coords = [
            np.array([2.4, 1.0, 0.0]),
            np.array([-2.2, 0.4, 0.0]),
            np.array([-1.8, -1.4, 0.0]),
            np.array([1.4, -1.8, 0.0]),
            np.array([0.4, 0.3, 0.0]),
        ]

        arrows = []
        for c in raw_coords:
            arr = Arrow(
                ORIGIN,
                c,
                buff=0,
                stroke_width=5.5,
                max_tip_length_to_length_ratio=0.25,
                color=V_COLOR,
            )
            arrows.append(arr)

        caption = MathTex(
            r"\hat{\vec{v}} = \frac{\vec{v}}{\|\vec{v}\|}",
            font_size=MIN_FONT + 6,
            color=RESULT_COLOR,
        )
        caption.to_corner(UL, buff=0.45)
        caption.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, unit circle, 5 vectors in V_COLOR, caption
        self.add(unit_circle, *arrows, caption)
        self.wait(1.5)

        # 2. Normalize each vector onto the unit circle
        target_arrows = []
        for c in raw_coords:
            u_coords = c / np.linalg.norm(c)
            u_arr = Arrow(
                ORIGIN,
                u_coords,
                buff=0,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.25,
                color=RESULT_COLOR,
            )
            target_arrows.append(u_arr)

        unit_tag = MathTex(r"\|\hat{\vec{v}}\| = 1", font_size=MIN_FONT + 2, color=HIGHLIGHT)
        unit_tag.to_corner(UR, buff=0.45)
        unit_tag.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        anims = [Transform(arr, targ) for arr, targ in zip(arrows, target_arrows)]
        anims.append(Write(unit_tag))

        self.play(*anims, run_time=2.2)
        self.wait(0.8)

        # Highlight unit circle
        self.play(unit_circle.animate.set_stroke(color=HIGHLIGHT, width=3.5), run_time=0.8)
        self.play(unit_circle.animate.set_stroke(color=INK_DIM, width=2.5), run_time=0.8)
        self.wait(2.5)
