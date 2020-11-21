import numpy as np
from manim import *


class ComplexPlaneWithFunctionDots(ComplexPlane):
    class InputDot(Dot):
        def __init__(self, plane, **kwargs):
            super().__init__(**kwargs)

            self.plane = plane

        def get_value(self):
            return self.plane.p2n(self.get_center())

        def set_value(self, value):
            self.move_to(self.plane.n2p(value))

            return self

    class OutputDot(Dot):
        def __init__(self, plane, input_dot, func, **kwargs):
            super().__init__(**kwargs)

            self.plane = plane
            self.input_dot = input_dot
            self.func = func

            self.update_position()
            always(self.update_position)

        def get_value(self):
            return self.plane.p2n(self.get_center())

        def update_position(self):
            self.move_to(self.plane.n2p(self.func(self.input_dot.get_value())))

    def get_function_dots(self, func, *, input_config={}, output_config={}):
        input_dot = self.InputDot(self, **input_config)
        output_dot = self.OutputDot(self, input_dot, func, **output_config)

        return input_dot, output_dot


class Euler(Scene):
    def construct(self):
        plane = ComplexPlaneWithFunctionDots()
        plane.add_coordinates(*plane.get_default_coordinate_values())
        self.add(plane)

        theta_dot, z_dot = plane.get_function_dots(
            lambda z: np.exp(1j * z),
            input_config={"color": RED},
            output_config={"color": YELLOW, "z_index": 1},
        )

        path = TracedPath(z_dot.get_center, min_distance_to_new_point=0)

        formula = MathTex("z", "=e^{i", r"\theta}").move_to(5.5 * LEFT + 2.5 * UP)
        formula[0].set_color(z_dot.get_color())
        formula[2].set_color(theta_dot.get_color())

        formula_box = Rectangle(
            width=formula.get_width() + MED_SMALL_BUFF,
            height=formula.get_height() + MED_SMALL_BUFF,
        )
        formula_box.move_to(formula).set_fill(BLACK, opacity=1).set_stroke(
            BLUE, opacity=1, width=DEFAULT_STROKE_WIDTH / 2
        )

        formula_group = VGroup(formula_box, formula)

        self.add(path, formula_group, theta_dot, z_dot)
        self.play(theta_dot.set_value, TAU, run_time=3)

        indicate_path = Circle(color=PINK)
        self.play(ShowCreationThenDestruction(indicate_path), run_time=3)

        self.play(theta_dot.set_value, 1j, run_time=3)
        self.play(Rotating(theta_dot, about_point=ORIGIN), run_time=3)
        self.play(theta_dot.move_to, plane.n2p(0))
