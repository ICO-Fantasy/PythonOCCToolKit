from typing import Annotated, Literal

import numpy as npt
from numpy.typing import ArrayLike, NDArray

"""
向量
通常描述为[x,y,z]
齐次空间描述为[x,y,z,w],其中w为向量的长度"""
Vector = Annotated[NDArray[npt.float_], Literal[3,]]
"""
点
通常描述为[x,y,z]
齐次空间描述为[x,y,z,0]
"""
Point = Annotated[NDArray[npt.float_], Literal[3,]]
"""
平移
T=[x,y,z]
"""
# 平移采用向量描述
"""
旋转
R=
|x y z|
|x y z|
|x y z|
"""
# 旋转采用四元数描述
"""
齐次变换
|R T|
|0 1|
"""
# 齐次变换采用4*4的齐次变换矩阵描述
