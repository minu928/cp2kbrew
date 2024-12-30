import numpy as np
from typing import Literal, Dict
from cp2kbrew.opener import log, trj
from cp2kbrew.dataclass import FrameData, FrameDataAtrr, FrameDataList
from cp2kbrew.errors import NotEqualFrameError
from cp2kbrew.space import calculate_volume

__all__ = ["log", "trj"]


def stack(framedatalist: FrameDataList, what: FrameDataAtrr):
    return np.stack([getattr(framedata, what) for framedata in framedatalist])


def tile(framedata: FrameData, nframes: int, what: FrameDataAtrr):
    return np.tile(getattr(framedata, what), reps=(nframes, 1))


def __check_tolerance(a, b, *, tol: 1e-6):
    return np.all(np.abs(a - b) < tol)


FixableErrorCode = Literal["FirstRestart", "LogIO", "NoisyRestart", "none"]
FIXABLE_ERROR_CODES = ["FirstRestart", "LogIO", "NoisyRestart", "none"]


def check(
    trj_framedatalist: FrameDataList, log_framedatalist: FrameDataList, *, what: str = "energy", tol: float = 1e-6
) -> FixableErrorCode:
    if not trj_framedatalist or not log_framedatalist:
        raise ValueError("Input frame data lists cannot be empty.")

    trj_energylist = stack(trj_framedatalist, what=what)
    log_energylist = stack(log_framedatalist, what=what)

    trj_nframes = len(trj_framedatalist)
    log_nframes = len(log_framedatalist)

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
    trj_framedatalist: FrameDataList,
    log_framedatalist: FrameDataList,
    errorcode: FixableErrorCode,
) -> Dict[Literal["trj", "log"], FrameDataList]:
    if not trj_framedatalist or not log_framedatalist:
        raise ValueError("Input frame data lists cannot be empty.")
    assert errorcode in FIXABLE_ERROR_CODES, f"Cannot fix the errorcode: {errorcode}."
    dict_framedatalist = {"trj": trj_framedatalist, "log": log_framedatalist}
    match errorcode:
        case "none":
            return dict_framedatalist
        case "FirstRestart":
            log_framedatalist = log_framedatalist[1:]
        case "LogIO":
            trj_framedatalist = trj_framedatalist[:-1]
        case "NoisyRestart":
            trj_energylist = stack(trj_framedatalist, what="energy")
            log_energylist = stack(log_framedatalist, what="energy")
            log_frames, trj_frames = [], []
            for trj_frame, trj_energy in enumerate(trj_energylist):
                log_frame = np.where(np.abs(trj_energy - log_energylist) < 1e-6)[0]
                if log_frame.size == 1:
                    log_frame = log_frame[0]
                    log_frames.append(log_frame)
                    trj_frames.append(trj_frame)
            log_framedatalist = [log_framedatalist[frame] for frame in log_frames]
            trj_framedatalist = [trj_framedatalist[frame] for frame in trj_frames]
    # Update the framedatalist
    dict_framedatalist["trj"] = trj_framedatalist
    dict_framedatalist["log"] = log_framedatalist
    if check(trj_framedatalist=trj_framedatalist, log_framedatalist=log_framedatalist) != "none":
        raise ValueError(f"Fix failed for error code: {errorcode}. Frame data still not equal.")
    return dict_framedatalist


def merge(trj_framedatalist: FrameDataList, log_framedatalist: FrameDataList) -> FrameDataList:
    trj_energylist = stack(trj_framedatalist, what="energy")
    log_energylist = stack(log_framedatalist, what="energy")
    if len(trj_energylist) != len(log_energylist):
        raise NotEqualFrameError(f"nframe Trj != nframe Log: {len(trj_energylist)} != {len(log_energylist)}")

    framedatalist = []
    for trj_framedata, log_framedata in zip(trj_framedatalist, log_framedatalist):
        framedata = FrameData(
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


def calculate_virial(framedata: FrameData) -> np.ndarray:
    volume = calculate_volume(framedata.box)
    return volume * framedata.stress
