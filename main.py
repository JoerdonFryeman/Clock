from os import system
from time import sleep
from keyboard import press
from keyboard import release
from threading import Thread
from keyboard import press_and_release
from clock import ClockWork

cl = ClockWork()


def press_symbol(value) -> None:
    """Increases or decreases transparency"""
    for i in range(value):
        press_and_release("-")


def get_consistency() -> None:
    """Passes the transparency level value as an argument"""
    press('ctrl+shift')
    press_symbol(int(cl.consistency))
    release('ctrl+shift')


def main() -> None:
    """Entry point"""
    system('cls')
    get_consistency()
    Thread(target=cl.run_function).start()
    Thread(target=cl.command_time).start()
    Thread(target=cl.break_function).start()
    input()
    sleep(0.3)


if __name__ == '__main__':
    main()
