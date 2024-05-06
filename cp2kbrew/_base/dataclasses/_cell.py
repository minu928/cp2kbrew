import re
import numpy as np
from cp2kbrew._base.dataclasses._interface import DataClass


class Cell(DataClass):
    patterns = [re.compile(r"\s+[^0-9]+\|\s+Cell lengths\s+\[ang\]\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+")]
    data = np.zeros(3, dtype=float)
    _fmt = float

    def _inner_match_patterns(self, data):
        self.data = np.array([data["x"], data["y"], data["z"]]).astype(self._fmt)
