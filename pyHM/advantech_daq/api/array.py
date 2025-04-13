from ctypes import POINTER, c_byte, c_int, c_int32, c_int64, cast
from typing import Callable

from . import c_uint_, dll
from .. import (
    AISignalType,
    AccessMode,
    ActiveSignal,
    BurnoutRetType,
    CounterCapability,
    CounterCascadeGroup,
    CountingType,
    CouplingType,
    DeviceTreeNode,
    DOCircuitType,
    EventId,
    FilterType,
    FreqMeasureMethod,
    IEPEType,
    ImpedanceType,
    OutSignalType,
    SignalDrop,
    SignalPolarity,
    TerminalBoard,
    TriggerAction,
    ValueRange,
    utils,
)

__all__ = [
    "dispose",
    "get_item",
    "get_length",
    "to_access_mode",
    "to_active_signal",
    "to_ai_signal_type",
    "to_burnout_ret_type",
    "to_byte",
    "to_counter_capability",
    "to_counter_cascade_group",
    "to_counting_type",
    "to_coupling_type",
    "to_device_tree_node",
    "to_do_circuit_type",
    "to_enum",
    "to_event_id",
    "to_filter_type",
    "to_freq_measure_method",
    "to_iepe_type",
    "to_impedance_type",
    "to_int32",
    "to_int64",
    "to_out_signal_type",
    "to_signal_drop",
    "to_signal_polarity",
    "to_simple_type",
    "to_terminal_board",
    "to_trigger_action",
    "to_value_range",
]


def to_simple_type[_CT, T2](
    dtype: type[_CT], TArrayObj: int, auto_free: bool
) -> list[T2]:
    if TArrayObj == 0 or get_length(TArrayObj) == 0:
        return []
    count: int = get_length(TArrayObj)
    arr: list[T2] = []
    for i in range(count):
        item: int = get_item(TArrayObj, i)
        int_obj: _CT = cast(item, POINTER(dtype)).contents
        arr.append(int_obj.value)

    if auto_free:
        dispose(TArrayObj)
    return arr


def to_int32(TArrayObj: int, auto_free: bool) -> list[int]:
    return to_simple_type(c_int32, TArrayObj, auto_free)


def to_int64(TArrayObj: int, auto_free: bool) -> list[int]:
    return to_simple_type(c_int64, TArrayObj, auto_free)


def to_byte(TArrayObj: int, auto_free: bool) -> list[int]:
    return to_simple_type(c_byte, TArrayObj, auto_free)


def dispose(TArrayObj: int) -> None:
    dll.TArray_Dispose.argtypes = [c_uint_]
    dll.TArray_Dispose(TArrayObj)


def get_length(TArrayObj: int) -> int:
    dll.TArray_getLength.argtypes = [c_uint_]
    dll.TArray_getLength.restype = c_int32
    return dll.TArray_getLength(TArrayObj)


def get_item(TArrayObj: int, index: int) -> int:
    dll.TArray_getItem.argtypes = [c_uint_, c_int32]
    dll.TArray_getItem.restype = c_uint_
    return dll.TArray_getItem(TArrayObj, index)


def to_device_tree_node(
    native_array: int, auto_free: bool = True
) -> list[DeviceTreeNode]:
    count: int = get_length(native_array)
    device_tree_node_list: list[DeviceTreeNode] = []
    for i in range(count):
        item = get_item(native_array, i)
        device_tree_node_obj_save: DeviceTreeNode = DeviceTreeNode()
        device_tree_node_obj: DeviceTreeNode = cast(
            item, POINTER(DeviceTreeNode)
        ).contents

        device_tree_node_obj_save.DeviceNumber = device_tree_node_obj.DeviceNumber
        device_tree_node_obj_save.Description = device_tree_node_obj.Description
        for j in range(8):
            device_tree_node_obj_save.ModulesIndex[j] = (
                device_tree_node_obj.ModulesIndex[j]
            )

        device_tree_node_list.append(device_tree_node_obj_save)
        del device_tree_node_obj
    if auto_free:
        dispose(native_array)
    return device_tree_node_list


def to_enum[T](
    p_array_obj: int, auto_free: bool, convert: Callable[[int], T]
) -> list[T]:
    if p_array_obj == 0:
        return []
    count: int = get_length(p_array_obj)
    data_list: list[T] = []
    for i in range(count):
        item = get_item(p_array_obj, i)
        enum_value = cast(item, POINTER(c_int)).contents.value
        # cast to enum
        enum_obj: T = convert(enum_value)
        data_list.append(enum_obj)
    if auto_free:
        dispose(p_array_obj)
    return data_list


def to_terminal_board(native_array: int, auto_free: bool) -> list[TerminalBoard]:
    return to_enum(native_array, auto_free, utils.toTerminalBoard)


def to_event_id(native_array: int, auto_free: bool) -> list[EventId]:
    return to_enum(native_array, auto_free, utils.toEventId)


def to_access_mode(native_array: int, auto_free: bool) -> list[AccessMode]:
    return to_enum(native_array, auto_free, utils.toAccessMode)


def to_value_range(native_array: int, auto_free: bool) -> list[ValueRange]:
    return to_enum(native_array, auto_free, utils.toValueRange)


def to_ai_signal_type(native_array: int, auto_free: bool) -> list[AISignalType]:
    return to_enum(native_array, auto_free, utils.toAISignalType)


def to_burnout_ret_type(native_array: int, auto_free: bool) -> list[BurnoutRetType]:
    return to_enum(native_array, auto_free, utils.toBurnoutRetType)


def to_filter_type(native_array: int, auto_free: bool) -> list[FilterType]:
    return to_enum(native_array, auto_free, utils.toFilterType)


def to_signal_drop(native_array: int, auto_free: bool) -> list[SignalDrop]:
    return to_enum(native_array, auto_free, utils.toSignalDrop)


def to_active_signal(native_array: int, auto_free: bool) -> list[ActiveSignal]:
    return to_enum(native_array, auto_free, utils.toActiveSignal)


def to_trigger_action(native_array: int, auto_free: bool) -> list[TriggerAction]:
    return to_enum(native_array, auto_free, utils.toTriggerAction)


def to_counter_capability(
    native_array: int, auto_free: bool
) -> list[CounterCapability]:
    return to_enum(native_array, auto_free, utils.toCounterCapability)


def to_signal_polarity(native_array: int, auto_free: bool) -> list[SignalPolarity]:
    return to_enum(native_array, auto_free, utils.toSignalPolarity)


def to_out_signal_type(native_array: int, auto_free: bool) -> list[OutSignalType]:
    return to_enum(native_array, auto_free, utils.toOutSignalType)


def to_freq_measure_method(
    native_array: int, auto_free: bool
) -> list[FreqMeasureMethod]:
    return to_enum(native_array, auto_free, utils.toFreqMeasureMethod)


def to_counter_cascade_group(
    native_array: int, auto_free: bool
) -> list[CounterCascadeGroup]:
    return to_enum(native_array, auto_free, utils.toCounterCascadeGroup)


def to_counting_type(native_array: int, auto_free: bool) -> list[CountingType]:
    return to_enum(native_array, auto_free, utils.toCountingType)


def to_coupling_type(native_array: int, auto_free: bool) -> list[CouplingType]:
    return to_enum(native_array, auto_free, utils.toCouplingType)


def to_iepe_type(native_array: int, auto_free: bool) -> list[IEPEType]:
    return to_enum(native_array, auto_free, utils.toIEPEType)


def to_impedance_type(native_array: int, auto_free: bool) -> list[ImpedanceType]:
    return to_enum(native_array, auto_free, utils.toImpedanceType)


def to_do_circuit_type(native_array: int, auto_free: bool) -> list[DOCircuitType]:
    return to_enum(native_array, auto_free, utils.toDoCircuitType)
