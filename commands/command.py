from enum import Enum
from typing import Literal, Union, Any
import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Command(BaseModel):
    pass


class CommandType(str, Enum):
    TEST = "test"
    STOP = "stop"
    FILL = "fill"


class TestCommand(Command):
    command_type: Literal[CommandType.TEST]


class FillCommand(Command):
    command_type: Literal[CommandType.FILL]
    color: tuple[int, int, int]
    brightness: float


class StopCommand(Command):
    command_type: Literal[CommandType.STOP]


class CommandSchema(BaseModel):
    command: Union[TestCommand, FillCommand, StopCommand] = Field(
        discriminator="command_type"
    )


def parse_command(json_data: dict[str, Any]) -> Command:
    logger.debug(f"JSON data >> {json_data}")
    command = CommandSchema.model_validate(json_data)
    logger.debug(f"Command type: {command.command.command_type}")
    return command.command
