"""Block 2.2: the determinant in 3D is a volume factor.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.6 (the determinant).
"""

from shared.anim.house import *
from shared.anim.linmap import *

S = 0.8  # scene length of one unit
O = np.array([0.0, 0.0, -1.5])  # where the origin sits in the scene


def unit_cube():
    """The unit cube [0,1]^3 (scaled by S) as six translucent faces."""
    v = lambda x, y, z: O + S * np.array([x, y, z], dtype=float)
    quads = [
        [v(0, 0, 0), v(1, 0, 0), v(1, 1, 0), v(0, 1, 0)],
        [v(0, 0, 1), v(1, 0, 1), v(1, 1, 1), v(0, 1, 1)],
        [v(0, 0, 0), v(1, 0, 0), v(1, 0, 1), v(0, 0, 1)],
        [v(0, 1, 0), v(1, 1, 0), v(1, 1, 1), v(0, 1, 1)],
        [v(0, 0, 0), v(0, 1, 0), v(0, 1, 1), v(0, 0, 1)],
        [v(1, 0, 0), v(1, 1, 0), v(1, 1, 1), v(1, 0, 1)],
    ]
    return VGroup(*[Polygon(*q, color=RESULT_COLOR, stroke_width=3,
                            fill_color=RESULT_COLOR, fill_opacity=0.3) for q in quads])


def mat3(rows):
    m = matrix_tex(rows, col_colors=(X_COLOR, Y_COLOR))
    return m


class Det3D(ThreeDScene):
    """The cube becomes a parallelepiped of volume det A = 6, then a flat sheet of volume 0."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        axes = ThreeDAxes(x_range=[-0.5, 3, 1], y_range=[-0.5, 2.5, 1], z_range=[0, 3.5, 1],
                          x_length=3.5 * S, y_length=3 * S, z_length=3.5 * S,
                          axis_config={"stroke_color": INK_DIM, "stroke_width": 2,
                                       "include_ticks": False, "include_tip": False})
        axes.shift(O - axes.c2p(0, 0, 0))
        cube = unit_cube()

        M1 = np.array([[2.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 3.0]])
        M2 = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]])
        rows1 = [[2, 1, 0], [0, 1, 0], [0, 0, 3]]
        rows2 = [[1, 0, 1], [0, 1, 1], [1, 1, 2]]

        mat1 = label_box(mat3(rows1).to_corner(UL, buff=0.25))
        vol1 = label_box(MathTex(r"\text{volume}=\det A=6", font_size=MIN_FONT, color=RESULT_COLOR)
                         .to_corner(DR, buff=0.25))
        mat2 = label_box(mat3(rows2).to_corner(UL, buff=0.25))
        vol2 = label_box(MathTex(r"\text{volume}=\det A=0", font_size=MIN_FONT, color=RESULT_COLOR)
                         .to_corner(DR, buff=0.25))
        flat = label_box(MathTex(r"\text{flat: a plane}", font_size=MIN_FONT, color=INK)
                         .to_corner(DL, buff=0.25))
        self.add_fixed_in_frame_mobjects(mat1, mat2, vol1, vol2, flat)
        self.remove(mat2, vol1, vol2, flat)

        self.add(axes, cube)
        self.wait(1.2)

        self.play(ApplyMatrix(M1, cube, about_point=O), run_time=3)
        self.add(vol1)
        self.wait(1.8)

        self.play(FadeOut(vol1), FadeOut(mat1), Transform(cube, unit_cube()), run_time=1.5)
        self.add(mat2)
        self.wait(0.6)
        self.play(ApplyMatrix(M2, cube, about_point=O), run_time=3)
        self.add(vol2, flat)
        self.wait(1.8)
