import entity


def translate(ent, xoff, yoff):
    if isinstance(ent, entity.Group):
        for c in ent.children:
            translate(c,xoff,yoff)
    elif isinstance(ent, entity.Entity):
        ent.translate(xoff, yoff)
    elif type(ent) is list:
        for i in ent:
            translate(i, xoff, yoff)

    return ent
