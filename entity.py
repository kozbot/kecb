from dataclasses import dataclass, field, InitVar
from decimal import Decimal


@dataclass
class Point:
    x: Decimal = Decimal(0.0)
    y: Decimal = Decimal(0.0)


@dataclass
class Line:
    start: Point = Point()
    end: Point = Point()


@dataclass
class PolyLine:
    points: list  # List of Point
    closed: bool


@dataclass
class Rect:
    TL: Point
    TR: Point
    BR: Point
    BL: Point


# TODO: Logic works, so this should be moved to creator
@dataclass
class ResolvedRect(Rect):
    points: InitVar[list]
    TL: any = field(init=False)
    TR: any = field(init=False)
    BR: any = field(init=False)
    BL: any = field(init=False)

    def __post_init__(self, points):
        if len(points) < 2:
            raise NotImplementedError(
                "Only a list of 2 or more points supported.")
        xlist = []
        ylist = []
        for p in points:
            xlist.append(p.x)
            ylist.append(p.y)

        leftmost = min(xlist)
        rightmost = max(xlist)
        topmost = max(ylist)
        botmost = min(ylist)

        if leftmost == rightmost:
            raise ValueError("X coordinates must not be the same.")

        if topmost == botmost:
            raise ValueError("Y coordinates must not be the same.")

        self.TL = Point(leftmost, topmost)
        self.TR = Point(rightmost, topmost)
        self.BR = Point(rightmost, botmost)
        self.BL = Point(leftmost, botmost)


@dataclass
class Circle:
    center: Point
    radius: float

    def extents(self):
        return Rect(TL=Point(self.center.x - self.radius, self.center.y + self.radius),
                    TR=Point(self.center.x + self.radius, self.center.y + self.radius),
                    BR=Point(self.center.x + self.radius, self.center.y - self.radius),
                    BL=Point(self.center.x - self.radius, self.center.y - self.radius))

@dataclass
class Arc:
    center: Point
    extents: Rect
    radius: float
    start: float
    end: float

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
