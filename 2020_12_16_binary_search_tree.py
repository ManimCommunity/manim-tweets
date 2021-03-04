from manim import *
import random
import math


class BinarySearchTree(VGroup):
    def __init__(
        self,
        scene,
        levels=3,
        base_offset=0.5,
        node_radius=0.5,
        child_offset_factor=1.2,
        label_scale_factor=1,
        color_nodes=False,
        max_value=16,
        animation_runtime=0.2,
        insertion_initial_offset=1,
    ):
        super().__init__()
        self.scene = scene
        self.empty = True
        self.child_down_offset = DOWN * child_offset_factor
        self.child_left_offset = LEFT * base_offset * 2 * math.log2(levels)
        self.node_radius = node_radius
        self.label_scale_factor = label_scale_factor
        self.color_nodes = color_nodes
        self.max_value = max_value
        self.animation_runtime = animation_runtime
        self.insertion_initial_offset = insertion_initial_offset

        self.root = self.get_node(None)
        self.add(self.root)

    def get_node(self, value):
        node = VDict(
            {
                "node": Circle(radius=self.node_radius, color=WHITE),
                "label": MathTex("\\varnothing" if value is None else str(value)).scale(
                    self.label_scale_factor
                ),
            }
        )
        if self.label_scale_factor != 0:
            node["label"] = MathTex(
                "\\varnothing" if value is None else str(value)
            ).scale(self.label_scale_factor)
        if value is not None:
            node_color = interpolate_color(BLUE, RED, value / self.max_value)
            node.set_stroke(node_color)
            if self.color_nodes:
                node.set_fill(node_color, opacity=1)
            node.color = node_color
        node.value = value
        node.left_child = None
        node.right_child = None
        return node

    def insert(self, value):
        node = self.get_node(value)
        if self.root.value is None:
            node.move_to(self.root.get_center())
            self.scene.play(
                FadeInFrom(node, UP * self.insertion_initial_offset),
                FadeOut(self.root),
                run_time=self.animation_runtime,
            )
            self.remove(self.root)
            self.root = node
            self.add(node)
            self.empty = False
            return

        node.move_to(self.root.get_center() + UP * self.insertion_initial_offset)
        cur_node = self.root
        child_left_offset = self.child_left_offset.copy()
        while cur_node is not None:
            if node.value <= cur_node.value:
                self.scene.play(
                    node.move_to,
                    cur_node.get_center() + 2 * cur_node["node"].radius * LEFT,
                    run_time=self.animation_runtime,
                )
                if cur_node.left_child is not None:
                    cur_node = cur_node.left_child
                else:
                    child_location = (
                        cur_node.get_center()
                        + self.child_down_offset
                        + child_left_offset
                    )
                    parent_child_vector = normalize(
                        child_location - cur_node.get_center()
                    )

                    edge_start = (
                        cur_node.get_center() + parent_child_vector * self.node_radius
                    )
                    edge_end = child_location - parent_child_vector * self.node_radius
                    edge = Line(edge_start, edge_end, stroke_color=node.color)

                    self.scene.play(
                        node.move_to,
                        child_location,
                        FadeIn(edge),
                        run_time=self.animation_runtime,
                    )
                    cur_node.left_child = node
                    self.add(node, edge)
                    break
            else:
                self.scene.play(
                    node.move_to,
                    cur_node.get_center() + 2 * cur_node["node"].radius * RIGHT,
                    run_time=self.animation_runtime,
                )
                if cur_node.right_child is not None:
                    cur_node = cur_node.right_child
                else:
                    child_location = (
                        cur_node.get_center()
                        + self.child_down_offset
                        - child_left_offset
                    )
                    parent_child_vector = normalize(
                        child_location - cur_node.get_center()
                    )

                    edge_start = (
                        cur_node.get_center() + parent_child_vector * self.node_radius
                    )
                    edge_end = child_location - parent_child_vector * self.node_radius
                    edge = Line(edge_start, edge_end, stroke_color=node.color)

                    self.scene.play(
                        node.move_to,
                        child_location,
                        FadeIn(edge),
                        run_time=self.animation_runtime,
                    )
                    cur_node.right_child = node
                    self.add(node, edge)
                    break
            child_left_offset /= 2


class DraftScene(Scene):
    def construct(self):
        tree = BinarySearchTree(self, base_offset=0.75, max_value=16).shift(UP * 2)
        self.add(tree)
        label = (
            Text("Great for storing structured data.").scale(0.8).to_edge(UP, buff=0.1)
        )
        self.add(label)

        nums = [8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15]
        for i in nums:
            tree.insert(i)

        self.wait(0.5)
        self.play(FadeOut(tree))
        self.remove(label)

        # tree = BinarySearchTree(
        #     self,
        #     base_offset=0.9,
        #     node_radius=0.05,
        #     child_offset_factor=0.8,
        #     label_scale_factor=0,
        #     color_nodes=True,
        #     max_value=31,
        #     animation_runtime=0.05,
        #     insertion_initial_offset=0.6
        # ).shift(UP * 2.5 + LEFT * 0.5)
        # self.add(tree)
        # self.add(
        #     Text("Though random data can get ugly.").scale(0.8).to_edge(UP, buff=0.1)
        # )

        # # Though random data can get ugly.
        # nums = [i + 1 for i in range(31)]
        # random.seed(0)
        # random.shuffle(nums)
        # for i in nums:
        #     tree.insert(i)

        # self.wait()
