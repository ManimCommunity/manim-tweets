from manim import *


class Lens(Scene):
    def construct(self):
        lens_height = 3
        lens_width = 0.5
        focal_length = 4

        lens = VGroup()
        lens.add(
            Line(
                UP * lens_height / 2 + LEFT * lens_width / 2,
                UP * lens_height / 2 + RIGHT * lens_width / 2,
            )
        )
        lens.add(
            Line(
                DOWN * lens_height / 2 + LEFT * lens_width / 2,
                DOWN * lens_height / 2 + RIGHT * lens_width / 2,
            )
        )
        lens_angle = TAU / 3 - 1.3
        left_arc = (
            Arc(start_angle=-lens_angle / 2, angle=lens_angle)
            .rotate(PI)
            .set_height(lens_height)
            .align_to(lens[0], LEFT)
        )
        left_arc.shift(LEFT * left_arc.get_width())
        lens.add(left_arc)
        right_arc = (
            Arc(start_angle=-lens_angle / 2, angle=lens_angle)
            .set_height(lens_height)
            .align_to(lens[0], RIGHT)
        )
        right_arc.shift(RIGHT * right_arc.get_width())
        lens.add(right_arc)

        original_dist_color = YELLOW
        image_dist_color = BLUE

        # Update the original.
        original_arrow = Arrow(ORIGIN, UP, buff=0).shift(3 * LEFT)
        original_arrow_tracker = ValueTracker(original_arrow.get_x())

        def update_original_arrow(mob):
            time = original_arrow_tracker.get_value()
            x_offset = RIGHT * (-4 + np.sin(time * 1.3))
            mob.move_to(x_offset)

        original_arrow.add_updater(update_original_arrow)

        # Update the arrow indicating the distance to the original.
        original_dist_arrow = Arrow(
            ORIGIN, RIGHT * original_arrow_tracker.get_value()
        ).set_color(original_dist_color)

        def update_original_dist_arrow(mob):
            original_arrow_x_offset = original_arrow.get_center()[0]
            mob.put_start_and_end_on(ORIGIN, RIGHT * original_arrow_x_offset)
            mob.shift(diagram_shift)

        original_dist_arrow.add_updater(update_original_dist_arrow)

        # Update the image arrow.
        image_arrow = Arrow(
            ORIGIN,
            DOWN,
            buff=0,
        ).shift(3 * RIGHT)

        def update_image(mob):
            object_lens_dist = original_arrow.get_center()[0]
            image_lens_dist = 1 / (1 / focal_length - 1 / object_lens_dist)
            magnification = image_lens_dist / object_lens_dist

            arrow_tip_height = mob.submobjects[0].get_height()
            new_arrow = Line(
                RIGHT * image_lens_dist + diagram_shift,
                RIGHT * image_lens_dist
                + UP * (magnification + arrow_tip_height)
                + diagram_shift,
            )
            mob.submobjects[0].next_to(new_arrow, DOWN, buff=0)
            new_arrow.add(mob.submobjects[0])
            mob.become(new_arrow)

        image_arrow.add_updater(update_image)

        # Update the arrow indicating the distance to the image.
        object_lens_dist = original_arrow.get_center()[0]
        image_lens_dist = 1 / (1 / focal_length - 1 / object_lens_dist)
        image_dist_arrow = Arrow(ORIGIN, RIGHT * image_lens_dist).set_color(
            image_dist_color
        )

        def update_image_dist_arrow(mob):
            object_lens_dist = original_arrow.get_center()[0]
            image_lens_dist = 1 / (1 / focal_length - 1 / object_lens_dist)
            start = ORIGIN + diagram_shift
            end = RIGHT * image_lens_dist + diagram_shift
            mob.put_start_and_end_on(start, end)

        image_dist_arrow.add_updater(update_image_dist_arrow)

        self.add(original_arrow, image_arrow)
        self.add(lens)

        """
        v = 1 / (1 / f - 1 / u)
        1 / u + 1 / v = (n - 1)(1 / R1 - 1 / R2 + (n-1)d / (n*R1*R2))
        (1 / u + 1 / v)/ (n-1) = 1 / R1 - 1 / R2 + (n-1)d / (n*R1*R2)
        (1 / u + 1 / v)/ (n-1) - 1/R1 + 1/R2 = (n-1)d / (n*R1*R2)
        (1/u + 1/v) / (n-1)^2 - (1/R1 + 1/R2)/(n-1) = d/(n*R1*R2)
        (n*R1*R2) * (1/u + 1/v) / (n-1)^2 - (1/R1 + 1/R2)/(n-1) = d
        """

        image_lens_dist = 10  # This is only to set the arrow size.
        diagram_shift = DOWN * 0.5

        original_dist_arrow.add_updater(update_original_dist_arrow)
        self.add(original_dist_arrow)

        # Indicate the distance to the image arrow.

        self.add(image_dist_arrow)

        VGroup(
            lens, original_arrow, image_arrow, original_dist_arrow, image_dist_arrow
        ).shift(diagram_shift)

        description = (
            Tex(
                "The distance between an object and its projected \\\\"
                "image is given by the thin lens equation: "
            )
            .scale(0.7)
            .to_edge(UP)
        )
        thin_lens_equation = (
            MathTex(
                "\\frac{1}{u}",
                "+",
                "\\frac{1}{v}",
                "=",
                "\\frac{1}{f}",
            )
            .scale(0.7)
            .next_to(description, DOWN)
        )
        # Color the distance variables.
        thin_lens_equation[0][2].set_color(original_dist_color)
        thin_lens_equation[2][2].set_color(image_dist_color)
        u_label = MathTex("u", fill_color=original_dist_color).shift(LEFT + DOWN)
        v_label = MathTex("v", fill_color=image_dist_color).shift(RIGHT + DOWN)

        self.play(
            original_arrow_tracker.animate.set_value(3.5),
            Write(description),
            rate_func=linear,
            run_time=3.5,
        )
        self.play(
            original_arrow_tracker.animate.set_value(4),
            rate_func=linear,
            run_time=0.5,
        )
        self.play(
            original_arrow_tracker.animate.set_value(5.5),
            Write(thin_lens_equation),
            Write(VGroup(u_label, v_label)),
            rate_func=linear,
            run_time=1.5,
        )
        self.play(
            original_arrow_tracker.animate.set_value(6.5),
            FadeOut(description),
            rate_func=linear,
            run_time=1,
        )

        image_dist_arrow.set_color(GRAY)
        v_label.set_color(GRAY)
        thin_lens_equation[2][2].set_color(GRAY)
        fixed_distance_explanation = (
            Tex(
                "If the distance to the image is fixed, the distance to the original "
                "will still change according to the lensmaker equation:"
            )
            .scale(0.7)
            .to_edge(UP)
        )
        self.wait(0.5)
        self.play(Write(fixed_distance_explanation))

        lens_width_color = RED
        lensmaker_equation = (
            MathTex(
                "(n-1)",
                "\\left[",
                "\\frac{1}{R_1}",
                "-",
                "\\frac{1}{R_2}",
                "+",
                "\\frac{(n-1)d}{nR_1R_2}",
                "\\right]",
            )
            .scale(0.7)
            .next_to(thin_lens_equation[3], RIGHT)
        )
        lensmaker_equation[6][5].set_color(lens_width_color)
        target = thin_lens_equation.generate_target()
        target.submobjects[4] = lensmaker_equation
        target.shift(RIGHT * -target.get_center()[1])

        distance_label = (
            DoubleArrow(
                LEFT * lens.get_width() / 2, RIGHT * lens.get_width() / 2, buff=0
            )
            .next_to(lens, UP, buff=SMALL_BUFF)
            .set_color(lens_width_color)
        )
        self.play(
            MoveToTarget(
                thin_lens_equation,
            ),
            FadeIn(distance_label),
        )

        self.play(FadeOut(fixed_distance_explanation))
        distance_explanation = (
            Tex(
                "If the ",
                "thickness of the lens",
                " is allowed to vary with the distance to the object "
                "the image can be preserved at a fixed distance.",
            )
            .scale(0.7)
            .to_edge(UP)
        )
        distance_explanation[1].set_color(lens_width_color)
        image_dist_arrow.clear_updaters()
        image_arrow.clear_updaters()

        def update_image_2(mob):
            object_lens_dist = original_arrow.get_center()[0]
            image_lens_dist = 1 / (1 / focal_length - 1 / object_lens_dist)
            magnification = image_lens_dist / object_lens_dist

            original_top = mob.get_top()

            arrow_tip_height = mob.submobjects[0].get_height()
            new_arrow = Line(
                original_top,
                original_top + UP * (magnification + arrow_tip_height),
            )
            mob.submobjects[0].next_to(new_arrow, DOWN, buff=0)
            new_arrow.add(mob.submobjects[0])
            mob.become(new_arrow)

        image_arrow.add_updater(update_image_2)

        initial_x_offset = original_arrow.get_center()[0]

        def update_lens_thickness(mob):
            original_arrow_x_offset = original_arrow.get_center()[0]
            new_width = lens_width / original_arrow_x_offset * initial_x_offset
            original_lens_center = mob.get_center()
            lens = VGroup()
            lens.add(
                Line(
                    UP * lens_height / 2 + LEFT * new_width / 2,
                    UP * lens_height / 2 + RIGHT * new_width / 2,
                )
            )
            lens.add(
                Line(
                    DOWN * lens_height / 2 + LEFT * new_width / 2,
                    DOWN * lens_height / 2 + RIGHT * new_width / 2,
                )
            )
            lens_angle = TAU / 3 - 1.3
            right_arc = (
                Arc(start_angle=-lens_angle / 2, angle=lens_angle)
                .set_height(lens_height)
                .align_to(lens[0], RIGHT)
            )
            right_arc.shift(RIGHT * right_arc.get_width())
            lens.add(right_arc)
            left_arc = (
                Arc(start_angle=-lens_angle / 2, angle=lens_angle)
                .rotate(PI)
                .set_height(lens_height)
                .align_to(lens[0], LEFT)
            )
            left_arc.shift(LEFT * left_arc.get_width())
            lens.add(left_arc)
            lens.move_to(original_lens_center)
            mob.become(lens)

            # Update width label.
            arrow_y_offset = distance_label.get_start()[1]
            distance_label.put_start_and_end_on(
                LEFT * lens.get_width() / 2 + UP * arrow_y_offset,
                RIGHT * lens.get_width() / 2 + UP * arrow_y_offset,
            )

        lens.add_updater(update_lens_thickness)

        self.play(
            original_arrow_tracker.animate.set_value(8),
            Write(distance_explanation),
            run_time=1.5,
            rate_func=linear,
        )
        self.play(
            original_arrow_tracker.animate.set_value(10.5),
            run_time=2.5,
            rate_func=linear,
        )
        for mob in self.mobjects:
            mob.clear_updaters()
        self.play(
            FadeOutAndShift(
                VGroup(*[m for m in self.mobjects if isinstance(m, VMobject)]), UP
            )
        )
        #
        #
        # class Eye(Scene):
        #     def construct(self):
        def get_eye():
            lens_height = 2
            lens_width = 0.6

            lens = Ellipse(
                width=lens_width,
                height=lens_height,
                fill_opacity=1,
                stroke_color=BLUE,
                fill_color="#EEEEEE",
            )

            cilliary_muscle_length = 0.2
            cilliary_muscle = VGroup(
                Line(
                    lens.get_top(),
                    lens.get_top() + cilliary_muscle_length * UP,
                    stroke_width=8,
                ).set_color(RED_E),
                Line(
                    lens.get_bottom(),
                    lens.get_bottom() + cilliary_muscle_length * DOWN,
                    stroke_width=8,
                ).set_color(RED_E),
            )

            vitreous_chamber_angle = 0.8 * TAU
            vitreous_chamber_back = Arc(
                angle=vitreous_chamber_angle,
                fill_opacity=1,
                fill_color=BLUE_C,
                stroke_color=RED_B,
            )
            angle_to_rotate = (vitreous_chamber_angle - TAU) / 2
            vitreous_chamber_back.rotate(
                PI - angle_to_rotate, about_point=ORIGIN
            ).scale(2).shift(RIGHT * 1.7)

            # retina = Arc(
            #     0.8 * TAU,
            #     stroke_color=RED_B,
            # )
            # retina.rotate(PI - angle_to_rotate, about_point=ORIGIN,).scale(
            #     2
            # ).shift(RIGHT * 1.7)

            aqueous_humor_angle = TAU - vitreous_chamber_angle
            aqueous_humor = (
                Arc(angle=aqueous_humor_angle, fill_opacity=1, stroke_opacity=0)
                .set_color(BLUE_A)
                .rotate(PI - aqueous_humor_angle / 2, about_point=ORIGIN)
                .scale(2.05)
                .next_to(vitreous_chamber_back, LEFT, buff=0)
            )

            cornea_angle = 0.4 * TAU
            cornea = Arc(
                angle=cornea_angle,
                stroke_color="#EEEEEE",
                stroke_opacity=0.5,
                fill_color=BLUE_A,
                fill_opacity=1,
                stroke_width=14,
            )
            cornea.rotate(PI - cornea_angle / 2, about_point=ORIGIN)
            cornea.next_to(vitreous_chamber_back, LEFT, buff=0)
            cornea.scale(1.2)

            eye = VGroup(
                # retina,
                cornea,
                vitreous_chamber_back,
                aqueous_humor,
                cilliary_muscle,
                lens,
            )
            eye.lens = lens
            eye.shift(-eye.get_center())
            return eye

        eye = get_eye()
        eye_text = Tex("Eye").scale(1.5).next_to(eye, UP)
        self.play(
            FadeInFrom(eye_text, UP),
            FadeInFrom(eye, UP),
        )
        self.wait(0.5)

        saved_eye = eye.generate_target()  # Save the eye to restore later.
        target_eye = eye.generate_target()
        target_eye.submobjects[0].shift(LEFT * 2)  # cornea
        target_eye.submobjects[2].shift(LEFT * 2)  # aqueous humor
        target_eye.submobjects[4].shift(RIGHT * 0.7)  # lens
        target_eye.submobjects[1].shift(RIGHT * 2)  # vitreous_chamber_back
        target_eye.submobjects[3].shift(LEFT * 0.5)  # cilliary_muscle
        self.play(
            MoveToTarget(eye),
            FadeOutAndShift(eye_text, UP),
        )

        cornea_label = Tex("Cornea").scale(0.8).next_to(target_eye.submobjects[0], LEFT)
        aqueous_humor_label = (
            Tex("Aqueous Humor").scale(0.8).next_to(target_eye.submobjects[2], DOWN)
        )
        lens_label = (
            Tex("Lens", fill_color=BLUE)
            .scale(0.8)
            .next_to(target_eye.submobjects[4], DOWN)
        )
        vitreous_chamber_label = (
            Tex("Vitreous\\\\Chamber")
            .scale(0.8)
            .move_to(target_eye.submobjects[1].get_center())
        )
        cilliary_muscle_label = (
            Tex("Cilliary\\\\Muscle").scale(0.8).next_to(target_eye.submobjects[3], UP)
        )
        retina_label = (
            Tex("Retina", fill_color=YELLOW)
            .scale(0.8)
            .next_to(target_eye.submobjects[1], RIGHT)
        )
        self.play(
            FadeIn(
                VGroup(
                    cornea_label,
                    aqueous_humor_label,
                    lens_label,
                    vitreous_chamber_label,
                    cilliary_muscle_label,
                    retina_label,
                )
            ),
        )

        eye_lens_explanation = Tex(
            "This is how the ",
            "lenses",
            " in our eyes focus light on our ",
            "retinas",
        ).scale(0.9)
        eye_lens_explanation[1].set_color(BLUE)
        eye_lens_explanation[3].set_color(YELLOW)
        eye_lens_explanation.shift(
            UP
            * (
                target_eye.submobjects[1].get_bottom()[1]
                - eye_lens_explanation.get_top()[1]
                - 0.8
            )
        )
        eye_lens_explanation_2 = (
            Tex("which are always a fixed distance away.")
            .scale(0.9)
            .next_to(eye_lens_explanation, DOWN, buff=SMALL_BUFF)
        )
        self.play(Write(eye_lens_explanation))
        self.wait(0.5)

        eye.target = saved_eye
        self.play(
            MoveToTarget(eye),
            FadeOut(
                VGroup(
                    cornea_label,
                    aqueous_humor_label,
                    lens_label,
                    vitreous_chamber_label,
                    cilliary_muscle_label,
                    retina_label,
                )
            ),
        )
        self.play(eye.animate.shift(3 * RIGHT), run_time=0.7)

        original_arrow = Arrow(ORIGIN, UP * 0.8, buff=0).shift(3 * LEFT)
        image_arrow = Arrow(ORIGIN, DOWN * 0.7, buff=0).shift(4.8 * RIGHT)
        focal_axis = Line(
            original_arrow.get_bottom(),
            image_arrow.get_top(),
            stroke_width=3,
            stroke_color=GREY_B,
        )
        self.play(FadeIn(VGroup(original_arrow, image_arrow)))
        self.play(ShowCreation(focal_axis), run_time=0.7)

        original_arrow_tracker = ValueTracker()

        # Update the original arrow.
        original_arrow_starting_position = original_arrow.get_center()

        def update_original(mob):
            time = original_arrow_tracker.get_value()
            x_offset = 1.5 * RIGHT * np.sin(time * 1.5)
            mob.move_to(original_arrow_starting_position + RIGHT * x_offset)

        original_arrow.add_updater(update_original)

        lens = eye.submobjects[4]
        original_image_height = image_arrow.get_height()
        object_lens_dist = lens.get_center()[0] - original_arrow.get_center()[0]
        image_lens_dist = image_arrow.get_center()[0] - lens.get_center()[0]
        original_magnification = image_lens_dist / object_lens_dist
        magnification_offset_ratio = original_image_height / original_magnification

        def update_image(mob):
            lens = eye.submobjects[4]
            object_lens_dist = lens.get_center()[0] - original_arrow.get_center()[0]
            image_lens_dist = image_arrow.get_center()[0] - lens.get_center()[0]
            magnification = image_lens_dist / object_lens_dist
            magnification *= magnification_offset_ratio
            image_arrow_base = image_arrow.get_top()

            arrow_tip_height = mob.submobjects[0].get_height()
            new_arrow = Line(
                image_arrow_base,
                image_arrow_base + DOWN * (magnification - arrow_tip_height),
            )
            mob.submobjects[0].next_to(new_arrow, DOWN, buff=0)
            new_arrow.add(mob.submobjects[0])
            mob.become(new_arrow)

        image_arrow.add_updater(update_image)

        # Update the thickness of the lens.
        starting_lens_dist = eye.lens.get_center()[0] - original_arrow.get_center()[0]

        def update_lens(mob):
            original_lens_dist = (
                eye.lens.get_center()[0] - original_arrow.get_center()[0]
            )
            mob.stretch_to_fit_width(0.6 * starting_lens_dist / original_lens_dist)

        lens = eye.lens
        lens.add_updater(update_lens)

        def update_axis(mob):
            new_axis = Line(
                original_arrow.get_bottom(),
                image_arrow.get_top(),
                stroke_width=3,
                stroke_color=GREY_B,
            )
            mob.become(new_axis)

        focal_axis.add_updater(update_axis)

        self.play(
            Write(eye_lens_explanation_2),
            original_arrow_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=1,
        )
        self.play(
            original_arrow_tracker.animate.set_value(6),
            rate_func=linear,
            run_time=5,
        )
