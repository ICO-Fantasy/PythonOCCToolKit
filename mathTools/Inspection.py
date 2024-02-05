"""
几何检查工具
Author: ICO
Date: 2024-02-05
"""

import numpy as np

from basicGeometricTyping import Point


def collinear_check(point_1: Point, point_2: Point, point_3: Point, linear_tolerance=1e-6) -> bool:
    """检查三点是否共线

    Parameters
    ----------
    `point_1` : Point
    `point_2` : Point
    `point_3` : Point
    `linear_tolerance` : float, 可选
        阈值，默认值：1e-6

    Returns
    -------
    bool
    共线则为 True，否则为 False
    """
    LINEAR_TOLERANCE = linear_tolerance
    vector_AB = np.array(point_1) - np.array(point_3)
    vector_AC = np.array(point_2) - np.array(point_3)
    # 如果叉乘结果为零向量，则说明三点共线
    cross_product = np.cross(vector_AB, vector_AC)
    # 使用阈值来容忍小的数值误差
    return np.linalg.norm(cross_product) < LINEAR_TOLERANCE
