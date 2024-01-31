"""
三点定圆
Author: ICO
Date: 2024-01-21"""
from OCC.Core.gp import gp_Ax2, gp_Circ

from dataExchange import get_point
from mathTools import three_point_fixed_circle


def make_circle_from_three_points(point1, point2, point3):
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
    p1 = get_point(point1)
    p2 = get_point(point2)
    p3 = get_point(point3)
    circle_center, radius, angle = three_point_fixed_circle(p1, p2, p3)
    gp_Ax2()
    return gp_Circ()
