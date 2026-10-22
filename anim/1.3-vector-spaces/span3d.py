# Block 1.3, authored in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


class Span3D(ThreeDScene):
    def construct(self):
        # Set 3D camera orientation before adding objects so frame 1 is correct
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)

        # 3D Axes scaled to fill frame comfortably
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2.5, 2.5, 1],
            x_length=7.5,
            y_length=7.5,
            z_length=4.5,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 2},
        )
        self.add(axes)

        # Vectors v and w in 3D (length ~2.6-2.8)
        v_coords = np.array([2.6, 0.8, -0.6])
        w_coords = np.array([-0.3, 2.5, 0.7])

        v_arrow = Arrow3D(
            start=ORIGIN,
            end=v_coords,
            thickness=0.04,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=V_COLOR,
        )
        w_arrow = Arrow3D(
            start=ORIGIN,
            end=w_coords,
            thickness=0.04,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=W_COLOR,
        )

        # Fixed in frame UI text
        title = Tex(r"Span of two vectors in 3D", font_size=MIN_FONT, color=INK)
        title.to_corner(UL, buff=0.4)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        v_legend = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        w_legend = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        legend = VGroup(v_legend, w_legend).arrange(RIGHT, buff=0.35)
        legend.next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)
        legend.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.add_fixed_in_frame_mobjects(title, legend)

        # Frame 1 givens
        self.add(v_arrow, w_arrow)
        self.wait(1.2)

        # Start slow ambient rotation so the plane stays face-on
        self.begin_ambient_camera_rotation(rate=0.05)

        # The span: a semi-transparent plane through the origin
        # Defined by span of v and w
        s = 0.88
        p1 = -s * v_coords - s * w_coords
        p2 = s * v_coords - s * w_coords
        p3 = s * v_coords + s * w_coords
        p4 = -s * v_coords + s * w_coords

        span_polygon = Polygon(
            p1,
            p2,
            p3,
            p4,
            fill_color=RESULT_COLOR,
            fill_opacity=0.35,
            stroke_color=RESULT_COLOR,
            stroke_width=2.5,
        )

        desc = Tex(
            r"$\text{Span}(\vec{v}, \vec{w}) =$ plane through origin",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        desc.to_edge(DOWN, buff=0.35)
        desc.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.add_fixed_in_frame_mobjects(desc)

        self.play(
            FadeIn(span_polygon),
            FadeIn(desc, shift=0.1 * DOWN),
            run_time=2.0,
        )
        self.wait(4.5)

        self.stop_ambient_camera_rotation()
        self.wait(1.2)


class ThirdVector3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2.5, 2.5, 1],
            x_length=7.5,
            y_length=7.5,
            z_length=4.5,
            axis_config={"stroke_color": INK_DIM, "stroke_width": 2},
        )
        self.add(axes)

        # Vectors v and w in 3D matching Span3D
        v_coords = np.array([2.6, 0.8, -0.6])
        w_coords = np.array([-0.3, 2.5, 0.7])

        v_arrow = Arrow3D(
            start=ORIGIN,
            end=v_coords,
            thickness=0.04,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=V_COLOR,
        )
        w_arrow = Arrow3D(
            start=ORIGIN,
            end=w_coords,
            thickness=0.04,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=W_COLOR,
        )

        # Semi-transparent plane for span(v, w)
        s = 0.88
        p1 = -s * v_coords - s * w_coords
        p2 = s * v_coords - s * w_coords
        p3 = s * v_coords + s * w_coords
        p4 = -s * v_coords + s * w_coords

        span_plane = Polygon(
            p1,
            p2,
            p3,
            p4,
            fill_color=RESULT_COLOR,
            fill_opacity=0.35,
            stroke_color=RESULT_COLOR,
            stroke_width=2.0,
        )

        # Fixed in frame UI
        title = Tex(r"Adding a third vector $\vec{u}$", font_size=MIN_FONT, color=INK)
        title.to_corner(UL, buff=0.4)
        title.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        v_legend = MathTex(r"\vec{v}", font_size=MIN_FONT, color=V_COLOR)
        w_legend = MathTex(r"\vec{w}", font_size=MIN_FONT, color=W_COLOR)
        u_legend = MathTex(r"\vec{u}", font_size=MIN_FONT, color=HIGHLIGHT)
        legend = VGroup(v_legend, w_legend, u_legend).arrange(RIGHT, buff=0.35)
        legend.next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)
        legend.add_background_rectangle(color=BG, opacity=0.9, buff=0.08)

        self.add_fixed_in_frame_mobjects(title, legend)

        # Frame 1 givens: axes, v, w, and their span plane
        self.add(v_arrow, w_arrow, span_plane)
        self.wait(1.2)

        self.begin_ambient_camera_rotation(rate=0.05)

        # Case 1: u is on the plane (coplanar)
        u_on_coords = 0.5 * v_coords + 0.45 * w_coords
        u_arrow = Arrow3D(
            start=ORIGIN,
            end=u_on_coords,
            thickness=0.045,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=HIGHLIGHT,
        )

        case1_text = Tex(
            r"$\vec{u}$ on the plane: span unchanged",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        case1_text.to_edge(DOWN, buff=0.35)
        case1_text.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
        self.add_fixed_in_frame_mobjects(case1_text)

        self.play(
            FadeIn(u_arrow),
            FadeIn(case1_text, shift=0.1 * DOWN),
            run_time=1.8,
        )
        self.wait(3.0)

        # Case 2: u moves off the plane (points up into 3D)
        u_off_coords = np.array([0.2, 0.4, 2.1])
        u_off_arrow = Arrow3D(
            start=ORIGIN,
            end=u_off_coords,
            thickness=0.045,
            height=0.28,
            base_radius=0.09,
            resolution=8,
            color=HIGHLIGHT,
        )

        case2_text = Tex(
            r"$\vec{u}$ off the plane: span is all of $\mathbb{R}^3$",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        )
        case2_text.to_edge(DOWN, buff=0.35)
        case2_text.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)

        self.play(
            Transform(u_arrow, u_off_arrow),
            FadeOut(case1_text),
            FadeIn(case2_text, shift=0.1 * DOWN),
            run_time=2.0,
        )
        self.add_fixed_in_frame_mobjects(case2_text)
        self.wait(3.5)

        self.stop_ambient_camera_rotation()
        self.wait(1.0)
