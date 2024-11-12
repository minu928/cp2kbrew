import re
import numpy as np
from ._interface import DataClass


int_a = ord("a")


class Cell(DataClass):
    patterns = [
        re.compile(r"\s+[^0-9]+\|\s+Cell lengths\s+\[ang\]\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+"),
        re.compile(r"\s+CELL\|\s+Vector\s+(?P<abc>\S+)\s+\[angstrom\]:\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+"),
    ]
    data = np.zeros((3, 3), dtype=float)
    _fmt = float

    def _inner_match_patterns(self, data):
        data_dict = data.groupdict()
        if abc := data_dict.get("abc"):
            idat = ord(abc) - int_a
            self.data[idat, :] = np.array([data_dict["x"], data_dict["y"], data_dict["z"]])
        else:
            self.data = np.diag([float(val) for val in data_dict.values()])
