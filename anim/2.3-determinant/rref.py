"""Block 2.3 callback to the Day 1 RREF: what row reduction does geometrically.

Row operations multiply on the left, so they warp the output space and leave
the null space alone. The Day 1 matrix [v w u] with u = v + w is used throughout.
"""

from shared.anim.house import *
from shared.anim.linmap import *

M0 = np.array([[1.0, 2.0, 3.0], [2.0, 1.0, 3.0], [1.0, 0.0, 1.0]])
REF = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
RREF = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
NULL = np.array([1.0, 1.0, -1.0])
COLS = (V_COLOR, W_COLOR, RESULT_COLOR)
PHI, THETA = 68 * DEGREES, -55 * DEGREES


def mat3(M):
    return matrix_tex([[int(e) for e in row] for row in M], col_colors=COLS)


def tag(tex, color=INK):
    return MathTex(tex, font_size=MIN_FONT, color=color)


def axes3(half, length):
    return ThreeDAxes(x_range=[-half, half, 1], y_range=[-half, half, 1], z_range=[-half, half, 1],
                      x_length=length, y_length=length, z_length=length,
                      axis_config={"stroke_color": INK_DIM, "stroke_width": 2,
                                   "include_ticks": False, "include_tip": False})


S = 0.7  # scene length of one unit in the single-panel scenes
O = np.array([0.0, 0.0, 0.3]) + 1.1 * np.array([-np.sin(THETA), np.cos(THETA), 0.0])


def P(vec):
    return O + S * np.asarray(vec, dtype=float)


def stage(scene):
    """Camera, floor, axes and axis letters shared by RrefOriginal and RrefWarp."""
    scene.set_camera_orientation(phi=PHI, theta=THETA)
    axes = axes3(3.4, 2 * 3.4 * S).shift(O)
    floor = Square(side_length=2 * 3.2 * S, stroke_width=0, fill_color=GRID,
                   fill_opacity=0.35).shift(O)
    ends = VGroup(tag("x", INK_DIM).move_to(P([3.8, -0.3, 0])), tag("y", INK_DIM).move_to(P([-0.9, 3.4, 0])),
                  tag("z", INK_DIM).move_to(P([0, 0, 3.2])))
    scene.add_fixed_orientation_mobjects(*ends)
    scene.add(floor, axes)
    return VGroup(floor, axes), ends


def columns(C, patch=True):
    """The columns of C as coloured arrows from the origin, with the v, u, w parallelogram shaded."""
    v, w, u = C[:, 0], C[:, 1], C[:, 2]
    arrows = [Line(P(0 * v), P(c), color=col, stroke_width=7) for c, col in zip((v, w, u), COLS)]
    tips = [Dot3D(P(c), radius=0.07, color=col) for c, col in zip((v, w, u), COLS)]
    group = VGroup(*arrows, *tips)
    if patch:
        group.add_to_back(Polygon(P(0 * v), P(v), P(u), P(w), stroke_width=0,
                                  fill_color=RESULT_COLOR, fill_opacity=0.18))
    return group


class RrefOriginal(ThreeDScene):
    """What A does: i, j, k go to v, w, u, space flattens onto their plane, the null line goes to 0."""

    def construct(self):
        world, ends = stage(self)
        assert np.allclose(M0 @ NULL, 0)
        t = ValueTracker(0.0)
        spin = ValueTracker(0.0)  # turn of the whole scene about the vertical axis through O

        def turned(mob):
            return mob.rotate(spin.get_value(), axis=OUT, about_point=O)

        def cur():
            a = t.get_value()
            return (1 - a) * np.eye(3) + a * M0

        def cube():
            C = cur()
            h = 0.5
            corners = {(x, y, z): P(C @ np.array([x, y, z])) for x in (-h, h) for y in (-h, h) for z in (-h, h)}
            quads = [[(x, -h, -h), (x, h, -h), (x, h, h), (x, -h, h)] for x in (-h, h)]
            quads += [[(-h, y, -h), (h, y, -h), (h, y, h), (-h, y, h)] for y in (-h, h)]
            quads += [[(-h, -h, z), (h, -h, z), (h, h, z), (-h, h, z)] for z in (-h, h)]
            col = interpolate_color(ManimColor(V_COLOR), ManimColor(RESULT_COLOR), t.get_value())
            return VGroup(*[Polygon(*[corners[q] for q in quad], color=col, stroke_width=2,
                                    fill_color=col, fill_opacity=0.12) for quad in quads])

        def null_line():
            a, b = P(cur() @ (-1.1 * NULL)), P(cur() @ (1.1 * NULL))
            if np.linalg.norm(b - a) < 1e-3:
                return Dot3D(P([0, 0, 0]), radius=0.09, color=HIGHLIGHT)
            return Line(a, b, color=HIGHLIGHT, stroke_width=7)

        ghost = DashedLine(P(-1.1 * NULL), P(1.1 * NULL), color=HIGHLIGHT, stroke_width=5,
                           dash_length=0.12).set_opacity(0.0)
        body = always_redraw(lambda: turned(cube()))
        arrows = always_redraw(lambda: turned(columns(cur(), patch=False)))
        line = always_redraw(lambda: turned(null_line()))

        mat = label_box(mat3(M0).to_corner(UL, buff=0.25))
        self.add_fixed_in_frame_mobjects(mat)
        self.add(body, ghost, line, arrows)
        self.wait(2.0)

        notes = VGroup(tag(r"\hat\imath,\hat\jmath,\hat k\ \to\ \vec v,\vec w,\vec u"),
                       tag(r"\text{space}\ \to\ \text{plane of }\vec v,\vec w", RESULT_COLOR),
                       tag(r"\text{line along }(1,1,-1)\ \to\ \mathbf 0", HIGHLIGHT))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        for n in notes:
            label_box(n)
        self.add_fixed_in_frame_mobjects(*notes)
        self.remove(*notes)

        self.play(FadeIn(notes[0]), run_time=0.8)
        self.play(t.animate.set_value(1.0), ghost.animate.set_opacity(0.8), run_time=5.0)
        self.wait(1.0)
        for n in notes[1:]:
            self.play(FadeIn(n), run_time=0.8)
            self.wait(2.0)
        # one full turn: the plane goes edge-on twice, and the clip ends where RrefWarp starts
        for e in ends:
            home = e.get_center() - O
            e.add_updater(lambda m, h=home: m.move_to(O + rotate_vector(h, spin.get_value(), OUT)))
        self.play(spin.animate.set_value(TAU), Rotate(VGroup(world, ghost), TAU, axis=OUT, about_point=O),
                  run_time=12, rate_func=linear)
        self.wait(1.5)


class RrefWarp(ThreeDScene):
    """Each row operation warps space; the columns' plane lands on the floor (REF), then on the axes (RREF)."""

    def construct(self):
        stage(self)
        E1 = np.array([[1, 0, 0], [-2, 1, 0], [-1, 0, 1]], dtype=float)
        M1 = E1 @ M0
        E2 = np.array([[1, 0, 0], [0, -1 / 3, 0], [0, -2 / 3, 1]], dtype=float)
        E3 = np.array([[1, -2, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
        assert np.allclose(E2 @ M1, REF) and np.allclose(E3 @ REF, RREF)
        assert np.allclose(M0 @ NULL, 0)

        t = ValueTracker(0.0)
        state = {"from": M0, "to": M0}

        def cur():
            a = t.get_value()
            return (1 - a) * state["from"] + a * state["to"]

        obj = always_redraw(lambda: columns(cur()))

        mat = label_box(mat3(M0).to_corner(UL, buff=0.25))
        self.add_fixed_in_frame_mobjects(mat)
        self.add(obj)
        self.wait(2.5)

        steps = [
            (E1, r"R_2-2R_1,\ R_3-R_1", None),
            (E2, r"-\tfrac13 R_2,\ R_3+2R_2", r"\text{REF: the plane lies flat}"),
            (E3, r"R_1-2R_2", r"\text{RREF: pivot columns on the axes}"),
        ]
        for E, op_tex, result_tex in steps:
            op = label_box(tag(op_tex, HIGHLIGHT).to_corner(UR, buff=0.3))
            self.add_fixed_in_frame_mobjects(op)
            self.remove(op)
            self.play(FadeIn(op), run_time=0.8)
            state["from"], state["to"] = cur(), E @ cur()
            t.set_value(0.0)
            new_mat = label_box(mat3(state["to"]).to_corner(UL, buff=0.25))
            self.add_fixed_in_frame_mobjects(new_mat)
            self.remove(new_mat)
            self.play(t.animate.set_value(1.0), FadeOut(mat), FadeIn(new_mat), run_time=3.0)
            mat = new_mat
            self.wait(0.6)
            if result_tex is None:
                self.play(FadeOut(op), run_time=0.6)
                continue
            res = label_box(tag(result_tex, RESULT_COLOR).to_corner(DR, buff=0.3))
            self.add_fixed_in_frame_mobjects(res)
            self.remove(res)
            self.play(FadeOut(op), FadeIn(res), run_time=0.8)
            self.wait(2.5)
            self.play(FadeOut(res), run_time=0.6)

        rel = label_box(tag(r"\vec u=\vec v+\vec w\ \text{at every step}", RESULT_COLOR)
                        .to_corner(DR, buff=0.3))
        self.add_fixed_in_frame_mobjects(rel)
        self.remove(rel)
        self.play(FadeIn(rel), run_time=0.8)
        self.wait(3.0)


class RrefCompare(ThreeDScene):
    """A, REF and RREF as maps: the same null line collapses, the image plane moves onto the axes."""

    def construct(self):
        self.set_camera_orientation(phi=PHI, theta=THETA)
        right = np.array([-np.sin(THETA), np.cos(THETA), 0.0])
        up = np.array([-np.cos(PHI) * np.cos(THETA), -np.cos(PHI) * np.sin(THETA), np.sin(PHI)])
        k = 0.34
        gap = 3.3
        names = ("A", r"\text{REF}", r"\text{RREF}")
        mats = (M0, REF, RREF)
        for M in mats:
            assert np.allclose(M @ NULL, 0)

        cubes, lines, panels = [], [], []
        for i, M in enumerate(mats):
            c = (i - 1) * gap * right - 0.55 * up
            axes = axes3(1.6, 2.6).shift(c)
            floor = Square(side_length=2.4, stroke_width=0, fill_color=GRID, fill_opacity=0.35).shift(c)
            cube = faces_of_centered_cube(k, V_COLOR).shift(c)
            ln = Line(c - 0.9 * k * NULL, c + 0.9 * k * NULL, color=HIGHLIGHT, stroke_width=7)
            ghost = DashedLine(c - 0.9 * k * NULL, c + 0.9 * k * NULL, color=HIGHLIGHT,
                               stroke_width=5, dash_length=0.1).set_opacity(0.0)
            cubes.append(cube)
            lines.append((ln, ghost, c))
            panels.append(VGroup(floor, axes, ghost, cube, ln))

        labels = VGroup()
        for i, (M, nm) in enumerate(zip(mats, names)):
            x = (i - 1) * gap
            m = mat3(M).scale(0.92).move_to([x, 1.75, 0])
            n = tag(nm).move_to([x, -2.45, 0])
            labels.add(label_box(m), label_box(n))
        self.add_fixed_in_frame_mobjects(labels)
        for p in panels:
            self.add(p)
        self.wait(2.5)

        anims = []
        for M, cube, (ln, ghost, c) in zip(mats, cubes, lines):
            anims += [ApplyMatrix(M, cube, about_point=c), ApplyMatrix(M, ln, about_point=c),
                      ghost.animate.set_opacity(0.9)]
        self.play(*anims, run_time=5)
        self.play(*[cb.animate.set_color(RESULT_COLOR) for cb in cubes], run_time=1.0)
        self.wait(4.0)


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
