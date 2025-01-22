import logging

from commands.command import FillCommand
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import LedStrip

logger = logging.getLogger(__name__)


def resume(
    led_strip: led_strip_module.LedStrip,
    command: FillCommand,
) -> CommandResult:
    led_strip_module.operations.fill(led_strip, command.color, command.brightness)
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
