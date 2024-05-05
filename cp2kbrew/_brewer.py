# %%
import re


patterns = {"cell": re.compile(r"\s+CELL\|\s+Vector\s+[a-c]\s+\[angstrom\]:\s+(?P<x>\S+)\s+(?P<y>\S+)\s+(?P<z>\S+)\s+")}


class Opener:
    def __init__(self, logfile, xyzfile) -> None:
        self.logfile = logfile
        self.xyzfile = xyzfile
        self._data_dict = {}

    def __dict__(self):
        return self._data_dict

    def load_logfile(self):
        data_dict = {}
        with open(self.logfile) as log:
            while this_line := log.readline():
                for key, pattern in patterns.items():
                    print(pattern.match(this_line))
                    if data := pattern.match(this_line):
                        print(data)


# %%

if __name__ == "__main__":
    opener = Opener(logfile="../src/2022.2/out.log", xyzfile="../NAME-pos-1.xyz")

# %%
