"""
圆弧有关计算
Author: ICO
Date: 2023-09-11"""
import numpy as np
import numpy.typing as npt

from geometricTyping import Vector

from ..mathTools.vector import angle_between_vectors


# todo 方法不完善
def angle_of_arcs(
    center: npt.NDArray[np.float64],
    p1: npt.NDArray[np.float64],
    p2: npt.NDArray[np.float64],
    p3: npt.NDArray[np.float64],
):
    """计算圆弧的角度

    Parameters
    ----------
    `center` : npt.NDArray[np.float64]
        _description_
    `p1` : npt.NDArray[np.float64]
        _description_
    `p2` : npt.NDArray[np.float64]
        _description_
    `p3` : npt.NDArray[np.float64]
        _description_

    Returns
    -------
    float
        _description_
    """
    vector1 = p1 - center
    vector2 = p2 - center
    vector3 = p3 - center

    angle1 = angle_between_vectors(vector1, vector2)
    angle2 = angle_between_vectors(vector2, vector3)
    angle = angle2 + angle1
    # 确保角度在 90 到 180 度之间
    if angle < np.pi:
        angle = np.pi - angle

    return angle
