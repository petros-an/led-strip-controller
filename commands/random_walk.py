import logging
import random
from typing import Literal

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
import led_strip as led_strip_module
from led_strip import operations

logger = logging.getLogger(__name__)

current_color = [0, 0, 0]


class RandomWalk(Command):
    command_type: Literal[CommandType.RANDOM_WALK]


def resume(
    led_strip: led_strip_module.LedStrip,
    __: RandomWalk,
) -> CommandResult:
    global current_color
    next_color = current_color

    index = random.choice([0, 1, 2])
    if random.choice([True, False]):
        for _ in range(random.randint(1, 5)):
            next_color[index] += 1
    else:
        for _ in range(random.randint(1, 5)):
            next_color[index] -= 1

    operations.fill(led_strip, tuple(next_color))  # type: ignore[arg-type]
    current_color = next_color

    return CommandResult()


def reset(led_strip: led_strip_module.LedStrip) -> None:
    global current_color
    current_color = [0, 0, 0]
