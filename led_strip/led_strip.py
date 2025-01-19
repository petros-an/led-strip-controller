from dataclasses import dataclass

import neopixel
import logging


logger = logging.getLogger(__name__)


@dataclass
class LedStrip:
    strip: neopixel.NeoPixel
