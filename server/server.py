import logging
from contextlib import contextmanager
import socket

from dataclasses import dataclass
from typing import Iterator

import commands

import led_strip
from commands.command import CommandType
from commands.rotate import RotateCommand

from server import connection as server_connection, schema
from server.connection import set_up_socket, NoDataRead

logger = logging.getLogger(__name__)


@dataclass
class Server:
    sock: socket.socket
    led_strip: led_strip.LedStrip


@contextmanager
def set_up_server_with_led_strip(
    host: str, port: int, led_number: int, pin: str
) -> Iterator[Server]:
    with led_strip.set_up_led_strip(led_number, pin) as led_strip_instance:
        with set_up_socket(host, port) as sock:
            yield Server(sock, led_strip_instance)


def run_server(server: Server) -> None:
    commands.execute_command(
        server.led_strip, RotateCommand(command_type=CommandType.ROTATE)
    )
    while True:
        try:
            connection = server_connection.accept_connection(server.sock)
            data = server_connection.read_from_connection(connection)
        except NoDataRead:
            commands.continue_execution(server.led_strip)
            continue

        try:
            command = schema.parse_command(data)
        except schema.InvalidFormat as e:
            server_connection.respond(
                connection, schema.make_invalid_format_response(e)
            )
            server_connection.close_connection(connection)
            continue

        try:
            result = commands.execute_command(server.led_strip, command)
        except commands.InvalidCommand as e:
            server_connection.respond(
                connection, schema.make_invalid_command_response(e)
            )
            server_connection.close_connection(connection)
            continue

        except commands.CommandExecutionError as e:
            server_connection.respond(
                connection, schema.make_execution_error_response(e)
            )
            server_connection.close_connection(connection)
            continue

        server_connection.respond(connection, schema.make_success_response(result))
        server_connection.close_connection(connection)
