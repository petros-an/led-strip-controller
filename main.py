import logging
import click

from server import set_up_server_with_led_strip, run_server

def setup_logging(log_level: str) -> None:
    logging.basicConfig(level=log_level.upper())



@click.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=6543)
@click.option("--led_number", default=300)
@click.option("--pin", default="D18")
@click.option("--log_level", default="info")
def main(host: str, port: int, led_number: int, pin: str, log_level: str) -> None:
    setup_logging(log_level)
    with set_up_server_with_led_strip(host, port, led_number, pin) as server:
        run_server(server)


if __name__ == "__main__":
    main()
