import socket
import logging
from contextlib import contextmanager
from typing import Iterator

logger = logging.getLogger(__name__)


class NoDataRead(Exception):
    pass


@contextmanager
def set_up_socket(
    host: str,
    port: int,
) -> Iterator[socket.socket]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        sock.settimeout(0.1)
        logger.info(f"Listening on {host}:{port}")
        try:
            yield sock
        finally:
            logger.info("Exiting server")


def accept_connection(sock: socket.socket) -> socket.socket:
    logger.info("Waiting for connection")
    try:
        conn, _ = sock.accept()
    except TimeoutError:
        raise NoDataRead
    logger.info(f"Accepted connection from {conn.getpeername()}")
    return conn


def read_from_connection(connection: socket.socket) -> str:
    try:
        data = connection.recv(256).decode("utf-8")
        logger.debug(f"Received >> {data}")
    except OSError:
        raise NoDataRead
    return data


def close_connection(connection: socket.socket) -> None:
    connection.close()


def respond(connection: socket.socket, response: str) -> None:
    connection.sendall(response.encode("utf-8"))
