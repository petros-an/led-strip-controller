import logging
from contextlib import contextmanager
import socket

from dataclasses import dataclass
from typing import ContextManager

import commands

import led_strip

from server import connection as server_connection, schema

logger = logging.getLogger(__name__)


@dataclass
class Server:
    sock: socket.socket
    led_strip: led_strip.LedStrip


@contextmanager
def set_up_socket(
    host: str,
    port: int,
) -> ContextManager[socket.socket]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        logger.info(f"Listening on {host}:{port}")
        try:
            yield sock
        finally:
            logger.info("Exiting server")


@contextmanager
def set_up_server_with_led_strip(
    host: str, port: int, led_number: int, pin: str
) -> ContextManager[Server]:
    with led_strip.set_up_led_strip(led_number, pin) as led_strip_instance:
        with set_up_socket(host, port) as sock:
            yield Server(sock, led_strip_instance)


def run_server(server: Server) -> None:
    while True:
        connection = server_connection.accept_connection(server.sock)
        data = server_connection.read_from_connection(connection)

        try:
            command = schema.parse_command(data)
            result = commands.execute_command(server.led_strip, command)
            server_connection.respond(connection, schema.make_success_response(result))

        except schema.InvalidFormat as e:
            server_connection.respond(
                connection, schema.make_invalid_format_response(e)
            )

        except commands.InvalidCommand as e:
            server_connection.respond(
                connection, schema.make_invalid_command_response(e)
            )

        except commands.CommandExecutionError as e:
            server_connection.respond(
                connection, schema.make_execution_error_response(e)
            )

        server_connection.close_connection(connection)
