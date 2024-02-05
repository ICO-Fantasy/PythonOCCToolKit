import numpy as np

from basicGeometricTyping import Point
from mathTools.Inspection import collinear_check

class Arc:
    """
    圆弧由其构成的起点、终点和圆心描述，起点和终点的不同会影响其圆弧角度大小
    旋转轴由起点向量叉乘终点向量得到，旋转遵守右手定则
    """

    def __init__(
        self,
        start_point: Point = np.array(0, 0, 0),
        end_point: Point = np.array(0, 0, 0),
        center: Point = np.array(0, 0, 0),
        is_obtuse=False,
    ):
        self.start_point = start_point
        self.end_point = end_point
        self.center = center
        self.is_obtuse = is_obtuse
        if collinear_check(self.start_point, self.end_point, self.center)