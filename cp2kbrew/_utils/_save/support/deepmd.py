import os
import numpy as np
from .._saveinterface import SaveInterface


class SaveDeePMDNPY(SaveInterface):
    _default_requests_list = ("force", "atom", "virial", "coord", "box", "energy")
    _default_units = {
        "cell": "angstrom",
        "coord": "angstrom",
        "stress": "eV/angstrom^3",
        "energy": "eV",
        "force": "eV/angstrom",
    }

    def _save_interface(self, path: str, requests_name: str, attr: type[np.ndarray], element_order: list) -> None:
        if requests_name == "atom":
            element_order = np.unique(attr) if element_order is None else element_order
            np.savetxt(os.path.join(path, "type_map.raw"), element_order, fmt="%s")
            element_dict = {element: i for i, element in enumerate(element_order)}
            firstframe_atom = attr[0]
            assert np.all([dat == firstframe_atom for dat in attr[1:]]), "Not All Frame Atom is not Same"
            type_raw_data = np.vectorize(element_dict.__getitem__)(firstframe_atom)
            np.savetxt(os.path.join(path, "type.raw"), type_raw_data, fmt="%d")
        else:
            save_path = os.path.join(path, "set.000")
            os.makedirs(save_path, exist_ok=True)
            np.save(os.path.join(save_path, requests_name), attr)
