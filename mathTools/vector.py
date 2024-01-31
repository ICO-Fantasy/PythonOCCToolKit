"""
向量有关计算
Author: ICO
Date: 2023-09-11"""
import numpy as np
import numpy.typing as npt

from geometricTyping import Vector


def angle_between_vectors(vector_1: Vector, vector_2: Vector):
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
    dotProduct = np.dot(vector_1, vector_2)
    normVector1 = np.linalg.norm(vector_1)
    normVector2 = np.linalg.norm(vector_2)

    cosTheta = dotProduct / (normVector1 * normVector2)

    # 使用 arccos 函数计算角度（弧度）
    angle: float = np.arccos(cosTheta)

    return angle


# end def
