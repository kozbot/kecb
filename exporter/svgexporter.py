from .exporter import Exporter
import svgwrite
import entity

class SvgExporter(Exporter):

    def __init__(self):
        super().__init__()
        self.dwg: svgwrite.Drawing = svgwrite.Drawing()

    def saveas(self, filename: str):
        self.dwg.saveas(filename=filename)

    def draw_point(self, ent):
        pass

    def draw_line(self, ent: entity.Line):
        self.dwg.add(self.dwg.line(start=ent.start,end=ent.end,stroke=svgwrite.rgb(0, 0, 0, '%')))

    def draw_circle(self, ent):
        pass

    def draw_arc(self, ent):
        pass

    def draw_rect(self, ent):
        pass

    def draw_polyline(self, ent: entity.PolyLine):
        pass