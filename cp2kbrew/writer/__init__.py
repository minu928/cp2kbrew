from cp2kbrew.writer.base import registry
from cp2kbrew.dataclass import FrameDataList

support_fmts = tuple(registry.keys())


def write(
    path: str,
    framedatalist: FrameDataList,
    fmt: str,
    *,
    querylist: list = None,
    **kwargs,
) -> None:
    assert fmt in support_fmts, f"To Support Error: {fmt} is not supported. Supporting: {support_fmts}"
    writer = registry.get(fmt)
    writer.write(path=path, framedatalist=framedatalist, querylist=querylist, **kwargs)
