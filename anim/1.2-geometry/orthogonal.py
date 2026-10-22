# Block 1.2 scenes, authored for this course in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class OrthogonalTest(Scene):
    r"""v = [2, 1], w = [-1, 2]; v.w = -2 + 2 = 0; right-angle mark appears;

    then a pair that is not orthogonal for contrast.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Givens: v = [2, 1], w = [-1, 2]
        # v . w = 2*(-1) + 1*2 = -2 + 2 = 0 -> orthogonal!
        v_coords = np.array([2.0, 1.0, 0.0])
        w_coords = np.array([-1.0, 2.0, 0.0])

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
        l_w.move_to(np.array([-1.4, 2.0, 0.0]))
        l_w.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title = Tex(r"Orthogonality test:", font_size=MIN_FONT, color=INK_DIM)
        title.move_to(np.array([-2.7, -0.6, 0.0]))
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, v, w, labels, title
        self.add(v_arr, l_v, w_arr, l_w, title)
        self.wait(1.5)

        # 2. Compute dot product in quadrant 3 (wide open space)
        calc1 = MathTex(
            r"\vec{v} \cdot \vec{w} = -2 + 2 = 0",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        calc1.next_to(title, DOWN, buff=0.25, aligned_edge=LEFT)
        calc1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Right angle elbow at origin
        u_v = v_coords / np.linalg.norm(v_coords)
        u_w = w_coords / np.linalg.norm(w_coords)
        s = 0.35
        q1 = s * u_v
        q2 = s * u_v + s * u_w
        q3 = s * u_w
        elbow = VGroup(
            Line(q1, q2, stroke_width=2.5, color=HIGHLIGHT),
            Line(q2, q3, stroke_width=2.5, color=HIGHLIGHT),
        )

        tag1 = Tex(
            r"$\implies$ Orthogonal ($90^\circ$)",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        tag1.next_to(calc1, DOWN, buff=0.25, aligned_edge=LEFT)
        tag1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(calc1), Create(elbow), run_time=1.4)
        self.play(Write(tag1), run_time=1.0)
        self.wait(1.5)

        # 3. Contrast pair: w' = [1, 2]
        # v . w' = 2*1 + 1*2 = 4 != 0
        w_prime_coords = np.array([1.0, 2.0, 0.0])
        w_prime_arr = Arrow(
            ORIGIN,
            w_prime_coords,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_w_prime = MathTex(r"\vec{w}'", font_size=MIN_FONT, color=W_COLOR)
        l_w_prime.move_to(np.array([1.35, 2.0, 0.0]))
        l_w_prime.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        calc2 = MathTex(
            r"\vec{v} \cdot \vec{w}' = 2 + 2 = 4 \ne 0",
            font_size=MIN_FONT,
            color=Y_COLOR,
        )
        calc2.next_to(title, DOWN, buff=0.25, aligned_edge=LEFT)
        calc2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        tag2 = Tex(
            r"$\implies$ Not orthogonal",
            font_size=MIN_FONT,
            color=Y_COLOR,
        )
        tag2.next_to(calc2, DOWN, buff=0.25, aligned_edge=LEFT)
        tag2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        angle_v = np.arctan2(1, 2)
        angle_w_prime = np.arctan2(2, 1)
        arc_not = Arc(
            radius=0.7,
            start_angle=angle_v,
            angle=angle_w_prime - angle_v,
            color=Y_COLOR,
            stroke_width=3,
        )

        self.play(
            Transform(w_arr, w_prime_arr),
            Transform(l_w, l_w_prime),
            FadeOut(elbow),
            Create(arc_not),
            FadeOut(calc1),
            FadeOut(tag1),
            FadeIn(calc2),
            FadeIn(tag2),
            run_time=2.0,
        )
        self.wait(2.5)


class OrthonormalCoordinates(Scene):
    r"""A rotated orthonormal pair u1, u2 (unit length, 90 deg apart);

    a vector x; its coordinates in that basis are just the two dot products
    x.u1 and x.u2, shown as projections.
    """

    def construct(self):
        plane = house_plane()
        self.add(plane)

        # Rotated orthonormal basis:
        # u1 = [0.8, 0.6]  (||u1|| = 1.0)
        # u2 = [-0.6, 0.8] (||u2|| = 1.0, u1 . u2 = 0)
        u1_coords = np.array([0.8, 0.6, 0.0])
        u2_coords = np.array([-0.6, 0.8, 0.0])

        # Vector x = 2*u1 + 1*u2 = [1.6 - 0.6, 1.2 + 0.8] = [1.0, 2.0]
        # x . u1 = 1.0*0.8 + 2.0*0.6 = 0.8 + 1.2 = 2.0
        # x . u2 = 1.0*(-0.6) + 2.0*0.8 = -0.6 + 1.6 = 1.0
        x_coords = np.array([1.0, 2.0, 0.0])

        u1_arr = Arrow(
            ORIGIN,
            u1_coords,
            buff=0,
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )
        l_u1 = MathTex(r"\vec{u}_1", font_size=MIN_FONT, color=V_COLOR)
        l_u1.next_to(u1_coords, DR, buff=0.15)
        l_u1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        u2_arr = Arrow(
            ORIGIN,
            u2_coords,
            buff=0,
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )
        l_u2 = MathTex(r"\vec{u}_2", font_size=MIN_FONT, color=W_COLOR)
        l_u2.next_to(u2_coords, LEFT, buff=0.18)
        l_u2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # Right angle elbow between u1 and u2 at origin
        s = 0.25
        p1 = s * u1_coords
        p2 = s * u1_coords + s * u2_coords
        p3 = s * u2_coords
        elbow = VGroup(
            Line(p1, p2, stroke_width=2.5, color=HIGHLIGHT),
            Line(p2, p3, stroke_width=2.5, color=HIGHLIGHT),
        )

        x_arr = Arrow(
            ORIGIN,
            x_coords,
            buff=0,
            stroke_width=6.5,
            max_tip_length_to_length_ratio=0.25,
            color=RESULT_COLOR,
        )
        l_x = MathTex(r"\vec{x}", font_size=MIN_FONT, color=RESULT_COLOR)
        l_x.next_to(x_coords, UR, buff=0.15)
        l_x.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        title = Tex(r"Orthonormal coordinates:", font_size=MIN_FONT - 2, color=INK_DIM)
        title.to_corner(UL, buff=0.35)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        basis_tag = Tex(r"$\{\vec{u}_1, \vec{u}_2\}$ orthonormal basis", font_size=MIN_FONT - 4, color=INK)
        basis_tag.next_to(title, DOWN, buff=0.14, aligned_edge=LEFT)
        basis_tag.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        # 1. Frame one shows givens: plane, u1, u2, x, elbow, labels, title
        self.add(u1_arr, l_u1, u2_arr, l_u2, elbow, x_arr, l_x, title, basis_tag)
        self.wait(1.5)

        # 2. Projection along u1: c1 = x . u1 = 2
        proj1_coords = 2.0 * u1_coords  # [1.6, 1.2, 0.0]
        drop1 = DashedLine(x_coords, proj1_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj1_arr = Arrow(
            ORIGIN,
            proj1_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=V_COLOR,
        )

        f_c1 = MathTex(
            r"c_1 = \vec{x} \cdot \vec{u}_1 = 2",
            font_size=MIN_FONT,
            color=V_COLOR,
        )
        f_c1.next_to(basis_tag, DOWN, buff=0.20, aligned_edge=LEFT)
        f_c1.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(drop1), GrowArrow(proj1_arr), Write(f_c1), run_time=1.6)
        self.wait(0.8)

        # 3. Projection along u2: c2 = x . u2 = 1
        proj2_coords = 1.0 * u2_coords  # [-0.6, 0.8, 0.0]
        drop2 = DashedLine(x_coords, proj2_coords, color=INK_DIM, stroke_width=3, dash_length=0.08)
        proj2_arr = Arrow(
            ORIGIN,
            proj2_coords,
            buff=0,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.25,
            color=W_COLOR,
        )

        f_c2 = MathTex(
            r"c_2 = \vec{x} \cdot \vec{u}_2 = 1",
            font_size=MIN_FONT,
            color=W_COLOR,
        )
        f_c2.next_to(f_c1, DOWN, buff=0.20, aligned_edge=LEFT)
        f_c2.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Create(drop2), GrowArrow(proj2_arr), Write(f_c2), run_time=1.6)
        self.wait(0.8)

        # 4. Reconstruction formula
        f_recon = MathTex(
            r"\vec{x} = c_1\vec{u}_1 + c_2\vec{u}_2",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        f_recon.next_to(f_c2, DOWN, buff=0.22, aligned_edge=LEFT)
        f_recon.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        f_num = MathTex(
            r"= 2\,\vec{u}_1 + 1\,\vec{u}_2",
            font_size=MIN_FONT + 2,
            color=RESULT_COLOR,
        )
        f_num.next_to(f_recon, DOWN, buff=0.18, aligned_edge=LEFT)
        f_num.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.play(Write(f_recon), run_time=1.4)
        self.play(Write(f_num), run_time=1.0)
        self.wait(2.5)
