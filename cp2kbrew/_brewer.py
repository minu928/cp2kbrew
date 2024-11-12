from typing import Literal
from numpy.typing import NDArray
from cp2kbrew import doctor
from cp2kbrew.tools import save, unit
from cp2kbrew.opener.log import LogOpener
from cp2kbrew.opener.trj import TrjOpener


class Brewer(object):
    def __init__(
        self,
        logfile: str,
        trjfile: str = None,
        *,
        trjfmt: str = "auto",
        mode: Literal["auto", "manual"] = "auto",
        verbose: bool = True,
        units: str = None,
    ) -> None:
        self.log = LogOpener(logfile=logfile)
        self.is_trj_included: bool = trjfile is not None
        self.trj = TrjOpener(trjfile=trjfile, fmt=trjfmt) if self.is_trj_included else None
        self._act_by_mode(mode=mode, verbose=verbose)
        self.convert_unit(unit.defaults if units is None else units)

    @property
    def atom(self) -> NDArray:
        return self.log.atom

    @property
    def cell(self) -> NDArray:
        return self.log.cell

    @property
    def coord(self) -> NDArray:
        if self.is_trj_included:
            return self.trj.coord
        return self.log.coord

    @property
    def energy(self) -> NDArray:
        return self.log.energy

    @property
    def force(self) -> NDArray:
        return self.log.force

    @property
    def stress(self) -> NDArray:
        return self.log.stress

    @property
    def virial(self) -> NDArray:
        return self.log.virial

    @property
    def nframe(self) -> int:
        return self.log.nframe

    def gather(self, *, verbose: bool = True, is_reset: bool = True):
        self.log.gather(verbose=verbose, is_reset=is_reset)
        if self.is_trj_included:
            self.trj.gather(verbose=verbose, is_reset=is_reset)
        return self

    def convert_unit(self, to: dict[str, str], *, sep="->") -> None:
        self.log.convert_unit(to=to, sep=sep)
        if self.is_trj_included:
            self.trj.convert_unit(to=to, sep=sep, ignore_notinclude=True)
        self.__update_unit()

    def __update_unit(self) -> None:
        if self.is_trj_included:
            for trj_unit, val_unit in self.trj.unit.items():
                assert self.log.unit[trj_unit] == val_unit, "Trj Unit and Log Unit is Different"
        self.unit = self.log.unit

    def _act_by_mode(self, mode: Literal["auto", "manual"], *, verbose: bool = True):
        if mode == "auto":
            self.gather(verbose=verbose)
            if self.is_trj_included:
                error = doctor.check(log=self.log, trj=self.trj)
                self.log, self.trj = doctor.fix(log=self.log, trj=self.trj, error=error, verbose=verbose)

    def save(
        self,
        fmt: str,
        *,
        savepath: str = "./",
        query_list: list = None,
        unit: dict[str, str] = None,
        element_order: list = None,
    ) -> None:
        save(
            fmt=fmt,
            obj=self,
            savepath=savepath,
            query_list=query_list,
            unit=unit,
            element_order=element_order,
        )
