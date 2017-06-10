import ezdxf
import os
from drawable import Drawable
import symbol as s
import config as cfg
from affine import Affine
from utils import btu


class Cursor(object):
    """Cursor"""

    def __init__(self, layout,
                 scale=cfg.UNIT_SCALE, offset=(0, 0),
                 rotation=0, origin=(0, 0)):

        super(Cursor, self).__init__()
        self.layout = layout
        self.scale = scale
        self.offset = offset
        self.rotation = rotation
        self.origin = origin

    def __add__(self, other):

        if isinstance(other, Drawable):
            other.plot(self.layout, self.origin, self.offset,
                       self.scale, self.rotation)
            self.Move(other.plot_offset)
            return self

    # Chainable methods

    def MoveTo(self, pos):

        self.offset = pos

        return self

    def Move(self, dist):

        self.offset *= Affine.translation(*dist)

        return self

    def Left(self, num_blocks=1):

        self.Move((btu(-1), 0))

        return self

    def Right(self, num_blocks=1):

        self.Move((btu(1), 0))

        return self

    def Up(self, num_blocks=1):

        self.Move((0, btu(1)))

        return self

    def Down(self, num_blocks=1):

        self.Move((0, btu(-1)))

        return self


if __name__ == '__main__':

    print("Generating Drawings...")

    print("Creating '/dxf' Folder")
    os.makedirs("./dxf", exist_ok=True)

    # TODO: Seperate these generations into functional groups

    print("A: Normally Open Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.NO()
    dwg.saveas('./dxf/NO.dxf')

    print("A: Normally Open Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.ITERM(label='#') + s.NO() + s.ITERM(label='#')
    dwg.saveas('./dxf/NO_ITERM.dxf')

    print("A: Normally Closed Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.NC()
    dwg.saveas('./dxf/NC.dxf')

    print("A: Normally Closed Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.ITERM(label='#') + s.NC() + s.ITERM(label='#')
    dwg.saveas('./dxf/NC_ITERM.dxf')

    print("A: Terminal")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.ETERM()
    dwg.saveas('./dxf/ETERM.dxf')

    print("A: Inline Terminal")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.ITERM(label='#')
    dwg.saveas('./dxf/ITERM.dxf')

    print("A: Circuit Breaker - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.CB()
    dwg.saveas('./dxf/CB_1P.dxf')

    print("A: Thermal Overload - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.OL()
    dwg.saveas('./dxf/OL_1P.dxf')

    print("A: Solenoid")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur + s.SOL()
    dwg.saveas('./dxf/SOL.dxf')
