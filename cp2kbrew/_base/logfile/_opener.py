import re
import numpy as np
from tqdm import tqdm
from typing import List
from copy import deepcopy
from .dataclasses import *
from cp2kbrew import unit

default_units = {
    "cell": "angstrom",
    "energy": "hatree",
    "force": "hatree/bohr",
    "stress": "GPa",
    "atom": "none",
    "coord": "angstrom",
}


class LogOpener(object):
    _end_patterns = ["\s+Extrapolation method:\s+ASPC\s+", "\s+\-\s+DBCSR STATISTICS\s+\-\s+"]

    def __init__(self, logfile: str) -> None:
        self.logfile = logfile
        self._frame = -1
        self.is_gathered = False
        self.unit = deepcopy(default_units)
        self.dataclasses: dict[str, type[DataClass]] = {
            "cell": Cell(),
            "energy": Energy(),
            "atom": Atom(),
            "force": Force(),
            "stress": Stress(),
            "coord": Coord(),
        }
        self.logdata_generator = self.__generate_data_from_logfile(logfile=self.logfile)
        self.nextframe()
        self.update_data(data=self.dataclasses, is_dataclass=True)

    @property
    def atom(self) -> type[np.ndarray]:
        return self._atom

    @property
    def cell(self) -> type[np.ndarray]:
        return self._cell

    @property
    def coord(self) -> type[np.ndarray]:
        return self._coord

    @property
    def energy(self) -> type[np.ndarray]:
        return self._energy

    @property
    def force(self) -> type[np.ndarray]:
        return self._force

    @property
    def stress(self) -> type[np.ndarray]:
        return self._stress

    @property
    def end_patterns(self) -> List[re.Pattern]:
        return [re.compile(ep) for ep in self._end_patterns]

    @property
    def nframe(self) -> int:
        return self._frame

    def reset(self) -> None:
        self.__init__(logfile=self.logfile)

    def __generate_data_from_logfile(self, logfile: str):
        with open(logfile, "r") as f:
            while this_line := f.readline():
                for end_pattern in self.end_patterns:
                    if end_pattern.match(this_line):
                        yield self.dataclasses
                for dataclass in self.dataclasses.values():
                    dataclass.decode_line(line=this_line)

    def nextframe(self):
        assert not self.is_gathered, "End of the Frame"
        self.dataclasses = next(self.logdata_generator)
        self._frame += 1

    def gather(self, *, verbose: bool = True, is_reset: bool = True):
        assert not self.is_gathered, f"Already Gather the data, Please Reset."
        if is_reset:
            self.reset()
        if verbose:
            pbar = tqdm(desc="[OPEN LOG]")

        __data = {key: [val.data] for key, val in self.dataclasses.items()}
        while True:
            try:
                self.nextframe()
                for key, val in self.dataclasses.items():
                    __data[key].append(val.data)
                if verbose:
                    pbar.update(n=1)
            except:
                break
        __data = {key: np.array(val) for key, val in __data.items()}

        self.update_data(data=__data.copy())
        self.is_gathered = True

    def update_data(self, data: dict[str, type[np.ndarray]], *, is_dataclass: bool = False):
        for key, val in data.items():
            if is_dataclass:
                val = np.array(val.data)[None, :]
            setattr(self, f"_{key}", val)

    def convert_unit(self, to: dict[str, str], *, sep: str = "->"):
        for to_key, to_unit in to.items():
            what = f"{self.unit[to_key]}{sep}{to_unit}"
            multiplicity = float(unit.convert(what=what))
            self.unit[to_key] = to_unit
            this_val = getattr(self, to_key)
            setattr(self, f"_{to_key}", multiplicity * this_val)
