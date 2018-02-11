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
                     labelfirst=True, transform=pack_transform(),
                     pole_offset=(btu(0), btu(-2)), rotation=0):
    for x in range(minpole, maxpole + 1):
        print(label + " - " + str(x) + ' Pole')
        dwg = new_dwg()
        msp = dwg.modelspace()
        cur = Cursor(msp, transform=transform,
                     poles=x, pole_offset=pole_offset, rotation=rotation)
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

    export_multipole(symbols=[s.MDS()],
                     label="Main Disconnect Switch",
                     file="MDS",
                     minpole=3,
                     maxpole=4,
                     pole_offset=(0, btu(-2)),
                     rotation=90)

    export_multipole(symbols=[s.CBMDS()],
                     label="Circuit Breaker Main Disconnect Switch",
                     file="CBMDS",
                     minpole=3,
                     maxpole=4,
                     pole_offset=(0, btu(-2)),
                     rotation=90)

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

    print("LSW_NO - Limit Switch Normally Open")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NO()
    dwg.saveas('./dxf/LSW_NO.dxf')

    print("LSW_NC_TS - Limit Switch Normally Closed Thermostat")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NC_TS()
    dwg.saveas('./dxf/LSW_NC_TS.dxf')

    print("LSW_NO_TS - Limit Switch Normally Open Thermostat")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NO_TS()
    dwg.saveas('./dxf/LSW_NO_TS.dxf')

    print("LSW_NC_FS - Limit Switch Normally Closed Flow")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NC_FS()
    dwg.saveas('./dxf/LSW_NC_FS.dxf')

    print("LSW_NO_FS - Limit Switch Normally Open Flow")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NO_FS()
    dwg.saveas('./dxf/LSW_NO_FS.dxf')

    print("LSW_NC_PS - Limit Switch Normally Closed Pressure")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NC_PS()
    dwg.saveas('./dxf/LSW_NC_PS.dxf')

    print("LSW_NO_PS - Limit Switch Normally Open Pressure")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NO_PS()
    dwg.saveas('./dxf/LSW_NO_PS.dxf')

    print("LSW_NC_LS - Limit Switch Normally Closed Level")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NC_LS()
    dwg.saveas('./dxf/LSW_NC_LS.dxf')

    print("LSW_NO_PS - Limit Switch Normally Open Level")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.LSW_NO_LS()
    dwg.saveas('./dxf/LSW_NO_LS.dxf')

    print("*** PUSH BUTTONS ***")

    print("PB_NO - Push Button Normally Open")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.PB_NO()
    dwg.saveas('./dxf/PB_NO.dxf')

    print("PB_NC - Push Button Normally Closed")
    dwg = new_dwg()
    msp = dwg.modelspace()
    cur = Cursor(msp, transform=t)
    cur + s.PB_NC()
    dwg.saveas('./dxf/PB_NC.dxf')
