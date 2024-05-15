from cp2kbrew._opener import Opener
from cp2kbrew._utils import Doctor


class Alchemist(Opener):
    def __init__(self, logfile: str, trjfile: str = None, *, trjfmt: str = "auto", mode: str = None) -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt, mode=mode)

    @property
    def doctor(self):
        return Doctor(opener=self)
