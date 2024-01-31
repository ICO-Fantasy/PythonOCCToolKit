"""计算两点线段间距离"""
from typing import Callable, Union

import numpy as np
import numpy.typing as npt

# 创建一个类型别名，用于表示数组
FloatArray = npt.NDArray[np.float_]


def distanceBetweenPointSegment(
    p,
    p1: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]],
    p2: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]] = None,
) -> tuple[np.float_, FloatArray]:
    """计算点到线段 (a0, a1) 之间的最短距离以及最短距离点。

    Args:
        point: 点
        a0 (npt.NDArray): 线段的起点
        a1 (npt.NDArray): 线段的终点

    Returns:
        tuple[npt.NDArray, float]: 最短距离点在线段上的坐标以及它们之间的最短距离。
    """
    if isinstance(p1, (tuple, list)):
        p1, p2 = p1
    # 将点p1和p2视为向量
    v1 = p2 - p1
    v2 = p - p1

    # 计算点p在线段上的投影点
    t = np.dot(v2, v1) / np.dot(v1, v1)

    # 如果投影点在线段内部，则最短距离是投影点到点p的距离
    if t >= 0.0 and t <= 1.0:
        projection = p1 + t * v1
        distance = np.linalg.norm(p - projection)
        nearest_point = projection
    else:
        # 如果投影点在线段之外，则最短距离是点p到线段端点p1和p2中的较近者
        distance1 = np.linalg.norm(p - p1)
        distance2 = np.linalg.norm(p - p2)
        if distance1 < distance2:
            distance = distance1
            nearest_point = p1
        else:
            distance = distance2
            nearest_point = p2

    return distance, nearest_point  # type: ignore


if __name__ == "__main__":
    p1 = np.array([1, 70.0, 3])
    p2 = np.array([-212.0055, -70.0, -64.0])
    p3 = np.array([-212.0055, 70.0, -80.0])
    p4 = np.array([-212.0055, -70.0, -80.0])
    distance, nearest_point = distanceBetweenPointSegment(p1, p2, p3)
    print(distance)
# end main
