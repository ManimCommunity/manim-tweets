from manim import *


class V040(Scene):
    def construct(self):
        self.camera.background_color = "#ece6e2"
        positions = VGroup(*[Dot() for _ in range(6)])
        positions.arrange_in_grid(n_rows=2, n_cols=3, buff=4)

        assets_path = "assets/2021_03_04/"
        world = SVGMobject(assets_path + "world.svg").scale(3)
        self.play(DrawBorderThenFill(world))
        self.wait(0.5)
        self.play(world.animate.scale(0.4).move_to(positions[0]))

        rocket = SVGMobject(assets_path + "rocket-2.svg").scale(2)
        self.play(DrawBorderThenFill(rocket))
        self.wait(0.5)
        self.play(rocket.animate.scale(0.5).move_to(positions[1]))

        blivet = SVGMobject(assets_path + "Blivet2.svg").scale(2)
        self.play(DrawBorderThenFill(blivet))
        self.wait(0.5)
        self.play(blivet.animate.scale(0.5).move_to(positions[2]))

        tree = SVGMobject(assets_path + "tree.svg").scale(2.5)
        self.play(DrawBorderThenFill(tree))
        self.wait(0.5)
        self.play(tree.animate.scale(0.75).move_to(positions[3]))

        knot = SVGMobject(assets_path + "present.svg").scale(1.5)
        self.play(DrawBorderThenFill(knot))
        self.wait(0.5)
        self.play(knot.animate.scale(0.75).move_to(positions[4]))

        banner = ManimBanner(dark_theme=False).scale(0.3).move_to(positions[5])
        banner.shift(RIGHT)
        self.play(FadeIn(banner))
        self.play(banner.expand())
        version = Tex(
            "\\textbf{v0.4.0}",
            tex_template=TexFontTemplates.gnu_freeserif_freesans,
        )
        version = (
            version.next_to(banner, DOWN).align_to(banner, RIGHT).set_color("#343434")
        )
        self.play(Write(version))
        self.wait(1)

        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.wait(0.5)
