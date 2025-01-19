import logging

from commands.command_result import CommandResult

logger = logging.getLogger(__name__)


def run() -> CommandResult:
    logger.info("Test!")
    return CommandResult()
