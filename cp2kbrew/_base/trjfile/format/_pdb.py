from ._interface import TrjOpenerInterface


class PDBOpener(TrjOpenerInterface):
    skip_head = 2

    def _inner_generate_trjdata(self, file):
        self._energy = file.readline().split()[-1]
        file.readline()
        coords = []
        while this_line := file.readline():
            if this_line.startswith("END"):
                break
            coords.append(this_line.split()[3:6])
        self._coords = coords
        self._natom = len(coords)
        del coords
