from manim import *


class DraftScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        def line_to_normal(line, rotation_direction="CLOCKWISE"):
            if rotation_direction == "CLOCKWISE":
                return normalize(
                    rotate_vector(line.get_end() - line.get_start(), PI / 2)
                )
            elif rotation_direction == "COUNTERCLOCKWISE":
                return normalize(
                    rotate_vector(line.get_end() - line.get_start(), -PI / 2)
                )
            else:
                raise Exception(rotation_direction)

        def get_h(triangle):
            h = Line(
                ORIGIN,
                ORIGIN
                + normalize(
                    rotate_vector(
                        triangle["c"].get_end() - triangle["c"].get_start(), PI / 2
                    )
                ),
            )
            h.shift(triangle_points["C"] - h.get_start())

            triangle_points["D"] = line_intersection(
                triangle["c"].get_start_and_end(), h.get_start_and_end()
            )
            h_length = get_norm(triangle_points["D"] - triangle_points["C"])

            h.put_start_and_end_on(
                h.get_start(),
                h.get_start()
                + normalize(
                    rotate_vector(
                        triangle["c"].get_end() - triangle["c"].get_start(), PI / 2
                    )
                )
                * h_length,
            )
            h.shift(triangle_points["C"] - h.get_start())
            return h

        triangle_points = {
            "A": LEFT * 2.7 + UP * 1.7,
            "B": RIGHT * 2.7 + DOWN * 1.3,
            "C": LEFT * 2.7 + DOWN * 1.3,
        }
        lines = [
            Line(triangle_points["A"], triangle_points["B"]),
            Line(triangle_points["B"], triangle_points["C"]),
            Line(triangle_points["C"], triangle_points["A"]),
        ]
        triangle = VDict(
            {
                "c": lines[0],
                "a": lines[1],
                "b": lines[2],
                "c_label": MathTex("c").move_to(
                    lines[0].get_center() + line_to_normal(lines[0]) * 0.3
                ),
                "a_label": MathTex("a").move_to(
                    lines[1].get_center() + line_to_normal(lines[1]) * 0.3
                ),
                "b_label": MathTex("b").move_to(
                    lines[2].get_center() + line_to_normal(lines[2]) * 0.3
                ),
            }
        )
        # self.play(ShowCreation(triangle))
        self.play(
            ShowCreation(VGroup(triangle["a"], triangle["b"], triangle["c"])),
        )
        self.play(
            Write(
                VGroup(triangle["a_label"], triangle["b_label"], triangle["c_label"])
            ),
        )
        self.wait(0.5)

        triangle.add({"h": get_h(triangle)})
        triangle.add(
            {
                "h_label": MathTex("h").move_to(
                    triangle["h"].get_center()
                    + line_to_normal(
                        triangle["h"], rotation_direction="COUNTERCLOCKWISE"
                    )
                    * 0.3
                )
            }
        )
        self.play(ShowCreation(triangle["h"]))
        self.play(Write(triangle["h_label"]))

        def get_triangle_area(points, color, opacity=0.7):
            return (
                Polygon(*points)
                .set_fill(color=color, opacity=opacity)
                .set_stroke(color=color)
            )

        triangle_area_positions = {
            "ABC": UP * 2.5 + LEFT * 2,
            "ADC": UP * 2.5 + LEFT * 0.1,
            "BDC": UP * 2.5 + RIGHT * 1.6,
        }

        # Animate full triangle area.
        ABC_area = get_triangle_area(
            [triangle_points["A"], triangle_points["B"], triangle_points["C"]], BLUE
        )
        self.play(FadeIn(ABC_area))
        ABC_area.generate_target().scale(0.3).move_to(triangle_area_positions["ABC"])
        self.play(MoveToTarget(ABC_area))
        self.wait(0.5)

        ADC_area = get_triangle_area(
            [triangle_points["A"], triangle_points["D"], triangle_points["C"]], ORANGE
        )
        ADC_area.generate_target().scale(0.3).move_to(triangle_area_positions["ADC"])
        triangle_area_equals = MathTex("=").next_to(ABC_area.target, RIGHT, buff=0.1)

        BDC_area = get_triangle_area(
            [triangle_points["B"], triangle_points["D"], triangle_points["C"]], GREEN
        )
        triangle_area_plus = MathTex("+").next_to(triangle_area_equals, RIGHT, buff=1.2)
        BDC_area.generate_target().scale(0.3).move_to(triangle_area_positions["BDC"])

        # Animate partial triangle areas.
        self.play(FadeIn(ADC_area), FadeIn(BDC_area))
        self.play(
            MoveToTarget(ADC_area),
            MoveToTarget(BDC_area),
            FadeIn(triangle_area_equals),
            FadeIn(triangle_area_plus),
        )
        self.wait(0.8)

        half_a_b = MathTex("\\frac{1}{2}ab").move_to(
            ABC_area.get_center() + RIGHT * 0.3
        )
        self.play(ReplacementTransform(ABC_area, half_a_b))
        self.wait(0.3)

        short_leg_length = Line(
            triangle_points["D"], triangle_points["A"], stroke_color=ORANGE
        )
        short_leg_variable = MathTex("x", color=ORANGE).move_to(
            triangle_points["A"] + (UP + LEFT) * 0.2
        )
        self.play(ShowCreation(short_leg_length), FadeIn(short_leg_variable))
        self.wait(0.3)

        half_h_x = MathTex("\\frac{1}{2}hx").move_to(ADC_area.get_center())
        self.play(ReplacementTransform(ADC_area, half_h_x))
        self.wait(0.3)

        long_leg_length = Line(
            triangle_points["D"], triangle_points["B"], stroke_color=GREEN
        )
        long_leg_variable = MathTex("y", color=GREEN).move_to(
            triangle_points["B"] + (DOWN + RIGHT) * 0.2
        )
        self.play(ShowCreation(long_leg_length), FadeIn(long_leg_variable))
        self.wait(0.3)

        half_h_y = MathTex("\\frac{1}{2}hy").move_to(BDC_area.get_center() + LEFT * 0.2)
        self.play(ReplacementTransform(BDC_area, half_h_y))
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(half_a_b[0][0:3])),
            FadeOut(VGroup(half_h_x[0][0:3])),
            FadeOut(VGroup(half_h_y[0][0:3])),
        )

        ab_equals_h_x_plus_y = MathTex("ab=h(x+y)").move_to(UP * 2.46)
        self.play(
            ReplacementTransform(
                VGroup(half_a_b[0][3:]), VGroup(ab_equals_h_x_plus_y[0][0:2])
            ),
            ReplacementTransform(triangle_area_equals, ab_equals_h_x_plus_y[0][2]),
            ReplacementTransform(triangle_area_plus, ab_equals_h_x_plus_y[0][6]),
            ReplacementTransform(half_h_x[0][3], ab_equals_h_x_plus_y[0][3]),
            FadeIn(ab_equals_h_x_plus_y[0][4]),
            ReplacementTransform(half_h_x[0][4], ab_equals_h_x_plus_y[0][5]),
            ReplacementTransform(half_h_y[0][4], ab_equals_h_x_plus_y[0][7]),
            ReplacementTransform(half_h_y[0][3], ab_equals_h_x_plus_y[0][3]),
            FadeIn(ab_equals_h_x_plus_y[0][8]),
        )
        self.wait(0.8)

        ab_equals_hc = MathTex("ab=hc")
        ab_equals_hc.shift(
            ab_equals_h_x_plus_y[0][0].get_center() - ab_equals_hc[0][0].get_center()
        )
        self.play(
            ReplacementTransform(ab_equals_h_x_plus_y[0][0], ab_equals_hc[0][0]),
            ReplacementTransform(ab_equals_h_x_plus_y[0][1], ab_equals_hc[0][1]),
            ReplacementTransform(ab_equals_h_x_plus_y[0][2], ab_equals_hc[0][2]),
            ReplacementTransform(ab_equals_h_x_plus_y[0][3], ab_equals_hc[0][3]),
            ReplacementTransform(
                VGroup(ab_equals_h_x_plus_y[0][4:]), ab_equals_hc[0][4]
            ),
            FadeOut(
                VGroup(
                    long_leg_length,
                    long_leg_variable,
                    short_leg_length,
                    short_leg_variable,
                )
            ),
        )
        self.wait(0.5)

        ab_over_h_equals_c = MathTex("\\frac{ab}{h}=c").move_to(
            ab_equals_hc.get_center()
        )
        self.play(
            ReplacementTransform(
                VGroup(ab_equals_hc[0][0:2]), VGroup(ab_over_h_equals_c[0][0:2])
            ),
            FadeIn(ab_over_h_equals_c[0][2]),
            ReplacementTransform(ab_equals_hc[0][3], ab_over_h_equals_c[0][3]),
            ReplacementTransform(ab_equals_hc[0][2], ab_over_h_equals_c[0][4]),
            ReplacementTransform(ab_equals_hc[0][4], ab_over_h_equals_c[0][5]),
        )
        self.wait(0.8)

        self.play(
            ab_over_h_equals_c.animate.shift(LEFT * 2),
            triangle.animate.shift(LEFT * 3),
        )

        pythagorean_theorem_text = MathTex(
            "\\underline{\\text{Pythagorean Theorem}}"
        ).shift(RIGHT * 3 + UP * 3)
        pythagorean_theorem = MathTex("a^2 + b^2 = c^2").next_to(
            pythagorean_theorem_text, DOWN
        )
        self.play(Write(pythagorean_theorem_text))
        self.wait(0.5)
        self.play(Write(pythagorean_theorem), run_time=1.5)
        self.wait(0.8)

        pythagorean_substitution = MathTex(
            "a^2 + b^2 = \\left(\\frac{ab}{h}\\right)^2"
        ).next_to(pythagorean_theorem, DOWN, buff=0.1)
        self.play(
            ReplacementTransform(
                VGroup(pythagorean_theorem[0][:6]).copy(),
                VGroup(pythagorean_substitution[0][:6]),
            ),
            FadeIn(
                VGroup(pythagorean_substitution[0][6], pythagorean_substitution[0][11])
            ),
            ReplacementTransform(
                VGroup(ab_over_h_equals_c[0][0:4]).copy(),
                VGroup(pythagorean_substitution[0][7:11]),
            ),
            ReplacementTransform(
                pythagorean_theorem[0][7],
                pythagorean_substitution[0][12],
            ),
            run_time=1.5,
        )
        self.wait(0.8)

        pythagorean_substitution_2 = MathTex(
            "a^2", "+", "b^2", "=", "\\frac{a^2b^2}{h^2}"
        ).next_to(pythagorean_substitution, DOWN)
        self.play(
            # Transform squares
            ReplacementTransform(
                pythagorean_substitution[0][-1].copy(), pythagorean_substitution_2[4][1]
            ),
            ReplacementTransform(
                pythagorean_substitution[0][-1].copy(), pythagorean_substitution_2[4][3]
            ),
            ReplacementTransform(
                pythagorean_substitution[0][-1].copy(), pythagorean_substitution_2[4][6]
            ),
            ReplacementTransform(
                pythagorean_substitution[0][0].copy(),
                pythagorean_substitution_2[0][0],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][1].copy(),
                pythagorean_substitution_2[0][1],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][2].copy(),
                pythagorean_substitution_2[1][0],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][3].copy(),
                pythagorean_substitution_2[2][0],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][4].copy(),
                pythagorean_substitution_2[2][1],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][5].copy(),
                pythagorean_substitution_2[3][0],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][7].copy(),
                pythagorean_substitution_2[4][0],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][8].copy(),
                pythagorean_substitution_2[4][2],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][9].copy(),
                pythagorean_substitution_2[4][4],
            ),
            ReplacementTransform(
                pythagorean_substitution[0][10].copy(),
                pythagorean_substitution_2[4][5],
            ),
        )
        self.wait(0.8)

        pythagorean_substitution_3 = MathTex(
            "\\frac{a^2}{a^2b^2}", "+", "\\frac{b^2}{a^2b^2}", "=", "\\frac{1}{h^2}"
        ).next_to(pythagorean_substitution_2, DOWN)
        self.play(
            ReplacementTransform(
                VGroup(pythagorean_substitution_2[4][:4]).copy(),
                VGroup(pythagorean_substitution_3[0][3:]),
            ),
            ReplacementTransform(
                VGroup(pythagorean_substitution_2[4][:4]).copy(),
                VGroup(pythagorean_substitution_3[2][3:]),
            ),
            ReplacementTransform(
                pythagorean_substitution_2[0][0].copy(),
                pythagorean_substitution_3[0][0],
            ),
            ReplacementTransform(
                pythagorean_substitution_2[0][1].copy(),
                pythagorean_substitution_3[0][1],
            ),
            FadeIn(pythagorean_substitution_3[0][2]),
            ReplacementTransform(
                pythagorean_substitution_2[1].copy(), pythagorean_substitution_3[1]
            ),
            ReplacementTransform(
                pythagorean_substitution_2[2][0].copy(),
                pythagorean_substitution_3[2][0],
            ),
            ReplacementTransform(
                pythagorean_substitution_2[2][1].copy(),
                pythagorean_substitution_3[2][1],
            ),
            FadeIn(pythagorean_substitution_3[2][2]),
            ReplacementTransform(
                pythagorean_substitution_2[3].copy(), pythagorean_substitution_3[3]
            ),
            FadeIn(pythagorean_substitution_3[4][0]),
            ReplacementTransform(
                pythagorean_substitution_2[4][4].copy(),
                pythagorean_substitution_3[4][1],
            ),
            ReplacementTransform(
                pythagorean_substitution_2[4][5].copy(),
                pythagorean_substitution_3[4][2],
            ),
            ReplacementTransform(
                pythagorean_substitution_2[4][6].copy(),
                pythagorean_substitution_3[4][3],
            ),
        )
        self.wait(0.8)

        crossed_tex = [
            VGroup(pythagorean_substitution_3[0][:2]),
            VGroup(pythagorean_substitution_3[0][3:5]),
            VGroup(pythagorean_substitution_3[2][:2]),
            VGroup(pythagorean_substitution_3[2][5:7]),
        ]
        crosses = []
        for tex in crossed_tex:
            crosses.append(Line(tex.get_critical_point(DL), tex.get_critical_point(UR)))
        self.play(*[ShowCreation(cross) for cross in crosses])
        self.wait(0.8)

        inverse_pythagorean_theorem = MathTex(
            "\\frac{1}{a^2} + \\frac{1}{b^2} = \\frac{1}{h^2}"
        ).next_to(pythagorean_substitution_3, DOWN)
        self.play(Write(inverse_pythagorean_theorem), run_time=3)
        self.play(
            AnimationOnSurroundingRectangle(
                inverse_pythagorean_theorem,
                ShowCreation,
                surrounding_rectangle_config={"color": BLACK},
            )
        )

        # Position labels for each side.
        self.wait()
