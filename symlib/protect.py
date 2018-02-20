import entity
from symlib.bit import MAGNETIC, THERMAL
from symlib.terminal import ITERM
import config as cfg


class OL(entity.CodedSymbol):
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