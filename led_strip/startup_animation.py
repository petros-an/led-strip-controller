from led_strip import operations
from led_strip.led_strip import LedStrip
import logging

logger = logging.getLogger(__name__)


def perform_startup_animation(led_strip: LedStrip) -> None:
    logger.info("Performing startup animation")
    brightness = 0.01
    for _ in range(5):
        operations.fill(led_strip, (0, 0, 0), brightness)

    operations.clear(led_strip)
