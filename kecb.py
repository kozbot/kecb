import ezdxf
import os
from drawable import Drawable
import symbol as s
from affine import Affine
from utils import btu, pack_transform


class Cursor(object):
    """Cursor"""

    def __init__(self, layout, transform,
                 poles=1, pole_offset=(btu(0), btu(-2)), **kwargs):

        super(Cursor, self).__init__()
        self.layout = layout
        self.poles = poles
        self.pole_offset = pole_offset
        self.origin = kwargs.get('origin', transform.origin)
        self.offset = kwargs.get('offset', transform.offset)
        self.scale = kwargs.get('scale', transform.scale)
        self.rotation = kwargs.get('rotation', transform.rotation)

    def __add__(self, other):

        if isinstance(other, Drawable):
            other.plot(self.layout, self.origin, self.offset,
                       self.scale, self.rotation, self.poles, self.pole_offset)

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

    t = pack_transform()

    # TODO: Seperate these generations into functional groups

    print("A: Normally Open Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.NO()
    dwg.saveas('./dxf/NO.dxf')

    print("A: Normally Open Contact - 3 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t, poles=3)
    cur + s.NO()
    dwg.saveas('./dxf/NO_3P.dxf')

    print("A: Normally Open Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#') + s.NO() + s.ITERM(label='#')
    dwg.saveas('./dxf/NO_ITERM.dxf')

    print("A: Normally Closed Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.NC()
    dwg.saveas('./dxf/NC.dxf')

    print("A: Normally Closed Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#') + s.NC() + s.ITERM(label='#')
    dwg.saveas('./dxf/NC_ITERM.dxf')

    print("A: Terminal")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ETERM()
    dwg.saveas('./dxf/ETERM.dxf')

    print("A: Inline Terminal")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#')
    dwg.saveas('./dxf/ITERM.dxf')

    print("A: Circuit Breaker - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.CB()
    dwg.saveas('./dxf/CB_1P.dxf')

    print("A: Thermal Overload - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.OL()
    dwg.saveas('./dxf/OL_1P.dxf')

    print("A: Solenoid")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.SOL()
    dwg.saveas('./dxf/SOL.dxf')
