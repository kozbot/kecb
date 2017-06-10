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

    def plot(self, layout, origin, offset, scale, rotation):
        self.layout = layout
        self.origin = origin
        self.offset = offset
        self.rotation = rotation
        self.scale = scale
        self.draw()

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
            start,  # Start Angle (draws CCW)
            end  # End Angle
        )

    def add_line(self, start, end):
        self.layout.add_line(
            self.trans_xy(start),
            self.trans_xy(end)
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
            attr
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
