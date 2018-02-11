from dataclasses import dataclass, field, InitVar
from decimal import Decimal
from affine import Affine
from typing import List
from anytree import NodeMixin


class Entity(NodeMixin):
    _bounds: object = None

    def __init__(self):
        super().__init__()
        self.parent = None
        self.linetype = None

    def calculate_bounds(self):
        raise NotImplementedError()

    def bounds(self):
        if self._bounds is not None:
            return self._bounds
        else:
            self.calculate_bounds()
            return self._bounds


class Point(Entity):

    def __init__(self, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y

    def calculate_bounds(self):
        self._bounds = Rect([Point(self.x, self.y),
                             Point(self.x, self.y),
                             Point(self.x, self.y),
                             Point(self.x, self.y)])

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError


class Line(Entity):
    def __init__(self, start: Point, end: Point):
        super().__init__()
        self.start = start
        self.end = end

    def calculate_bounds(self):
        self._bounds = resolve_rect([self.start, self.end])


class PolyLine(Entity):
    def __init__(self, points: List[Point], closed: bool):
        super().__init__()
        self.points = points
        self.closed = closed

    def calculate_bounds(self):
        self._bounds = resolve_rect(points=self.points)


class Rect(Entity):
    def __init__(self, points: List[Point]):
        super().__init__()
        if len(points) is not 4:
            raise ValueError("Rect should have 4 points.")
        self.points = points

    def calculate_bounds(self):
        self._bounds = Rect(self.points)

    @staticmethod
    def __add__(self, other):
        if isinstance(other, Rect):
            return resolve_rect(self.points + other.points)

    @staticmethod
    def identity():
        return Rect([Point(0, 0),
                     Point(0, 0),
                     Point(0, 0),
                     Point(0, 0)])


def resolve_rect(points: list):
    if len(points) < 2:
        raise NotImplementedError(
            "Only a list of 2 or more points supported.")

    xlist = []
    ylist = []
    for p in points:
        xlist.append(p.x)
        ylist.append(p.y)

    left = min(xlist)
    right = max(xlist)
    top = max(ylist)
    bottom = min(ylist)

    # if left == right:
    #     raise ValueError("X coordinates must not be the same.")

    # if top == bottom:
    #     raise ValueError("Y coordinates must not be the same.")

    return Rect([Point(left, top),
                 Point(right, top),
                 Point(right, bottom),
                 Point(left, bottom)])


class Arc(Entity):
    center: Point
    extents: Rect
    start: Decimal
    end: Decimal

    # TODO: This is not correct, work out the math later.
    def calculate_bounds(self):
        self._bounds = Rect.identity()


# TODO: Review common drawing libraries to see what normal variations on creation are.
def resolve_arc_CRSE(center: Point, radius, start, end):
    pass


class Circle(Entity):
    center: Point
    radius: Decimal

    def calculate_bounds(self):
        self._bounds = Rect([Point(self.center.x - self.radius, self.center.y + self.radius),
                             Point(self.center.x + self.radius, self.center.y + self.radius),
                             Point(self.center.x + self.radius, self.center.y - self.radius),
                             Point(self.center.x - self.radius, self.center.y - self.radius)])


class Group(Entity):
    def __init__(self):
        super().__init__()
        self.transform = Affine.identity()
        self.entities: List[Entity] = []

    def calculate_bounds(self):
        for e in self.entities:
            self._bounds = self._bounds + e.calculate_bounds()

    def _post_detach_children(self, children):
        self._bounds = Rect.identity()
        self.calculate_bounds()

# class Arc(object):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__()
#         if kwargs.keys() & {'center'} and kwargs.keys() & {'xc', 'yc'}:
#             if kwargs.keys() >= {'width', 'height', 'x', 'y'}:
#                 self._center = (kwargs['x'] + (kwargs['width'] / 2.0),
#                                 kwargs['y'] - (kwargs['height'] / 2.0))
#             elif kwargs.keys() >= {'rect'}:
#                 self._center
#
#             print(self._center)
