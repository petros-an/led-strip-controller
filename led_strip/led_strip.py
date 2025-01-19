from contextlib import contextmanager
from dataclasses import dataclass
from time import sleep

import board
import neopixel
import logging

logger = logging.getLogger(__name__)


@dataclass
class LedStrip:
    strip: neopixel.NeoPixel


def perform_startup_animation(led_strip: LedStrip) -> None:
    brightness = 0.01
    for _ in range(5):
        led_strip.strip.brightness = brightness
        led_strip.strip.fill((0, 0, 255))
        sleep(0.1)
        led_strip.strip.fill((0, 255, 0))
        sleep(0.1)

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
