from mdbrew import MDState

from cp2kbrew.writer.base import registry

support_fmts = tuple(registry.keys())


def write(
    path: str,
    mdstates: list[MDState],
    fmt: str,
    *,
    querylist: list = None,
    **kwargs,
) -> None:
    assert fmt in support_fmts, f"To Support Error: {fmt} is not supported. Supporting: {support_fmts}"
    writer = registry.get(fmt)
    writer.write(path=path, mdstates=mdstates, querylist=querylist, **kwargs)
