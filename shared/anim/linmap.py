"""Helpers for the Day 2 matrix clips: a 2x2 matrix acting on the plane.

    from shared.anim.house import *
    from shared.anim.linmap import *

The picture follows Visual Kernel's "SEE Matrix" engine: every vector in a
patch of the plane is drawn as a dot, and a matrix moves every dot to M @ p.
Dots keep their round shape while they move (only their centres are mapped),
so a scaling never turns them into ellipses.

Colour conventions on top of house.py:
  - basis i-hat and the first matrix column are X_COLOR (green),
  - basis j-hat and the second matrix column are Y_COLOR (rose),
  - the dot cloud runs from V_COLOR (left) to W_COLOR (right), so each dot
    can be followed by its colour after the move,
  - the "F" marker is INK, to show orientation (reflections flip it).
"""

from shared.anim.house import *  # noqa: F401,F403


def m2(a, b, c, d):
    """The 2x2 matrix [[a, b], [c, d]] as a 3x3 array manim can apply in-plane."""
    return np.array([[a, b, 0.0], [c, d, 0.0], [0.0, 0.0, 1.0]])


def dot_cloud(x_range=(-2, 2), y_range=(-1.5, 1.5), step=0.25, radius=0.045):
    """A rectangle of dots, coloured teal to violet from left to right."""
    xs = np.arange(x_range[0], x_range[1] + 1e-9, step)
    ys = np.arange(y_range[0], y_range[1] + 1e-9, step)
    span = max(x_range[1] - x_range[0], 1e-9)
    dots = VGroup()
    for x in xs:
        colour = interpolate_color(ManimColor(V_COLOR), ManimColor(W_COLOR), (x - x_range[0]) / span)
        for y in ys:
            dots.add(Dot([x, y, 0], radius=radius, color=colour))
    return dots


def disc_cloud(radius=1.5, step=0.2, dot_radius=0.045):
    """A disc of dots, same colouring as dot_cloud."""
    dots = dot_cloud((-radius, radius), (-radius, radius), step, dot_radius)
    keep = [d for d in dots if np.linalg.norm(d.get_center()) <= radius + 1e-9]
    return VGroup(*keep)


def move_dots(dots, M, **kwargs):
    """Animation moving every dot centre p to M @ p (dots stay round)."""
    M = np.asarray(M, dtype=float)
    if M.shape == (2, 2):
        M = m2(*M.flatten())
    return AnimationGroup(*[d.animate.move_to(M @ d.get_center()) for d in dots], **kwargs)


def shift_dots(dots, b, **kwargs):
    """Animation translating every dot by b (for affine maps)."""
    b = np.array([b[0], b[1], 0.0])
    return AnimationGroup(*[d.animate.shift(b) for d in dots], **kwargs)


def f_marker(scale=1.0, color=INK):
    """An upright letter-F polygon with its corner at the origin. It has no
    mirror symmetry, so a reflection visibly flips it."""
    pts = [(0, 0), (0.3, 0), (0.3, 0.6), (0.8, 0.6), (0.8, 0.85), (0.3, 0.85),
           (0.3, 1.1), (1.0, 1.1), (1.0, 1.35), (0, 1.35)]
    poly = Polygon(*[np.array([x, y, 0]) * scale for x, y in pts],
                   color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    return poly


def basis_arrows(M=None, tip=0.18):
    """Arrows for the images of i-hat and j-hat (the columns of M)."""
    M = np.eye(2) if M is None else np.asarray(M, dtype=float)[:2, :2]
    i_hat = Arrow(ORIGIN, [M[0, 0], M[1, 0], 0], buff=0, color=X_COLOR,
                  stroke_width=6, max_tip_length_to_length_ratio=0.25, tip_length=tip)
    j_hat = Arrow(ORIGIN, [M[0, 1], M[1, 1], 0], buff=0, color=Y_COLOR,
                  stroke_width=6, max_tip_length_to_length_ratio=0.25, tip_length=tip)
    return i_hat, j_hat


def matrix_tex(M, font_size=MIN_FONT, col_colors=(X_COLOR, Y_COLOR), fmt="{:g}"):
    """A bracketed matrix whose first column is green and second rose (the
    images of i-hat and j-hat). Entries may be numbers or TeX strings; pass
    col_colors=(None, None) for plain ink."""
    rows = [[e if isinstance(e, str) else fmt.format(e) for e in row] for row in M]
    mat = Matrix(rows, element_to_mobject=lambda e: MathTex(e, font_size=font_size, color=INK),
                 h_buff=0.9, v_buff=0.7, bracket_h_buff=0.15)
    mat.get_brackets().set_color(INK)
    for j, col in enumerate(mat.get_columns()):
        if j < len(col_colors) and col_colors[j]:
            col.set_color(col_colors[j])
    return mat


def label_box(mob, opacity=0.85, buff=0.1):
    """Background rectangle so a label stays readable over dots and grid."""
    mob.add_background_rectangle(color=BG, opacity=opacity, buff=buff)
    return mob


def lin_plane(unit=0.5, **kwargs):
    """A house plane whose grid squares are `unit` scene units wide, filling
    the 10 x 5.625 frame. Draw in plane coordinates with plane.c2p(x, y) or
    simply multiply by unit: the plane is centred at the origin and uniformly
    scaled, so move_dots(dots, M) with plane-coordinate M is still correct."""
    half_w, half_h = 5 / unit, 2.8125 / unit
    return house_plane(x_range=[-np.ceil(half_w), np.ceil(half_w), 1],
                       y_range=[-np.ceil(half_h), np.ceil(half_h), 1],
                       x_length=2 * np.ceil(half_w) * unit,
                       y_length=2 * np.ceil(half_h) * unit, **kwargs)
