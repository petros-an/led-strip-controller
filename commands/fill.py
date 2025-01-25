import logging
from typing import Literal

from commands.command import Command, CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import LedStrip

logger = logging.getLogger(__name__)


class FillCommand(Command):
    command_type: Literal[CommandType.FILL]
    color: tuple[int, int, int]


def resume(
    led_strip: led_strip_module.LedStrip,
    command: FillCommand,
) -> CommandResult:
    led_strip_module.operations.fill(led_strip, command.color)
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
