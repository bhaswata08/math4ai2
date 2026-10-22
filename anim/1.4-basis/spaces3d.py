# Block 1.4. Authored for this course, in the style of 3Blue1Brown's Essence of Linear Algebra.

import numpy as np

from shared.anim.house import *


def make_axes():
    return ThreeDAxes(
        x_range=[-4, 4, 1],
        y_range=[-4, 4, 1],
        z_range=[-2.5, 2.5, 1],
        x_length=7.5,
        y_length=7.5,
        z_length=4.5,
        axis_config={"stroke_color": INK_DIM, "stroke_width": 2},
    )


def arrow(end, color):
    return Arrow3D(
        start=ORIGIN,
        end=np.array(end, dtype=float),
        thickness=0.04,
        height=0.28,
        base_radius=0.09,
        resolution=8,
        color=color,
    )


def card(text, color=INK, corner=None, edge=None):
    t = Tex(text, font_size=MIN_FONT, color=color)
    if corner is not None:
        t.to_corner(corner, buff=0.4)
    if edge is not None:
        t.to_edge(edge, buff=0.35)
    t.add_background_rectangle(color=BG, opacity=0.9, buff=0.1)
    return t


def parallelogram(a, b, s, color, opacity=0.3):
    a, b = np.array(a, float), np.array(b, float)
    return Polygon(
        -s * a - s * b, s * a - s * b, s * a + s * b, -s * a + s * b,
        fill_color=color, fill_opacity=opacity,
        stroke_color=color, stroke_width=2.5,
    )


class DimensionCount(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)
        axes = make_axes()
        self.add(axes)

        v = np.array([2.2, 1.2, 0.9])
        w = np.array([-0.8, 2.2, 0.6])
        u = np.array([0.5, -0.6, 2.0])

        line = Line3D(-1.55 * v, 1.55 * v, color=V_COLOR, thickness=0.015)
        line.set_opacity(0.55)
        va, wa, ua = arrow(v, V_COLOR), arrow(w, W_COLOR), arrow(u, X_COLOR)

        title = card(r"A line through $\vec 0$", corner=UL)
        cap = card(r"dimension 1: one basis vector", color=V_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(title, cap)

        # Frame 1: axes, the line and its basis vector
        self.add(line, va)
        self.wait(1.0)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(2.5)

        # Beat 2: plane
        plane = parallelogram(v, w, 0.9, W_COLOR)
        title2 = card(r"A plane through $\vec 0$", corner=UL)
        cap2 = card(r"dimension 2: two basis vectors", color=W_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(title2, cap2)
        self.remove(title2, cap2)
        self.play(
            FadeOut(title), FadeOut(cap),
            FadeIn(plane), FadeIn(wa),
            FadeIn(title2), FadeIn(cap2),
            run_time=1.5,
        )
        self.wait(2.5)

        # Beat 3: all of space
        cube = Cube(side_length=3.1, fill_color=X_COLOR, fill_opacity=0.08,
                    stroke_color=X_COLOR, stroke_width=1)
        cube.set_z_index(-1)
        title3 = card(r"All of space", corner=UL)
        cap3 = card(r"dimension 3: three basis vectors", color=X_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(title3, cap3)
        self.remove(title3, cap3)
        self.play(
            FadeOut(title2), FadeOut(cap2),
            FadeIn(cube), FadeIn(ua),
            FadeIn(title3), FadeIn(cap3),
            run_time=1.5,
        )
        self.wait(2.5)

        # End caption
        cap4 = card(r"dimension = number of vectors in a basis", color=RESULT_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(cap4)
        self.remove(cap4)
        self.play(FadeOut(cap3), FadeIn(cap4), run_time=1.0)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()


class SubspaceIntersection3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)
        axes = make_axes()
        self.add(axes)

        s = 2.4
        e1, e2, e3 = np.eye(3)
        plane_z = parallelogram(e1, e2, s, V_COLOR, 0.28)   # z = 0
        plane_x = parallelogram(2.4 * e2, 1.45 * e3, 1.0, W_COLOR, 0.28)   # x = 0
        y_line = Line3D(np.array([0, -3.5, 0]), np.array([0, 3.5, 0]),
                        color=HIGHLIGHT, thickness=0.05)

        title = card(r"Two planes through $\vec 0$", corner=UL)
        lab_z = card(r"$z=0$", color=V_COLOR)
        lab_x = card(r"$x=0$", color=W_COLOR)
        VGroup(lab_z, lab_x).arrange(RIGHT, buff=0.4).next_to(title, DOWN, buff=0.2, aligned_edge=LEFT)
        cap = card(r"$z=0$: span$\{[1,0,0],[0,1,0]\}$", color=V_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(title, lab_z, lab_x, cap)
        self.remove(lab_x)

        # Frame 1: axes and first plane
        self.add(plane_z)
        self.wait(1.0)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(1.5)

        cap2 = card(r"$x=0$: span$\{[0,1,0],[0,0,1]\}$", color=W_COLOR, edge=DOWN)
        self.add_fixed_in_frame_mobjects(cap2)
        self.remove(cap2)
        self.play(FadeIn(plane_x), FadeIn(lab_x), FadeOut(cap), FadeIn(cap2), run_time=1.5)
        self.wait(2.0)

        cap3 = card(r"two planes through $\vec 0$ meet in a line through $\vec 0$",
                    color=HIGHLIGHT, edge=DOWN)
        self.add_fixed_in_frame_mobjects(cap3)
        self.remove(cap3)
        self.play(FadeIn(y_line), FadeOut(cap2), FadeIn(cap3), run_time=1.5)
        self.wait(3.0)

        # Optional: a line not in the plane meets it only at 0
        d = np.array([1.6, -1.0, 1.9])
        skew = Line3D(-d, d, color=RESULT_COLOR, thickness=0.03)
        cap4 = card(r"a line not in the plane meets it only at $\vec 0$",
                    color=RESULT_COLOR, edge=DOWN)
        title4 = card(r"A line and a plane through $\vec 0$", corner=UL)
        self.add_fixed_in_frame_mobjects(cap4, title4)
        self.remove(cap4, title4)
        self.play(FadeOut(plane_x), FadeOut(y_line), FadeOut(lab_x),
                  FadeIn(skew), FadeOut(cap3), FadeIn(cap4),
                  FadeOut(title), FadeIn(title4), run_time=1.5)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
