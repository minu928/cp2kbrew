from scipy import constants


__all__ = ["support_items", "support_keys"]

length_dict = {"angstrom": 1.0, "nm": 10.0, "bohr": constants.value("atomic unit of length") * 1e10, "m": 1e10}

energy_dict = {"J": 1.0, "eV": constants.eV, "hatree": constants.value("atomic unit of energy")}

header_dict = {"G": "1e9*", "M": "1e6*"}

special_dict = {"Pa": "J/m^3", "N": "J/m"}

support_items = {
    "energy": energy_dict,
    "length": length_dict,
    "header": header_dict,
    "special": special_dict,
}

support_keys = {key: tuple(val.keys()) for key, val in support_items.items()}
