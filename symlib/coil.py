import entity
from symlib.bit import MAGNETIC
from symlib.terminal import ITERM


class SOL(entity.CodedSymbol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate(self):
        return [
            ITERM(),
            MAGNETIC().translate(xoff=20),
            ITERM().translate(xoff=40),
        ]
