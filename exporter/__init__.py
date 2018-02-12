from importlib.util import find_spec

HAVE_DXF = False
if find_spec('ezdxf') is not None:
    HAVE_DXF = True
    from .dxfexporter import DxfExporter

HAVE_SVG = False
if find_spec('svgwrite') is not None:
    HAVE_SVG = True
    from .svgexporter import SvgExporter
