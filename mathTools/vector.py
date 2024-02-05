"""
向量有关计算
Author: ICO
Date: 2023-09-11"""

import numpy as np
import numpy.typing as npt

from basicGeometricTyping import Vector


def angle_between_vectors(start_vector: Vector, end_vector: Vector):
    """计算两向量夹角

    Parameters
    ----------
    `vector_1` : Vector
        _description_
    `vector_2` : Vector
        _description_

    Returns
    -------
    float
        两向量夹角，范围在 [0,pi]
    """

    _cos_theta = np.dot(start_vector, end_vector) / (np.linalg.norm(start_vector) * np.linalg.norm(end_vector))
    # 使用 arccos 函数计算角度（弧度）
    angle: float = np.arccos(_cos_theta)

    return angle


# end def
