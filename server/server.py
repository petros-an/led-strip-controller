import asyncio
import logging
from contextlib import contextmanager

from dataclasses import dataclass
from typing import Iterator, Callable


import commands

import led_strip
from commands import continue_execution
from led_strip import LedStrip

from server import schema, websocket_server

logger = logging.getLogger(__name__)


@dataclass
class Server:
    led_strip: led_strip.LedStrip
    host: str
    port: int


@contextmanager
def set_up_server_with_led_strip(
    host: str, port: int, led_number: int, pin: str
) -> Iterator[Server]:
    with led_strip.set_up_led_strip(led_number, pin) as led_strip_instance:
        yield Server(led_strip_instance, host, port)


def handle_message(data: str, strip: LedStrip) -> str:
    try:
        command = schema.parse_command(data)
    except schema.InvalidFormat as e:
        return schema.make_invalid_format_response(e)

    try:
        result = commands.execute_command(strip, command)
        return schema.make_success_response(result)

    except commands.InvalidCommand as e:
        return schema.make_invalid_command_response(e)
    except commands.CommandExecutionError as e:
        return schema.make_execution_error_response(e)


def make_message_handler(led_strip: LedStrip) -> Callable[[str], str]:
    def message_handler(data: str) -> str:
        return handle_message(data, led_strip)

    return message_handler


async def resume_execution_periodically(led_strip: LedStrip, period: float) -> None:
    while True:
        await asyncio.sleep(period)
        continue_execution(led_strip)


async def run_server(server: Server) -> None:
    handler = make_message_handler(server.led_strip)
    asyncio.create_task(resume_execution_periodically(server.led_strip, 0.1))
    await websocket_server.serve_forever(server.host, server.port, handler)
