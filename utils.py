import config
from collections import namedtuple


# Convert blocks to units
def btu(block):
    return block * config.UNITS_PER_BLOCK


def pack_transform(origin=(0, 0),
                   offset=(0, 0),
                   scale=config.UNIT_SCALE,
                   rotation=0):

    Transform = namedtuple('Transform',
                           ['origin', 'offset', 'scale', 'rotation'])

    t = Transform(origin=origin, offset=offset, scale=scale, rotation=rotation)

    return t
