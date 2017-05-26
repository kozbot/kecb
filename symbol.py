from drawable import Drawable
import numpy as np


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


class SOL(Symbol):  # Need to add inline terminals to finish this

    def __init__(self):
        super(SOL, self).__init__()

    def draw(self):
        self.draw_magnetic()
