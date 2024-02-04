from enum import Enum

# pyOCC
from OCC.Core.Prs3d import Prs3d_DatumParts
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLUE, Quantity_NOC_GREEN, Quantity_NOC_RED


class AxisDirection(Enum):
    X_AXIS = Prs3d_DatumParts.Prs3d_DatumParts_XAxis
    Y_AXIS = Prs3d_DatumParts.Prs3d_DatumParts_YAxis
    Z_AXIS = Prs3d_DatumParts.Prs3d_DatumParts_ZAxis


class AxisColor(Enum):
    X_AXIS = Quantity_Color(Quantity_NOC_GREEN)
    Y_AXIS = Quantity_Color(Quantity_NOC_BLUE)
    Z_AXIS = Quantity_Color(Quantity_NOC_RED)


class VisualizationCONFIG:
    # 使用枚举类定义坐标轴方向和颜色
    X_AXIS_DIRECTION = AxisDirection.X_AXIS
    Y_AXIS_DIRECTION = AxisDirection.Y_AXIS
    Z_AXIS_DIRECTION = AxisDirection.Z_AXIS
    X_AXIS_COLOR = AxisColor.X_AXIS
    Y_AXIS_COLOR = AxisColor.Y_AXIS
    Z_AXIS_COLOR = AxisColor.Z_AXIS


# if __name__ == "__main__":
#     # 使用配置值
#     X_AXIS_DIRECTION = VisualizationCONFIG.X_AXIS_DIRECTION
#     Y_AXIS_DIRECTION = VisualizationCONFIG.Y_AXIS_DIRECTION
#     Z_AXIS_DIRECTION = VisualizationCONFIG.Z_AXIS_DIRECTION
#     X_AXIS_COLOR = VisualizationCONFIG.X_AXIS_COLOR
#     Y_AXIS_COLOR = VisualizationCONFIG.Y_AXIS_COLOR
#     Z_AXIS_COLOR = VisualizationCONFIG.Z_AXIS_COLOR
# # end main
