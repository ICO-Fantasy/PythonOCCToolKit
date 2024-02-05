"""
三点定圆
Author: ICO
Date: 2024-01-21"""
from OCC.Core.gp import gp_Ax2, gp_Circ, gp_Pnt

from basicGeometricTyping import Point
from dataExchange.gp import from_point
from mathTools import three_point_fixed_circle


def make_circle_from_three_points(point_1:gp_Pnt, point_2:gp_Pnt, point_3:gp_Pnt):
    """三点定圆

    Parameters
    ----------
    `point1` : _type_
        _description_
    `point2` : _type_
        _description_
    `point3` : _type_
        _description_

    Returns
    -------
    _type_
        圆心，半径，角度
    """
    p1 = from_point(point_1)
    p2 = from_point(point_2)
    p3 = from_point(point_3)
    circle_center, radius, angle = three_point_fixed_circle(p1, p2, p3)
    _ax=gp_Ax2()
    return gp_Circ(_ax,)
