from enum import Enum
from typing import Literal
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Command(BaseModel):
    command_type: "CommandType"


class CommandType(str, Enum):
    TEST = "test"
    STOP = "stop"
    FILL = "fill"
    ROTATE = "rotate"


class TestCommand(Command):
    command_type: Literal[CommandType.TEST]


class FillCommand(Command):
    command_type: Literal[CommandType.FILL]
    color: tuple[int, int, int]
    brightness: float


class StopCommand(Command):
    command_type: Literal[CommandType.STOP]
