import os
import numpy as np
from copy import deepcopy
from abc import ABCMeta, abstractmethod


class SaveInterface(metaclass=ABCMeta):
    _alias = {"cell": ("box", "boxes", "cells")}

    def __init__(self, *, requests_list: list[str] = None) -> None:
        self._requests_list = self._assign_requests_list(requests_list=requests_list)
        self.unit = deepcopy(self._default_units)

    @property
    @abstractmethod
    def _default_units(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def _default_requests_list(self) -> list[str]:
        pass

    @property
    def requests_list(self) -> list[str]:
        return self._requests_list

    @requests_list.setter
    def request_list(self, requests_list: list[str]):
        self._requests_list = requests_list

    def _assign_requests_list(self, requests_list: list[str]):
        return self._default_requests_list if requests_list is None else requests_list

    def find_alias(self, what: str):
        for key, alias_list in self._alias.items():
            if what in alias_list:
                return key
        raise KeyError(f"{what} is not a supported keys")

    def save(
        self,
        obj,
        *,
        path: str = "./",
        request_list: list = None,
        element_order: list = None,
        unit: dict[str, str] = None,
    ) -> None:

        request_list = self.request_list if request_list is None else request_list
        if unit is not None and not hasattr(obj, "convert_unit"):
            raise ValueError(f"Unit Conversion Failed: obj not has attribute 'convert_unit'")
        unit = self.unit if unit is None else unit
        obj.convert_unit(to=unit)
        for requests_name in self.request_list:
            requests_name = self.find_alias(what=requests_name) if not hasattr(obj, requests_name) else requests_name
            attr = getattr(obj, requests_name)
            self._save_interface(path=path, requests_name=requests_name, attr=attr, element_order=element_order)

    @abstractmethod
    def _save_interface(self, path: str, requests_name: str, attr: type[np.ndarray]) -> None:
        pass
