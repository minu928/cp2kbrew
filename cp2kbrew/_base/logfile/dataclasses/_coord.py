import re
import numpy as np
from ._interface import DataClass


class Coord(DataClass):
    _test_line = " Atom  Kind  Element       X           Y           Z          Z(eff)       Mass"
    patterns = [re.compile("\s+Atom\s+Kind\s+Element\s+X\s+Y\s+Z\s+Z")]
    data = np.zeros([1, 3], dtype=float)
    _fmt = float
    _slice = slice(4, 7)

    def _inner_match_patterns(self, data):
        self.is_request_control = True
        self._tmp_data = []

    def _check_is_endline(self, line: str) -> bool:
        return line == "\n"
