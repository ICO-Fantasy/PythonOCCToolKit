"""
常用几何的类型提示
Author: ICO
Date: 2024-01-01
"""

from enum import Enum
from typing import Annotated, Literal

import numpy as npt
from numpy.typing import ArrayLike, NDArray

Vector = Annotated[NDArray[npt.float_], Literal[3,]]
"""
向量
通常描述为 [x,y,z],
齐次空间描述为 [x,y,z,w], 其中 w 为向量的长度
"""
Point = Annotated[NDArray[npt.float_], Literal[3,]]
"""
点
通常描述为 [x,y,z],
齐次空间描述为 [x,y,z,0]
"""
# 平移采用向量描述
"""
平移
T=[x,y,z]
"""
# 旋转采用四元数描述
Quaternion = Annotated[NDArray[npt.float_], Literal[4,]]
"""
旋转\n
|x y z|\n
|x y z|  = [x,y,z,w] \n
|x y z|
"""
# 关于欧拉角描述的旋转顺序
"""
内旋 (intrinsic rotations) = 旋转轴 (rotated axis)
外旋 (extrinsic rotations) = 固定轴 (static/fixed axis)
规定内旋表示为：rxyz
规定外旋表示为：sxyz
"""
# 齐次变换采用 4*4 的齐次变换矩阵描述
TransformMatrix_4x4 = Annotated[NDArray[npt.float_], Literal[4, 4]]
"""
齐次变换\n
|R T|\n
|0 1|
"""
