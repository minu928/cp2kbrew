import re
import numpy as np
from cp2kbrew._base.dataclasses._interface import DataClass


class Stress(DataClass):
    patterns = [re.compile("\s+STRESS\|\s+x\s+y\s+")]
    data = np.zeros([1, 3], dtype=float)
    _fmt = float
    _slice = slice(2, 5)

    def _inner_match_patterns(self, data):
        self.is_request_control = True
        self._tmp_data = []

    def _check_is_endline(self, line: str) -> bool:
        return line.startswith(" STRESS| 1/3 Trace")
