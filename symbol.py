from drawable import Drawable
import ezdxf
import config as cfg


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


class SOL(Symbol):  # Need to add inline terminals to finish this

    def __init__(self):
        super(SOL, self).__init__()

    def draw(self):
        self.draw_inline_terminal()
        self.move((1, 0))
        self.draw_magnetic()
        self.move((1, 0))
        self.draw_inline_terminal()


class OL(Symbol):  # Need to add inline terminals to finish this

    def __init__(self):
        super(OL, self).__init__()

    def draw(self):
        ITERM().sym_plot(self)
        self.move((1, 0))
        self.draw_thermal()

        self.move((2, 0))

        ITERM().sym_plot(self)


class CB(Symbol):
    def __init__(self, ):
        super(CB, self).__init__()

    def draw(self):
        ITERM(left=True, right=False).sym_plot(self)
        self.add_arc(center=(30, -5), radius=25, start=37, end=143)
        ITERM(left=False, right=True)\
            .sym_plot(self, (2 * cfg.UPB, 0))
