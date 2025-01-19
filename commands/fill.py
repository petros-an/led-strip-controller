import logging

from commands.command_result import CommandResult
import led_strip as led_strip_module

logger = logging.getLogger(__name__)


def run(
    led_strip: led_strip_module.LedStrip, color: tuple[int, int, int], brightness: float
) -> CommandResult:
    led_strip_module.operations.fill(led_strip, color, brightness)
    return CommandResult()
