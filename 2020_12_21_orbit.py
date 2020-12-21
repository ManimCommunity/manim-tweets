import numpy as np
from manim import *

ORBIT_WIDTH = 3.2
ORBIT_HEIGHT = 0.4
PATH_SCALE_FACTOR = 0.5
ORBIT_RATE = 0.23
WAIT_TIME = 20
EARTH_START_PROPORTION = 0.738
SUN_MOVEMENT_RATE = 1.1
CAMERA_LAG_TIME = 3.4
DIAGRAM_STROKE_WIDTH = 2
# EARTH_SUN_X_DISPLACEMENT_MIN = -1.637
EARTH_SUN_X_DISPLACEMENT_MIN = -1.6094
# EARTH_SUN_X_DISPLACEMENT_MAX = 1.561
EARTH_SUN_X_DISPLACEMENT_MAX = 1.5904
LABEL_SCALE_FACTOR = 0.35
ARROW_SCALE_FACTOR = 0.4


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class DraftScene(MovingCameraScene):
    def construct(self):
        # Earth
        orbit_path = Ellipse(
            width=ORBIT_WIDTH,
            height=ORBIT_HEIGHT,
            stroke_opacity=0,
        )
        self.add(orbit_path)  # TODO: Remove this

        v = ValueTracker()
        earth = Dot(color=BLUE, stroke_opacity=0).move_to(
            orbit_path.point_from_proportion(EARTH_START_PROPORTION)
        )

        def orbit(earth):
            alpha = (EARTH_START_PROPORTION + v.get_value() * ORBIT_RATE) % 1
            earth.move_to(orbit_path.point_from_proportion(alpha))

        earth.add_updater(orbit)
        self.add(earth)

        # Earth trail
        last_earth_sun_distance = 0

        def trail_earth(path, dt):
            path.add_line_to(earth.get_center())

            # Update the camera here, since updaters can't be added to the
            # camera.
            if v.get_value() >= CAMERA_LAG_TIME:
                self.camera_frame.shift(
                    normalize(sun_shift_direction) * SUN_MOVEMENT_RATE * dt
                )

            earth_sun_x_displacement = (sun.get_center() - earth.get_center())[0]

            # if (
            #     abs(earth_sun_x_displacement - EARTH_SUN_X_DISPLACEMENT_MIN) < 0.001
            #     or abs(earth_sun_x_displacement - EARTH_SUN_X_DISPLACEMENT_MAX) < 0.0015
            # ):
            if (
                earth_sun_x_displacement < EARTH_SUN_X_DISPLACEMENT_MIN
                or earth_sun_x_displacement > EARTH_SUN_X_DISPLACEMENT_MAX
            ):
                diagram = VGroup()
                ellipse = Ellipse(
                    width=ORBIT_WIDTH,
                    height=ORBIT_HEIGHT,
                    stroke_opacity=1,
                    stroke_color=WHITE,
                    stroke_width=DIAGRAM_STROKE_WIDTH,
                ).move_to(orbit_path.get_center())

                sun_dot = Dot(
                    color=WHITE, fill_opacity=0, stroke_width=DIAGRAM_STROKE_WIDTH
                ).move_to(ellipse.get_center())

                sun_shine = VGroup()
                for theta in np.linspace(0, 2 * PI, num=8, endpoint=False):
                    shine = Line(
                        start=sun_dot.get_center() + sun_dot.radius * RIGHT,
                        end=sun_dot.get_center() + (sun_dot.radius + 0.07) * RIGHT,
                        stroke_width=DIAGRAM_STROKE_WIDTH,
                    )
                    shine.rotate(theta, about_point=sun_dot.get_center())
                    sun_shine.add(shine)

                earth_dot = Dot(
                    color=WHITE, fill_opacity=0, stroke_width=DIAGRAM_STROKE_WIDTH
                ).move_to(earth.get_center())

                earth_axis_tilt_direction = normalize(UP * 1.5 + LEFT)
                earth_axis = Line(
                    start=earth.get_center() + earth_axis_tilt_direction * 0.15,
                    end=earth.get_center() - earth_axis_tilt_direction * 0.15,
                    stroke_width=DIAGRAM_STROKE_WIDTH,
                )
                self.add(earth_axis)

                earth_label = VGroup()
                if earth_sun_x_displacement < 0:
                    date_tex = Tex(
                        "JUNE 21", tex_template=TexFontTemplates.american_typewriter
                    )
                    earth_tex = Tex(
                        "EARTH", tex_template=TexFontTemplates.american_typewriter
                    ).next_to(date_tex, DOWN)
                    earth_label.add(date_tex, earth_tex)
                    earth_label.scale(LABEL_SCALE_FACTOR)
                    earth_label.next_to(earth, RIGHT, buff=0.1)
                else:
                    earth_tex = Tex(
                        "EARTH", tex_template=TexFontTemplates.american_typewriter
                    )
                    date_tex = Tex(
                        "DEC 21", tex_template=TexFontTemplates.american_typewriter
                    ).next_to(earth_tex, DOWN)
                    earth_label.add(date_tex, earth_tex)
                    earth_label.scale(LABEL_SCALE_FACTOR)
                    earth_label.next_to(earth, LEFT, buff=0.1)
                earth_north = (
                    Tex("N", tex_template=TexFontTemplates.american_typewriter)
                    .scale(LABEL_SCALE_FACTOR)
                    .next_to(earth_dot, earth_axis_tilt_direction, buff=0.1)
                )
                earth_north.shift(RIGHT * 0.15)

                sun_label = (
                    Tex("SUN", tex_template=TexFontTemplates.american_typewriter)
                    .scale(LABEL_SCALE_FACTOR)
                    .next_to(sun, LEFT, buff=0.04)
                )
                sun_label.shift(UP * 0.07)

                arrows = VGroup()
                right_arrow = Arrow(
                    start=LEFT, end=RIGHT * 0.3, stroke_width=DIAGRAM_STROKE_WIDTH
                )
                VMobject.scale(right_arrow, ARROW_SCALE_FACTOR)
                right_arrow.next_to(ellipse, DOWN, buff=0.1)
                right_arrow.shift(RIGHT * 0.1)
                arrows.add(right_arrow)

                left_arrow = Arrow(
                    start=RIGHT, end=LEFT * 0.3, stroke_width=DIAGRAM_STROKE_WIDTH
                )
                VMobject.scale(left_arrow, ARROW_SCALE_FACTOR)
                left_arrow.next_to(ellipse, UP, buff=0.1)
                left_arrow.shift(LEFT * 0.1)
                arrows.add(left_arrow)

                diagram.add(
                    ellipse,
                    sun_dot,
                    earth_dot,
                    earth_label,
                    sun_label,
                    arrows,
                    sun_shine,
                    earth_north,
                )
                self.add(diagram)

            earth_orbit_alpha = (
                EARTH_START_PROPORTION + v.get_value() * ORBIT_RATE
            ) % 1

            if any(
                # abs(earth_orbit_alpha - x) < 0.0075 # low quality
                abs(earth_orbit_alpha - x) < 0.0019
                for x in [0.15 + 0.25 * x for x in [0, 1, 2, 3]]
            ):
                line1 = Line(
                    start=sun.get_center(),
                    end=sun.get_center()
                    + 0.6 * rotate_vector(-sun_shift_direction, -PI / 8),
                    stroke_width=DIAGRAM_STROKE_WIDTH,
                )
                line2 = Line(
                    start=sun.get_center(),
                    end=sun.get_center()
                    + 0.6 * rotate_vector(-sun_shift_direction, PI / 8),
                    stroke_width=DIAGRAM_STROKE_WIDTH,
                )
                arrow = VGroup(line1, line2)
                self.add(arrow)

            # Don't label March when the animation first starts.
            if v.get_value() < 0.3:
                return

            # if abs(earth_orbit_alpha - 0.3) < 0.007: # low quality
            if abs(earth_orbit_alpha - 0.3) < 0.0019:  # low quality
                self.add(
                    Tex(
                        "SETPEMBER 23",
                        tex_template=TexFontTemplates.american_typewriter,
                    )
                    .scale(LABEL_SCALE_FACTOR)
                    .next_to(earth, RIGHT, buff=0.1)
                    .shift(RIGHT * 0.5 + DOWN * 0.2)
                )
            # elif abs(earth_orbit_alpha - 0.8) < 0.008: # low quality
            elif abs(earth_orbit_alpha - 0.8) < 0.002:  # low quality
                self.add(
                    Tex(
                        "MARCH 21",
                        tex_template=TexFontTemplates.american_typewriter,
                    )
                    .scale(LABEL_SCALE_FACTOR)
                    .next_to(earth, LEFT, buff=0.1)
                    .shift(LEFT * 0.6 + DOWN * 0.15)
                )

        earth_trail = VMobject(stroke_width=DIAGRAM_STROKE_WIDTH)
        earth_trail.points = np.array([earth.get_center()])
        earth_trail.add_updater(trail_earth)
        self.add(earth_trail)

        # Sun
        sun_shift_direction = ORIGIN - earth.get_center()
        sun = Dot(color=YELLOW)
        always_shift(sun, normalize(sun_shift_direction), rate=SUN_MOVEMENT_RATE)
        always_shift(orbit_path, normalize(sun_shift_direction), rate=SUN_MOVEMENT_RATE)
        self.add(sun)

        # Sun trail
        original_earth_center = earth.get_center()
        sun_trail = Line(
            original_earth_center, sun.get_center(), stroke_width=DIAGRAM_STROKE_WIDTH
        )

        def trail_sun(trail):
            trail.put_start_and_end_on(original_earth_center, sun.get_center())

        sun_trail.add_updater(trail_sun)
        self.add(sun_trail)

        self.play(v.set_value, WAIT_TIME, run_time=WAIT_TIME, rate_func=linear)
