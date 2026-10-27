"""Block 3.2: eigenfaces. Faces are points in R^4096; the top eigenvectors of C, reshaped, look like faces."""

import os

from shared.anim.house import *

HERE = os.path.dirname(os.path.abspath(__file__))
M_PTS = 400


def tex(s, color=INK, size=MIN_FONT):
    return MathTex(s, font_size=size, color=color)


def load():
    d = np.load(os.path.join(HERE, "data", "olivetti.npz"))
    imgs = d["images"].astype(float)
    mu = imgs.mean(0)
    X = imgs - mu
    _, s, Vt = np.linalg.svd(X, full_matrices=False)
    lam = s ** 2 / M_PTS
    return imgs, mu, X, Vt, lam, lam / lam.sum()


def to_u8(v, lo=None, hi=None):
    v = np.asarray(v, float).reshape(64, 64)
    lo = v.min() if lo is None else lo
    hi = v.max() if hi is None else hi
    return (255 * np.clip((v - lo) / (hi - lo), 0, 1)).astype(np.uint8)


def pic(arr, h, pos):
    im = ImageMobject(arr)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
    im.set_height(h)
    return im.move_to([pos[0], pos[1], 0])


class Eigenfaces(Scene):
    def construct(self):
        imgs, mu, X, Vt, lam, share = load()

        # frame one: five faces, five different people
        idx = [0, 50, 120, 210, 330]
        h = 1.7
        xs = [-3.8, -1.9, 0, 1.9, 3.8]
        faces = Group(*[pic(to_u8(imgs[i], 0, 255), h, (x, 0.7)) for i, x in zip(idx, xs)])
        lab = tex(r"\mathbf{x}_i \in \mathbb{R}^{4096}").move_to([0, -0.7, 0])
        sub = tex(r"64\times 64 \text{ pixels, one number each}", INK_DIM).move_to([0, -1.5, 0])
        self.add(faces, lab, sub)
        self.wait(3.5)
        self.play(FadeOut(faces), FadeOut(lab), FadeOut(sub), run_time=0.7)

        # mean face and eigenfaces
        fh = 1.75
        mu_img = pic(to_u8(mu, 0, 255), fh, (-3.9, 0.15))
        mu_lab = tex(r"\boldsymbol\mu", RESULT_COLOR).move_to([-3.9, -0.98, 0])
        cap = VGroup(tex(r"\mathbf p_j \in", INK_DIM), tex(r"\mathbb{R}^{4096}", INK_DIM)).arrange(DOWN, buff=0.12).move_to([-3.9, -1.95, 0])
        cols = [-1.95, 0.02, 1.99, 3.95]
        rows = [1.425, -0.975]
        eig, labs = Group(), VGroup()
        for j in range(8):
            r, c = divmod(j, 4)
            x, y = cols[c], rows[r]
            eig.add(pic(to_u8(Vt[j]), fh, (x, y)))
            l = MathTex(rf"\mathbf p_{j + 1}", rf"\ {100 * share[j]:.1f}\%", font_size=MIN_FONT, color=INK_DIM)
            l[0].set_color(RESULT_COLOR)
            l.move_to([x, y - fh / 2 - 0.3, 0])
            labs.add(l)
        self.play(FadeIn(mu_img), FadeIn(mu_lab), run_time=0.8)
        self.wait(2.5)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(eig[j]), FadeIn(labs[j]))
                                for j in range(8)], lag_ratio=0.4, run_time=5.0))
        self.wait(1.5)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(2.5)


class FaceReconstruction(Scene):
    def construct(self):
        imgs, mu, X, Vt, lam, share = load()
        FACE = 100
        x = X[FACE]
        alpha = Vt @ x
        cum = np.cumsum(share)
        ks = [0, 1, 5, 10, 25, 50, 100, 200]

        def recon(k):
            return mu + alpha[:k] @ Vt[:k]

        def err(k):
            return np.linalg.norm(x - alpha[:k] @ Vt[:k]) / np.linalg.norm(x)

        H = 2.7
        yf = 0.05
        xl, xr = -1.55, 1.55
        ratio_lo, ratio_hi = 0, 255
        orig = pic(to_u8(imgs[FACE], 0, 255), H, (xr, yf))
        orig_lab = tex(r"\text{original}", INK).move_to([xr, yf - H / 2 - 0.27, 0])
        rec_lab = tex(r"\hat{\mathbf x}", RESULT_COLOR).move_to([xl, yf - H / 2 - 0.22, 0])

        formula = MathTex(r"\hat{\mathbf x}", r"=", r"\boldsymbol\mu", r"+",
                          r"\sum_{j=1}^{k}", r"\alpha_j", r"\mathbf p_j", font_size=MIN_FONT, color=INK)
        formula[0].set_color(RESULT_COLOR)
        formula[2].set_color(RESULT_COLOR)
        formula[6].set_color(RESULT_COLOR)
        formula.move_to([0, 2.05, 0])

        def view(k):
            im = pic(to_u8(recon(k), 0, 255), H, (xl, yf))
            if k == 0:
                kl = tex(r"k=0:\ \boldsymbol\mu", RESULT_COLOR)
                el = tex(rf"\|\mathbf x-\hat{{\mathbf x}}\|/\|\mathbf x-\boldsymbol\mu\|={err(0):.2f}", INK_DIM)
            else:
                kl = tex(rf"k={k}\ \cdot\ {100 * cum[k - 1]:.1f}\%\text{{ of variance}}", RESULT_COLOR)
                el = tex(rf"\|\mathbf x-\hat{{\mathbf x}}\|/\|\mathbf x-\boldsymbol\mu\|={err(k):.2f}", INK_DIM)
            kl.move_to([0, -2.03, 0])
            el.move_to([0, -2.47, 0])
            return im, VGroup(kl, el)

        cur, txt = view(0)
        self.add(orig, orig_lab, rec_lab, formula, cur, txt)
        self.wait(2.2)
        for k in ks[1:]:
            new, ntxt = view(k)
            self.play(FadeIn(new, run_time=0.5), FadeOut(txt, run_time=0.25), run_time=0.5)
            self.remove(cur)
            cur = new
            self.play(FadeIn(ntxt, run_time=0.25))
            txt = ntxt
            self.wait(1.8)
        self.wait(2.0)
