import numpy as np
from typing import Literal, Dict

from mdbrew.type import MDState, MDStateAttr

from cp2kbrew.opener import log, trj
from cp2kbrew.errors import NotEqualFrameError
from cp2kbrew.space import calculate_volume

__all__ = ["log", "trj"]


def stack(mdstates: list[MDState], what: MDStateAttr):
    return np.stack([getattr(mdstate, what) for mdstate in mdstates])


def tile(mdstate: MDState, nframes: int, what: MDStateAttr):
    return np.tile(getattr(mdstate, what), reps=(nframes, 1))


def __check_tolerance(a, b, *, tol: 1e-6):
    return np.all(np.abs(a - b) < tol)


FixableErrorCode = Literal["FirstRestart", "LogIO", "NoisyRestart", "none"]
FIXABLE_ERROR_CODES = ["FirstRestart", "LogIO", "NoisyRestart", "none"]


def check(
    trj_mdstates: list[MDState], log_mdstates: list[MDState], *, what: str = "energy", tol: float = 1e-6
) -> FixableErrorCode:
    if not trj_mdstates or not log_mdstates:
        raise ValueError("Input frame data lists cannot be empty.")

    trj_energylist = stack(trj_mdstates, what=what)
    log_energylist = stack(log_mdstates, what=what)

    trj_nframes = len(trj_mdstates)
    log_nframes = len(log_mdstates)

    if log_nframes != trj_nframes:
        if log_nframes == trj_nframes + 1:
            if __check_tolerance(log_energylist[1:], trj_energylist, tol=tol):
                return "FirstRestart"
        elif log_nframes + 1 == trj_nframes:
            if __check_tolerance(log_energylist, trj_energylist[:-1], tol=tol):
                return "LogIO"
        return "NoisyRestart"

    if __check_tolerance(log_energylist, trj_energylist, tol=tol):
        return "none"

    raise ValueError("Frame numbers match, but energy values do not.")


def fix(
    trj_mdstates: list[MDState], log_mdstates: list[MDState], errorcode: FixableErrorCode
) -> Dict[Literal["trj", "log"], list[MDState]]:
    if not trj_mdstates or not log_mdstates:
        raise ValueError("Input frame data lists cannot be empty.")
    assert errorcode in FIXABLE_ERROR_CODES, f"Cannot fix the errorcode: {errorcode}."
    dict_framedatalist = {"trj": trj_mdstates, "log": log_mdstates}
    match errorcode:
        case "none":
            return dict_framedatalist
        case "FirstRestart":
            log_mdstates = log_mdstates[1:]
        case "LogIO":
            trj_mdstates = trj_mdstates[:-1]
        case "NoisyRestart":
            trj_energylist = stack(trj_mdstates, what="energy")
            log_energylist = stack(log_mdstates, what="energy")
            log_frames, trj_frames = [], []
            for trj_frame, trj_energy in enumerate(trj_energylist):
                log_frame = np.where(np.abs(trj_energy - log_energylist) < 1e-6)[0]
                if log_frame.size == 1:
                    log_frame = log_frame[0]
                    log_frames.append(log_frame)
                    trj_frames.append(trj_frame)
            log_mdstates = [log_mdstates[frame] for frame in log_frames]
            trj_mdstates = [trj_mdstates[frame] for frame in trj_frames]
    # Update the framedatalist
    dict_framedatalist["trj"] = trj_mdstates
    dict_framedatalist["log"] = log_mdstates
    if check(trj_mdstates=trj_mdstates, log_mdstates=log_mdstates) != "none":
        raise ValueError(f"Fix failed for error code: {errorcode}. Frame data still not equal.")
    return dict_framedatalist


def merge(trj_mdstates: list[MDState], log_mdstates: list[MDState]) -> list[MDState]:
    trj_energylist = stack(trj_mdstates, what="energy")
    log_energylist = stack(log_mdstates, what="energy")
    if len(trj_energylist) != len(log_energylist):
        raise NotEqualFrameError(f"nframe Trj != nframe Log: {len(trj_energylist)} != {len(log_energylist)}")

    framedatalist = []
    for trj_framedata, log_framedata in zip(trj_mdstates, log_mdstates):
        framedata = MDState(
            coord=trj_framedata.coord,
            force=log_framedata.force,
            box=log_framedata.box,
            energy=log_framedata.energy,
            stress=log_framedata.stress,
            atom=log_framedata.atom,
            virial=log_framedata.virial,
        )
        framedatalist.append(framedata)
    return framedatalist


def calculate_virial(mdstate: MDState) -> np.ndarray:
    volume = calculate_volume(mdstate.box)
    return volume * mdstate.stress
