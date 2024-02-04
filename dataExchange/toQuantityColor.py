"""
从 RGB 颜色值得到 Quantity_Color
Author: ICO
Date: 2024-01-21"""

from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

color_map = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
}


def to_Quantity_Color(r: int | tuple[int, int, int] | list[int] = 0, g=0, b=0, hex_color=None, rgb_color=None, color_name=None):
    if rgb_color:
        r, g, b = rgb_color
    elif hex_color:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    elif color_name:
        r, g, b = color_map[color_name]
    elif isinstance(r, tuple | list) and len(r) == 3:
        r, g, b = r
    elif isinstance(r, int):
        r, g, b = r, g, b

    return Quantity_Color(r / 255.0, g / 255.0, b / 255.0, Quantity_TOC_RGB)
