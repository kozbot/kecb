import config as cfg
from affine import Affine
from utils import btu


class Drawable(object):

    _sym_plot_limit = 0

    def __init__(self):
        super(Drawable, self).__init__()
        self.plot_offset = (btu(1), 0)
        self.extents = (btu(1), btu(1))

    def draw(self):
        raise NotImplementedError("draw method not implemented")

    def draw_multipole(self):
        self.draw_multipole_basic()

    def draw_multipole_basic(self):
        px, py = self.pole_offset
        original_offset = self.offset
        for i in range(0, self.poles):
            self.offset =\
                original_offset * Affine.translation(xoff=px * i, yoff=py * i)
            self.draw()

        self.offset = original_offset

    def plot(self, layout, origin, offset, scale, rotation,
             poles, pole_offset):
        self.layout = layout
        self.origin = origin
        self.offset = offset
        self.rotation = rotation
        self.scale = scale
        self.poles = poles
        self.pole_offset = pole_offset
        if poles == 1:
            self.draw()
        else:
            self.draw_multipole()

    def sym_plot(self, sym, offset=(0, 0)):
        if Drawable._sym_plot_limit >= 20:
            raise RecursionError()

        Drawable._sym_plot_limit += 1
        self.layout = sym.layout
        self.scale = sym.scale
        self.origin = sym.origin
        self.rotation = sym.rotation
        self.offset = sym.offset * Affine.translation(*offset)
        self.draw()
        Drawable._sym_plot_limit -= 1

    def add_arc(self, center, radius, start, end):
        self.layout.add_arc(
            self.trans_xy(center),
            self.trans_scale(radius),
            start + self.rotation,  # Start Angle (draws CCW)
            end + self.rotation  # End Angle
        )

    def add_line(self, start, end, **atr):
        self.layout.add_line(
            self.trans_xy(start),
            self.trans_xy(end),
            dxfattribs={
                'linetype': atr.get('linetype', 'BYLAYER')
            }
        )

    def add_circle(self, center, radius):
        self.layout.add_circle(
            self.trans_xy(center),
            self.trans_scale(radius)  # Radius
        )

    def add_text(self, label, pos, height=10, alignment='MIDDLE_CENTER'):
        if cfg.DISABLE_TEXT is not True:
            self.layout.add_text(
                label, dxfattribs={'height': self.trans_scale(height)}
            ).set_pos(
                self.trans_xy(pos),
                align=alignment
            )

    def add_polyline2d(self, points, attr={}):
        self.layout.add_polyline2d(
            [self.trans_xy(point) for point in points],
            dxfattribs=attr
        )

    def add_rectangle(self, points, attr={}):
        if(len(points) < 2):
            raise NotImplementedError(
                "Only a list of 2 or more points supported.")

        leftmost = min(points, key=lambda x: x[0])

        rightmost = max(points, key=lambda x: x[0])

        topmost = max(points, key=lambda y: y[1])

        botmost = min(points, key=lambda y: y[1])

        if(leftmost[0] == rightmost[0]):
            raise ValueError("X coordinates must not be the same.")

        if(topmost[1] == botmost[1]):
            raise ValueError("Y coordinates must not be the same.")

        # TL = (leftmost[0], topmost[1])
        # TR = (rightmost[0], topmost[1])
        # BR = (rightmost[0], botmost[1])
        # BL = (leftmost[0], botmost[1])

        plist = [
            (leftmost[0], topmost[1]),
            (rightmost[0], topmost[1]),
            (rightmost[0], botmost[1]),
            (leftmost[0], botmost[1])
        ]

        self.layout.add_polyline2d(
            [self.trans_xy(point) for point in plist],
            dxfattribs=attr
        )

    def move(self, dist):
        self.offset = self.offset * Affine.translation(*dist)

    def trans_scale(self, number):
        return self.scale * number

    def trans_xy(self, point):
        p = point * Affine.translation(*self.offset)
        p *= Affine.rotation(self.rotation)
        p *= Affine.translation(*self.origin)
        p *= Affine.scale(self.scale)

        return p
