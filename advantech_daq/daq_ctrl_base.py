# -*- coding:utf-8 -*-
from pathlib import Path

from advantech_daq import (
    AccessMode,
    ControlState,
    DeviceInformation,
    DeviceTreeNode,
    ErrorCode,
    Scenario,
    utils,
)
from advantech_daq.api import array, daq_ctrl_base, is_error_code
from advantech_daq.device_ctrl import DeviceCtrl

__all__ = ["DAQCtrlBase"]


class DAQCtrlBase:
    def __init__(
        self,
        scenario: Scenario,
        dev_info: str,
        profile_path: str = "",
    ) -> None:
        self._deviceCtrl: DeviceCtrl | None = None
        self._obj: int = daq_ctrl_base.create(scenario.value)

        if dev_info:
            self.selectedDevice = dev_info
        if profile_path:
            if Path(profile_path).exists():
                self.load_profile(profile_path)
            else:
                raise FileNotFoundError(profile_path)

    @property
    def initialized(self) -> bool:
        return self.state != ControlState.Uninitialized

    def cleanup(self) -> None:
        daq_ctrl_base.cleanup(self._obj)

    def dispose(self) -> None:
        daq_ctrl_base.dispose(self._obj)

    @property
    def selectedDevice(self) -> DeviceInformation:
        dev_info: DeviceInformation = DeviceInformation()
        daq_ctrl_base.get_selected_device(self._obj, dev_info)
        return dev_info

    @selectedDevice.setter
    def selectedDevice(self, dev_info: DeviceInformation | int | str) -> None:
        if not isinstance(dev_info, (DeviceInformation, int, str)):
            raise TypeError("The parameter value is not supported.")

        ret: ErrorCode
        if isinstance(dev_info, str):
            ret = ErrorCode.lookup(
                daq_ctrl_base.set_selected_device(
                    self._obj, DeviceInformation(Description=dev_info)
                )
            )
        elif isinstance(dev_info, int):
            ret = ErrorCode.lookup(
                daq_ctrl_base.set_selected_device(
                    self._obj, DeviceInformation(Description="", DeviceNumber=dev_info)
                )
            )
        else:
            ret = ErrorCode.lookup(
                daq_ctrl_base.set_selected_device(self._obj, dev_info)
            )

        if is_error_code(ret):
            raise ValueError(
                f"The device is not opened, and the error code is 0x{ret.value:X}"
            )

    @property
    def state(self) -> ControlState:
        return utils.toControlState(daq_ctrl_base.get_state(self._obj))

    @property
    def device(self) -> DeviceCtrl:
        if self._deviceCtrl is None:
            self._deviceCtrl = DeviceCtrl(daq_ctrl_base.get_device(self._obj))
        return self._deviceCtrl

    @property
    def supportedDevices(self) -> list[DeviceTreeNode]:
        return array.to_device_tree_node(daq_ctrl_base.get_supported_devices(self._obj))

    @property
    def supportedModes(self) -> list[AccessMode]:
        return array.to_access_mode(daq_ctrl_base.get_supported_modes(self._obj), True)

    @property
    def module(self) -> int:
        return daq_ctrl_base.get_module(self._obj)

    def load_profile(self, profile_path: str) -> None:
        ret: ErrorCode = ErrorCode.lookup(
            daq_ctrl_base.load_profile(self._obj, profile_path)
        )
        if is_error_code(ret):
            raise ValueError(
                f"Profile loading has failed, the error code is 0x{ret.value:X}"
            )
