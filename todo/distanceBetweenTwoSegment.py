"""计算两点线段间距离"""
from typing import Callable, Union

import numpy as np
import numpy.typing as npt

# 创建一个类型别名，用于表示数组
FloatArray = npt.NDArray[np.float_]


def distanceBetweenTwoSegment(
    a0: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]],
    a1: Union[FloatArray, tuple[FloatArray, FloatArray], list[FloatArray]],
    b0: Union[FloatArray, None] = None,
    b1: Union[FloatArray, None] = None,
    clampAll: bool = True,
    clampA0: bool = False,
    clampA1: bool = False,
    clampB0: bool = False,
    clampB1: bool = False,
) -> tuple[FloatArray, FloatArray, np.float_]:
    """计算两条由 numpy.array 对表示的线段 (a0, a1, b0, b1) 之间的最短距离以及最短距离点。

    Args:
        a0 (npt.NDArray): 线段 A 的起点
        a1 (npt.NDArray): 线段 A 的终点
        b0 (npt.NDArray): 线段 B 的起点
        b1 (npt.NDArray): 线段 B 的终点
        clampAll (bool, optional): 是否夹紧(clamp)所有线段。默认为 False。
        clampA0 (bool, optional): 是否夹紧线段 A 的起点。默认为 False。
        clampA1 (bool, optional): 是否夹紧线段 A 的终点。默认为 False。
        clampB0 (bool, optional): 是否夹紧线段 B 的起点。默认为 False。
        clampB1 (bool, optional): 是否夹紧线段 B 的终点。默认为 False。

    Returns:
        tuple[npt.NDArray, npt.NDArray, float]: 最短距离点在线段 A 和线段 B 上的坐标以及它们之间的最短距离。
    """
    if isinstance(a0, (tuple, list)):
        (a0, a1), (b0, b1) = a0, a1
    # 如果 clampAll=True，则设置所有夹紧标志为 True
    if clampAll:
        clampA0 = True
        clampA1 = True
        clampB0 = True
        clampB1 = True
    if not isinstance(b0, np.ndarray) or not isinstance(b1, np.ndarray):
        raise KeyError("输入错误")
    # 计算分母
    A = a1 - a0
    B = b1 - b0
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    _A = A / magA
    _B = B / magB

    cross = np.cross(_A, _B)
    denom = np.linalg.norm(cross) ** 2

    # 如果线段平行（分母为0），检查线段是否重叠
    # 如果不重叠，存在最短距离点
    # 如果重叠，存在无限多最短距离点，但仍然有最短距离
    if not denom:
        d0 = np.dot(_A, (b0 - a0))

        # 只有在夹紧的情况下才可能重叠
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A, (b1 - a0))

            # 线段 B 在线段 A 之前？
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.abs(d0) < np.abs(d1):
                        return a0, b0, np.linalg.norm(a0 - b0)
                    return a0, b1, np.linalg.norm(a0 - b1)

            # 线段 B 在线段 A 之后？
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.abs(d0) < np.abs(d1):
                        return a1, b0, np.linalg.norm(a1 - b0)  # type: ignore
                    return a1, b1, np.linalg.norm(a1 - b1)  # type: ignore

        # 线段重叠，返回平行线段的距离
        return None, None, np.linalg.norm(((d0 * _A) + a0) - b0)  # type: ignore

    # 线段相交：计算投影的最短距离点
    t = b0 - a0
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA / denom
    t1 = detB / denom

    pA = a0 + (_A * t0)  # 线段 A 上投影的最短距离点
    pB = b0 + (_B * t1)  # 线段 B 上投影的最短距离点

    # 夹紧投影点
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1

        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1

        # 夹紧投影点 A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B, (pA - b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)

        # 夹紧投影点 B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A, (pB - a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)

    return pA, pB, np.linalg.norm(pA - pB)  # type: ignore


if __name__ == "__main__":
    p1 = np.array([-212.0055, 70.0, -64.0])
    p2 = np.array([-212.0055, -70.0, -64.0])
    p3 = np.array([-212.0055, 70.0, -80.0])
    p4 = np.array([-212.0055, -70.0, -80.0])
    _, _, distance = distanceBetweenTwoSegment(p1, p2, p3, p4)
    print(distance)
# end main
