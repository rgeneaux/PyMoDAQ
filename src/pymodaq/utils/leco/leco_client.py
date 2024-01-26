
import logging

import numpy as np
from qtpy.QtCore import QObject, Signal

from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.parameter import ioxml

from pyleco.core import COORDINATOR_PORT
from pyleco.core.message import Message
from pyleco.utils.listener import Listener
from pyleco.directors.director import Director


class PymodaqListener(Listener):

    def __init__(self, name: str,
                 server_name: str,  # of the pymodaq server
                 host: str = "localhost", port: int = COORDINATOR_PORT,
                 logger: logging.Logger | None = None,
                 timeout: float = 1,
                 **kwargs) -> None:
        super().__init__(name, host, port, logger=logger, timeout=timeout,
                         **kwargs)
        self.signals = self.ListenerSignals()
        # self.signals.message.connect(self.handle_message)
        self.cmd_signal = self.signals.cmd_signal
        self.server_name = server_name
        self.request_buffer: dict[str, list[Message]] = {}

    local_methods = ["pong", "set_log_level"]

    class ListenerSignals(QObject):
        cmd_signal = Signal(ThreadCommand)
        """
        Possible messages sendable via `cmd_signal`
            For all modules: Info, Infos, Info_xml, set_info

            For a detector: Send Data 0D, Send Data 1D, Send Data 2D

            For an actuator: move_abs, move_home, move_rel, check_position, stop_motion
        """
        # message = Signal(Message)

    def start_listen(self, data_host: str | None = None, data_port: int | None = None) -> None:
        super().start_listen(data_host, data_port)
        # self.message_handler.finish_handle_commands = self.finish_handle_commands  # type: ignore
        self.message_handler.name_changing_methods = [self.indicate_sign_in_out]
        communicator = self.message_handler.get_communicator()
        if self.message_handler.namespace is not None:
            self.signals.cmd_signal.emit(ThreadCommand("leco_connected"))
        self.director = Director(actor=self.server_name, communicator=communicator)
        for method in (
            self.set_info,
            self.move_abs,
            self.move_rel,
            self.move_home,
            self.get_actuator_value,
            self.stop_motion,
        ):
            communicator.register_rpc_method(method=method)

    def stop_listen(self) -> None:
        super().stop_listen()
        self.signals.cmd_signal.emit(ThreadCommand("leco_disconnected"))

    def indicate_sign_in_out(self, full_name: str):
        if "." in full_name:
            self.signals.cmd_signal.emit(ThreadCommand("leco_connected"))
        else:
            self.signals.cmd_signal.emit(ThreadCommand("leco_disconnected"))

    # def finish_handle_commands(self, message: Message) -> None:
    #     """Handle the list of commands: Redirect them to the application."""
    #     try:
    #         method = message.data.get("method")  # type: ignore
    #     except AttributeError:
    #         method = None
    #     if method in self.local_methods:
    #         super(PipeHandler, self.message_handler).handle_commands(message)
    #     else:
    #         self.signals.message.emit(message)

    # def handle_message(self, message: Message) -> None:
    #     """Handle a message from the message_handler."""
    #     if message.header_elements.message_type != MessageTypes.JSON:
    #         raise IOError("Unknown message format received: {message}")
    #     command: dict = message.data  # type: ignore
    #     method = command.get("method")
    #     if method is None:
    #         raise IOError("invalid command received.")
    #     try:
    #         self.request_buffer[method].append(message)
    #     except KeyError:
    #         self.request_buffer[method] = [message]

    # generic commands
    def set_info(self, path: list[str], param_dict_str: str) -> None:
        self.signals.cmd_signal.emit(ThreadCommand("set_info", attribute=[path, param_dict_str]))

    # detector commands
    def send_data(self, grabber_type: str = "") -> None:
        self.signals.cmd_signal.emit(ThreadCommand(f"Send Data {grabber_type}"))

    # actuator commands
    def move_abs(self, position: float) -> None:
        self.signals.cmd_signal.emit(ThreadCommand("move_abs", attribute=[position]))

    def move_rel(self, position: float) -> None:
        self.signals.cmd_signal.emit(ThreadCommand("move_rel", attribute=[position]))

    def move_home(self) -> None:
        self.signals.cmd_signal.emit(ThreadCommand("move_home"))

    def get_actuator_value(self) -> None:
        """Request that the actuator value is sent later on."""
        # according to DAQ_Move, this supersedes "check_position"
        self.signals.cmd_signal.emit(ThreadCommand("get_actuator_value"))

    def stop_motion(self,) -> None:
        # not implemented in DAQ_Move!
        self.signals.cmd_signal.emit(ThreadCommand("stop_motion"))

    # @Slot(ThreadCommand)
    def queue_command(self, command: ThreadCommand):
        """Queue a command to send it via LECO to the server."""

        # generic commands
        if command.command == "ini_connection":
            try:
                if self.thread.is_alive():
                    return  # already started
            except AttributeError:
                pass  # start later on, as there is no thread.
            self.start_listen()

        elif command.command == "quit":
            try:
                self.stop_listen()
            except Exception:
                pass
            finally:
                self.cmd_signal.emit(ThreadCommand('disconnected'))

        elif command.command == 'update_connection':
            # self.ipaddress = command.attribute['ipaddress']
            # self.port = command.attribute['port']
            pass  # TODO change name?

        elif command.command == 'data_ready':
            # code from the original
            # self.data_ready(data=command.attribute)
            # def data_ready(data): self.send_data(datas[0]['data'])
            self.director.ask_rpc(method="set_data", data=command.attribute[0]['data'])

        elif command.command == 'send_info':
            self.director.ask_rpc(method="set_info",
                                  path=command.attribute['path'],
                                  param_dict_str=ioxml.parameter_to_xml_string(command.attribute['param']))

        elif command.command == 'position_is':
            self.director.ask_rpc(method="set_position", position=command.attribute[0].value())

        elif command.command == 'move_done':
            # name of parameter unknown
            self.director.ask_rpc(method="set_move_done", position=command.attribute[0].value())

        elif command.command == 'x_axis':
            if isinstance(command.attribute[0], np.ndarray):
                self.director.ask_rpc(method="set_x_axis", data=command.attribute[0])
            elif isinstance(command.attribute[0], dict):
                self.director.ask_rpc(method="set_x_axis", **command.attribute[0])
            else:
                raise ValueError("Nothing to send!")

        elif command.command == 'y_axis':
            if isinstance(command.attribute[0], np.ndarray):
                self.director.ask_rpc(method="set_y_axis", data=command.attribute[0])
            elif isinstance(command.attribute[0], dict):
                self.director.ask_rpc(method="set_y_axis", **command.attribute[0])
            else:
                raise ValueError("Nothing to send!")

        else:
            raise IOError('Unknown TCP client command')