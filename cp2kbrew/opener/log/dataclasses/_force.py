import re
import numpy as np
from ._interface import DataClass


class Force(DataClass):
    patterns = [re.compile("\s+\#\s+Atom\s+Kind\s+Element\s+X\s+Y\s+")]
    data = np.zeros([1, 3], dtype=float)
    _fmt = float
    _slice = slice(3, 6)

    def _inner_match_patterns(self, data):
        self.is_request_control = True
        self._tmp_data = []

    def _check_is_endline(self, line: str) -> bool:
        return line.startswith(" SUM OF ATOMIC")
