from manim import *


class Pendulum(VGroup):
    def phi_fun(self, amplitude, acceleration, length, time):
        return amplitude * np.sin(np.sqrt(acceleration / length) * time - np.pi / 2)

    def __init__(self, weight, amplitude, acceleration, length, time):
        VGroup.__init__(self)
        self.sound_stamps_there = []
        self.sound_stamps_back = []

        self.amplitude = amplitude
        self.acceleration = acceleration
        self.length = length
        self.time = time
        self.phi = self.phi_fun(amplitude, acceleration, length, time)
        self.anchor = Dot(ORIGIN, color=RED)
        self.line = Line(
            ORIGIN, length * 1.8 * DOWN, stroke_width=1.6, stroke_opacity=0.2
        )
        self.line.rotate(self.phi * DEGREES, about_point=self.line.get_start())
        self.mass = Dot().set_color(BLUE).scale(1.4)
        self.mass.move_to(self.line.get_end())
        self.mobj = VGroup(self.line, self.anchor, self.mass)
        self.add(self.mobj)

    def start(self):
        self.mobj.current_time = 0.000001

        def updater(mob, dt):
            mob.current_time += dt
            old_phi = self.phi_fun(
                self.amplitude,
                self.acceleration,
                self.length,
                mob.current_time - 2 * dt,
            )
            new_phi = self.phi_fun(
                self.amplitude, self.acceleration, self.length, mob.current_time
            )
            mob[0].rotate(
                (new_phi - self.phi) * DEGREES, about_point=self.line.get_start()
            )
            if (old_phi > self.phi) & (
                self.phi < new_phi
            ):  # only used when sound is added.
                self.sound_stamps_there.append(mob.current_time)
            if (old_phi < self.phi) & (self.phi > new_phi):
                self.sound_stamps_there.append(mob.current_time)

            self.phi = new_phi
            self.mass.move_to(self.line.get_end())

        self.mobj.add_updater(updater)


class PendulumScene(Scene):
    def construct(self):
        g = 10
        oszilations = np.array([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        period_length = 30
        times = 1 / oszilations * period_length
        lengths = (times / (2 * PI)) ** 2 * g
        total = len(lengths)
        pendulums1 = []
        for i, val in enumerate(lengths):
            pendulum = Pendulum(
                weight=1, amplitude=32, acceleration=g, length=val, time=0
            )
            if i % 2 == 0:
                pendulum.mass.set_color(GREEN)
            anchor_pos = pendulum.anchor.get_center()
            dest_pos = (-total / 2 + i) * 0.6 * RIGHT + 3.5 * UP
            pendulum.shift(anchor_pos + dest_pos)
            pendulums1.append(pendulum)
            self.add(pendulum)
        pendulums2 = []
        for i, val in enumerate(lengths):
            pendulum = Pendulum(
                weight=1, amplitude=32, acceleration=10, length=val, time=0
            )
            if i % 2 == 0:
                pendulum.mass.set_color(GREEN)
            anchor_pos = pendulum.anchor.get_center()
            dest_pos = 3.5 * UP
            pendulum.shift(anchor_pos + dest_pos)
            pendulums2.append(pendulum)
        self.wait()
        self.play(Transform(VGroup(*pendulums1), VGroup(*pendulums2)))
        self.wait(1)
        for el in pendulums1:
            el.start()
        self.wait(35)
        banner = ManimBanner(dark_theme=True).scale(0.3).to_corner(DR)
        self.play(FadeIn(banner))
        self.play(banner.expand())
        self.wait(30)
