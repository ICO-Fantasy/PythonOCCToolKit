"""
从 python 字符串转换到 TCollection 类型字符
(在后续的 pyOCC 版本中可能会删除)
Author: ICO
Date: 2024-02-04"""

from OCC.Core.TCollection import (TCollection_AsciiString,
                                  TCollection_ExtendedString)


def to_ExtendedString(string: str):
    return TCollection_ExtendedString(string,True)


# end if
def to_AsciiString(string: str):
    return TCollection_AsciiString(string)


# end if
