# pyOCC
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeWire,
)
from OCC.Core.gp import gp_Pnt, gp_Vec
from OCC.Core.TopoDS import TopoDS_Shell


def create_tetrahedron(edge_length):
    # 创建四个顶点
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(edge_length, 0, 0)
    p3 = gp_Pnt(edge_length / 2, edge_length * 0.866, 0)
    p4 = gp_Pnt(edge_length / 2, edge_length * 0.288, edge_length * 0.816)

    # 计算重心坐标
    center_of_mass = gp_Pnt(
        (p1.X() + p2.X() + p3.X() + p4.X()) / 4, (p1.Y() + p2.Y() + p3.Y() + p4.Y()) / 4, (p1.Z() + p2.Z() + p3.Z() + p4.Z()) / 4
    )

    # 将顶点移动到重心位置
    v1 = BRepBuilderAPI_MakeVertex(gp_Pnt(p1.XYZ() - center_of_mass.XYZ())).Vertex()
    v2 = BRepBuilderAPI_MakeVertex(gp_Pnt(p2.XYZ() - center_of_mass.XYZ())).Vertex()
    v3 = BRepBuilderAPI_MakeVertex(gp_Pnt(p3.XYZ() - center_of_mass.XYZ())).Vertex()
    v4 = BRepBuilderAPI_MakeVertex(gp_Pnt(p4.XYZ() - center_of_mass.XYZ())).Vertex()

    # 创建 6 条边
    edge1 = BRepBuilderAPI_MakeEdge(v1, v2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(v2, v3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(v3, v1).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(v1, v4).Edge()
    edge5 = BRepBuilderAPI_MakeEdge(v2, v4).Edge()
    edge6 = BRepBuilderAPI_MakeEdge(v3, v4).Edge()

    # 创建四个线框
    wire1 = BRepBuilderAPI_MakeWire(edge1, edge5, edge4).Wire()
    wire2 = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
    wire3 = BRepBuilderAPI_MakeWire(edge2, edge6, edge5).Wire()
    wire4 = BRepBuilderAPI_MakeWire(edge3, edge4, edge6).Wire()

    # 创建四个面
    face1 = BRepBuilderAPI_MakeFace(wire1).Face()
    face2 = BRepBuilderAPI_MakeFace(wire2).Face()
    face3 = BRepBuilderAPI_MakeFace(wire3).Face()
    face4 = BRepBuilderAPI_MakeFace(wire4).Face()

    # 创建正四面体
    # tetrahedron = BRepBuilderAPI_MakeSolid(face1, face2, face3, face4).Solid()
    builder = BRep_Builder()
    shell = TopoDS_Shell()
    builder.MakeShell(shell)
    builder.Add(shell, face1)
    builder.Add(shell, face2)
    builder.Add(shell, face3)
    builder.Add(shell, face4)

    return shell
