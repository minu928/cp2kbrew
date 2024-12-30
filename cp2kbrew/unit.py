from typing import Dict, Literal
from unitbrew import create_multiplier
from cp2kbrew.dataclass import FrameUnit, FrameData, FrameDataAtrr


def create_multiplierdict(
    from_unit: FrameUnit,
    to_unit: FrameUnit,
    *,
    targets=("coord", "force", "box", "energy", "stress", "virial"),
    is_None_pass: bool = True,
) -> Dict[str, float]:
    try:
        return {
            target: create_multiplier(f"{getattr(from_unit, target)}->{getattr(to_unit, target)}")
            for target in targets
            if getattr(from_unit, target) is not None or not is_None_pass
        }
    except AttributeError as e:
        raise ValueError(f"Invalid target field: {e}")


def convert_unit(framedata: FrameData, mutiplierdict: Dict[FrameDataAtrr, float]):
    for target, multiplier in mutiplierdict.items():
        val = getattr(framedata, target) * multiplier
        setattr(framedata, target, val)
    return framedata
