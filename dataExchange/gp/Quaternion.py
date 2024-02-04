"""
gp_Quaternion 的数据交换
Author: ICO
Date: 2024-02-04"""

import json

import numpy as np

# logger
from loguru import logger

# pyOCC
from OCC.Core.gp import gp_Dir, gp_EulerSequence, gp_Quaternion, gp_Trsf

# local
from geometricTyping import Quaternion


def gp_Quaternion2quat(quat: gp_Quaternion) -> Quaternion:
    return np.matrix([[quat.X(), quat.Y(), quat.Z(), quat.W()]])


# end def
def gp_Quaternion2euler(quat: gp_Quaternion, sequence="euler"):
    match sequence:
        case "euler":
            gp_sequence = gp_EulerSequence.gp_EulerAngles
        case "ypr":
            gp_sequence = gp_EulerSequence.gp_YawPitchRoll
        case "sxyz":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_XYZ
        case "sxzy":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_XZY
        case "syzx":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_YZX
        case "syxz":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_YXZ
        case "szxy":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_ZXY
        case "szyx":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_ZYX
        case "rxyz":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_XYZ
        case "rxzy":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_XZY
        case "ryzx":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_YZX
        case "ryxz":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_YXZ
        case "rzxy":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_ZXY
        case "rzyx":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_ZYX
        case "sxyx":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_XYX
        case "sxzx":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_XZX
        case "syzy":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_YZY
        case "syxy":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_YXY
        case "szyz":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_ZYZ
        case "szxz":
            gp_sequence = gp_EulerSequence.gp_Extrinsic_ZXZ
        case "rxyx":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_XYX
        case "rxzx":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_XZX
        case "ryzy":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_YZY
        case "ryxy":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_YXY
        case "rzxz":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_ZXZ
        case "rzyz":
            gp_sequence = gp_EulerSequence.gp_Intrinsic_ZYZ
        case _:
            gp_sequence = gp_EulerSequence.gp_EulerAngles
    # end match
    return quat.GetEulerAngles(gp_sequence)
