from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wrappers import neopixel

import logging


logger = logging.getLogger(__name__)


@dataclass
class LedStrip:
    strip: "neopixel.NeoPixel"  # type: ignore[name-defined]
