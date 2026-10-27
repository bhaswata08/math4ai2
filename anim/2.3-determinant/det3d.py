"""Block 2.2: the determinant in 3D is a volume factor.

Idea from 3Blue1Brown, Essence of Linear Algebra ch.6 (the determinant).
"""

from shared.anim.house import *
from shared.anim.linmap import *

S = 0.9  # scene length of one unit
O = np.array([-0.3, 0.0, -1.9])  # where the origin sits in the scene


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
        # the plane the flat cube lies in: z = x + y
        corner = lambda x, y: O + S * np.array([x, y, M2[2] @ [x, y, 0]])
        sheet = Polygon(corner(-0.2, -0.2), corner(1.8, -0.2), corner(1.8, 1.8), corner(-0.2, 1.8),
                        color=V_COLOR, stroke_width=2, fill_color=V_COLOR, fill_opacity=0.12)
        self.play(FadeIn(sheet), run_time=1.0)
        self.wait(1.0)
        # edge-on: the plane seen from inside its own direction is a line
        self.move_camera(phi=88 * DEGREES, theta=-45 * DEGREES, run_time=3)
        self.wait(2.0)
        self.move_camera(phi=68 * DEGREES, theta=-55 * DEGREES, run_time=2.5)
        self.wait(3.0)


def faces_of_centered_cube(scale, color, opacity=0.25):
    v = lambda x, y, z: scale * np.array([x, y, z], dtype=float)
    h = 0.5
    quads = [
        [v(-h, -h, -h), v(h, -h, -h), v(h, h, -h), v(-h, h, -h)],
        [v(-h, -h, h), v(h, -h, h), v(h, h, h), v(-h, h, h)],
        [v(-h, -h, -h), v(h, -h, -h), v(h, -h, h), v(-h, -h, h)],
        [v(-h, h, -h), v(h, h, -h), v(h, h, h), v(-h, h, h)],
        [v(-h, -h, -h), v(-h, h, -h), v(-h, h, h), v(-h, -h, h)],
        [v(h, -h, -h), v(h, h, -h), v(h, h, h), v(h, -h, h)],
    ]
    return VGroup(*[Polygon(*q, color=color, stroke_width=3, fill_color=color, fill_opacity=opacity)
                    for q in quads])


class ThreeFlatteners(ThreeDScene):
    """The cube squashed onto a plane (rank 2), a line (rank 1) and a point (rank 0)."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        axes = ThreeDAxes(x_range=[-0.5, 3, 1], y_range=[-0.5, 2.5, 1], z_range=[0, 3.5, 1],
                          x_length=3.5 * S, y_length=3 * S, z_length=3.5 * S,
                          axis_config={"stroke_color": INK_DIM, "stroke_width": 2,
                                       "include_ticks": False, "include_tip": False})
        axes.shift(O - axes.c2p(0, 0, 0))
        cube = unit_cube()
        beats = [
            ([[1, 0, 0], [0, 1, 0], [0, 0, 0]], r"\text{a plane: rank }2"),
            ([[1, 0, 0], [0, 0, 0], [0, 0, 0]], r"\text{a line: rank }1"),
            ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], r"\text{a point: rank }0"),
        ]
        mats, labs = [], []
        for rows, txt in beats:
            m = label_box(mat3(rows).to_corner(UL, buff=0.25))
            t = label_box(MathTex(txt, font_size=MIN_FONT, color=RESULT_COLOR).to_corner(DR, buff=0.25))
            mats.append(m)
            labs.append(t)
        self.add_fixed_in_frame_mobjects(*mats, *labs)
        self.remove(*mats, *labs)
        self.add(axes, cube, mats[0])
        self.wait(2.0)
        for n, ((rows, _), m, t) in enumerate(zip(beats, mats, labs)):
            if n > 0:
                self.play(FadeOut(mats[n - 1]), FadeOut(labs[n - 1]), Transform(cube, unit_cube()), run_time=1.2)
                self.play(FadeIn(m), run_time=0.6)
                self.wait(0.8)
            M = np.array(rows, dtype=float)
            M = np.where(np.abs(M) < 1e-9, 0.0, M)
            if not M.any():
                M = 0.001 * np.eye(3)
            self.play(ApplyMatrix(M, cube, about_point=O), run_time=2.5)
            if n == 2:
                end = Dot3D(O, radius=0.09, color=RESULT_COLOR)
                self.play(FadeIn(end, scale=3), run_time=0.6)
            self.play(FadeIn(t), run_time=0.6)
            self.wait(2.5)


class NullSpaceCollapse(ThreeDScene):
    """A = [[1,0,1],[0,1,1],[1,1,2]]: the cube flattens to a plane and the null line collapses to 0."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES)
        A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 2.0]])
        v = np.array([1.0, 1.0, -1.0])
        assert np.allclose(A @ v, 0)
        k = 0.8
        axes = ThreeDAxes(x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1], z_range=[-1.5, 1.5, 1],
                          x_length=3.2, y_length=3.2, z_length=3.2,
                          axis_config={"stroke_color": INK_DIM, "stroke_width": 2,
                                       "include_ticks": False, "include_tip": False})
        cube = faces_of_centered_cube(k, V_COLOR)
        line = Line(-0.9 * k * v, 0.9 * k * v, color=HIGHLIGHT, stroke_width=7)
        ghost = DashedLine(-0.9 * k * v, 0.9 * k * v, color=HIGHLIGHT, stroke_width=4, dash_length=0.12)
        ghost.set_opacity(0.0)

        mat = label_box(mat3([[1, 0, 1], [0, 1, 1], [1, 1, 2]]).to_corner(UL, buff=0.25))
        rnk = int(np.linalg.matrix_rank(A))
        nul = 3 - rnk
        in_lbl = label_box(MathTex(r"\text{input: 3 dimensions}", font_size=MIN_FONT, color=INK)
                           .to_corner(UR, buff=0.25))
        img = label_box(MathTex(rf"\text{{image: a plane, rank }}{rnk}", font_size=MIN_FONT,
                                color=RESULT_COLOR).to_corner(DL, buff=0.25))
        nsp = label_box(MathTex(rf"\text{{null space: a line, dim }}{nul}", font_size=MIN_FONT,
                                color=HIGHLIGHT).next_to(img, UP, buff=0.15, aligned_edge=LEFT))
        img.to_corner(DR, buff=0.25)
        nsp.next_to(img, UP, buff=0.15, aligned_edge=RIGHT)
        eq = MathTex("3", "=", str(rnk), "+", str(nul), font_size=64, color=INK)
        eq[2].set_color(RESULT_COLOR)
        eq[4].set_color(HIGHLIGHT)
        eq.to_corner(UR, buff=0.3)
        label_box(eq)
        self.add_fixed_in_frame_mobjects(mat, in_lbl, img, nsp, eq)
        self.remove(img, nsp, eq)
        self.add(axes, ghost, cube, line)
        self.wait(2.5)
        self.play(ApplyMatrix(A, cube), ApplyMatrix(A, line), ghost.animate.set_opacity(0.6), run_time=5)
        self.play(cube.animate.set_color(RESULT_COLOR), run_time=1.0)
        self.play(FadeIn(img), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(nsp), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(in_lbl), FadeIn(eq), run_time=1.0)
        self.wait(3.0)
