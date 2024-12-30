import numpy as np
from numpy.typing import NDArray

npf64 = np.float64
npstr = np.str_

Box = NDArray[npf64]
Stress = NDArray[npf64]
Virial = NDArray[npf64]
Coord = NDArray[npf64]
Energy = NDArray[npf64]
Force = NDArray[npf64]
Atom = NDArray[npstr]

FilePath = str
Frame = int
