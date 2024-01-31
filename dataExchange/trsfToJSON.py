import json

from OCC.Core.gp import gp_Trsf


def trsfToJSON(trsf: gp_Trsf):
    """
    Return
    ------
    `Location`: [x,y,z], `Matrix`: r_matrix(3*3), `shape`: float, `scale`: float
    """
    location = [trsf.Value(1, 4), trsf.Value(2, 4), trsf.Value(3, 4)]
    r_matrix = [
        trsf.Value(1, 1),
        trsf.Value(1, 2),
        trsf.Value(1, 3),
        trsf.Value(2, 1),
        trsf.Value(2, 2),
        trsf.Value(2, 3),
        trsf.Value(3, 1),
        trsf.Value(3, 2),
        trsf.Value(3, 3),
    ]
    shape = trsf.Form()
    scale = trsf.ScaleFactor()
    data = {"Location": location, "Matrix": r_matrix, "shape": shape, "scale": scale}
    # print(1111)
    # print(f'"Location": {location}, "Matrix": {Rmatrix}, "shape": {shpae}, "scale": {scale}')
    return json.dumps(data)


# if __name__ == "__main__":
#     atrsf = gp_Trsf()
#     atrsf.SetTranslationPart(gp_Vec(10, 20, 30))
#     atrsf.SetRotationPart(gp_Quaternion(gp_Vec(0, 0, 1), 180))
#     trsfToJSON(atrsf)
# # end main
