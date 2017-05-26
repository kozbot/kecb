class Drawable(object):  # Stub class in case I find a use for it

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
