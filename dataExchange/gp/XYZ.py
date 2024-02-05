"""
gp_XYZ 的数据交换
Author: ICO
Date: 2024-02-04"""

# logger
from loguru import logger

# pyOCC
from OCC.Core.gp import gp_XYZ


def from_gp_XYZ(xyz: gp_XYZ):
    """获取 gp_XYZ 的取值

    Parameters
    ----------
    pnt : gp_XYZ
        _description_

    Returns
    -------
    tuple[float, float, float]
        返回点的元组
    """
    return (xyz.X(), xyz.Y(), xyz.Z())


# end def
