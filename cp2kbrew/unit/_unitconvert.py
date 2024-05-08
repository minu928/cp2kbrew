from scipy import constants
from ._interface import UnitConvertInterface


length_dict = {"angstrom": 1.0, "nm": 10.0, "bohr": constants.value("atomic unit of length") * 1e10, "m": 1e10}
energy_dict = {"J": 1.0, "eV": constants.eV, "hatree": constants.value("atomic unit of energy")}
header_dict = {"G": "1e9*", "M": "1e6*"}
special_dict = {"Pa": "J/m^3", "N": "J/m"}


class UnitConvert(UnitConvertInterface):
    def __init__(self, what: str, *, sep: str = "->") -> None:
        self._sep = sep
        self._what = what
        self._inspected_what = self.inspect(what=what, sep=sep)
        self._multiplicity = eval(self._inspected_what)

    def __repr__(self) -> str:
        from_unit, to_unit = self._what.split(self._sep)
        return f"1 {from_unit} = {self._multiplicity} {to_unit}"

    @property
    def value(self) -> float:
        return float(self._multiplicity)

    @property
    def eval_value(self) -> str:
        return self._inspected_what

    def inspect(self, what, sep: str):
        what = self._encode_specialcase(what=what)
        replace_dict_list = [length_dict, energy_dict, header_dict]
        for replace_dict in replace_dict_list:
            for key, val in replace_dict.items():
                what = what.replace(key, str(f"{val}"))
        what = what.replace("^", "**")
        what = what.replace(sep, "/")
        return what

    def _encode_specialcase(self, what: str):
        for key, val in special_dict.items():
            what = what.replace(key, val)
        return what
