"""
判断 topo 的相对关系
Author: ICO
Date: 2023-09-11
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import numpy as np
from OCC.Core.BRep import BRep_Tool, BRep_Tool_CurveOnSurface, BRep_Tool_Surface
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeVertex
from OCC.Core.BRepClass3d import BRepClass3d_SolidClassifier
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.Geom import Geom_Surface
from OCC.Core.GeomAbs import GeomAbs_CurveType
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.gp import gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.IntTools import IntTools_Context, IntTools_EdgeEdge
from OCC.Core.TopAbs import TopAbs_State, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Face, TopoDS_Shape

from . import get_two_points, getXYZ


def pointOnFace(pnt: gp_Pnt, face: TopoDS_Face, tol=1e-2):
    """判断点是否在平面所在的面上"""
    # 使用 ProjLib_ProjectOnPlane 进行投影

    """判断点在 TopoDS_Face 内部"""
    vertex = BRepBuilderAPI_MakeVertex(pnt).Vertex()
    anExtrema = BRepExtrema_DistShapeShape(face, vertex)
    # print(anExtrema.Value())
    if (anExtrema.IsDone() == True) & (anExtrema.Value() <= tol):
        classifier = BRepClass3d_SolidClassifier(face, pnt, tol)
        # return classifier.IsOnAFace() # 等价于 TopAbs_State.TopAbs_ON
        if classifier.State() == TopAbs_State.TopAbs_ON:
            # print("在面上")
            return True
        elif classifier.State() == TopAbs_State.TopAbs_IN:
            # print("在实体内部")
            return False
        else:
            return False
        # end if
    # end if
    return False


# end def
def edgeOnFace(edge: TopoDS_Edge, face: TopoDS_Face, tol=1e-2, two_point=False):
    """
    判断面是否在平面所在的面上 (默认认为 edge 是直线)
    """
    start_point, end_point = get_two_points(edge)
    start_bool = pointOnFace(start_point, face, tol)
    if two_point:
        return start_bool and pointOnFace(end_point, face, tol)
    else:
        return start_bool
    # end if


# end def
def twoParallelLine(line1, line2, tol=1e-6):
    """检查两直线是否平行"""
    match (line1, line2):
        case (tuple(gp_Pnt()), tuple(gp_Pnt())):
            point1, point2 = line1
            point3, point4 = line2
        case (TopoDS_Edge(), TopoDS_Edge()):
            point1, point2 = getEdgePoint(line1)  # type: ignore
            point3, point4 = getEdgePoint(line2)  # type: ignore
        case (TopoDS_Shape(), TopoDS_Shape()):
            point1, point2 = getEdgePoint(line1)  # type: ignore
            point3, point4 = getEdgePoint(line2)  # type: ignore
        case _:
            print(f"twoParallelLine 输入错误 (无法识别的输入类型) line1: {type(line1)}, line2:{type(line1)}")
            return False
    dir1 = gp_Dir(gp_Vec(point1, point2))
    dir2 = gp_Dir(gp_Vec(point3, point4))
    return dir1.IsParallel(dir2, tol)


# end def
def getEdgePoint(edge: TopoDS_Edge | TopoDS_Shape):
    """获取 `TopoDS_Edge` 两个端点"""
    # 创建一个顶点资源
    vertex_tool = BRep_Tool()
    # 获取顶点资源
    explorer = TopExp_Explorer(edge, TopAbs_VERTEX)
    # 获取第一个端点
    first_vertex = explorer.Current()
    first_point = vertex_tool.Pnt(first_vertex)  # type: ignore
    # 继续遍历获取第二个端点
    explorer.Next()
    second_vertex = explorer.Current()
    second_point = vertex_tool.Pnt(second_vertex)  # type: ignore

    return first_point, second_point


# end def
def pointOnLineSegment(line: tuple[gp_Pnt, gp_Pnt], point: list[float], tolerance=1e-6):
    """判断点是否在线段上"""
    a, b = line
    startPoint, endPoint = getXYZ(a), getXYZ(b)
    v1 = np.array(startPoint) - np.array(point)
    v2 = np.array(endPoint) - np.array(point)
    normV1 = np.linalg.norm(v1, 2)
    normV2 = np.linalg.norm(v2, 2)
    EPS = 1.0e-8
    if normV1 < tolerance or normV2 < tolerance:
        return True
    else:
        cosTheta = np.dot(v1, v2) / (normV1 * normV2)
        if abs(cosTheta + 1.0) < EPS:
            return True
    return False


# end def
def twoEdgeIntersection(line1: tuple[gp_Pnt, gp_Pnt], line2: tuple[gp_Pnt, gp_Pnt], tolerance=1e-6) -> bool:
    """检测两直线是否相交"""
    if isinstance(line1, tuple) and isinstance(line2, tuple):
        a, b = line1
        c, d = line2
    else:
        raise KeyError("输入参数的格式不正确")
    # end if
    startPointAB, endPointAB = getXYZ(a), getXYZ(b)
    startPointCD, endPointCD = getXYZ(c), getXYZ(d)
    a11 = endPointAB[0] - startPointAB[0]
    a12 = startPointCD[0] - endPointCD[0]
    b1 = startPointCD[0] - startPointAB[0]

    a21 = endPointAB[1] - startPointAB[1]
    a22 = startPointCD[1] - endPointCD[1]
    b2 = startPointCD[1] - startPointAB[1]

    a31 = endPointAB[2] - startPointAB[2]
    a32 = startPointCD[2] - endPointCD[2]
    b3 = startPointCD[2] - startPointAB[2]

    A11 = a11**2 + a21**2 + a31**2
    A12 = a11 * a12 + a21 * a22 + a31 * a32
    A21 = A12
    A22 = a12**2 + a22**2 + a32**2
    B1 = a11 * b1 + a21 * b2 + a31 * b3
    B2 = a12 * b1 + a22 * b2 + a32 * b3

    EPS = 1.0e-10
    temp = A11 * A22 - A12 * A21
    if abs(temp) < EPS:
        if (
            pointOnLineSegment(line1, startPointCD, tolerance)
            or pointOnLineSegment(line1, endPointCD, tolerance)
            or pointOnLineSegment(line2, startPointAB, tolerance)
            or pointOnLineSegment(line2, endPointAB, tolerance)
        ):
            return True
    else:
        t = [-(A12 * B2 - A22 * B1) / temp, (A11 * B2 - A21 * B1) / temp]
        if (t[0] >= 0 - EPS and t[0] <= 1.0 + EPS) and (t[1] >= 0 - EPS and t[1] <= 1.0 + EPS):
            if (
                abs(
                    (startPointAB[0] + (endPointAB[0] - startPointAB[0]) * t[0])
                    - (startPointCD[0] + (endPointCD[0] - startPointCD[0]) * t[1])
                )
                < tolerance
                and abs(
                    (startPointAB[1] + (endPointAB[1] - startPointAB[1]) * t[0])
                    - (startPointCD[1] + (endPointCD[1] - startPointCD[1]) * t[1])
                )
                < tolerance
                and abs(
                    (startPointAB[2] + (endPointAB[2] - startPointAB[2]) * t[0])
                    - (startPointCD[2] + (endPointCD[2] - startPointCD[2]) * t[1])
                )
                < tolerance
            ):
                return True
    return False


# end def
def getTwoEdgeIntersection(line1: tuple[gp_Pnt, gp_Pnt], line2: tuple[gp_Pnt, gp_Pnt], tolerance=1e-6):
    """
    获取两相交直线的交点
    """
    if isinstance(line1, tuple) and isinstance(line2, tuple):
        a, b = line1
        c, d = line2
    else:
        raise KeyError("输入参数的格式不正确")
    # end if
    startPointAB, endPointAB = getXYZ(a), getXYZ(b)
    startPointCD, endPointCD = getXYZ(c), getXYZ(d)
    d1 = np.array(endPointAB) - np.array(startPointAB)
    d2 = np.array(endPointCD) - np.array(startPointCD)

    cross = np.cross(d1, d2)

    if np.linalg.norm(cross) < tolerance:
        return None  # 直线平行或共线，没有交点

    v = np.array(startPointCD) - np.array(startPointAB)
    t = np.dot(v, cross) / np.dot(cross, cross)

    # if not (0 <= t <= 1):
    #     return None  # 交点不在线段 AB 上

    intersection_point = np.array(startPointAB) + t * d1
    return gp_Pnt(intersection_point[0], intersection_point[1], intersection_point[2])


# end def
def minDistanceBetweenPointLine(point: gp_Pnt, line_segment: TopoDS_Edge | TopoDS_Shape):
    """计算点和线段或圆弧 (默认为整圆) 的最短距离"""
    brep_edge = BRepAdaptor_Curve(topo_edge)  # type: ignore
    edge_type = brep_edge.GetType()
    match edge_type:
        case GeomAbs_CurveType.GeomAbs_Line:
            # 将 line_segment 包装成 Geom_Curve
            curve, _, _ = BRep_Tool.Curve(line_segment)  # type: ignore
            # 使用 GeomAPI_ProjectPointOnCurve 计算点到线段的最短距离
            projector = GeomAPI_ProjectPointOnCurve(point, curve)
            # 获取投影点
            projected_point = projector.NearestPoint()
            # 计算点到线段的最短距离
            return point.Distance(projected_point)
        case GeomAbs_CurveType.GeomAbs_Circle:
            circle = brep_edge.Circle()
            # 获取圆心坐标
            circle_center = circle.Location()
            # 获取圆半径
            circle_radius = circle.Radius()
            return point.Distance(circle_center) - circle_radius
        case GeomAbs_CurveType.GeomAbs_BSplineCurve:
            # todo 需要首先将样条曲线拟合为圆弧
            pass
        case GeomAbs_CurveType.GeomAbs_BezierCurve:
            # todo 需要首先将贝塞尔曲线拟合为圆弧
            pass
        case (_):
            print("未知的曲线类型")
    # end match


# end def
if __name__ == "__main__":
    from OCC.Core.AIS import AIS_Shape
    from SimpleGui import initDisplay

    from dataExchange.toQuantityColor import to_Quantity_Color
    from pyOCCTools.geometric.makeFace import make_face_from_points

    display, start_display, add_menu, add_function_to_menu = initDisplay()
    apnt = gp_Pnt(10, 10, 0)
    p1 = gp_Pnt(-212.0055, 70.0, -64.0)
    p2 = gp_Pnt(-212.0055, -70.0, -64.0)
    p3 = gp_Pnt(-212.0055, 70.0, -80.0)
    p4 = gp_Pnt(-212.0055, -70.0, -80.0)
    p5 = gp_Pnt(-194.3834, 70.0, -64.0)
    p6 = gp_Pnt(-194.3834, -70.0, -64.0)
    p7 = gp_Pnt(-194.3834, 70.0, -80.0)
    p8 = gp_Pnt(-194.3834, -70.0, -80.0)
    pp1 = p1
    pp2 = p6
    pp3 = p2
    pp4 = p5
    w1 = BRepBuilderAPI_MakeEdge(pp1, pp2).Shape()
    print(minDistanceBetweenPointLine(apnt, w1))
    # w2 = BRepBuilderAPI_MakeEdge(pp3, pp4).Shape()
    # display.Context.Display(AIS_Shape(w1), True)
    # display.Context.Display(AIS_Shape(w2), True)
    # aface = makeFaceFromPoint(p1, p2, p4, p3)
    # display.Context.Display(AIS_Shape(aface), True)
    # print(pointOnFace(p6, aface))
    # bbbb = twoEdgeIntersection((pp1, pp2), (pp3, pp4))
    # print(bbbb)
    start_display()
# end main
