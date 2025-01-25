import logging
from time import sleep
from typing import Literal

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import operations

logger = logging.getLogger(__name__)

step = 0
period = 10


class RotateCommand(Command):
    command_type: Literal[CommandType.ROTATE]


def resume(
    led_strip: led_strip_module.LedStrip,
    _: RotateCommand,
) -> CommandResult:
    global step

    remainder = step % period

    if 0 <= remainder < period // 3:
        color = (255, 0, 0)
    elif period // 3 <= remainder < 2 * period // 3:
        color = (0, 255, 0)
    elif 2 * period // 3 <= remainder < period:
        color = (0, 0, 255)
    else:
        color = (0, 0, 0)

    operations.fill(led_strip, color)
    sleep(0.1)

    step += 1

    return CommandResult()


def reset(led_strip: led_strip_module.LedStrip) -> None:
    global step
    step = 0
