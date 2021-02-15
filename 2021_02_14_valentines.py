from manim import *


class ValentineScene(GraphScene, MovingCameraScene):
    def setup(self):
        MovingCameraScene.setup(self)

    def construct(self):
        self.camera.background_color = WHITE
        self.axes_color = BLACK
        self.x_min = -PI
        self.x_max = PI
        self.x_axis_config = {"tick_frequency": PI / 2}
        self.x_axis_width = 10

        self.y_min = -3
        self.y_max = 3
        self.y_axis_height = 10
        self.graph_origin = ORIGIN

        self.camera_frame.scale(1.3)
        self.setup_axes()
        self.remove(
            self.x_axis, self.y_axis, self.y_axis_label_mob, self.x_axis_label_mob
        )
        self.y_axis_label_mob.shift(0.4 * DOWN + 0.2 * RIGHT)
        self.play(
            Write(
                VGroup(
                    self.x_axis,
                    self.y_axis,
                    self.y_axis_label_mob,
                    self.x_axis_label_mob,
                )
            )
        )

        axis_labels = [
            MathTex("\\frac{\\pi}{2}")
            .scale(0.8)
            .move_to(self.coords_to_point(PI / 2, -0.35)),
            MathTex("-\\frac{\\pi}{2}")
            .scale(0.8)
            .move_to(self.coords_to_point(-PI / 2, -0.35)),
        ]

        # Label axes.
        self.play(*[Write(label) for label in axis_labels])

        # Draw positive sin.
        positive_sin = self.get_graph(
            lambda x: np.sin(x) + 1, color=GRAY, x_min=-PI, x_max=PI
        )
        positive_sin_label = (
            MathTex("f(x) = ", "\\sin(x) + 1")
            .scale(0.7)
            .move_to(self.coords_to_point(-PI, 1.2))
        )
        self.play(
            Write(positive_sin_label),
            ShowCreation(positive_sin),
        )
        self.wait(0.7)

        # Trace heart section.
        heart_red = "#e0245e"
        heart_stroke_width = 6

        def draw_positive_section(section, dt):
            section.total_time += dt
            section.total_time = min(section.total_time, 1)
            new_section = self.get_graph(
                lambda x: np.sin(x) + 1,
                color=heart_red,
                x_min=-PI / 2,
                x_max=-PI / 2 + PI * section.total_time,
                stroke_width=heart_stroke_width,
            )
            section.become(new_section)

        positive_sin_heart_section = self.get_graph(
            lambda x: np.sin(x) + 1,
            color=heart_red,
            x_min=-PI / 2,
            x_max=-PI / 2,
            stroke_width=heart_stroke_width,
        )
        positive_sin_heart_section.total_time = 0
        positive_sin_heart_section.add_updater(draw_positive_section)
        self.add(positive_sin_heart_section)

        self.wait()
        self.wait(0.7)

        # Draw negative sin.
        negative_sin = self.get_graph(
            lambda x: -np.sin(x) - 1, color=GRAY, x_min=-PI, x_max=PI
        )
        negative_sin_label = (
            MathTex("f(x) = ", "-\\sin(x) - 1")
            .scale(0.7)
            .move_to(self.coords_to_point(-PI, -1.2))
        )
        self.play(
            Write(negative_sin_label),
            ShowCreation(negative_sin),
        )
        self.wait(0.7)

        # Trace heart section.
        def draw_negative_section(section, dt):
            section.total_time += dt
            section.total_time = min(section.total_time, 1)
            new_section = self.get_graph(
                lambda x: -np.sin(x) - 1,
                color=heart_red,
                x_min=-PI / 2,
                x_max=-PI / 2 + PI * section.total_time,
                stroke_width=heart_stroke_width,
            )
            section.become(new_section)

        negative_sin_heart_section = self.get_graph(
            lambda x: -np.sin(x) - 1,
            color=heart_red,
            x_min=-PI / 2,
            x_max=PI / 2,
            stroke_width=heart_stroke_width,
        )
        negative_sin_heart_section.total_time = 0
        negative_sin_heart_section.add_updater(draw_negative_section)
        self.add(negative_sin_heart_section)
        self.wait()
        self.wait(0.7)

        # Draw the positive circle.
        positive_circle = Circle(
            radius=self.y_axis_config["unit_size"],
            stroke_color=GRAY,
        ).move_to(self.coords_to_point(PI / 2, 1))
        positive_circle_label = (
            MathTex("\\left(x-\\frac{\\pi}{2}\\right)^2 + (y-1)^2 = 1")
            .scale(0.7)
            .next_to(positive_circle, UR, buff=0.1)
            .shift(LEFT * 0.8 + DOWN * 0.2)
        )
        self.bring_to_back(positive_circle)
        self.play(ShowCreation(positive_circle), Write(positive_circle_label))

        # Trace the heart section.
        def draw_positive_circle_section(section, dt):
            section.total_time += dt
            section.total_time = min(section.total_time, 1)
            new_section = Arc(
                radius=self.y_axis_config["unit_size"],
                start_angle=PI / 2,
                angle=-PI * section.total_time,
                color=heart_red,
                stroke_width=heart_stroke_width,
            ).move_arc_center_to(self.coords_to_point(PI / 2, 1))
            section.become(new_section)

        positive_circle_heart_section = Arc(
            radius=self.y_axis_config["unit_size"],
            start_angle=PI / 2,
            angle=-PI,
            color=heart_red,
            stroke_width=heart_stroke_width,
        ).move_arc_center_to(self.coords_to_point(PI / 2, 1))
        positive_circle_heart_section.total_time = 0
        self.add(positive_circle_heart_section)
        positive_circle_heart_section.add_updater(draw_positive_circle_section)
        self.wait()
        self.wait(0.7)

        # Draw the negative circle.
        negative_circle = Circle(
            radius=self.y_axis_config["unit_size"],
            stroke_color=GRAY,
        ).move_to(self.coords_to_point(PI / 2, -1))
        negative_circle_label = (
            MathTex("\\left(x-\\frac{\\pi}{2}\\right)^2 + (y+1)^2 = 1")
            .scale(0.7)
            .next_to(negative_circle, DR, buff=0.1)
            .shift(LEFT * 0.8 + UP * 0.2)
        )
        self.bring_to_back(negative_circle)
        self.play(ShowCreation(negative_circle), Write(negative_circle_label))

        # Trace the heart section.
        def draw_negative_circle_section(section, dt):
            section.total_time += dt
            section.total_time = min(section.total_time, 1)
            new_section = Arc(
                radius=self.y_axis_config["unit_size"],
                start_angle=-PI / 2,
                angle=PI * section.total_time,
                color=heart_red,
                stroke_width=heart_stroke_width,
            ).move_arc_center_to(self.coords_to_point(PI / 2, -1))
            section.become(new_section)

        negative_circle_heart_section = Arc(
            radius=self.y_axis_config["unit_size"],
            start_angle=-PI / 2,
            angle=PI,
            color=heart_red,
            stroke_width=heart_stroke_width,
        ).move_arc_center_to(self.coords_to_point(PI / 2, 1))
        negative_circle_heart_section.total_time = 0
        self.add(negative_circle_heart_section)
        negative_circle_heart_section.add_updater(draw_negative_circle_section)

        self.wait()
        self.wait(0.7)

        # Flip over y = x
        def inverse_function(func):
            flipped_func = func.copy()
            for i, point in enumerate(func.points):
                x, y, _ = point
                flipped_func.points[i] = self.coords_to_point(y * 2 / PI, x * PI / 5.2)
            return flipped_func

        graph_sections = [
            positive_sin,
            positive_sin_heart_section,
            negative_sin,
            negative_sin_heart_section,
            positive_circle,
            positive_circle_heart_section,
            negative_circle,
            negative_circle_heart_section,
        ]
        for func in graph_sections:
            func.clear_updaters()

        transforms = []
        for func in graph_sections:
            transforms.append(Transform(func, inverse_function(func)))

        graph_label_data = [
            # f(x) = sin(x) + 1
            {
                "label": positive_sin_label,
                "offset": UP * 4.5 + RIGHT * 0.5,
                "inverse": ["f(x) = ", "-\\arcsin(-x + 1)"],
            },
            # f(x) = sin(x) - 1
            {
                "label": negative_sin_label,
                "offset": UP * 4.5 + LEFT * 0.5,
                "inverse": ["f(x) = ", "-\\arcsin(x + 1)"],
            },
            # \\left(x-\\frac{\\pi}{2}\\right)^2 + (y-1)^2 = 1
            {
                "label": positive_circle_label,
                "offset": DOWN * 4.1 + RIGHT * 0,
                "inverse": "\\left(y-\\frac{\\pi}{2}\\right)^2 + (x-1)^2 = 1",
            },
            # \\left(x-\\frac{\\pi}{2}\\right)^2 + (y+1)^2 = 1
            {
                "label": negative_circle_label,
                "offset": DOWN * 4.1 + LEFT * 0,
                "inverse": "\\left(y-\\frac{\\pi}{2}\\right)^2 + (x+1)^2 = 1",
            },
        ]
        animations = []
        for i, data in enumerate(graph_label_data):
            label = data["label"]
            offset = data["offset"]
            inverse = data["inverse"]
            x, y, _ = label.get_center()
            target = label.generate_target()
            # Match the corresponding terms for the sin transformations.
            if i < 2:
                target_tex = MathTex(inverse[0], inverse[1])
            else:
                target_tex = MathTex(inverse)
            target.become(target_tex)
            target.move_to(self.coords_to_point(y, x)).shift(offset)
            animations.append(MoveToTarget(label))

        self.play(self.camera_frame.animate.scale(1.2), *transforms, *animations)
        self.wait(0.5)

        graph_sections = [
            positive_sin,
            negative_sin,
            positive_circle,
            negative_circle,
        ]
        graph_labels = [data["label"] for data in graph_label_data]
        animations = [
            FadeOut(mob)
            for mob in graph_sections
            + graph_labels
            + axis_labels
            + [self.x_axis, self.y_axis, self.x_axis_label_mob, self.y_axis_label_mob]
        ]
        self.play(*animations)

        heart_mob = VMobject(
            stroke_color=heart_red,
            fill_color=heart_red,
            stroke_width=heart_stroke_width,
        )
        for i, graph_section in enumerate(
            [
                positive_sin_heart_section,
                positive_circle_heart_section,
                negative_sin_heart_section,
                negative_circle_heart_section,
            ]
        ):
            heart_mob.append_points(graph_section.points)

        self.remove(
            positive_sin_heart_section,
            positive_circle_heart_section,
            negative_circle_heart_section,
            negative_sin_heart_section,
        )
        self.add(heart_mob)
        self.play(heart_mob.animate.set_fill(opacity=1))
        self.wait(0.5)

        heart_mob.generate_target().scale(0.15).shift(UP * 1.7)
        self.play(MoveToTarget(heart_mob))

        message_front = (
            Text("With", fill_color=BLACK).scale(1.5).next_to(heart_mob, LEFT)
        )
        message_back = (
            Text("from", fill_color=BLACK).scale(1.5).next_to(heart_mob, RIGHT)
        )

        self.play(FadeIn(message_front), FadeIn(message_back))

        banner_location = (
            VGroup(message_front, heart_mob, message_back).get_center() + 3 * DOWN
        )

        banner = ManimBanner(dark_theme=False).scale(0.9).move_to(banner_location)
        banner.scale_factor = 2.5
        self.play(banner.create())

        for mob in [banner.triangle, banner.circle, banner.square]:
            mob.clear_updaters()
        self.bring_to_front(banner.M)

        # Position the targets of the M.
        banner.M.generate_target().shift(LEFT * banner.anim.get_width() * 0.57),

        # Position the anim based on the location of the target.
        banner.anim.next_to(banner.M.target, RIGHT, 0.1)
        banner.anim.align_to(banner.M.target, DOWN)

        self.play(
            banner.M.animate.shift(LEFT * banner.anim.get_width() * 0.57),
            banner.triangle.animate.shift(RIGHT * banner.anim.get_width() * 0.57),
            banner.square.animate.shift(RIGHT * banner.anim.get_width() * 0.57),
            banner.circle.animate.shift(RIGHT * banner.anim.get_width() * 0.57),
            AnimationGroup(
                ApplyMethod(VGroup(banner.anim[1], banner.anim[2]).set_opacity, 1),
                ApplyMethod(VGroup(banner.anim[0], banner.anim[-1]).set_opacity, 1),
                lag_ratio=0.3,
            ),
        )

        self.wait()


class FunctionPlotWithLabelledYAxis(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_min=0,
            y_max=100,
            y_axis_config={"tick_frequency": 10},
            y_labeled_nums=np.arange(0, 100, 10),
            **kwargs
        )

    def construct(self):
        self.setup_axes()
        dot = Dot().move_to(self.coords_to_point(PI / 2, 20))
        func_graph = self.get_graph(lambda x: 20 * np.sin(x))
        self.add(dot, func_graph)
        func_graph.add_updater(lambda mob, dt: mob)
        self.play(func_graph.animate.shift(UP))
