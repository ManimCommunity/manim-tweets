from manim import *


def lissajous_curve_func(t):
    return np.array((np.sin(3 * t), np.sin(4 * t) + 2 / 3 * PI, 0))


class TwitterScene(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        dot = Dot()
        dummy_func = ParametricFunction(lissajous_curve_func, t_max=TAU, fill_opacity=0)
        dummy_func.scale(2).move_to(ORIGIN)
        func1 = dummy_func.copy().set_stroke(width=18)
        func1 = CurvesAsSubmobjects(func1)
        func1.set_color_by_gradient(YELLOW_A, YELLOW_D)
        func2 = dummy_func.copy().set_color(BLACK).set_stroke(width=20)
        dot.add_updater(lambda m: m.move_to(dummy_func.get_end()))
        dummy_func.set_opacity(0)
        # or dummy_func.fade(1) )
        self.add(dot)
        self.play(
            ShowCreation(dummy_func),
            ShowCreation(func2),
            ShowCreation(func1),
            rate_func=linear,
            run_time=9,
        )
        self.add(func1)
        self.wait()
        banner = ManimBanner(dark_theme=False).scale(0.3).to_corner(DR)
        self.play(FadeIn(banner))
        self.play(banner.expand())
        self.wait(3)
