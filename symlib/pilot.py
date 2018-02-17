import entity
from symlib.terminal import ITERM


class PB_NO(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(right=False),
            entity.Line(start=entity.Point(10, -10), end=entity.Point(50, -10)),
            entity.Line(start=entity.Point(30, -10), end=entity.Point(30, 10)),
            ITERM(left=False).translate(xoff=40, yoff=0)
        ]


class PB_NC(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(right=False),
            entity.Line(start=entity.Point(10, -5), end=entity.Point(50, -5)),
            entity.Line(start=entity.Point(30, -5), end=entity.Point(30, 10)),
            ITERM(left=False).translate(xoff=40, yoff=0)
        ]
