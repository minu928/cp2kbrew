import numpy as np
from typing import Literal, List
from dataclasses import dataclass
from unitbrew.style import FrameUnit
from cp2kbrew.typing import npstr, npf64, Box, Atom, Coord, Energy, Stress, Virial, Force
from cp2kbrew.space import convert_to_box_matrix

__all__ = ["FrameUnit", "FrameData", "FRAMEDATA_ATTR", "FrameDataAtrr"]


@dataclass(slots=True)
class FrameData:
    force: Force = None
    energy: Energy = None
    atom: Atom = None
    coord: Coord = None
    stress: Stress = None
    virial: Virial = None
    box: Box = None

    def __post_init__(self):
        if self.force is not None:
            self.force = np.array(self.force, dtype=npf64)
        if self.energy is not None:
            self.energy = np.array(self.energy, dtype=npf64)
        if self.atom is not None:
            self.atom = np.array(self.atom, dtype=npstr)
        if self.coord is not None:
            self.coord = np.array(self.coord, dtype=npf64)
        if self.stress is not None:
            self.stress = np.array(self.stress, dtype=npf64)
        if self.virial is not None:
            self.virial = np.array(self.virial, dtype=npf64)
        if self.box is not None:
            self.box = convert_to_box_matrix(self.box, dtype=npf64)


FRAMEDATA_ATTR = ("force", "energy", "atom", "coord", "stress", "virial", "box")
FrameDataAtrr = Literal["force", "energy", "atom", "coord", "stress", "virial", "box"]
FrameDataList = List[FrameData]
