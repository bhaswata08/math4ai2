# Adapted from 3b1b/videos _2017/nn/part3.py, (c) 3Blue1Brown, CC BY-NC-SA 4.0

from shared.anim.house import *
import numpy as np


class TinyNetwork(Scene):
    def construct(self):
        # 1. Title at top
        title = MathTex(
            r"\text{The simplest network: one neuron per layer}",
            font_size=MIN_FONT,
            color=INK,
        ).move_to(UP * 2.35)
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. 4 Neurons horizontally across upper half (y = 1.15)
        r = 0.32
        p0 = np.array([-3.75, 1.15, 0])
        p1 = np.array([-1.90, 1.15, 0])
        p2 = np.array([-0.05, 1.15, 0])
        p3 = np.array([1.80, 1.15, 0])

        neuron_0 = Circle(radius=r, color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p0)
        neuron_1 = Circle(radius=r, color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p1)
        neuron_2 = Circle(radius=r, color=INK, stroke_width=3.0, fill_color=BG, fill_opacity=1.0).move_to(p2)
        neuron_3 = Circle(radius=r, color=INK, stroke_width=3.0, fill_color=BG, fill_opacity=1.0).move_to(p3)

        lbl_a0 = MathTex(r"a^{(0)}", font_size=MIN_FONT, color=INK_DIM).next_to(neuron_0, UP, buff=0.14)
        lbl_a1 = MathTex(r"a^{(1)}", font_size=MIN_FONT, color=INK_DIM).next_to(neuron_1, UP, buff=0.14)
        lbl_a2 = MathTex(r"a^{(L-1)}", font_size=MIN_FONT, color=V_COLOR).next_to(neuron_2, UP, buff=0.14)
        lbl_a3 = MathTex(r"a^{(L)}", font_size=MIN_FONT, color=V_COLOR).next_to(neuron_3, UP, buff=0.14)

        # Edges between neurons
        edge_0 = Arrow(neuron_0.get_right(), neuron_1.get_left(), buff=0.08, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        edge_1 = Arrow(neuron_1.get_right(), neuron_2.get_left(), buff=0.08, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        edge_2 = Arrow(neuron_2.get_right(), neuron_3.get_left(), buff=0.08, color=V_COLOR, stroke_width=3.5, max_tip_length_to_length_ratio=0.22)

        lbl_w1 = MathTex(r"w^{(1)}", font_size=MIN_FONT, color=INK_DIM).next_to(edge_0, DOWN, buff=0.12)
        lbl_w1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        lbl_w2 = MathTex(r"w^{(2)}", font_size=MIN_FONT, color=INK_DIM).next_to(edge_1, DOWN, buff=0.12)
        lbl_w2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        lbl_wL = MathTex(r"w^{(L)}", font_size=MIN_FONT, color=V_COLOR).next_to(edge_2, DOWN, buff=0.12)
        lbl_wL.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Cost and Target on the right
        cost_box = RoundedRectangle(corner_radius=0.1, width=1.25, height=0.65, color=RESULT_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([3.65, 1.15, 0]))
        cost_txt = MathTex(r"C", font_size=MIN_FONT, color=RESULT_COLOR).move_to(cost_box.get_center())

        arrow_a_to_c = Arrow(neuron_3.get_right(), cost_box.get_left(), buff=0.08, color=RESULT_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)

        y_box = RoundedRectangle(corner_radius=0.1, width=1.05, height=0.58, color=V_COLOR, stroke_width=2.2, fill_color=BG, fill_opacity=1.0).move_to(np.array([3.65, 0.05, 0]))
        y_txt = MathTex(r"y", font_size=MIN_FONT, color=V_COLOR).move_to(y_box.get_center())

        arrow_y_to_c = Arrow(y_box.get_top(), cost_box.get_bottom(), buff=0.08, color=INK_DIM, stroke_width=2.2, max_tip_length_to_length_ratio=0.25)

        early_group = VGroup(neuron_0, neuron_1, edge_0, edge_1, lbl_a0, lbl_a1, lbl_w1, lbl_w2)
        last_group = VGroup(neuron_2, neuron_3, edge_2, lbl_a2, lbl_a3, lbl_wL, cost_box, cost_txt, arrow_a_to_c, y_box, y_txt, arrow_y_to_c)

        # Frame 0 must show givens (never open on empty frame)
        self.add(title, early_group, last_group)
        self.wait(1.5)

        # 3. Dim early layers, focus just on last two layers
        self.play(
            early_group.animate.set_opacity(0.18),
            run_time=1.2,
        )
        self.wait(0.8)

        # 4. Introduce bias b^{(L)} feeding into Neuron 3 from below
        bias_arrow = Arrow(
            np.array([1.80, 0.22, 0]), np.array([1.80, 0.75, 0]),
            buff=0.05, color=V_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.25,
        )
        bias_lbl = MathTex(r"+ b^{(L)}", font_size=MIN_FONT, color=V_COLOR).next_to(bias_arrow, DOWN, buff=0.08)
        bias_lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(bias_arrow), FadeIn(bias_lbl), run_time=1.0)
        self.wait(0.8)

        # 5. Formulas for the last link in a single row below (y = -1.45)
        eq_z = MathTex(
            r"z^{(L)}", r"=", r"w^{(L)}", r"a^{(L-1)}", r"+", r"b^{(L)}",
            font_size=MIN_FONT,
        )
        eq_z[0].set_color(INK)
        eq_z[2].set_color(V_COLOR)
        eq_z[3].set_color(V_COLOR)
        eq_z[5].set_color(V_COLOR)

        eq_a = MathTex(
            r"a^{(L)}", r"=", r"\sigma(", r"z^{(L)}", r")",
            font_size=MIN_FONT,
        )
        eq_a[0].set_color(V_COLOR)
        eq_a[3].set_color(INK)

        eq_c = MathTex(
            r"C", r"=", r"(", r"a^{(L)}", r"-", r"y", r")^2",
            font_size=MIN_FONT,
        )
        eq_c[0].set_color(RESULT_COLOR)
        eq_c[3].set_color(V_COLOR)
        eq_c[5].set_color(V_COLOR)

        box_c_formula = SurroundingRectangle(eq_c, color=RESULT_COLOR, buff=0.12, stroke_width=2)
        group_c = VGroup(eq_c, box_c_formula)

        VGroup(eq_z, eq_a).arrange(RIGHT, buff=0.7).move_to(np.array([0.0, -1.0, 0]))
        group_c.move_to(np.array([0.0, -2.0, 0]))
        eq_c.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Write(eq_z), run_time=1.2)
        self.wait(0.6)
        self.play(Write(eq_a), run_time=1.2)
        self.wait(0.6)
        self.play(Write(eq_c), FadeIn(box_c_formula), run_time=1.4)
        self.wait(3.0)


class DependencyTree(Scene):
    def construct(self):
        # 1. Title
        title = MathTex(
            r"\text{Dependency tree: how a nudge ripples to the cost}",
            font_size=MIN_FONT,
            color=INK,
        ).move_to(UP * 2.35)
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Main path nodes across y = 0.50
        box_w = RoundedRectangle(corner_radius=0.1, width=1.35, height=0.62, stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([-3.6, 0.50, 0]))
        txt_w = MathTex(r"w^{(L)}", font_size=MIN_FONT, color=V_COLOR).move_to(box_w.get_center())

        box_z = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.62, stroke_color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([-1.2, 0.50, 0]))
        txt_z = MathTex(r"z^{(L)}", font_size=MIN_FONT, color=INK).move_to(box_z.get_center())

        box_a = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.62, stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([1.2, 0.50, 0]))
        txt_a = MathTex(r"a^{(L)}", font_size=MIN_FONT, color=V_COLOR).move_to(box_a.get_center())

        box_c = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.62, stroke_color=RESULT_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([3.6, 0.50, 0]))
        txt_c = MathTex(r"C", font_size=MIN_FONT, color=RESULT_COLOR).move_to(box_c.get_center())

        # Auxiliary inputs below:
        box_a_prev = RoundedRectangle(corner_radius=0.1, width=1.35, height=0.62, stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([-3.6, -0.65, 0]))
        txt_a_prev = MathTex(r"a^{(L-1)}", font_size=MIN_FONT, color=V_COLOR).move_to(box_a_prev.get_center())

        box_b = RoundedRectangle(corner_radius=0.1, width=1.35, height=0.62, stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([-1.2, -0.75, 0]))
        txt_b = MathTex(r"b^{(L)}", font_size=MIN_FONT, color=V_COLOR).move_to(box_b.get_center())

        box_y = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.62, stroke_color=V_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(np.array([3.6, -0.65, 0]))
        txt_y = MathTex(r"y", font_size=MIN_FONT, color=V_COLOR).move_to(box_y.get_center())

        # Arrows connecting the nodes
        arr_w_z = Arrow(box_w.get_right(), box_z.get_left(), buff=0.1, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr_ap_z = Arrow(box_a_prev.get_right(), box_z.get_bottom(), buff=0.1, color=INK_DIM, stroke_width=2.2, max_tip_length_to_length_ratio=0.2)
        arr_b_z = Arrow(box_b.get_top(), box_z.get_bottom(), buff=0.1, color=INK_DIM, stroke_width=2.2, max_tip_length_to_length_ratio=0.25)
        arr_z_a = Arrow(box_z.get_right(), box_a.get_left(), buff=0.1, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr_a_c = Arrow(box_a.get_right(), box_c.get_left(), buff=0.1, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
        arr_y_c = Arrow(box_y.get_top(), box_c.get_bottom(), buff=0.1, color=INK_DIM, stroke_width=2.2, max_tip_length_to_length_ratio=0.25)

        tree_mobs = VGroup(
            box_w, txt_w, box_a_prev, txt_a_prev, box_b, txt_b,
            box_z, txt_z, box_a, txt_a, box_c, txt_c, box_y, txt_y,
            arr_w_z, arr_ap_z, arr_b_z, arr_z_a, arr_a_c, arr_y_c,
        )

        # Frame 0 setup
        tree_mobs.shift(DOWN * 0.3)
        self.add(title, tree_mobs)
        self.wait(1.5)

        # 3. Nudge dw on w^{(L)}
        flash_w = SurroundingRectangle(box_w, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        nudge_w = MathTex(r"dw", font_size=MIN_FONT, color=X_COLOR).next_to(box_w, UP, buff=0.14)
        nudge_w.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(flash_w), FadeIn(nudge_w), run_time=0.6)
        self.play(FadeOut(flash_w), run_time=0.4)
        self.wait(0.4)

        # 4. Propagate w -> z:
        # Local factor ABOVE arrow: \frac{\partial z^{(L)}}{\partial w^{(L)}}
        lbl_f1 = MathTex(r"\frac{\partial z^{(L)}}{\partial w^{(L)}}", font_size=MIN_FONT + 2, color=X_COLOR)
        lbl_f1.next_to(arr_w_z, UP, buff=0.55)
        lbl_f1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        nudge_z = MathTex(r"dz", font_size=MIN_FONT, color=X_COLOR).next_to(box_z, UP, buff=0.14)
        nudge_z.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        flash_z = SurroundingRectangle(box_z, color=HIGHLIGHT, buff=0.08, stroke_width=3)

        self.play(
            arr_w_z.animate.set_color(X_COLOR).set_stroke(width=4),
            FadeIn(lbl_f1),
            run_time=1.0,
        )
        self.play(Create(flash_z), FadeIn(nudge_z), run_time=0.5)
        self.play(FadeOut(flash_z), run_time=0.3)
        self.wait(0.6)

        # 5. Propagate z -> a:
        # Local factor ABOVE arrow: \frac{\partial a^{(L)}}{\partial z^{(L)}}
        lbl_f2 = MathTex(r"\frac{\partial a^{(L)}}{\partial z^{(L)}}", font_size=MIN_FONT + 2, color=W_COLOR)
        lbl_f2.next_to(arr_z_a, UP, buff=0.55)
        lbl_f2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        nudge_a = MathTex(r"da", font_size=MIN_FONT, color=W_COLOR).next_to(box_a, UP, buff=0.14)
        nudge_a.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        flash_a = SurroundingRectangle(box_a, color=HIGHLIGHT, buff=0.08, stroke_width=3)

        self.play(
            arr_z_a.animate.set_color(W_COLOR).set_stroke(width=4),
            FadeIn(lbl_f2),
            run_time=1.0,
        )
        self.play(Create(flash_a), FadeIn(nudge_a), run_time=0.5)
        self.play(FadeOut(flash_a), run_time=0.3)
        self.wait(0.6)

        # 6. Propagate a -> C:
        # Local factor ABOVE arrow: \frac{\partial C}{\partial a^{(L)}}
        lbl_f3 = MathTex(r"\frac{\partial C}{\partial a^{(L)}}", font_size=MIN_FONT + 2, color=Y_COLOR)
        lbl_f3.next_to(arr_a_c, UP, buff=0.55)
        lbl_f3.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        nudge_c = MathTex(r"dC", font_size=MIN_FONT, color=RESULT_COLOR).next_to(box_c, UP, buff=0.14)
        nudge_c.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        flash_c = SurroundingRectangle(box_c, color=HIGHLIGHT, buff=0.08, stroke_width=3)

        self.play(
            arr_a_c.animate.set_color(Y_COLOR).set_stroke(width=4),
            FadeIn(lbl_f3),
            run_time=1.0,
        )
        self.play(Create(flash_c), FadeIn(nudge_c), run_time=0.5)
        self.play(FadeOut(flash_c), run_time=0.3)
        self.wait(0.6)

        # 7. Summary chain flow at bottom
        flow_summary = MathTex(
            r"dw", r"\;\longrightarrow\;",
            r"dz", r"\;\longrightarrow\;",
            r"da", r"\;\longrightarrow\;",
            r"dC",
            font_size=MIN_FONT + 2,
        )
        flow_summary[0].set_color(X_COLOR)
        flow_summary[1].set_color(INK_DIM)
        flow_summary[2].set_color(X_COLOR)
        flow_summary[3].set_color(INK_DIM)
        flow_summary[4].set_color(W_COLOR)
        flow_summary[5].set_color(INK_DIM)
        flow_summary[6].set_color(RESULT_COLOR)
        flow_summary.move_to(np.array([0.0, -2.15, 0]))
        flow_summary.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        flow_box = SurroundingRectangle(flow_summary, color=RESULT_COLOR, buff=0.12, stroke_width=2)

        self.play(Write(flow_summary), FadeIn(flow_box), run_time=1.4)
        self.wait(3.0)


class ChainRuleProduct(Scene):
    def construct(self):
        # 1. Title
        title = MathTex(
            r"\text{Chain rule: multiplying three local factors}",
            font_size=MIN_FONT,
            color=INK,
        ).move_to(UP * 2.35)
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Main chain rule equation with generous spacing between factors
        chain_eq = MathTex(
            r"\frac{\partial C}{\partial w^{(L)}}",  # 0
            r"=",                                    # 1
            r"\frac{\partial z^{(L)}}{\partial w^{(L)}}",  # 2
            r"\quad\cdot\quad",                      # 3
            r"\frac{\partial a^{(L)}}{\partial z^{(L)}}",  # 4
            r"\quad\cdot\quad",                      # 5
            r"\frac{\partial C}{\partial a^{(L)}}",  # 6
            font_size=MIN_FONT + 2,
        )
        chain_eq[0].set_color(RESULT_COLOR)
        chain_eq[1].set_color(INK)
        chain_eq[2].set_color(X_COLOR)
        chain_eq[3].set_color(INK)
        chain_eq[4].set_color(W_COLOR)
        chain_eq[5].set_color(INK)
        chain_eq[6].set_color(Y_COLOR)
        chain_eq.move_to(np.array([0.0, 1.35, 0]))
        chain_eq.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0 setup
        self.add(title, chain_eq)
        self.wait(1.5)

        # Coordinates under each factor
        x1 = chain_eq[2].get_x()
        x2 = chain_eq[4].get_x()
        x3 = chain_eq[6].get_x()

        # 3. Factor 1: evaluate dz/dw = a^{(L-1)}
        arr1 = Arrow(np.array([x1, 0.85, 0]), np.array([x1, 0.35, 0]), buff=0.05, color=X_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        eval_f1 = MathTex(r"a^{(L-1)}", font_size=MIN_FONT + 2, color=X_COLOR).move_to(np.array([x1, -0.05, 0]))
        eval_f1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(arr1), run_time=0.8)
        self.play(FadeIn(eval_f1, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.6)

        # 4. Factor 2: evaluate da/dz = \sigma'(z^{(L)})
        arr2 = Arrow(np.array([x2, 0.85, 0]), np.array([x2, 0.35, 0]), buff=0.05, color=W_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        eval_f2 = MathTex(r"\sigma'(z^{(L)})", font_size=MIN_FONT + 2, color=W_COLOR).move_to(np.array([x2, -0.05, 0]))
        eval_f2.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(arr2), run_time=0.8)
        self.play(FadeIn(eval_f2, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.6)

        # 5. Factor 3: evaluate dC/da = 2(a^{(L)} - y)
        arr3 = Arrow(np.array([x3, 0.85, 0]), np.array([x3, 0.35, 0]), buff=0.05, color=Y_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
        eval_f3 = MathTex(r"2(a^{(L)} - y)", font_size=MIN_FONT + 2, color=Y_COLOR).move_to(np.array([x3, -0.05, 0]))
        eval_f3.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        self.play(Create(arr3), run_time=0.8)
        self.play(FadeIn(eval_f3, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.8)

        # 6. Gather evaluated factors into the final product formula at y = -1.45
        final_eq = MathTex(
            r"\frac{\partial C}{\partial w^{(L)}}",  # 0
            r"=",                                    # 1
            r"a^{(L-1)}",                            # 2
            r"\cdot",                                # 3
            r"\sigma'(z^{(L)})",                     # 4
            r"\cdot",                                # 5
            r"2(a^{(L)} - y)",                       # 6
            font_size=MIN_FONT + 2,
        )
        final_eq[0].set_color(RESULT_COLOR)
        final_eq[1].set_color(INK)
        final_eq[2].set_color(X_COLOR)
        final_eq[3].set_color(INK)
        final_eq[4].set_color(W_COLOR)
        final_eq[5].set_color(INK)
        final_eq[6].set_color(Y_COLOR)
        final_eq.move_to(np.array([0.0, -1.85, 0]))
        final_eq.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        final_box = SurroundingRectangle(final_eq, color=RESULT_COLOR, buff=0.14, stroke_width=2.5)

        self.play(
            Write(final_eq),
            run_time=1.4,
        )
        self.play(FadeIn(final_box), run_time=0.6)
        self.wait(3.0)


class GoDeeper(Scene):
    def construct(self):
        # 1. Title
        title = MathTex(
            r"\text{The backward pass: reusing factors one layer back}",
            font_size=MIN_FONT,
            color=INK,
        ).move_to(UP * 2.35)
        title.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # 2. Chain of neurons at y = 1.05
        r = 0.32
        p_l2 = np.array([-3.45, 1.05, 0])
        p_l1 = np.array([-1.15, 1.05, 0])
        p_l = np.array([1.15, 1.05, 0])
        p_c = np.array([3.45, 1.05, 0])

        neuron_l2 = Circle(radius=r, color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p_l2)
        neuron_l1 = Circle(radius=r, color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p_l1)
        neuron_l = Circle(radius=r, color=INK_DIM, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p_l)

        box_c = RoundedRectangle(corner_radius=0.1, width=1.1, height=0.65, color=RESULT_COLOR, stroke_width=2.5, fill_color=BG, fill_opacity=1.0).move_to(p_c)
        txt_c = MathTex(r"C", font_size=MIN_FONT, color=RESULT_COLOR).move_to(box_c.get_center())

        lbl_l2 = MathTex(r"a^{(L-2)}", font_size=MIN_FONT, color=INK_DIM).next_to(neuron_l2, UP, buff=0.12)
        lbl_l1 = MathTex(r"a^{(L-1)}", font_size=MIN_FONT, color=V_COLOR).next_to(neuron_l1, UP, buff=0.12)
        lbl_l = MathTex(r"a^{(L)}", font_size=MIN_FONT, color=V_COLOR).next_to(neuron_l, UP, buff=0.12)

        arr_fwd_1 = Arrow(neuron_l2.get_right(), neuron_l1.get_left(), buff=0.08, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        arr_fwd_2 = Arrow(neuron_l1.get_right(), neuron_l.get_left(), buff=0.08, color=INK_DIM, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)
        arr_fwd_3 = Arrow(neuron_l.get_right(), box_c.get_left(), buff=0.08, color=RESULT_COLOR, stroke_width=2.5, max_tip_length_to_length_ratio=0.22)

        lbl_wl1 = MathTex(r"w^{(L-1)}", font_size=MIN_FONT, color=V_COLOR).next_to(arr_fwd_1, DOWN, buff=0.1)
        lbl_wl1.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)
        lbl_wl = MathTex(r"w^{(L)}", font_size=MIN_FONT, color=V_COLOR).next_to(arr_fwd_2, DOWN, buff=0.1)
        lbl_wl.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        network_group = VGroup(
            neuron_l2, neuron_l1, neuron_l, box_c, txt_c,
            lbl_l2, lbl_l1, lbl_l,
            arr_fwd_1, arr_fwd_2, arr_fwd_3,
            lbl_wl1, lbl_wl,
        )

        # 3. Middle formula at y = -0.15: sensitivity wrt previous activation
        eq_prev_a = MathTex(
            r"\frac{\partial C}{\partial a^{(L-1)}}",  # 0
            r"=",                                      # 1
            r"w^{(L)}",                                # 2
            r"\cdot",                                  # 3
            r"\sigma'(z^{(L)})",                       # 4
            r"\cdot",                                  # 5
            r"2(a^{(L)} - y)",                         # 6
            font_size=MIN_FONT + 2,
        )
        eq_prev_a[0].set_color(RESULT_COLOR)
        eq_prev_a[1].set_color(INK)
        eq_prev_a[2].set_color(V_COLOR)
        eq_prev_a[3].set_color(INK)
        eq_prev_a[4].set_color(W_COLOR)
        eq_prev_a[5].set_color(INK)
        eq_prev_a[6].set_color(Y_COLOR)
        eq_prev_a.move_to(np.array([0.0, -0.6, 0]))
        eq_prev_a.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        # Frame 0 setup
        self.add(title, network_group, eq_prev_a)
        self.wait(1.5)

        # 4. Highlight the reused factors from layer L: \sigma'(z^{(L)}) \cdot 2(a^{(L)} - y)
        reused_group = VGroup(eq_prev_a[4], eq_prev_a[5], eq_prev_a[6])
        reused_brace = Brace(reused_group, DOWN, buff=0.1, color=HIGHLIGHT)
        reused_lbl = MathTex(
            r"\text{reused from layer } L",
            font_size=MIN_FONT,
            color=HIGHLIGHT,
        ).next_to(reused_brace, DOWN, buff=0.12)

        self.play(Create(reused_brace), FadeIn(reused_lbl), run_time=1.2)
        self.wait(1.2)

        # 5. Travelling backward sweep highlight (right -> left)
        # Curved highlight pulses sweeping backwards: C -> a^{(L)} -> a^{(L-1)} -> a^{(L-2)}
        flash_c = SurroundingRectangle(box_c, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(flash_c), run_time=0.35)
        self.play(FadeOut(flash_c), run_time=0.25)

        pulse_c_to_l = Arrow(box_c.get_left(), neuron_l.get_right(), buff=0.08, color=HIGHLIGHT, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        flash_l = SurroundingRectangle(neuron_l, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(pulse_c_to_l), run_time=0.4)
        self.play(Create(flash_l), FadeOut(pulse_c_to_l), run_time=0.35)
        self.play(FadeOut(flash_l), run_time=0.25)

        pulse_l_to_l1 = Arrow(neuron_l.get_left(), neuron_l1.get_right(), buff=0.08, color=HIGHLIGHT, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        flash_l1 = SurroundingRectangle(neuron_l1, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(pulse_l_to_l1), run_time=0.4)
        self.play(Create(flash_l1), FadeOut(pulse_l_to_l1), run_time=0.35)
        self.play(FadeOut(flash_l1), run_time=0.25)

        pulse_l1_to_l2 = Arrow(neuron_l1.get_left(), neuron_l2.get_right(), buff=0.08, color=HIGHLIGHT, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        flash_l2 = SurroundingRectangle(neuron_l2, color=HIGHLIGHT, buff=0.08, stroke_width=3)
        self.play(Create(pulse_l1_to_l2), run_time=0.4)
        self.play(Create(flash_l2), FadeOut(pulse_l1_to_l2), run_time=0.35)
        self.play(FadeOut(flash_l2), run_time=0.25)
        self.wait(0.6)

        # 6. Apply to layer L-1's weights: the recursive chain rule
        self.play(FadeOut(reused_brace), FadeOut(reused_lbl), FadeOut(eq_prev_a), run_time=0.6)

        eq_prev_w = MathTex(
            r"\frac{\partial C}{\partial w^{(L-1)}}",  # 0
            r"=",                                      # 1
            r"a^{(L-2)}",                              # 2
            r"\cdot",                                  # 3
            r"\sigma'(z^{(L-1)})",                     # 4
            r"\cdot",                                  # 5
            r"\frac{\partial C}{\partial a^{(L-1)}}",  # 6
            font_size=MIN_FONT + 2,
        )
        eq_prev_w[0].set_color(RESULT_COLOR)
        eq_prev_w[1].set_color(INK)
        eq_prev_w[2].set_color(X_COLOR)
        eq_prev_w[3].set_color(INK)
        eq_prev_w[4].set_color(W_COLOR)
        eq_prev_w[5].set_color(INK)
        eq_prev_w[6].set_color(RESULT_COLOR)
        eq_prev_w.move_to(np.array([0.0, -1.5, 0]))
        eq_prev_w.add_background_rectangle(color=BG, opacity=0.85, buff=0.08)

        box_final = SurroundingRectangle(eq_prev_w, color=RESULT_COLOR, buff=0.14, stroke_width=2.5)

        self.play(Write(eq_prev_w), run_time=1.4)
        self.play(FadeIn(box_final), run_time=0.6)
        self.wait(3.0)
