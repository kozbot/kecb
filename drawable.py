import numpy as np
import config as cfg


class Drawable(object):

    _sym_plot_limit = 0

    def __init__(self):
        super(Drawable, self).__init__()
        self.plot_offset = (1, 0)
        self.extents = (1, 1)

    def draw(self):
        raise NotImplementedError("draw method not implemented")

    def plot(self, layout, scale, offset):
        self.layout = layout
        self.scale = scale
        self.offset = offset
        self.draw()

    def sym_plot(self, sym, offset=np.array(np.mat('0; 0'))):
        if Drawable._sym_plot_limit >= 20:
            raise RecursionError()

        Drawable._sym_plot_limit += 1
        self.layout = sym.layout
        self.scale = sym.scale
        self.offset = sym.offset + offset
        self.draw()
        Drawable._sym_plot_limit -= 1

    def add_arc(self, center, radius, start, end):
        self.layout.add_arc(
            # (np.array([center[0], center[1]]) + self.offset) * self.scale,
            self.trans_xy(center),
            # (np.array([radius])) * cfg.UNIT_SCALE,
            self.trans_scale(radius),
            start,  # Start Angle (draws CCW)
            end  # End Angle
        )

    def add_line(self, start, end):
        self.layout.add_line(
            # (np.array([start[0], start[1]]) + self.offset) * self.scale,
            self.trans_xy(start),
            # (np.array([end[0], end[1]]) + self.offset) * self.scale
            self.trans_xy(end)
        )

    def add_circle(self, center, radius):
        self.layout.add_circle(
            # (np.array([center[0], center[1]]) + self.offset) * self.scale,
            self.trans_xy(center),
            self.trans_scale(radius)  # Radius
        )

    def add_text(self, label, pos, height=10, alignment='MIDDLE_CENTER'):
        if cfg.DISABLE_TEXT is not True:
            self.layout.add_text(
                # label, dxfattribs={'height': height * cfg.UNIT_SCALE}
                label, dxfattribs={'height': self.trans_scale(height)}
            ).set_pos(
                # (np.array([pos[0], pos[1]]) + self.offset) * self.scale,
                self.trans_xy(pos),
                align=alignment
            )

    def add_polyline2d(self, points, attr={}):
        self.layout.add_polyline2d(
            [self.trans_xy(point) for point in points],
            attr
        )

    def move(self, dist):
        mvoff = np.array([[dist[0] * cfg.UPB], [dist[1] * cfg.UPB]])

        self.offset = self.offset + mvoff

    def trans_scale(self, number):
        return self.scale[0] * number

    def trans_xy(self, point):
        return (self.scale * np.array([[point[0]], [point[1]]])) + self.offset
