from typing import Any
from unittest.mock import Mock, call

import pytest

from commands.set_brightness import SetBrightnessCommand
from commands.stop import StopCommand
from commands.test import TestCommand

from commands.fill import FillCommand


from commands.rotate import RotateCommand
from commands import execute_command, rotate, parse_command, fill
from commands.command import CommandType, Command
from led_strip import LedStrip
from pytest import MonkeyPatch


def test_fill_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", m := Mock())
    strip = LedStrip(Mock())
    command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
    )
    execute_command(strip, command)
    m.assert_called_once_with(strip, (255, 0, 0))


def test_rotate_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", m := Mock())
    strip = LedStrip(Mock())
    command = RotateCommand(
        command_type=CommandType.ROTATE,
    )
    execute_command(strip, command)
    m.assert_called_once()


def test_stop_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.clear", mock_clear := Mock())
    strip = LedStrip(Mock())
    fill_command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
    )
    execute_command(strip, fill_command)
    command = StopCommand(command_type=CommandType.STOP)
    execute_command(strip, command)
    mock_clear.assert_called_once_with(strip)


def test_change_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", mock_fill := Mock())

    strip = LedStrip(Mock())
    fill.current_color = (0, 0, 0)
    fill_command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
    )
    execute_command(strip, fill_command)
    mock_fill.assert_called_once_with(strip, (255, 0, 0))

    test_command = TestCommand(command_type=CommandType.TEST)
    execute_command(strip, test_command)
    assert rotate.step == 0


def test_rotate_command_full(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", mock_fill := Mock())
    rotate.period = 10
    strip = LedStrip(Mock())
    rotate_command = RotateCommand(
        command_type=CommandType.ROTATE,
    )
    for _ in range(9):
        execute_command(strip, rotate_command)

    assert mock_fill.call_args_list == [
        call(strip, (255, 0, 0)),
        call(strip, (255, 0, 0)),
        call(strip, (255, 0, 0)),
        call(strip, (0, 255, 0)),
        call(strip, (0, 255, 0)),
        call(strip, (0, 255, 0)),
        call(strip, (0, 0, 255)),
        call(strip, (0, 0, 255)),
        call(strip, (0, 0, 255)),
    ]

    assert rotate.step == 9


def test_set_brightness(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "led_strip.operations.set_brightness", mock_set_brightness := Mock()
    )
    strip = LedStrip(Mock())
    brightness_command = SetBrightnessCommand(
        command_type=CommandType.SET_BRIGHTNESS,
        brightness=0.5,
    )
    execute_command(strip, brightness_command)
    mock_set_brightness.assert_called_once_with(strip, 0.5)


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {"command": {"command_type": "fill", "color": [255, 0, 0]}},
            FillCommand(command_type=CommandType.FILL, color=(255, 0, 0)),
        ),
        (
            {"command": {"command_type": "stop"}},
            StopCommand(command_type=CommandType.STOP),
        ),
        (
            {"command": {"command_type": "test"}},
            TestCommand(command_type=CommandType.TEST),
        ),
        (
            {"command": {"command_type": "rotate"}},
            RotateCommand(command_type=CommandType.ROTATE),
        ),
        (
            {"command": {"command_type": "set_brightness", "brightness": 0.5}},
            SetBrightnessCommand(
                command_type=CommandType.SET_BRIGHTNESS, brightness=0.5
            ),
        ),
    ],
)
def test_parse_command(
    monkeypatch: MonkeyPatch, data: dict[str, Any], expected: Command
) -> None:
    assert parse_command(data) == expected
