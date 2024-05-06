import numpy as np
from abc import ABCMeta, abstractmethod
from typing import TextIO


class TrjOpenerInterface(metaclass=ABCMeta):
    skip_head: int = 0

    def __init__(self, trjfile: str) -> None:
        self._frame = -1
        self._energy = None
        self._coords = None
        self.trjdata_generator = self._generate_trjdata(trjfile=trjfile)
        self.nextframe()

    @property
    def natoms(self) -> int:
        return int(self._natoms)

    @property
    def coords(self):
        return np.array(self._coords).astype(float)

    @property
    def energy(self):
        return np.array([self._energy]).astype(float)

    @property
    def frame(self):
        return self._frame

    def nextframe(self) -> None:
        self._frame += 1
        next(self.trjdata_generator)

    def _generate_trjdata(self, trjfile: str):
        with open(trjfile, "r") as f:
            [f.readline() for _ in range(self.skip_head)]
            while True:
                try:
                    yield self._inner_generate_trjdata(file=f)
                except:
                    break

    @abstractmethod
    def _inner_generate_trjdata(self, file: TextIO):
        pass
