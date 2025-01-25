import logging
from typing import Literal

from commands.command import Command, CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import LedStrip

logger = logging.getLogger(__name__)


class SetBrightnessCommand(Command):
    command_type: Literal[CommandType.SET_BRIGHTNESS]
    brightness: float


def resume(
    led_strip: led_strip_module.LedStrip,
    command: SetBrightnessCommand,
) -> CommandResult:
    led_strip_module.operations.set_brightness(led_strip, command.brightness)
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
