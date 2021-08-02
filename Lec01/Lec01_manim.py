from manimlib import *
import numpy as np


class KinEnApprox(Scene):
    def construct(self):
        axes = Axes(
            (0, 2, 0.5),
            (0, 3, 0.5),
            )
        axes.add_coordinate_labels(
            font_size=26,
            y_values=[1, 2],
            num_decimal_places=1,
        )
        axes.add(Tex('v').shift(6.5*RIGHT+2.5*DOWN))
        axes.add(Tex('T(v)').shift(6.5*LEFT+3.5*UP))
        axes.add(Tex('c', color=RED).shift(2.6*DOWN+0.5*RIGHT))
        # axes.align_to(, direction=RIGHT)
        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        ekin_rel_graph = axes.get_graph(
            lambda x: 1.0/np.sqrt(1.0-np.power(x, 2))-1.0 if x < 1.0 else 10.0,
            color=GREEN,
            x_range=(0.0, 1.0, 0.001)
        )
        ekin_classic_graph = axes.get_graph(
            lambda x: np.power(x, 2)/2,
            color=BLUE,
        )
        ekin_approx_graph1 = axes.get_graph(
            lambda x: np.power(x, 2)/2,
            color=YELLOW,
        )
        ekin_approx_graph2 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4),
            color=YELLOW,
        )
        ekin_approx_graph3 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6),
            color=YELLOW,
        )
        ekin_approx_graph4 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8),
            color=YELLOW,
        )
        ekin_approx_graph5 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10),
            color=YELLOW,
        )
        ekin_approx_graph6 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10) + 231/1024*np.power(x, 12),
            color=YELLOW,
        )
        ekin_approx_graph7 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10) + 231/1024*np.power(x, 12)
            + 429/2048*np.power(x, 14),
            color=YELLOW,
        )
        ekin_approx_graph8 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10) + 231/1024*np.power(x, 12)
            + 429/2048*np.power(x, 14) + 6435/32768*np.power(x, 16),
            color=YELLOW,
        )
        ekin_approx_graph9 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10) + 231/1024*np.power(x, 12)
            + 429/2048*np.power(x, 14) + 6435/32768*np.power(x, 16)
            + 12155/65536*np.power(x, 18),
            color=YELLOW,
        )
        ekin_approx_graph10 = axes.get_graph(
            lambda x: np.power(x, 2)/2 + 3/8*np.power(x, 4)
            + 5/16*np.power(x, 6) + 35/128*np.power(x, 8)
            + 63/256*np.power(x, 10) + 231/1024*np.power(x, 12)
            + 429/2048*np.power(x, 14) + 6435/32768*np.power(x, 16)
            + 12155/65536*np.power(x, 18) + 46189/262144*np.power(x, 20),
            color=YELLOW,
        )
        ekin_approx_graph = [
            ekin_approx_graph1,
            ekin_approx_graph2,
            ekin_approx_graph3,
            ekin_approx_graph4,
            ekin_approx_graph5,
            ekin_approx_graph6,
            ekin_approx_graph7,
            ekin_approx_graph8,
            ekin_approx_graph9,
            ekin_approx_graph10
        ]

        edge_graph = axes.get_v_line(
            axes.input_to_graph_point(1, ekin_rel_graph),
            color=RED)

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        # ekin_rel_label = axes.get_graph_label(ekin_rel_graph, "\\sin(x)")
        ekin_rel_label = axes.get_graph_label(
            ekin_rel_graph,
            "m_0c^2\\left(\\frac{1}{\\sqrt{1-\\frac{v^2}{c^2}}} - 1\\right)",
            x=0.9)
        ekin_classic_label = axes.get_graph_label(
            ekin_classic_graph, "\\frac{1}{2}m_0v^2", x=1.5)
        ekin_approx_label = []

        for i in range(10):
            ekin_approx_label.append(
                axes.get_graph_label(
                    ekin_approx_graph[i],
                    Text(
                        f"Approximation {i+1}",
                        color=YELLOW,
                        size=28),
                    x=0.5, color=YELLOW))

        self.play(
            ShowCreation(ekin_rel_graph),
            FadeIn(ekin_rel_label)
        )
        self.play(
            ShowCreation(ekin_classic_graph),
            FadeIn(ekin_classic_label)
        )
        self.play(
            ShowCreation(edge_graph),
        )
        self.wait(5)
        self.play(
            ShowCreation(ekin_approx_graph1),
            FadeIn(ekin_approx_label[0])
        )

        for i in range(9):
            self.wait(2)
            self.play(
                ReplacementTransform(
                    ekin_approx_graph[i], ekin_approx_graph[i+1]),
                FadeTransform(
                    ekin_approx_label[i], ekin_approx_label[i+1]),
            )
        self.wait(5)
