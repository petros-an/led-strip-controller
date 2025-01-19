import logging
import click

from server import set_up_server_with_led_strip, run_server

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=6543)
@click.option("--led_number", default=300)
@click.option("--pin", default="D18")
def main(host: str, port: int, led_number: int, pin: str) -> None:
    with set_up_server_with_led_strip(host, port, led_number, pin) as server:
        run_server(server)


if __name__ == "__main__":
    main()
