"""
从 python 字符串转换到 TCollection 类型字符
(在后续的 pyOCC 版本中可能会删除)
Author: ICO
Date: 2024-02-04"""

# logger
from loguru import logger
from OCC.Core.AIS import AIS_ViewCube

# pyOCC
from OCC.Core.TCollection import TCollection_AsciiString, TCollection_ExtendedString


def create_view_cube():
    a_view_cube = AIS_ViewCube()  # 视图立方体
    # 设置坐标轴半径
    axis_size = 6
    a_view_cube.SetAxesRadius(axis_size)
    a_view_cube.SetAxesConeRadius(axis_size * 1.5)
    a_view_cube.SetAxesSphereRadius(axis_size * 1.5)
    # 修改坐标轴文字颜色
    aDrawer = a_view_cube.Attributes()
    aDrawer.SetDatumAspect(Prs3d_DatumAspect())  # 动态设置
    aDatumAsp = aDrawer.DatumAspect()  # 获取 Prs3d_DatumAspect 对象指针
    aDatumAsp.TextAspect(X_AXIS_DIRECTION).SetColor(X_AXIS_COLOR)
    aDatumAsp.TextAspect(Y_AXIS_DIRECTION).SetColor(Y_AXIS_COLOR)
    aDatumAsp.TextAspect(Z_AXIS_DIRECTION).SetColor(Z_AXIS_COLOR)
    aDatumAsp.TextAspect(X_AXIS_DIRECTION).SetHeight(axis_size * 5)
    aDatumAsp.TextAspect(Y_AXIS_DIRECTION).SetHeight(axis_size * 5)
    aDatumAsp.TextAspect(Z_AXIS_DIRECTION).SetHeight(axis_size * 5)
    # 修改坐标轴颜色
    aDatumAsp.ShadingAspect(X_AXIS_DIRECTION).SetColor(X_AXIS_COLOR)
    aDatumAsp.ShadingAspect(Y_AXIS_DIRECTION).SetColor(Y_AXIS_COLOR)
    aDatumAsp.ShadingAspect(Z_AXIS_DIRECTION).SetColor(Z_AXIS_COLOR)
    # 设置描边和描边颜色
    aDrawer.SetFaceBoundaryDraw(True)
    aDrawer.SetFaceBoundaryAspect(Prs3d_LineAspect(Graphic3d_AspectLine3d()))
    aDrawer.FaceBoundaryAspect().SetColor(getColor(228, 144, 255))
    # 设置立方体标签
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Xneg, "左")
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Xpos, "右")
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Yneg, "前")
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Ypos, "后")
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Zpos, "上")
    a_view_cube.SetBoxSideLabel(V3d_TypeOfOrientation.V3d_Zneg, "下")
    a_view_cube.SetFont("SimSun")
    a_view_cube.SetFontHeight(50)
    a_view_cube.SetTextColor(getColor(241, 217, 37))
    # 设置立方体面颜色
    a_view_cube.SetBoxColor(getColor(0, 194, 168))
    # 设置半透明立方体
    a_view_cube.SetTransparency(0.6)
    # 设置立方体面到边的距离
    a_view_cube.SetBoxFacetExtension(14)

    # 设置轴标签
    # a_view_cube.SetAxesLabels("x","y","Z")
    # 设置盒子圆角
    # a_view_cube.SetRoundRadius(0.1)
    # 设置立方体面到边间空隙的可选择范围
    # a_view_cube.SetBoxEdgeGap(0)


# end def
