from drawable import Drawable
import ezdxf
from utils import btu


class Symbol(Drawable):

    def __init__(self):
        super(Symbol, self).__init__()

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
        super(PE, self).__init__()

    def draw(self):
        self.add_line((0, 0), (0, -12))
        self.add_line((-6, -12), (6, -12))
        self.add_line((-4, -14), (4, -14))
        self.add_line((-2, -16), (2, -16))


class SG(Symbol):
    def __init__(self, ):
        super(SG, self).__init__()

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
        super(LSW_NC, self).__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        # *** CODE USED TO CALCULATE ***
        # from sympy import Point, Ellipse, Line
        # from sympy.geometry import Ray

        # te = Ellipse(Point(50, 0), 5, 5)
        # tans = te.tangent_lines(Point(15, 0))
        # wall = Line(p1=(55, 0), p2=(55, 10))
        # r = Ray(p1=tans[1].p1, p2=tans[1].p2)

        # print(r.intersection(wall)[0].evalf())

        self.add_line(
            (15, 0),
            (55, 5.77350269189626),
        )
        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class LSW_NO(Symbol):
    def __init__(self, ):
        super(LSW_NO, self).__init__()

    def draw(self):
        self.draw_inline_terminal(right=False)

        # *** CODE USED TO CALCULATE ***
        # from sympy import Point, Ellipse, Line
        # from sympy.geometry import Ray
        # from mpmath import *

        # te = Ellipse(Point(50, 0), 5, 5)
        # tans = te.tangent_lines(Point(15, 0))
        # wall = Line(p1=(55, -30), p2=(55, 30))
        # r = Ray(p1=tans[1].p1, p2=tans[1].p2)

        # print("NC Switch Line Endpoint:")
        # print(r.intersection(wall)[0].evalf())

        # nol = tans[0].rotate(radians(-5), Point(15, 0))

        # r = Ray(p1=nol.p1, p2=nol.p2)

        # print("NO Switch Line Endpoint:")
        # print(r.intersection(wall)[0].evalf())

        self.add_line(
            (15, 0),
            (55, -9.39164600762439),
        )
        self.move((btu(2), 0))
        self.draw_inline_terminal(left=False)


class CG(Symbol):
    def __init__(self, ):
        super(CG, self).__init__()

    def draw(self):
        self.add_line((0, 0), (0, -12))
        self.add_line((-6, -12), (6, -12))

        self.add_line((-6, -12), (-9, -17))
        self.add_line((0, -12), (-3, -17))
        self.add_line((6, -12), (3, -17))


class NO(Symbol):

    def __init__(self):
        super(NO, self).__init__()

    def draw(self):
        self.draw_no_contact()


class NC(Symbol):

    def __init__(self):
        super(NC, self).__init__()

    def draw(self):
        self.draw_nc_contact()


class ETERM(Symbol):
    def __init__(self):
        super(ETERM, self).__init__()

    def draw(self):
        self.draw_terminal()


class ITERM(Symbol):

    def __init__(self, left=True, right=True, label=None):
        super(ITERM, self).__init__()
        self._left = left
        self._right = right
        self._label = label

    def draw(self):
        self.draw_inline_terminal(left=self._left,
                                  right=self._right,
                                  label=self._label)


class SOL(Symbol):

    def __init__(self):
        super(SOL, self).__init__()

    def draw(self):
        self.draw_inline_terminal()
        self.move((btu(1), 0))
        self.draw_magnetic()
        self.move((btu(1), 0))
        self.draw_inline_terminal()


class OL(Symbol):

    def __init__(self):
        super(OL, self).__init__()

    def draw(self):
        ITERM().sym_plot(self)
        self.move((btu(1), 0))
        self.draw_thermal()

        self.move((btu(2), 0))

        ITERM().sym_plot(self)


class CB(Symbol):

    def __init__(self):
        super(CB, self).__init__()

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
        super(GEN_DEV_NC, self).__init__()

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
        super(GEN_DEV_NO, self).__init__()

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
        super(GEN_DEV, self).__init__()

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
