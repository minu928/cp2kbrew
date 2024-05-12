import re
import numpy as np
from ._interface import DataClass


int_a = ord("a")
int_x = ord("x")


class Cell(DataClass):
    patterns = [
        re.compile(r"\s+[^0-9]+\|\s+Cell lengths\s+\[ang\]\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+"),
        re.compile(r"\s+CELL\|\s+Vector\s+(?P<abc>\S+)\s+\[angstrom\]:\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+"),
    ]
    data = np.zeros(3, dtype=float)
    _fmt = float

    def _inner_match_patterns(self, data):
        data_dict = data.groupdict()
        if abc := data_dict.get("abc"):
            idat = ord(abc) - int_a
            ixyz = chr(idat + int_x)
            self.data[idat] = data_dict[ixyz]
        else:
            self.data = np.array([data["x"], data["y"], data["z"]]).astype(self._fmt)
