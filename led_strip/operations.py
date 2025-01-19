import logging
from led_strip.led_strip import LedStrip

logger = logging.getLogger(__name__)


def fill(led_strip: LedStrip, color: tuple[int, int, int], brightness: float) -> None:
    logger.info(f"Filling strip with color {color} and brightness {brightness}")
    led_strip.strip.brightness = brightness
    led_strip.strip.fill(color)


def clear(led_strip: LedStrip) -> None:
    logger.info("Clearing led strip")
    fill(led_strip, (0, 0, 0), 0)
