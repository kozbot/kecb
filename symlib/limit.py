import entity
from symlib.terminal import ITERM
import symlib.util as util
from affine import Affine


LSW_NC_LINE_END = 5.77350269189626


def LSW_NC():
    base = [ITERM(right=False)]
    base.append(entity.Line(entity.Point(15, 0), entity.Point(55, LSW_NC_LINE_END)))
    base.append(ITERM(left=False).translate(xoff=40,yoff=0))
    return base