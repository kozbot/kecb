import entity


class PE(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.Line(entity.Point(0, 0), entity.Point(0, -12)),
            entity.Line(entity.Point(-6, -12), entity.Point(6, -12)),
            entity.Line(entity.Point(-4, -14), entity.Point(4, -14)),
            entity.Line(entity.Point(-2, -16), entity.Point(2, -16)),
        ]


class SG(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.Line(entity.Point(0, 0), entity.Point(0, -12)),
            entity.PolyLine(points=[entity.Point(-6, -12), entity.Point(6, -12), entity.Point(0, -18)],
                            closed=True)
        ]


class CG(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.Line(entity.Point(0, 0), entity.Point(0, -12)),
            entity.Line(entity.Point(-6, -12), entity.Point(6, -12)),
            entity.Line(entity.Point(-6, -12), entity.Point(-9, -17)),
            entity.Line(entity.Point(0, -12), entity.Point(-3, -17)),
            entity.Line(entity.Point(6, -12), entity.Point(3, -17)),
        ]
