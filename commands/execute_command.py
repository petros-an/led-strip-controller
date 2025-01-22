from typing import Protocol, Optional, cast

from commands.command import Command, CommandType
from commands.command_result import CommandResult
from commands.exceptions import InvalidCommand
from led_strip.led_strip import LedStrip
from commands import fill as fill_command
from commands import test as test_command
from commands import stop as stop_command
from commands import rotate as rotate_command
import logging

logger = logging.getLogger(__name__)


class CommandModule(Protocol):
    @staticmethod
    def resume(led_strip: LedStrip, command: Command) -> CommandResult: ...

    @staticmethod
    def reset(led_strip: LedStrip) -> None: ...


module_map = {
    CommandType.TEST: test_command,
    CommandType.STOP: stop_command,
    CommandType.FILL: fill_command,
    CommandType.ROTATE: rotate_command,
}
_current_command: Optional[Command] = None


def set_current_command(command: Optional[Command]) -> None:
    global _current_command
    _current_command = command


def get_current_command() -> Optional[Command]:
    return _current_command


def get_module_for_command(command: Command) -> CommandModule:
    try:
        return cast(CommandModule, module_map[command.command_type])
    except KeyError:
        raise InvalidCommand


def execute_command(led_strip: LedStrip, command: Command) -> CommandResult:
    previous_command = get_current_command()
    set_current_command(command)

    if previous_command != command and previous_command is not None:
        previous_command_module = get_module_for_command(previous_command)
        previous_command_module.reset(led_strip)

    command_module = get_module_for_command(command)
    return command_module.resume(led_strip, command)


def continue_execution(led_strip: LedStrip) -> CommandResult:
    current_command = get_current_command()
    logger.info(f"Continuing execution: {current_command}")
    if current_command:
        return execute_command(led_strip, current_command)
    else:
        return CommandResult()
