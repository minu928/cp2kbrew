import os
from pathlib import Path
from abc import ABCMeta, abstractmethod

import numpy as np
from mdbrew import MDState, MDStateAttr

from cp2kbrew.handler import stack
from cp2kbrew.typing import FilePath


__all__ = ["writers", "Writer", "DeePMDNPYWriter", "TrjEXTXYZWriter"]


class Writer(metaclass=ABCMeta):
    def __repr__(self) -> str:
        return self.fmt

    def __init_subclass__(cls):
        registry[cls.fmt] = cls

    @property
    @abstractmethod
    def fmt(self) -> str:
        pass

    @property
    @abstractmethod
    def querylist(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def write(cls, path: FilePath, mdstates: list[MDState], *, querylist: list[MDStateAttr] = None, **kwargs):
        pass


registry: dict[str, Writer] = {}


class DeePMDNPYWriter(Writer):
    fmt = "deepmd@npy"
    querylist = ("force", "energy", "virial", "atom", "coord", "box")

    @classmethod
    def write(cls, path: FilePath, mdstates: list[MDState], *, querylist: list[MDStateAttr] = None, **kwargs):
        querylist = querylist or cls.querylist
        exist_ok = kwargs.get("exist_ok", False)
        os.makedirs(Path(path), exist_ok=exist_ok)
        save_path = os.path.join(path, "set.000")
        os.makedirs(save_path, exist_ok=exist_ok)
        for queryname in querylist:
            querydata = stack(mdstates, what=queryname)
            if queryname == "atom":
                atom_order = kwargs.get("atom_order", None)
                atom_order = np.unique(querydata) if atom_order is None else atom_order
                np.savetxt(os.path.join(path, "type_map.raw"), atom_order, fmt="%s")
                atom_dict = {element: i for i, element in enumerate(atom_order)}
                firstframe_atom = querydata[0]
                assert np.all([dat == firstframe_atom for dat in querydata[1:]]), "Not All Frame Atom is not Same"
                type_raw_data = np.vectorize(atom_dict.__getitem__)(firstframe_atom)
                np.savetxt(os.path.join(path, "type.raw"), type_raw_data, fmt="%d")
            else:
                nframe = len(querydata)
                if queryname != "energy":
                    querydata = querydata.reshape(nframe, -1)
                np.save(os.path.join(save_path, queryname), querydata)


class TrjEXTXYZWriter(Writer):
    fmt = "trj@extxyz"
    querylist = ("force", "energy", "stress", "atom", "coord", "box")

    @classmethod
    def write(cls, path: FilePath, mdstates: list[MDState], *, querylist: list[MDStateAttr] = None, **kwargs):
        querylist = querylist or cls.querylist
        fmt = kwargs.get("fmt", "%.8s")
        config = {
            "line": f"Properties=species:S:1:pos:R:3",
            "data": ["atom", "coord"],
            "fmt": f"{fmt} {fmt} {fmt} {fmt}",
        }
        if "force" in querylist:
            config["line"] += ":forces:R:3"
            config["data"].append("force")
            config["fmt"] += f" {fmt} {fmt} {fmt}"

        with Path(path).open(mode=kwargs.get("mode", "w")) as f:
            for framedata in mdstates:
                natoms = len(framedata.atom)
                f.writelines(f"\t{natoms}\n")

                # * Info Line
                infoline = ""
                if "energy" in querylist:
                    infoline += f'energy="{framedata.energy}" '
                if "box" in querylist:
                    infoline += f'Lattice="{" ".join(framedata.box.flatten().astype(str))}" '
                if "virial" in querylist:
                    infoline += f'virial="{" ".join(framedata.virial.flatten().astype(str))}" '
                if "stress" in querylist:
                    infoline += f'stress="{" ".join(framedata.stress.flatten().astype(str))}" '
                infoline += config["line"] + ' pbc="T T T" \n'
                f.writelines(infoline)

                property_data = np.concatenate([getattr(framedata, what) for what in config["data"]], axis=-1)
                np.savetxt(f, property_data, fmt=config["fmt"])
