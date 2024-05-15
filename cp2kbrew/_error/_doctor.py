import numpy as np
from cp2kbrew._error._errorcodes import errorcodes_library
from cp2kbrew._opener import Opener


class Doctor:
    def __init__(self, opener: Opener) -> None:
        self._errocode_library = {name: errorcode(opener=opener) for name, errorcode in errorcodes_library.items()}
        self._errorcodes = []
        self.openers = opener.openers

    def __len__(self) -> int:
        return len(self._errorcodes)

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def errorcodes(self) -> list[str]:
        return self._errorcodes

    @property
    def support_errocodes_keys(self) -> list[str]:
        return list(self._errocode_library.keys())

    def decode_errorcode(self, errorcode: str) -> str:
        return self._errocode_library.get(errorcode).error

    def check(self, *, verbose: bool = False) -> None:
        self._errorcodes = []
        for errorcode, errcodes in self._errocode_library.items():
            if errcodes.check():
                self.report_error(errorcode=errorcode, verbose=verbose)

    def report_error(self, errorcode: str, *, verbose: bool = True) -> None:
        assert errorcode in self.support_errocodes_keys, KeyError(f"reported error should be in {self.support_errocodes_keys}")
        error = self._errocode_library[errorcode].error
        if verbose:
            print(f"[E.REPORT]: {errorcode}({error})")
        self._errorcodes.append(errorcode)

    def fix(self, errorcode: str) -> None:
        assert errorcode in self.support_errocodes_keys, KeyError(f"Not Supported errorcode({errorcode})")
        cls_errorcode = self._errocode_library.get(errorcode)
        cls_errorcode.fix()
