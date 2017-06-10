import ezdxf
import os
from drawable import Drawable
import symbol as s
from affine import Affine
from utils import btu, pack_transform, new_dwg


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


def export_multipole(symbols, label, file, minpole=1, maxpole=4,
                     labelfirst=True, transform=pack_transform()):

    for x in range(minpole, maxpole + 1):
        print(label + " - " + str(x) + ' Pole')
        dwg = new_dwg()
        msp = dwg.modelspace()
        cur = Cursor(msp, transform=transform, poles=x)
        for sym in symbols:
            cur = cur + sym
        fname = file + ('' if labelfirst is False and x == minpole
                        else '_' + str(x) + 'P')
        dwg.saveas('./dxf/' + fname + '.dxf')


if __name__ == '__main__':

    print("Generating Drawings...")

    print("Creating '/dxf' Folder")
    os.makedirs("./dxf", exist_ok=True)

    t = pack_transform()

    # TODO: Seperate these generations into functional groups

    export_multipole(symbols=[s.NO()],
                     label="A: Normally Open Contact",
                     file="NO",
                     labelfirst=False)

    print("A: Normally Open Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#') + s.NO() + s.ITERM(label='#')
    dwg.saveas('./dxf/NO_ITERM.dxf')

    export_multipole(symbols=[s.NC()],
                     label="A: Normally Closed Contact",
                     file="NC",
                     labelfirst=False)

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

    export_multipole(symbols=[s.CB()],
                     label="A: Circuit Breaker",
                     file="CB")

    export_multipole(symbols=[s.OL()],
                     label="A: Thermal Overload",
                     file="OL")

    print("A: Solenoid")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.SOL()
    dwg.saveas('./dxf/SOL.dxf')
