import logging

from commands.command import TestCommand
from commands.command_result import CommandResult
from led_strip import LedStrip

logger = logging.getLogger(__name__)


def resume(led_strip: LedStrip, _: TestCommand) -> CommandResult:
    logger.info("Test!")
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
