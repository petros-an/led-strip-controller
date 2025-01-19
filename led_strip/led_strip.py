from contextlib import contextmanager
from dataclasses import dataclass

import board
import neopixel
import logging

from led_strip import operations

logger = logging.getLogger(__name__)


@dataclass
class LedStrip:
    strip: neopixel.NeoPixel


def perform_startup_animation(led_strip: LedStrip) -> None:
    logger.info("Performing startup animation")
    brightness = 0.01
    for _ in range(5):
        operations.fill(led_strip, (0, 0, 0), brightness)

    operations.clear(led_strip)


@contextmanager
def set_up_led_strip(led_number: int, pin: str) -> LedStrip:
    board_pin = getattr(board, pin)
    with neopixel.NeoPixel(board_pin, led_number) as neopixel_strip:
        led_strip = LedStrip(neopixel_strip)
        perform_startup_animation(led_strip)
        try:
            yield led_strip
        finally:
            logger.info("Turning off led strip")
