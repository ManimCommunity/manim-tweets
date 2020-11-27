from manim import *
import colour


NUM_DOTS = 250
FALL_TIME = 1
RUNTIME = 2.5
RED = "#FF4040"
BLUE = "#4040FF"


class EventMobject(VGroup):
    def __init__(self, probability, label, color=WHITE, y_coordinate=0):
        super().__init__()
        line = Line(
            start=LEFT * probability * config["frame_width"] * 0.5,
            end=RIGHT * probability * config["frame_width"] * 0.5,
            stroke_width=12,
            color=color,
        )
        label = Tex(label, color=color).next_to(line, direction=DOWN)

        self.line = line
        self.label = label
        self.event_color = color

        self.add(self.line, self.label)

    def put_start_and_end_on(self, start, end):
        self.line.put_start_and_end_on(start, end)
        self.label.next_to(self.line, direction=DOWN)

    def set_label(self, label):
        self.label = Tex(label, color=self.event_color)
        self.submobjects[1] = self.label

    def set_color(self, color):
        super().set_color(color)
        self.event_color = color


class Label(VDict):
    def __init__(self, label, color=BLUE):
        super().__init__()
        tex = Tex(label, color=color)
        label_background = Rectangle(
            height=tex.get_height() + MED_SMALL_BUFF,
            width=tex.get_width() + MED_SMALL_BUFF,
            stroke_opacity=0,
            fill_color=BLACK,
            fill_opacity=1,
        ).move_to(tex.get_center())
        self.add({"background": label_background, "tex": tex})


class DraftScene(Scene):
    def construct(self):
        event_a = EventMobject(0.7, "$A$", color=BLUE).shift(
            UP * 0.1 * config["frame_height"]
        )
        events = [event_a]

        p_a = Label("P($A$)").to_corner(UP + RIGHT)

        self.add(event_a, p_a)
        self.wait(0.5)

        self.raindrop_scene(events, p_a)

        p_not_a = Label("P($\\neg A$)").to_corner(UP + RIGHT)

        self.play(
            event_a.set_color,
            WHITE,
            FadeOutAndShift(p_a),
            FadeInFrom(p_not_a, UP),
        )

        event_a.event_color = WHITE
        self.raindrop_scene(events, p_not_a, default_dot_color=BLUE)

        event_a_target = event_a.generate_target()
        event_a_target.put_start_and_end_on(
            UP * 0.2 * config["frame_height"]
            + LEFT * (0.5 * config["frame_width"] - 1),
            UP * 0.2 * config["frame_height"] + RIGHT * 2.5,
        )
        event_a_target.set_color(BLUE)

        event_b = event_a_target.copy()
        event_b.set_label("$B$")
        event_b.put_start_and_end_on(
            UP * 0.0 * config["frame_height"]
            + RIGHT * (0.5 * config["frame_width"] - 1),
            UP * 0.0 * config["frame_height"] + LEFT * 2.5,
        )
        events.append(event_b)
        p_a_or_b = Label("P($A \\cup B$)").to_corner(UP + RIGHT)

        self.play(
            MoveToTarget(event_a),
            FadeIn(event_b),
            FadeOutAndShift(p_not_a),
            FadeInFrom(p_a_or_b, UP),
        )
        event_a.event_color = BLUE
        self.raindrop_scene(events, p_a_or_b)

        p_a_and_b = Label(
            "P($A \\cap B$)", color=interpolate_color(BLUE, RED, 0.5)
        ).to_corner(UP + RIGHT)
        self.play(
            event_b.set_color,
            RED,
            FadeOutAndShift(p_a_or_b),
            FadeInFrom(p_a_and_b, UP),
        )
        event_b.event_color = RED

        self.raindrop_scene(events, p_a_and_b)

        p_a_given_b = Label(
            "P($A \\mid B$)", color=interpolate_color(BLUE, RED, 0.5)
        ).to_corner(UP + RIGHT)

        event_b_target = event_b.generate_target()
        event_b_target.put_start_and_end_on(
            UP * event_b.line.get_center()[1] + RIGHT * 0.5 * config["frame_width"],
            UP * event_b.line.get_center()[1] + LEFT * 0.5 * config["frame_width"],
        )

        # Scale both events by the same amount.
        event_b_growth_ratio = (
            event_b_target.line.get_length() / event_b.line.get_length()
        )
        event_a_offset = event_a.line.get_right()[0] - event_b.line.get_right()[0]

        event_a_target = event_a.generate_target()
        event_a_right = UP * event_a.line.get_center()[1] + RIGHT * (
            event_b_target.line.get_right()[0] + event_a_offset * event_b_growth_ratio
        )
        event_a_target.put_start_and_end_on(
            event_a_right + LEFT * event_b_target.line.get_length(),
            event_a_right,
        )
        event_a_target.label.move_to(
            UP * event_a.label.get_center()[1]
            + RIGHT
            * (event_a_target.get_right()[0] - config["frame_width"] * 0.5)
            * 0.5
        )

        self.play(
            FadeOutAndShift(p_a_and_b),
            FadeInFrom(p_a_given_b, UP),
            MoveToTarget(event_b),
            MoveToTarget(event_a),
        )

        self.raindrop_scene(events, p_a_given_b)

        self.wait()

    def raindrop_scene(self, events, label, default_dot_color=WHITE):
        upper_left_corner = (
            UP * 0.5 * config["frame_height"] + LEFT * 0.5 * config["frame_width"]
        )

        tracker = ValueTracker(0)
        tracker.add_updater(lambda t, dt: t.increment_value(dt))
        self.add(tracker)

        # Reach the bottom of the screen in 1 second
        falling_rate = config["frame_height"] / FALL_TIME

        def fall(dot, dt):
            if tracker.get_value() < dot.falling_delay:
                return
            old_center = dot.get_center()
            dot.shift(DOWN * falling_rate * dt)
            new_center = dot.get_center()

            for event in events:
                if (
                    event.get_left()[0] < old_center[0]
                    and old_center[0] < event.get_right()[0]
                    and new_center[1] < event.line.get_center()[1]
                    and event.line.get_center()[1] < old_center[1]
                ):
                    dot_color = np.array(color.Color(dot.get_color()).get_rgb())
                    event_color = np.array(color.Color(event.event_color).get_rgb())
                    dot.color_array.append(event_color)
                    new_color = interpolate(
                        dot_color, event_color, 1 / len(dot.color_array)
                    )
                    dot.set_color(colour.Color(rgb=new_color))

        for _ in range(NUM_DOTS):
            dot = Dot(color=default_dot_color).move_to(
                upper_left_corner + random.random() * RIGHT * config["frame_width"]
            )
            dot.shift(UP * dot.radius)
            dot.falling_delay = random.random() * RUNTIME
            dot.color_array = []
            dot.add_updater(fall)
            self.add(dot)

        self.add(*events)
        self.add(label)
        self.wait(RUNTIME + FALL_TIME)
