from typing import Literal

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
from led_strip import operations as led_strip_operations, LedStrip


class StopCommand(Command):
    command_type: Literal[CommandType.STOP]


def resume(led_strip: LedStrip, _: StopCommand) -> CommandResult:
    led_strip_operations.clear(led_strip)
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
