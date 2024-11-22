# -*- coding:utf-8 -*-
from _ctypes import Array
from typing import Any

from advantech_daq import (
    AISignalType,
    AccessMode,
    ActiveSignal,
    AIChannelType,
    BaudRate,
    BurnoutRetType,
    CodingType,
    ControlState,
    CounterCapability,
    CounterCascadeGroup,
    CountingType,
    CouplingType,
    Depository,
    DIOPortDir,
    DOCircuitType,
    ErrorRetType,
    EventId,
    FilterType,
    FreqMeasureMethod,
    IEPEType,
    ImpedanceType,
    OutSignalType,
    ProductId,
    SamplingMethod,
    SignalDrop,
    SignalPolarity,
    TerminalBoard,
    TriggerAction,
    ValueRange,
)

__all__ = [
    "create_array",
    "toAISignalType",
    "toAccessMode",
    "toActiveSignal",
    "toAiChannelType",
    "toBaudRate",
    "toBurnoutRetType",
    "toCodingType",
    "toControlState",
    "toCounterCapability",
    "toCounterCascadeGroup",
    "toCountingType",
    "toCouplingType",
    "toDepository",
    "toDioPortDir",
    "toDoCircuitType",
    "toErrorRetType",
    "toEventId",
    "toFilterType",
    "toFreqMeasureMethod",
    "toIEPEType",
    "toImpedanceType",
    "toOutSignalType",
    "toProductId",
    "toSamplingMethod",
    "toSignalDrop",
    "toSignalPolarity",
    "toTerminalBoard",
    "toTriggerAction",
    "toValueRange",
    "to_enum_item",
]


def create_array[T](dtype: type[T], num: int) -> Array[T]:
    return (dtype * num)()


def to_enum_item[T](enum_type: type[T], value: Any) -> T:
    if value not in enum_type:
        raise ValueError(f"{enum_type.__name__} has no {value!r}")
    return enum_type(value)


def toAccessMode(value: int) -> AccessMode:
    return to_enum_item(enum_type=AccessMode, value=value)


def toControlState(value: int) -> ControlState:
    return to_enum_item(enum_type=ControlState, value=value)


def toProductId(value: int) -> ProductId:
    return to_enum_item(enum_type=ProductId, value=value)


def toTerminalBoard(value: int) -> TerminalBoard:
    return to_enum_item(enum_type=TerminalBoard, value=value)


def toDepository(value: int) -> Depository:
    return to_enum_item(enum_type=Depository, value=value)


def toAiChannelType(value: int) -> AIChannelType:
    return to_enum_item(enum_type=AIChannelType, value=value)


def toAISignalType(value: int) -> AISignalType:
    return to_enum_item(enum_type=AISignalType, value=value)


def toValueRange(value: int) -> ValueRange:
    return to_enum_item(enum_type=ValueRange, value=value)


def toSamplingMethod(value: int) -> SamplingMethod:
    return to_enum_item(enum_type=SamplingMethod, value=value)


def toFilterType(value: int) -> FilterType:
    return to_enum_item(enum_type=FilterType, value=value)


def toBurnoutRetType(value: int) -> BurnoutRetType:
    return to_enum_item(enum_type=BurnoutRetType, value=value)


def toSignalDrop(value: int) -> SignalDrop:
    return to_enum_item(enum_type=SignalDrop, value=value)


def toSignalPolarity(value: int) -> SignalPolarity:
    return to_enum_item(enum_type=SignalPolarity, value=value)


def toTriggerAction(value: int) -> TriggerAction:
    return to_enum_item(enum_type=TriggerAction, value=value)


def toActiveSignal(value: int) -> ActiveSignal:
    return to_enum_item(enum_type=ActiveSignal, value=value)


def toDioPortDir(value: int) -> DIOPortDir:
    return to_enum_item(enum_type=DIOPortDir, value=value)


def toDoCircuitType(value: int) -> DOCircuitType:
    return to_enum_item(enum_type=DOCircuitType, value=value)


def toEventId(value: int) -> EventId:
    return to_enum_item(enum_type=EventId, value=value)


def toCounterCapability(value: int) -> CounterCapability:
    return to_enum_item(enum_type=CounterCapability, value=value)


def toCounterCascadeGroup(value: int) -> CounterCascadeGroup:
    return to_enum_item(enum_type=CounterCascadeGroup, value=value)


def toFreqMeasureMethod(value: int) -> FreqMeasureMethod:
    return to_enum_item(enum_type=FreqMeasureMethod, value=value)


def toCountingType(value: int) -> CountingType:
    return to_enum_item(enum_type=CountingType, value=value)


def toOutSignalType(value: int) -> OutSignalType:
    return to_enum_item(enum_type=OutSignalType, value=value)


def toCouplingType(value: int) -> CouplingType:
    return to_enum_item(enum_type=CouplingType, value=value)


def toIEPEType(value: int) -> IEPEType:
    return to_enum_item(enum_type=IEPEType, value=value)


def toImpedanceType(value: int) -> ImpedanceType:
    return to_enum_item(enum_type=ImpedanceType, value=value)


def toBaudRate(value: int) -> BaudRate:
    return to_enum_item(enum_type=BaudRate, value=value)


def toCodingType(value: int) -> CodingType:
    return to_enum_item(enum_type=CodingType, value=value)


def toErrorRetType(value: int) -> ErrorRetType:
    return to_enum_item(enum_type=ErrorRetType, value=value)
