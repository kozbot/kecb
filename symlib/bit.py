import entity


class MAGNETIC(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.PolyLine(points=[
                entity.Point(0, 0),
                entity.Point(10, 10),
                entity.Point(10, -10),
                entity.Point(20, 0)
            ], closed=False)
        ]


class THERMAL(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.Arc.from_crse(center=entity.Point(10, 0), radius=10, start=270, end=180),
            entity.Arc.from_crse(center=entity.Point(30, 0), radius=10, start=90, end=0)
        ]
