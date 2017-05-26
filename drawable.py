import numpy as np


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
        raise NotImplementedError()

    def add_text(self, label, pos, height=10, alignment='MIDDLE_CENTER'):
        raise NotImplementedError()

    def add_polyline2d(self, points, attr={}):
        self.layout.add_polyline2d(
            [(np.array([point[0], point[1]]) + self.offset) * self.scale
                for point in points],
            attr
        )
