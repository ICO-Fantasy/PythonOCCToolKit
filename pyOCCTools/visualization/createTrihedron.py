"""
创建三维坐标系
Author: ICO
Date: 2024-02-04"""

# logger
from typing import Optional

# pyOCC
from OCC.Core.AIS import AIS_Shape, AIS_Trihedron
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf

# local
from .visualizationCONFIG import VisualizationCONFIG

# 使用配置值
X_AXIS_DIRECTION = VisualizationCONFIG.X_AXIS_DIRECTION
Y_AXIS_DIRECTION = VisualizationCONFIG.Y_AXIS_DIRECTION
Z_AXIS_DIRECTION = VisualizationCONFIG.Z_AXIS_DIRECTION
X_AXIS_COLOR = VisualizationCONFIG.X_AXIS_COLOR
Y_AXIS_COLOR = VisualizationCONFIG.Y_AXIS_COLOR
Z_AXIS_COLOR = VisualizationCONFIG.Z_AXIS_COLOR


def bind_trihedron(ais_shape: AIS_Shape):
    ais_trihedron = create_trihedron(ais_shape)
    return ais_trihedron


def create_trihedron(input: Optional[gp_Trsf] = None, arrow_length: int = 200, arrow_width=2.5) -> AIS_Trihedron:
    if not input:
        input = gp_Trsf()
    # 提取平移和旋转部分
    translation_part = input.TranslationPart()
    rotation_part = input.VectorialPart()

    # 创建坐标轴
    origin = gp_Pnt(translation_part.X(), translation_part.Y(), translation_part.Z())
    direction = gp_Dir(rotation_part.Column(3))
    x_direction = gp_Dir(rotation_part.Column(1))
    a_ax2 = gp_Ax2(origin, direction, x_direction)
    a_geom = Geom_Axis2Placement(a_ax2)
    a_trihedron = AIS_Trihedron(a_geom)

    # 设置显示属性
    a_trihedron.SetDrawArrows(True)  # 是否绘制箭头
    a_trihedron.SetSize(arrow_length)  # 设置坐标轴箭头的长度
    # 设置轴线宽
    a_trihedron.Attributes().DatumAspect().LineAspect(X_AXIS_DIRECTION).SetWidth(arrow_width)
    a_trihedron.Attributes().DatumAspect().LineAspect(Y_AXIS_DIRECTION).SetWidth(arrow_width)
    a_trihedron.Attributes().DatumAspect().LineAspect(Z_AXIS_DIRECTION).SetWidth(arrow_width)
    # 设置轴颜色
    a_trihedron.SetDatumPartColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetDatumPartColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetDatumPartColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)
    # 设置箭头颜色
    a_trihedron.SetArrowColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetArrowColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetArrowColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)
    # 设置文本颜色
    a_trihedron.SetTextColor(X_AXIS_DIRECTION, X_AXIS_COLOR)
    a_trihedron.SetTextColor(Y_AXIS_DIRECTION, Y_AXIS_COLOR)
    a_trihedron.SetTextColor(Z_AXIS_DIRECTION, Z_AXIS_COLOR)

    return a_trihedron
