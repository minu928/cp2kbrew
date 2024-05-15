import numpy as np
from cp2kbrew._opener import Opener


def calc_energy_deviation(e1, e2, *, tol: float = 1e-10):
    return np.abs(e1 - e2) < tol


class Doctor:
    result_candidates = ["PERFECT", "SUCCESS", "FAILED"]

    def __init__(self, opener: Opener) -> None:
        self._openers = opener.openers
        self._energy = self._load_energy()
        self._restart_frames = self._openers["log"].restart_frames

    def _load_energy(self):
        return {key: val.energy for key, val in self._openers.items()}

    def fix(self, *, tol: float = 1e-10) -> str:
        if np.all(list(self.check(tol=tol).values())):
            return "PERFECT"

        log_energy = self._energy["log"]
        success = 0
        nframe_trj = len(self._energy["trj"])
        candiate_indexes = np.zeros(nframe_trj, dtype=int)

        for frame, trj_energy in enumerate(self._energy["trj"]):
            deviation = calc_energy_deviation(trj_energy, log_energy, tol=tol)
            std_indices = np.where(deviation)[0]
            n_std = len(std_indices)
            if n_std == 0:
                raise ValueError(f"There is no log data in frame ({frame})")
            elif n_std == 1:
                candiate_indexes[frame] = std_indices
                success += 1
            else:
                candiate_indexes[frame] = std_indices[0]
                success += 1
        if success == nframe_trj:
            self._openers["log"].modify_data(leftframes=candiate_indexes)
            self._energy = self._load_energy()
            return "SUCCESS"
        return "FAILED"

    def check(self, *, tol: float = 1e-10) -> dict[str, bool]:
        nframe_log, nframe_trj = self._openers["log"].nframe, self._openers["trj"].nframe
        check_list: dict[str, bool] = {"energy": False, "nframe": False}
        if nframe_log == nframe_trj:
            check_list["nframe"] = True
            if np.all(calc_energy_deviation(*self._energy.values(), tol=tol)):
                check_list["energy"] = True
        return check_list
