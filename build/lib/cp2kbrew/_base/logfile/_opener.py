import re
from typing import List
from .dataclasses import *


class LogOpener:
    _end_patterns = ["\s+Extrapolation method:\s+ASPC\s+", "\s+\-\s+DBCSR STATISTICS\s+\-\s+"]

    def __init__(self, logfile: str) -> None:
        self._frame = -1
        self.logdata_generator = self._generate_data_from_logfile(logfile=logfile)
        self.nextframe()

    @property
    def data(self):
        return {key: dataclass.data for key, dataclass in self.dataclasses.items()}

    @property
    def end_patterns(self) -> List[re.Pattern]:
        return [re.compile(ep) for ep in self._end_patterns]

    @end_patterns.setter
    def end_patterns(self, patterns):
        self._end_patterns = patterns

    @property
    def frame(self) -> int:
        return self._frame

    def _generate_data_from_logfile(self, logfile: str):
        self.reset_dataclasses()
        with open(logfile, "r") as f:
            while this_line := f.readline():
                for end_pattern in self.end_patterns:
                    if end_pattern.match(this_line):
                        yield self.dataclasses
                for key, dataclass in self.dataclasses.items():
                    dataclass.decode_line(line=this_line)

    def reset_dataclasses(self) -> dict[str, DataClass]:
        self.dataclasses = {"cell": Cell(), "energy": Energy(), "atom": Atom(), "force": Force(), "stress": Stress()}

    def nextframe(self):
        self.dataclasses = next(self.logdata_generator)
        self._frame += 1
