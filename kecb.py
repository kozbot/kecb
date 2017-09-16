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
                     label="Normally Open Contact",
                     file="NO",
                     labelfirst=False)

    print("Normally Open Contact w/ Inline Terminals")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#') + s.NO() + s.ITERM(label='#')
    dwg.saveas('./dxf/NO_ITERM.dxf')

    export_multipole(symbols=[s.NC()],
                     label="Normally Closed Contact",
                     file="NC",
                     labelfirst=False)

    print("Normally Closed Contact w/ Inline Terminals")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#') + s.NC() + s.ITERM(label='#')
    dwg.saveas('./dxf/NC_ITERM.dxf')

    print("Terminal")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ETERM()
    dwg.saveas('./dxf/ETERM.dxf')

    print("Inline Terminal")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.ITERM(label='#')
    dwg.saveas('./dxf/ITERM.dxf')

    export_multipole(symbols=[s.CB()],
                     label="Circuit Breaker",
                     file="CB")

    export_multipole(symbols=[s.OL()],
                     label="Thermal Overload",
                     file="OL")

    print("Solenoid")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.SOL()
    dwg.saveas('./dxf/SOL.dxf')

    print("Generic Device")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.GEN_DEV()
    dwg.saveas('./dxf/GEN_DEV.dxf')

    print("Generic Device NO")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.GEN_DEV_NO()
    dwg.saveas('./dxf/GEN_DEV_NO.dxf')

    print("Generic Device NC")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.GEN_DEV_NC()
    dwg.saveas('./dxf/GEN_DEV_NC.dxf')

    print("LINETYPES")
    dwg = new_dwg()
    msp = dwg.modelspace()
    ly = 0
    for lt in dwg.linetypes:
        msp.add_line(
            (0, ly),
            (40, ly),
            dxfattribs={
                'linetype': lt.dxf.name,
                'ltscale': 2.0
            }
        )
        ly += 20
    dwg.saveas('./dxf/LINETYPES.dxf')

    print("*** GROUND SYMBOLS ***")

    print("PE - Protective Earth")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.PE()
    dwg.saveas('./dxf/PE.dxf')

    print("SG - Signal Ground")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.SG()
    dwg.saveas('./dxf/SG.dxf')

    print("CG - Chassis Ground")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.CG()
    dwg.saveas('./dxf/CG.dxf')

    print("*** LIMIT SWITCHES ***")

    print("LSW_NC - Limit Switch Normally Closed")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NC()
    dwg.saveas('./dxf/LSW_NC.dxf')
