import os
import sys
from typing import Union

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from OCC.Core.AIS import AIS_ConnectedInteractive, AIS_MultipleConnectedInteractive, AIS_Shape, AIS_Trihedron
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.gp import *
from OCC.Core.Prs3d import *
from OCC.Core.Quantity import *
from OCC.Core.TopLoc import TopLoc_Location

from . import VisualizationCONFIG, getColor

# 使用配置值
X_AXIS_DIRECTION = VisualizationCONFIG.X_AXIS_DIRECTION
Y_AXIS_DIRECTION = VisualizationCONFIG.Y_AXIS_DIRECTION
Z_AXIS_DIRECTION = VisualizationCONFIG.Z_AXIS_DIRECTION
X_AXIS_COLOR = VisualizationCONFIG.X_AXIS_COLOR
Y_AXIS_COLOR = VisualizationCONFIG.Y_AXIS_COLOR
Z_AXIS_COLOR = VisualizationCONFIG.Z_AXIS_COLOR


def bindTrihedron(ais_shape: AIS_Shape) -> tuple[AIS_Shape, AIS_Trihedron]:
    # ais_shape_trihedron = AIS_ConnectedInteractive()
    ais_trihedron = createTrihedron(ais_shape)
    # ais_shape_trihedron.Connect(ais_trihedron)
    # ais_shape_trihedron.Connect(ais_shape)
    # ais_shape_trihedron = ais_shape_trihedron.ConnectedTo()
    # ais_shape_trihedron = ais_shape_trihedron.Connect(ais_shape)
    return ais_shape, ais_trihedron


# def createTrihedron(input=None, size=200):
#     XAxis = X_AXIS_DIRECTION
#     YAxis = Y_AXIS_DIRECTION
#     ZAxis = Z_AXIS_DIRECTION
#     X_AXIS_COLOR = getColor(0, 255, 0)
#     Y_AXIS_COLOR = getColor(0, 0, 255)
#     Z_AXIS_COLOR = getColor(255, 0, 0)
#     if isinstance(input, AIS_Shape):
#         a_location = input.Shape().Location()
#         a_trsf = a_location.Transformation()
#         translation_part = a_trsf.TranslationPart()
#         rotation_part = a_trsf.VectorialPart()
#         origin = gp_Pnt(translation_part.X(), translation_part.Y(), translation_part.Z())
#         direction = gp_Dir(rotation_part.Column(3))
#         a_ax2 = gp_Ax2(origin, direction)
#         a_geom = Geom_Axis2Placement(a_ax2)
#         a_trihedron = AIS_Trihedron(a_geom)
#     elif isinstance(input, TopLoc_Location):
#         a_trsf = input.Transformation()
#         translation_part = a_trsf.TranslationPart()
#         rotation_part = a_trsf.VectorialPart()
#         origin = gp_Pnt(translation_part.X(), translation_part.Y(), translation_part.Z())
#         direction = gp_Dir(rotation_part.Column(3))
#         a_ax2 = gp_Ax2(origin, direction)
#         a_geom = Geom_Axis2Placement(a_ax2)
#         a_trihedron = AIS_Trihedron(a_geom)
#     else:
#         a_ax2 = gp_Ax2()
#         a_geom = Geom_Axis2Placement(a_ax2)
#         a_trihedron = AIS_Trihedron(a_geom)
#     a_trihedron.SetDrawArrows(True)
#     a_trihedron.SetSize(size)
#     a_trihedron.Attributes().DatumAspect().LineAspect(Prs3d_DP_XAxis).SetWidth(2.5)
#     a_trihedron.Attributes().DatumAspect().LineAspect(Prs3d_DP_YAxis).SetWidth(2.5)
#     a_trihedron.Attributes().DatumAspect().LineAspect(Prs3d_DP_ZAxis).SetWidth(2.5)
#     a_trihedron.SetDatumPartColor(XAxis, X_AXIS_COLOR)
#     a_trihedron.SetDatumPartColor(YAxis, Y_AXIS_COLOR)
#     a_trihedron.SetDatumPartColor(ZAxis, Z_AXIS_COLOR)
#     a_trihedron.SetArrowColor(XAxis, X_AXIS_COLOR)
#     a_trihedron.SetArrowColor(YAxis, Y_AXIS_COLOR)
#     a_trihedron.SetArrowColor(ZAxis, Z_AXIS_COLOR)
#     a_trihedron.SetTextColor(XAxis, X_AXIS_COLOR)
#     a_trihedron.SetTextColor(YAxis, Y_AXIS_COLOR)
#     a_trihedron.SetTextColor(ZAxis, Z_AXIS_COLOR)
#     return a_trihedron


def createTrihedron(
    input: Union[AIS_Shape, TopLoc_Location, gp_Trsf, None] = None, arrow_length: int = 200, arrow_width=2.5
) -> AIS_Trihedron:
    # 根据输入类型进行处理
    match input:
        case AIS_Shape():
            a_trsf = input.LocalTransformation()
        case TopLoc_Location():
            a_trsf = input.Transformation()
        case gp_Trsf():
            a_trsf = input
        case _:
            a_trsf = gp_Trsf()

    # 提取平移和旋转部分
    translation_part = a_trsf.TranslationPart()
    rotation_part = a_trsf.VectorialPart()

    # 创建坐标轴
    origin = gp_Pnt(translation_part.X(), translation_part.Y(), translation_part.Z())
    direction = gp_Dir(rotation_part.Column(3))
    y_direction = gp_Dir(rotation_part.Column(1))
    a_ax2 = gp_Ax2(origin, direction, y_direction)
    a_geom = Geom_Axis2Placement(a_ax2)
    a_trihedron = AIS_Trihedron(a_geom)

    # 设置显示属性
    a_trihedron.SetDrawArrows(True)
    a_trihedron.SetSize(arrow_length)
    a_trihedron.Attributes().DatumAspect().LineAspect(X_AXIS_DIRECTION).SetWidth(arrow_width)
    a_trihedron.Attributes().DatumAspect().LineAspect(Y_AXIS_DIRECTION).SetWidth(arrow_width)
    a_trihedron.Attributes().DatumAspect().LineAspect(Z_AXIS_DIRECTION).SetWidth(arrow_width)
    a_trihedron.SetDatumPartColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetDatumPartColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetDatumPartColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)
    a_trihedron.SetArrowColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetArrowColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetArrowColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)
    a_trihedron.SetTextColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetTextColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetTextColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)

    return a_trihedron
