from typing import List
import entity


class ETERM(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            entity.PolyLine(
                points=[entity.Point(0, 10), entity.Point(20, 10), entity.Point(20, -10), entity.Point(0, -10)],
                closed=True),
            entity.Circle(center=entity.Point(10, 0), radius=10)
        ]


class ITERM(entity.CodedSymbol):
    def __init__(self, *args, left=True, right=True, label=None, **kwargs):
        self.left = left
        self.right = right
        self.label = label
        super().__init__(*args, **kwargs)

    def generate(self):
        base: List[entity.Entity] = [entity.Circle(entity.Point(10, 0), 5)]

        if self.left:
            base.append(entity.Line(entity.Point(0, 0), entity.Point(5, 0)))

        if self.right:
            base.append(entity.Line(entity.Point(15, 0), entity.Point(20, 0)))

        return base

        # if self.label is not None:
        #     self.add_text(label, (10, -10),
        #                   height=10, alignment='MIDDLE_CENTER')
