from cp2kbrew._opener import Opener
from cp2kbrew._utils import Doctor


class Alchemist(Opener):
    def __init__(self, logfile: str, trjfile: str = None, *, trjfmt: str = "auto", mode: str = None) -> None:
        super().__init__(logfile, trjfile, trjfmt=trjfmt, mode=mode)

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
