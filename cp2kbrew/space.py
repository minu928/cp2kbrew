import numpy as np
from cp2kbrew.typing import Box, npf64


def convert_to_box_matrix(box, *, dtype=npf64, dim: int = 3) -> Box:
    box = np.asarray(box).astype(dtype=dtype)
    if not box.size:
        return box
    ndim = box.ndim
    shape = box.shape
    if ndim == 0:
        return np.eye(dim) * box
    elif ndim == 1 and shape[0] == dim:
        return np.diag(box)
    elif ndim == 2 and shape == (dim, dim):
        return box
    else:
        raise ValueError(f"We can not diagonalize the box shape. {shape}")


def calculate_volume(box, *, dtype=npf64) -> npf64:
    a, b, c = convert_to_box_matrix(box=box, dtype=dtype)
    return np.cross(a, b) @ c
