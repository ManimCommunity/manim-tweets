from manim import *


class Pendulum(VGroup):
    def phi_function(self, amplitude, acceleration, length, time):
        return amplitude * np.sin(np.sqrt(acceleration / length) * time - np.pi / 2)

    def __init__(self, weight, amplitude, acceleration, length, time):
        VGroup.__init__(self)
        self.sound_stamps_there = []
        self.sound_stamps_back = []

        self.amplitude = amplitude
        self.acceleration = acceleration
        self.length = length
        self.time = time
        self.phi = self.phi_function(amplitude, acceleration, length, time)
        self.anchor = Dot(ORIGIN)
        self.line = Line(ORIGIN, length * DOWN)
        self.line.rotate(self.phi * DEGREES, about_point=self.line.get_start())
        self.mass = LabeledDot(label=f"{weight}" + r"\, \text{kg}").scale(0.3)
        self.mass.move_to(self.line.get_end())
        self.mobj = VGroup(self.line, self.anchor, self.mass)
        self.add(self.mobj)

    def start(self):
        self.mobj.current_time = 0.000001

        def updater(mob, dt):
            mob.current_time += dt
            new_phi = self.phi_function(self.amplitude, self.acceleration, self.length, mob.current_time)
            mob[0].rotate( (new_phi - self.phi) * DEGREES, about_point=self.line.get_start() )
            if np.sign(self.phi) < np.sign(new_phi):
                self.sound_stamps_there.append(mob.current_time)
            if np.sign(self.phi) > np.sign(new_phi):
                self.sound_stamps_back.append(mob.current_time)

            self.phi = new_phi
            self.mass.move_to(self.line.get_end())

        self.mobj.add_updater(updater)