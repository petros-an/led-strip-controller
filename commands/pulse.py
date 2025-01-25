import logging
from typing import Literal

from pydantic import Field

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import operations

logger = logging.getLogger(__name__)

step = 0


class PulseCommand(Command):
    command_type: Literal[CommandType.PULSE]
    color: tuple[int, int, int]
    window: int = Field(ge=1, le=30)


def resume(
    led_strip: led_strip_module.LedStrip,
    command: PulseCommand,
) -> CommandResult:
    global step

    length = len(led_strip.strip)
    window = command.window
    color = command.color

    index = step % length

    operations.fill_no_autowrite(led_strip, (0, 0, 0))

    for i in range(
        max(0, index - window),
        min(length, index + window),
    ):
        operations.set_pixel_color_no_autowrite(led_strip, i, color)

    operations.write(led_strip)

    step += 1

    return CommandResult()


def reset(led_strip: led_strip_module.LedStrip) -> None:
    global step
    step = 0
