from drawable import Drawable
import ezdxf
from utils import btu


class Symbol(Drawable):

    def __init__(self):
        super().__init__()

    def draw_no_contact(self):

        self.add_line((0, 0), (5, 0))

        self.add_line((15, 0), (20, 0))

        self.add_line((5, 10), (5, -10))

        self.add_line((15, 10), (15, -10))

    def draw_nc_contact(self):
        self.draw_no_contact()
        self.add_line((0, -10), (20, 10))

    def draw_magnetic(self):
        self.add_polyline2d(
            [
                (0, 0),
                (10, 10),
                (10, -10),
                (20, 0)
            ]
        )

    def draw_inline_terminal(self, left=True, right=True, label=None):
        self.add_circle((10, 0), 5)

        if left:
            self.add_line((0, 0), (5, 0))

        if right:
            self.add_line((15, 0), (20, 0))

        if label is not None:
            self.add_text(label, (10, -10),
                          height=10, alignment='MIDDLE_CENTER')

    def draw_terminal(self):
        self.add_polyline2d(
            [
                (0, 10),
                (20, 10),
                (20, -10),
                (0, -10)
            ],
            attr={'flags': ezdxf.const.POLYLINE_CLOSED}
        )

        self.add_circle((10, 0), 10)

    def draw_thermal(self):

        self.add_arc((10, 0), 10, 270, 180)

        self.add_arc((30, 0), 10, 90, 0)


#    Ground Symbols

class PE(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.add_line((0, 0), (0, -12))
        self.add_line((-6, -12), (6, -12))
        self.add_line((-4, -14), (4, -14))
        self.add_line((-2, -16), (2, -16))


class SG(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.add_line((0, 0), (0, -12))
        self.add_polyline2d(
            [
                (-6, -12),
                (6, -12),
                (0, -18)
            ],
            attr={'flags': ezdxf.const.POLYLINE_CLOSED}
        )


class LSW_NC(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        self.add_line(
            (15, 0),
            (55, 5.77350269189626),
        )
        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class LSW_NO(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        self.add_line(
            (15, 0),
            (49.0734179127745, -8.00013698266566),
        )
        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class LSW_NC_TS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NC().sym_plot(self)
        self.add_polyline2d(
            [
                (30, 2.1650635094611),
                (30, -10),
                (35, -10),
                (35, -15),
                (25, -15),
                (25, -20),
                (30, -20),
                (30, -25)
            ]
        )


class LSW_NO_TS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NO().sym_plot(self)
        self.add_polyline2d(
            [
                (30, -3.52186725285915),
                (30, -10),
                (35, -10),
                (35, -15),
                (25, -15),
                (25, -20),
                (30, -20),
                (30, -25)
            ]
        )


class LSW_NC_FS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NC().sym_plot(self)
        self.add_polyline2d(
            [
                (30, 2.1650635094611),
                (30, -20),
                (40, -20),
                (30, -10)
            ]
        )


class LSW_NO_FS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NO().sym_plot(self)
        self.add_polyline2d(
            [
                (30, -3.52186725285915),
                (30, -20),
                (40, -20),
                (30, -10)
            ]
        )


class LSW_NC_PS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NC().sym_plot(self)
        self.add_line(
            (30, 2.1650635094611),
            (30, -15)
        )
        self.add_arc(
            (30, -25),
            10,
            0,
            180
        )
        self.add_line(
            (20, -25),
            (40, -25)
        )


class LSW_NO_PS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NO().sym_plot(self)
        self.add_line(
            (30, -3.52186725285915),
            (30, -15)
        )
        self.add_arc(
            (30, -25),
            10,
            0,
            180
        )
        self.add_line(
            (20, -25),
            (40, -25)
        )


class LSW_NC_LS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NC().sym_plot(self)
        self.add_line(
            (30, 2.1650635094611),
            (30, -15)
        )
        self.add_circle(
            (30, -25),
            10,
        )


class LSW_NO_LS(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        LSW_NO().sym_plot(self)
        self.add_line(
            (30, -3.52186725285915),
            (30, -15)
        )
        self.add_circle(
            (30, -25),
            10,
        )


class PB_NO(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        self.add_line(
            (10, -10),
            (50, -10),
        )

        self.add_line(
            (30, -10),
            (30, 10),
        )

        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class PB_NC(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        self.add_line(
            (10, -5),
            (50, -5),
        )

        self.add_line(
            (30, -5),
            (30, 10),
        )

        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class CG(Symbol):
    def __init__(self, ):
        super().__init__()

    def draw(self):
        self.add_line((0, 0), (0, -12))
        self.add_line((-6, -12), (6, -12))

        self.add_line((-6, -12), (-9, -17))
        self.add_line((0, -12), (-3, -17))
        self.add_line((6, -12), (3, -17))


class NO(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        self.draw_no_contact()


class NC(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        self.draw_nc_contact()


class ETERM(Symbol):
    def __init__(self):
        super().__init__()

    def draw(self):
        self.draw_terminal()


class ITERM(Symbol):

    def __init__(self, left=True, right=True, label=None):
        super().__init__()
        self._left = left
        self._right = right
        self._label = label

    def draw(self):
        self.draw_inline_terminal(left=self._left,
                                  right=self._right,
                                  label=self._label)


class SOL(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        self.draw_inline_terminal()
        self.move((btu(1), 0))
        self.draw_magnetic()
        self.move((btu(1), 0))
        self.draw_inline_terminal()


class OL(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        ITERM().sym_plot(self)
        self.move((btu(1), 0))
        self.draw_thermal()

        self.move((btu(2), 0))

        ITERM().sym_plot(self)


class CB(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        ITERM(left=True, right=False).sym_plot(self)
        self.add_arc(center=(30, -5), radius=25, start=37, end=143)
        ITERM(left=False, right=True)\
            .sym_plot(self, (btu(2), 0))

    def draw_multipole(self):
        self.draw_multipole_basic()

        self.add_line(
            (30, 20),
            (30, 20 + (self.pole_offset[1] * (self.poles - 1))),
            linetype='PHANTOM'
        )


class GEN_DEV_NC(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        ETERM().sym_plot(self)

        self.add_line(
            (20, 0),
            (40, 0)
        )

        NC().sym_plot(self, offset=(btu(2), 0))

        self.add_line(
            (60, 0),
            (80, 0)
        )

        ETERM().sym_plot(self, offset=(btu(4), 0))

        self.add_rectangle(
            [
                (-10, 20),
                (110, -20)
            ],
            attr={'flags': ezdxf.const.POLYLINE_CLOSED, 'linetype': 'PHANTOM'}
        )


class GEN_DEV_NO(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        ETERM().sym_plot(self)

        self.add_line(
            (20, 0),
            (40, 0)
        )

        NO().sym_plot(self, offset=(btu(2), 0))

        self.add_line(
            (60, 0),
            (80, 0)
        )

        ETERM().sym_plot(self, offset=(btu(4), 0))

        self.add_rectangle(
            [
                (-10, 20),
                (110, -20)
            ],
            attr={'flags': ezdxf.const.POLYLINE_CLOSED, 'linetype': 'PHANTOM'}
        )


class GEN_DEV(Symbol):

    def __init__(self):
        super().__init__()

    def draw(self):
        ETERM().sym_plot(self)

        ETERM().sym_plot(self, offset=(btu(4), 0))

        self.add_rectangle(
            [
                (-10, 20),
                (110, 20),
                (110, -20),
                (-10, -20)
            ],
            attr={'flags': ezdxf.const.POLYLINE_CLOSED, 'linetype': 'PHANTOM'}
        )
