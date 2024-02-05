import numpy as np
import pandas as pd

# 假设 df1 和 df2 是两个形状不一致的 DataFrame
d1 = np.array([["A", "B", "C"], [1, 2, 3]])
d2 = np.array([["X", "Y", "Z", "R"], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)

# 使用 concat 进行拼接，axis=1 表示按列拼接
result = pd.concat([df1, df2], axis=1)

print(result)
