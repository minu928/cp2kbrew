import numpy as np
from typing import Literal, Dict, Union
from cp2kbrew.opener.log import LogOpener
from cp2kbrew.opener.trj import TrjOpener

errors = ["None", "FirstRestartError", "LogIOError", "NoisyRestartError"]


def check_tolerance(a, b, *, tol=1e-6):
    return np.all(np.abs(a - b) < tol)


def check(log: LogOpener, trj: TrjOpener, *, tol: float = 1e-6) -> str:
    log_energies, trj_energies = log.energy, trj.energy
    log_nframe, trj_nframe = log.nframe, trj.nframe
    if log_nframe != trj_nframe:
        if log_nframe == trj_nframe + 1 and check_tolerance(log_energies[1:], trj_energies, tol=tol):
            return "FirstRestartError"
        elif log_nframe + 1 == trj_nframe and check_tolerance(log_energies, trj_energies[:-1], tol=tol):
            return "LogIOError"
        else:
            return "NoisyRestartError"
    elif np.all(log_energies - trj_energies < tol):
        return "None"
    else:
        raise f"Same Frame But Not Equal Energies"


def fix(
    log: LogOpener,
    trj: TrjOpener,
    error: Literal["None", "FirstRestartError", "LogIOError", "NoisyRestartError"],
    *,
    tol: float = 1e-6,
    verbose: bool = True,
) -> Union[LogOpener, TrjOpener]:
    assert error in errors, f"Not Supporting Error, We supports: {errors}"
    if verbose:
        print(f"Input error is {error}")
    if error == "None":
        return True
    try:
        if verbose:
            print(f" -> Try Fix...")
        if error == "FirstRestartError":
            log.modify_data(range(1, log.nframe))
        elif error == "LogIOError":
            trj.modify_data(range(log.nframe))
        elif error == "NoisyRestartError":
            log_energies = log.energy
            trj_energies = trj.energy
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
            log.modify_data(new_log_frames)
        if verbose:
            print(f" -> Check Energy Tolerance")
        assert check_tolerance(log.energy, trj.energy, tol=tol), f"Energies are still not equal.."
        if verbose:
            print(f" -> Success")
    except Exception as e:
        if verbose:
            print(f" -> Failed", end="")
        raise e

    return log, trj
