import numpy as np
import ezdxf
import os

UNITS_PER_BLOCK = UPB = 20.0  # Drawing in a 20x20 grid
BLOCK_SIZE = 1.0 / 8.0  # Imperial - 1/8"
UNIT_SCALE = BLOCK_SIZE / UPB
SCALE = np.array([UNIT_SCALE, UNIT_SCALE])  # [ X, Y ]


class Cursor(object):
    """Cursor"""

    def __init__(self, layout,
                 scale=SCALE, offset=np.array([0, 0]), UPB=UNITS_PER_BLOCK):

        super(Cursor, self).__init__()
        self.layout = layout
        self.scale = scale
        self.offset = offset
        self.UPB = UPB

    # Utility primitive methods for readability

    def add_line(self, start, end):

        self.layout.add_line(
            (np.array([start[0], start[1]]) + self.offset) * self.scale,
            (np.array([end[0], end[1]]) + self.offset) * self.scale
        )

    def add_circle(self, center, radius):

        self.layout.add_circle(
            (np.array([center[0], center[1]]) + self.offset) * self.scale,
            (np.array([radius])) * UNIT_SCALE  # Radius
        )

    # Drawing methods

    def draw_no_contact(self):

        self.add_line((0, 0), (5, 0))

        self.add_line((15, 0), (20, 0))

        self.add_line((5, 10), (5, -10))

        self.add_line((15, 10), (15, -10))

    def draw_nc_contact(self):

        self.draw_no_contact

    def draw_inline_terminal(self, left=True, right=True, label=None):

        self.add_circle((10, 0), 5)

        if left:
            self.add_line((0, 0), (5, 0))

        if right:
            self.add_line((15, 0), (20, 0))

        if label is not None:
            # TODO: Add
            # self.add_text(self,label,pos,height=10,align='MIDDLE_CENTER')
            self.layout.add_text(
                label, dxfattribs={'height': 10 * UNIT_SCALE}
            ).set_pos(
                (np.array([10, -10]) + self.offset) * self.scale,
                align='MIDDLE_CENTER'
            )

    # Chainable methods

    def MoveTo(self, pos):
        self.offset = np.array([pos[0] * self.UPB, pos[1] * self.UPB])

        return self

    def Move(self, dist):

        mvoff = np.array([dist[0] * self.UPB, dist[1] * self.UPB])

        self.offset = self.offset + mvoff

        return self

    def Left(self, num_blocks=1):

        self.Move((-1, 0))

        return self

    def Right(self, num_blocks=1):

        self.Move((1, 0))

        return self

    def Up(self, num_blocks=1):

        self.Move((0, 1))

        return self

    def Down(self, num_blocks=1):

        self.Move((0, -1))

        return self

    def NO(self):

        self.draw_no_contact()

        self.Right(1)

        return self

    def NC(self):

        self.draw_no_contact()

        self.add_line((0, -10), (20, 10))

        self.Right(1)

        return self

    def ITERM(self, **kwargs):

        self.draw_inline_terminal(**kwargs)

        self.Right(1)

        return self


def draw_multipole(method, layout, scale=SCALE, offset=np.array([0, 0]),
                   gap=2, poles=1):
    original_offset = offset

    for x in range(0, poles):
        offset = original_offset + np.array([0, x * -gap * UPB])
        method(layout, scale, offset)


def add_scaled_line(layout, scale, offset, start, end):

    layout.add_line(
        (np.array([start[0], start[1]]) + offset) * scale,
        (np.array([end[0], end[1]]) + offset) * scale
    )


def draw_no_contact(layout, scale=SCALE, offset=np.array([0, 0])):

    add_scaled_line(layout, scale, offset, start=(0, 0), end=(5, 0))

    add_scaled_line(layout, scale, offset, start=(15, 0), end=(20, 0))

    add_scaled_line(layout, scale, offset, start=(5, 10), end=(5, -10))

    add_scaled_line(layout, scale, offset, start=(15, 10), end=(15, -10))


def draw_nc_contact(layout, scale=SCALE, offset=np.array([0, 0])):

    draw_no_contact(layout, scale, offset)

    add_scaled_line(layout, scale, offset, start=(0, -10), end=(20, 10))


def draw_terminal(layout, scale=SCALE, offset=np.array([0, 0])):

    layout.add_polyline2d(
        [
            (np.array([0, 10]) + offset) * scale,
            (np.array([20, 10]) + offset) * scale,
            (np.array([20, -10]) + offset) * scale,
            (np.array([0, -10]) + offset) * scale
        ],
        {'flags': ezdxf.const.POLYLINE_CLOSED}
    )

    layout.add_circle(
        (np.array([10, 0]) + offset) * scale,  # Center
        (np.array([10])) * UNIT_SCALE  # Radius
    )


def draw_inline_terminal(layout, scale=SCALE, offset=np.array([0, 0]),
                         left=True, right=True, label=None):

    layout.add_circle(
        (np.array([10, 0]) + offset) * scale,  # Center
        (np.array([5])) * UNIT_SCALE  # Radius
    )
    if left:
        add_scaled_line(layout, scale, offset, start=(0, 0), end=(5, 0))

    if right:
        add_scaled_line(layout, scale, offset, start=(15, 0), end=(20, 0))

    if label is not None:
        layout.add_text(
            label, dxfattribs={'height': 10 * UNIT_SCALE}
        ).set_pos(
            (np.array([10, -10]) + offset) * scale,
            align='MIDDLE_CENTER'
        )


def draw_circuit_breaker(layout, scale=SCALE, offset=np.array([0, 0]), poles=1):

    original_offset = offset

    for x in range(0, poles):
        offset = original_offset + np.array([0, x * -2 * UPB])

        draw_inline_terminal(layout, scale, offset, left=True, right=False)

        layout.add_arc(
            (np.array([30, -5]) + offset) * scale,  # Center
            (np.array([25])) * UNIT_SCALE,  # Radius
            37,  # Start Angle (draws CCW)
            143  # End Angle
        )

        draw_inline_terminal(layout, scale, offset +
                             np.array([2 * UPB, 0]), left=False, right=True)

    if poles > 1:
        layout.add_line(
            (np.array([30, 20]) + original_offset) * scale,
            (np.array([30, 20 - ((poles - 1) * 2 * UPB)]) +
             original_offset) * scale,
        )


def draw_thermal(layout, scale=SCALE, offset=np.array([0, 0])):

    layout.add_arc(
        (np.array([10, 0]) + offset) * scale,  # Center
        (np.array([10])) * UNIT_SCALE,  # Radius
        270,  # Start Angle (draws CCW)
        180  # End Angle
    )

    layout.add_arc(
        (np.array([30, 0]) + offset) * scale,  # Center
        (np.array([10])) * UNIT_SCALE,  # Radius
        90,  # Start Angle (draws CCW)
        0  # End Angle
    )


def draw_thermal_overload(layout, scale=SCALE, offset=np.array([0, 0])):

    draw_inline_terminal(layout, scale, offset)

    draw_thermal(layout, scale, offset + np.array([1 * UPB, 0]))

    draw_inline_terminal(layout, scale, offset +
                         np.array([3 * UPB, 0]), left=True, right=True)


def draw_magnetic(layout, scale=SCALE, offset=np.array([0, 0])):

    layout.add_polyline2d(
        [
            (np.array([0, 0]) + offset) * scale,
            (np.array([10, 10]) + offset) * scale,
            (np.array([10, -10]) + offset) * scale,
            (np.array([20, 0]) + offset) * scale
        ]
    )


def draw_solenoid(layout, scale=SCALE, offset=np.array([0, 0])):

    draw_inline_terminal(layout, scale, offset)

    draw_magnetic(layout, scale, offset + np.array([1 * UPB, 0]))

    draw_inline_terminal(layout, scale, offset +
                         np.array([2 * UPB, 0]), left=True, right=True)


def draw_thermal_magnetic_breaker(layout, scale=SCALE, offset=np.array([0, 0])):

    original_offset = offset

    # Use the 3 pole call to generate connecting line
    draw_circuit_breaker(layout, scale, original_offset, poles=3)

    for x in range(0, 3):  # 3 Poles
        offset = original_offset + np.array([0, x * -2 * UPB])

        draw_magnetic(layout, scale, offset + np.array([3 * UPB, 0]))

        draw_thermal_overload(layout, scale, offset + np.array([4 * UPB, 0]))

        layout.add_text(
            (x * 2) + 1, dxfattribs={'height': 10 * UNIT_SCALE}
        ).set_pos(
            (np.array([10, -10]) + offset) * scale,
            align='MIDDLE_CENTER'
        )

        layout.add_text(
            (x + 1) * 2, dxfattribs={'height': 10 * UNIT_SCALE}
        ).set_pos(
            (np.array([10, -10]) + offset + np.array([7 * UPB, 0])) * scale,
            align='MIDDLE_CENTER'
        )


if __name__ == '__main__':
    print("Generating Drawings...")

    print("Creating '/dxf' Folder")
    os.makedirs("./dxf", exist_ok=True)

    # TODO: Seperate these generations into functional groups

    print("A: Normally Open Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_no_contact(msp)
    dwg.saveas('./dxf/NO.dxf')

    print("A: Normally Open Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur.ITERM(label='#').NO().ITERM(label='#')
    dwg.saveas('./dxf/NO_ITERM.dxf')

    print("A: Normally Closed Contact")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_nc_contact(msp)
    dwg.saveas('./dxf/NC.dxf')

    print("A: Normally Closed Contact w/ Inline Terminals")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    cur = Cursor(msp)
    cur.ITERM(label='#').NC().ITERM(label='#')
    dwg.saveas('./dxf/NC_ITERM.dxf')

    print("A: Terminal")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_terminal(msp)
    dwg.saveas('./dxf/ETERM.dxf')

    print("A: Inline Terminal")
    dwg = ezdxf.new()
    cur = Cursor(msp)
    cur.ITERM(label='#')
    dwg.saveas('./dxf/ITERM.dxf')

    print("A: Circuit Breaker - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_circuit_breaker(msp, poles=1)
    dwg.saveas('./dxf/CB_1P.dxf')

    print("A: Circuit Breaker - 2 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_circuit_breaker(msp, poles=2)
    dwg.saveas('./dxf/CB_2P.dxf')

    print("A: Circuit Breaker - 3 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_circuit_breaker(msp, poles=3)
    dwg.saveas('./dxf/CB_3P.dxf')

    print("A: Thermal Overload - 1 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_thermal_overload(msp)
    dwg.saveas('./dxf/OL_1P.dxf')

    print("A: Thermal Overload - 2 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_multipole(draw_thermal_overload, msp, gap=2, poles=2)
    dwg.saveas('./dxf/OL_2P.dxf')

    print("A: Thermal Overload - 3 Pole")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_multipole(draw_thermal_overload, msp, gap=2, poles=3)
    dwg.saveas('./dxf/OL_3P.dxf')

    print("A: Solenoid")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_solenoid(msp)
    dwg.saveas('./dxf/SOL.dxf')

    print("A: Motor Protector")
    dwg = ezdxf.new()
    msp = dwg.modelspace()
    draw_thermal_magnetic_breaker(msp)
    dwg.saveas('./dxf/MP.dxf')
