import entity


class NO(entity.Group):
    def __init__(self):
        super().__init__()
        self.children = [
            entity.Line(entity.Point(0, 0), entity.Point(5, 0)),
            entity.Line(entity.Point(15, 0), entity.Point(20, 0)),
            entity.Line(entity.Point(5, 10), entity.Point(5, -10)),
            entity.Line(entity.Point(15, 10), entity.Point(15, -10)),
        ]


class NC(entity.Group):
    def __init__(self):
        super().__init__()
        self.children = [
            NO(),
            entity.Line(entity.Point(0, 10), entity.Point(20, -10)),
        ]