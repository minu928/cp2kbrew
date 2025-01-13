from typing import Dict
from mdbrew import unit, MDState, MDUnit
from mdbrew._core import MDStateAttr


metal = MDUnit(coord="angstrom", box="angstrom", force="hatree/bohr", energy="eV", stress="eV/angstrom^3", virial="eV")


def create_multiplierdict(
    from_unit: MDState,
    to_unit: MDState,
    *,
    targets=("coord", "force", "box", "energy", "stress", "virial"),
    is_None_pass: bool = True,
) -> Dict[str, float]:
    try:
        return {
            target: unit.convert(f"{getattr(from_unit, target)}->{getattr(to_unit, target)}")
            for target in targets
            if getattr(from_unit, target) is not None or not is_None_pass
        }
    except AttributeError as e:
        raise ValueError(f"Invalid target field: {e}")


def convert_unit(framedata: MDState, mutiplierdict: Dict[MDStateAttr, float]):
    for target, multiplier in mutiplierdict.items():
        val = getattr(framedata, target) * multiplier
        setattr(framedata, target, val)
    return framedata
