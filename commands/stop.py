from commands.command_result import CommandResult
from led_strip import operations as led_strip_operations


def run(led_strip) -> CommandResult:
    led_strip_operations.clear(led_strip)
    return CommandResult()
