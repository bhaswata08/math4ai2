"""Block 3.2: handwritten digits (R^64) projected onto the first two principal directions."""

from shared.anim.house import *
from shared.anim.linmap import label_box

CLASSES = (0, 2, 4)           # best-separated visually distinct triple in PC1/PC2
COLORS = {0: V_COLOR, 2: W_COLOR, 4: Y_COLOR}

_d = np.load("anim/3.2-pca/data/digits.npz")
IMAGES = _d["images"].astype(float)          # (1797, 64), values 0..16
TARGET = _d["target"]
M_PTS = len(IMAGES)
_Xc = IMAGES - IMAGES.mean(0)
_C = _Xc.T @ _Xc / M_PTS                      # C = X^T X / m on centred data
_w, _V = np.linalg.eigh(_C)
_o = np.argsort(_w)[::-1]
EIGVALS, EIGVECS = _w[_o], _V[:, _o]
P2 = EIGVECS[:, :2].copy()
for j in range(2):                            # sign convention: fix the sign of each axis
    if P2[np.argmax(np.abs(P2[:, j])), j] < 0:
        P2[:, j] *= -1
SCORES = _Xc @ P2                             # (m, 2) = X P_2
SHARE = EIGVALS[:2].sum() / EIGVALS.sum()


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def digit_image(vec, cell=0.15, border=INK_DIM):
    g = VGroup()
    for r in range(8):
        for c in range(8):
            v = vec[r * 8 + c] / 16.0
            sq = Square(side_length=cell, stroke_width=0, fill_opacity=1,
                        fill_color=interpolate_color(ManimColor(BG), ManimColor(INK), v))
            sq.move_to([c * cell, -r * cell, 0])
            g.add(sq)
    g.move_to(ORIGIN)
    frame = SurroundingRectangle(g, buff=0.04, color=border, stroke_width=3)
    return VGroup(g, frame)


class DigitsScatter(Scene):
    def construct(self):
        # example images: first sample of each chosen class
        imgs = VGroup(*[digit_image(IMAGES[np.where(TARGET == c)[0][0]], cell=0.17, border=COLORS[c])
                        for c in CLASSES]).arrange(RIGHT, buff=0.7)
        imgs.move_to([0, 0.35, 0])
        cap = tex(r"\mathbf{x}_i \in \mathbb{R}^{64}", INK)
        cap.next_to(imgs, DOWN, buff=0.45)
        sub = tex(r"8\times 8 = 64\ \text{pixels}", INK_DIM)
        sub.next_to(cap, DOWN, buff=0.25)
        self.add(imgs, cap, sub)
        self.wait(3.0)

        # scatter geometry: L-shaped axes at the left and bottom so numbers stay off the points
        S = SCORES[np.isin(TARGET, CLASSES)]
        XR, YR = (-25, 35), (-35, 25)
        L = 3.7
        ref = Axes(x_range=[*XR, 10], y_range=[*YR, 10], x_length=L, y_length=L)
        ref.move_to([-2.1, -0.2, 0])
        c2p = ref.c2p
        xax = Line(c2p(XR[0], YR[0]), c2p(XR[1], YR[0]), color=INK_DIM, stroke_width=3)
        yax = Line(c2p(XR[0], YR[0]), c2p(XR[0], YR[1]), color=INK_DIM, stroke_width=3)
        xt, yt = [-20, 0, 20], [-20, 0, 20]
        ticks = VGroup(
            *[Line(c2p(v, YR[0]), c2p(v, YR[0]) + 0.08 * DOWN, color=INK_DIM, stroke_width=3) for v in xt],
            *[Line(c2p(XR[0], v), c2p(XR[0], v) + 0.08 * LEFT, color=INK_DIM, stroke_width=3) for v in yt])
        xnum = VGroup(*[tex(f"{v}", INK_DIM).next_to(c2p(v, YR[0]), DOWN, buff=0.14) for v in xt])
        ynum = VGroup(*[tex(f"{v}", INK_DIM).next_to(c2p(XR[0], v), LEFT, buff=0.14) for v in yt])
        xlab = tex(r"\alpha_{i1}", INK).next_to(xax, RIGHT, buff=0.1).align_to(xnum, UP)
        ylab = tex(r"\alpha_{i2}", INK).next_to(yax, UP, buff=0.1)
        frame = VGroup(xax, yax, ticks, xnum, ynum, xlab, ylab)

        dots = {}
        for c in CLASSES:
            pts = SCORES[TARGET == c]
            dots[c] = VGroup(*[Dot(c2p(a, b), radius=0.035, color=COLORS[c], fill_opacity=0.8)
                               for a, b in pts])
        cen = {c: SCORES[TARGET == c].mean(0) for c in CLASSES}
        off = {0: (-16, -26), 2: (-12, 21), 4: (29, 21)}   # label spot, data units
        labs = {}
        for c in CLASSES:
            labs[c] = tex(str(c), COLORS[c], 56).move_to(c2p(*off[c]))

        self.play(FadeOut(cap), FadeOut(sub), FadeIn(frame), run_time=1.0)
        self.play(*[imgs[k].animate.scale(0.25).move_to(c2p(*cen[c]))
                    for k, c in enumerate(CLASSES)], run_time=1.5)
        for k, c in enumerate(CLASSES):
            self.play(FadeOut(imgs[k]), FadeIn(dots[c], lag_ratio=0.02), FadeIn(labs[c]),
                      run_time=1.3)
        self.wait(1.5)

        # share of variance over all 64 components
        r1 = tex(r"\lambda_1+\lambda_2", INK)
        r2 = tex(r"\sum\nolimits_{j=1}^{64}\lambda_j", INK)
        bar = Line(LEFT, RIGHT, color=INK_DIM).set_width(max(r1.width, r2.width) + 0.2)
        frac = VGroup(r1, bar, r2).arrange(DOWN, buff=0.2)
        res = tex(rf"= {100 * SHARE:.1f}\%", RESULT_COLOR)
        share = VGroup(frac, res).arrange(DOWN, buff=0.3)
        share.move_to([3.2, 0, 0])
        assert share.get_right()[0] < 4.85 and share.get_left()[0] > 1.0, (share.get_left(), share.get_right())
        self.play(FadeIn(frac), run_time=0.8)
        self.wait(0.6)
        self.play(FadeIn(res), run_time=0.8)
        self.wait(2.0)
