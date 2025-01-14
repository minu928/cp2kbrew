from pathlib import Path
from typing import Iterable, Union, List
from dataclasses import replace

from mdbrew import MDState, MDUnit, MDStateAttr

from cp2kbrew import opener
from cp2kbrew import handler
from cp2kbrew.unit import metal
from cp2kbrew.errors import NotAllUnitSameError
from cp2kbrew.utils import str_to_slice
from cp2kbrew.writer import write
from cp2kbrew.typing import FilePath
from cp2kbrew.unit import create_multiplierdict, convert_unit


__all__ = ["brew", "Brewer", "ClusterBrewer"]


class Brewer:
    def __init__(self, logfile: FilePath, trjfile: FilePath = None, *, unit: MDUnit = metal):
        self.logfile = Path(logfile)
        self.trjfile = Path(trjfile) if trjfile else None
        self._unit = opener.log.extract_frameunit(logfile=self.logfile)
        self._mdstates = self._collect_and_merge_mdstates(logfile=self.logfile, trjfile=self.trjfile)
        self.update_unit(unit=unit)
        self.update_virial()

    def __repr__(self):
        return f"Brewer(nframes={self.nframes}, natoms={self.natoms})"

    @property
    def nframes(self) -> int:
        return len(self.mdstates)

    @property
    def natoms(self) -> int:
        return len(self.mdstates[0].atom)

    @property
    def mdstates(self) -> list[MDState]:
        return self._mdstates

    @property
    def unit(self):
        return self._unit

    @staticmethod
    def _collect_and_merge_mdstates(logfile: FilePath, trjfile: FilePath) -> list[MDState]:
        mdstates = opener.log.collect_mdstates(logfile=logfile)
        if trjfile:
            log_mdstates = mdstates
            trj_mdstates = opener.trj.collect_mdstates(trjfile=trjfile)
            errorcode = handler.check(trj_mdstates=trj_mdstates, log_mdstates=log_mdstates)
            dict_mdstates = handler.fix(
                trj_mdstates=trj_mdstates,
                log_mdstates=log_mdstates,
                errorcode=errorcode,
            )
            mdstates = handler.merge(
                trj_mdstates=dict_mdstates["trj"],
                log_mdstates=dict_mdstates["log"],
            )
        return mdstates

    def update_unit(self, unit: MDUnit):
        mulitplierdict = create_multiplierdict(from_unit=self.unit, to_unit=unit, is_None_pass=True)
        self._mdstates = [convert_unit(framedata, mulitplierdict) for framedata in self._mdstates]
        self._unit = unit

    def update_virial(self):
        try:
            self._mdstates = [
                replace(framedata, virial=handler.calculate_virial(framedata)) for framedata in self._mdstates
            ]
        except Exception as e:
            raise ValueError(f"Failed to update virial: {str(e)}")

    def brew(self, what: MDStateAttr):
        return handler.stack(mdstates=self.mdstates, what=what)

    def write(
        self,
        path: FilePath,
        fmt: str,
        frames: Union[str, slice, Iterable] = ":",
        *,
        querylist: List[MDStateAttr] = None,
        **kwargs,
    ):
        try:
            if isinstance(frames, str):
                mdstates = self.mdstates[str_to_slice(frames)]
            elif isinstance(frames, slice):
                mdstates = self.mdstates[frames]
            elif isinstance(frames, Iterable):
                mdstates = [self.mdstates[int(frame)] for frame in frames]
            else:
                raise ValueError(
                    "Frames must be either a slice string ('1::2'), " "slice object (slice(1, None, 2)), or Iterable"
                )
            write(path=path, fmt=fmt, mdstates=mdstates, querylist=querylist, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to process frames: {str(e)}")


class ClusterBrewer(Brewer):
    def __init__(self, logfile_list: List[FilePath], trjfile_list: List[FilePath] = None, *, unit: MDUnit = metal):
        self.logfile_list = [Path(logfile) for logfile in logfile_list]
        self.trjfile_list = [Path(trjfile) for trjfile in trjfile_list] if trjfile_list else []
        self._validate_file_list()
        self._unit = self._initialize_unit()
        self._mdstates = self._init_mdstates()
        self.update_unit(unit=unit)
        self.update_virial()

    def _validate_file_list(self):
        if self.trjfile_list and len(self.logfile_list) != len(self.trjfile_list):
            raise ValueError("logfile_list and trjfile_list must have the same length.")

    def _init_mdstates(self) -> list[MDState]:
        return [
            self._collect_and_merge_mdstates(logfile, trjfile)[0]
            for logfile, trjfile in zip(self.logfile_list, self.trjfile_list or [None] * len(self.logfile_list))
        ]

    def _initialize_unit(self) -> list[MDState]:
        unit_list = [opener.log.extract_frameunit(logfile=logfile) for logfile in self.logfile_list]
        if not all(unit == unit_list[0] for unit in unit_list):
            raise NotAllUnitSameError("Units across logfiles are inconsistent.")
        return unit_list[0]


def brewer(
    logfiles: Union[FilePath, List[FilePath]],
    trjfiles: Union[FilePath, List[FilePath]] = None,
    *,
    unit: MDUnit = metal,
):
    if isinstance(logfiles, List):
        return ClusterBrewer(logfile_list=logfiles, trjfile_list=trjfiles, unit=unit)
    return Brewer(logfile=logfiles, trjfile=trjfiles, unit=unit)
