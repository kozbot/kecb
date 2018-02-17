import entity


class NO(entity.CodedSymbol):
    min_pole = 1
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.Line(entity.Point(0, 0), entity.Point(5, 0)),
            entity.Line(entity.Point(15, 0), entity.Point(20, 0)),
            entity.Line(entity.Point(5, 10), entity.Point(5, -10)),
            entity.Line(entity.Point(15, 10), entity.Point(15, -10)),
        ]


class NC(entity.CodedSymbol):
    min_pole = 1
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            NO(),
            entity.Line(entity.Point(0, 10), entity.Point(20, -10)),
        ]
