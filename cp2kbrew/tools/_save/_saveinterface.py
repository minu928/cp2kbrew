from copy import deepcopy
from abc import ABCMeta, abstractmethod
from numpy.typing import NDArray


class SaveInterface(metaclass=ABCMeta):
    def __init__(self, *, querylist: list[str] = None) -> None:
        self._querylist = querylist or self._default_querylist
        self.unit = deepcopy(self._default_units)

    def __init_subclass__(cls) -> None:
        saver_dict[cls.fmt] = cls

    @property
    @abstractmethod
    def fmt(self) -> str:
        pass

    @property
    @abstractmethod
    def _default_units(self) -> dict[str, str]:
        pass

    @property
    @abstractmethod
    def _default_querylist(self) -> list[str]:
        pass

    @property
    def querylist(self) -> list[str]:
        return self._querylist

    @querylist.setter
    def querylist(self, querylist: list[str]):
        self._querylist = querylist

    @abstractmethod
    def save(self, savepath: str, query_data: dict[str, NDArray], **kwrgs) -> None:
        pass


saver_dict: dict[str, type[SaveInterface]] = {}
