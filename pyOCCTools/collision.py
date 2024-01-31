"""
干涉检测
Author: ICO
Date: 2024-01-21"""
# logger
from loguru import logger

# pyOCC
from OCC.Core.AIS import AIS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepExtrema import BRepExtrema_ShapeProximity
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh

"""
BRepMesh_IncrementalMesh

Parameters
----------
theShape: TopoDS_Shape
    参数类型：const TopoDS_Shape&
    描述：要进行网格化的形状。
theLinDeflection: float
    参数类型：const Standard_Real
    描述：线性偏差，控制三角化中的线性细节。
    它定义了离散化过程中生成的三角形的最大边长。
    较小的值会产生更精细的网格，但也会增加计算时间和内存需求。
    通常以模型单位为参考，表示在模型中的线性尺寸。
isRelative: bool (optional, default to Standard_False)
    参数类型：const Standard_Boolean（默认值：Standard_False）
    描述：是否使用相对值。
    如果设置为 Standard_True，则 theLinDeflection 用于每条边的离散化，其值为 <theLinDeflection> * <size of edge>。
    而对于面的离散化，使用它们边缘的最大偏差。
theAngDeflection: float (optional, default to 0.5)
    参数类型：const Standard_Real（默认值：0.5）
    描述：角度偏差，用于控制三角化中的角度细节。
    它定义了生成的三角形中最大角度的上限。较小的值会产生更细致的网格。
isInParallel: bool (optional, default to Standard_False)
    参数类型：const Standard_Boolean（默认值：Standard_False）
    描述：是否使用并行计算进行网格生成。
    如果设置为 Standard_True，则形状将在并行模式下进行网格生成。这在处理大型模型时可能提高性能。

Return
-------
None

"""


def ais_collision_calculator(ais_a: AIS_Shape, ais_b: AIS_Shape, get_collision_a=True, get_collision_b=True):
    """利用 AIS 对象进行干涉判断

    Parameters
    ----------
    `ais_a` : AIS_Shape
        干涉对象 A
    `ais_b` : AIS_Shape
        干涉对象 B
    `get_collision_a` : bool, 可选
        是否返回 A 中干涉碰撞的面，默认值：True
    `get_collision_b` : bool, 可选
        是否返回 B 中干涉碰撞的面，默认值：True

    Returns
    -------
    _type_
        发生了干涉碰撞的面（包含 A 和 B 的结果）
    """
    # 获取 AIS 对象的 TopoDS
    shape_a = ais_a.Shape()
    shape_b = ais_b.Shape()
    # 获取 AIS 对象的 Trsf
    trsf_a = ais_a.Transformation()
    trsf_b = ais_b.Transformation()
    # 移动原有的 shape
    shape_a = BRepBuilderAPI_Transform(shape_a, trsf_a).Shape()
    shape_b = BRepBuilderAPI_Transform(shape_b, trsf_b).Shape()
    # 生成网格
    mesh_a = BRepMesh_IncrementalMesh(shape_a, 1, False, 0.5, False)
    # mesh_a.Perform() #会自动调用 Perform()
    mesh_b = BRepMesh_IncrementalMesh(shape_b, 1, False, 0.5, False)
    # mesh_b.Perform() #会自动调用 Perform()
    # 碰撞检查
    checker = BRepExtrema_ShapeProximity(shape_a, shape_b, 0.1)
    checker.Perform()  # 需要手动调用 Perform()
    if checker.IsDone():
        # 获取 shape_a 的碰撞部分
        if get_collision_a:
            overlaps1 = checker.OverlapSubShapes1()
            face_indices1 = overlaps1.Keys()
            collision_face_a = []
            for ind in face_indices1:
                face = checker.GetSubShape1(ind)
                collision_face_a.append(face)

        # 获取 shape_b 的碰撞部分
        if get_collision_b:
            overlaps2 = checker.OverlapSubShapes2()
            face_indices2 = overlaps2.Keys()
            collision_face_b = []
            for ind in face_indices2:
                face = checker.GetSubShape2(ind)
                collision_face_b.append(face)
        # 返回发生干涉的面
        if collision_face_a or collision_face_b:
            return [*collision_face_a, *collision_face_b]
    else:
        logger.warning(f"干涉判断失败")
        return []


# end def
if __name__ == "__main__":
    pass
    # *两种变换方法等价
    # box_B_shape.Location(TopLoc_Location(box_B_trsf))
    # box_B_shape = BRepBuilderAPI_Transform(box_B_shape, box_B_trsf).Shape()
# end main
