import os
from unittest.mock import Mock, call

os.environ["TESTING"] = "1"

from commands.rotate import RotateCommand
from commands import execute_command, rotate
from commands.command import FillCommand, CommandType, TestCommand, StopCommand
from led_strip import LedStrip
from pytest import MonkeyPatch


def test_fill_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", m := Mock())
    strip = LedStrip(Mock())
    command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
        brightness=1.0,
    )
    execute_command(strip, command)
    m.assert_called_once_with(strip, (255, 0, 0), 1.0)


def test_rotate_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", m := Mock())
    strip = LedStrip(Mock())
    command = RotateCommand(
        command_type=CommandType.ROTATE,
    )
    execute_command(strip, command)
    m.assert_called_once()


def test_stop_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", mock_fill := Mock())
    monkeypatch.setattr("led_strip.operations.clear", mock_clear := Mock())
    strip = LedStrip(Mock())
    fill_command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
        brightness=1.0,
    )
    execute_command(strip, fill_command)
    mock_fill.assert_called_once_with(strip, (255, 0, 0), 1.0)

    command = StopCommand(command_type=CommandType.STOP)
    execute_command(strip, command)
    mock_clear.assert_called_once_with(strip)


def test_change_command(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("led_strip.operations.fill", mock_fill := Mock())

    strip = LedStrip(Mock())
    fill_command = FillCommand(
        command_type=CommandType.FILL,
        color=(255, 0, 0),
        brightness=1.0,
    )
    execute_command(strip, fill_command)
    mock_fill.assert_called_once_with(strip, (255, 0, 0), 1.0)

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
        call(strip, (255, 0, 0), 1.0),
        call(strip, (255, 0, 0), 1.0),
        call(strip, (255, 0, 0), 1.0),
        call(strip, (0, 255, 0), 1.0),
        call(strip, (0, 255, 0), 1.0),
        call(strip, (0, 255, 0), 1.0),
        call(strip, (0, 0, 255), 1.0),
        call(strip, (0, 0, 255), 1.0),
        call(strip, (0, 0, 255), 1.0),
    ]

    assert rotate.step == 9
