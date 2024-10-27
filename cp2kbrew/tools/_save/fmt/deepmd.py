import os
import numpy as np
from typing import Sequence
from numpy.typing import NDArray
from .._saveinterface import SaveInterface


class SaveDeePMDNPY(SaveInterface):
    _default_querylist = ("force", "atom", "virial", "coord", "cell", "energy")
    _default_units = {
        "cell": "angstrom",
        "coord": "angstrom",
        "stress": "eV/angstrom^3",
        "energy": "eV",
        "force": "eV/angstrom",
    }
    fmt = "deepmd@npy"

    def save(
        self,
        savepath: str,
        query_data: dict[str, NDArray],
        **kwrgs,
    ) -> None:
        for name, data in query_data.items():
            if name == "atom":
                element_order = kwrgs.get("element_order", None)
                element_order = np.unique(data) if element_order is None else element_order
                np.savetxt(os.path.join(savepath, "type_map.raw"), element_order, fmt="%s")
                element_dict = {element: i for i, element in enumerate(element_order)}
                firstframe_atom = data[0]
                assert np.all([dat == firstframe_atom for dat in data[1:]]), "Not All Frame Atom is not Same"
                type_raw_data = np.vectorize(element_dict.__getitem__)(firstframe_atom)
                np.savetxt(os.path.join(savepath, "type.raw"), type_raw_data, fmt="%d")
            else:
                if name == "cell":
                    name = "box"
                nframe = len(data)
                if name != "energy":
                    data = data.reshape(nframe, -1)
                save_path = os.path.join(savepath, "set.000")
                os.makedirs(save_path, exist_ok=True)
                np.save(os.path.join(save_path, name), data)
