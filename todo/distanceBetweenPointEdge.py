"""计算点到线段或圆弧间距离
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

from .getEdge import getTwoPoint, getXYZ
from .getPnt import getXYZ

# 创建一个类型别名，用于表示数组
FloatArray = npt.NDArray[np.float_]


class SegmentDistanceCalculator:
    p: FloatArray
    p1: FloatArray
    p2: FloatArray
    p3: FloatArray
    circle_a: TopoDS_Edge
    circle_b: TopoDS_Edge
    circle_center_a: FloatArray
    circle_center_b: FloatArray
    circle_radius_a: float
    circle_radius_b: float

    def __init__(
        self,
        segment_type="line",
    ):
        self.type = segment_type

    def init(self, p, p1, p2=None, p3=None):
        """
        Purpose:
        """
        if not p3:
            if (
                isinstance(p, np.ndarray)
                and isinstance(p1, np.ndarray)
                and isinstance(p2, np.ndarray)
                and isinstance(p3, np.ndarray)
            ):
                self.type = "circle"
                self.p, self.p1, self.p2, self.p3 = p, p1, p2, p3
            elif isinstance(p, gp_Pnt) and isinstance(p1, gp_Pnt) and isinstance(p2, gp_Pnt) and isinstance(p3, gp_Pnt):
                self.p, self.p1, self.p2, self.p3 = (
                    np.array(getXYZ(p)),
                    np.array(getXYZ(p1)),
                    np.array(getXYZ(p2)),
                    np.array(getXYZ(p3)),
                )
            elif isinstance(p, (tuple, list)) and isinstance(p1, (tuple, list)):
                if (
                    isinstance(p[0], np.ndarray)
                    and isinstance(p[1], np.ndarray)
                    and isinstance(p1[0], np.ndarray)
                    and isinstance(p1[1], np.ndarray)
                ):
                    self.p, self.p1, self.p2, self.p3 = p[0], p[1], p1[0], p1[1]
                elif (
                    isinstance(p[0], gp_Pnt)
                    and isinstance(p[1], gp_Pnt)
                    and isinstance(p1[0], gp_Pnt)
                    and isinstance(p1[1], gp_Pnt)
                ):
                    self.p, self.p1, self.p2, self.p3 = (
                        np.array(getXYZ(p[0])),
                        np.array(getXYZ(p[1])),
                        np.array(getXYZ(p1[0])),
                        np.array(getXYZ(p1[1])),
                    )
                else:
                    log.warning("输入错误")
            elif isinstance(p, TopoDS_Edge) and isinstance(p1, TopoDS_Edge):
                brep_edge_a = BRepAdaptor_Curve(p)  # type: ignore
                brep_edge_b = BRepAdaptor_Curve(p1)  # type: ignore
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
                    brep_edge_a.GetType() == GeomAbs_CurveType.GeomAbs_BSplineCurve
                    and brep_edge_b.GetType() == GeomAbs_CurveType.GeomAbs_BSplineCurve
                ):
                    self.type = "circle"
                    # todo 首先要拟合为 circle
                    pass
                else:
                    log.warning("输入错误")
                self.p, self.p1, self.p2, self.p3 = (
                    np.array(getXYZ(getTwoPoint(p)[0])),
                    np.array(getXYZ(getTwoPoint(p)[1])),
                    np.array(getXYZ(getTwoPoint(p1)[0])),
                    np.array(getXYZ(getTwoPoint(p1)[1])),
                )
            else:
                log.warning("输入错误")
            # end if
        else:
            if isinstance(p, np.ndarray) and isinstance(p1, np.ndarray) and isinstance(p2, np.ndarray):
                self.type = "line"
            # end if
            pass
        # end if

    # end def
    def compute(self):
        """
        Purpose:
        """
        if self.type == "line":
            return distanceBetweenTwoSegment(
                self.p,
                self.p1,
                self.p2,
                self.p3,
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
        line_length = np.linalg.norm(self.p1 - self.p)
        vector_circle = self.circle_center_b - self.p
        vector_line_normal = (self.p1 - self.p) / line_length
        projection_vector = vector_circle * vector_line_normal * vector_line_normal
        projection_point = projection_vector + self.p
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
