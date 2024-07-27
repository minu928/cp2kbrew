import re
import numpy as np
from tqdm import tqdm
from typing import List
from copy import deepcopy
from .dataclasses import *
from cp2kbrew.tools import unit


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
    _restart_patterns = [r"\s+\*\s+RESTART INFORMATION\s+\*\s+"]

    def __init__(self, logfile: str) -> None:
        self.restart_frames = []
        self._frame = 0
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
        self.logfile = logfile
        self.logdata_generator = self.__generate_data_from_logfile(logfile=self.logfile)
        self.nextframe()
        self.update_data(data=self.dataclasses, is_dataclass=True)

    def __repr__(self) -> str:
        return self.__class__.__name__

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
    def virial(self) -> type[np.ndarray]:
        self.unit["virial"] = f"{self.unit['stress']}*{self.unit['cell']}^3"
        vol = np.array([np.linalg.det(cell) for cell in self.cell])
        return self.stress * vol[:, None, None]

    @property
    def end_patterns(self) -> List[re.Pattern]:
        return [re.compile(ep) for ep in self._end_patterns]

    @property
    def restart_patterns(self) -> List[re.Pattern]:
        return [re.compile(rp) for rp in self._restart_patterns]

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
                for restart_pattern in self.restart_patterns:
                    if restart_pattern.match(this_line):
                        self.restart_frames.append(self.nframe)
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
            pbar = tqdm(desc="[OPEN LOG]", unit=" frame")
            pbar.update(n=1)
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
        return self

    def update_data(self, data: dict[str, type[np.ndarray]], *, is_dataclass: bool = False):
        for key, val in data.items():
            if is_dataclass:
                val = np.array([val.data])[None, :]
            setattr(self, f"_{key}", val)

    def convert_unit(self, to: dict[str, str], *, sep: str = "->", ignore_notinclude: bool = False):
        if ignore_notinclude:
            to = {key: val for key, val in to.items() if hasattr(self, key)}
        for to_key, to_unit in to.items():
            what = f"{self.unit[to_key]}{sep}{to_unit}"
            multiplicity = float(unit.convert(what=what))
            self.unit[to_key] = to_unit
            this_val = getattr(self, to_key)
            setattr(self, f"_{to_key}", multiplicity * this_val)

    def modify_data(self, leftframes: int):
        for unit in self.unit.keys():
            if unit == "virial":
                continue
            setattr(self, f"_{unit}", getattr(self, unit)[leftframes])
        self._frame = len(self.energy)
