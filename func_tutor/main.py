from manim import *


class FuncExample(Scene):
    def construct(self):
        ax = Axes(x_range=(-3, 3), y_range=(-3, 3))
        curve = ax.plot(lambda x: (x+2)*x*(x-2)/2, color=RED)
        area = ax.get_area(curve, x_range=(-2, 0))

        self.play(Create(ax, run_time=2), Create(curve, run_time=5))  # same time
        # self.play(Create(curve) first create ax, then curve
        self.play(FadeIn(area), run_time=0.5)
        self.wait(2)


class SquareToCircle(Scene):
    def construct(self):
        green_square = Square(color=GREEN, fill_opacity=0.5)
        self.play(DrawBorderThenFill(green_square))

        blue_circle = Circle(color=BLUE, fill_opacity=0.5)

        # self.play(Transform(green_square, blue_circle)) green_square becomes blue_circle
        # (object stored in circle is in square now), and blue_circle is smth else
        self.play(ReplacementTransform(green_square, blue_circle))  # blue_circle is still the same obj
        self.wait(2)
        self.play(Indicate(blue_circle), run_time=1)
        self.play(FadeOut(blue_circle))  # works correctly with ReplacementTransform


class Positioning(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)

        # next_to
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN)
        green_dot.next_to(red_dot, RIGHT)  # RIGHT = [1, 0, 0]

        self.add(red_dot, green_dot)

        # shift
        s = Square(color=ORANGE)
        s.shift(2*UP, 4*RIGHT)
        self.add(s)

        # move to
        c = Circle(color=PURPLE)
        c.move_to([-3, -2, 0])
        self.add(c)

        # align to
        c2 = Circle(radius=0.5, color=RED, fill_opacity=0.5)
        c3 = c2.copy()
        c3.set_color(YELLOW)
        c4 = c2.copy().set_color(ORANGE)

        c2.align_to(s, UP)
        c3.align_to(s, RIGHT)
        c4.align_to(s, UP + RIGHT)
        self.add(c2, c3, c4)


class CriticalPoints(Scene):
    def construct(self):
        c = Circle(color=GREEN, fill_opacity=0.5)
        self.add(c)

        for d in [(0, 0, 0), UP, UR, RIGHT, DR, DOWN, DL, LEFT, UL]:
            self.add(Cross(scale_factor=0.2).move_to(c.get_critical_point(d)))

        s = Square(color=RED, fill_opacity=0.5)
        s.move_to([1, 0, 0], aligned_edge=LEFT)
        self.add(s)


from manim.utils.unit import Percent, Pixels


class UsefulUnits(Scene):
    def construct(self):
        for perc in range(5, 51, 5):
            self.add(Circle(radius=perc*Percent(X_AXIS)))
            self.add(Square(side_length=2*perc*Percent(Y_AXIS), color=YELLOW))

        d = Dot()
        d.shift(100*Pixels*RIGHT)
        self.add(d)


class Grouping(Scene):
    def construct(self):
        red_dot = Dot(color=RED)
        green_dot = Dot(color=GREEN).next_to(red_dot, RIGHT)
        blue_dot = Dot(color=BLUE).next_to(red_dot, UP)

        dot_group = VGroup(red_dot, green_dot, blue_dot)
        dot_group.to_edge(RIGHT)
        self.add(dot_group)

        circles = VGroup(*[Circle(radius=0.2) for _ in range(20)])
        circles.arrange(UP, buff=0.5)
        self.add(circles)

        stars = VGroup(*[Star(color=YELLOW, fill_opacity=1).scale(0.5) for _ in range(20)])
        stars.arrange_in_grid(4, 5, buff=0.2)
        self.add(stars)


config.background_color = BLACK
# config.frame_width = 9
# config.frame_height = 16
#
# config.pixel_height = 1920
# config.pixel_width = 1080


class SimpleScene(Scene):
    def construct(self):
        plane = NumberPlane(x_range=(-4.5, 4.5), y_range=(-8, 8))
        t = Triangle(color=PURPLE, fill_opacity=0.5)
        self.add(plane, t)


class ChangeDefaults(Scene):
    def construct(self):
        Text.set_default(color=GREEN)
        t = Text("Hello world!")
        self.add(t)
