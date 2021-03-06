from exporter import DxfExporter
import symlib.contact as sc
import symlib.terminal as st
import symlib.ground as sg
import symlib.limit as sl
import symlib.generic as gen
import symlib.protect as protect
import symlib.coil as coil
import symlib.pilot as pilot
import inspect
import os
from entity import CodedSymbol


# TODO: Rather than all this insanity get a list of all the symlib.* classes and convert to set to eliminate duplicates.

def is_contact(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.contact")


def is_terminal(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.terminal")


def is_ground(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.ground")


def is_limit(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.limit")


def is_generic(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.generic")


def is_protect(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.protect")


def is_coil(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.coil")

def is_pilot(o):
    return inspect.isclass(o) and issubclass(o, CodedSymbol) and (o.__module__ == "symlib.pilot")

def export_list(symbols):
    for symbol in symbols:
        min_pole = symbol[1].min_pole
        max_pole = symbol[1].max_pole
        for pole in range(min_pole, max_pole + 1):
            d = DxfExporter()
            d.draw(symbol[1](poles=pole))
            if pole != 1 and min_pole != max_pole:
                d.saveas("./dxf/" + symbol[0] + "_" + str(pole) + "P.dxf")
                print(symbol[0] + "_" + str(pole))
            else:
                print(symbol[0])
                d.saveas("./dxf/" + symbol[0] + ".dxf")


if __name__ == "__main__":
    os.makedirs('./dxf',exist_ok=True)

    print("Contacts:")
    export_list(inspect.getmembers(sc, is_contact))

    print("Terminals:")
    export_list(inspect.getmembers(st, is_terminal))

    print("Grounds:")
    export_list(inspect.getmembers(sg, is_ground))

    print("Limit Switches:")
    export_list(inspect.getmembers(sl, is_limit))

    print("Generic Devices:")
    export_list(inspect.getmembers(gen, is_generic))

    print("Protection Symbols:")
    export_list(inspect.getmembers(protect, is_protect))

    print("Coil Symbols:")
    export_list(inspect.getmembers(coil, is_coil))

    print("Pilot Devices:")
    export_list(inspect.getmembers(pilot, is_pilot))
