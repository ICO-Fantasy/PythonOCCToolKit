from OCC.Core.Prs3d import Prs3d_DatumParts
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLUE, Quantity_NOC_GREEN, Quantity_NOC_RED


class VisualizationCONFIG:
    # 定义坐标轴方向和颜色
    X_AXIS_DIRECTION = Prs3d_DatumParts.Prs3d_DatumParts_XAxis
    Y_AXIS_DIRECTION = Prs3d_DatumParts.Prs3d_DatumParts_YAxis
    Z_AXIS_DIRECTION = Prs3d_DatumParts.Prs3d_DatumParts_ZAxis
    X_AXIS_COLOR = Quantity_Color(Quantity_NOC_GREEN)
    Y_AXIS_COLOR = Quantity_Color(Quantity_NOC_BLUE)
    Z_AXIS_COLOR = Quantity_Color(Quantity_NOC_RED)


if __name__ == "__main__":
    # 使用配置值
    X_AXIS_DIRECTION = VisualizationCONFIG.X_AXIS_DIRECTION
    Y_AXIS_DIRECTION = VisualizationCONFIG.Y_AXIS_DIRECTION
    Z_AXIS_DIRECTION = VisualizationCONFIG.Z_AXIS_DIRECTION
    X_AXIS_COLOR = VisualizationCONFIG.X_AXIS_COLOR
    Y_AXIS_COLOR = VisualizationCONFIG.Y_AXIS_COLOR
    Z_AXIS_COLOR = VisualizationCONFIG.Z_AXIS_COLOR
# end main
