from manim import *
import pkg_resources

version_num = "0.1.1"


class Ball(LabeledDot):
    def __init__(self, lable=r"\alpha", **kwargs):
        LabeledDot.__init__(
            self, lable, radius=0.4, fill_opacity=1, color=BLUE, **kwargs
        )
        self.velocity = np.array((2, 1.5, 0))

    def get_top(self):
        return self.get_center()[1] + self.radius

    def get_bottom(self):
        return self.get_center()[1] - self.radius

    def get_right_edge(self):
        return self.get_center()[0] + self.radius

    def get_left_edge(self):
        return self.get_center()[0] - self.radius


class Box(Rectangle):
    def __init__(self, **kwargs):
        Rectangle.__init__(self, height=6, width=8, color=GREEN_C, **kwargs)  # Edges
        self.top = 0.5 * self.height
        self.bottom = -0.5 * self.height
        self.right_edge = 0.5 * self.width
        self.left_edge = -0.5 * self.width


class TwitterScene(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        version = Tex(f"v{version_num}").to_corner(UR).set_color(BLACK)
        self.add(version)

        box = Box()
        ball = Ball(lable=Text("v0.1.1").scale(0.3))
        self.add(box)
        self.play(Write(ball))

        def update_ball(ball, dt):
            ball.acceleration = np.array((0, -5, 0))
            ball.velocity = ball.velocity + ball.acceleration * dt
            ball.shift(ball.velocity * dt)  # Bounce off ground and roof
            if ball.get_bottom() <= box.bottom or ball.get_top() >= box.top:
                ball.velocity[1] = -ball.velocity[1]
            # Bounce off walls
            if (
                ball.get_left_edge() <= box.left_edge
                or ball.get_right_edge() >= box.right_edge
            ):
                ball.velocity[0] = -ball.velocity[0]

        ball.add_updater(update_ball)
        self.add(ball)

        ball2 = Ball(lable=r"\Psi")
        self.play(Write(ball2))
        ball2.add_updater(update_ball)

        ball3 = Ball(lable=r"\alpha")
        self.play(Write(ball3))
        ball3.add_updater(update_ball)

        ball4 = Ball(lable=r"\lambda")
        self.play(Write(ball4))
        ball4.add_updater(update_ball)

        self.wait(3)
        cu1 = Cutout(
            box,
            ball,
            ball2,
            ball3,
            ball4,
            fill_opacity=0.2,
            color=GREY,
            stroke_color=RED,
        )
        self.add(cu1)
        cu1_small = cu1.copy().scale(0.3).to_edge(RIGHT).shift(2 * UP)
        self.play(Transform(cu1, cu1_small))

        cu2 = Cutout(
            box,
            ball,
            ball2,
            ball3,
            ball4,
            fill_opacity=0.2,
            color=GREY,
            stroke_color=RED,
        )
        self.add(cu2)
        cu2_small = cu2.copy().scale(0.3).to_edge(RIGHT)
        self.play(Transform(cu2, cu2_small))

        self.wait()
        #
        banner = ManimBanner(dark_theme=False).scale(0.3).to_corner(DR)
        self.play(*[FadeOut(x) for x in self.mobjects], FadeIn(banner), run_time=2.5)
        self.play(banner.expand())
        self.wait()
