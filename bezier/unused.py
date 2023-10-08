from manim import *


class BezierImage(Scene):
    def construct(self):
        points = [
            np.array([x, y, 0])
            for x, y in [
                (-5, 2), (-2, 2), (-5, -3), (2, 3),
                (4, 3.2), (6, 0), (6, -3), (0, -1),
            ]
        ]
        lines, dots = self.get_lines_and_dots_from_points(points)
        self.add(lines)
        self.add(dots)

    def get_lines_and_dots_from_points(self, points: list[np.array]) -> tuple[VGroup, VGroup]:
        lines = VGroup(*[
            Line(points[i], points[i+1])
            for i in range(len(points) - 1)
        ])
        dots = VGroup(*[Dot(p) for p in points])

        return lines, dots
