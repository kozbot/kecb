from .exporter import Exporter
import ezdxf
from ezdxf.tools import standards as std
import entity


class DxfExporter(Exporter):

    def __init__(self):
        super().__init__()
        self.dwg = ezdxf.new(dxfversion='AC1015')
        for linetype in std.linetypes():
            try:
                self.dwg.linetypes.new(name=linetype[0],
                                       dxfattribs={'description': linetype[1],
                                                   'pattern': linetype[2]})
            except ValueError as e:
                pass
        self.msp = self.dwg.modelspace()

    def draw_line(self, ent: entity.Line):
        attr = {'linetype': 'BYLAYER'}
        if ent.linetype is not None:
            attr['linetype'] = ent.linetype
        self.msp.add_line(ent.start, ent.end)

    def draw_polyline(self, ent: entity.PolyLine):
        attr = {}
        if ent.closed:
            attr['flags'] = ezdxf.const.POLYLINE_CLOSED
        self.msp.add_polyline2d(ent.points, dxfattribs=attr)

    def saveas(self, filename: str):
        self.dwg.saveas(filename=filename)
