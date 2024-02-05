"""
gp_Trsf 的数据交换
Author: ICO
Date: 2024-02-04"""

import json

import numpy as np

# logger
from loguru import logger

# pyOCC
from OCC.Core.gp import gp_Dir, gp_Trsf

# local
from basicGeometricTyping import Quaternion, TransformMatrix_4x4, Vector

from .Quaternion import gp_Quaternion_as_quat
from .XYZ import from_gp_XYZ


def gp_Trsf_as_transform_matrix(trsf: gp_Trsf) -> TransformMatrix_4x4:
    transform = np.matrix(
        [
            [trsf.Value(1, 1), trsf.Value(1, 2), trsf.Value(1, 3), trsf.Value(1, 4)],
            [trsf.Value(2, 1), trsf.Value(2, 2), trsf.Value(2, 3), trsf.Value(2, 4)],
            [trsf.Value(3, 1), trsf.Value(3, 2), trsf.Value(3, 3), trsf.Value(3, 4)],
            [0, 0, 0, 1],
        ]
    )
    return transform


# end def
def gp_Trsf_as_vec_quat(trsf: gp_Trsf) -> tuple[Vector, Quaternion]:
    """从 gp_Trsf 中获取平移变换和旋转四元数

    Parameters
    ----------
    `trsf` : gp_Trsf

    Returns
    -------
    tuple[Vector, Quaternion]
        平移变换和旋转四元数
    """
    return from_gp_XYZ(trsf.TranslationPart()), gp_Quaternion_as_quat(trsf.GetRotation())


def gp_Trsf_as_vectors(trsf: gp_Trsf) -> tuple[Vector, Vector, Vector, Vector]:
    """从 gp_Trsf 中获取平移变换和三个方向向量

    Parameters
    ----------
    `trsf` : gp_Trsf

    Returns
    -------
    tuple[Vector, Vector, Vector, Vector]
        平移变换，x 方向向量，y 方向向量，z 方向向量
    """
    rotation_matrix = trsf.VectorialPart()
    return (
        from_gp_XYZ(trsf.TranslationPart()),
        from_gp_XYZ(rotation_matrix.Column(1)),
        from_gp_XYZ(rotation_matrix.Column(2)),
        from_gp_XYZ(rotation_matrix.Column(3)),
    )


def trsf_as_json(trsf: gp_Trsf):
    """
    把 gp_Trsf 转为 json 格式

    Parameters
    ----------
    `trsf` : gp_Trsf

    Return
    ------
    `Location`: [x,y,z], `Matrix`: r_matrix(3*3), `shape`: float, `scale`: float
    """
    location = [trsf.Value(1, 4), trsf.Value(2, 4), trsf.Value(3, 4)]
    r_matrix = [
        trsf.Value(1, 1),
        trsf.Value(1, 2),
        trsf.Value(1, 3),
        trsf.Value(2, 1),
        trsf.Value(2, 2),
        trsf.Value(2, 3),
        trsf.Value(3, 1),
        trsf.Value(3, 2),
        trsf.Value(3, 3),
    ]
    shape = trsf.Form()  # 矩阵形状（变换的类型）
    scale = trsf.ScaleFactor()  # 缩放
    data = {"Location": location, "Matrix": r_matrix, "shape": shape, "scale": scale}
    return json.dumps(data)
