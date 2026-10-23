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
        title.move_to(np.array([2.55, 1.95, 0.0]))
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

        readout_box = VGroup(row_w, row_L, row_dL, row_step).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        readout_box.move_to(np.array([2.55, 0.15, 0.0]))
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
            title, readout_box, row_w, row_L, row_dL, row_step,
            proj_line, ball
        )
        self.wait(1.2)

        # 5. Perform 5 gradient descent steps
        for _ in range(5):
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
            self.play(FadeOut(tan_line), FadeOut(step_arrow), run_time=0.3)
            self.wait(0.2)

        self.wait(2.0)


# =============================================================================
# SCENE 2: LearningRates
# =============================================================================
class LearningRates(Scene):
    def construct(self):
        panel_centers_x = [-3.15, 0.0, 3.15]
        etas = [0.05, 0.30, 1.05]
        eta_labels = [r"\eta = 0.05", r"\eta = 0.30", r"\eta = 1.05"]

        panels = []
        balls = []
        current_w = []

        w0 = -1.25

        for cx, eta_val, lbl_str in zip(panel_centers_x, etas, eta_labels):
            # Axes for this panel
            ax = Axes(
                x_range=[-2.6, 2.6, 1.0],
                y_range=[0.0, 5.5, 2.0],
                x_length=2.7,
                y_length=3.3,
                axis_config={
                    "stroke_color": INK_DIM,
                    "stroke_width": 2.0,
                    "include_ticks": False,
                },
                tips=False,
            ).move_to(np.array([cx, -0.45, 0.0]))

            curve = ax.plot(
                lambda w: w ** 2,
                x_range=[-2.25, 2.25],
                color=V_COLOR,
                stroke_width=3.5,
            )

            # Panel title
            title = MathTex(lbl_str, font_size=MIN_FONT, color=INK)
            title.move_to(np.array([cx, 1.80, 0.0]))
            title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

            # Initial ball
            ball = Dot(ax.c2p(w0, w0 ** 2), radius=0.09, color=RESULT_COLOR)

            panels.append({"axes": ax, "curve": curve, "title": title, "eta": eta_val, "center_x": cx})
            balls.append(ball)
            current_w.append(w0)

            # First frame has all panel axes, curves, titles, balls
            self.add(ax, curve, title, ball)

        self.wait(1.5)

        # Run 8 steps simultaneously
        n_steps = 8
        for step in range(n_steps):
            step_anims = []
            new_w = []
            for j in range(3):
                eta_val = panels[j]["eta"]
                ax = panels[j]["axes"]
                w_prev = current_w[j]

                # Update rule for L(w) = w^2: w_next = w - eta * 2 * w
                w_raw = w_prev - eta_val * 2.0 * w_prev

                # Diverging ball clipping: stop before leaving the panel [-2.45, 2.45]
                w_clamped = np.clip(w_raw, -2.45, 2.45)
                new_w.append(w_clamped)

                p_start = ax.c2p(w_prev, min(5.3, w_prev ** 2))
                p_end = ax.c2p(w_clamped, min(5.3, w_clamped ** 2))

                # Step trace line
                trace_line = Line(p_start, p_end, color=RESULT_COLOR, stroke_width=2.0, stroke_opacity=0.6)
                self.add(trace_line)

                step_anims.append(balls[j].animate.move_to(p_end))

            current_w = new_w
            self.play(*step_anims, run_time=0.65, rate_func=smooth)
            self.wait(0.15)

        self.wait(2.5)


# =============================================================================
# SCENE 3: Descent2D
# =============================================================================
class Descent2D(Scene):
    def construct(self):
        # 1. 2D Coordinate axes
        scale = 0.85
        x_min, x_max = -4.2, 4.2
        y_min, y_max = -2.0, 2.0

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.0,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([0.0, 0.25, 0.0]))

        lbl_w1 = MathTex(r"w_1", font_size=MIN_FONT, color=INK_DIM)
        lbl_w1.next_to(axes.x_axis.get_end(), DOWN, buff=0.10)
        lbl_w1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_w2 = MathTex(r"w_2", font_size=MIN_FONT, color=INK_DIM)
        lbl_w2.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_w2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Concentric elliptical contours of L(w1, w2) = w1^2 / 2 + 4 w2^2
        levels = [0.6, 1.6, 3.2, 6.0, 9.5, 13.5]
        contours = get_bowl_contours(axes, levels, scale_x=scale, scale_y=scale)

        # Minimum at origin
        min_dot = Dot(axes.c2p(0, 0), radius=0.07, color=V_COLOR)

        # 3. Starting point (-3.5, 1.2)
        p_start = np.array([-3.5, 1.2])
        ball = Dot(axes.c2p(*p_start), radius=0.09, color=RESULT_COLOR)

        lbl_start = MathTex(r"\mathbf{w}_0", font_size=MIN_FONT, color=RESULT_COLOR)
        lbl_start.next_to(axes.c2p(*p_start), UP + LEFT, buff=0.28)
        lbl_start.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 4. Single Caption at bottom
        caption = MathTex(
            r"\text{steps follow } -\nabla L,\ \text{perpendicular to the contours}",
            font_size=MIN_FONT,
            color=RESULT_COLOR,
        )
        caption.move_to(np.array([0.0, -2.25, 0.0]))
        caption.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 5. Compute 2D gradient descent trajectory with zig-zag
        eta = 0.22
        curr = p_start.copy()
        gd_pts = [curr.copy()]
        for _ in range(10):
            # Gradient of L = w1^2/2 + 4 w2^2 is [w1, 8 w2]
            grad = np.array([curr[0], 8.0 * curr[1]])
            curr = curr - eta * grad
            gd_pts.append(curr.copy())

        # Build arrows for each step
        arrows = []
        for i in range(len(gd_pts) - 1):
            p1 = axes.c2p(*gd_pts[i])
            p2 = axes.c2p(*gd_pts[i + 1])
            arr = Arrow(
                p1, p2,
                buff=0,
                stroke_width=4.0,
                max_tip_length_to_length_ratio=0.25,
                color=RESULT_COLOR,
            )
            arrows.append(arr)

        # 6. First frame: givens immediately visible
        self.add(
            axes, lbl_w1, lbl_w2, contours, min_dot,
            ball, lbl_start, caption
        )
        self.wait(1.2)

        # 7. Animate steps one by one
        for i, arr in enumerate(arrows):
            p_next = axes.c2p(*gd_pts[i + 1])
            self.play(GrowArrow(arr), ball.animate.move_to(p_next), run_time=0.55)
            self.wait(0.12)

        self.wait(2.2)


# =============================================================================
# SCENE 4: BatchVsSGD
# =============================================================================
class BatchVsSGD(Scene):
    def construct(self):
        # 1. Coordinate axes
        scale = 1.25  # units per unit of w; window zoomed to where the paths go
        x_min, x_max = -4.3, 0.8
        y_min, y_max = -1.8, 1.8

        axes = Axes(
            x_range=[x_min, x_max, 1.0],
            y_range=[y_min, y_max, 1.0],
            x_length=(x_max - x_min) * scale,
            y_length=(y_max - y_min) * scale,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.0,
                "include_ticks": False,
            },
            tips=False,
        ).move_to(np.array([-1.43, 0.0, 0.0]))

        lbl_w1 = MathTex(r"w_1", font_size=MIN_FONT, color=INK_DIM)
        lbl_w1.next_to(axes.x_axis.get_end(), UP + LEFT, buff=0.10)
        lbl_w1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_w2 = MathTex(r"w_2", font_size=MIN_FONT, color=INK_DIM)
        lbl_w2.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)
        lbl_w2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Contours of true full-batch loss, clipped to the zoomed window
        levels = [0.6, 1.6, 3.2, 6.0, 9.5, 13.5]
        contours = get_bowl_contours(axes, levels, scale_x=scale, scale_y=scale)
        window = Rectangle(width=axes.x_length, height=axes.y_length).move_to(axes.get_center())
        contours = VGroup(*[
            Intersection(c, window, stroke_color=INK_DIM, stroke_width=1.5,
                         fill_color=V_COLOR, fill_opacity=c.get_fill_opacity())
            for c in contours
        ])
        min_dot = Dot(axes.c2p(0, 0), radius=0.07, color=V_COLOR)

        # 3. Fixed seed synthetic linear regression data: N = 64
        N = 64
        rng = np.random.default_rng(42)
        x_raw = rng.standard_normal(N)
        # Normalize so mean = 0 and var = 0.125, making Hessian [1, 0; 0, 8] with factor 8
        x_data = (x_raw - np.mean(x_raw)) / np.std(x_raw) * np.sqrt(0.125)
        noise = rng.standard_normal(N) * 0.02
        y_data = noise

        def compute_batch_grad(w, sample_indices):
            diff = w[0] * x_data[sample_indices] + w[1] - y_data[sample_indices]
            g1 = 8.0 * np.mean(diff * x_data[sample_indices])
            g2 = 8.0 * np.mean(diff)
            return np.array([g1, g2])

        # 4. Generate paths for all three optimizers from SAME start
        w_start = np.array([-3.5, 1.2])
        n_updates = 24
        eta = 0.08

        # Batch GD (all 64 points)
        w_b = w_start.copy()
        path_b = [w_b.copy()]
        for _ in range(n_updates):
            g = compute_batch_grad(w_b, np.arange(N))
            w_b = w_b - eta * g
            path_b.append(w_b.copy())

        # Mini-batch GD (16 points)
        rng_mb = np.random.default_rng(101)
        w_mb = w_start.copy()
        path_mb = [w_mb.copy()]
        for _ in range(n_updates):
            batch_idx = rng_mb.choice(N, size=16, replace=False)
            g = compute_batch_grad(w_mb, batch_idx)
            w_mb = w_mb - eta * g
            path_mb.append(w_mb.copy())

        # SGD (1 point)
        rng_sgd = np.random.default_rng(202)
        w_sgd = w_start.copy()
        path_sgd = [w_sgd.copy()]
        for _ in range(n_updates):
            idx = [rng_sgd.choice(N)]
            g = compute_batch_grad(w_sgd, idx)
            w_sgd = w_sgd - eta * g
            path_sgd.append(w_sgd.copy())

        # 5. Legend in its own column right of the map
        leg_line_b = Line(ORIGIN, RIGHT * 0.5, color=RESULT_COLOR, stroke_width=3.5)
        leg_lbl_b = MathTex(r"\text{Batch}", font_size=MIN_FONT, color=RESULT_COLOR)
        row_b = VGroup(leg_line_b, leg_lbl_b).arrange(RIGHT, buff=0.15)

        leg_line_mb = Line(ORIGIN, RIGHT * 0.5, color=W_COLOR, stroke_width=3.5)
        leg_lbl_mb = MathTex(r"\text{Mini-batch}", font_size=MIN_FONT, color=W_COLOR)
        row_mb = VGroup(leg_line_mb, leg_lbl_mb).arrange(RIGHT, buff=0.15)

        leg_line_sgd = Line(ORIGIN, RIGHT * 0.5, color=Y_COLOR, stroke_width=3.5)
        leg_lbl_sgd = MathTex(r"\text{SGD}", font_size=MIN_FONT, color=Y_COLOR)
        row_sgd = VGroup(leg_line_sgd, leg_lbl_sgd).arrange(RIGHT, buff=0.15)

        legend = VGroup(row_b, row_mb, row_sgd).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        legend.move_to(np.array([3.30, 0.25, 0.0]))
        legend.add_background_rectangle(color=BG, opacity=0.88, buff=0.12)

        # Start dot & label
        start_dot = Dot(axes.c2p(*w_start), radius=0.09, color=INK)
        lbl_w0 = MathTex(r"\mathbf{w}_0", font_size=MIN_FONT, color=INK)
        lbl_w0.next_to(axes.c2p(*w_start), LEFT, buff=0.32)
        lbl_w0.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Dynamic tracking dots for each path
        dot_b = Dot(axes.c2p(*w_start), radius=0.08, color=RESULT_COLOR)
        dot_mb = Dot(axes.c2p(*w_start), radius=0.08, color=W_COLOR)
        dot_sgd = Dot(axes.c2p(*w_start), radius=0.08, color=Y_COLOR)

        # First frame: contours, axes, start marker, legend
        self.add(axes, lbl_w1, lbl_w2, contours, min_dot, start_dot, lbl_w0, legend)
        self.wait(1.5)

        # 6. Simultaneously draw paths step by step
        for k in range(n_updates):
            p_b1 = axes.c2p(*path_b[k])
            p_b2 = axes.c2p(*path_b[k + 1])
            seg_b = Line(p_b1, p_b2, color=RESULT_COLOR, stroke_width=3.5)

            p_mb1 = axes.c2p(*path_mb[k])
            p_mb2 = axes.c2p(*path_mb[k + 1])
            seg_mb = Line(p_mb1, p_mb2, color=W_COLOR, stroke_width=3.5)

            p_sgd1 = axes.c2p(*path_sgd[k])
            p_sgd2 = axes.c2p(*path_sgd[k + 1])
            seg_sgd = Line(p_sgd1, p_sgd2, color=Y_COLOR, stroke_width=3.5)

            self.add(seg_b, seg_mb, seg_sgd)
            dot_b.move_to(p_b2)
            dot_mb.move_to(p_mb2)
            dot_sgd.move_to(p_sgd2)
            self.add(dot_b, dot_mb, dot_sgd)

            self.wait(0.25)

        self.wait(2.5)


# =============================================================================
# SCENE 5: LossCurves
# =============================================================================
class LossCurves(Scene):
    def construct(self):
        # 1. Re-generate identical data and optimization runs
        N = 64
        rng = np.random.default_rng(42)
        x_raw = rng.standard_normal(N)
        x_data = (x_raw - np.mean(x_raw)) / np.std(x_raw) * np.sqrt(0.125)
        noise = rng.standard_normal(N) * 0.02
        y_data = noise

        def full_loss(w):
            return 0.5 * w[0] ** 2 + 4.0 * w[1] ** 2

        def compute_batch_grad(w, sample_indices):
            diff = w[0] * x_data[sample_indices] + w[1] - y_data[sample_indices]
            g1 = 8.0 * np.mean(diff * x_data[sample_indices])
            g2 = 8.0 * np.mean(diff)
            return np.array([g1, g2])

        w_start = np.array([-3.5, 1.2])
        n_updates = 24
        eta = 0.08

        # Run 1: Batch GD (24 updates)
        w_b = w_start.copy()
        losses_b_updates = [full_loss(w_b)]
        for _ in range(n_updates):
            w_b -= eta * compute_batch_grad(w_b, np.arange(N))
            losses_b_updates.append(full_loss(w_b))

        # Run 2: Mini-batch GD (24 updates)
        rng_mb = np.random.default_rng(101)
        w_mb = w_start.copy()
        losses_mb_updates = [full_loss(w_mb)]
        for _ in range(n_updates):
            idx = rng_mb.choice(N, size=16, replace=False)
            w_mb -= eta * compute_batch_grad(w_mb, idx)
            losses_mb_updates.append(full_loss(w_mb))

        # Run 3: SGD (24 updates)
        rng_sgd = np.random.default_rng(202)
        w_sgd = w_start.copy()
        losses_sgd_updates = [full_loss(w_sgd)]
        for _ in range(n_updates):
            idx = [rng_sgd.choice(N)]
            w_sgd -= eta * compute_batch_grad(w_sgd, idx)
            losses_sgd_updates.append(full_loss(w_sgd))

        # -------------------------------------------------------------
        # VIEW 1: Loss vs Number of Updates
        # -------------------------------------------------------------
        axes_upd = Axes(
            x_range=[0, 24, 6],
            y_range=[0, 18, 6],
            x_length=6.4,
            y_length=2.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.0,
                "include_ticks": True,
            },
            tips=False,
        ).move_to(np.array([-0.6, -0.35, 0.0]))

        lbl_x_upd = MathTex(r"\text{Updates } (k)", font_size=MIN_FONT, color=INK_DIM)
        lbl_x_upd.next_to(axes_upd.x_axis, DOWN, buff=0.15)
        lbl_x_upd.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        lbl_y = MathTex(r"\text{Loss } L", font_size=MIN_FONT, color=INK_DIM)
        lbl_y.next_to(axes_upd.y_axis.get_end(), UP + RIGHT * 0.15, buff=0.12)
        lbl_y.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Plot curves for View 1
        curve_b_upd = axes_upd.plot_line_graph(
            x_values=list(range(n_updates + 1)),
            y_values=losses_b_updates,
            line_color=RESULT_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )
        curve_mb_upd = axes_upd.plot_line_graph(
            x_values=list(range(n_updates + 1)),
            y_values=losses_mb_updates,
            line_color=W_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )
        curve_sgd_upd = axes_upd.plot_line_graph(
            x_values=list(range(n_updates + 1)),
            y_values=losses_sgd_updates,
            line_color=Y_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )

        # Legend on the right
        leg_line_b = Line(ORIGIN, RIGHT * 0.45, color=RESULT_COLOR, stroke_width=3.5)
        leg_lbl_b = MathTex(r"\text{Batch}", font_size=MIN_FONT, color=RESULT_COLOR)
        row_b = VGroup(leg_line_b, leg_lbl_b).arrange(RIGHT, buff=0.12)

        leg_line_mb = Line(ORIGIN, RIGHT * 0.45, color=W_COLOR, stroke_width=3.5)
        leg_lbl_mb = MathTex(r"\text{Mini-batch}", font_size=MIN_FONT, color=W_COLOR)
        row_mb = VGroup(leg_line_mb, leg_lbl_mb).arrange(RIGHT, buff=0.12)

        leg_line_sgd = Line(ORIGIN, RIGHT * 0.45, color=Y_COLOR, stroke_width=3.5)
        leg_lbl_sgd = MathTex(r"\text{SGD}", font_size=MIN_FONT, color=Y_COLOR)
        row_sgd = VGroup(leg_line_sgd, leg_lbl_sgd).arrange(RIGHT, buff=0.12)

        legend = VGroup(row_b, row_mb, row_sgd).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        legend.move_to(np.array([3.45, 0.45, 0.0]))
        legend.add_background_rectangle(color=BG, opacity=0.88, buff=0.10)

        # Caption 1 at the top
        caption1 = MathTex(r"\text{per update: batch GD takes optimal steps}", font_size=MIN_FONT, color=RESULT_COLOR)
        caption1.move_to(np.array([0.0, 2.40, 0.0]))
        caption1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # First frame shows View 1 givens
        self.add(
            axes_upd, lbl_x_upd, lbl_y,
            curve_b_upd, curve_mb_upd, curve_sgd_upd,
            legend, caption1
        )
        self.wait(3.5)

        # -------------------------------------------------------------
        # VIEW 2: Loss vs Data Points Processed (Computation / Epochs)
        # -------------------------------------------------------------
        # Data points processed across 4 epochs (256 points total)
        # Batch: 4 updates (points 0, 64, 128, 192, 256)
        w_b_ep = w_start.copy()
        pts_b = [0]
        losses_b_ep = [full_loss(w_b_ep)]
        for s in range(4):
            w_b_ep -= eta * compute_batch_grad(w_b_ep, np.arange(N))
            pts_b.append((s + 1) * 64)
            losses_b_ep.append(full_loss(w_b_ep))

        # Mini-batch: 16 updates (points 0, 16, 32, ..., 256)
        rng_mb2 = np.random.default_rng(101)
        w_mb_ep = w_start.copy()
        pts_mb = [0]
        losses_mb_ep = [full_loss(w_mb_ep)]
        for s in range(16):
            idx = rng_mb2.choice(N, size=16, replace=False)
            w_mb_ep -= eta * compute_batch_grad(w_mb_ep, idx)
            pts_mb.append((s + 1) * 16)
            losses_mb_ep.append(full_loss(w_mb_ep))

        # SGD: 256 updates (evaluated every 4 points)
        rng_sgd2 = np.random.default_rng(202)
        w_sgd_ep = w_start.copy()
        pts_sgd = [0]
        losses_sgd_ep = [full_loss(w_sgd_ep)]
        for s in range(256):
            idx = [rng_sgd2.choice(N)]
            w_sgd_ep -= eta * compute_batch_grad(w_sgd_ep, idx)
            if (s + 1) % 4 == 0 or s < 16:
                pts_sgd.append(s + 1)
                losses_sgd_ep.append(full_loss(w_sgd_ep))

        axes_ep = Axes(
            x_range=[0, 256, 64],
            y_range=[0, 18, 6],
            x_length=6.4,
            y_length=2.8,
            axis_config={
                "stroke_color": INK_DIM,
                "stroke_width": 2.0,
                "include_ticks": True,
            },
            tips=False,
        ).move_to(np.array([-0.6, -0.35, 0.0]))

        lbl_x_ep = MathTex(r"\text{Data points processed (epochs)}", font_size=MIN_FONT, color=INK_DIM)
        lbl_x_ep.next_to(axes_ep.x_axis, DOWN, buff=0.15)
        lbl_x_ep.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        curve_b_ep = axes_ep.plot_line_graph(
            x_values=pts_b,
            y_values=losses_b_ep,
            line_color=RESULT_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )
        curve_mb_ep = axes_ep.plot_line_graph(
            x_values=pts_mb,
            y_values=losses_mb_ep,
            line_color=W_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )
        curve_sgd_ep = axes_ep.plot_line_graph(
            x_values=pts_sgd,
            y_values=losses_sgd_ep,
            line_color=Y_COLOR,
            add_vertex_dots=False,
            stroke_width=3.5,
        )

        caption2 = MathTex(r"\text{per data point: SGD converges much faster}", font_size=MIN_FONT, color=RESULT_COLOR)
        caption2.move_to(np.array([0.0, 2.40, 0.0]))
        caption2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Transition from View 1 to View 2
        self.play(FadeOut(caption1), FadeOut(lbl_x_upd), run_time=0.4)
        self.play(
            FadeIn(caption2),
            FadeIn(lbl_x_ep),
            ReplacementTransform(axes_upd, axes_ep),
            ReplacementTransform(curve_b_upd, curve_b_ep),
            ReplacementTransform(curve_mb_upd, curve_mb_ep),
            ReplacementTransform(curve_sgd_upd, curve_sgd_ep),
            run_time=1.8,
        )
        self.wait(4.0)
