"""计算两点线段间距离"""
import math
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from typing import Callable, Union

import numpy as np
import numpy.typing as npt

from todo.threePointFixedCircle import three_point_fixed_circle

# 创建一个类型别名，用于表示数组
FloatArray = npt.NDArray[np.float_]


def distanceBetweenPointCircle(
    p,
    p1: Union[FloatArray, tuple[FloatArray, FloatArray, FloatArray], list[FloatArray]],
    p2: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]] = None,
    p3: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]] = None,
) -> tuple[np.float_, FloatArray]:
    """计算点到线段 (a0, a1) 之间的最短距离以及最短距离点。

    Args:
        point: 点
        a0 (npt.NDArray): 线段的起点
        a1 (npt.NDArray): 线段的终点
        a3 (npt.NDArray): 线段的终点

    Returns:
        tuple[npt.NDArray, float]: 最短距离点在线段上的坐标以及它们之间的最短距离。
    """
    if isinstance(p1, (tuple, list)):
        p1, p2, p3 = p1
    circle_center, radius, _ = three_point_fixed_circle(p1.tolist(), p2.tolist(), p3.tolist())
    distance = np.linalg.norm(p - circle_center)
    if distance <= radius:
        distance = 0.0
    else:
        distance = distance - radius
    # todo nearest_point
    return distance, _  # type: ignore


if __name__ == "__main__":
    p1 = np.array([1, 70.0, 3])
    p2 = np.array([-212.0055, -70.0, -64.0])
    p3 = np.array([-212.0055, 70.0, -80.0])
    p4 = np.array([-212.0055, -70.0, -80.0])
    distance, nearest_point = distanceBetweenPointCircle(p1, p2, p3, p4)
    print(distance)
# end main
