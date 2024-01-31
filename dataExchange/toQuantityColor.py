"""
从 RGB 颜色值得到 Quantity_Color
Author: ICO
Date: 2024-01-21"""
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


def to_Quantity_Color(r: int | tuple[int, int, int], g=0, b=0):
    if isinstance(r, tuple):
        r, g, b = r
    return Quantity_Color(r / float(255), g / float(255), b / float(255), Quantity_TOC_RGB)
