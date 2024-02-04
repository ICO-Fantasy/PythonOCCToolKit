# PythonOCCToolKit

Python CAD Tool kits

`dataExchange`主要处理OCC和python之间的数据交换

`mathTools`是一些数学计算方法

`pyOCCTools`是一些与OCC数据有关的算法

`gemoetricTyping.pyi`定义了一些类型提示

`error`规定了一些自定义的错误类型

项目遵守 `PEP 8`命名规范：

- 模块(module))名，为首字母小写驼峰；
- 类(class)名，为首字母大写驼峰；
- 方法(function)名，为小写下划线；
- 变量(variable)、参数(parameter)名，为全小写下划线；
- 常量(constant)名，为全大写下划线；

项目中所用第三方库PySide6和python-occ中的命名格式为C++格式，不遵循 `PEP 8`规范，在 `dataExchange`中的部分方法名沿用其命名
