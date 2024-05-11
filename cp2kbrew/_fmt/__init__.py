from .support import ToDeePMD
from ._interface import ToInterface


__all__ = []


to_fmt_dict: dict[str, type[ToInterface]] = {"deepmd": ToDeePMD}


def to(fmt: str) -> ToInterface:
    assert fmt in to_fmt_dict, f"To Support Error: {fmt} is not supported."
    return to_fmt_dict[fmt]()
