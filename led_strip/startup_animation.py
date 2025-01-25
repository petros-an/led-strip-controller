from random import randrange
from time import sleep

from led_strip import operations
from led_strip.led_strip import LedStrip
import logging

logger = logging.getLogger(__name__)


def perform_startup_animation(led_strip: LedStrip) -> None:
    logger.info("Performing startup animation")
    operations.set_brightness(led_strip, 0.01)
    for _ in range(5):
        r = randrange(0, 256)
        g = randrange(0, 256)
        b = randrange(0, 256)
        operations.fill(led_strip, (r, g, b))
        sleep(0.3)

    operations.clear(led_strip)
