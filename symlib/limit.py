import entity
from symlib.terminal import ITERM

LSW_NC_LINE_END = 5.77350269189626


class LSW_NC(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(right=False),
            entity.Line(entity.Point(15, 0), entity.Point(55, LSW_NC_LINE_END)),
            ITERM(left=False).translate(xoff=40, yoff=0)
        ]
