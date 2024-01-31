"""
坐标变换
Author: ICO
Date: 2024-01-21"""
from OCC.Core.gp import gp_Trsf


def change_ref_coord(trsf: gp_Trsf, new_ref: gp_Trsf, old_ref=gp_Trsf()):
    """将齐次变换的参考系调整到新的参考系

    Parameters
    ----------
    `trsf` : gp_Trsf
        _description_
    `new_ref` : gp_Trsf
        新参考系
    `old_ref` : _type_, 可选
        旧参考系，默认值：gp_Trsf()

    Returns
    -------
    gp_Trsf
        变换后的齐次变换
    """
    new_trsf = old_ref.Multiplied(trsf)
    temp_trsf = new_ref.Inverted()
    return_trsf = temp_trsf.Multiplied(new_trsf)
    return return_trsf


# end def
