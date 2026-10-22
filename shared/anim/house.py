"""House style for every manim clip in the course.

Import this first in a scene file:

    from shared.anim.house import *

It sets the background to the deck's background colour so a clip sits on
the slide with no visible frame, and fixes the colour roles below. Use the
role names, never raw hex, so a colour means the same thing in every clip
and on every slide (the deck CSS carries the same tokens).

Text floor: clips play about 1100px wide on a 1280px slide, so a clip is
shown at roughly 0.57x of its 1920px render. Keep every MathTex and Text at
font_size >= 40 so nothing lands below about 23px on the slide.
"""

from manim import *  # noqa: F401,F403

# Deck tokens. Keep in sync with shared/css/custom.css.
BG = "#12151b"
INK = "#e9ebef"
INK_DIM = "#a7b0be"
INK_FAINT = "#6d7789"
GRID = "#2a3f5c"

# Colour roles.
V_COLOR = "#6fd0c0"      # first given vector (teal)
W_COLOR = "#c792ea"      # second given vector (violet)
RESULT_COLOR = "#f0a35e" # anything derived: sums, scaled vectors, projections (amber)
X_COLOR = "#8bd17c"      # x components and x axis movement (green)
Y_COLOR = "#e8798a"      # y components and y axis movement (rose)
HIGHLIGHT = "#ffd166"    # momentary emphasis only, never a resting colour

MIN_FONT = 40

config.background_color = BG
config.frame_rate = 30


def house_plane(**kwargs):
    """A NumberPlane in the house style: faint grid, light axes."""
    style = dict(
        background_line_style={"stroke_color": GRID, "stroke_width": 2, "stroke_opacity": 0.8},
        axis_config={"stroke_color": INK_DIM, "stroke_width": 3},
        faded_line_ratio=1,
    )
    style.update(kwargs)
    return NumberPlane(**style)
