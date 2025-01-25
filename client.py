import asyncio
import json
import random
from typing import Any

import click
from websockets.asyncio.client import connect


async def send_command(command: str, url: str) -> None:
    data: dict[str, Any]
    match command:
        case "fill":
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            data = {"command": {"command_type": "fill", "color": [r, g, b]}}
        case "stop":
            data = {"command": {"command_type": "stop"}}
        case "test":
            data = {"command": {"command_type": "test"}}
        case "rotate":
            data = {"command": {"command_type": "rotate"}}
        case "set_brightness":
            data = {
                "command": {
                    "command_type": "set_brightness",
                    "brightness": random.random(),
                }
            }
        case "pulse":
            data = {"command": {"command_type": "pulse", "speed": 1}}
        case _:
            raise ValueError(f"Unknown command: {command}")

    async with connect(url) as websocket:
        print(f"->>> {json.dumps(data)}")
        await websocket.send(json.dumps(data))
        message = await websocket.recv()
        print(message)


@click.command()
@click.option("--command", default="fill")
@click.option("--url", default="ws://localhost:6543")
def main(command: str, url: str) -> None:
    asyncio.run(send_command(command, url))


if __name__ == "__main__":
    main()
