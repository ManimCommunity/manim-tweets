from manim import *


class HamiltonianCycle(Scene):
    def construct(self):
        dots = [Dot(z_index=30) for _ in range(20)]
        for ind, dot in enumerate(dots[:5]):
            dot.move_to(
                3.75
                * (
                    np.cos(ind / 5 * TAU + TAU / 4) * RIGHT
                    + np.sin(ind / 5 * TAU + TAU / 4) * UP
                )
            )
        for ind, dot in enumerate(dots[5:10]):
            dot.move_to(
                2.75
                * (
                    np.cos(ind / 5 * TAU + TAU / 4) * RIGHT
                    + np.sin(ind / 5 * TAU + TAU / 4) * UP
                )
            )
        for ind, dot in enumerate(dots[10:15]):
            dot.move_to(
                1.5
                * (
                    np.cos(ind / 5 * TAU - TAU / 4) * RIGHT
                    + np.sin(ind / 5 * TAU - TAU / 4) * UP
                )
            )
        for ind, dot in enumerate(dots[15:]):
            dot.move_to(
                0.75
                * (
                    np.cos(ind / 5 * TAU - TAU / 4) * RIGHT
                    + np.sin(ind / 5 * TAU - TAU / 4) * UP
                )
            )
        lines = (
            [
                Line(dots[k].get_center(), dots[(k + 1) % 5].get_center())
                for k in range(5)
            ]
            + [Line(dots[k].get_center(), dots[5 + k].get_center()) for k in range(5)]
            + [
                Line(dots[5 + k].get_center(), dots[10 + (k + 2) % 5].get_center())
                for k in range(5)
            ]
            + [
                Line(dots[5 + k].get_center(), dots[10 + (k + 3) % 5].get_center())
                for k in range(5)
            ]
            + [
                Line(dots[10 + k].get_center(), dots[15 + k].get_center())
                for k in range(5)
            ]
            + [
                Line(dots[15 + k].get_center(), dots[15 + (k + 1) % 5].get_center())
                for k in range(5)
            ]
        )
        vgroup = VGroup(*lines, *dots)
        vgroup.move_to(ORIGIN)
        self.play(*[ShowCreation(dot) for dot in dots])
        self.play(*[ShowCreation(line) for line in lines])
        self.wait(1)
        cycle_ind = [
            0,
            1,
            2,
            7,
            14,
            6,
            13,
            5,
            12,
            9,
            11,
            16,
            17,
            18,
            19,
            15,
            10,
            8,
            3,
            4,
        ]
        cycle_lines = []
        for k in range(len(cycle_ind)):
            self.play(
                dots[cycle_ind[k]].animate.set_color(RED),
                run_time=0.3,
                rate_function=linear,
            )
            new_line = Line(
                dots[cycle_ind[k]].get_center(),
                dots[cycle_ind[(k + 1) % len(cycle_ind)]].get_center(),
                color=RED,
                stroke_width=5,
            )
            cycle_lines.append(new_line)
            self.play(ShowCreation(new_line), run_time=0.65)
        self.wait(1)
        self.play(VGroup(vgroup, *cycle_lines).animate.shift(3 * LEFT))
        t1 = Tex("The graph")
        t1.next_to(vgroup, RIGHT)
        self.play(Write(t1))
        self.play(
            ApplyFunction(
                lambda obj: obj.scale(0.2).next_to(t1, RIGHT).shift(0.4 * UP),
                VGroup(*lines, *dots).copy(),
            )
        )
        t2 = Tex("has a Hamiltonian cycle.")
        t2.next_to(t1, DOWN)
        t2.align_to(t1, LEFT)
        self.play(Write(t2))
        self.wait(1)
        self.play(*[FadeOut(obj) for obj in self.mobjects])
