from os import system
from time import sleep
from keyboard import press
from keyboard import release
from threading import Thread
from bext import hide, title
from datetime import datetime
from visual import settings, Visual
from keyboard import press_and_release

hide()
title("Электроника 54")


class ClockWork(Visual):
    """Watch movement class"""

    switch = False

    def __init__(self):
        self.settings = settings

    @staticmethod
    def press_release(value) -> None:
        """Increases or decreases transparency"""
        for i in range(value):
            press_and_release("-")

    def consistency(self) -> None:
        """Passes the transparency level value as an argument"""
        press('ctrl+shift')
        self.press_release(int(self.settings[1]))
        release('ctrl+shift')

    def breaker(self) -> None:
        """Exit function"""
        input()
        self.switch = True
        press_and_release('enter')

    def runner(self) -> None:
        """Start function"""
        self.switch = False

    def coords_of_number(self, value, one, two, three) -> None:
        """Numeric coordinates"""
        self.number(value[0], one, three)
        self.number(value[1], two, three)

    def command_time(self) -> None:
        """System time function"""
        coords = (85, 101, 45, 61, 5, 21, 10)

        while not self.switch:
            self.coords_of_number(f'{datetime.now():%S}', coords[0], coords[1], coords[6])
            self.coords_of_number(f'{datetime.now():%M}', coords[2], coords[3], coords[6])
            self.coords_of_number(f'{datetime.now():%H}', coords[4], coords[5], coords[6])

    def main(self) -> None:
        """Entry point"""
        system('cls')
        self.consistency()
        Thread(target=self.runner).start()
        Thread(target=self.command_time).start()
        Thread(target=self.breaker).start()
        input()
        sleep(0.3)


if __name__ == '__main__':
    clock = ClockWork()
    clock.main()
