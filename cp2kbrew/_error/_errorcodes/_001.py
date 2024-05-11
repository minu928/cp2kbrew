import numpy as np
from ._interface import ErrorCodeInterface, calc_dEnergy


class ErrorCode001(ErrorCodeInterface):
    error = "RESTART_FIRST_FRAME_ERROR"

    def fix(self) -> None:
        self._home._log_opener.modify_data(leftframes=slice(1, None))

    def check(self) -> bool:
        ## * nFrames
        if self._check_nframe():
            return False

        # * Restart Conditions
        if len(self.restart_frames) > 1:
            return False
        is_restart_in_first = self.restart_frames[0] == 0

        # * Energy Conditions
        is_oneframe_log_energy_shift_ok = np.all(calc_dEnergy(self.log_energy[1:], self.trj_energy))
        return is_restart_in_first and is_oneframe_log_energy_shift_ok
