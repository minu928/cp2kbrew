import numpy as np
from numpy.typing import NDArray
from .._saveinterface import SaveInterface


class SaveEXTXYZ(SaveInterface):
    _default_querylist = ("force", "atom", "virial", "coord", "cell", "energy")
    _default_units = {
        "cell": "angstrom",
        "coord": "angstrom",
        "stress": "eV/angstrom^3",
        "energy": "eV",
        "force": "eV/angstrom",
    }
    fmt = "trj@extxyz"

    def save(
        self,
        savepath: str,
        query_data: dict[str, NDArray],
        *,
        fmt: str = "%.8s",
        **kwrgs,
    ) -> None:
        property_line = f"Properties=species:S:1:pos:R:3"
        property_data = [query_data["atom"], query_data["coord"]]
        property_fmt = f"{fmt} {fmt} {fmt} {fmt}"
        if "force" in query_data:
            property_line += ":forces:R:3"
            property_data.append(query_data["force"])
            property_fmt += f" {fmt} {fmt} {fmt}"
        property_data = np.concatenate(property_data, axis=-1)
        mode = kwrgs.get("mode", "w")
        with open(f"{savepath}", mode=mode) as f:
            nframe, natoms, _ = query_data["atom"].shape
            for frame in range(nframe):
                f.writelines(f"\t{natoms}\n")
                # * Info Line
                infoline = ""
                if "cell" in query_data:
                    infoline += f'Lattice="{" ".join(query_data["cell"][frame].flatten().astype(str))}" '
                if "energy" in query_data:
                    infoline += f'energy="{query_data["energy"][frame][0]}" '
                if "virial" in query_data:
                    infoline += f'virial="{" ".join(query_data["virial"][frame].flatten().astype(str))}" '
                infoline += property_line + " "
                infoline += 'pbc="True True True" '
                infoline += "\n"
                f.writelines(infoline)
                np.savetxt(f, property_data[frame], fmt=property_fmt)
