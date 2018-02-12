from typing import List
import entity


# def ITERM(left=True, right=True, label=None):
#     base: List[entity.Entity] = [entity.Circle(entity.Point(10, 0), 5)]
#
#     if left:
#         base.append(entity.Line(entity.Point(0, 0), entity.Point(5, 0)))
#
#     if right:
#         base.append(entity.Line(entity.Point(15, 0), entity.Point(20, 0)))
#
#     # if label is not None:
#     #     self.add_text(label, (10, -10),
#     #                   height=10, alignment='MIDDLE_CENTER')
#
#     return base


class ITERM(entity.Group):
    def __init__(self, left=True, right=True, label=None):
        super().__init__()
        base: List[entity.Entity] = [entity.Circle(entity.Point(10, 0), 5)]

        if left:
            base.append(entity.Line(entity.Point(0, 0), entity.Point(5, 0)))

        if right:
            base.append(entity.Line(entity.Point(15, 0), entity.Point(20, 0)))

        self.children = base

        # if label is not None:
        #     self.add_text(label, (10, -10),
        #                   height=10, alignment='MIDDLE_CENTER')
