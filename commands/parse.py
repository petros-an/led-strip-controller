import logging
from typing import Any, Union

from pydantic import BaseModel, Field

from commands import Command
from commands.command import TestCommand, FillCommand, StopCommand
from commands.rotate import RotateCommand

logger = logging.getLogger(__name__)


class CommandSchema(BaseModel):
    command: Union[TestCommand, FillCommand, StopCommand, RotateCommand] = Field(
        discriminator="command_type"
    )


def parse_command(json_data: dict[str, Any]) -> Command:
    logger.debug(f"JSON data >> {json_data}")
    command = CommandSchema.model_validate(json_data)
    logger.debug(f"Command type: {command.command.command_type}")
    return command.command
