import entity
from symlib.terminal import ETERM
from symlib.contact import NO, NC


class GEN_DEV(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ETERM(),
            entity.Rect(points=[
                entity.Point(-10, 20),
                entity.Point(110, 20),
                entity.Point(110, -20),
                entity.Point(-10, -20),
            ], linetype='PHANTOM'),
            ETERM().translate(xoff=80, yoff=0)
        ]


class GEN_DEV_NO(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ETERM(),
            entity.Line(start=entity.Point(20, 0), end=entity.Point(40, 0)),
            NO().translate(xoff=40, yoff=0),
            entity.Line(start=entity.Point(60, 0), end=entity.Point(80, 0)),
            entity.Rect(points=[
                entity.Point(-10, 20),
                entity.Point(110, 20),
                entity.Point(110, -20),
                entity.Point(-10, -20),
            ], linetype='PHANTOM'),
            ETERM().translate(xoff=80, yoff=0)
        ]


class GEN_DEV_NC(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ETERM(),
            entity.Line(start=entity.Point(20, 0), end=entity.Point(40, 0)),
            NC().translate(xoff=40, yoff=0),
            entity.Line(start=entity.Point(60, 0), end=entity.Point(80, 0)),
            entity.Rect(points=[
                entity.Point(-10, 20),
                entity.Point(110, 20),
                entity.Point(110, -20),
                entity.Point(-10, -20),
            ], linetype='PHANTOM'),
            ETERM().translate(xoff=80, yoff=0)
        ]