"""
获取 TopoDS_Face 的几何信息
Author: ICO
Date: 2024-01-21"""
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepGProp import BRepGProp_Face
from OCC.Core.gp import gp_Vec
from OCC.Core.TopoDS import TopoDS_Face


def get_face_normal(topo_face: TopoDS_Face):
    brep_adp_face = BRepAdaptor_Surface(topo_face)
    center_u = brep_adp_face.FirstUParameter() + (brep_adp_face.LastUParameter() - brep_adp_face.FirstUParameter()) / 2
    center_v = brep_adp_face.FirstVParameter() + (brep_adp_face.LastVParameter() - brep_adp_face.FirstVParameter()) / 2
    center_point = brep_adp_face.Value(center_u, center_v)
    face_normal = gp_Vec()
    brep_face = BRepGProp_Face(topo_face)
    brep_face.Normal(center_u, center_v, center_point, face_normal)  # face1 的法线
    return face_normal


# end def
def get_face_center(topo_face: TopoDS_Face):
    brep_adp_face = BRepAdaptor_Surface(topo_face)
    center_u = brep_adp_face.FirstUParameter() + (brep_adp_face.LastUParameter() - brep_adp_face.FirstUParameter()) / 2
    center_v = brep_adp_face.FirstVParameter() + (brep_adp_face.LastVParameter() - brep_adp_face.FirstVParameter()) / 2
    center_point = brep_adp_face.Value(center_u, center_v)
    return center_point


# end def
