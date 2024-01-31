import math
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from OCC.Core.AIS import AIS_MultipleConnectedInteractive, AIS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone, BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Vec
from OCC.Core.Quantity import Quantity_Color
from OCC.Display.SimpleGui import init_display

from pyOCC.getColor import getColor


class AIS_Arrow(AIS_MultipleConnectedInteractive):
    def __init__(
        self,
        pnt: gp_Pnt,
        dir: gp_Dir,
        length=100,
        size=1,
        arrow_angle=20,
        cone_scale=1.5,
        arrow_color: tuple[int, int, int] = (255, 0, 0),
    ):
        super().__init__()
        # 将输入参数存储为对象属性
        self.r_size = size / 2
        self.arrow_angle = arrow_angle
        self.start_point = pnt
        self.direction = dir
        self.bottom_radius = self.r_size * cone_scale
        self.arrow_length = length
        self.arrow_high = self.bottom_radius / math.tan(math.radians(self.arrow_angle))
        self.cone_start = pnt.Translated(gp_Vec(dir).Scaled(self.arrow_length - self.arrow_high))
        self.arrow_color = getColor(arrow_color)
        # 创建锥体和圆柱体
        self._makeCone()
        self._makeCylinder()
        # 设置颜色
        self.SetColor(getColor(arrow_color))
        # 连接锥体和圆柱体
        self.Connect(self.cone)
        self.Connect(self.cylinder)

    # end alternate constructor

    def _makeCone(self):
        """创建锥体并将其存储为 self.cone"""
        axis = gp_Ax2(self.cone_start, self.direction)
        cone = BRepPrimAPI_MakeCone(axis, self.bottom_radius, 0, self.arrow_high).Shape()
        self.cone = AIS_Shape(cone)

    # end def
    def _makeCylinder(self):
        """创建圆柱体并将其存储为 self.cylinder"""
        axis = gp_Ax2(self.start_point, self.direction)
        cylinder = BRepPrimAPI_MakeCylinder(axis, self.r_size, self.arrow_length - self.arrow_high).Shape()
        self.cylinder = AIS_Shape(cylinder)

    # end def
    def SetColor(self, theColor: Quantity_Color):
        """设置锥体和圆柱体的颜色"""
        self.cone.SetColor(theColor)
        self.cylinder.SetColor(theColor)

    # end def


if __name__ == "__main__":
    display, start_display, add_menu, add_function_to_menu = init_display(size=(1920, 980), display_triedron=True)

    aarow = AIS_Arrow(gp_Pnt(*(0, 0, 0)), gp_Dir(*(1, 0, 0)))
    display.Context.Display(aarow, True)
    display.FitAll()
    start_display()
# end main
