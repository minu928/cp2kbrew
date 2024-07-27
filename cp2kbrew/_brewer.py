import numpy as np
from cp2kbrew._opener import Opener


errors = ("FirstRestartError", "NoisyRestartError", "LogIOError")


class Brewer(Opener):

    def __init__(self, logfile: str, trjfile: str = None, *, trjfmt: str = "auto", mode: str = "auto") -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt)

    def check(self, *, tol: float = 1e-8) -> str:
        log_energies, trj_energies = self.log.energy, self.trj.energy
        log_nframe, trj_nframe = self.log.nframe, self.trj.nframe
        if log_nframe != trj_nframe:
            if log_nframe == trj_nframe + 1 and all(log_energies[1:] - trj_energies < tol):
                return "FirstRestartError"
            elif log_nframe + 1 == trj_nframe and all(log_energies - trj_energies[1:] < tol):
                return "LogIOError"
            else:
                return "NoisyRestartError"
        return "None"

    def fix(self):

        return self
