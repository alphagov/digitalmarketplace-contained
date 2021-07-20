import os
import sys
import traceback
from colored import fg, bg, attr  # type: ignore
from typing import NoReturn


def display_status_banner(status_text: str) -> None:
    print(f"{fg('white')}{bg('blue')}{attr('bold')} {status_text} {attr('reset')}")


def exit_with_error_message(exception: Exception) -> NoReturn:
    exception_message: str = str(exception)
    print(
        f"{fg('white')}{bg('red')}{attr('bold')} "
        f"An error has occurred and the program is terminating {os.linesep} Error: {exception_message} "
        f"{attr('reset')}")
    print(traceback.format_exc())
    sys.exit(exception_message)
