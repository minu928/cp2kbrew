from .support import SaveDeePMDNPY
from ._saveinterface import SaveInterface


__all__ = []


to_fmt_dict: dict[str, type[SaveInterface]] = {"deepmd@npy": SaveDeePMDNPY}


def save(
    fmt: str,
    obj,
    *,
    path: str = "./",
    request_list: list = None,
    element_order: list = None,
    unit: dict[str, str] = None,
) -> SaveInterface:
    assert fmt in to_fmt_dict, f"To Support Error: {fmt} is not supported."
    return to_fmt_dict[fmt]().save(
        obj=obj,
        path=path,
        request_list=request_list,
        element_order=element_order,
        unit=unit,
    )
