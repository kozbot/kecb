from .exporter import Exporter
import ezdxf
from ezdxf.tools import standards as std
import entity
from affine import Affine


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

    def draw_point(self, ent: entity.Point, transform=None):
        attr = {}
        if transform is not None:
            point = self.transform_point(ent.x, ent.y)
        else:
            point = (ent.x, ent.y)
        self.msp.add_point(point, dxfattribs=attr)

    def draw_line(self, ent: entity.Line, transform=None):
        attr = {'linetype': 'BYLAYER'}
        if ent.linetype is not None:
            attr['linetype'] = ent.linetype

        if transform is not None:
            start = self.transform_point((ent.start.x, ent.start.y), transform)
            end = self.transform_point((ent.end.x, ent.end.y), transform)
        else:
            start = (ent.start.x, ent.start.y)
            end = (ent.end.x, ent.end.y)
        print("LINE ENTITY: ", ent)
        print("LINE START: ", start, "LINE END: ", end)
        self.msp.add_line(start, end, dxfattribs=attr)

    def draw_polyline(self, ent: entity.PolyLine, transform=None):
        attr = {}
        if ent.closed:
            attr['flags'] = ezdxf.const.POLYLINE_CLOSED
        points = []
        for p in ent.points:
            if transform is not None:
                points.append(self.transform_point((p.x, p.y), transform))
            else:
                points.append((p.x, p.y))

        self.msp.add_polyline2d(points, dxfattribs=attr)

    def draw_circle(self, ent: entity.Circle, transform=None, scale=1):
        attr = {}
        if transform is not None:
            center = self.transform_point((ent.center.x, ent.center.y), transform)
            radius = ent.radius * transform.scale
        else:
            center = (ent.center.x, ent.center.y)
            radius = ent.radius
        self.msp.add_circle(center, radius, dxfattribs=attr)

    def saveas(self, filename: str):
        self.dwg.saveas(filename=filename)
