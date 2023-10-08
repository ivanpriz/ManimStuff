import math
from manim import *


def lerp(line: Line, t: float) -> np.array:
    pos = line.point_from_proportion(t)
    return pos


def lerp_from_points(start_point_pos: np.array, end_point_pos: np.array, t: float) -> np.array:
    vec = end_point_pos - start_point_pos
    return start_point_pos + vec * t


class QuadraticBezierFromStartToFinish(Animation):
    def __init__(
            self,
            mobject,  # point to draw line
            point_a: Dot,
            point_b: Dot,
            point_c: Dot,
            point_i: Dot,
            point_j: Dot,
            line_a_c: Line,
            line_c_b: Line,
            # line_i_j: Line,
            **kwargs
    ):
        super().__init__(mobject, **kwargs)
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.point_i = point_i
        self.point_j = point_j
        # self.line_a_c = Line(self.point_a.get_center(), self.point_c.get_center())
        self.line_a_c = line_a_c
        # self.line_b_c = Line(self.point_c.get_center(), self.point_a.get_center())
        self.line_c_b = line_c_b
        self.line_i_j = None

    def _setup_scene(self, scene: Scene) -> None:
        self.line_i_j = Line(self.point_i.get_center(), self.point_j.get_center())
        scene.add(self.line_i_j)
        scene.add(self.point_i)
        scene.add(self.point_j)
        trace = TracedPath(self.mobject.get_center)
        scene.add(trace)

    def begin(self) -> None:
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)

        point_i_pos = lerp_from_points(self.point_a.get_center(), self.point_c.get_center(), alpha)
        point_j_pos = lerp_from_points(self.point_c.get_center(), self.point_b.get_center(), alpha)
        # self.line_i_j.target = Line(point_i_pos, point_j_pos)
        self.line_i_j.become(Line(point_i_pos, point_j_pos))
        point_f_pos = lerp(self.line_i_j, alpha)
        self.point_i.move_to(point_i_pos)
        self.point_j.move_to(point_j_pos)
        # MoveToTarget(self.line_i_j)
        self.mobject.move_to(point_f_pos)


class QuadraticBezierFromMiddleToStart(QuadraticBezierFromStartToFinish):
    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)

        a_c_middle = (self.point_a.get_center() + self.point_c.get_center())/2
        c_b_middle = (self.point_c.get_center() + self.point_b.get_center())/2
        point_i_pos = lerp_from_points(a_c_middle, self.point_a.get_center(), alpha)
        point_j_pos = lerp_from_points(c_b_middle, self.point_c.get_center(), alpha)
        # self.line_i_j.target = Line(point_i_pos, point_j_pos)
        self.line_i_j.become(Line(point_i_pos, point_j_pos))
        point_f_pos = lerp_from_points((point_j_pos + point_i_pos)/2, point_i_pos, alpha)
        self.point_i.move_to(point_i_pos)
        self.point_j.move_to(point_j_pos)
        # MoveToTarget(self.line_i_j)
        self.mobject.move_to(point_f_pos)


class QuadraticBezierFromFinishToMiddle(QuadraticBezierFromStartToFinish):
    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)

        a_c_middle = (self.point_a.get_center() + self.point_c.get_center())/2
        c_b_middle = (self.point_c.get_center() + self.point_b.get_center())/2
        point_i_pos = lerp_from_points(a_c_middle, self.point_a.get_center(), alpha)
        point_j_pos = lerp_from_points(c_b_middle, self.point_c.get_center(), alpha)
        # self.line_i_j.target = Line(point_i_pos, point_j_pos)
        self.line_i_j.become(Line(point_i_pos, point_j_pos))
        point_f_pos = lerp_from_points((point_j_pos + point_i_pos)/2, point_i_pos, alpha)
        self.point_i.move_to(point_i_pos)
        self.point_j.move_to(point_j_pos)
        # MoveToTarget(self.line_i_j)
        self.mobject.move_to(point_f_pos)


class MoveBetweenDots(Animation):
    def __init__(self, mobject, dot_start: Dot, dot_finish: Dot, num_of_runs: float, **kwargs):
        super().__init__(mobject, **kwargs)
        self.dot_start = dot_start
        self.dot_finish = dot_finish
        self.num_of_runs = num_of_runs
        self.one_run_time = kwargs["run_time"]/self.num_of_runs
        self.one_run_alpha_share = 1/self.num_of_runs
        self.direction_vector = self.dot_finish.get_center() - self.dot_start.get_center()

    def begin(self) -> None:
        self.mobject.move_to(self.dot_start.get_center())
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)
        # starts from 0
        run_no = np.floor(alpha/self.one_run_alpha_share)
        t = (alpha - self.one_run_alpha_share*run_no)/self.one_run_alpha_share
        # if run is even we move to dot_finish, and vice versa
        # print(f"alpha: {alpha}, run_no: {run_no}, completion: {run_completion}, select: {int(math.floor(run_no)) % 2}")
        if int(math.floor(run_no)) % 2 == 0:
            # self.mobject.move_to(self.dot_start.get_center() + self.direction_vector * t)
            self.mobject.move_to(lerp_from_points(self.dot_start.get_center(), self.dot_finish.get_center(), t))
        else:
            # self.mobject.move_to(self.dot_finish.get_center() - self.direction_vector * t)
            self.mobject.move_to(lerp_from_points(self.dot_finish.get_center(), self.dot_start.get_center(), t))


class CustomLabeledDot(VGroup):
    def __init__(self, dot, label, *args, **kwargs):
        super().__init__(dot, label, *args, **kwargs)
        self.dot = dot
        self.label = label

    def get_center(self) -> np.ndarray:
        return self.dot.get_center()


class MoveDot(Scene):
    def construct(self):
        dot_c = LabeledDot(label="C")
        label = Text("c")
        always(label.next_to, dot_c, UP)
        self.add(label)
        dot_a = LabeledDot(label="A")
        dot_a.move_to(np.array([-4, -2, 0]))
        dot_c.move_to(dot_a.get_center())
        dot_b = LabeledDot(label="B")
        dot_b.move_to(np.array([4, -2, 0]))

        # self.add(Text("Абакаба"))
        self.play(AnimationGroup(FadeIn(dot_a), FadeIn(dot_b)))
        self.wait()

        self.play(FadeIn(dot_c))
        self.play(Indicate(dot_c))

        self.play(dot_c.animate(run_time=0).move_to(dot_b.get_center()))
        self.play(Indicate(dot_c))
        self.wait()
        self.play(dot_c.animate(run_time=0).move_to(dot_a.get_center()))
        self.play(Indicate(dot_c))
        self.wait()

        a_b_line = Line(dot_a.get_center(), dot_b.get_center())
        self.play(FadeIn(a_b_line))

        between_rt = 4
        num_of_runs = 2
        self.play(
            MoveBetweenDots(
                dot_c,
                dot_a,
                dot_b,
                run_time=between_rt,
                num_of_runs=num_of_runs,
                rate_func=linear,
            )
        )
        self.play(
            dot_c
            .animate(run_time=between_rt/num_of_runs/2, rate_func=linear)
            .move_to((dot_b.get_center() + dot_a.get_center())/2)
        )

        # self.play(FadeOut(a_b_line))
        #
        # self.play(dot_c.animate(run_time=2).shift(UP*3))
        #
        # c_dot_pos = dot_c.get_center()
        # a_c_line = Line(dot_a.get_center(), c_dot_pos)
        # b_c_line = Line(dot_b.get_center(), c_dot_pos)
        # a_c_line_center = (dot_a.get_center() + dot_c.get_center())/2
        # b_c_line_center = (dot_b.get_center() + dot_c.get_center())/2
        # self.play(AnimationGroup(FadeIn(a_c_line), FadeIn(b_c_line)))
        #
        # dot_i = LabeledDot(label="I")
        # dot_j = LabeledDot(label="J")
        # dot_i.move_to(a_c_line_center)
        # dot_j.move_to(b_c_line_center)
        # self.play(AnimationGroup(FadeIn(dot_i), FadeIn(dot_j)))
        #
        # run_time = 4
        # num_of_runs = 2
        # self.play(
        #     AnimationGroup(
        #         dot_i.animate.move_to(dot_a.get_center()),
        #         dot_j.animate.move_to(dot_c.get_center()),
        #         run_time=run_time/num_of_runs/2,
        #         rate_func=linear,
        #     )
        # )
        # self.play(
        #     AnimationGroup(
        #         MoveBetweenDots(
        #             dot_i,
        #             dot_a,
        #             dot_c,
        #             num_of_runs=num_of_runs,
        #             run_time=run_time,
        #             rate_func=linear,
        #         ),
        #         MoveBetweenDots(
        #             dot_j,
        #             dot_c,
        #             dot_b,
        #             num_of_runs=num_of_runs,
        #             run_time=run_time,
        #             rate_func=linear,
        #         )
        #     )
        # )
        # self.play(
        #     AnimationGroup(
        #         dot_i.animate.move_to(a_c_line_center),
        #         dot_j.animate.move_to(b_c_line_center),
        #         run_time=run_time / num_of_runs / 2,
        #         rate_func=linear,
        #     )
        # )
        #
        # # i_j_line = Line(dot_i.get_center(), dot_j.get_center())
        # # self.play(FadeIn(i_j_line))
        # point_f = LabeledDot(label="F")
        # point_f.move_to((dot_i.get_center() + dot_j.get_center())/2)
        # self.play(FadeIn(point_f))
        #
        # self.play(QuadraticBezierFromMiddleToStart(
        #     point_f,
        #     point_a=dot_a,
        #     point_b=dot_b,
        #     point_c=dot_c,
        #     point_i=dot_i,
        #     point_j=dot_j,
        #     line_a_c=a_c_line,
        #     line_c_b=b_c_line,
        #     # line_i_j=i_j_line,
        #     run_time=2
        # ))
        #
        # self.play(QuadraticBezierFromStartToFinish(
        #     point_f,
        #     point_a=dot_a,
        #     point_b=dot_b,
        #     point_c=dot_c,
        #     point_i=dot_i,
        #     point_j=dot_j,
        #     line_a_c=a_c_line,
        #     line_c_b=b_c_line,
        #     # line_i_j=i_j_line,
        #     run_time=4
        # ))

        self.wait(2)
