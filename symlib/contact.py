import entity as ent


def NO():
    return [
        ent.Line(ent.Point(0, 0), ent.Point(5, 0)),
        ent.Line(ent.Point(15, 0), ent.Point(20, 0)),
        ent.Line(ent.Point(5, 10), ent.Point(5, -10)),
        ent.Line(ent.Point(15, 10), ent.Point(15, -10)),
    ]


def NC():
    base = NO()
    base.append(ent.Line(ent.Point(0, 10), ent.Point(20, -10)))
    return base
