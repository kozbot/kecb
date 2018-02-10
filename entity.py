from dataclasses import dataclass, field, InitVar
from decimal import Decimal


class Entity:
    _bounds: object = None

    def calculate_bounds(self):
        raise NotImplementedError()

    def bounds(self):
        if self._bounds is not None:
            return self._bounds
        else:
            self.calculate_bounds()
            return self._bounds


@dataclass
class Point(Entity):
    x: Decimal = Decimal(0.0)
    y: Decimal = Decimal(0.0)

    def calculate_bounds(self):
        self._bounds = Rect(TL=Point(self.x, self.y),
                            TR=Point(self.x, self.y),
                            BR=Point(self.x, self.y),
                            BL=Point(self.x, self.y))


@dataclass
class Line(Entity):
    start: Point = Point()
    end: Point = Point()

    def calculate_bounds(self):
        self._bounds = resolve_rect([self.start, self.end])


@dataclass
class PolyLine(Entity):
    points: list  # List of Point
    closed: bool

    def calculate_bounds(self):
        self._bounds = resolve_rect(points=self.points)


@dataclass
class Rect(Entity):
    TL: Point
    TR: Point
    BR: Point
    BL: Point

    def calculate_bounds(self):
        self._bounds = Rect(TL=self.TL,
                            TR=self.TR,
                            BR=self.BR,
                            BL=self.BL)


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

    return Rect(TL=Point(left, top),
                TR=Point(right, top),
                BR=Point(right, bottom),
                BL=Point(left, bottom))


@dataclass
class Arc(Entity):
    center: Point
    extents: Rect
    start: Decimal
    end: Decimal

    # TODO: This is not correct, work out the math later.
    def calculate_bounds(self):
        self._bounds = Rect(TL=self.TL,
                            TR=self.TR,
                            BR=self.BR,
                            BL=self.BL)

# TODO: Review common drawing libraries to see what normal variations on creation are.
def resolve_arc_CRSE(center: Point, radius, start, end):
    pass


@dataclass
class Circle(Entity):
    center: Point
    radius: Decimal

    def calculate_bounds(self):
        self._bounds = Rect(TL=Point(self.center.x - self.radius, self.center.y + self.radius),
                            TR=Point(self.center.x + self.radius, self.center.y + self.radius),
                            BR=Point(self.center.x + self.radius, self.center.y - self.radius),
                            BL=Point(self.center.x - self.radius, self.center.y - self.radius))

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
