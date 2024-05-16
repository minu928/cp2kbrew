import numpy as np
from numpy.typing import NDArray
from cp2kbrew._opener.logfile import LogOpener
from cp2kbrew._opener.trjfile import TrjOpener
from cp2kbrew._utils import save


class Opener(object):
    def __init__(
        self,
        logfile: str,
        trjfile: str = None,
        *,
        trjfmt: str = "auto",
        mode: str = None,
    ) -> None:
        self._log_opener = LogOpener(logfile=logfile)
        self.__is_trj_opener_included: bool = trjfile is not None
        if self.__is_trj_opener_included:
            self._trj_opener = TrjOpener(trjfile=trjfile, fmt=trjfmt)
        self._update_unit()

    @property
    def openers(self):
        return {"log": self._log_opener, "trj": self._trj_opener}

    @property
    def atom(self) -> NDArray:
        return self._log_opener.atom

    @property
    def cell(self) -> NDArray:
        return self._log_opener.cell

    @property
    def coord(self) -> NDArray:
        if self.__is_trj_opener_included:
            return self._trj_opener.coord
        return self._log_opener.coord

    @property
    def energy(self) -> NDArray:
        return self._log_opener.energy

    @property
    def force(self) -> NDArray:
        return self._log_opener.force

    @property
    def stress(self) -> NDArray:
        return self._log_opener.stress

    @property
    def virial(self) -> NDArray:
        return self._log_opener.virial

    @property
    def nframe(self) -> int:
        return self._log_opener.nframe

    def gather(self, *, verbose: bool = True, is_reset: bool = True):
        self._log_opener.gather(verbose=verbose, is_reset=is_reset)
        if self.__is_trj_opener_included:
            self._trj_opener.gather(verbose=verbose, is_reset=is_reset)
        return self

    def convert_unit(self, to: dict[str, str], *, sep="->") -> None:
        self._log_opener.convert_unit(to=to, sep=sep)
        self._trj_opener.convert_unit(to=to, sep=sep, ignore_notinclude=True)
        self._update_unit()

    def _update_unit(self) -> None:
        if self.__is_trj_opener_included:
            for trj_unit, val_unit in self._trj_opener.unit.items():
                assert self._log_opener.unit[trj_unit] == val_unit, "Trj Unit and Log Unit is Different"
        self.unit = self._log_opener.unit

    def save(
        self,
        fmt: str,
        *,
        path: str = "./",
        request_list: list = None,
        element_order: list = None,
        unit: dict[str, str] = None,
    ) -> None:
        save(fmt=fmt, obj=self, path=path, request_list=request_list, element_order=element_order, unit=unit)
