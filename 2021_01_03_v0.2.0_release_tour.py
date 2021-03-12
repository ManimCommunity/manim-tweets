from manim import *


class ReleaseV020(Scene):
    def construct(self):
        banner = ManimBanner().scale(0.35).to_edge(UP, buff=0.25).shift(RIGHT * 1.09375)
        self.play(FadeIn(banner))
        self.play(banner.expand())
        release_tour = MarkupText("<tt>v0.2.0</tt> Release Tour")
        release_tour.next_to(banner, DOWN)
        self.play(Write(release_tour))
        self.wait(1)
        boxes = [Square(side_length=config.frame_height / 3) for _ in range(6)]
        boxes_left = VGroup(*boxes[:3]).arrange(DOWN, buff=0).to_edge(LEFT, buff=0)
        boxes_right = VGroup(*boxes[3:]).arrange(DOWN, buff=0).to_edge(RIGHT, buff=0)
        self.play(AnimationGroup(*[FadeIn(box) for box in boxes], lag_ratio=0.1))

        content_0 = (
            VGroup(
                MarkupText(
                    '<tt>CONFIG</tt> dicts have been <b><color col="red">removed!</color></b>'
                ).scale(0.7),
                Code("assets/2021_01_03/config_old.py"),
                MarkupText("is now written as").scale(0.5),
                Code("assets/2021_01_03/config_new.py"),
            )
            .arrange(DOWN)
            .to_edge(DOWN, buff=0.25)
        )
        self.play(Write(content_0), run_time=4)
        self.wait(1.5)
        self.play(content_0.animate.scale(0.27).move_to(boxes[0].get_center()))
        self.wait(0.25)

        content_1 = (
            VGroup(
                MarkupText("New <tt>.animate</tt> syntax for method animations!").scale(
                    0.7
                ),
                Code("assets/2021_01_03/methodanim_old.py"),
                MarkupText("is now written as").scale(0.5),
                Code("assets/2021_01_03/methodanim_new.py"),
                Square(fill_color="#525893", fill_opacity=1),
            )
            .scale(0.8)
            .arrange(DOWN)
            .to_edge(DOWN, buff=0.25)
        )
        self.play(Write(content_1), run_time=3)
        self.wait(0.5)
        self.play(content_1[-1].animate.scale(0.65).rotate(-PI / 4))
        self.wait(1.5)
        self.play(content_1.animate.scale(0.27).move_to(boxes[1].get_center()))
        self.wait(0.25)

        content_2 = (
            Group(
                VGroup(
                    MarkupText("<b>New feature:</b> plugin system!").scale(0.7),
                    MarkupText(
                        "Discover @ <tt>https://plugins.manim.community</tt>"
                    ).scale(0.5),
                    MarkupText("Example: <tt>manim-rubikscube</tt>").scale(0.5),
                ).arrange(DOWN),
                ImageMobject("assets/2021_01_03/rubikscube.png"),
            )
            .arrange(DOWN)
            .to_edge(DOWN, buff=0.25)
        )
        self.play(Write(content_2[0]), run_time=2)
        self.play(FadeIn(content_2[1]))
        self.wait(1.5)
        self.play(content_2.animate.scale(0.27).move_to(boxes[2].get_center()))
        self.wait(0.25)

        content_3 = (
            VGroup(
                MarkupText("<b>New feature:</b> <tt>MarkupText</tt>").scale(0.7),
                Code("assets/2021_01_03/markup_example.py").scale(0.8),
                MarkupText("renders as").scale(0.5),
                VGroup(
                    MarkupText("<b>foo</b> <i>bar</i> <b><i>foobar</i></b>"),
                    MarkupText(
                        "<s>foo</s> <u>bar</u>" "<big>big</big> <small>small</small>"
                    ),
                    MarkupText('<gradient from="RED" to="YELLOW">colors</gradient>'),
                )
                .arrange(DOWN)
                .scale(0.8),
            )
            .arrange(DOWN)
            .scale(0.7)
            .to_edge(DOWN, buff=0.25)
        )
        self.play(Write(content_3), run_time=4)
        self.wait(1.5)
        self.play(content_3.animate.scale(0.27).move_to(boxes[3].get_center()))
        self.wait(0.25)

        import networkx as nx
        import numpy as np

        g = nx.erdos_renyi_graph(15, 0.3)
        circle_layout_g = dict(
            [(v, np.append(pos, 0)) for v, pos in nx.layout.circular_layout(g).items()]
        )
        G = Graph(g.nodes, g.edges, layout_scale=2.5)
        content_4 = (
            VGroup(MarkupText("<b>New feature:</b> <tt>Graph</tt>").scale(0.7), G)
            .arrange(DOWN)
            .to_edge(DOWN, buff=0.25)
        )
        ct = G.get_center()
        self.play(Write(content_4), run_time=3)
        self.wait(0.5)

        self.play(
            *[G[v].animate.move_to(ct + 1.5 * circle_layout_g[v]) for v in G.vertices]
        )
        self.wait(1.5)
        self.play(content_4.animate.scale(0.4).move_to(boxes[4].get_center()))
        self.wait(0.25)

        content_5 = (
            VGroup(
                MarkupText("... many more bugfixes").scale(0.7),
                MarkupText("and improvements!").scale(0.7),
                ManimBanner().scale(0.4),
                MarkupText("Changelog:").scale(0.7),
                MarkupText(
                    "<tt>https://docs.manim.community/en/v0.2.0/changelog.html</tt>"
                ).scale(0.3),
            )
            .arrange(DOWN)
            .to_edge(DOWN, buff=0.25)
        )
        self.play(Write(content_5), run_time=2)
        self.wait(1.5)
        self.play(content_5.animate.scale(0.4).move_to(boxes[5].get_center()))

        self.wait(0.25)
        group = VGroup(banner, release_tour)
        self.play(group.animate.move_to(ORIGIN))
        self.play(*[FadeOut(mobj) for mobj in self.mobjects])
        self.wait(0.25)
