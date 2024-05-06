from ._interface import TrjOpenerInterface


class XYZOpener(TrjOpenerInterface):
    def _inner_generate_trjdata(self, file):
        self._natoms = int(file.readline().strip())
        self._energy = file.readline().split()[-1]
        self._coords = [file.readline().split()[1:4] for _ in range(self._natoms)]
