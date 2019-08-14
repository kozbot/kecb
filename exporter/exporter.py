import entity
import config as cfg
from affine import Affine


class Exporter:
    def __init__(self):
        super().__init__()

    def draw(self, ent, transform=None):
        if transform is None:
            transform = entity.Transform(scale=cfg.EXPORTER_SCALE_DEFAULT)
        if isinstance(ent, entity.Point):
            self.draw_point(ent, transform=transform)
        elif isinstance(ent, entity.Line):
            self.draw_line(ent, transform=transform)
        elif isinstance(ent, entity.PolyLine):
            self.draw_polyline(ent, transform=transform)
        elif isinstance(ent, entity.Rect):
            self.draw_rect(ent, transform=transform)
        elif isinstance(ent, entity.Arc):
            self.draw_arc(ent, transform=transform)
        elif isinstance(ent, entity.Circle):
            self.draw_circle(ent, transform=transform)
        elif isinstance(ent, entity.Group):
            for child in ent.children:
                self.draw(child, transform=ent.affine() + transform)
        elif type(ent) is list:
            for i in ent:
                self.draw(i, transform=transform)
        else:
            raise ValueError("Entity Type not supported.")

    def draw_point(self, ent: entity.Point, transform=None):
        raise NotImplementedError()

    def draw_line(self, ent: entity.Line, transform=None):
        raise NotImplementedError()

    def draw_polyline(self, ent: entity.PolyLine, transform=None):
        raise NotImplementedError()

    def draw_rect(self, ent: entity.Rect, transform=None):
        raise NotImplementedError()

    def draw_arc(self, ent, transform=None):
        raise NotImplementedError()

    def draw_circle(self, ent: entity.Circle, transform=None):
        raise NotImplementedError()

    def saveas(self, filename: str):
        raise NotImplementedError

    def transform_point(self, point, transform):
        p = point * Affine.translation(xoff=transform.offset[0], yoff=transform.offset[1])
        p *= Affine.rotation(transform.rotation)
        p *= Affine.translation(xoff=transform.origin[0], yoff=transform.origin[1])
        p *= Affine.scale(transform.scale)
        return p
