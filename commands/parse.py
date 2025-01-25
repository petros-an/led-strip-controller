import logging
from typing import Any, Union

from pydantic import BaseModel, Field

from commands import Command
from commands.fill import FillCommand
from commands.pulse import PulseCommand
from commands.rotate import RotateCommand
from commands.set_brightness import SetBrightnessCommand
from commands.stop import StopCommand
from commands.test import TestCommand

logger = logging.getLogger(__name__)


class CommandSchema(BaseModel):
    command: Union[
        TestCommand,
        FillCommand,
        StopCommand,
        RotateCommand,
        SetBrightnessCommand,
        PulseCommand,
    ] = Field(discriminator="command_type")


def parse_command(json_data: dict[str, Any]) -> Command:
    logger.debug(f"JSON data >> {json_data}")
    command = CommandSchema.model_validate(json_data)
    logger.debug(f"Command type: {command.command.command_type}")
    return command.command
