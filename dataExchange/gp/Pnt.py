"""
gp_Pnt 的数据交换
Author: ICO
Date: 2024-01-21"""

import numpy as np
# logger
from loguru import logger
# pyOCC
from OCC.Core.gp import gp_Pnt

# local
from basicGeometricTyping import Point


def from_point(pnt: gp_Pnt) -> Point:
    """获取 gp_Pnt 的三坐标

    Parameters
    ----------
    pnt : gp_Pnt
        _description_

    Returns
    -------
    tuple[float, float, float]
        返回点的元组
    """
    return np.matrix([[pnt.X(), pnt.Y(), pnt.Z()]])


# end def
