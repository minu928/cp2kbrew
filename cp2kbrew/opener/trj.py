from pathlib import Path
from typing import TextIO, Generator
from dataclasses import dataclass

from mdbrew.type import MDState, MDUnit

from cp2kbrew.typing import FilePath


default_unit = MDUnit(energy="eV", coord="anstrom")


@dataclass
class TrjOpener:
    def __init_subclass__(cls):
        trjopeners[cls.fmt] = cls

    def generate_mdstates(self, trjfile: FilePath) -> Generator[MDState, None, None]:
        with Path(trjfile).open("r") as f:
            for _ in range(self.skip_head):
                next(f)
            while True:
                try:
                    yield self.extract_mdstates(f)
                except EOFError:
                    break
                except Exception as e:
                    raise AssertionError(f"Unexpected error in {self.__class__.__name__}: {e}")

    @staticmethod
    def extract_mdstates(file: TextIO) -> MDState:
        raise NotImplementedError


trjopeners: dict[str, TrjOpener] = {}


class PDBOpener(TrjOpener):
    skip_head = 2
    fmt = "pdb"

    @staticmethod
    def extract_mdstates(file: TextIO) -> MDState:
        line = file.readline()
        if not line:
            raise EOFError
        energy = float(line.split()[-1])
        next(file)
        coord = []
        while (line := file.readline()) and not line.startswith("END"):
            coord.append([float(x) for x in line.split()[3:6]])
        return MDState(energy=energy, coord=coord)


class XYZOpener(TrjOpener):
    skip_head = 0
    fmt = "xyz"

    @staticmethod
    def extract_mdstates(file: TextIO) -> MDState:
        line = file.readline()
        if not line:
            raise EOFError
        energy = float(file.readline().split()[-1])
        coord = []
        for _ in range(int(line)):
            line = file.readline().split()
            coord.append([float(x) for x in line[1:4]])
        return MDState(energy=energy, coord=coord)


def generate_mdstates(trjfile: FilePath, *, fmt: str = None) -> Generator[MDState, None, None]:
    if fmt is None:
        fmt = Path(trjfile).suffix[1:]
    return trjopeners[fmt]().generate_mdstates(trjfile)


def collect_mdstates(trjfile: FilePath) -> list[MDState]:
    return list(generate_mdstates(trjfile))
