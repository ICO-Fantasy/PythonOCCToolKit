"""计算两线段或圆弧间距离
Author: ICO
Date: 2023-09-11"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import logging
from typing import Callable, Union

log = logging.getLogger(__name__)

import numpy as np
import numpy.typing as npt
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_CurveType
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Edge

from mathTools import distanceBetweenTwoSegment

from .getEdge import getTwoPoint
from .getPnt import getXYZ

# 创建一个类型别名，用于表示数组
FloatArray = npt.NDArray[np.float_]


class SegmentDistanceCalculator:
    a0: FloatArray
    a1: FloatArray
    b0: FloatArray
    b1: FloatArray
    circle_a: TopoDS_Edge
    circle_b: TopoDS_Edge
    circle_center_a: FloatArray
    circle_center_b: FloatArray
    circle_radius_a: float
    circle_radius_b: float

    def __init__(
        self,
        segment_type="line",
        clampAll: bool = True,
        clampA0: bool = False,
        clampA1: bool = False,
        clampB0: bool = False,
        clampB1: bool = False,
    ):
        self.type = segment_type
        self.clampAll = clampAll
        self.clampA0 = clampA0
        self.clampA1 = clampA1
        self.clampB0 = clampB0
        self.clampB1 = clampB1

    def init(self, a0, a1, b0=None, b1=None):
        """
        Purpose:
        """
        if (
            isinstance(a0, np.ndarray)
            and isinstance(a1, np.ndarray)
            and isinstance(b0, np.ndarray)
            and isinstance(b1, np.ndarray)
        ):
            self.a0, self.a1, self.b0, self.b1 = a0, a1, b0, b1
        elif isinstance(a0, gp_Pnt) and isinstance(a1, gp_Pnt) and isinstance(b0, gp_Pnt) and isinstance(b1, gp_Pnt):
            self.a0, self.a1, self.b0, self.b1 = (
                np.array(getXYZ(a0)),
                np.array(getXYZ(a1)),
                np.array(getXYZ(b0)),
                np.array(getXYZ(b1)),
            )
        elif isinstance(a0, (tuple, list)) and isinstance(a1, (tuple, list)):
            if (
                isinstance(a0[0], np.ndarray)
                and isinstance(a0[1], np.ndarray)
                and isinstance(a1[0], np.ndarray)
                and isinstance(a1[1], np.ndarray)
            ):
                self.a0, self.a1, self.b0, self.b1 = a0[0], a0[1], a1[0], a1[1]
            elif (
                isinstance(a0[0], gp_Pnt)
                and isinstance(a0[1], gp_Pnt)
                and isinstance(a1[0], gp_Pnt)
                and isinstance(a1[1], gp_Pnt)
            ):
                self.a0, self.a1, self.b0, self.b1 = (
                    np.array(getXYZ(a0[0])),
                    np.array(getXYZ(a0[1])),
                    np.array(getXYZ(a1[0])),
                    np.array(getXYZ(a1[1])),
                )
            else:
                log.warning("输入错误")
        elif isinstance(a0, TopoDS_Edge) and isinstance(a1, TopoDS_Edge):
            brep_edge_a = BRepAdaptor_Curve(a0)  # type: ignore
            brep_edge_b = BRepAdaptor_Curve(a1)  # type: ignore
            # 曲线类型
            if (
                brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_Line
                and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_Line
            ):
                self.type = "line"
            elif (
                brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_Circle
                and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_Circle
            ):
                self.type = "circle"
                self.circle_center_a = np.array(getXYZ(brep_edge_a.Circle().Location()))
                self.circle_center_b = np.array(getXYZ(brep_edge_a.Circle().Location()))
                self.circle_radius_a = brep_edge_a.Circle().Radius()
                self.circle_radius_b = brep_edge_a.Circle().Radius()
            elif (
                brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_Line
                and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_Circle
            ):
                self.type = "line&circle"
                # 默认 a 为 line, b 为 circle
                self.circle_center_b = np.array(getXYZ(brep_edge_b.Circle().Location()))
                self.circle_radius_b = brep_edge_b.Circle().Radius()
            elif (
                brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_Circle
                and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_Line
            ):
                brep_edge_a, brep_edge_b = brep_edge_b, brep_edge_a
                a0, a1 = a1, a0
                self.type = "line&circle"
                # 默认 a 为 line, b 为 circle
                self.circle_center_b = np.array(getXYZ(brep_edge_b.Circle().Location()))
                self.circle_radius_b = brep_edge_b.Circle().Radius()
            elif (
                brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_BSplineCurve
                and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_BSplineCurve
            ):
                self.type = "circle"
                # todo 首先要拟合为 circle
                pass
            else:
                log.warning("输入错误")
            self.a0, self.a1, self.b0, self.b1 = (
                np.array(getXYZ(getTwoPoint(a0)[0])),
                np.array(getXYZ(getTwoPoint(a0)[1])),
                np.array(getXYZ(getTwoPoint(a1)[0])),
                np.array(getXYZ(getTwoPoint(a1)[1])),
            )
        else:
            log.warning("输入错误")
        # end if

    # end def
    def compute(self):
        """
        Purpose:
        """
        if self.type == "line":
            return distanceBetweenTwoSegment(
                self.a0,
                self.a1,
                self.b0,
                self.b1,
                self.clampAll,
                self.clampA0,
                self.clampA1,
                self.clampB0,
                self.clampB1,
            )
        if self.type == "circle":
            return self.distanceBetweenTwoCircle()
        if self.type == "line&circle":
            return self.distanceBetweenLineCircle()
        else:
            log.warning("未知线型")
            raise TypeError("未知线型")

    # end def

    # end def
    def distanceBetweenTwoCircle(self) -> tuple[FloatArray, FloatArray, np.float_]:
        center_distance = np.linalg.norm(self.circle_center_a - self.circle_center_b)
        if center_distance >= self.circle_radius_a + self.circle_radius_b:
            # todo 算圆弧间距离或者端点到圆弧距离
            if True:
                # 计算单位向量
                vector_a = self.circle_radius_a * (self.circle_center_b - self.circle_center_a) / center_distance
                vector_b = self.circle_radius_b * (self.circle_center_a - self.circle_center_b) / center_distance
                # 得到两个交点
                point_a = self.circle_center_a + vector_a
                point_b = self.circle_center_b + vector_b
                return point_a, point_b, np.linalg.norm(point_a - point_b)  # 得到直线距离

        else:
            log.info("距离小于两圆半径之和")
            raise ValueError("距离小于两圆半径之和")

    def distanceBetweenLineCircle(self) -> tuple[FloatArray, FloatArray, np.float_]:
        line_length = np.linalg.norm(self.a1 - self.a0)
        vector_circle = self.circle_center_b - self.a0
        vector_line_normal = (self.a1 - self.a0) / line_length
        projection_vector = vector_circle * vector_line_normal * vector_line_normal
        projection_point = projection_vector + self.a0
        # 计算投影点到圆弧的距离
        distance = np.linalg.norm(self.circle_center_b - projection_point) - self.circle_radius_b
        arc_point = (
            distance * (self.circle_center_b - projection_point) / np.linalg.norm(self.circle_center_b - projection_point)
            + projection_point
        )
        return projection_point, arc_point, abs(distance)

    # end def


# end class
if __name__ == "__main__":
    p1 = gp_Pnt(-212.0055, 70.0, -64.0)
    p2 = gp_Pnt(-212.0055, -70.0, -64.0)
    p3 = gp_Pnt(-212.0055, 70.0, -80.0)
    p4 = gp_Pnt(-212.0055, -70.0, -80.0)
    # p1 = np.array([-212.0055, 70.0, -64.0])
    # p2 = np.array([-212.0055, -70.0, -64.0])
    # p3 = np.array([-212.0055, 70.0, -80.0])
    # p4 = np.array([-212.0055, -70.0, -80.0])
    cal = SegmentDistanceCalculator()
    cal.init(p1, p2, p3, p4)
    edge_a_pnt, edge_b_pnt, distance = cal.compute()
    print(distance)
# end main
