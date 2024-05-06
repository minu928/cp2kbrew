from .format import XYZOpener, PDBOpener, TrjOpenerInterface

trjopener: dict[str, type[TrjOpenerInterface]] = {
    "xyz": XYZOpener,
    "pdb": PDBOpener,
}


__all__ = ["trjopener"]
