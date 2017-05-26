from drawable import Drawable
import numpy as np


class Symbol(Drawable):

    def __init__(self):
        super(Symbol, self).__init__()


class NO(Symbol):

    def __init__(self):
        super(NO, self).__init__()

    def draw(self):
        print(self.offset)
        self.layout.add_line(
            (np.array([0, 0]) + self.offset) * self.scale,
            (np.array([10, 10]) + self.offset) * self.scale
        )
