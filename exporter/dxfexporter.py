from .exporter import Exporter
import ezdxf
from ezdxf.tools import standards as std
import entity
import config as cfg


class DxfExporter(Exporter):

    def __init__(self):
        super().__init__()
        self.dwg = ezdxf.new(dxfversion='AC1015')
        ezdxf.setup_linetypes(self.dwg)
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
            attr['ltscale'] = cfg.LINETYPE_SCALE
        if transform is not None:
            start = self.transform_point((ent.start.x, ent.start.y), transform)
            end = self.transform_point((ent.end.x, ent.end.y), transform)
        else:
            start = (ent.start.x, ent.start.y)
            end = (ent.end.x, ent.end.y)
        self.msp.add_line(start, end, dxfattribs=attr)

    def draw_rect(self, ent: entity.Rect, transform=None):
        attr = {}
        attr['flags'] = ezdxf.const.POLYLINE_CLOSED
        if ent.linetype is not None:
            attr['linetype'] = ent.linetype
            attr['ltscale'] = cfg.LINETYPE_SCALE
        points = []
        for p in ent.points:
            if transform is not None:
                points.append(self.transform_point((p.x, p.y), transform))
            else:
                points.append((p.x, p.y))

        self.msp.add_polyline2d(points, dxfattribs=attr)

    def draw_polyline(self, ent: entity.PolyLine, transform=None):
        attr = {}
        if ent.closed:
            attr['flags'] = ezdxf.const.POLYLINE_CLOSED
        if ent.linetype is not None:
            attr['linetype'] = ent.linetype
            attr['ltscale'] = cfg.LINETYPE_SCALE
        points = []
        for p in ent.points:
            if transform is not None:
                points.append(self.transform_point((p.x, p.y), transform))
            else:
                points.append((p.x, p.y))

        self.msp.add_polyline2d(points, dxfattribs=attr)

    def draw_circle(self, ent: entity.Circle, transform=None):
        attr = {}
        if transform is not None:
            center = self.transform_point((ent.center.x, ent.center.y), transform)
            radius = ent.radius * transform.scale
        else:
            center = (ent.center.x, ent.center.y)
            radius = ent.radius
        self.msp.add_circle(center, radius, dxfattribs=attr)

    def draw_arc(self, ent, transform=None):
        if transform is not None:
            center = self.transform_point((ent.center.x, ent.center.y), transform)
            radius = ent.radius * transform.scale
            start = ent.start + transform.rotation
            end = ent.end + transform.rotation
        else:
            center = (ent.center.x, ent.center.y)
            radius = ent.radius
            start = ent.start
            end = ent.end
        self.msp.add_arc(center=center, radius=radius, start_angle=start, end_angle=end)

    def saveas(self, filename: str):
        self.dwg.saveas(filename=filename)
