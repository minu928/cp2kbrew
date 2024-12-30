from pathlib import Path
from typing import TextIO, Dict, Generator, List
from dataclasses import dataclass
from cp2kbrew.dataclass import FrameData, FrameUnit
from cp2kbrew.typing import FilePath


default_unit = FrameUnit(energy="eV", coord="anstrom")


@dataclass
class TrjOpener:
    def __init_subclass__(cls):
        trjopeners[cls.fmt] = cls

    def generate_framedata(self, trjfile: FilePath) -> Generator[FrameData, None, None]:
        with Path(trjfile).open("r") as f:
            for _ in range(self.skip_head):
                next(f)
            while True:
                try:
                    yield self.extract_framedata(f)
                except EOFError:
                    break
                except Exception as e:
                    raise AssertionError(f"Unexpected error in {self.__class__.__name__}: {e}")

    @staticmethod
    def extract_framedata(file: TextIO) -> FrameData:
        raise NotImplementedError


trjopeners: Dict[str, TrjOpener] = {}


class PDBOpener(TrjOpener):
    skip_head = 2
    fmt = "pdb"

    @staticmethod
    def extract_framedata(file: TextIO) -> FrameData:
        line = file.readline()
        if not line:
            raise EOFError
        energy = float(line.split()[-1])
        next(file)
        coord = []
        while (line := file.readline()) and not line.startswith("END"):
            coord.append([float(x) for x in line.split()[3:6]])
        return FrameData(energy=energy, coord=coord)


class XYZOpener(TrjOpener):
    skip_head = 0
    fmt = "xyz"

    @staticmethod
    def extract_framedata(file: TextIO) -> FrameData:
        line = file.readline()
        if not line:
            raise EOFError
        energy = float(file.readline().split()[-1])
        coord = []
        for _ in range(int(line)):
            line = file.readline().split()
            coord.append([float(x) for x in line[1:4]])
        return FrameData(energy=energy, coord=coord)


def generate_framedata(trjfile: FilePath, *, fmt: str = None) -> Generator[FrameData, None, None]:
    if fmt is None:
        fmt = Path(trjfile).suffix[1:]  # 더 안전한 확장자 추출
    return trjopeners[fmt]().generate_framedata(trjfile)


def collect_framedata(trjfile: FilePath) -> List[FrameData]:
    return list(generate_framedata(trjfile))
