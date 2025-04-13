from . import ErrorCode
from .api import is_error_code, record

__all__ = ["Record"]


class Record:
    def __init__(self, native_record_obj: int) -> None:
        self._obj: int = native_record_obj

    @property
    def sectionLength(self) -> int:
        return record.get_section_length(self._obj)

    @sectionLength.setter
    def sectionLength(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(record.set_section_length(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set sectionLength is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def sectionCount(self) -> int:
        return record.get_section_count(self._obj)

    @sectionCount.setter
    def sectionCount(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(record.set_section_count(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set sectionCount is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def cycles(self) -> int:
        return record.get_cycles(self._obj)

    @cycles.setter
    def cycles(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(record.set_cycles(self._obj, value))
        if is_error_code(ret):
            raise ValueError(f"set cycles is failed, the error code is 0x{ret.value:X}")
