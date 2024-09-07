import numpy as np
from typing import Literal
from cp2kbrew._opener import Opener

errors = ["None", "FirstRestartError", "LogIOError", "NoisyRestartError"]
chk_tol = lambda a, b, tol: all(np.abs(a - b) < tol)


class Brewer(Opener):
    def __init__(
        self,
        logfile: str,
        trjfile: str = None,
        *,
        trjfmt: str = "auto",
        mode: Literal["auto", "manual"] = "auto",
        verbose: bool = True,
    ) -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt)
        self.act_by_mode(mode=mode, verbose=verbose)

    def act_by_mode(self, mode: Literal["auto", "manual"], *, verbose: bool = True):
        if mode == "auto":
            self.gather(verbose=verbose)
            if self.is_trj_included:
                error = self.check()
                self.fix(error=error, verbose=verbose)

    def check(self, *, tol: float = 1e-6) -> str:
        log_energies, trj_energies = self.log.energy, self.trj.energy
        log_nframe, trj_nframe = self.log.nframe, self.trj.nframe
        if log_nframe != trj_nframe:
            if log_nframe == trj_nframe + 1 and chk_tol(log_energies[1:], trj_energies, tol=tol):
                return "FirstRestartError"
            elif log_nframe + 1 == trj_nframe and chk_tol(log_energies, trj_energies[:-1], tol=tol):
                return "LogIOError"
            else:
                return "NoisyRestartError"
        elif all(log_energies - trj_energies < tol):
            return "None"
        else:
            raise f"Same Frame But Not Equal Energies"

    def fix(
        self,
        error: Literal["None", "FirstRestartError", "LogIOError", "NoisyRestartError"],
        *,
        tol: float = 1e-6,
        verbose: bool = True,
    ) -> None:
        assert error in errors, f"Not Supporting Error, We supports: {errors}"
        if verbose:
            print(f"Input error is {error}")
        if error == "None":
            return True
        try:
            if verbose:
                print(f" -> Try Fix...")
            if error == "FirstRestartError":
                self.log.modify_data(range(1, self.log.nframe))
            elif error == "LogIOError":
                self.trj.modify_data(range(self.log.nframe))
            elif error == "NoisyRestartError":
                log_energies = self.log.energy
                trj_energies = self.trj.energy
                log_chk_frame = 0
                new_log_frames = np.zeros(len(trj_energies), dtype=int) - 1
                for itrj, trj_energy in enumerate(trj_energies):
                    for ilog, log_energy in enumerate(log_energies[log_chk_frame:]):
                        if abs(log_energy - trj_energy) < tol:
                            log_chk_frame += ilog
                            if verbose:
                                print(f"\tTRJ({itrj}) -> LOG({log_chk_frame})")
                            new_log_frames[itrj] = log_chk_frame
                            break
                assert -1 not in new_log_frames, f"Not matched Error {np.where(new_log_frames == -1)[0]}"
                self.log.modify_data(new_log_frames)
            if verbose:
                print(f" -> Check Energy Tolerance")
            assert chk_tol(self.log.energy, self.trj.energy, tol=tol), f"Energies are still not equal.."
            if verbose:
                print(f" -> Success")
        except Exception as e:
            if verbose:
                print(f" -> Failed", end="")
            raise e
