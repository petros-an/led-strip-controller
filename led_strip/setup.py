from contextlib import contextmanager
from typing import Iterator

from led_strip.operations import set_brightness
from wrappers import neopixel, board

import logging

from led_strip.led_strip import LedStrip
from led_strip.startup_animation import perform_startup_animation

logger = logging.getLogger(__name__)


@contextmanager
def set_up_led_strip(led_number: int, pin: str) -> Iterator[LedStrip]:
    board_pin = getattr(board, pin)
    with neopixel.NeoPixel(board_pin, led_number, auto_write=False) as neopixel_strip:
        led_strip = LedStrip(neopixel_strip)
        perform_startup_animation(led_strip)
        set_brightness(led_strip, 1)
        try:
            yield led_strip
        finally:
            logger.info("Turning off led strip")
