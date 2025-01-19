from commands.command import Command, TestCommand, StopCommand, FillCommand
from commands.command_result import CommandResult
from commands.exceptions import InvalidCommand
from led_strip.led_strip import LedStrip
from commands import fill as fill_command
from commands import test as test_command
from commands import stop as stop_command


def execute_command(led_strip: LedStrip, command: Command) -> CommandResult:
    if isinstance(command, TestCommand):
        return test_command.run()
    elif isinstance(command, StopCommand):
        return stop_command.run(led_strip)
    elif isinstance(command, FillCommand):
        return fill_command.run(led_strip, command.color, command.brightness)
    else:
        raise InvalidCommand
