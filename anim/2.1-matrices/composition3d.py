"""Block 2.1: two 3D turns in both orders, side by side, so AB != BA.

Authored for this course. It replaces the Visual Kernel segment
(SEE Matrix ch.1 part 2, 287-305 s), whose layout kept the old BA panel
and an empty x panel on screen. The turns match that footage: A turns
60 degrees about the x axis, B turns 45 degrees about the z axis.
"""

from shared.anim.house import *

SIDE = 1.5
LEFT_C = np.array([-2.5, 0.0, 0.0])
RIGHT_C = np.array([2.5, 0.0, 0.0])


def cube(center):
    """A cube with each pair of opposite faces in its own colour: x faces
    green, y faces rose, z faces violet. Each face is coloured by the axis
    its centre sits on, so the result does not depend on Manim's face order."""
    c = Cube(side_length=SIDE, fill_opacity=0.92, stroke_color=INK, stroke_width=2)
    for face in c:
        axis = int(np.argmax(np.abs(face.get_center())))
        face.set_fill((X_COLOR, Y_COLOR, W_COLOR)[axis], opacity=0.92)
    return c.shift(center)


def axis_line(center, direction, length=3.2):
    d = np.asarray(direction, dtype=float)
    return DashedLine(center - d * length / 2, center + d * length / 2,
                      color=INK_DIM, stroke_width=2, dash_length=0.12)


class TwoOrders3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=72 * DEGREES, theta=-70 * DEGREES,
                                    focal_distance=400)

        left, right = cube(LEFT_C), cube(RIGHT_C)
        axes = VGroup(*[axis_line(c, d) for c in (LEFT_C, RIGHT_C)
                        for d in (RIGHT, OUT)])

        def text(t, color=INK):
            return Tex(t, font_size=MIN_FONT, color=color)

        def maths(t, color=INK):
            return MathTex(t, font_size=MIN_FONT, color=color)

        l_head = text("$A$ first, then $B$").move_to([-2.5, 2.35, 0])
        r_head = text("$B$ first, then $A$").move_to([2.5, 2.35, 0])
        self.add_fixed_in_frame_mobjects(l_head, r_head)
        self.add(axes, left, right)
        self.wait(1.5)

        def step(label_l, label_r):
            ll = maths(label_l, RESULT_COLOR).move_to([-2.5, -2.3, 0])
            rl = maths(label_r, RESULT_COLOR).move_to([2.5, -2.3, 0])
            self.add_fixed_in_frame_mobjects(ll, rl)
            return ll, rl

        ll, rl = step(r"A:\ 60^\circ \text{ about } x", r"B:\ 45^\circ \text{ about } z")
        self.play(FadeIn(ll), FadeIn(rl), run_time=0.5)
        self.play(Rotate(left, 60 * DEGREES, axis=RIGHT, about_point=LEFT_C),
                  Rotate(right, 45 * DEGREES, axis=OUT, about_point=RIGHT_C),
                  run_time=2.2)
        self.wait(0.8)

        ll2, rl2 = step(r"B:\ 45^\circ \text{ about } z", r"A:\ 60^\circ \text{ about } x")
        self.remove(ll2, rl2)
        self.play(FadeOut(ll), FadeOut(rl), run_time=0.3)
        self.add_fixed_in_frame_mobjects(ll2, rl2)
        self.play(FadeIn(ll2), FadeIn(rl2), run_time=0.4)
        self.play(Rotate(left, 45 * DEGREES, axis=OUT, about_point=LEFT_C),
                  Rotate(right, 60 * DEGREES, axis=RIGHT, about_point=RIGHT_C),
                  run_time=2.2)
        self.wait(0.8)

        lr = maths("BA", RESULT_COLOR).move_to([-2.5, -2.3, 0])
        rr = maths("AB", RESULT_COLOR).move_to([2.5, -2.3, 0])
        neq = maths(r"AB \neq BA", HIGHLIGHT).move_to([0, -2.3, 0])
        self.play(FadeOut(ll2), FadeOut(rl2), run_time=0.3)
        self.add_fixed_in_frame_mobjects(lr, rr, neq)
        self.remove(lr, rr, neq)
        self.play(FadeIn(lr), FadeIn(rr), run_time=0.6)
        self.play(FadeIn(neq), run_time=0.8)
        self.wait(3)
