import manim as mn
import numpy as np

def regular_vertices(n, *, radius=1, start_angle=None):
    if start_angle is None:
        if n % 2 == 0:
            start_angle = 0
        else:
            start_angle = mn.TAU / 4

    start_vector = mn.rotate_vector(mn.RIGHT * radius, start_angle)
    vertices     = mn.compass_directions(n, start_vector)

    return vertices, start_angle

class Star(mn.Polygon):
    def __init__(self, n=5, *, density=2, outer_radius=1, inner_radius=None, start_angle=None, **kwargs):
        if density <= 0 or density >= n / 2:
            raise ValueError(f"Incompatible density {density}")

        inner_angle = mn.TAU / (2 * n)

        if inner_radius is None:
            # Calculate the inner radius for n and density.
            # See https://math.stackexchange.com/a/2136292

            outer_angle = mn.TAU * density / n

            inverse_x = 1 - np.tan(inner_angle) * ((np.cos(outer_angle) - 1) / np.sin(outer_angle))

            inner_radius = outer_radius / (np.cos(inner_angle) * inverse_x)

        outer_vertices, self.start_angle = regular_vertices(n, radius=outer_radius, start_angle=start_angle)
        inner_vertices, _                = regular_vertices(n, radius=inner_radius, start_angle=self.start_angle + inner_angle)

        vertices = []
        for pair in zip(outer_vertices, inner_vertices):
            vertices.extend(pair)

        super().__init__(*vertices, **kwargs)

class ModularMultiplier(mn.Group):
    def __init__(self, mobject, *, modulus, factor, rate_func=mn.linear, line_config=None, **kwargs):
        super().__init__(**kwargs)

        self.mobject   = mobject.copy()
        self.modulus   = modulus
        self.factor    = mn.ValueTracker(factor)
        self.rate_func = rate_func

        self.add(self.mobject)

        if line_config is None:
            line_config = {}

        self.line_config = line_config
        self.init_lines()
        mn.always(self.update_lines)

    def number_to_point(self, n):
        n %= self.modulus
        n /= self.modulus

        return self.mobject.point_from_proportion(self.rate_func(n))

    def n2p(self, n):
        return self.number_to_point(n)

    def init_lines(self):
        self.lines = mn.VGroup()
        self.add_to_back(self.lines)

        factor = self.factor.get_value()
        for n in range(self.modulus):
            n_point    = self.n2p(n)
            mult_point = self.n2p(n * factor)

            line = mn.Line(n_point, mult_point, **self.line_config)
            self.lines.add(line)

    def update_lines(self):
        factor = self.factor.get_value()

        for n, line in enumerate(self.lines):
            n_point    = self.n2p(n)
            mult_point = self.n2p(n * factor)

            line.set_start_and_end_attrs(n_point, mult_point)
            line.generate_points()

class ModularScene(mn.Scene):
    def construct(self):
        mod = ModularMultiplier(
            Star(outer_radius=3, color=mn.BLUE),

            modulus = 300,
            factor  = 1,

            line_config = {
                "stroke_width": 1,
            },
        )

        mod_var    = mn.Tex("Modulus", "$=$", f"${mod.modulus}$")
        factor_var = mn.Variable(mod.factor.get_value(), mn.Tex("Factor"))

        # Arrange mod_var so it lines up well with factor_var's elements
        mod_var[2].align_to(factor_var, mn.UR)
        mod_var[1].next_to(factor_var.label[0], mn.RIGHT)
        mod_var[0].next_to(mod_var[1], mn.LEFT)
        mod_var.shift((factor_var.height + 0.25) * mn.UP)

        factor_var.add_updater(lambda v: v.tracker.set_value(mod.factor.get_value()))

        info = mn.VGroup(mod_var, factor_var)
        info.to_corner(mn.UR)

        self.add(info, mod)

        self.animate_factors(mod, [2, 1])

    def animate_factors(self, mod, iterable, *, wait=0.3, run_time=2, **kwargs):
        for f in iterable:
            self.play(mod.factor.animate.set_value(f), run_time=run_time, **kwargs)
            self.wait(wait)
