import re
import numpy as np
from cp2kbrew._base.dataclasses._interface import DataClass


class Atom(DataClass):
    patterns = [re.compile(r"\s+Atom\s+Kind\s+Element\s+X\s+Y\s+Z\s+Z\(eff\)\s+")]
    data = np.zeros([10], dtype=float)
    _fmt = "<U4"
    _slice = slice(2, 3)

    def _inner_match_patterns(self, data):
        self.is_request_control = True
        self._tmp_data = []

    def _check_is_endline(self, line: str) -> bool:
        return line.strip() == ""
