import entity
from symlib.terminal import ITERM

LSW_NO_LINE_END = (49.0734179127745, -8.00013698266566)
LSW_NO_LINE_INTERSECT = (30, -3.52186725285915)
LSW_NC_LINE_END = (55, 5.77350269189626)
LSW_NC_LINE_INTERSECT = (30, 2.1650635094611)


class LSW_NO(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(right=False),
            entity.Line(entity.Point(15, 0), entity.Point(*LSW_NO_LINE_END)),
            ITERM(left=False).translate(xoff=40, yoff=0)
        ]


class LSW_NC(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(right=False),
            entity.Line(entity.Point(15, 0), entity.Point(*LSW_NC_LINE_END)),
            ITERM(left=False).translate(xoff=40, yoff=0)
        ]


class LSW_NO_TS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NO(),
            entity.PolyLine(points=[
                entity.Point(*LSW_NO_LINE_INTERSECT),
                entity.Point(30, -10),
                entity.Point(35, -10),
                entity.Point(35, -15),
                entity.Point(25, -15),
                entity.Point(25, -20),
                entity.Point(30, -20),
                entity.Point(30, -25)
            ], closed=False)
        ]


class LSW_NC_TS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NC(),
            entity.PolyLine(points=[
                entity.Point(*LSW_NC_LINE_INTERSECT),
                entity.Point(30, -10),
                entity.Point(35, -10),
                entity.Point(35, -15),
                entity.Point(25, -15),
                entity.Point(25, -20),
                entity.Point(30, -20),
                entity.Point(30, -25)
            ], closed=False)
        ]


class LSW_NO_FS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NO(),
            entity.PolyLine(points=[
                entity.Point(*LSW_NO_LINE_INTERSECT),
                entity.Point(30, -20),
                entity.Point(40, -20),
                entity.Point(30, -10),
            ], closed=False)
        ]


class LSW_NC_FS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NC(),
            entity.PolyLine(points=[
                entity.Point(*LSW_NC_LINE_INTERSECT),
                entity.Point(30, -20),
                entity.Point(40, -20),
                entity.Point(30, -10),
            ], closed=False)
        ]


class LSW_NO_PS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NO(),
            entity.Line(start=entity.Point(*LSW_NO_LINE_INTERSECT), end=entity.Point(30, -15)),
            entity.Arc.from_crse(center=entity.Point(30, -25), radius=10, start=0, end=180),
            entity.Line(start=entity.Point(20, -25), end=entity.Point(40, -25))
        ]


class LSW_NC_PS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NC(),
            entity.Line(start=entity.Point(*LSW_NC_LINE_INTERSECT), end=entity.Point(30, -15)),
            entity.Arc.from_crse(center=entity.Point(30, -25), radius=10, start=0, end=180),
            entity.Line(start=entity.Point(20, -25), end=entity.Point(40, -25))
        ]


class LSW_NO_LS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NO(),
            entity.Line(start=entity.Point(*LSW_NO_LINE_INTERSECT), end=entity.Point(30, -15)),
            entity.Circle(center=entity.Point(30, -25), radius=10)
        ]


class LSW_NC_LS(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            LSW_NC(),
            entity.Line(start=entity.Point(*LSW_NC_LINE_INTERSECT), end=entity.Point(30, -15)),
            entity.Circle(center=entity.Point(30, -25), radius=10)
        ]
