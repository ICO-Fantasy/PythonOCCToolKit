from loguru import logger
from OCC.Core.IFSelect import IFSelect_ItemsByEntity, IFSelect_RetDone
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopoDS import TopoDS_Shape


def read_step(dir_path: str):
    """read the STEP file and returns a compound"""
    # 生成一个 step 模型类
    reader = STEPControl_Reader()
    # 加载一个文件并且返回一个状态枚举值
    status = reader.ReadFile(dir_path)

    # 如果正常执行且有模型
    if status == IFSelect_RetDone:  # check status
        fails_only = False
        # 如果存在无效或者不完整步骤实体，会显示错误信息
        reader.PrintCheckLoad(fails_only, IFSelect_ItemsByEntity)
        reader.PrintCheckTransfer(fails_only, IFSelect_ItemsByEntity)

        # 执行步骤文件转换
        ok = reader.TransferRoot(1)
        # 返回转换后的形状
        aResShape = reader.Shape(1)
    else:
        logger.error("模型加载失败")
    return aResShape
