import socket
import logging

logger = logging.getLogger(__name__)


def accept_connection(sock: socket.socket) -> socket.socket:
    logger.info("Waiting for connection")
    conn, _ = sock.accept()
    logger.info(f"Accepted connection from {conn.getpeername()}")
    return conn


def read_from_connection(connection: socket.socket) -> str:
    data = connection.recv(256).decode("utf-8")
    logger.debug(f"Received >> {data}")
    return data


def close_connection(connection: socket.socket) -> None:
    connection.close()


def respond(connection: socket.socket, response: str) -> None:
    connection.sendall(response.encode("utf-8"))
