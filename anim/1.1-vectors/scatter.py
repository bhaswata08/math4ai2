"""A scatter plot is a cloud of vectors.

Idea from 3b1b/videos _2016/eola/chapter1.py DataAnalyst, (c) 3Blue1Brown,
CC BY-NC-SA 4.0. Rewritten rather than ported: the upstream scene starts
from a table of numbers, this one starts from the scatter plot students
already know, turns every point into an arrow from the origin, then drops
the shafts and keeps the tips.

    shared/anim/render.sh anim/1.1-vectors/scatter.py ScatterAsVectors decks/1.1-vectors
"""

from shared.anim.house import *

# One unit per scene unit, origin pushed to the lower left so the data can
# fill the frame and the arrows fan out instead of bunching.
X_RANGE = (-2, 12.2, 1)
Y_RANGE = (-1.2, 6.8, 1)


def cloud(n=30, seed=7):
    """A correlated cloud in plane coordinates, kept clear of the frame edge."""
    rng = np.random.default_rng(seed)
    u = np.array([1.0, 0.5]) / np.linalg.norm([1.0, 0.5])
    perp = np.array([-u[1], u[0]])
    pts = []
    while len(pts) < n:
        p = np.array([5.5, 3.0]) + rng.normal(0, 2.1) * u + rng.normal(0, 0.55) * perp
        if 0.6 < p[0] < 10.8 and 0.4 < p[1] < 6.0:
            pts.append(p)
    return pts


def caption(text):
    t = Tex(text, font_size=48, color=INK)
    t.to_corner(UL, buff=0.45)
    t.add_background_rectangle(color=BG, opacity=0.9, buff=0.15)
    return t


def swap(old, new):
    """Crossfade captions. Transform between two Tex strings scrambles the glyphs."""
    return [FadeOut(old, shift=0.15 * UP), FadeIn(new, shift=0.15 * UP)]


class ScatterAsVectors(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=X_RANGE, y_range=Y_RANGE, x_length=14.2, y_length=8,
            background_line_style={"stroke_color": GRID, "stroke_width": 2, "stroke_opacity": 0.8},
            axis_config={"stroke_color": INK_DIM, "stroke_width": 3},
            faded_line_ratio=1,
        )
        origin = plane.c2p(0, 0)
        star_xy = (6, 4)
        data = cloud() + [np.array(star_xy, dtype=float)]
        pts = [plane.c2p(*p) for p in data]
        star = pts[-1]

        dots = VGroup(*[Dot(p, radius=0.08, color=INK_DIM) for p in pts])

        # 1. A scatter plot, as students know it. It is already on screen in
        # the first frame, because that frame is what the slide shows before
        # the clip plays.
        cap = caption("A scatter plot")
        self.add(plane, dots, cap)
        self.wait(1.5)

        # 2. One point is a vector: an arrow from the origin to it.
        one = Arrow(origin, star, buff=0, color=V_COLOR, stroke_width=6,
                    max_tip_length_to_length_ratio=0.08)
        coords = Matrix([[star_xy[0]], [star_xy[1]]], element_to_mobject_config={"font_size": 48})
        coords.set_color(V_COLOR)
        coords.next_to(star, UL, buff=0.25).shift(0.6 * UP)
        coords.add_background_rectangle(color=BG, opacity=0.9, buff=0.12)
        self.play(dots[-1].animate.set_color(V_COLOR).scale(1.5))
        self.play(GrowArrow(one), FadeIn(coords), run_time=1.2)
        self.wait(1.5)

        # 3. Every point is a vector.
        cap2 = caption("Every point is a vector")
        arrows = VGroup(*[
            Arrow(origin, p, buff=0, color=V_COLOR, stroke_width=3,
                  max_tip_length_to_length_ratio=0.1, tip_length=0.22)
            for p in pts[:-1]
        ])
        self.play(FadeOut(coords), *swap(cap, cap2))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), run_time=2.5)
        self.wait(1.5)

        # 4. Drop the tails, keep the heads. The tips stay put while the
        # shafts fade, then each tip settles into a dot.
        cap3 = caption("Drop the tails, keep the heads")
        everything = VGroup(*arrows, one)
        tips = VGroup(*[a.tip.copy() for a in everything])
        self.add(tips)
        self.play(*swap(cap2, cap3), FadeOut(everything), FadeOut(dots), run_time=1.5)
        final = VGroup(*[Dot(p, radius=0.09, color=V_COLOR) for p in pts])
        self.play(*[ReplacementTransform(t, d) for t, d in zip(tips, final)], run_time=1)
        self.wait(1)

        # 5. The shape of the cloud: an ellipse from the data's own spread
        # (2.3 standard deviations along each principal direction), which is
        # the picture PCA returns to on Day 3.
        cap4 = caption("The shape of the data")
        xy = np.array([p[:2] for p in pts])
        centre = xy.mean(axis=0)
        evals, evecs = np.linalg.eigh(np.cov(xy.T))
        major = evecs[:, 1]
        shape = Ellipse(width=2 * 2.3 * np.sqrt(evals[1]), height=2 * 2.3 * np.sqrt(evals[0]),
                        color=RESULT_COLOR, stroke_width=5)
        shape.rotate(np.arctan2(major[1], major[0])).move_to([*centre, 0])
        self.play(*swap(cap3, cap4), Create(shape), run_time=1.5)
        self.wait(2)
