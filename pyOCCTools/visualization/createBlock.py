import math

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import *
from OCC.Core.TopLoc import TopLoc_Location

from printTools import *

boxsize = {
    "A": (448, 235, 548),
    "B": (550, 245, 565),
    "C": (483, 343, 350),
    "D": (488, 323, 253),
}


def makeBlock(index: str):
    type = index[0]
    gesture = index[1]
    num = int(index[2])
    lx, ly, lz = [float(x) for x in boxsize[type]]

    if type == "A" or "B":
        if gesture == "1":
            ablock = BRepPrimAPI_MakeBox(lx, ly * num, lz).Shape()
            atrsf = gp_Trsf()
            atrsf.SetTranslationPart(gp_Vec(lx, ly * num / 2, lz))
            aquat = gp_Quaternion()
            aquat.SetEulerAngles(gp_EulerSequence.gp_Intrinsic_YXY, -math.pi / 2, 0, 0)
            atrsf.SetRotationPart(aquat)
            atrsf.Invert()
            printTrsf(atrsf)
            newlocal = TopLoc_Location(atrsf)
            newblock = ablock.Moved(newlocal)
            return newblock
        elif gesture == "2":
            pass
        elif gesture == "3":
            pass
    elif type == "C" or "D":
        if gesture == "1":
            pass
        elif gesture == "2":
            pass
        elif gesture == "3":
            pass
