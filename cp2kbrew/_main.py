from cp2kbrew._opener import Opener
from cp2kbrew._error import Doctor


class Alchemist(Opener):
    def __init__(self, logfile: str, trjfile: str = None, *, trjfmt: str = "auto", mode: str = None) -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt, mode=mode)
        self._doctor = Doctor(opener=self)

    @property
    def doctor(self):
        return self._doctor

    def check_data(self, *, verbose: bool = True):
        self._doctor.check(verbose=verbose)
