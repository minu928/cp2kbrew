from . import fmt
from ._saveinterface import saver_dict

__all__ = ["save", "fmt"]


def save(
    fmt: str,
    obj,
    *,
    savepath: str = "./",
    querylist: list = None,
    unit: dict[str, str] = None,
    **kwrgs,
) -> None:
    assert fmt in saver_dict, f"To Support Error: {fmt} is not supported."
    save_object = saver_dict[fmt](querylist=querylist)

    # * Convert the unit
    if unit is not None and not hasattr(obj, "convert_unit"):
        raise ValueError(f"Unit Conversion Failed: obj not has attribute 'convert_unit'")
    unit = save_object.unit if unit is None else unit
    obj.convert_unit(to=unit)

    # * Send the query data
    query_data = {query_name: getattr(obj, query_name) for query_name in save_object.querylist}
    save_object.save(
        savepath=savepath,
        query_data=query_data,
        kwrgs=kwrgs,
    )
