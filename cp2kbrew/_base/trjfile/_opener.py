import numpy as np
from numpy import ndarray
from tqdm import tqdm
from .format import XYZOpener, PDBOpener, TrjOpenerInterface
from cp2kbrew import unit

trjopener_dict: dict[str, type[TrjOpenerInterface]] = {"xyz": XYZOpener, "pdb": PDBOpener}


class TrjOpener(object):
    def __init__(self, trjfile: str, *, fmt: str = "auto") -> None:
        self._trjfile = trjfile
        self.fmt = self.__check_fmt(trjfile=trjfile, fmt=fmt)
        self.__trjopener = trjopener_dict[self.fmt](trjfile=trjfile)
        self._coord = self.__trjopener.coord[None, ...]
        self._energy = self.__trjopener.energy[None, ...]
        self.unit = {"energy": "hatree", "coord": "angstrom"}

    @property
    def coord(self) -> type[ndarray]:
        return self._coord

    @property
    def energy(self) -> type[ndarray]:
        return self._energy

    @property
    def natom(self) -> int:
        return self.__trjopener.natom

    @property
    def nframe(self) -> int:
        return self.__trjopener.frame

    def __check_fmt(self, trjfile: str, fmt: str):
        if fmt == "auto":
            fmt = trjfile.split(".")[-1]
        assert fmt in trjopener_dict, KeyError(
            f"TrjOpener Support Format ({list(trjopener_dict.keys())}), Not include ({fmt})"
        )
        return fmt

    def gather(self, *, verbose: bool = True, is_reset: bool = True, what: tuple = ("energy", "coord")):
        self.reset()
        if verbose:
            pbar = tqdm(desc="[OPEN TRJ]")
        __data = {key: [getattr(self.__trjopener, key)] for key in what}
        while True:
            try:
                self.__trjopener.nextframe()
                for key in what:
                    __data[key].append(getattr(self.__trjopener, key))
                if verbose:
                    pbar.update(n=1)
            except:
                break
        for key, val in __data.items():
            setattr(self, f"_{key}", np.array(val))

    def convert_unit(self, to: dict[str, str], *, sep: str = "->", ignore_notinclude: bool = False):
        if ignore_notinclude:
            to = {key: val for key, val in to.items() if hasattr(self, key)}
        for to_key, to_unit in to.items():
            what = f"{self.unit[to_key]}{sep}{to_unit}"
            multiplicity = float(unit.convert(what=what))
            self.unit[to_key] = to_unit
            this_val = getattr(self, to_key)
            setattr(self, f"_{to_key}", multiplicity * this_val)

    def reset(self) -> None:
        self.__init__(trjfile=self._trjfile, fmt=self.fmt)
