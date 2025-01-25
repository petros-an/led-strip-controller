from enum import Enum
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
    SET_BRIGHTNESS = "set_brightness"
    PULSE = "pulse"
    RANDOM_WALK = "random_walk"
