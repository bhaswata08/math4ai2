# Original work for Mathematics for AI, CC BY-NC-SA 4.0 (mini-batch layout after 3b1b/videos _2017/nn/part3.py)

from shared.anim.house import *
import numpy as np


# =============================================================================
# Helper math functions
# =============================================================================

def loss_1d(w):
    """Smooth 1D loss with single basin, minimum at w ≈ 0.67."""
    return 0.5 * (w - 1.0) ** 2 + 0.2 * np.sin(2.0 * (w - 1.0)) + 0.2


def d_loss_1d(w):
    """Exact derivative of loss_1d."""
    return (w - 1.0) + 0.4 * np.cos(2.0 * (w - 1.0))


def get_bowl_contours(axes, levels, scale_x=1.0, scale_y=1.0):
    """Create concentric elliptical contours for L(w1, w2) = w1^2/2 + 4 w2^2."""
    mobs = []
    opacities = np.linspace(0.04, 0.22, len(levels))
    origin = axes.c2p(0.0, 0.0)
    for lvl, opac in zip(levels, opacities):
        a = np.sqrt(2.0 * lvl)
        b = np.sqrt(lvl / 4.0)
        ell = Ellipse(
            width=2.0 * a * scale_x,
            height=2.0 * b * scale_y,
            stroke_color=INK_DIM,
            stroke_width=1.5,
            fill_color=V_COLOR,
            fill_opacity=opac,
        ).move_to(origin)
        mobs.append(ell)
    return VGroup(*mobs)


# =============================================================================
# SCENE 1: Descent1D
# =============================================================================
class Descent1D(Scene):
    def construct(self):
        # 1. Coordinate axes on the left
        axes = Axes(
            x_range=[-2.2, 2.6, 1.0],
            y_range=[0.0, 5.0, 1.0],
            x_length=5.0,
            y_length=3.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.5,
                "include_ticks": True,
            },
            tips=False,
        ).move_to(np.array([-2.0, -0.35, 0.0]))

        lbl_w = MathTex("w", font_size=MIN_FONT, color=X_COLOR)
        lbl_w.next_to(axes.x_axis.get_end(), DOWN, buff=0.12)
        lbl_w.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_L = MathTex(r"L(w)", font_size=MIN_FONT, color=V_COLOR)
        lbl_L.next_to(axes.y_axis.get_end(), UP + RIGHT * 0.1, buff=0.12)
        lbl_L.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        curve = axes.plot(
            loss_1d,
            x_range=[-2.0, 2.45],
            color=V_COLOR,
            stroke_width=4.0,
        )

        # 2. Right-hand panel: title and live readouts
        title = MathTex(r"w \leftarrow w - \eta \, L'(w)", font_size=MIN_FONT, color=INK)
        title.move_to(np.array([2.55, 2.4, 0.0]))
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Value tracker for w
        w0 = -1.8
        eta = 0.42
        w_tracker = ValueTracker(w0)

        # Readout rows
        lbl_w_row = MathTex(r"w =", font_size=MIN_FONT, color=X_COLOR)
        num_w_row = DecimalNumber(
            w0,
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=X_COLOR,
            include_sign=True,
        )
        num_w_row.add_updater(lambda m: m.set_value(w_tracker.get_value()))
        row_w = VGroup(lbl_w_row, num_w_row).arrange(RIGHT, buff=0.15)

        lbl_L_row = MathTex(r"L(w) =", font_size=MIN_FONT, color=V_COLOR)
        num_L_row = DecimalNumber(
            loss_1d(w0),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=V_COLOR,
        )
        num_L_row.add_updater(lambda m: m.set_value(loss_1d(w_tracker.get_value())))
        row_L = VGroup(lbl_L_row, num_L_row).arrange(RIGHT, buff=0.15)

        lbl_dL_row = MathTex(r"L'(w) =", font_size=MIN_FONT, color=RESULT_COLOR)
        num_dL_row = DecimalNumber(
            d_loss_1d(w0),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=RESULT_COLOR,
            include_sign=True,
        )
        num_dL_row.add_updater(lambda m: m.set_value(d_loss_1d(w_tracker.get_value())))
        row_dL = VGroup(lbl_dL_row, num_dL_row).arrange(RIGHT, buff=0.15)

        lbl_step_row = MathTex(r"|\Delta w| =", font_size=MIN_FONT, color=X_COLOR)
        num_step_row = DecimalNumber(
            eta * abs(d_loss_1d(w0)),
            num_decimal_places=2,
            font_size=MIN_FONT,
            color=X_COLOR,
        )
        num_step_row.add_updater(lambda m: m.set_value(eta * abs(d_loss_1d(w_tracker.get_value()))))
        row_step = VGroup(lbl_step_row, num_step_row).arrange(RIGHT, buff=0.15)

        lbl_eta_row = MathTex(rf"\eta = {eta:.2f}", font_size=MIN_FONT, color=INK)
        row_eta = VGroup(lbl_eta_row)

        readout_box = VGroup(row_eta, row_w, row_L, row_dL, row_step).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        readout_box.move_to(np.array([2.55, -0.1, 0.0]))
        readout_box.add_background_rectangle(color=BG, opacity=0.85, buff=0.10)

        # 3. Dynamic ball and vertical dashed projection line
        ball = always_redraw(
            lambda: Dot(
                axes.c2p(w_tracker.get_value(), loss_1d(w_tracker.get_value())),
                radius=0.10,
                color=RESULT_COLOR,
            )
        )
        proj_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(w_tracker.get_value(), 0),
                axes.c2p(w_tracker.get_value(), loss_1d(w_tracker.get_value())),
                color=INK_FAINT,
                stroke_width=1.5,
                dash_length=0.08,
            )
        )

        # 4. First frame: givens immediately visible
        self.add(
            axes, lbl_w, lbl_L, curve,
            title, readout_box, row_eta, row_w, row_L, row_dL, row_step,
            proj_line, ball
        )
        self.wait(1.2)

        # 5. Perform 5 gradient descent steps
        for it in range(5):
            w_curr = w_tracker.get_value()
            grad = d_loss_1d(w_curr)
            w_next = w_curr - eta * grad

            # Tangent line segment
            tan_span = 0.50
            w_t_min = max(-2.1, w_curr - tan_span)
            w_t_max = min(2.4, w_curr + tan_span)
            tan_line = axes.plot(
                lambda u, wc=w_curr, g=grad: loss_1d(wc) + g * (u - wc),
                x_range=[w_t_min, w_t_max],
                color=RESULT_COLOR,
                stroke_width=3.2,
            )

            # Step arrow along w axis
            step_arrow = Arrow(
                axes.c2p(w_curr, 0.0),
                axes.c2p(w_next, 0.0),
                buff=0,
                stroke_width=4.0,
                max_tip_length_to_length_ratio=0.30,
                color=X_COLOR,
            )

            # Step animations
            self.play(Create(tan_line), GrowArrow(step_arrow), run_time=0.6)
            self.play(w_tracker.animate.set_value(w_next), run_time=0.9, rate_func=smooth)
            if it == 0:
                self.wait(0.5)  # hold the first step so the numbers can be checked
            self.play(FadeOut(tan_line), FadeOut(step_arrow), run_time=0.3)
            self.wait(0.2)

        self.wait(2.0)


# =============================================================================
# SCENE 2: LearningRates
# =============================================================================
class LearningRates(Scene):
    """L = w^2 under three step sizes. The factor (1 - 2 eta) drives every panel."""

    def construct(self):
        centers = [-3.2, 0.0, 3.2]
        etas = [0.05, 0.30, 1.05]
        w0 = -1.25
        n_steps = 12
        axes_y = -0.25

        def grad(w):
            return 2.0 * w  # L = w^2

        # live values, computed from the update rule itself
        paths = []
        for eta in etas:
            ws = [w0]
            for _ in range(n_steps):
                ws.append(ws[-1] - eta * grad(ws[-1]))
            paths.append(ws)
        factors = [1.0 - 2.0 * eta for eta in etas]
        fcols = [X_COLOR if abs(f) < 1 else Y_COLOR for f in factors]

        YMAX = 5.5

        def make_view(cx, R):
            """Axes and curve of one panel, spanning w in [-R, R], y in [0, YMAX]."""
            ax = Axes(
                x_range=[-R, R, 1.0],
                y_range=[0.0, YMAX, YMAX],
                x_length=2.8,
                y_length=3.0,
                axis_config={"stroke_color": INK_DIM, "stroke_width": 2.0, "include_ticks": False},
                tips=False,
            ).move_to(np.array([cx, axes_y, 0.0]))
            wmax = min(0.93 * R, np.sqrt(YMAX))
            curve = ax.plot(lambda w: w ** 2, x_range=[-wmax, wmax], color=V_COLOR, stroke_width=3.5)
            tick_vals = [-2, 0, 2] if R < 3 else [-4, 0, 4]
            ticks = VGroup(*[
                MathTex(f"{v}", font_size=MIN_FONT, color=INK_DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.08)
                for v in tick_vals
            ])
            return ax, VGroup(ax, curve, ticks)

        # the diverging panel has a wider fixed w range, so the parabola is drawn flatter
        # and the ball can be seen climbing out through the top
        Rs = [2.6, 2.6, 4.5]
        views, groups = [], []
        for cx, R in zip(centers, Rs):
            ax, grp = make_view(cx, R)
            views.append(ax)
            groups.append(grp)

        heads = []
        for cx, eta, f, col in zip(centers, etas, factors, fcols):
            h1 = MathTex(rf"\eta = {eta:.2f}", font_size=MIN_FONT, color=INK).move_to(np.array([cx, 2.45, 0]))
            h2 = MathTex(rf"1-2\eta = {f:.2f}", font_size=MIN_FONT, color=col).move_to(np.array([cx, 1.85, 0]))
            heads.append(VGroup(h1, h2))

        def readout(j, k):
            return MathTex(rf"w_{{{k}}} = {paths[j][k] + 0.0:+.2f}".replace("-0.00", "0.00").replace("+0.00", "0.00"), font_size=MIN_FONT, color=RESULT_COLOR).move_to(
                np.array([centers[j], -2.5, 0])
            )

        def inside(w):
            return w ** 2 <= YMAX

        def top_pt(j, w):
            return views[j].c2p(w, YMAX)

        balls = [Dot(views[j].c2p(w0, w0 ** 2), radius=0.09, color=RESULT_COLOR) for j in range(3)]
        reads = [readout(j, 0) for j in range(3)]
        past = [VGroup() for _ in range(3)]
        out_arrow = None  # up arrow that replaces the ball once it has left the top

        self.add(*groups, *heads, *balls, *reads)
        self.wait(1.5)

        for k in range(n_steps):
            anims, new_reads = [], []
            exit_now = False
            for j in range(3):
                w_prev, w_next = paths[j][k], paths[j][k + 1]
                if inside(w_prev):
                    dot = Dot(views[j].c2p(w_prev, w_prev ** 2), radius=0.05, color=INK_FAINT)
                    past[j].add(dot)
                    self.add(dot)
                if inside(w_next):
                    anims.append(balls[j].animate.move_to(views[j].c2p(w_next, w_next ** 2)))
                elif inside(w_prev):
                    anims.append(balls[j].animate.move_to(top_pt(j, w_next)))
                    exit_now = True
                elif out_arrow is not None:
                    anims.append(out_arrow.animate.move_to(top_pt(j, w_next) + UP * 0.2))
                new_reads.append(readout(j, k + 1))
            self.play(*anims, run_time=0.7, rate_func=smooth)
            if exit_now:
                p_top = top_pt(2, paths[2][k + 1])
                out_arrow = Arrow(p_top + DOWN * 0.0, p_top + UP * 0.4, buff=0, stroke_width=6,
                                  color=Y_COLOR, max_tip_length_to_length_ratio=0.5)
                self.play(FadeOut(balls[2]), GrowArrow(out_arrow), run_time=0.3)
            for j in range(3):
                self.remove(reads[j])
                reads[j] = new_reads[j]
                self.add(reads[j])
            self.wait(0.15)

        # verdicts: the factor alone decides
        verdicts = [r"\text{crawls}", r"\text{converges}", r"\text{diverges}"]
        vcols = [X_COLOR, X_COLOR, Y_COLOR]
        vtex = [
            MathTex(v, font_size=MIN_FONT, color=c).move_to(np.array([cx, -2.5, 0]))
            for v, c, cx in zip(verdicts, vcols, centers)
        ]
        self.wait(0.5)
        self.play(*[FadeOut(r) for r in reads], run_time=0.4)
        self.play(*[FadeIn(v) for v in vtex], run_time=0.5)
        self.wait(3.0)
