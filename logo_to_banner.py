from manim import *



def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


# Render with -c "#ece6e2"
class DraftScene(Scene):
    def construct(self):
        logo_green = "#81b29a"
        logo_blue = "#454866"
        logo_red = "#e07a5f"
        logo_black = "#343434"

        ds_m = MathTex(r"\mathbb{M}", z_index=20).scale(7).set_color(logo_black)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)

        circle = Circle(color=logo_green, fill_opacity=1, z_index=7).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1, z_index=5).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1, z_index=3).shift(RIGHT)

        vgroup = VGroup(triangle, square, circle, ds_m).scale(0.7)
        vgroup.move_to(ORIGIN)

        self.add(circle, square, triangle)

        shape_center = VGroup(circle, square, triangle).get_center()

        spiral_run_time = 2.1
        expansion_factor = 8
        m_height_over_anim_height = 0.75748
        m_shape_offset = 4.37
        m_anim_buff = 0.06

        tracker = ValueTracker(0)

        for mob in [circle, square, triangle]:
            mob.final_position = mob.get_center()
            mob.initial_position = (
                mob.final_position
                + (mob.final_position - shape_center) * expansion_factor
            )
            mob.initial_to_final_distance = np.linalg.norm(
                mob.final_position - mob.initial_position
            )
            mob.move_to(mob.initial_position)
            mob.current_time = 0
            mob.starting_mobject = mob.copy()

            def updater(mob, dt):
                mob.become(mob.starting_mobject)
                mob.shift(
                    normalize((shape_center - mob.get_center()))
                    * mob.initial_to_final_distance
                    * tracker.get_value()
                )
                mob.rotate(TAU * tracker.get_value(), about_point=shape_center)
                mob.rotate(-TAU * tracker.get_value())

            mob.add_updater(updater)

        self.play(tracker.set_value, 1, run_time=spiral_run_time)

        circle.clear_updaters()
        square.clear_updaters()
        triangle.clear_updaters()

        self.wait(0.3)

        self.play(FadeIn(ds_m), rate_func=rate_functions.ease_in_sine)
        self.wait(0.7)

        ds_m_target = ds_m.generate_target()
        circle_target = circle.generate_target().shift(RIGHT * m_shape_offset)
        square_target = square.generate_target().shift(RIGHT * m_shape_offset)
        triangle_target = triangle.generate_target().shift(RIGHT * m_shape_offset)

        anim = VGroup()
        for i, ch in enumerate("anim"):
            tex = Tex(
                "\\textbf{" + ch + "}",
                z_index=10,
                tex_template=TexFontTemplates.gnu_freeserif_freesans,
            )
            if i != 0:
                tex.next_to(anim, buff=0.01)
            tex.align_to(ds_m, DOWN)
            anim.add(tex)

        anim.set_color(logo_black) \
            .set_height(m_height_over_anim_height * ds_m.get_height()) \
            .next_to(ds_m_target, buff=m_anim_buff) \
            .align_to(ds_m, DOWN)

        banner = VGroup(
            ds_m_target, anim, circle_target, square_target, triangle_target
        )
        banner.move_to(ORIGIN)

        ds_m_offset_vec = ds_m_target.get_center() - ds_m.get_center()

        self.play(
            circle.shift,
            ds_m_offset_vec,
            square.shift,
            ds_m_offset_vec,
            triangle.shift,
            ds_m_offset_vec,
            ds_m.shift,
            ds_m_offset_vec,
        )

        tracker.set_value(0)
        shape_center = VGroup(circle, square, triangle).get_center()
        for mob in [circle, square, triangle]:
            mob.starting_mobject = mob.copy()
            mob.shape_center_offset = mob.get_center() - shape_center

            def updater(mob, dt):
                center = shape_center + RIGHT * tracker.get_value() * m_shape_offset
                mob.become(mob.starting_mobject)
                mob.move_to(center + mob.shape_center_offset)

            mob.add_updater(updater)

        self.play(
            tracker.set_value,
            1,
            FadeIn(anim, lag_ratio=1),
        )
        anim.z_index = 20
        self.wait(1)
