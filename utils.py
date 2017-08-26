import config
from collections import namedtuple
import ezdxf
from ezdxf.tools import standards as std


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


def new_dwg():
    dwg = ezdxf.new(dxfversion='AC1015')
    for linetype in std.linetypes():
        try:
            dwg.linetypes.new(name=linetype[0],
                              dxfattribs={'description': linetype[1],
                                          'pattern': linetype[2]})
        except ValueError as e:
            pass

    return dwg
