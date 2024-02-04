"""
QT & OCC 三维显示窗口
"""

from loguru import logger

# local
from myViewer3d import myViewer3d

# pyOCC
from OCC.Core.AIS import AIS_InteractiveContext, AIS_Shape, AIS_Trihedron, AIS_ViewCube
from OCC.Core.Aspect import Aspect_GradientFillMethod, Aspect_TOTP_RIGHT_LOWER, Aspect_TypeOfTriedronPosition
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex, BRepBuilderAPI_Transform
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec
from OCC.Core.Graphic3d import (
    Graphic3d_AspectLine3d,
    Graphic3d_Camera,
    Graphic3d_GraduatedTrihedron,
    Graphic3d_RenderingParams,
    Graphic3d_RM_RASTERIZATION,
    Graphic3d_StereoMode_QuadBuffer,
    Graphic3d_StructureManager,
    Graphic3d_TransformPers,
    Graphic3d_TransModeFlags,
    Graphic3d_Vec2i,
)
from OCC.Core.Prs3d import Prs3d_DatumAspect, Prs3d_DatumParts, Prs3d_LineAspect
from OCC.Core.Quantity import (
    Quantity_Color,
    Quantity_NOC_BLACK,
    Quantity_NOC_BLUE,
    Quantity_NOC_GREEN,
    Quantity_NOC_RED,
    Quantity_NOC_WHITE,
    Quantity_TOC_RGB,
)
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_ShapeEnum, TopAbs_SHELL, TopAbs_SOLID, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import topods
from OCC.Core.V3d import V3d_TypeOfOrientation, V3d_View, V3d_ZBUFFER
from OCC.Display.OCCViewer import Viewer3d

# PySide6
from PySide6 import QtGui
from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPalette
from PySide6.QtWidgets import QApplication, QRubberBand, QStyleFactory, QWidget

# local
from pyOCCTools import VisualizationCONFIG, createTrihedron, getColor

# 使用配置值
X_AXIS_DIRECTION = VisualizationCONFIG.X_AXIS_DIRECTION
Y_AXIS_DIRECTION = VisualizationCONFIG.Y_AXIS_DIRECTION
Z_AXIS_DIRECTION = VisualizationCONFIG.Z_AXIS_DIRECTION
X_AXIS_COLOR = VisualizationCONFIG.X_AXIS_COLOR
Y_AXIS_COLOR = VisualizationCONFIG.Y_AXIS_COLOR
Z_AXIS_COLOR = VisualizationCONFIG.Z_AXIS_COLOR


class qtBaseViewerWidget(QWidget):
    """The base Qt Widget for an OCC viewer"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewer3d = myViewer3d()
        self.context: AIS_InteractiveContext = self.viewer3d.Context
        self.view: V3d_View = self.viewer3d.View
        self.viewer: V3d_View = self.viewer3d.Viewer
        self.camera: Graphic3d_Camera = self.viewer3d.camera
        self.structure_manager: Graphic3d_StructureManager = self.viewer3d.structure_manager
        # self._inited = False

        # 开启鼠标跟踪
        self.setMouseTracking(True)
        # Strong focus
        self.setFocusPolicy(Qt.WheelFocus)

        self.setAttribute(Qt.WA_NativeWindow)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.setAutoFillBackground(False)

    # end alternate constructor
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewer3d.View.MustBeResized()

    # end def
    def paintEngine(self):
        return None

    # end def
    # def focusInEvent(self, event):
    #     window = self.window()
    #     # print("Focused Window:", window.windowTitle())  # 打印窗口标题
    #     event.accept()  # 接受焦点事件
    # end def


# end class
class qtViewer3dWidget(qtBaseViewerWidget):
    # emit signal when selection is changed
    # 选中了 AIS 对象的信号
    signal_AISs_selected = Signal(list)

    def __init__(
        self,
        parent=None,
        view_trihedron=False,
        origin_trihedron=False,
        view_cube=True,
        bg_color_aspect: tuple[tuple, tuple, Aspect_GradientFillMethod] = (
            (37, 55, 113),
            (36, 151, 132),
            Aspect_GradientFillMethod.Aspect_GradientFillMethod_Vertical,
        ),
        selection_color: tuple[int, int, int] = (13, 141, 255),
        enable_multiply_select=False,
    ):
        super().__init__(parent)

        self.setObjectName("qt_viewer_3d")

        self._draw_box = []
        self._rubber_band = None
        self.enable_multiply_select = enable_multiply_select
        self._view_trihedron = view_trihedron
        self._origin_trihedron = origin_trihedron
        self._view_cube = view_cube
        self._bg_gradient_color = bg_color_aspect
        self._selection_color = selection_color
        self._zoom_area = False
        self._select_area = False
        self._inited = False
        self._left_is_down = False
        self._middle_is_down = False
        self._right_is_down = False
        self._selection = None
        self._drawtext = True
        self._qApp = QApplication.instance()
        self._key_map = {}
        self._shift_key_map = {}
        self._ctrl_key_map = {}
        self._current_cursor = "arrow"
        self._available_cursors = {}
        self._floor = True

    # end alternate constructor
    @property
    def qApp(self):
        # reference to QApplication instance
        return self._qApp

    @qApp.setter
    def qApp(self, value):
        self._qApp = value

    # end property
    def InitDriver(self):
        """初始化，并设置快捷键和光标"""
        # print(int(self.winId()))
        self.viewer3d.Create(window_handle=int(self.winId()), parent=self)
        # 设置显示实体
        self.viewer3d.SetModeShaded()
        # 开启抗锯齿
        self.viewer3d.enable_anti_aliasing()
        self._inited = True
        # dict mapping keys to functions
        self._key_map = {
            # ord("A"): self.viewer3d.EnableAntiAliasing,  # 开启抗锯齿
            # ord("B"): self.viewer3d.DisableAntiAliasing,  # 关闭抗锯齿
            ord("F"): self.viewer3d.FitAll,  # 适应窗口
            ord("G"): self.viewer3d.change_selection_mode,  # 设置选择模式
            ord("H"): self.viewer3d.SetModeHLR,  # 隐藏线模式
            ord("S"): self.viewer3d.SetModeShaded,  # 实体模式
            ord("W"): self.viewer3d.SetModeWireFrame,  # 线框模式
        }
        self.create_cursors()
        # 设置选中后展示的颜色
        self.viewer3d.set_selection_color(1, getColor(self._selection_color))
        if self._view_trihedron:
            self.display_view_trihedron()
        if self._origin_trihedron:
            self.display_origin_trihedron()
        if self._view_cube:
            self.display_view_cube()
        if self._floor:
            pass
        # 设置渐变背景
        self.viewer3d.View.SetBgGradientColors(
            getColor(self._bg_gradient_color[0]), getColor(self._bg_gradient_color[1]), self._bg_gradient_color[2], True
        )
        # ******************************************************
        # *TEST
        # ******************************************************
        if False:
            # 开启光追效果
            self.viewer3d.SetRaytracingMode(depth=1)
        if True:
            # 开启光栅化效果
            self.viewer3d.SetRasterizationMode()
        if False:
            # 测试其它显示渲染效果
            # 设置之后背景色消失了
            self.viewer3d.ChangeRenderingParams(
                Method=Graphic3d_RM_RASTERIZATION,  # 使用光栅化渲染方法
                RaytracingDepth=3,  # 光线追踪深度为 3，控制反射和阴影的级别
                IsShadowEnabled=True,  # 启用阴影效果
                IsReflectionEnabled=False,  # 启用反射效果
                IsAntialiasingEnabled=False,  # 启用抗锯齿效果，使图形边缘更平滑
                IsTransparentShadowEnabled=False,  # 启用透明阴影效果
                StereoMode=Graphic3d_StereoMode_QuadBuffer,  # 设置立体立体视图模式为四缓冲立体视图
                AnaglyphFilter=Graphic3d_RenderingParams.Anaglyph_RedCyan_Optimized,  # 设置立体视图的滤光片类型
                ToReverseStereo=False,  # 不反转立体视图
            )

    # end def
    """
    ==============================================================
    Qt类方法重写
    ==============================================================
    """

    def keyPressEvent(self, event):
        """监听按键，并打印日志"""
        super().keyPressEvent(event)
        code = event.key()
        modifiers = event.modifiers()
        match (modifiers):
            case Qt.KeyboardModifier.ShiftModifier:
                if code in self._shift_key_map:
                    self._shift_key_map[code]()
                elif code in range(256):
                    logger.info(f"按键 Shift + {chr(code)} (key code: {code}) 未绑定")
                # else:
                #     logger.info(f"key: code {code} not mapped to any function")
            case Qt.KeyboardModifier.ControlModifier:
                if code in self._ctrl_key_map:
                    self._ctrl_key_map[code]()
                elif code in range(256):
                    logger.info(f"按键 Ctrl + {chr(code)} (key code: {code}) 未绑定")
                # else:
                #     logger.info(f"key: code {code} not mapped to any function")
            case Qt.KeyboardModifier.NoModifier:
                if code in self._key_map:
                    self._key_map[code]()
                elif code in range(256):
                    logger.info(f"按键 {chr(code)} (key code: {code}) 未绑定")
                else:
                    logger.info(f"key: code {code} not mapped to any function")
        # end match

    # end def
    def focusInEvent(self, event):
        if self._inited:
            self.viewer3d.Repaint()

    # end def
    def focusOutEvent(self, event):
        if self._inited:
            self.viewer3d.Repaint()

    # end def
    def paintEvent(self, event):
        if not self._inited:
            self.InitDriver()

        self.viewer3d.Context.UpdateCurrentViewer()
        #! 不能在此处 FitAll，会导致适应窗口缩放时候出错
        # self.viewer3d.FitAll()

    # end def
    def wheelEvent(self, event):
        modifiers = event.modifiers()
        """滚轮旋转"""
        delta = event.angleDelta().y()
        if delta > 0:
            zoom_factor = 2.0
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                zoom_factor = 1.1
        else:
            zoom_factor = 0.5
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                zoom_factor = 0.9
        # end if
        self.viewer3d.ZoomFactor(zoom_factor)

    # end def
    @property
    def cursor(self):
        return self._current_cursor

    @cursor.setter
    def cursor(self, value):
        """在更新的同时更新光标事件"""
        if not self._current_cursor == value:
            self._current_cursor = value
            cursor = self._available_cursors.get(value)

            if cursor:
                self.qApp.setOverrideCursor(cursor)
            else:
                self.qApp.restoreOverrideCursor()
            # end if
        # end if

    # end property
    def mousePressEvent(self, event):
        """鼠标点击响应"""
        self.setFocus()
        self.drag_start_position_x = event.position().toPoint().x()
        self.drag_start_position_y = event.position().toPoint().y()
        #! 必须加，否则旋转有迟滞
        self.viewer3d.StartRotation(event.position().toPoint().x(), event.position().toPoint().y())

    # end def
    def mouseMoveEvent(self, event):
        """鼠标移动响应"""
        pt = event.position().toPoint()
        buttons = event.buttons()
        modifiers = event.modifiers()
        match (buttons, modifiers):
            case (Qt.MouseButton.MiddleButton, Qt.KeyboardModifier.NoModifier):
                # 旋转
                # ROTATE
                self.cursor = "rotate"
                self.viewer3d.Rotation(pt.x(), pt.y())
                self._draw_box = []
            case (Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier):
                # 区域选择
                # SELECT AREA
                # todo 未完成
                self._select_area = True
                self._calculate_draw_box(event)
                # self.update()
            case (Qt.MouseButton.MiddleButton, Qt.KeyboardModifier.ControlModifier):
                # 平移
                # PAN
                dx = pt.x() - self.drag_start_position_x
                dy = pt.y() - self.drag_start_position_y
                self.drag_start_position_x = pt.x()
                self.drag_start_position_y = pt.y()
                self.cursor = "pan"
                self.viewer3d.Pan(dx, -dy)
                self._draw_box = []
            case (Qt.MouseButton.RightButton, Qt.KeyboardModifier.ShiftModifier):
                # 局部放大
                # ZOOM WINDOW
                self._zoom_area = True
                self.cursor = "zoom-area"
                self._calculate_draw_box(event)
                # self.update()
            case _:
                self._draw_box = []
                self.viewer3d.MoveTo(pt.x(), pt.y())
                self.cursor = "arrow"
        # 动态缩放
        # DYNAMIC ZOOM
        #! 暂时移除
        # elif buttons == Qt.RightButton and not modifiers == Qt.ShiftModifier:
        #     self.cursor = "zoom"
        #     self.viewer3d.Repaint()
        #     self.viewer3d.DynamicZoom(
        #         abs(self.dragStartPosX),
        #         abs(self.dragStartPosY),
        #         abs(pt.x()),
        #         abs(pt.y()),
        #     )
        #     self.dragStartPosX = pt.x()
        #     self.dragStartPosY = pt.y()
        #     self._draw_box = []

    # end def
    def mouseReleaseEvent(self, event):
        if self._rubber_band:
            self._rubber_band.hide()  # 删除选择框
        position = event.position().toPoint()
        button = event.button()
        buttons = event.buttons()  # 允许组合按键（左键 + 右键）
        modifier = event.modifiers()
        match button:
            case Qt.MouseButton.LeftButton:
                if self._select_area and self._draw_box and self.enable_multiply_select:
                    # 区域框选
                    [start_x, start_y, dx, dy] = self._draw_box
                    self.viewer3d.SelectArea(start_x, start_y, start_x + dx, start_y + dy)
                    self._select_area = False
                    self.update()
                    # !取消回调，不在该类中处理业务逻辑，利用qt信号进行逻辑处理，只传出ais对象列表
                    if self.viewer3d.selected_AISs:
                        self.signal_AISs_selected.emit(self.viewer3d.selected_AISs)
                else:
                    match modifier:
                        case Qt.KeyboardModifier.ControlModifier:
                            # 摁住 CTRL 多选
                            if self.enable_multiply_select:
                                self.viewer3d.ShiftSelect(position.x(), position.y())
                        case _:
                            # 单选
                            self.viewer3d.Select(position.x(), position.y())
                    # !取消回调，不在该类中处理业务逻辑，利用qt信号进行逻辑处理，只传出ais对象列表
                    if self.viewer3d.selected_AISs:
                        self.signal_AISs_selected.emit(self.viewer3d.selected_AISs)
                    # end match
                # end if
            case Qt.MouseButton.RightButton:
                if self._zoom_area and self._draw_box:
                    [start_x, start_y, dx, dy] = self._draw_box
                    self.viewer3d.ZoomArea(start_x, start_y, start_x + dx, start_y + dy)
                    self._zoom_area = False
                    self.update()
            case _:
                pass
        # end match
        self._draw_box = []
        self.cursor = "arrow"

    # end def
    """
    ==============================================================
    自定义方法
    ==============================================================
    """

    def _calculate_draw_box(self, event: QtGui.QMouseEvent, tolerance=2):
        """计算框选范围

        Parameters
        ----------
        `event` : QtGui.QMouseEvent
            _description_
        `tolerance` : int, optional
            最小的框大小，by default 2

        Returns
        -------
        `_draw_box`:list[x,y,dx,dy]
            起始点`x`, `y`和框的长宽`dx`, `dy`
        """
        point = event.position().toPoint()
        dx = point.x() - self.drag_start_position_x
        dy = point.y() - self.drag_start_position_y
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return None
        self._draw_box = [self.drag_start_position_x, self.drag_start_position_y, dx, dy]
        # todo 绘制选择框
        self.drawRubberBand(self.drag_start_position_x, self.drag_start_position_y, point.x(), point.y())

    # end def
    def drawRubberBand(self, minX, minY, maxX, maxY):
        aRect = QRect()

        # Set the rectangle correctly.
        aRect.setX(minX) if minX < maxX else aRect.setX(maxX)
        aRect.setY(minY) if minY < maxY else aRect.setY(maxY)

        aRect.setWidth(abs(maxX - minX))
        aRect.setHeight(abs(maxY - minY))

        if not self._rubber_band:
            self._rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            # setStyle is important, set to windows style will just draw rectangle frame, otherwise will draw a solid rectangle.
            self._rubber_band.setStyle(QStyleFactory.create("windows"))
            # print(QStyleFactory.keys())
            # self._rubber_band.setStyle(QStyleFactory.create("Fusion"))
        self._rubber_band.setGeometry(aRect)
        self._rubber_band.show()

    # end def
    def create_cursors(self):
        """设置鼠标光标"""
        self._available_cursors = {
            "arrow": QtGui.QCursor(Qt.CursorShape.ArrowCursor),  # default
            "pan": QtGui.QCursor(Qt.CursorShape.SizeAllCursor),  # 平移
            "rotate": QtGui.QCursor(Qt.CursorShape.CrossCursor),  # 旋转
            "zoom": QtGui.QCursor(Qt.CursorShape.SizeVerCursor),  # 缩放
            "zoom-area": QtGui.QCursor(Qt.CursorShape.SizeVerCursor),  # 局部缩放
        }

        self._current_cursor = "arrow"

    # end def
    def display_view_trihedron(self):
        """显示视图坐标轴"""
        a_origin_trihedron = createTrihedron(arrow_length=50)
        a_origin_trihedron.SetTransformPersistence(
            Graphic3d_TransformPers(
                (Graphic3d_TransModeFlags.Graphic3d_TMF_TriedronPers),
                Aspect_TypeOfTriedronPosition.Aspect_TOTP_RIGHT_LOWER,
                Graphic3d_Vec2i(80, 50),
            )
        )
        self.viewer3d.Context.Display(a_origin_trihedron, False)

    # end def
    def display_view_cube(self):
        """显示视图立方体"""
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

        # 显示视图立方体
        self.viewer3d.Context.Display(a_view_cube, False)

    # end def
    def display_origin_trihedron(self, arrow_length=1000, arrow_width=5):
        """显示原点坐标轴"""
        a_origin_trihedron = createTrihedron(arrow_length=arrow_length, arrow_width=arrow_width)
        self.viewer3d.Context.Display(a_origin_trihedron, False)

    def EraseAll(self):
        self.viewer3d.EraseAll()
        if self._view_trihedron:
            self.display_view_trihedron()
        if self._origin_trihedron:
            self.display_origin_trihedron()
        if self._view_cube:
            self.display_view_cube()
        self.context.UpdateCurrentViewer()

    # end def
    def display_graduated_trihedron(self):
        """显示带刻度的立方体"""
        a_trihedron_data = Graphic3d_GraduatedTrihedron()
        self.viewer3d.View.GraduatedTrihedronDisplay(a_trihedron_data)

    # end def


# end class
# class qtViewer3dWidgetWithManipulator(qtViewer3dWidget):
#     def __init__(self):
#         super().__init__(
#             self,
#             bg_color_aspect=((37, 55, 113), (36, 151, 132), Aspect_GradientFillMethod.Aspect_GradientFillMethod_Vertical),
#             selection_color=(13, 141, 255),
#         )
#         self.manipulator=AIS_Manipulator()

#     # end default constructor
#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)
#         pt = event.position().toPoint()
#         if self.manipulator.HasActiveMode():
#             self.manipulator.StartTransform(pt.x(),pt.y(),self.viewer3d.View)
#     # end def

# # end class
if __name__ == "__main__":
    app = QApplication([])
    ex = qtViewer3dWidget()
    ex.show()
    app.exec()
# end main
