import logging
from time import sleep
from typing import Literal

from pydantic import Field

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import operations

logger = logging.getLogger(__name__)

step = 0
period = 10


class PulseCommand(Command):
    command_type: Literal[CommandType.PULSE]
    speed: int = Field(None, ge=1, le=10)


def resume(
    led_strip: led_strip_module.LedStrip,
    command: PulseCommand,
) -> CommandResult:
    global step

    length = len(led_strip.strip)
    index = step % length
    operations.fill(led_strip, (0, 0, 0))
    for i in range(
        index - length // 10,
        index + length,
    ):
        if 0 <= i < length:
            operations.set_pixel_color(led_strip, i, (0, 0, 255 // 10 * i))

    for i in range(
        index - length,
        index + length + 10,
    ):
        if 0 <= i < length:
            operations.set_pixel_color(led_strip, i, (0, 0, 255 - 255 // 10 * i))

    sleep(0.1)

    step += 1

    return CommandResult()


def reset(led_strip: led_strip_module.LedStrip) -> None:
    global step
    step = 0
