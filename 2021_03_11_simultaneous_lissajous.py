from manim import *


class Lissajous(Scene):
    def construct(self):
        # Simultaneous lissajous curves.
        lissajous_size = 2
        lissajous_a = 1
        lissajous_b = 1
        lissajous_delta = PI / 4
        lissajous_rate = 5
        lissajous_alpha = ValueTracker()
        offset = PI / 2

        def lissajous_location(t, delta):
            A = lissajous_size
            a = lissajous_a
            b = lissajous_b
            x = A * np.sin(a * t + offset)
            y = A * np.sin(b * t + delta + offset)
            return x * RIGHT + y * UP

        def get_line_length(mob):
            length = 0
            start_anchors = mob.get_start_anchors()
            for i in range(len(start_anchors) - 1):
                length += get_norm(start_anchors[i + 1] - start_anchors[i])
            return length

        def grow_line(mob):
            new_position = lissajous_location(
                lissajous_alpha.get_value() * mob.rate, mob.delta
            )

            # Update line length.
            mob.add_line_to(new_position)
            mob.line_length += get_norm(new_position - mob.points[-1])

            while get_line_length(mob) > mob.maximum_length:
                mob.set_points(mob.points[4:])

        def get_lissajous_line(delta, rate):
            line = VMobject()
            line.delta = delta
            line.line_length = 0
            line.maximum_length = 8
            line.rate = rate
            line.points = np.array([lissajous_location(0, line.delta)])
            line.add_updater(grow_line)
            return line

        self.add(get_lissajous_line(1 * PI / 8, 1).set_color(RED))
        self.add(get_lissajous_line(2 * PI / 8, 2).set_color(ORANGE))
        self.add(get_lissajous_line(3 * PI / 8, 3).set_color(YELLOW))
        self.add(get_lissajous_line(4 * PI / 8, 4).set_color(GREEN))
        self.add(get_lissajous_line(5 * PI / 8, 5).set_color(BLUE))
        self.add(get_lissajous_line(6 * PI / 8, 6).set_color(BLUE_B))
        self.add(get_lissajous_line(7 * PI / 8, 7).set_color(PURPLE))

        self.play(lissajous_alpha.animate.set_value(20), run_time=32, rate_func=linear)
