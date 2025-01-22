from commands.command import StopCommand
from commands.command_result import CommandResult
from led_strip import operations as led_strip_operations, LedStrip


def resume(led_strip: LedStrip, _: StopCommand) -> CommandResult:
    led_strip_operations.clear(led_strip)
    return CommandResult()


def reset(led_strip: LedStrip) -> None:
    pass
