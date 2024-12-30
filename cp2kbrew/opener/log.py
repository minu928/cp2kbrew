import re
from pathlib import Path
from typing import Generator, List
from unitbrew.style import FrameUnit
from cp2kbrew.dataclass import FrameData
from cp2kbrew.typing import FilePath

END_PATTERNS = ["\s+Extrapolation method:\s+ASPC\s+", "\s+\-\s+DBCSR STATISTICS\s+\-\s+"]


def generate_framedata(logfile: FilePath) -> Generator[FrameData, None, None]:
    data = {
        "energy": None,
        "coord": [],
        "atom": [],
        "force": [],
        "stress": [],
        "box": [],
    }
    with Path(logfile).open("r") as f:
        is_coord_line_start = False
        is_force_line_start = False
        is_stress_line_start = False
        while line := f.readline():
            for end in END_PATTERNS:
                if re.match(end, line):
                    yield FrameData(**data)
                    data["energy"] = None
                    data["box"] = []
                    data["coord"] = []
                    data["force"] = []
                    data["stress"] = []

            # LINE: box
            if line.startswith(" CELL| Vector"):
                splited_line = line.split()
                data["box"].append(splited_line[4:7])
                continue
            if line.startswith(" MD| Cell lengths [ang"):
                data["box"] = line.split()[-3:]
                continue

            # LINE: energy
            if line.startswith(" ENERGY| Total"):
                splited_line = line.split()
                data["energy"] = splited_line[-1]
                continue

            # LINE: coord and atom
            if line.startswith(" Atom  Kind  Element"):
                data["atom"] = []
                data["coord"] = []
                is_coord_line_start = True
                continue
            elif line == "\n":
                is_coord_line_start = False
                continue
            elif is_coord_line_start:
                splited_line = line.split()
                data["atom"].append([splited_line[2]])
                data["coord"].append(splited_line[4:7])
                continue

            # LINE: force
            if line.startswith(" # Atom   Kind"):
                data["force"] = []
                is_force_line_start = True
                continue
            elif line.startswith(" SUM OF ATOMIC"):
                is_force_line_start = False
                continue
            elif is_force_line_start:
                data["force"].append(line.split()[3:7])
                continue

            # LINE: stress
            if line.startswith(" STRESS| Analytical"):
                data["stress"] = []
                is_stress_line_start = True
                next(f)  # skip next line
                continue
            elif line.startswith(" STRESS| 1/3"):
                is_stress_line_start = False
                continue
            elif is_stress_line_start:
                data["stress"].append(line.split()[2:])
                continue


def collect_framedata(logfile: FilePath) -> List[FrameData]:
    return list(generate_framedata(logfile))


def extract_frameunit(logfile: FilePath) -> FrameUnit:
    unit = {
        "energy": None,
        "coord": None,
        "force": None,
        "stress": None,
        "box": None,
    }
    with Path(logfile).open("r") as f:
        while line := f.readline():
            if all([u != None for u in unit.values()]):
                return FrameUnit(**unit)
            # LINE: box
            if line.startswith(" CELL| Vector"):
                unit["box"] = line.split()[3][1:-2]
                continue

            # LINE: energy
            if line.startswith(" ENERGY| Total"):
                this_unit = line.split()[-2][1:-2]
                unit["energy"] = "hatree" if this_unit == "a.u." else this_unit
                continue

            # LINE: coord and atom
            if "ATOMIC COORDINATES" in line:
                unit["coord"] = line.split()[-1]
                continue

            # LINE: force
            if line.startswith(" ATOMIC FORCES in"):
                this_unit = line.split()[-1][1:-1]
                unit["force"] = "hatree/bohr" if this_unit == "a.u." else this_unit

            # LINE: stress
            if line.startswith(" STRESS| Analytical"):
                unit["stress"] = line.split()[-1][1:-1]
                continue
