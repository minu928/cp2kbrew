from abc import ABCMeta, abstractmethod


def calc_dEnergy(e1, e2, *, std: float = 1e-10):
    return e1 - e2 < std


class ErrorCodeInterface(metaclass=ABCMeta):
    def __init__(self, home) -> None:
        self._home = home

    def __repr__(self) -> str:
        return self.error

    @property
    def log_energy(self):
        return self._home._log_opener.energy

    @property
    def trj_energy(self):
        return self._home._trj_opener.energy

    @property
    def restart_frames(self) -> list[int]:
        return self._home._log_opener.restart_frames

    @property
    @abstractmethod
    def error(self) -> str:
        pass

    @abstractmethod
    def fix(self) -> None:
        pass

    @abstractmethod
    def check(self) -> bool:
        pass

    def _check_nframe(self) -> bool:
        return len(self.log_energy) == len(self.trj_energy)
