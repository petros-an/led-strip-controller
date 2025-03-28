import websockets
import logging

from websockets import ConnectionClosedError

logger = logging.getLogger(__name__)


class NoDataRead(Exception):
    pass


def make_websocket_connection_handler(handler):
    async def handle_websocket_connection(websocket) -> None:
        try:
            async for message in websocket:
                response = await handler(message)
                await websocket.send(response)
        except ConnectionClosedError:
            return

    return handle_websocket_connection


async def serve_forever(host: str, port: int, handler) -> None:
    connection_handler = make_websocket_connection_handler(handler)

    async with websockets.serve(connection_handler, host, port) as websock:
        await websock.serve_forever()
