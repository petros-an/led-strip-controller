import logging
from typing import Literal

from commands import Command
from commands.command import CommandType
from commands.command_result import CommandResult
from led_strip import LedStrip

logger = logging.getLogger(__name__)


class TestCommand(Command):
    command_type: Literal[CommandType.TEST]


def resume(led_strip: LedStrip, _: TestCommand) -> CommandResult:
    logger.info("Test!")
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
