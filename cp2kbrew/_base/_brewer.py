import numpy as np
from tqdm import tqdm
from copy import deepcopy
from cp2kbrew import unit
from .trjfile import trjopener
from .logfile import LogOpener, default_units


class CP2KBrewer(object):
    def __init__(
        self,
        logfile: str,
        trjfile: str = None,
        *,
        fmt: str = "auto",
        is_gather_run: bool = True,
        total: int = None,
        verbose: bool = True,
    ) -> None:
        self._is_data_updated = False
        self._is_gathered_data = False
        self._multiplicity = {key: 1.0 for key in default_units.keys()}
        self.units = deepcopy(default_units)
        self.log_opener = LogOpener(logfile=logfile)
        self.is_trjfile_None = trjfile is None
        if not self.is_trjfile_None:
            self.trj_opener = trjopener[self._check_fmt(file=trjfile, fmt=fmt)](trjfile=trjfile)
        self.reset_data()
        if is_gather_run:
            self.gather(total=total, verbose=verbose)

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def nframe(self) -> int:
        return int(self.log_opener.frame + 1)

    @property
    def natoms(self) -> int:
        return int(len(self.log_opener.data["atom"]))

    @property
    def virial(self):
        if not hasattr(self, "_virial"):
            assert hasattr(self, "stress"), ArithmeticError("Theres is no stress in log")
            self.units["stress"] = f"({self.units['stress']}*{self.units['cell']}^3)"
            self._virial = self.stress * np.prod(self.cell, axis=-1)
        return self._virial

    def reset_data(self):
        self._update_data()
        for key in self._current_data.keys():
            setattr(self, key, None)

    def gather(self, *, total: int = None, verbose: bool = True):
        if self._is_gathered_data:
            return self

        if verbose:
            pbar = tqdm(desc="[GATHER DATA]", total=total)

        _data = {key: [val] for key, val in self._current_data.items()}
        while True:
            try:
                self._nextframe()
                self._update_data()
                for key, val in self._current_data.items():
                    _data[key].append(val.copy())
                if verbose:
                    pbar.update(n=1)
            except:
                break
        self._data = {key: np.array(val) for key, val in _data.items()}

        for key, val in self._data.items():
            setattr(self, key, val)

        self._is_gathered_data = True

        return self

    def convert_unit(self, to: dict[str, str], *, sep: str = "->"):
        assert self._is_gathered_data, f"Please gather the data."
        for to_key, to_unit in to.items():
            what = f"{self.units[to_key]}{sep}{to_unit}"
            multiplicity = float(unit.convert(what=what))
            self.units[to_key] = to_unit
            this_val = getattr(self, to_key)
            setattr(self, to_key, multiplicity * this_val)

    def _check_fmt(self, file, fmt):
        if fmt == "auto":
            return file.split(".")[-1]
        return fmt

    def _assert_errors(self):
        log_energy = self.log_opener.data["energy"]
        trj_energy = self.trj_opener.energy
        assert abs(log_energy - trj_energy) < 1e-7, f"Energy at Frame({self.frame}), LOG({log_energy})!=TRJ({trj_energy})"

    def _update_data(self):
        self._current_data = self.log_opener.data
        if not self.is_trjfile_None:
            self._current_data["coords"] = self.trj_opener.coords
            self._assert_errors()

    def _nextframe(self):
        self.log_opener.nextframe()
        self.trj_opener.nextframe()
