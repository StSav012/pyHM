from . import (
    ActiveSignal,
    ErrorCode,
    FilterType,
    SignalDrop,
    TriggerAction,
    utils,
)
from .api import is_error_code, trigger

__all__ = ["Trigger"]


class Trigger:
    def __init__(self, native_trig_obj: int):
        self._obj: int = native_trig_obj

    @property
    def source(self) -> SignalDrop:
        return utils.toSignalDrop(trigger.get_source(self._obj))

    @source.setter
    def source(self, value: SignalDrop) -> None:
        if not isinstance(value, SignalDrop):
            raise TypeError("a SignalDrop is required")
        ret: ErrorCode = ErrorCode.lookup(trigger.set_source(self._obj, value.value))
        if is_error_code(ret):
            raise ValueError(f"set source is failed, the error code is 0x{ret.value:X}")

    @property
    def edge(self) -> ActiveSignal:
        return utils.toActiveSignal(trigger.get_edge(self._obj))

    @edge.setter
    def edge(self, value: ActiveSignal) -> None:
        if not isinstance(value, ActiveSignal):
            raise TypeError("a ActiveSignal is required")
        ret: ErrorCode = ErrorCode.lookup(trigger.set_edge(self._obj, value.value))
        if is_error_code(ret):
            raise ValueError(f"set edge is failed, the error code is 0x{ret.value:X}")

    @property
    def level(self) -> float:
        return trigger.get_level(self._obj)

    @level.setter
    def level(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(trigger.set_level(self._obj, value))
        if is_error_code(ret):
            raise ValueError(f"set level is failed, the error code is 0x{ret.value:X}")

    @property
    def action(self) -> TriggerAction:
        return utils.toTriggerAction(trigger.get_action(self._obj))

    @action.setter
    def action(self, value: TriggerAction) -> None:
        if not isinstance(value, TriggerAction):
            raise TypeError("a TriggerAction is required")
        ret: ErrorCode = ErrorCode.lookup(trigger.set_action(self._obj, value.value))
        if is_error_code(ret):
            raise ValueError(f"set action is failed, the error code is 0x{ret.value:X}")

    @property
    def delayCount(self) -> int:
        return trigger.get_delay_count(self._obj)

    @delayCount.setter
    def delayCount(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(trigger.set_delay_count(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set delayCount is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def hysteresisIndex(self) -> float:
        return trigger.get_hysteresis_index(self._obj)

    @hysteresisIndex.setter
    def hysteresisIndex(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            trigger.set_hysteresis_index(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set hysteresisIndex is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def filterType(self) -> FilterType:
        return utils.toFilterType(trigger.get_filter_type(self._obj))

    @filterType.setter
    def filterType(self, value: FilterType) -> None:
        if not isinstance(value, FilterType):
            raise TypeError("a FilterType is required")
        ret: ErrorCode = ErrorCode.lookup(
            trigger.set_filter_type(self._obj, value.value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set filterType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def filterCutoffFreq(self) -> float:
        return trigger.get_filter_cutoff_freq(self._obj)

    @filterCutoffFreq.setter
    def filterCutoffFreq(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            trigger.set_filter_cutoff_freq(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set filterCutoffFreq is failed, the error code is 0x{ret.value:X}"
            )
