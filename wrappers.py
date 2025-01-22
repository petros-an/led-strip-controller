from os import getenv
from unittest.mock import Mock

TESTING = getenv("TESTING") == "1"
if TESTING:

    class _NeoPixel:
        def __init__(self, *args, **kwargs):
            self.strip = Mock()
            self.fill = Mock()

        def __enter__(self):
            return _NeoPixel()

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    neopixel = Mock(NeoPixel=_NeoPixel)
    board = Mock()
else:
    import neopixel as _neopixel

    neopixel = _neopixel
    import board as _board

    board = _board
