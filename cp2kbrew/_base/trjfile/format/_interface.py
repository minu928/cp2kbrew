import numpy as np
from abc import ABCMeta, abstractmethod
from typing import TextIO


class TrjOpenerInterface(metaclass=ABCMeta):
    skip_head: int = 0

    def __init__(self, trjfile: str) -> None:
        self._trjfile = trjfile
        self._frame = 0
        self._energy = None
        self._coord = None
        self.trjdata_generator = self._generate_trjdata(trjfile=trjfile)
        self.nextframe()

    @property
    def natom(self) -> int:
        return int(self._natom)

    @property
    def coord(self):
        return np.array(self._coord).astype(float)

    @property
    def energy(self):
        return np.array([self._energy]).astype(float)

    @property
    def frame(self):
        return self._frame

    def nextframe(self) -> None:
        next(self.trjdata_generator)
        self._frame += 1

    def reset(self) -> None:
        self.__init__(trjfile=self._trjfile)

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
