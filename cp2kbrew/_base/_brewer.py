import numpy as np
from tqdm import tqdm
from .logfile import LogOpener
from .trjfile import trjopener


class CP2kBrewer(object):
    def __init__(self, logfile: str, trjfile: str, *, trjformat: str = "auto") -> None:
        self.log_opener = LogOpener(logfile=logfile)
        self.trjformat = self._check_trjformat(trjfile=trjfile, trjformat=trjformat)
        self.trj_opener = trjopener[self.trjformat](trjfile=trjfile)

    def _check_trjformat(self, trjfile, trjformat):
        if trjformat == "auto":
            return trjfile.split(".")[-1]
        return trjformat

    @property
    def frame(self) -> int:
        assert (
            self.log_opener.frame == self.trj_opener.frame
        ), f"Frame of Openers are different, LOG({self.log_opener.frame}) != TRJ({self.trj_opener.frame})"
        return self.log_opener.frame

    @property
    def data(self):
        _data = self.log_opener.data
        _data["coords"] = self.trj_opener.coords
        assert (
            abs(_data["energy"] - self.trj_opener.energy) < 1e-7
        ), f"Energy are different at Frame {self.frame}, LOG({_data['energy']}) != TRJ({self.trj_opener.energy})"
        return _data

    @property
    def gathered_data(self):
        if not hasattr(self, "_gathered_data"):
            self.gather()
        return self._gathered_data

    def gather(self, *, total: int = None, verbose: bool = True):
        if verbose:
            pbar = tqdm(desc="[GATHER DATA]", total=total)
        _data = {key: [val] for key, val in self.data.items()}
        while True:
            try:
                self.nextframe()
                for key, val in self.data.items():
                    _data[key].append(val)
                if verbose:
                    pbar.update(n=1)
            except:
                break
        _data = {key: np.array(val) for key, val in _data.items()}
        self._gathered_data = _data
        return self._gathered_data

    def nextframe(self):
        self.log_opener.nextframe()
        self.trj_opener.nextframe()
