from typing import Annotated, Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray

Vector = Annotated[NDArray[np.float_], Literal[3,]]
Point = Annotated[NDArray[np.float_], Literal[3,]]
