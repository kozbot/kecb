import numpy as np
import config as cfg


class Drawable(object):

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

    def add_line(self, start, end):
        self.layout.add_line(
            (np.array([start[0], start[1]]) + self.offset) * self.scale,
            (np.array([end[0], end[1]]) + self.offset) * self.scale
        )

    def add_circle(self, center, radius):
        self.layout.add_circle(
            (np.array([center[0], center[1]]) + self.offset) * self.scale,
            (np.array([radius])) * cfg.UNIT_SCALE  # Radius
        )

    def add_text(self, label, pos, height=10, alignment='MIDDLE_CENTER'):
        if cfg.DISABLE_TEXT is not False:
            self.layout.add_text(
                label, dxfattribs={'height': height * cfg.UNIT_SCALE}
            ).set_pos(
                (np.array([pos[0], pos[1]]) + self.offset) * self.scale,
                align=alignment
            )

    def add_polyline2d(self, points, attr={}):
        self.layout.add_polyline2d(
            [(np.array([point[0], point[1]]) + self.offset) * self.scale
                for point in points],
            attr
        )
