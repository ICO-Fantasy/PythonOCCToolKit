"""
获取点的坐标
Author: ICO
Date: 2024-01-21"""
from OCC.Core.gp import gp_Pnt


def get_point(pnt: gp_Pnt):
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
    return (pnt.X(), pnt.Y(), pnt.Z())


# end def
