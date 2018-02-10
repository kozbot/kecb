import entity


class Exporter:

    def draw(self, ent):
        if isinstance(ent, entity.Point):
            self.draw_point(ent)
        elif isinstance(ent, entity.Line):
            self.draw_line(ent)
        elif isinstance(ent, entity.PolyLine):
            self.draw_polyline(ent)
        elif isinstance(ent, entity.Rect):
            self.draw_rect(ent)
        elif isinstance(ent, entity.Arc):
            self.draw_arc(ent)
        elif isinstance(ent, entity.Circle):
            self.draw_circle(ent)
        else:
            raise ValueError("Entity Type: " + type(ent) + " not supported.")

    def draw_point(self, ent):
        raise NotImplementedError()

    def draw_line(self, ent):
        raise NotImplementedError()

    def draw_circle(self, ent):
        raise NotImplementedError()

    def draw_arc(self, ent):
        raise NotImplementedError()

    def draw_rect(self, ent):
        raise NotImplementedError()

    def draw_polyline(self, ent):
        raise NotImplementedError()


import ezdxf
from ezdxf.tools import standards as std


class ExportDXF(Exporter):

    def draw_point(self, ent):
        pass

    def draw_line(self, ent):
        pass

    def draw_circle(self, ent):
        pass

    def draw_arc(self, ent):
        pass

    def draw_rect(self, ent):
        pass

    def draw_polyline(self, ent):
        pass


class ExportSVG(Exporter):
    def draw_point(self, ent):
        pass

    def draw_line(self, ent):
        pass

    def draw_circle(self, ent):
        pass

    def draw_arc(self, ent):
        pass

    def draw_rect(self, ent):
        pass

    def draw_polyline(self, ent):
        pass
