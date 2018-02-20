import entity
from symlib.bit import MAGNETIC, THERMAL
from symlib.terminal import ITERM
from symlib.limit import LSW_NO, LSW_NO_LINE_END , LSW_NO_LINE_INTERSECT
import config as cfg


class OL(entity.CodedSymbol):
    min_pole = 1
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(),
            THERMAL().translate(xoff=20, yoff=0),
            ITERM().translate(xoff=60, yoff=0)
        ]


class CB(entity.CodedSymbol):
    min_pole = 1
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(left=True, right=False),
            entity.Arc.from_crse(center=entity.Point(30, -5), radius=25, start=37, end=143),
            ITERM(left=False, right=True).translate(xoff=40, yoff=0)
        ]

    def generate_multipole(self, poles=1):
        entities = self.generate_multipole_basic(poles=poles)
        entities.append(entity.Line(start=entity.Point(30, 20),
                                    end=entity.Point(30, 20 + (cfg.POLE_OFFSET * (poles - 1))),
                                    linetype='PHANTOM'))
        return entities


class MDS(entity.CodedSymbol):
    min_pole = 3
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translate(xoff=0, yoff=-60)
        self.rotate(90)

    def generate(self):
        return [
            LSW_NO()
        ]

    def generate_multipole(self, poles=1):
        entities = self.generate_multipole_basic(poles=poles)
        entities.append(entity.PolyLine(points=[
            entity.Point(*LSW_NO_LINE_INTERSECT),
            entity.Point(LSW_NO_LINE_INTERSECT[0], LSW_NO_LINE_INTERSECT[1] + cfg.POLE_OFFSET * (poles - 0.5)),
            entity.Point(LSW_NO_LINE_END[0], LSW_NO_LINE_END[1] + cfg.POLE_OFFSET * (poles - 0.5)),
        ], closed=False, linetype='PHANTOM'))
        return entities


# TODO : Check on if the CB is 180 degrees off because it feels backwards
class CBMDS(entity.CodedSymbol):
    min_pole = 3
    max_pole = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translate(xoff=0, yoff=-60)
        self.rotate(90)

    def generate(self):
        return [
            CB()
        ]

    def generate_multipole(self, poles=1):
        entities = self.generate_multipole_basic(poles=poles)
        entities.append(entity.PolyLine(points=[
            entity.Point(30, 20),
            entity.Point(LSW_NO_LINE_INTERSECT[0], LSW_NO_LINE_INTERSECT[1] + cfg.POLE_OFFSET * (poles - 0.5)),
            entity.Point(LSW_NO_LINE_END[0], LSW_NO_LINE_END[1] + cfg.POLE_OFFSET * (poles - 0.5)),
        ], closed=False, linetype='PHANTOM'))
        return entities
