import re
import numpy as np
from cp2kbrew._base.dataclasses._interface import DataClass


class Energy(DataClass):
    patterns = [re.compile(r"\s+ENERGY\|\s+Total\s+FORCE_EVAL\s+\(\s+QS\s+\)\s+energy\s+\[a.u.\]\:\s+(?P<energy>\S+)\s+")]
    data = 0.0
    _fmt = float

    def _inner_match_patterns(self, data):
        self.data = np.array([data["energy"]]).astype(self._fmt)
