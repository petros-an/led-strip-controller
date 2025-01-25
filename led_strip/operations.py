import logging
from led_strip.led_strip import LedStrip

logger = logging.getLogger(__name__)


def fill(led_strip: LedStrip, color: tuple[int, int, int]) -> None:
    fill_no_autowrite(led_strip, color)
    write(led_strip)


def fill_no_autowrite(led_strip: LedStrip, color: tuple[int, int, int]) -> None:
    logger.info(f"Filling strip with color {color}")
    led_strip.strip.fill(color)


def clear(led_strip: LedStrip) -> None:
    logger.info("Clearing led strip")
    fill(led_strip, (0, 0, 0))
    set_brightness(led_strip, 1)


def set_brightness(led_strip: LedStrip, brightness: float) -> None:
    led_strip.strip.brightness = brightness
    write(led_strip)


def set_pixel_color_no_autowrite(
    led_strip: LedStrip, index: int, color: tuple[int, int, int]
) -> None:
    led_strip.strip[index] = color


def set_pixel_color(
    led_strip: LedStrip, index: int, color: tuple[int, int, int]
) -> None:
    led_strip.strip[index] = color
    write(led_strip)


def write(led_strip: LedStrip) -> None:
    led_strip.strip.show()
