import json
import logging
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ValidationError

import commands

logger = logging.getLogger(__name__)


class InvalidFormat(Exception):
    pass


def make_invalid_format_response(e: InvalidFormat) -> str:
    return ResponseSchema(status=Status.INVALID_INPUT, error=str(e)).model_dump_json()


def make_invalid_command_response(e: commands.InvalidCommand) -> str:
    return ResponseSchema(status=Status.INVALID_INPUT, error=str(e)).model_dump_json()


def make_execution_error_response(e: commands.CommandExecutionError) -> str:
    return ResponseSchema(status=Status.INTERNAL_ERROR, error=str(e)).model_dump_json()


def make_success_response(command_result: commands.CommandResult) -> str:
    return ResponseSchema(status=Status.OK, error=None).model_dump_json()


def parse_command(data: str) -> commands.Command:
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError:
        raise InvalidFormat("Invalid JSON format")

    try:
        command = commands.parse_command(json_data)
    except ValidationError:
        raise InvalidFormat("Invalid command format")

    return command


class Status(Enum):
    OK = "ok"
    INVALID_INPUT = "invalid_input"
    INTERNAL_ERROR = "internal_error"


class ResponseSchema(BaseModel):
    status: Status
    error: Optional[str]
