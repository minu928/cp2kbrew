import re
import numpy as np
from typing import List
from abc import abstractmethod, ABCMeta


class DataClass(metaclass=ABCMeta):
    is_request_control: bool = False
    _fmt = None
    _slice = None

    @property
    @abstractmethod
    def patterns(self) -> List[re.Pattern]:
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    def decode_line(self, line: str):
        if self.is_request_control:
            if self._check_is_endline(line=line):
                self.is_request_control = False
                self.data = np.array(self._tmp_data).astype(self._fmt)
                del self._tmp_data
            else:
                self._tmp_data.append(line.split()[self._slice])
        else:
            for pattern in self.patterns:
                if data := pattern.match(line):
                    self._inner_match_patterns(data=data)
                    break

    @abstractmethod
    def _inner_match_patterns(self, data):
        pass

    def _check_is_endline(self, line: str) -> bool:
        pass
