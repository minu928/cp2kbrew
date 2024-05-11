from ._interface import UnitConvertInterface
from ._support import support_items


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
        what = "(" + self._encode_specialcase(what=what)
        replace_dict_list = [val for key, val in support_items.items() if key != "special"]
        for replace_dict in replace_dict_list:
            for key, val in replace_dict.items():
                what = what.replace(key, str(f"{val}"))
        what = what.replace("^", "**")
        what = what.replace(sep, ")/(")
        what += ")"
        return what

    def _encode_specialcase(self, what: str):
        for key, val in support_items["special"].items():
            what = what.replace(key, val)
        return what
