# coding=utf-8
from ctypes import Structure, c_double, c_int32, c_int64, c_uint8, c_wchar
from enum import Enum, IntEnum
from typing import Any

__all__ = [
    "DAQ_NAVI_VER",
    "MAX_AI_CH_COUNT",
    "MAX_AO_CH_COUNT",
    "MAX_CNTR_CH_COUNT",
    "MAX_DEVICE_DESC_LEN",
    "MAX_DIO_PORT_COUNT",
    "MAX_DIO_TRIG_COUNT",
    "MAX_SIG_DROP_DESC_LEN",
    "MAX_TRIG_COUNT",
    "MAX_VRG_DESC_LEN",
    "AccessMode",
    "ActiveSignal",
    "AIChannelType",
    "AISignalType",
    "BaudRate",
    "BfdAIEventArgs",
    "BfdAOEventArgs",
    "BfdCntrEventArgs",
    "BfdDIEventArgs",
    "BfdDOEventArgs",
    "BurnoutRetType",
    "CntrEventArgs",
    "CodingType",
    "ControlState",
    "CounterCapability",
    "CounterCascadeGroup",
    "CounterOperationMode",
    "CounterValueRegister",
    "CountingType",
    "CouplingType",
    "DataMark",
    "Depository",
    "DeviceEventArgs",
    "DeviceInformation",
    "DeviceTreeNode",
    "DiSnapEventArgs",
    "DIOPortDir",
    "DIOPortType",
    "DOCircuitType",
    "ErrorCode",
    "ErrorRetType",
    "EventId",
    "FilterType",
    "FreqMeasureMethod",
    "FwAction",
    "IEPEType",
    "ImpedanceType",
    "MapFuncPiece",
    "MathInterval",
    "MathIntervalType",
    "ModuleType",
    "OutSignalType",
    "ProductId",
    "PulseWidth",
    "SamplingMethod",
    "Scenario",
    "SignalDrop",
    "SignalPolarity",
    "SignalPosition",
    "TemperatureDegree",
    "TerminalBoard",
    "TriggerAction",
    "UdCntrEventArgs",
    "ValueRange",
    "ValueUnit",
]

DAQ_NAVI_VER = 0x400

MAX_DEVICE_DESC_LEN = 64
MAX_VRG_DESC_LEN = 256
MAX_SIG_DROP_DESC_LEN = 256

MAX_AI_CH_COUNT = 128
MAX_AO_CH_COUNT = 128
MAX_DIO_PORT_COUNT = 32
MAX_CNTR_CH_COUNT = 8
MAX_TRIG_COUNT = 4
MAX_DIO_TRIG_COUNT = 2


class TerminalBoard(IntEnum):
    WiringBoard = 0
    PCLD8710 = 1
    PCLD789 = 2
    PCLD8115 = 3


class ModuleType(IntEnum):
    DaqGroup = 1
    DaqDevice = 2
    DaqAi = 3
    DaqAo = 4
    DaqDio = 5
    DaqCounter = 6
    DaqCali = 7
    DaqFw = 8
    DaqAny = -1


class FwAction(IntEnum):
    FwNormal = 1
    FwMandatory = 2

    FwAbort = -1


class AccessMode(IntEnum):
    ModeRead = 0
    ModeWrite = 1
    ModeWriteWithReset = 2
    ModeWriteShared = 3


class Depository(IntEnum):
    DepositoryNone = 0
    DepositoryOnSystem = 1
    DepositoryOnDevice = 2


class MathIntervalType(IntEnum):
    # Right boundary definition, define the maximum value state, use the bit 0,1
    RightOpenSet = (0x0,)  # No maximum value limitation.
    RightClosedBoundary = (0x1,)  # The maximum value is included.
    RightOpenBoundary = (0x2,)  # The maximum value is not included.

    # Left boundary definition, define the minimum value state, used the bit 2, 3
    LeftOpenSet = (0x0,)  # No minimum value limitation.
    LeftClosedBoundary = (0x4,)  # The minimum value is included.
    LeftOpenBoundary = (0x8,)  # The minimum value is not included

    # The signality expression
    Boundless = (0x0,)  # Boundless set. (LeftOpenSet | RightOpenSet)

    # The combination notation
    LOSROS = (0x0,)  # (LeftOpenSet | RightOpenSet), algebra notation: (un-limit, max)
    LOSRCB = (
        0x1,
    )  # (LeftOpenSet | RightClosedBoundary), algebra notation: (un-limit, max ]
    LOSROB = (
        0x2,
    )  # (LeftOpenSet | RightOpenBoundary), algebra notation: (un-limit, max)

    LCBROS = (
        0x4,
    )  # (LeftClosedBoundary | RightOpenSet), algebra notation: [min, un-limit)
    LCBRCB = (
        0x5,
    )  # (LeftClosedBoundary | RightClosedBoundary), algebra notation: [ min, right ]
    LCBROB = (
        0x6,
    )  # (LeftClosedBoundary | RightOpenBoundary), algebra notation: [ min, right)

    LOBROS = (
        0x8,
    )  # (LeftOpenBoundary | RightOpenSet), algebra notation: (min, un-limit)
    LOBRCB = (
        0x9,
    )  # (LeftOpenBoundary | RightClosedBoundary), algebra notation: (min, right ]
    LOBROB = (
        0xA,
    )  # (LeftOpenBoundary | RightOpenBoundary), algebra notation: (min, right)


class AIChannelType(IntEnum):
    AllSingleEnded = 0
    AllDifferential = 1
    AllSeDiffAdj = 2
    MixedSeDiffAdj = 3


class AISignalType(IntEnum):
    SingleEnded = 0
    Differential = 1
    PseudoDifferential = 2


class CouplingType(IntEnum):
    DCCoupling = 0
    ACCoupling = 1


class ImpedanceType(IntEnum):
    Impedance1MOmh = 0
    Impedance50Omh = 1


class IEPEType(IntEnum):
    IEPENone = 0
    IEPE4mA = 1
    IEPE10mA = 2
    IEPE2mA = 3


class FilterType(IntEnum):
    NoFilter = 0
    LowPass = 1
    HighPass = 2
    BandPass = 3
    BandStop = 4


class DIOPortType(IntEnum):
    PortDI = 0  # the port number references to a DI port
    PortDO = 1  # the port number references to a DO port
    PortDIO = 2  # the port number references to a DI port and a DO port
    Port8255A = 3  # the port number references to a PPI port A mode DIO port.
    Port8255C = 4  # the port number references to a PPI port C mode DIO port.
    PortIndvdlDIO = 5  # the port number references to a port whose each channel can be configured as in or out.


class DIOPortDir(IntEnum):
    Input = 0x00
    LOutHIn = 0x0F
    LInHOut = 0xF0
    Output = 0xFF


class DOCircuitType(IntEnum):
    TTL = 0
    Sink = 1
    Source = 2
    Relay = 3


class SamplingMethod(IntEnum):
    EqualTimeSwitch = 0
    Simultaneous = 1


class TemperatureDegree(IntEnum):
    Celsius = 0
    Fahrenheit = 1
    Rankine = 2
    Kelvin = 3


class BurnoutRetType(IntEnum):
    Current = 0
    ParticularValue = 1
    UpLimit = 2
    LowLimit = 3
    LastCorrectValue = 4


class ValueUnit(IntEnum):
    Kilovolt = 0  # KV
    Volt = 1  # V
    MilliVolt = 2  # mV
    MicroVolt = 3  # uV
    KiloAmpere = 4  # KA
    Ampere = 5  # A
    MilliAmpere = 6  # mA
    MicroAmpere = 7  # uA
    CelsiusUnit = 8  # Celsius


class ValueRange(IntEnum):
    V_OMIT = -1  # Unknown when `get`, ignored when `set`
    V_Neg15To15 = 0  # +/- 15 V
    V_Neg10To10 = 1  # +/- 10 V
    V_Neg5To5 = 2  # +/- 5 V
    V_Neg2pt5To2pt5 = 3  # +/- 2.5 V
    V_Neg1pt25To1pt25 = 4  # +/- 1.25 V
    V_Neg1To1 = 5  # +/- 1 V

    V_0To15 = 6  # 0~15 V
    V_0To10 = 7  # 0~10 V
    V_0To5 = 8  # 0~5 V
    V_0To2pt5 = 9  # 0~2.5 V
    V_0To1pt25 = 10  # 0~1.25 V
    V_0To1 = 11  # 0~1 V

    mV_Neg625To625 = 12  # +/- 625mV
    mV_Neg500To500 = 13  # +/- 500 mV
    mV_Neg312pt5To312pt5 = 14  # +/- 312.5 mV
    mV_Neg200To200 = 15  # +/- 200 mV
    mV_Neg150To150 = 16  # +/- 150 mV
    mV_Neg100To100 = 17  # +/- 100 mV
    mV_Neg50To50 = 18  # +/- 50 mV
    mV_Neg30To30 = 19  # +/- 30 mV
    mV_Neg20To20 = 20  # +/- 20 mV
    mV_Neg15To15 = 21  # +/- 15 mV
    mV_Neg10To10 = 22  # +/- 10 mV
    mV_Neg5To5 = 23  # +/- 5 mV

    mV_0To625 = 24  # 0 ~ 625 mV
    mV_0To500 = 25  # 0 ~ 500 mV
    mV_0To150 = 26  # 0 ~ 150 mV
    mV_0To100 = 27  # 0 ~ 100 mV
    mV_0To50 = 28  # 0 ~ 50 mV
    mV_0To20 = 29  # 0 ~ 20 mV
    mV_0To15 = 30  # 0 ~ 15 mV
    mV_0To10 = 31  # 0 ~ 10 mV

    mA_Neg20To20 = 32  # +/- 20mA
    mA_0To20 = 33  # 0 ~ 20 mA
    mA_4To20 = 34  # 4 ~ 20 mA
    mA_0To24 = 35  # 0 ~ 24 mA

    # For USB4702_4704
    V_Neg2To2 = 36  # +/- 2 V
    V_Neg4To4 = 37  # +/- 4 V
    V_Neg20To20 = 38  # +/- 20 V

    JType_0To760C = 0x8000  # T/C J type 0~760 'C
    KType_0To1370C = 0x8001  # T/C K type 0~1370 'C
    TType_Neg100To400C = 0x8002  # T/C T type -100~400 'C
    EType_0To1000C = 0x8003  # T/C E type 0~1000 'C
    RType_500To1750C = 0x8004  # T/C R type 500~1750 'C
    SType_500To1750C = 0x8005  # T/C S type 500~1750 'C
    BType_500To1800C = 0x8006  # T/C B type 500~1800 'C

    Pt392_Neg50To150 = 0x8007  # Pt392 -50~150 'C
    Pt385_Neg200To200 = 0x8008  # Pt385 -200~200 'C
    Pt385_0To400 = 0x8009  # Pt385 0~400 'C
    Pt385_Neg50To150 = 0x800A  # Pt385 -50~150 'C
    Pt385_Neg100To100 = 0x800B  # Pt385 -100~100 'C
    Pt385_0To100 = 0x800C  # Pt385 0~100 'C
    Pt385_0To200 = 0x800D  # Pt385 0~200 'C
    Pt385_0To600 = 0x800E  # Pt385 0~600 'C
    Pt392_Neg100To100 = 0x800F  # Pt392 -100~100 'C
    Pt392_0To100 = 0x8010  # Pt392 0~100 'C
    Pt392_0To200 = 0x8011  # Pt392 0~200 'C
    Pt392_0To600 = 0x8012  # Pt392 0~600 'C
    Pt392_0To400 = 0x8013  # Pt392 0~400 'C
    Pt392_Neg200To200 = 0x8014  # Pt392 -200~200 'C
    Pt1000_Neg40To160 = 0x8015  # Pt1000 -40~160 'C

    Balcon500_Neg30To120 = 0x8016  # Balcon500 -30~120 'C

    Ni518_Neg80To100 = 0x8017  # Ni518 -80~100 'C
    Ni518_0To100 = 0x8018  # Ni518 0~100 'C
    Ni508_0To100 = 0x8019  # Ni508 0~100 'C
    Ni508_Neg50To200 = 0x801A  # Ni508 -50~200 'C

    Thermistor_3K_0To100 = 0x801B  # Thermistor 3K 0~100 'C
    Thermistor_10K_0To100 = 0x801C  # Thermistor 10K 0~100 'C

    JType_Neg210To1200C = 0x801D  # T/C J type -210~1200 'C
    KType_Neg270To1372C = 0x801E  # T/C K type -270~1372 'C
    TType_Neg270To400C = 0x801F  # T/C T type -270~400 'C
    EType_Neg270To1000C = 0x8020  # T/C E type -270~1000 'C
    RType_Neg50To1768C = 0x8021  # T/C R type -50~1768 'C
    SType_Neg50To1768C = 0x8022  # T/C S type -50~1768 'C
    BType_40To1820C = 0x8023  # T/C B type 40~1820 'C

    JType_Neg210To870C = 0x8024  # T/C J type -210~870 'C
    RType_0To1768C = 0x8025  # T/C R type 0~1768 'C
    SType_0To1768C = 0x8026  # T/C S type 0~1768 'C
    TType_Neg20To135C = 0x8027  # T/C T type -20~135 'C

    V_0To30 = 0x8028  # 0 ~ 30 V
    A_0To3 = 0x8029  # 0 ~ 3 A

    Pt100_Neg50To150 = 0x802A  # Pt100 -50~150 'C
    Pt100_Neg200To200 = 0x802B  # Pt100 -200~200 'C
    Pt100_0To100 = 0x802C  # Pt100 0~100 'C
    Pt100_0To200 = 0x802D  # Pt100 0~200 'C
    Pt100_0To400 = 0x802E  # Pt100 0~400 'C
    Btype_300To1820C = 0x802F  # T/C B type 300~1820 'C

    V_Neg12pt5To12pt5 = 0x8030  # +/- 12.5 V
    V_Neg6To6 = 0x8031  # +/- 6 V */
    V_Neg3To3 = 0x8032  # +/- 3 V */
    V_Neg1pt5To1pt5 = 0x8033  # +/- 1.5 V */
    mV_Neg750To750 = 0x8034  # +/- 750 mV */
    mV_Neg375To375 = 0x8035  # +/- 375 mV */
    mV_Neg187pt5To187pt5 = 0x8036  # +/- 187.5 mV */

    Pt100_385_3Wire = 0x8037  # Pt100     Mode:3 Wire     Type:0.385
    Pt100_385_24Wire = 0x8038  # Pt100     Mode:2/4 Wire   Type:0.385
    Pt100_392_3Wire = 0x8039  # Pt100     Mode:3 Wire     Type:0.392
    Pt100_392_24Wire = 0x803A  # Pt100     Mode:2/4 Wire   Type:0.392
    Pt1000_385_3Wire = 0x803B  # Pt1000    Mode:3 Wire     Type:0.385
    Pt1000_385_24Wire = 0x803C  # Pt1000    Mode:2/4 Wire   Type:0.385
    NiFe604_518_3Wire = 0x803D  # NiFe604   Mode:3 Wire     Type:0.518
    NiFe604_518_24Wire = 0x803E  # NiFe604   Mode:2/4 Wire   Type:0.518
    Balco500_518_3Wire = 0x803F  # Balco500  Mode:3 Wire     Type:0.518
    Balco500_518_24Wire = 0x8040  # Balco500  Mode:2/4 Wire   Type:0.518
    V_Neg12To12 = 0x8041  # +/- 12 V

    # 0xC000 ~ 0xF000 : user customized value range type
    UserCustomizedVrgStart = 0xC000
    UserCustomizedVrgEnd = 0xF000

    # AO external reference type
    V_ExternalRefBipolar = 0xF001  # External reference voltage unipolar
    V_ExternalRefUnipolar = 0xF002  # External reference voltage bipolar


class SignalPolarity(IntEnum):
    Negative = 0
    Positive = 1


class CountingType(IntEnum):
    CountingNone = 0
    DownCount = 1  # counter value decreases on each clock
    UpCount = 2  # counter value increases on each clock
    PulseDirection = 3  # counting direction is determined by two signals, one is clock, the other is direction signal
    TwoPulse = 4  # counting direction is determined by two signals, an up-counting, and a down-counting ones
    AbPhaseX1 = 5  # AB phase, 1x rate up/down counting
    AbPhaseX2 = 6  # AB phase, 2x rate up/down counting
    AbPhaseX4 = 7  # AB phase, 4x rate up/down counting


class OutSignalType(IntEnum):
    SignalOutNone = 0  # no output or output is 'disabled'
    ChipDefined = 1  # hardware chip defined
    NegChipDefined = 2  # hardware chip defined, negative logical
    PositivePulse = 3  # a low-to-high pulse
    NegativePulse = 4  # a high-to-low pulse
    ToggledFromLow = 5  # the level toggled from low to high
    ToggledFromHigh = 6  # the level toggled from high to low


class CounterCapability(IntEnum):
    Primary = 1
    InstantEventCount = 2
    OneShot = 3
    TimerPulse = 4
    InstantFreqMeter = 5
    InstantPwmIn = 6
    InstantPwmOut = 7
    UpDownCount = 8
    BufferedEventCount = 9
    BufferedPwmIn = 10
    BufferedPwmOut = 11
    BufferedUpDownCount = 12
    InstantEdgeSeparation = 13


class CounterOperationMode(IntEnum):
    C8254_M0 = 0  # 8254 mode 0, interrupt on terminal count
    C8254_M1 = 1  # 8254 mode 1, hardware retriggerable one-shot
    C8254_M2 = 2  # 8254 mode 2, rate generator
    C8254_M3 = 3  # 8254 mode 3, square save mode
    C8254_M4 = 4  # 8254 mode 4, software triggered strobe
    C8254_M5 = 5  # 8254 mode 5, hardware triggered strobe

    C1780_MA = 6  # Mode A level & pulse out, Software-Triggered without Hardware Gating
    C1780_MB = (
        7  # Mode B level & pulse out, Software-Triggered with Level Gating, = 8254_M0
    )
    C1780_MC = 8  # Mode C level & pulse out, Hardware-triggered strobe level
    C1780_MD = 9  # Mode D level & Pulse out, Rate generate with no hardware gating
    C1780_ME = 10  # Mode E level & pulse out, Rate generator with level Gating
    C1780_MF = 11  # Mode F level & pulse out, Non-retriggerable One-shot (Pulse type = 8254_M1)
    C1780_MG = 12  # Mode G level & pulse out, Software-triggered delayed pulse one-shot
    C1780_MH = 13  # Mode H level & pulse out, Software-triggered delayed pulse one-shot with hardware gating
    C1780_MI = 14  # Mode I level & pulse out, Hardware-triggered delay pulse strobe
    C1780_MJ = 15  # Mode J level & pulse out, Variable Duty Cycle Rate Generator with No Hardware Gating
    C1780_MK = 16  # Mode K level & pulse out, Variable Duty Cycle Rate Generator with Level Gating
    C1780_ML = 17  # Mode L level & pulse out, Hardware-Triggered Delayed Pulse One-Shot
    C1780_MO = (
        18  # Mode O level & pulse out, Hardware-Triggered Strobe with Edge Disarm
    )
    C1780_MR = (
        19  # Mode R level & pulse out, Non-Retriggerbale One-Shot with Edge Disarm
    )
    C1780_MU = 20  # Mode U level & pulse out, Hardware-Triggered Delayed Pulse Strobe with Edge Disarm
    C1780_MX = 21  # Mode X level & pulse out, Hardware-Triggered Delayed Pulse One-Shot with Edge Disarm


class CounterValueRegister(IntEnum):
    CntLoad = 0
    CntPreset = 0
    CntHold = 1
    CntOverCompare = 2
    CntUnderCompare = 3


class CounterCascadeGroup(IntEnum):
    GroupNone = 0  # no cascade
    Cnt0Cnt1 = 1  # Counter 0 as first, counter 1 as second.
    Cnt2Cnt3 = 2  # Counter 2 as first, counter 3 as second
    Cnt4Cnt5 = 3  # Counter 4 as first, counter 5 as second
    Cnt6Cnt7 = 4  # Counter 6 as first, counter 7 as second


class FreqMeasureMethod(IntEnum):
    # Intelligently select the measurement method according to the input signal.
    AutoAdaptive = 0
    # Using system timing clock to calculate the frequency
    CountingPulseBySysTime = 1
    # Using the device timing clock to calculate the frequency
    CountingPulseByDevTime = 2
    # Calculate the frequency from the period of the signal
    PeriodInverse = 3


class ActiveSignal(IntEnum):
    ActiveNone = 0
    RisingEdge = 1
    FallingEdge = 2
    BothEdge = 3
    HighLevel = 4
    LowLevel = 5


class TriggerAction(IntEnum):
    ActionNone = 0  # No action to take even if the trigger condition is satisfied
    DelayToStart = 1  # Begin to start after the specified time is elapsed if the trigger condition is satisfied
    DelayToStop = 2  # Stop execution after the specified time is elapsed if the trigger condition is satisfied
    Mark = 3  # Generate a mark data


class SignalPosition(IntEnum):
    InternalSig = 0
    OnConnector = 1
    OnAMSI = 2


class SignalDrop(IntEnum):
    SignalNone = 0  # No connection

    # Internal signal connector
    InternalClock = (
        1  # Device built-in clock, the highest freq one if there are several ones.
    )
    Internal1KHz = 2  # Device built-in clock, 1KHz
    Internal10KHz = 3  # Device built-in clock, 10KHz
    Internal100KHz = 4  # Device built-in clock, 100KHz
    Internal1MHz = 5  # Device built-in clock, 1MHz
    Internal10MHz = 6  # Device built-in clock, 10MHz
    Internal20MHz = 7  # Device built-in clock, 20MHz
    Internal30MHz = 8  # Device built-in clock, 30MHz
    Internal40MHz = 9  # Device built-in clock, 40MHz
    Internal50MHz = 10  # Device built-in clock, 50MHz
    Internal60MHz = 11  # Device built-in clock, 60MHz

    DIPatternMatch = 12  # When DI pattern match occurred
    DIStatusChange = 13  # When DI status change occurred

    # Function pin on connector
    ExtAnalogClock = 14  # Analog clock pin of connector
    ExtAnalogScanClock = 15  # scan clock pin of connector
    ExtAnalogTrigger = 16  # external analog trigger pin of connector
    ExtAnalogTrigger0 = (16,)  # external analog trigger pin of connector 0
    ExtDigitalClock = 17  # digital clock pin of connector
    ExtDigitalTrigger0 = (
        18  # external digital trigger 0 pin(or DI start trigger pin) of connector
    )
    ExtDigitalTrigger1 = (
        19  # external digital trigger 1 pin(or DI stop trigger pin) of connector
    )
    ExtDigitalTrigger2 = (
        20  # external digital trigger 2 pin(or DO start trigger pin) of connector
    )
    ExtDigitalTrigger3 = (
        21  # external digital trigger 3 pin(or DO stop trigger pin) of connector
    )
    ChFreezeDO = 22  # Channel freeze DO ports pin

    # Signal source or target on the connector
    # AI channel pins
    AI0 = 23
    AI1 = 24
    AI2 = 25
    AI3 = 26
    AI4 = 27
    AI5 = 28
    AI6 = 29
    AI7 = 30
    AI8 = 31
    AI9 = 32
    AI10 = 33
    AI11 = 34
    AI12 = 35
    AI13 = 36
    AI14 = 37
    AI15 = 38
    AI16 = 39
    AI17 = 40
    AI18 = 41
    AI19 = 42
    AI20 = 43
    AI21 = 44
    AI22 = 45
    AI23 = 46
    AI24 = 47
    AI25 = 48
    AI26 = 49
    AI27 = 50
    AI28 = 51
    AI29 = 52
    AI30 = 53
    AI31 = 54
    AI32 = 55
    AI33 = 56
    AI34 = 57
    AI35 = 58
    AI36 = 59
    AI37 = 60
    AI38 = 61
    AI39 = 62
    AI40 = 63
    AI41 = 64
    AI42 = 65
    AI43 = 66
    AI44 = 67
    AI45 = 68
    AI46 = 69
    AI47 = 70
    AI48 = 71
    AI49 = 72
    AI50 = 73
    AI51 = 74
    AI52 = 75
    AI53 = 76
    AI54 = 77
    AI55 = 78
    AI56 = 79
    AI57 = 80
    AI58 = 81
    AI59 = 82
    AI60 = 83
    AI61 = 84
    AI62 = 85
    AI63 = 86

    # AO channel pins
    AO0 = 87
    AO1 = 88
    AO2 = 89
    AO3 = 90
    AO4 = 91
    AO5 = 92
    AO6 = 93
    AO7 = 94
    AO8 = 95
    AO9 = 96
    AO10 = 97
    AO11 = 98
    AO12 = 99
    AO13 = 100
    AO14 = 101
    AO15 = 102
    AO16 = 103
    AO17 = 104
    AO18 = 105
    AO19 = 106
    AO20 = 107
    AO21 = 108
    AO22 = 109
    AO23 = 110
    AO24 = 111
    AO25 = 112
    AO26 = 113
    AO27 = 114
    AO28 = 115
    AO29 = 116
    AO30 = 117
    AO31 = 118

    # DI pins
    DI0 = 119
    DI1 = 120
    DI2 = 121
    DI3 = 122
    DI4 = 123
    DI5 = 124
    DI6 = 125
    DI7 = 126
    DI8 = 127
    DI9 = 128
    DI10 = 129
    DI11 = 130
    DI12 = 131
    DI13 = 132
    DI14 = 133
    DI15 = 134
    DI16 = 135
    DI17 = 136
    DI18 = 137
    DI19 = 138
    DI20 = 139
    DI21 = 140
    DI22 = 141
    DI23 = 142
    DI24 = 143
    DI25 = 144
    DI26 = 145
    DI27 = 146
    DI28 = 147
    DI29 = 148
    DI30 = 149
    DI31 = 150
    DI32 = 151
    DI33 = 152
    DI34 = 153
    DI35 = 154
    DI36 = 155
    DI37 = 156
    DI38 = 157
    DI39 = 158
    DI40 = 159
    DI41 = 160
    DI42 = 161
    DI43 = 162
    DI44 = 163
    DI45 = 164
    DI46 = 165
    DI47 = 166
    DI48 = 167
    DI49 = 168
    DI50 = 169
    DI51 = 170
    DI52 = 171
    DI53 = 172
    DI54 = 173
    DI55 = 174
    DI56 = 175
    DI57 = 176
    DI58 = 177
    DI59 = 178
    DI60 = 179
    DI61 = 180
    DI62 = 181
    DI63 = 182
    DI64 = 183
    DI65 = 184
    DI66 = 185
    DI67 = 186
    DI68 = 187
    DI69 = 188
    DI70 = 189
    DI71 = 190
    DI72 = 191
    DI73 = 192
    DI74 = 193
    DI75 = 194
    DI76 = 195
    DI77 = 196
    DI78 = 197
    DI79 = 198
    DI80 = 199
    DI81 = 200
    DI82 = 201
    DI83 = 202
    DI84 = 203
    DI85 = 204
    DI86 = 205
    DI87 = 206
    DI88 = 207
    DI89 = 208
    DI90 = 209
    DI91 = 210
    DI92 = 211
    DI93 = 212
    DI94 = 213
    DI95 = 214
    DI96 = 215
    DI97 = 216
    DI98 = 217
    DI99 = 218
    DI100 = 219
    DI101 = 220
    DI102 = 221
    DI103 = 222
    DI104 = 223
    DI105 = 224
    DI106 = 225
    DI107 = 226
    DI108 = 227
    DI109 = 228
    DI110 = 229
    DI111 = 230
    DI112 = 231
    DI113 = 232
    DI114 = 233
    DI115 = 234
    DI116 = 235
    DI117 = 236
    DI118 = 237
    DI119 = 238
    DI120 = 239
    DI121 = 240
    DI122 = 241
    DI123 = 242
    DI124 = 243
    DI125 = 244
    DI126 = 245
    DI127 = 246
    DI128 = 247
    DI129 = 248
    DI130 = 249
    DI131 = 250
    DI132 = 251
    DI133 = 252
    DI134 = 253
    DI135 = 254
    DI136 = 255
    DI137 = 256
    DI138 = 257
    DI139 = 258
    DI140 = 259
    DI141 = 260
    DI142 = 261
    DI143 = 262
    DI144 = 263
    DI145 = 264
    DI146 = 265
    DI147 = 266
    DI148 = 267
    DI149 = 268
    DI150 = 269
    DI151 = 270
    DI152 = 271
    DI153 = 272
    DI154 = 273
    DI155 = 274
    DI156 = 275
    DI157 = 276
    DI158 = 277
    DI159 = 278
    DI160 = 279
    DI161 = 280
    DI162 = 281
    DI163 = 282
    DI164 = 283
    DI165 = 284
    DI166 = 285
    DI167 = 286
    DI168 = 287
    DI169 = 288
    DI170 = 289
    DI171 = 290
    DI172 = 291
    DI173 = 292
    DI174 = 293
    DI175 = 294
    DI176 = 295
    DI177 = 296
    DI178 = 297
    DI179 = 298
    DI180 = 299
    DI181 = 300
    DI182 = 301
    DI183 = 302
    DI184 = 303
    DI185 = 304
    DI186 = 305
    DI187 = 306
    DI188 = 307
    DI189 = 308
    DI190 = 309
    DI191 = 310
    DI192 = 311
    DI193 = 312
    DI194 = 313
    DI195 = 314
    DI196 = 315
    DI197 = 316
    DI198 = 317
    DI199 = 318
    DI200 = 319
    DI201 = 320
    DI202 = 321
    DI203 = 322
    DI204 = 323
    DI205 = 324
    DI206 = 325
    DI207 = 326
    DI208 = 327
    DI209 = 328
    DI210 = 329
    DI211 = 330
    DI212 = 331
    DI213 = 332
    DI214 = 333
    DI215 = 334
    DI216 = 335
    DI217 = 336
    DI218 = 337
    DI219 = 338
    DI220 = 339
    DI221 = 340
    DI222 = 341
    DI223 = 342
    DI224 = 343
    DI225 = 344
    DI226 = 345
    DI227 = 346
    DI228 = 347
    DI229 = 348
    DI230 = 349
    DI231 = 350
    DI232 = 351
    DI233 = 352
    DI234 = 353
    DI235 = 354
    DI236 = 355
    DI237 = 356
    DI238 = 357
    DI239 = 358
    DI240 = 359
    DI241 = 360
    DI242 = 361
    DI243 = 362
    DI244 = 363
    DI245 = 364
    DI246 = 365
    DI247 = 366
    DI248 = 367
    DI249 = 368
    DI250 = 369
    DI251 = 370
    DI252 = 371
    DI253 = 372
    DI254 = 373
    DI255 = 374

    # DIO pins
    DIO0 = 375
    DIO1 = 376
    DIO2 = 377
    DIO3 = 378
    DIO4 = 379
    DIO5 = 380
    DIO6 = 381
    DIO7 = 382
    DIO8 = 383
    DIO9 = 384
    DIO10 = 385
    DIO11 = 386
    DIO12 = 387
    DIO13 = 388
    DIO14 = 389
    DIO15 = 390
    DIO16 = 391
    DIO17 = 392
    DIO18 = 393
    DIO19 = 394
    DIO20 = 395
    DIO21 = 396
    DIO22 = 397
    DIO23 = 398
    DIO24 = 399
    DIO25 = 400
    DIO26 = 401
    DIO27 = 402
    DIO28 = 403
    DIO29 = 404
    DIO30 = 405
    DIO31 = 406
    DIO32 = 407
    DIO33 = 408
    DIO34 = 409
    DIO35 = 410
    DIO36 = 411
    DIO37 = 412
    DIO38 = 413
    DIO39 = 414
    DIO40 = 415
    DIO41 = 416
    DIO42 = 417
    DIO43 = 418
    DIO44 = 419
    DIO45 = 420
    DIO46 = 421
    DIO47 = 422
    DIO48 = 423
    DIO49 = 424
    DIO50 = 425
    DIO51 = 426
    DIO52 = 427
    DIO53 = 428
    DIO54 = 429
    DIO55 = 430
    DIO56 = 431
    DIO57 = 432
    DIO58 = 433
    DIO59 = 434
    DIO60 = 435
    DIO61 = 436
    DIO62 = 437
    DIO63 = 438
    DIO64 = 439
    DIO65 = 440
    DIO66 = 441
    DIO67 = 442
    DIO68 = 443
    DIO69 = 444
    DIO70 = 445
    DIO71 = 446
    DIO72 = 447
    DIO73 = 448
    DIO74 = 449
    DIO75 = 450
    DIO76 = 451
    DIO77 = 452
    DIO78 = 453
    DIO79 = 454
    DIO80 = 455
    DIO81 = 456
    DIO82 = 457
    DIO83 = 458
    DIO84 = 459
    DIO85 = 460
    DIO86 = 461
    DIO87 = 462
    DIO88 = 463
    DIO89 = 464
    DIO90 = 465
    DIO91 = 466
    DIO92 = 467
    DIO93 = 468
    DIO94 = 469
    DIO95 = 470
    DIO96 = 471
    DIO97 = 472
    DIO98 = 473
    DIO99 = 474
    DIO100 = 475
    DIO101 = 476
    DIO102 = 477
    DIO103 = 478
    DIO104 = 479
    DIO105 = 480
    DIO106 = 481
    DIO107 = 482
    DIO108 = 483
    DIO109 = 484
    DIO110 = 485
    DIO111 = 486
    DIO112 = 487
    DIO113 = 488
    DIO114 = 489
    DIO115 = 490
    DIO116 = 491
    DIO117 = 492
    DIO118 = 493
    DIO119 = 494
    DIO120 = 495
    DIO121 = 496
    DIO122 = 497
    DIO123 = 498
    DIO124 = 499
    DIO125 = 500
    DIO126 = 501
    DIO127 = 502
    DIO128 = 503
    DIO129 = 504
    DIO130 = 505
    DIO131 = 506
    DIO132 = 507
    DIO133 = 508
    DIO134 = 509
    DIO135 = 510
    DIO136 = 511
    DIO137 = 512
    DIO138 = 513
    DIO139 = 514
    DIO140 = 515
    DIO141 = 516
    DIO142 = 517
    DIO143 = 518
    DIO144 = 519
    DIO145 = 520
    DIO146 = 521
    DIO147 = 522
    DIO148 = 523
    DIO149 = 524
    DIO150 = 525
    DIO151 = 526
    DIO152 = 527
    DIO153 = 528
    DIO154 = 529
    DIO155 = 530
    DIO156 = 531
    DIO157 = 532
    DIO158 = 533
    DIO159 = 534
    DIO160 = 535
    DIO161 = 536
    DIO162 = 537
    DIO163 = 538
    DIO164 = 539
    DIO165 = 540
    DIO166 = 541
    DIO167 = 542
    DIO168 = 543
    DIO169 = 544
    DIO170 = 545
    DIO171 = 546
    DIO172 = 547
    DIO173 = 548
    DIO174 = 549
    DIO175 = 550
    DIO176 = 551
    DIO177 = 552
    DIO178 = 553
    DIO179 = 554
    DIO180 = 555
    DIO181 = 556
    DIO182 = 557
    DIO183 = 558
    DIO184 = 559
    DIO185 = 560
    DIO186 = 561
    DIO187 = 562
    DIO188 = 563
    DIO189 = 564
    DIO190 = 565
    DIO191 = 566
    DIO192 = 567
    DIO193 = 568
    DIO194 = 569
    DIO195 = 570
    DIO196 = 571
    DIO197 = 572
    DIO198 = 573
    DIO199 = 574
    DIO200 = 575
    DIO201 = 576
    DIO202 = 577
    DIO203 = 578
    DIO204 = 579
    DIO205 = 580
    DIO206 = 581
    DIO207 = 582
    DIO208 = 583
    DIO209 = 584
    DIO210 = 585
    DIO211 = 586
    DIO212 = 587
    DIO213 = 588
    DIO214 = 589
    DIO215 = 590
    DIO216 = 591
    DIO217 = 592
    DIO218 = 593
    DIO219 = 594
    DIO220 = 595
    DIO221 = 596
    DIO222 = 597
    DIO223 = 598
    DIO224 = 599
    DIO225 = 600
    DIO226 = 601
    DIO227 = 602
    DIO228 = 603
    DIO229 = 604
    DIO230 = 605
    DIO231 = 606
    DIO232 = 607
    DIO233 = 608
    DIO234 = 609
    DIO235 = 610
    DIO236 = 611
    DIO237 = 612
    DIO238 = 613
    DIO239 = 614
    DIO240 = 615
    DIO241 = 616
    DIO242 = 617
    DIO243 = 618
    DIO244 = 619
    DIO245 = 620
    DIO246 = 621
    DIO247 = 622
    DIO248 = 623
    DIO249 = 624
    DIO250 = 625
    DIO251 = 626
    DIO252 = 627
    DIO253 = 628
    DIO254 = 629
    DIO255 = 630

    # Counter clock pins
    CntClk0 = 631
    CntClk1 = 632
    CntClk2 = 633
    CntClk3 = 634
    CntClk4 = 635
    CntClk5 = 636
    CntClk6 = 637
    CntClk7 = 638

    # counter gate pins
    CntGate0 = 639
    CntGate1 = 640
    CntGate2 = 641
    CntGate3 = 642
    CntGate4 = 643
    CntGate5 = 644
    CntGate6 = 645
    CntGate7 = 646

    # counter out pins
    CntOut0 = 647
    CntOut1 = 648
    CntOut2 = 649
    CntOut3 = 650
    CntOut4 = 651
    CntOut5 = 652
    CntOut6 = 653
    CntOut7 = 654

    # counter frequency out pins
    CntFreqOut0 = 655
    CntFreqOut1 = 656
    CntFreqOut2 = 657
    CntFreqOut3 = 658
    CntFreqOut4 = 659
    CntFreqOut5 = 660
    CntFreqOut6 = 661
    CntFreqOut7 = 662

    # AMSI pins
    AMSI0 = 663
    AMSI1 = 664
    AMSI2 = 665
    AMSI3 = 666
    AMSI4 = 667
    AMSI5 = 668
    AMSI6 = 669
    AMSI7 = 670
    AMSI8 = 671
    AMSI9 = 672
    AMSI10 = 673
    AMSI11 = 674
    AMSI12 = 675
    AMSI13 = 676
    AMSI14 = 677
    AMSI15 = 678
    AMSI16 = 679
    AMSI17 = 680
    AMSI18 = 681
    AMSI19 = 682

    # new clocks
    Internal2Hz = 683  # Device built-in clock, 2Hz
    Internal20Hz = 684  # Device built-in clock, 20Hz
    Internal200Hz = 685  # Device built-in clock, 200KHz
    Internal2KHz = 686  # Device built-in clock, 2KHz
    Internal20KHz = 687  # Device built-in clock, 20KHz
    Internal200KHz = 688  # Device built-in clock, 200KHz
    Internal2MHz = 689  # Device built-in clock, 2MHz

    # New Function pin on connector
    ExtAnalogTrigger1 = 690  # external analog trigger pin of connector 1

    # Reference clock
    ExtDigRefClock = 691  # digital clock pin of connector
    Internal100MHz = 692
    AIConvClock = 693

    # digital trigger from master after ADC latency
    SigExtDigitalTrgADCLatency = 694
    SigExtDigitalTrg0ADCLatency = SigExtDigitalTrgADCLatency
    SigExtDigitalTrg1ADCLatency = 695

    # digital trigger from master/MSDI pin after ADC latency
    MDSITrg0 = 696
    MDSITrg1 = 697

    MDSITrg0ADCLatency = 698
    MDSITrg1ADCLatency = 699

    # reference clock source from master/MDSI pin
    MDSIRefClock = 700
    MDSIClock = 701

    # clock source & trigger for Master/Slave module
    # internal clock x, as a master module
    IntClock0 = 702
    IntClock1 = 703
    IntClock2 = 704
    IntClock3 = 705

    # clock from internal clock x, as a slave module
    IntClk0Slv = 706
    IntClk1Slv = 707
    IntClk2Slv = 708
    IntClk3Slv = 709

    # Trigger x from trigger pin, as a slave module
    ExtDigTrg0Slv = 710
    ExtDigTrg1Slv = 711
    ExtDigTrg2Slv = 712
    ExtDigTrg3Slv = 713


class EventId(IntEnum):
    DeviceRemoved = 0  # The device was removed from system
    DeviceReconnected = 1  # The device is reconnected
    PropertyChanged = 2  # Some properties of the device were changed
    # -----------------------------------------------------------------
    # AI events
    # -----------------------------------------------------------------
    BufferedAIDataReady = 3
    BufferedAIOverrun = 4
    BufferedAICacheOverflow = 5
    BufferedAIStopped = 6

    # -----------------------------------------------------------------
    #  AO event IDs
    # -----------------------------------------------------------------
    BufferedAODataTransmitted = 7
    BufferedAOUnderRun = 8
    BufferedAOCacheEmptied = 9
    BufferedAOTransStopped = 10
    BufferedAOStopped = 11

    # -----------------------------------------------------------------
    #  DIO event IDs
    # -----------------------------------------------------------------
    DIInterrupt = 12
    DIIntChannel000 = DIInterrupt
    DIIntChannel001 = 13
    DIIntChannel002 = 14
    DIIntChannel003 = 15
    DIIntChannel004 = 16
    DIIntChannel005 = 17
    DIIntChannel006 = 18
    DIIntChannel007 = 19
    DIIntChannel008 = 20
    DIIntChannel009 = 21
    DIIntChannel010 = 22
    DIIntChannel011 = 23
    DIIntChannel012 = 24
    DIIntChannel013 = 25
    DIIntChannel014 = 26
    DIIntChannel015 = 27
    DIIntChannel016 = 28
    DIIntChannel017 = 29
    DIIntChannel018 = 30
    DIIntChannel019 = 31
    DIIntChannel020 = 32
    DIIntChannel021 = 33
    DIIntChannel022 = 34
    DIIntChannel023 = 35
    DIIntChannel024 = 36
    DIIntChannel025 = 37
    DIIntChannel026 = 38
    DIIntChannel027 = 39
    DIIntChannel028 = 40
    DIIntChannel029 = 41
    DIIntChannel030 = 42
    DIIntChannel031 = 43
    DIIntChannel032 = 44
    DIIntChannel033 = 45
    DIIntChannel034 = 46
    DIIntChannel035 = 47
    DIIntChannel036 = 48
    DIIntChannel037 = 49
    DIIntChannel038 = 50
    DIIntChannel039 = 51
    DIIntChannel040 = 52
    DIIntChannel041 = 53
    DIIntChannel042 = 54
    DIIntChannel043 = 55
    DIIntChannel044 = 56
    DIIntChannel045 = 57
    DIIntChannel046 = 58
    DIIntChannel047 = 59
    DIIntChannel048 = 60
    DIIntChannel049 = 61
    DIIntChannel050 = 62
    DIIntChannel051 = 63
    DIIntChannel052 = 64
    DIIntChannel053 = 65
    DIIntChannel054 = 66
    DIIntChannel055 = 67
    DIIntChannel056 = 68
    DIIntChannel057 = 69
    DIIntChannel058 = 70
    DIIntChannel059 = 71
    DIIntChannel060 = 72
    DIIntChannel061 = 73
    DIIntChannel062 = 74
    DIIntChannel063 = 75
    DIIntChannel064 = 76
    DIIntChannel065 = 77
    DIIntChannel066 = 78
    DIIntChannel067 = 79
    DIIntChannel068 = 80
    DIIntChannel069 = 81
    DIIntChannel070 = 82
    DIIntChannel071 = 83
    DIIntChannel072 = 84
    DIIntChannel073 = 85
    DIIntChannel074 = 86
    DIIntChannel075 = 87
    DIIntChannel076 = 88
    DIIntChannel077 = 89
    DIIntChannel078 = 90
    DIIntChannel079 = 91
    DIIntChannel080 = 92
    DIIntChannel081 = 93
    DIIntChannel082 = 94
    DIIntChannel083 = 95
    DIIntChannel084 = 96
    DIIntChannel085 = 97
    DIIntChannel086 = 98
    DIIntChannel087 = 99
    DIIntChannel088 = 100
    DIIntChannel089 = 101
    DIIntChannel090 = 102
    DIIntChannel091 = 103
    DIIntChannel092 = 104
    DIIntChannel093 = 105
    DIIntChannel094 = 106
    DIIntChannel095 = 107
    DIIntChannel096 = 108
    DIIntChannel097 = 109
    DIIntChannel098 = 110
    DIIntChannel099 = 111
    DIIntChannel100 = 112
    DIIntChannel101 = 113
    DIIntChannel102 = 114
    DIIntChannel103 = 115
    DIIntChannel104 = 116
    DIIntChannel105 = 117
    DIIntChannel106 = 118
    DIIntChannel107 = 119
    DIIntChannel108 = 120
    DIIntChannel109 = 121
    DIIntChannel110 = 122
    DIIntChannel111 = 123
    DIIntChannel112 = 124
    DIIntChannel113 = 125
    DIIntChannel114 = 126
    DIIntChannel115 = 127
    DIIntChannel116 = 128
    DIIntChannel117 = 129
    DIIntChannel118 = 130
    DIIntChannel119 = 131
    DIIntChannel120 = 132
    DIIntChannel121 = 133
    DIIntChannel122 = 134
    DIIntChannel123 = 135
    DIIntChannel124 = 136
    DIIntChannel125 = 137
    DIIntChannel126 = 138
    DIIntChannel127 = 139
    DIIntChannel128 = 140
    DIIntChannel129 = 141
    DIIntChannel130 = 142
    DIIntChannel131 = 143
    DIIntChannel132 = 144
    DIIntChannel133 = 145
    DIIntChannel134 = 146
    DIIntChannel135 = 147
    DIIntChannel136 = 148
    DIIntChannel137 = 149
    DIIntChannel138 = 150
    DIIntChannel139 = 151
    DIIntChannel140 = 152
    DIIntChannel141 = 153
    DIIntChannel142 = 154
    DIIntChannel143 = 155
    DIIntChannel144 = 156
    DIIntChannel145 = 157
    DIIntChannel146 = 158
    DIIntChannel147 = 159
    DIIntChannel148 = 160
    DIIntChannel149 = 161
    DIIntChannel150 = 162
    DIIntChannel151 = 163
    DIIntChannel152 = 164
    DIIntChannel153 = 165
    DIIntChannel154 = 166
    DIIntChannel155 = 167
    DIIntChannel156 = 168
    DIIntChannel157 = 169
    DIIntChannel158 = 170
    DIIntChannel159 = 171
    DIIntChannel160 = 172
    DIIntChannel161 = 173
    DIIntChannel162 = 174
    DIIntChannel163 = 175
    DIIntChannel164 = 176
    DIIntChannel165 = 177
    DIIntChannel166 = 178
    DIIntChannel167 = 179
    DIIntChannel168 = 180
    DIIntChannel169 = 181
    DIIntChannel170 = 182
    DIIntChannel171 = 183
    DIIntChannel172 = 184
    DIIntChannel173 = 185
    DIIntChannel174 = 186
    DIIntChannel175 = 187
    DIIntChannel176 = 188
    DIIntChannel177 = 189
    DIIntChannel178 = 190
    DIIntChannel179 = 191
    DIIntChannel180 = 192
    DIIntChannel181 = 193
    DIIntChannel182 = 194
    DIIntChannel183 = 195
    DIIntChannel184 = 196
    DIIntChannel185 = 197
    DIIntChannel186 = 198
    DIIntChannel187 = 199
    DIIntChannel188 = 200
    DIIntChannel189 = 201
    DIIntChannel190 = 202
    DIIntChannel191 = 203
    DIIntChannel192 = 204
    DIIntChannel193 = 205
    DIIntChannel194 = 206
    DIIntChannel195 = 207
    DIIntChannel196 = 208
    DIIntChannel197 = 209
    DIIntChannel198 = 210
    DIIntChannel199 = 211
    DIIntChannel200 = 212
    DIIntChannel201 = 213
    DIIntChannel202 = 214
    DIIntChannel203 = 215
    DIIntChannel204 = 216
    DIIntChannel205 = 217
    DIIntChannel206 = 218
    DIIntChannel207 = 219
    DIIntChannel208 = 220
    DIIntChannel209 = 221
    DIIntChannel210 = 222
    DIIntChannel211 = 223
    DIIntChannel212 = 224
    DIIntChannel213 = 225
    DIIntChannel214 = 226
    DIIntChannel215 = 227
    DIIntChannel216 = 228
    DIIntChannel217 = 229
    DIIntChannel218 = 230
    DIIntChannel219 = 231
    DIIntChannel220 = 232
    DIIntChannel221 = 233
    DIIntChannel222 = 234
    DIIntChannel223 = 235
    DIIntChannel224 = 236
    DIIntChannel225 = 237
    DIIntChannel226 = 238
    DIIntChannel227 = 239
    DIIntChannel228 = 240
    DIIntChannel229 = 241
    DIIntChannel230 = 242
    DIIntChannel231 = 243
    DIIntChannel232 = 244
    DIIntChannel233 = 245
    DIIntChannel234 = 246
    DIIntChannel235 = 247
    DIIntChannel236 = 248
    DIIntChannel237 = 249
    DIIntChannel238 = 250
    DIIntChannel239 = 251
    DIIntChannel240 = 252
    DIIntChannel241 = 253
    DIIntChannel242 = 254
    DIIntChannel243 = 255
    DIIntChannel244 = 256
    DIIntChannel245 = 257
    DIIntChannel246 = 258
    DIIntChannel247 = 259
    DIIntChannel248 = 260
    DIIntChannel249 = 261
    DIIntChannel250 = 262
    DIIntChannel251 = 263
    DIIntChannel252 = 264
    DIIntChannel253 = 265
    DIIntChannel254 = 266
    DIIntChannel255 = 267

    DIStatusChange = 268
    DICosIntPort000 = DIStatusChange
    DICosIntPort001 = 269
    DICosIntPort002 = 270
    DICosIntPort003 = 271
    DICosIntPort004 = 272
    DICosIntPort005 = 273
    DICosIntPort006 = 274
    DICosIntPort007 = 275
    DICosIntPort008 = 276
    DICosIntPort009 = 277
    DICosIntPort010 = 278
    DICosIntPort011 = 279
    DICosIntPort012 = 280
    DICosIntPort013 = 281
    DICosIntPort014 = 282
    DICosIntPort015 = 283
    DICosIntPort016 = 284
    DICosIntPort017 = 285
    DICosIntPort018 = 286
    DICosIntPort019 = 287
    DICosIntPort020 = 288
    DICosIntPort021 = 289
    DICosIntPort022 = 290
    DICosIntPort023 = 291
    DICosIntPort024 = 292
    DICosIntPort025 = 293
    DICosIntPort026 = 294
    DICosIntPort027 = 295
    DICosIntPort028 = 296
    DICosIntPort029 = 297
    DICosIntPort030 = 298
    DICosIntPort031 = 299

    DIPatternMatch = 300
    DIPatternMatchIntPort000 = DIPatternMatch
    DIPatternMatchIntPort001 = 301
    DIPatternMatchIntPort002 = 302
    DIPatternMatchIntPort003 = 303
    DIPatternMatchIntPort004 = 304
    DIPatternMatchIntPort005 = 305
    DIPatternMatchIntPort006 = 306
    DIPatternMatchIntPort007 = 307
    DIPatternMatchIntPort008 = 308
    DIPatternMatchIntPort009 = 309
    DIPatternMatchIntPort010 = 310
    DIPatternMatchIntPort011 = 311
    DIPatternMatchIntPort012 = 312
    DIPatternMatchIntPort013 = 313
    DIPatternMatchIntPort014 = 314
    DIPatternMatchIntPort015 = 315
    DIPatternMatchIntPort016 = 316
    DIPatternMatchIntPort017 = 317
    DIPatternMatchIntPort018 = 318
    DIPatternMatchIntPort019 = 319
    DIPatternMatchIntPort020 = 320
    DIPatternMatchIntPort021 = 321
    DIPatternMatchIntPort022 = 322
    DIPatternMatchIntPort023 = 323
    DIPatternMatchIntPort024 = 324
    DIPatternMatchIntPort025 = 325
    DIPatternMatchIntPort026 = 326
    DIPatternMatchIntPort027 = 327
    DIPatternMatchIntPort028 = 328
    DIPatternMatchIntPort029 = 329
    DIPatternMatchIntPort030 = 330
    DIPatternMatchIntPort031 = 331

    BufferedDIDataReady = 332
    BufferedDIOverRun = 333
    BufferedDICacheOverflow = 334
    BufferedDIStopped = 335

    BufferedDODataTransmitted = 336
    BufferedDOUnderRun = 337
    BufferedDOCacheEmptied = 338
    BufferedDOTransStopped = 339
    BufferedDOStopped = 340

    ReflectWdtOccurred = 341

    # -----------------------------------------------------------------
    # Counter/Timer event IDs
    # -----------------------------------------------------------------
    CntTerminalCount0 = 342
    CntTerminalCount1 = 343
    CntTerminalCount2 = 344
    CntTerminalCount3 = 345
    CntTerminalCount4 = 346
    CntTerminalCount5 = 347
    CntTerminalCount6 = 348
    CntTerminalCount7 = 349

    CntOverCompare0 = 350
    CntOverCompare1 = 351
    CntOverCompare2 = 352
    CntOverCompare3 = 353
    CntOverCompare4 = 354
    CntOverCompare5 = 355
    CntOverCompare6 = 356
    CntOverCompare7 = 357

    CntUnderCompare0 = 358
    CntUnderCompare1 = 359
    CntUnderCompare2 = 360
    CntUnderCompare3 = 361
    CntUnderCompare4 = 362
    CntUnderCompare5 = 363
    CntUnderCompare6 = 364
    CntUnderCompare7 = 365

    CntEcOverCompare0 = 366
    CntEcOverCompare1 = 367
    CntEcOverCompare2 = 368
    CntEcOverCompare3 = 369
    CntEcOverCompare4 = 370
    CntEcOverCompare5 = 371
    CntEcOverCompare6 = 372
    CntEcOverCompare7 = 373

    CntEcUnderCompare0 = 374
    CntEcUnderCompare1 = 375
    CntEcUnderCompare2 = 376
    CntEcUnderCompare3 = 377
    CntEcUnderCompare4 = 378
    CntEcUnderCompare5 = 379
    CntEcUnderCompare6 = 380
    CntEcUnderCompare7 = 381

    CntOneShot0 = 382
    CntOneShot1 = 383
    CntOneShot2 = 384
    CntOneShot3 = 385
    CntOneShot4 = 386
    CntOneShot5 = 387
    CntOneShot6 = 388
    CntOneShot7 = 389

    CntTimer0 = 390
    CntTimer1 = 391
    CntTimer2 = 392
    CntTimer3 = 393
    CntTimer4 = 394
    CntTimer5 = 395
    CntTimer6 = 396
    CntTimer7 = 397

    CntPWMInOverflow0 = 398
    CntPWMInOverflow1 = 399
    CntPWMInOverflow2 = 400
    CntPWMInOverflow3 = 401
    CntPWMInOverflow4 = 402
    CntPWMInOverflow5 = 403
    CntPWMInOverflow6 = 404
    CntPWMInOverflow7 = 405

    UdIndex0 = 406
    UdIndex1 = 407
    UdIndex2 = 408
    UdIndex3 = 409
    UdIndex4 = 410
    UdIndex5 = 411
    UdIndex6 = 412
    UdIndex7 = 413

    CntPatternMatch0 = 414
    CntPatternMatch1 = 415
    CntPatternMatch2 = 416
    CntPatternMatch3 = 417
    CntPatternMatch4 = 418
    CntPatternMatch5 = 419
    CntPatternMatch6 = 420
    CntPatternMatch7 = 421

    CntCompareTableEnd0 = 422
    CntCompareTableEnd1 = 423
    CntCompareTableEnd2 = 424
    CntCompareTableEnd3 = 425
    CntCompareTableEnd4 = 426
    CntCompareTableEnd5 = 427
    CntCompareTableEnd6 = 428
    CntCompareTableEnd7 = 429

    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # v1.1: new event of AI
    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#
    BufferedAIBurnOut = 430
    BufferedAITimeStampOverrun = 431
    BufferedAITimeStampCacheOverflow = 432
    BufferedAIMarkOverrun = 433
    BufferedAIConvStopped = 434  # Reserved for later using

    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # v1.2: new event of Buffered Counter
    # ##xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    CIDataReady = 435
    CIDataReady0 = CIDataReady
    CIDataReady1 = 436
    CIDataReady2 = 437
    CIDataReady3 = 438
    CIDataReady4 = 439
    CIDataReady5 = 440
    CIDataReady6 = 441
    CIDataReady7 = 442

    CIOverRun = 443
    CIOverRun0 = CIOverRun
    CIOverRun1 = 444
    CIOverRun2 = 445
    CIOverRun3 = 446
    CIOverRun4 = 447
    CIOverRun5 = 448
    CIOverRun6 = 449
    CIOverRun7 = 450

    CICacheOverflow = 451
    CICacheOverflow0 = CICacheOverflow
    CICacheOverflow1 = 452
    CICacheOverflow2 = 453
    CICacheOverflow3 = 454
    CICacheOverflow4 = 455
    CICacheOverflow5 = 456
    CICacheOverflow6 = 457
    CICacheOverflow7 = 458

    CODataTransmitted = 459
    CODataTransmitted0 = CODataTransmitted
    CODataTransmitted1 = 460
    CODataTransmitted2 = 461
    CODataTransmitted3 = 462
    CODataTransmitted4 = 463
    CODataTransmitted5 = 464
    CODataTransmitted6 = 465
    CODataTransmitted7 = 466

    COUnderRun = 467
    COUnderRun0 = COUnderRun
    COUnderRun1 = 468
    COUnderRun2 = 469
    COUnderRun3 = 470
    COUnderRun4 = 471
    COUnderRun5 = 472
    COUnderRun6 = 473
    COUnderRun7 = 474

    CoCacheEmptied = 475
    CoCacheEmptied0 = CoCacheEmptied
    CoCacheEmptied1 = 476
    CoCacheEmptied2 = 477
    CoCacheEmptied3 = 478
    CoCacheEmptied4 = 479
    CoCacheEmptied5 = 480
    CoCacheEmptied6 = 481
    CoCacheEmptied7 = 482

    COTransStopped = 483
    COTransStopped0 = COTransStopped
    COTransStopped1 = 484
    COTransStopped2 = 485
    COTransStopped3 = 486
    COTransStopped4 = 487
    COTransStopped5 = 488
    COTransStopped6 = 489
    COTransStopped7 = 490

    CntrStopped = 491
    CntrStopped0 = CntrStopped
    CntrStopped1 = 492
    CntrStopped2 = 493
    CntrStopped3 = 494
    CntrStopped4 = 495
    CntrStopped5 = 496
    CntrStopped6 = 497
    CntrStopped7 = 498


class ErrorCode(Enum):
    # <summary>
    # The operation is completed successfully.
    # </summary>
    Success = 0

    # ************************************************************************
    # warning
    # ************************************************************************
    # <summary>
    # The interrupt resource is not available.
    # </summary>
    WarningInterruptNotAvailable = 0xA0000000

    # <summary>
    # The parameter is out of the range.
    # </summary>
    WarningParamOutOfRange = 0xA0000001

    # <summary>
    # The property value is out of range.
    # </summary>
    WarningPropValueOutOfRange = 0xA0000002

    # <summary>
    # The property value is not supported.
    # </summary>
    WarningPropValueNotSupported = 0xA0000003

    # <summary>
    # The property value conflicts with the current state.
    # </summary>
    WarningPropValueConflict = 0xA0000004

    # <summary>
    # The value range of all channels in a group should be same,
    # such as 4~20mA of PCI-1724.
    # </summary>
    WarningVrgOfGroupNotSame = 0xA0000005

    # <summary>
    # Some properties of a property set are failed to be written into device.
    #
    # </summary>
    WarningPropPartialFailed = 0xA0000006

    # <summary>
    # The operation had been stopped.
    #
    # </summary>
    WarningFuncStopped = 0xA0000007

    # <summary>
    # The operation is time-out.
    #
    # </summary>
    WarningFuncTimeout = 0xA0000008

    # <summary>
    # The cache is over-run.
    #
    # </summary>
    WarningCacheOverflow = 0xA0000009

    # <summary>
    # The channel is burn-out.
    #
    # </summary>
    WarningBurnout = 0xA000000A

    # <summary>
    # The current data record is end.
    #
    # </summary>
    WarningRecordEnd = 0xA000000B

    # <summary>
    # The specified profile is not valid.
    #
    # </summary>
    WarningProfileNotValid = 0xA000000C

    # <summary>
    # firmware version is not newer than the FW in Device.
    #
    # </summary>
    WarningFileMismatch = 0xA000000D

    # ***********************************************************************
    # error
    # ***********************************************************************
    # <summary>
    # The handle is NULL or its type doesn't match the required operation.
    # </summary>
    ErrorHandleNotValid = 0xE0000000

    # <summary>
    # The parameter value is out of range.
    # </summary>
    ErrorParamOutOfRange = 0xE0000001

    # <summary>
    # The parameter value is not supported.
    # </summary>
    ErrorParamNotSupported = 0xE0000002

    # <summary>
    # The parameter value format is not the expected.
    # </summary>
    ErrorParamFormatUnexpected = 0xE0000003

    # <summary>
    # Not enough memory is available to complete the operation.
    # </summary>
    ErrorMemoryNotEnough = 0xE0000004

    # <summary>
    # The data buffer is null.
    # </summary>
    ErrorBufferIsNull = 0xE0000005

    # <summary>
    # The data buffer is too small for the operation.
    # </summary>
    ErrorBufferTooSmall = 0xE0000006

    # <summary>
    # The data length exceeded the limitation.
    # </summary>
    ErrorDataLenExceedLimit = 0xE0000007

    # <summary>
    # The required function is not supported.
    # </summary>
    ErrorFuncNotSupported = 0xE0000008

    # <summary>
    # The required event is not supported.
    # </summary>
    ErrorEventNotSupported = 0xE0000009

    # <summary>
    # The required property is not supported.
    # </summary>
    ErrorPropNotSupported = 0xE000000A

    # <summary>
    # The required property is read-only.
    # </summary>
    ErrorPropReadOnly = 0xE000000B

    # <summary>
    # The specified property value conflicts with the current state.
    # </summary>
    ErrorPropValueConflict = 0xE000000C

    # <summary>
    # The specified property value is out of range.
    # </summary>
    ErrorPropValueOutOfRange = 0xE000000D

    # <summary>
    # The specified property value is not supported.
    # </summary>
    ErrorPropValueNotSupported = 0xE000000E

    # <summary>
    # The handle hasn't own the privilege of the operation the user wanted.
    # </summary>
    ErrorPrivilegeNotHeld = 0xE000000F

    # <summary>
    # The required privilege is not available because someone else had own it.
    # </summary>
    ErrorPrivilegeNotAvailable = 0xE0000010

    # <summary>
    # The driver of specified device was not found.
    # </summary>
    ErrorDriverNotFound = 0xE0000011

    # <summary>
    # The driver version of the specified device mismatched.
    # </summary>
    ErrorDriverVerMismatch = 0xE0000012

    # <summary>
    # The loaded driver count exceeded the limitation.
    # </summary>
    ErrorDriverCountExceedLimit = 0xE0000013

    # <summary>
    # The device is not opened.
    # </summary>
    ErrorDeviceNotOpened = 0xE0000014

    # <summary>
    # The required device does not exist.
    # </summary>
    ErrorDeviceNotExist = 0xE0000015

    # <summary>
    # The required device is unrecognized by driver.
    # </summary>
    ErrorDeviceUnrecognized = 0xE0000016

    # <summary>
    # The configuration data of the specified device is lost or unavailable.
    # </summary>
    ErrorConfigDataLost = 0xE0000017

    # <summary>
    # The function is not initialized and can't be started.
    # </summary>
    ErrorFuncNotInited = 0xE0000018

    # <summary>
    # The function is busy.
    # </summary>
    ErrorFuncBusy = 0xE0000019

    # <summary>
    # The interrupt resource is not available.
    # </summary>
    ErrorIntrNotAvailable = 0xE000001A

    # <summary>
    # The DMA channel is not available.
    # </summary>
    ErrorDmaNotAvailable = 0xE000001B

    # <summary>
    # Time out when reading/writing the device.
    # </summary>
    ErrorDeviceIoTimeOut = 0xE000001C

    # <summary>
    # The given signature does not match with the device current one.
    # </summary>
    ErrorSignatureNotMatch = 0xE000001D

    # <summary>
    # The function cannot be executed while the buffered AI is running.
    # </summary>
    ErrorFuncConflictWithBfdAi = 0xE000001E

    # <summary>
    # The value range is not available in single-ended mode.
    # </summary>
    ErrorVrgNotAvailableInSeMode = 0xE000001F

    # <summary>
    # The value range is not available in 50omh input impedance mode..
    # </summary>
    ErrorVrgNotAvailableIn50ohmMode = 0xE0000020

    # <summary>
    # The coupling type is not available in 50omh input impedance mode..
    # </summary>
    ErrorCouplingNotAvailableIn50ohmMode = 0xE0000021

    # <summary>
    # The coupling type is not available in IEPE mode.
    # </summary>
    ErrorCouplingNotAvailableInIEPEMode = 0xE0000022

    # <summary>
    # The Communication is failed when reading/writing the device.
    # </summary>
    ErrorDeviceCommunicationFailed = 0xE0000023

    # <summary>
    # The device's 'fix number' conflicted with other device's
    # </summary>
    ErrorFixNumberConflict = 0xE0000024

    # <summary>
    # The Trigger source conflicted with other trigger configuration
    # </summary>
    ErrorTrigSrcConflict = 0xE0000025

    # <summary>
    # All properties of a property set are failed to be written into device.
    # </summary>
    ErrorPropAllFailed = 0xE0000026

    # <summary>
    # These devices can not be merged as a Fusion Device.
    # </summary>
    ErrorDeviceNotFusionable = 0xE0000027

    # Open File error
    ErrorFileOpenFailed = 0xE0000028

    # File is not for the device
    ErrorNotCompatible = 0xE0000029

    # <summary>
    # Undefined error
    # </summary>
    ErrorUndefined = 0xE000FFFF

    @staticmethod
    def lookup(value: int) -> "ErrorCode":
        value = value & 0xFFFFFFFF
        for code in ErrorCode:
            if value == code.value:
                return code
        return ErrorCode.ErrorUndefined

    # def toInt(self) -> int:
    #     return self.value
    #
    # def toString(self) -> str:
    #     return AdxEnumToString("ErrorCode", self.value, 256)


class ProductId(IntEnum):
    BD_DEMO = 0x00  # demo board
    BD_PCL818 = 0x05  # PCL-818 board
    BD_PCL818H = 0x11  # PCL-818H
    BD_PCL818L = 0x21  # PCL-818L
    BD_PCL818HG = 0x22  # PCL-818HG
    BD_PCL818HD = 0x2B  # PCL-818HD
    BD_PCM3718 = 0x37  # PCM-3718
    BD_PCM3724 = 0x38  # PCM-3724
    BD_PCM3730 = 0x5A  # PCM-3730
    BD_PCI1750 = 0x5E  # PCI-1750
    BD_PCI1751 = 0x5F  # PCI-1751
    BD_PCI1710 = 0x60  # PCI-1710
    BD_PCI1712 = 0x61  # PCI-1712
    BD_PCI1710HG = 0x67  # PCI-1710HG
    BD_PCI1711 = 0x73  # PCI-1711
    BD_PCI1711L = 0x75  # PCI-1711L
    BD_PCI1713 = 0x68  # PCI-1713
    BD_PCI1753 = 0x69  # PCI-1753
    BD_PCI1760 = 0x6A  # PCI-1760
    BD_PCI1720 = 0x6B  # PCI-1720
    BD_PCM3718H = 0x6D  # PCM-3718H
    BD_PCM3718HG = 0x6E  # PCM-3718HG
    BD_PCI1716 = 0x74  # PCI-1716
    BD_PCI1731 = 0x75  # PCI-1731
    BD_PCI1754 = 0x7B  # PCI-1754
    BD_PCI1752 = 0x7C  # PCI-1752
    BD_PCI1756 = 0x7D  # PCI-1756
    BD_PCM3725 = 0x7F  # PCM-3725
    BD_PCI1762 = 0x80  # PCI-1762
    BD_PCI1721 = 0x81  # PCI-1721
    BD_PCI1761 = 0x82  # PCI-1761
    BD_PCI1723 = 0x83  # PCI-1723
    BD_PCI1730 = 0x87  # PCI-1730
    BD_PCI1733 = 0x88  # PCI-1733
    BD_PCI1734 = 0x89  # PCI-1734
    BD_PCI1710L = 0x90  # PCI-1710L
    BD_PCI1710HGL = 0x91  # PCI-1710HGL
    BD_PCM3712 = 0x93  # PCM-3712
    BD_PCM3723 = 0x94  # PCM-3723
    BD_PCI1780 = 0x95  # PCI-1780
    BD_MIC3756 = 0x96  # MIC-3756
    BD_PCI1755 = 0x97  # PCI-1755
    BD_PCI1714 = 0x98  # PCI-1714
    BD_PCI1757 = 0x99  # PCI-1757
    BD_MIC3716 = 0x9A  # MIC-3716
    BD_MIC3761 = 0x9B  # MIC-3761
    BD_MIC3753 = 0x9C  # MIC-3753
    BD_MIC3780 = 0x9D  # MIC-3780
    BD_PCI1724 = 0x9E  # PCI-1724
    BD_PCI1758UDI = 0xA3  # PCI-1758UDI
    BD_PCI1758UDO = 0xA4  # PCI-1758UDO
    BD_PCI1747 = 0xA5  # PCI-1747
    BD_PCM3780 = 0xA6  # PCM-3780
    BD_MIC3747 = 0xA7  # MIC-3747
    BD_PCI1758UDIO = 0xA8  # PCI-1758UDIO
    BD_PCI1712L = 0xA9  # PCI-1712L
    BD_PCI1763UP = 0xAC  # PCI-1763UP
    BD_PCI1736UP = 0xAD  # PCI-1736UP
    BD_PCI1714UL = 0xAE  # PCI-1714UL
    BD_MIC3714 = 0xAF  # MIC-3714
    BD_PCM3718HO = 0xB1  # PCM-3718HO
    BD_PCI1741U = 0xB3  # PCI-1741U
    BD_MIC3723 = 0xB4  # MIC-3723
    BD_PCI1718HDU = 0xB5  # PCI-1718HDU
    BD_MIC3758DIO = 0xB6  # MIC-3758DIO
    BD_PCI1727U = 0xB7  # PCI-1727U
    BD_PCI1718HGU = 0xB8  # PCI-1718HGU
    BD_PCI1715U = 0xB9  # PCI-1715U
    BD_PCI1716L = 0xBA  # PCI-1716L
    BD_PCI1735U = 0xBB  # PCI-1735U
    BD_USB4711 = 0xBC  # USB4711
    BD_PCI1737U = 0xBD  # PCI-1737U
    BD_PCI1739U = 0xBE  # PCI-1739U
    BD_PCI1742U = 0xC0  # PCI-1742U
    BD_USB4718 = 0xC6  # USB-4718
    BD_MIC3755 = 0xC7  # MIC3755
    BD_USB4761 = 0xC8  # USB4761
    BD_PCI1784 = 0xCC  # PCI-1784
    BD_USB4716 = 0xCD  # USB4716
    BD_PCI1752U = 0xCE  # PCI-1752U
    BD_PCI1752USO = 0xCF  # PCI-1752USO
    BD_USB4751 = 0xD0  # USB4751
    BD_USB4751L = 0xD1  # USB4751L
    BD_USB4750 = 0xD2  # USB4750
    BD_MIC3713 = 0xD3  # MIC-3713
    BD_USB4711A = 0xD8  # USB4711A
    BD_PCM3753P = 0xD9  # PCM3753P
    BD_PCM3784 = 0xDA  # PCM3784
    BD_PCM3761I = 0xDB  # PCM-3761I
    BD_MIC3751 = 0xDC  # MIC-3751
    BD_PCM3730I = 0xDD  # PCM-3730I
    BD_PCM3813I = 0xE0  # PCM-3813I
    BD_PCIE1744 = 0xE1  # PCIE-1744
    BD_PCI1730U = 0xE2  # PCI-1730U
    BD_PCI1760U = 0xE3  # PCI-1760U
    BD_MIC3720 = 0xE4  # MIC-3720
    BD_PCM3810I = 0xE9  # PCM-3810I
    BD_USB4702 = 0xEA  # USB4702
    BD_USB4704 = 0xEB  # USB4704
    BD_PCM3810I_HG = 0xEC  # PCM-3810I_HG
    BD_PCI1713U = 0xED  # PCI-1713U

    # !!!BioDAQ only Product ID starts from here!!!
    BD_PCI1706U = 0x800
    BD_PCI1706MSU = 0x801
    BD_PCI1706UL = 0x802
    BD_PCIE1752 = 0x803
    BD_PCIE1754 = 0x804
    BD_PCIE1756 = 0x805
    BD_MIC1911 = 0x806
    BD_MIC3750 = 0x807
    BD_MIC3711 = 0x808
    BD_PCIE1730 = 0x809
    BD_PCI1710_ECU = 0x80A
    BD_PCI1720_ECU = 0x80B
    BD_PCIE1760 = 0x80C
    BD_PCIE1751 = 0x80D
    BD_ECUP1706 = 0x80E
    BD_PCIE1753 = 0x80F
    BD_PCIE1810 = 0x810
    BD_ECUP1702L = 0x811
    BD_PCIE1816 = 0x812
    BD_PCM27D24DI = 0x813
    BD_PCIE1816H = 0x814
    BD_PCIE1840 = 0x815
    BD_PCL725 = 0x816
    BD_PCI176E = 0x817
    BD_PCIE1802 = 0x818
    BD_AIISE730 = 0x819
    BD_PCIE1812 = 0x81A
    BD_MIC1810 = 0x81B
    BD_PCIE1802L = 0x81C
    BD_PCIE1813 = 0x81D
    BD_PCIE1840L = 0x81E
    BD_PCIE1730H = 0x81F
    BD_PCIE1756H = 0x820
    BD_PCIERXM01 = 0x821  # PCIe-RXM01
    BD_MIC1816 = 0x822
    BD_USB5830 = 0x823
    BD_USB5850 = 0x824
    BD_USB5860 = 0x825
    BD_VPX1172 = 0x826
    BD_USB5855 = 0x827
    BD_USB5856 = 0x828
    BD_USB5862 = 0x829
    BD_PCIE1840T = 0x82A
    BD_AudioCard = 0x82B
    BD_AIIS1750 = 0x82C
    BD_PCIE1840HL = 0x82D
    BD_PCIE1765 = 0x82E
    BD_PCIE1761H = 0x82F
    BD_PCIE1762H = 0x830
    BD_PCIE1884 = 0x831
    BD_PCIE1758DIO = 0x832
    BD_PCIE1758DI = 0x833
    BD_PCIE1758DO = 0x834

    #
    BD_USB5817 = 0x835
    BD_USB5801 = 0x836
    BD_PCM2731 = 0x837
    BD_MOS1110 = 0x838
    BD_PCIE1750UH = 0x839
    BD_PCIE1750U = 0x83A
    BD_USB5820 = 0x83B

    #
    BD_THK1710R = 0x83C
    BD_PCIE1803 = 0x83D
    BD_PCIE1824 = 0x83E
    BD_PCIE1805 = 0x83F

    #
    BD_MIOE1747 = 0x840
    BD_ECUP1710 = 0x841
    BD_PCIE1824L = 0x842

    #
    BD_PCIE1763AH = 0x843
    BD_PCIE1763DH = 0x844

    #
    BD_MIC1816B = 0x845

    #
    BD_SUSIGPIO = 0x846

    #
    BD_MIC1810B = 0x847

    # iDAQ series
    BD_IDAQ731 = 0x848
    BD_IDAQ763D = 0x849
    BD_IDAQ817 = 0x84A
    BD_IDAQ821 = 0x84B

    #
    BD_EAPIGPIO = 0x84C

    # iDAQ series
    BD_IDAQ841 = 0x84D
    BD_IDAQ801 = 0x84E
    BD_IDAQ815 = 0x84F

    #
    BD_PCIE1842 = 0x850
    BD_MIOE3842 = 0x851

    BD_USB4716B = 0x852

    # iDAQ Fusion (Virtual Fusion Device, iDAQSyncBpInternal)
    BD_IDAQ1CHASSYNC = 0x853  # Fused device of modules from same chassis

    BD_USB4711B = 0x854
    BD_IDAQ751 = 0x855

    BD_FusionAuto = 0x856

    BD_AIIS1882 = 0x857

    BD_MIOE3842L = 0x858

    BD_PCI1716B = 0x859
    BD_USB4750B = 0x85A
    BD_USB4761B = 0x85B
    BD_PCI1716LB = 0x85C
    BD_PCI1716H = 0x85D

    BD_PCIE1816B = 0x85E
    BD_PCIE1816HB = 0x85F

    BD_ECUP1710T = 0x860
    BD_PCI1712B = 0x861
    BD_PCI1715B = 0x862
    BD_PCI1721B = 0x863

    BD_USB4751B = 0x864
    BD_USB4751LB = 0x865

    BD_PCIE1841 = 0x866
    BD_PCIE1841L = 0x867
    BD_PCIE1810B = 0x868
    BD_PCIE1812B = 0x869
    BD_PCIE1760B = 0x86A
    BD_PCIE1751B = 0x86B
    BD_PCIE1753B = 0x86C

    # WISE-5000 starts from here
    BD_WISE5051 = 0x901
    BD_WISE5056 = 0x902
    BD_WISE5056SO = 0x903
    BD_WISE5015 = 0x904
    BD_WISE5017 = 0x905
    BD_WISE5018 = 0x906
    BD_WISE5024 = 0x907
    BD_WISE5080 = 0x908
    BD_WISE5074 = 0x909
    BD_WISE5001 = 0x90A
    BD_WISE5052 = 0x90B
    BD_WISE5057 = 0x90C
    BD_WISE5057SO = 0x90D
    BD_WISE5017C = 0x90E
    BD_WISE5017V = 0x90F
    BD_WISE5079 = 0x910

    BD_AMAX5051 = 0x911
    BD_AMAX5056 = 0x912
    BD_AMAX5056SO = 0x913
    BD_AMAX5015 = 0x914
    BD_AMAX5017 = 0x915
    BD_AMAX5018 = 0x916
    BD_AMAX5024 = 0x917
    BD_AMAX5080 = 0x918
    BD_AMAX5074 = 0x919
    BD_AMAX5001 = 0x91A
    BD_AMAX5052 = 0x91B
    BD_AMAX5057 = 0x91C
    BD_AMAX5057SO = 0x91D
    BD_AMAX5017C = 0x91E
    BD_AMAX5017V = 0x91F
    BD_AMAX5079 = 0x920
    BD_AMAX5017H = 0x921
    BD_AMAX5082 = 0x923
    BD_AMAX5060 = 0x924
    # Unknown productId
    BD_UNKNOWN = -1


class ControlState(IntEnum):
    Idle = 0
    Ready = 1
    Running = 2
    Stopped = 3
    Uninitialized = -1


# Absolute counter related definitions
class BaudRate(IntEnum):
    BaudRate2000KHz = 2000000  # 2MHz
    BaudRate1500KHz = 1500000  # 1.5MHz
    BaudRate1000KHz = 1000000  # 1MHz
    BaudRate500KHz = 500000  # 500KHz

    # Dummy ID, to ensure the type is compiled as 'int' by various compiler
    BaudRateUnknown = -1


class CodingType(IntEnum):
    BinaryCode = 0
    GrayCode = 1

    # Dummy ID, to ensure the type is compiled as 'int' by various compiler
    CodingUnknown = -1


class ErrorRetType(IntEnum):
    Current = 0
    ParticularValue = 1
    UpLimit = 2
    LowLimit = 3
    LastCorrectValue = 4

    ReturnUnknown = -1


class Scenario(IntEnum):
    InstantAI = 1 << 0
    BufferedAI = 1 << 1
    WaveformAI = 1 << 2
    InstantAO = 1 << 3
    BufferedAO = 1 << 4
    InstantDI = 1 << 5
    InstantDO = 1 << 6
    EventCounter = 1 << 7
    FreqMeter = 1 << 8
    OneShot = 1 << 9
    TimerPulse = 1 << 10
    PowerMeter = 1 << 11
    PulseWidthModulator = 1 << 12
    UdCounter = 1 << 13
    BufferedEventCounter = 1 << 14
    BufferedPowerMeter = 1 << 15
    BufferedPulseWidthModulator = 1 << 16
    BufferedUdCounter = 1 << 17
    EdgeSeparation = 1 << 18
    BufferedDI = 1 << 19
    BufferedDO = 1 << 20
    Calibration = 1 << 21
    Firmware = 1 << 22
    AbsCounter = 1 << 23


class MathInterval(Structure):
    _fields_ = [
        ("Type", c_int32),
        ("Min", c_double),
        ("Max", c_double),
    ]


class MapFuncPiece(Structure):
    _fields_ = [
        ("Size", c_int32),  # the size of structure
        ("Degree", c_int32),  # the polynomial degree
        ("UpperLimit", c_double),  # the upper limit for this scaling polynomial
        (
            "Coef",
            c_double * 2,
        ),  # variable length array for the coefficient of polynomial, in increasing degree
    ]


class DataMark(Structure):
    _fields_ = [
        ("DataIndex", c_int64),
        ("SrcId", c_int32),
        ("_reserved_", c_int32),
    ]


class DeviceInformation(Structure):
    _fields_ = [
        ("DeviceNumber", c_int32),
        ("DeviceMode", c_int32),  # AccessMode
        ("ModuleIndex", c_int32),
        ("Description", c_wchar * MAX_DEVICE_DESC_LEN),
    ]

    def __init__(
        self,
        Description: str = "",
        DeviceNumber: int = -1,
        DeviceMode: AccessMode = AccessMode.ModeWrite,
        ModuleIndex: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.DeviceNumber = DeviceNumber
        self.DeviceMode = DeviceMode
        self.ModuleIndex = ModuleIndex
        self.Description = Description


class DeviceTreeNode(Structure):
    _fields_ = [
        ("DeviceNumber", c_int32),
        ("ModulesIndex", c_int32 * 8),
        ("Description", c_wchar * MAX_DEVICE_DESC_LEN),
    ]


class DeviceEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
    ]


class BfdAIEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
        ("MarkCount", c_int32),
    ]


class BfdAOEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
    ]


class DiSnapEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("SrcNum", c_int32),
        ("Length", c_int32),
        ("PortData", c_uint8 * MAX_DIO_PORT_COUNT),
    ]


class BfdDIEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
        ("MarkCount", c_int32),
    ]


class BfdDOEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Offset", c_int32),
        ("Count", c_int32),
    ]


class CntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Channel", c_int32),
    ]


class UdCntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Length", c_int32),
        ("Data", c_int32 * MAX_CNTR_CH_COUNT),
    ]


class BfdCntrEventArgs(Structure):
    _fields_ = [
        ("Id", c_int32),  # EventId
        ("Channel", c_int32),
        ("Offset", c_int32),
        ("Count", c_int32),
    ]


class PulseWidth(Structure):
    _fields_ = [
        ("HiPeriod", c_double),
        ("LoPeriod", c_double),
    ]
