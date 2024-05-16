from cp2kbrew._opener import Opener
from cp2kbrew._utils import Doctor


class Alchemist(Opener):
    support_modes = ("auto", "debug")

    def __init__(self, logfile: str, trjfile: str = None, *, trjfmt: str = "auto", mode: str = "auto") -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt, mode=mode)
        self._act_by_mode(mode=mode)

    def __repr__(self) -> str:
        status = ""
        status += "=" * 25 + "\n"
        status += f"{'Opener':^25s}\n"
        status += "=" * 25 + "\n"
        status += f"nFrame : {self.nframe}\n"
        status += f"nCell  : {self.cell.shape}\n"
        status += f"nCoord : {self.coord.shape}\n"
        status += f"nEnergy: {self.energy.shape}\n"
        status += f"nStress: {self.stress.shape}\n"
        status += f"nVirial: {self.virial.shape}\n"
        status += "=" * 25 + "\n"
        status += "=" * 25 + "\n"
        status += f"{'Doctor':^25s}\n"
        status += "=" * 25 + "\n"
        status += "\n".join([f"{k.upper()} = {v}" for k, v in self.doctor.check().items()]) + "\n"
        status += "=" * 25 + "\n"
        return status

    @property
    def doctor(self):
        return Doctor(opener=self)

    def _act_by_mode(self, mode: str):
        assert mode in self.support_modes, f"mode({mode}) is not supported."
        if mode == "auto":
            print(f"[STEP 01] -> gather")
            self.gather()
            print(f"[STEP 02] -> check")
            if not all(list(self.doctor.check().values())):
                print(f"[STEP 03] -> fix")
                fixed_result = self.doctor.fix()
                assert fixed_result in ["SUCCESS", "PERFECT"], f"fixing the data is failed.."
