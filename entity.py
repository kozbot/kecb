from affine import Affine
from typing import List
from anytree import NodeMixin
from utils import pack_transform


class Transform():
    __slots__ = ['origin', 'offset', 'rotation', 'scale']

    def __init__(self, origin = (0,0), offset=(0,0), rotation=0, scale=1):
        super().__init__()
        self.origin = origin
        self.offset = offset
        self.rotation = rotation
        self.scale = scale


class Entity(NodeMixin):
    _bounds = None

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

    def translate(self, xoff, yoff):
        raise NotImplementedError()


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

    def translate(self, xoff, yoff):
        self.x += xoff
        self.y += yoff
        return self


class Line(Entity):
    def __init__(self, start: Point, end: Point):
        super().__init__()
        self.start = start
        self.end = end

    def calculate_bounds(self):
        self._bounds = resolve_rect([self.start, self.end])

    def translate(self, xoff, yoff):
        self.start.translate(xoff, yoff)
        self.end.translate(xoff, yoff)
        return self


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
    start: float
    end: float

    # TODO: This is not correct, work out the math later.
    def calculate_bounds(self):
        self._bounds = Rect.identity()


# TODO: Review common drawing libraries to see what normal variations on creation are.
def resolve_arc_CRSE(center: Point, radius, start, end):
    pass


class Circle(Entity):
    def __init__(self, center: Point, radius: float):
        super().__init__()
        self.transform = Affine.identity()
        self.center: Point = center
        self.radius: float = radius

    def calculate_bounds(self):
        self._bounds = Rect([Point(self.center.x - self.radius, self.center.y + self.radius),
                             Point(self.center.x + self.radius, self.center.y + self.radius),
                             Point(self.center.x + self.radius, self.center.y - self.radius),
                             Point(self.center.x - self.radius, self.center.y - self.radius)])

    def translate(self, xoff, yoff):
        self.center.translate(xoff, yoff)
        return self


class Group(Entity):
    def __init__(self):
        super().__init__()
        self.entities: List[Entity] = []
        self.origin: Point = Point(0, 0)
        self.rotation = 0
        self.scale = 1

    def calculate_bounds(self):
        for e in self.children:
            self._bounds = self._bounds + e.calculate_bounds()

    def _post_detach_children(self, children):
        self._bounds = Rect.identity()
        self.calculate_bounds()

    def translate(self, xoff, yoff):
        self.origin.translate(xoff, yoff)
        return self

    def rotate(self, rotation):
        self.rotation = rotation
        return self

    def affine(self):
        return Transform(origin=(self.origin.x,self.origin.y), scale=self.scale,rotation=self.rotation)

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
