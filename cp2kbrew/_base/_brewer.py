import numpy as np
from tqdm import tqdm
from copy import deepcopy
from .logfile import LogOpener
from .trjfile import trjopener
from cp2kbrew.unit import UnitConvert


default_units = {
    "cell": "angstrom",
    "energy": "eV",
    "force": "hatree/bohr",
    "stress": "GPa",
    "atom": "none",
}


class CP2KBrewer(object):
    def __init__(self, logfile: str, trjfile: str, *, fmt: str = "auto", is_gather_run: bool = True) -> None:
        self._is_data_updated = False
        self._is_gathered_data = False
        self._multiplicity = {key: 1.0 for key in default_units.keys()}
        self.units = deepcopy(default_units)
        self.log_opener = LogOpener(logfile=logfile)
        self.trj_opener = trjopener[self._check_fmt(file=trjfile, fmt=fmt)](trjfile=trjfile)
        self.reset_data()
        if is_gather_run:
            self.gather()

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def nframe(self) -> int:
        return int(self.log_opener.frame + 1)

    @property
    def natoms(self) -> int:
        return int(len(self.log_opener.data["atom"]))

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
                self._assert_errors()
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
            multiplicity = float(UnitConvert(what=what))
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
        self._current_data["coords"] = self.trj_opener.coords

    def _nextframe(self):
        self.log_opener.nextframe()
        self.trj_opener.nextframe()
