"""Block 3.1: low-rank approximation. A matrix is a sum of rank-1 layers; truncating the sum compresses an image."""

import os

from PIL import Image

from shared.anim.house import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "assets", "moon_gray.png")


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def ramp_gray(t):
    """BG -> INK for t in [0, 1]."""
    return interpolate_color(ManimColor(BG), ManimColor(INK), float(np.clip(t, 0, 1)))


def ramp_div(t):
    """Diverging: t in [-1, 1], teal (negative) -> BG -> amber (positive)."""
    t = float(np.clip(t, -1, 1))
    end = RESULT_COLOR if t >= 0 else V_COLOR
    return interpolate_color(ManimColor(BG), ManimColor(end), abs(t))


def heat(vals, cell, ramp, center=ORIGIN):
    """A grid of squares coloured by vals (2-D array, row 0 on top)."""
    vals = np.atleast_2d(vals)
    r, c = vals.shape
    g = VGroup()
    for i in range(r):
        for j in range(c):
            sq = Square(cell, stroke_width=0.6, stroke_color=BG, fill_opacity=1,
                        fill_color=ramp(vals[i, j]))
            sq.move_to([(j - (c - 1) / 2) * cell, -(i - (r - 1) / 2) * cell, 0])
            g.add(sq)
    return g.move_to(center)


SMILEY = ["000111111000", "001000000100", "010000000010", "100110011001",
          "100110011001", "100000000001", "100100001001", "100011110001",
          "010000000010", "001000000100", "000111111000", "000000000000"]


class RankOneLayers(Scene):
    """A 12x12 picture rebuilt one rank-1 layer at a time."""

    def construct(self):
        A = np.array([[int(ch) for ch in r] for r in SMILEY], float)
        U, s, Vt = np.linalg.svd(A)
        rank = int(np.sum(s > 1e-9))
        terms = []
        for k in range(rank):
            u, v = U[:, k], Vt[k]
            if u.sum() < 0:
                u, v = -u, -v
            terms.append((s[k], u, v))
        print("sigma", s[:rank].round(2).tolist())

        c = 0.18
        gx, gy = -0.35, 0.2
        ax, ay = -3.7, 0.2
        sx, sy = 3.55, 0.2
        a_grid = heat(A, c, ramp_gray, [ax, ay, 0])
        a_lab = tex("A").move_to([ax, 2.2, 0])

        def layer(k):
            sg, u, v = terms[k]
            term = sg * np.outer(u, v)
            grid = heat(term / np.abs(term).max(), c, ramp_div, [gx, gy, 0])
            ucol = heat(u[:, None] / np.abs(u).max(), c, ramp_div,
                        [gx - 6 * c - 0.14 - c / 2, gy, 0])
            vrow = heat(v[None, :] / np.abs(v).max(), c, ramp_div,
                        [gx, gy + 6 * c + 0.14 + c / 2, 0])
            ucol.set_stroke(RESULT_COLOR, 2.5, background=False)
            vrow.set_stroke(V_COLOR, 2.5, background=False)
            for m in ucol:
                m.set_stroke(RESULT_COLOR, 1.2)
            for m in vrow:
                m.set_stroke(V_COLOR, 1.2)
            S = sum(sg_ * np.outer(u_, v_) for sg_, u_, v_ in terms[:k + 1])
            run = heat(S, c, ramp_gray, [sx, sy, 0])
            return VGroup(ucol, vrow, grid), run

        def counter(k):
            return tex(f"k={k}", RESULT_COLOR).move_to([sx, 1.62, 0])

        layer_grp, run = layer(0)
        kc = counter(1)
        cap = MathTex(r"A=", r"\sigma_1", r"\mathbf u_1", r"\mathbf v_1^T", r"+",
                      r"\sigma_2", r"\mathbf u_2", r"\mathbf v_2^T", r"+\cdots",
                      font_size=MIN_FONT, color=INK)
        for i, col in ((2, RESULT_COLOR), (6, RESULT_COLOR), (3, V_COLOR), (7, V_COLOR)):
            cap[i].set_color(col)
        cap.move_to([0, -1.85, 0])
        plus = tex("+", INK).move_to([(gx + sx) / 2, gy, 0])
        lay_lab = MathTex(r"\sigma_k", r"\mathbf u_k", r"\mathbf v_k^T", font_size=MIN_FONT, color=INK)
        lay_lab[1].set_color(RESULT_COLOR)
        lay_lab[2].set_color(V_COLOR)
        lay_lab.move_to([gx, 2.2, 0])
        sum_lab = tex("A_k", RESULT_COLOR).move_to([sx, 2.2, 0])
        self.add(a_grid, a_lab, layer_grp, run, kc, cap, plus, lay_lab, sum_lab)
        self.wait(1.8)
        for k in range(1, rank):
            new_layer, new_run = layer(k)
            new_kc = counter(k + 1)
            self.play(Transform(layer_grp, new_layer), Transform(run, new_run),
                      FadeOut(kc), FadeIn(new_kc), run_time=1.2)
            kc = new_kc
            self.wait(1.0 if k < rank - 1 else 1.0)
        self.wait(1.0)


def load_image():
    return np.asarray(Image.open(IMG).convert("L"), dtype=float)


def pct_text(p):
    return f"{p:.1f}" if p < 10 else f"{p:.0f}"


class ImageCompression(Scene):
    """Rank-k reconstruction next to the original, with the storage cost."""

    def construct(self):
        img = load_image()
        m, n = img.shape
        U, s, Vt = np.linalg.svd(img, full_matrices=False)

        def recon(k):
            R = (U[:, :k] * s[:k]) @ Vt[:k]
            return np.clip(R, 0, 255).astype(np.uint8)

        W = 3.6
        ycen = 0.15

        def pic(arr, x):
            im = ImageMobject(arr)
            im.set_width(W)
            return im.move_to([x, ycen, 0])

        orig = pic(img.astype(np.uint8), 2.05)
        ks = [1, 2, 5, 10, 20, 50]
        cur = pic(recon(ks[0]), -2.05)

        def header(k):
            return tex(f"k={k}", RESULT_COLOR).move_to([0, 2.25, 0])

        def storage(k):
            used = k * (m + n + 1)
            full = m * n
            pct = 100 * used / full
            l1 = tex(rf"k(m+n+1)={k}\cdot {m + n + 1}={used:,}".replace(",", "{,}"), RESULT_COLOR)
            l2 = tex(rf"mn={full:,}".replace(",", "{,}") + rf"\quad({pct_text(pct)}\%)", INK)
            return VGroup(l1, l2).arrange(DOWN, buff=0.18).move_to([0, -1.95, 0])

        lab_l = tex("A_k", RESULT_COLOR).move_to([-2.05, 2.25, 0])
        lab_r = tex("A", INK).move_to([2.05, 2.25, 0])
        hd = header(ks[0])
        st = storage(ks[0])
        self.add(orig, cur, hd, st, lab_l, lab_r)
        self.wait(1.5)
        for k in ks[1:]:
            new = pic(recon(k), -2.05)
            self.play(FadeIn(new, run_time=0.4), Transform(hd, header(k)), Transform(st, storage(k)),
                      run_time=0.4)
            self.remove(cur)
            cur = new
            self.wait(1.5)
        self.wait(0.5)


class SingularSpectrum(Scene):
    """Singular values of the image: a few large, a long tail; keep the first 20."""

    def construct(self):
        img = load_image()
        s = np.linalg.svd(img, compute_uv=False)
        N = 60  # bars drawn; energy uses all 240
        K = 20
        energy = (s[:K] ** 2).sum() / (s ** 2).sum() * 100
        print("energy", energy)

        x0, x1 = -3.6, 3.9
        y0, y1 = -0.6, 1.5
        bw = (x1 - x0) / N
        bars = VGroup()
        for i, sv in enumerate(s[:N]):
            h = (y1 - y0) * sv / s[0]
            r = Rectangle(width=bw, height=h, stroke_width=0, fill_color=INK_DIM, fill_opacity=1)
            r.move_to([x0 + (i + 0.5) * bw, y0 + h / 2, 0])
            bars.add(r)
        xaxis = Line([x0 - 0.05, y0 - 0.04, 0], [x1 + 0.15, y0 - 0.04, 0], color=INK, stroke_width=3)
        yaxis = Line([x0 - 0.05, y0 - 0.04, 0], [x0 - 0.05, y1 + 0.2, 0], color=INK, stroke_width=3)
        lab_i = tex("i").move_to([x1 + 0.6, y0 - 0.04, 0])
        lab_s = tex(r"\sigma_i").move_to([x0 + 0.1, y1 + 0.65, 0])
        cap1 = tex(r"\text{keep }\sigma_1,\dots,\sigma_{20}", RESULT_COLOR).move_to([0, -1.3, 0])
        cap2 = tex(rf"\sum\nolimits_{{i\le 20}}\sigma_i^2\,/\sum\nolimits_i\sigma_i^2={energy:.1f}\%", INK).move_to([0, -2.05, 0])
        cut = DashedLine([x0 + K * bw, y0, 0], [x0 + K * bw, y1 + 0.1, 0], color=INK_FAINT, stroke_width=3)

        self.add(bars, xaxis, yaxis, lab_i, lab_s)
        self.wait(1.8)
        self.play(*[b.animate.set_fill(RESULT_COLOR) for b in bars[:K]],
                  *[b.animate.set_fill(INK_FAINT, opacity=0.45) for b in bars[K:]],
                  Create(cut), FadeIn(cap1), run_time=1.5)
        self.wait(1.2)
        self.play(FadeIn(cap2), run_time=1.0)
        self.wait(5.0)
