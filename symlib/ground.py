import entity


def PE():
    return [entity.Line(entity.Point(0, 0), entity.Point(0, -12)),
            entity.Line(entity.Point(-6, -12), entity.Point(6, -12)),
            entity.Line(entity.Point(-4, -14), entity.Point(4, -14)),
            entity.Line(entity.Point(-2, -16), entity.Point(2, -16)), ]


def SG():
    return [entity.Line(entity.Point(0, 0), entity.Point(0, -12)),
            entity.PolyLine(points=[entity.Point(-6, -12), entity.Point(6, -12), entity.Point(0, -18)], closed=True)]
