from manim import *
import random
from enum import Enum


class SwapMode(Enum):
    OVER = 1
    ACROSS = 2


class Array(VGroup):
    def __init__(self, array, run_time=0.3):
        super().__init__()
        self.run_time = run_time
        self.build_array(array)

    def build_array(self, array):
        for i, x in enumerate(array):
            cell = VDict({"cell": Square(), "number": Integer(x)})
            if i != 0:
                cell.next_to(self, RIGHT, buff=0)
            self.add(cell)
        self.move_to(ORIGIN)

    def value_at_index(self, index):
        return self[index]["number"].get_value()

    def swap(self, scn, i, j, swap_mode=SwapMode.ACROSS):
        # Swap in submobjects list
        temp = self.submobjects[i]
        self.submobjects[i] = self.submobjects[j]
        self.submobjects[j] = temp

        # Swap on screen
        if swap_mode == SwapMode.ACROSS:
            scn.play(
                self.submobjects[j].animate.shift(
                    LEFT * self.submobjects[i].get_width()
                ),
                self.submobjects[i].animate.shift(
                    RIGHT * self.submobjects[j].get_width()
                ),
                run_time=self.run_time,
            )
        elif swap_mode == SwapMode.OVER:
            scn.play(
                self.submobjects[j].animate.shift(
                    self.submobjects[j].get_height() * UP
                ),
                run_time=self.run_time / 3,
            )
            scn.play(
                self.submobjects[j].animate.shift(
                    self.submobjects[j].get_width() * LEFT
                ),
                self.submobjects[i].animate.shift(
                    self.submobjects[j].get_width() * RIGHT
                ),
                run_time=self.run_time / 3,
            )
            scn.play(
                self.submobjects[j].animate.shift(
                    self.submobjects[j].get_height() * DOWN
                ),
                run_time=self.run_time / 3,
            )
        else:
            raise ValueError(f"Unknown SwapMode {swap_mode}")


class HeightArray(Array):
    def __init__(self, array, unit_width=1.5, unit_height=1, run_time=0.3):
        self.unit_height = unit_height
        self.unit_width = unit_width
        super().__init__(array, run_time=run_time)

    def value_at_index(self, index):
        return self[index].get_height() / self.unit_height

    def build_array(self, array):
        for i, x in enumerate(array):
            cell = Rectangle(width=self.unit_width, height=x * self.unit_height)
            if i != 0:
                cell.next_to(self, RIGHT, buff=0)
                cell.align_to(self, DOWN)
            self.add(cell)
        self.move_to(ORIGIN)


class DraftScene(Scene):
    def construct(self):
        self.sort_array()

    def sort_array(self):
        arr = list(range(1, 51))
        random.shuffle(arr)
        arr_mob = HeightArray(arr, run_time=0.03)
        if type(arr_mob) == Array:
            arr_mob.set_width(13)
        elif isinstance(arr_mob, HeightArray):
            arr_mob.set_height(7)
            arr_mob.to_edge(DOWN)
        self.play(ShowCreation(arr_mob))
        self.wait()

        i = 1
        arr_mob[0].set_color(GREEN)
        while i < len(arr_mob.submobjects):
            arr_mob[i].set_color(YELLOW)
            j = i
            while j > 0 and arr_mob.value_at_index(j - 1) > arr_mob.value_at_index(j):
                arr_mob.swap(self, j, j - 1)
                j = j - 1
            arr_mob[j].set_color(GREEN)
            i = i + 1
        self.wait()
