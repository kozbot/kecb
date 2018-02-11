import entity
from affine import Affine


class Exporter:
    def __init__(self):
        super().__init__()
        self.transform = Affine.identity()

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
        elif isinstance(ent, entity.Group):
            pre_transform = self.transform
            self.transform *= ent.transform
            for c in ent.children:
                self.draw(c)
        elif type(ent) is list:
            for i in ent:
                self.draw(i)
        else:
            raise ValueError("Entity Type not supported.")

    def draw_point(self, ent):
        raise NotImplementedError()

    def draw_line(self, ent: entity.Line):
        raise NotImplementedError()

    def draw_circle(self, ent):
        raise NotImplementedError()

    def draw_arc(self, ent):
        raise NotImplementedError()

    def draw_rect(self, ent):
        raise NotImplementedError()

    def draw_polyline(self, ent:entity.PolyLine):
        raise NotImplementedError()

    def saveas(self, filename:str):
        raise NotImplementedError


