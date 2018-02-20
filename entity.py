from affine import Affine
from typing import List
from anytree import NodeMixin
from config import POLE_OFFSET


class Transform:
    __slots__ = ['origin', 'offset', 'rotation', 'scale']

    def __init__(self, origin=(0, 0), offset=(0, 0), rotation=0, scale=1):
        super().__init__()
        self.origin = origin
        self.offset = offset
        self.rotation = rotation
        self.scale = scale

    def __add__(self, other):
        if not other:
            return self
        elif type(other) is Transform:
            return Transform(origin=(self.origin[0] + other.origin[0], self.origin[1] + other.origin[1]),
                             offset=(self.offset[0] + other.offset[0], self.offset[1] + other.offset[1]),
                             rotation=self.rotation + other.rotation,
                             scale=self.scale * other.scale)
        else:
            raise TypeError


class Entity(NodeMixin):
    _bounds = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.parent = None
        self.linetype = kwargs.get('linetype', None)

    def calculate_bounds(self):
        raise NotImplementedError()

    def bounds(self):
        if self._bounds is not None:
            return self._bounds
        else:
            self.calculate_bounds()
            return self._bounds

    def translate(self, xoff, yoff):
        raise NotImplementedError

    def duplicate(self):
        raise NotImplementedError


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

    def duplicate(self):
        return Point(x=self.x, y=self.y)


class Line(Entity):
    def __init__(self, start: Point, end: Point, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end

    def calculate_bounds(self):
        self._bounds = resolve_rect([self.start, self.end])

    def translate(self, xoff, yoff):
        self.start.translate(xoff, yoff)
        self.end.translate(xoff, yoff)
        return self

    def duplicate(self):
        return Line(start=self.start.duplicate(), end=self.end.duplicate())


class PolyLine(Entity):
    def __init__(self, points: List[Point], closed: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = points
        self.closed = closed

    def calculate_bounds(self):
        self._bounds = resolve_rect(points=self.points)

    def translate(self, xoff, yoff):
        for point in self.points:
            point.translate(xoff=xoff, yoff=yoff)

        return self

    def duplicate(self):
        points = []
        for p in self.points:
            points.append(p.duplicate())
        return PolyLine(points=points, closed=self.closed)


class Rect(Entity):
    def __init__(self, *args, points: List[Point], **kwargs):
        super().__init__(*args, **kwargs)
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
        return Rect(points=[Point(0, 0),
                            Point(0, 0),
                            Point(0, 0),
                            Point(0, 0)])

    def translate(self, xoff, yoff):
        for p in self.points:
            p.translate(xoff=xoff, yoff=yoff)

    def duplicate(self):
        points = []
        for p in self.points:
            points.append(p.duplicate())
        return Rect(points=points)


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

    return Rect(points=[Point(left, top),
                        Point(right, top),
                        Point(right, bottom),
                        Point(left, bottom)])


class Arc(Entity):
    center: Point
    radius: float
    start: float
    end: float
    fit: Rect

    def __init__(self):
        super().__init__()

    # TODO: This is not correct, work out the math later.
    def calculate_bounds(self):
        self._bounds = Rect.identity()

    def translate(self, xoff, yoff):
        self.center.translate(xoff=xoff, yoff=yoff)
        self.fit.translate(xoff=xoff, yoff=yoff)
        return self

    def duplicate(self):
        a = Arc()
        a.center = self.center.duplicate()
        a.radius = self.radius
        a.start = self.start
        a.end = self.end
        a.fit = self.fit
        return a

    @staticmethod
    def from_crse(center: Point, radius, start, end):
        a = Arc()
        a.center = center
        a.radius = radius
        if start == end:
            raise ValueError("Start and End angles cannot be the same.")
        if start > 360 or start < 0:
            a.start = start % 360
        else:
            a.start = start

        if end > 360 or end < 0:
            a.end = end % 360
        else:
            a.end = end
        a.fit = resolve_rect(points=[Point(a.center.x - a.radius, a.center.y + a.radius),
                                     Point(a.center.x + a.radius, a.center.y - a.radius)])
        return a


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

    def duplicate(self):
        return Circle(center=self.center.duplicate(), radius=self.radius)


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

    def translate(self, xoff=0, yoff=0):
        self.origin.translate(xoff, yoff)
        return self

    def rotate(self, rotation):
        self.rotation = rotation
        return self

    def affine(self):
        return Transform(origin=(self.origin.x, self.origin.y), scale=self.scale, rotation=self.rotation)

    def duplicate(self):
        new = []
        for child in self.children:
            new.append(child.duplicate())
        newgroup = Group()
        newgroup.children = new
        return newgroup


class CodedSymbol(Group):
    min_pole = 1
    max_pole = 1

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.poles = kwargs.get("poles", 1)
        self.children = self.generate()

        if self.poles > 1:
            self.children = self.generate_multipole(poles=self.poles)

    def generate(self):
        raise NotImplementedError

    def generate_multipole(self, poles=1):
        return self.generate_multipole_basic(poles=poles)

    def generate_multipole_basic(self, poles):
        px, py = 0, POLE_OFFSET
        entities = []
        for child in self.children:
            if isinstance(child, CodedSymbol):
                entities.extend(child.generate_multipole(poles=poles))
            else:
                for i in range(0, poles):
                    entities.append(
                        child.duplicate().translate(xoff=(i * px) + self.origin.x,
                                                    yoff=(i * py) + self.origin.y))
        return entities

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
