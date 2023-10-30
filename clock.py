from bext import goto
from datetime import datetime
from keyboard import press_and_release
from configuration import Configuration


class ClockWork(Configuration):
    switch = False

    @classmethod
    def break_function(cls):
        """Exit function"""
        input()
        cls.switch = True
        press_and_release('enter')

    @classmethod
    def run_function(cls):
        """Start function"""
        cls.switch = False

    def coord_of_number(self, value, one, two, three):
        """Numeric coordinates"""
        self.get_graphic_number(value[0], one, three)
        self.get_graphic_number(value[1], two, three)

    def command_time(self):
        """System time function"""
        # if self.width == 120 and self.height == 30:
        coordinates = (85, 101, 45, 61, 5, 21, 10)
        # else:
        #     coordinates = (
        #         int(self.width // 1.57), int(self.width // 1.36), int(self.width // 2.5),
        #         int(self.width // 2.02), int(self.width // 6.22), int(self.width // 3.90),
        #         int(self.height // 2.47)
        #     )

        while not self.switch:
            self.coord_of_number(f'{datetime.now():%S}', coordinates[0], coordinates[1], coordinates[6])
            self.coord_of_number(f'{datetime.now():%M}', coordinates[2], coordinates[3], coordinates[6])
            self.coord_of_number(f'{datetime.now():%H}', coordinates[4], coordinates[5], coordinates[6])

    def get_graphic_number(self, value, x, y):
        """Visualization function"""
        if int(value) == 0:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 1:
            goto(x, y)
            self.color.print(self.first_color + '  ████████    ')
            goto(x, y + 1)
            self.color.print(self.first_color + '  ██░░░░██    ')
            goto(x, y + 2)
            self.color.print(self.first_color + '  ████░░██    ')
            goto(x, y + 3)
            self.color.print(self.first_color + '    ██░░██    ')
            goto(x, y + 4)
            self.color.print(self.first_color + '    ██░░██    ')
            goto(x, y + 5)
            self.color.print(self.first_color + '    ██░░██    ')
            goto(x, y + 6)
            self.color.print(self.first_color + '    ██░░██    ')
            goto(x, y + 7)
            self.color.print(self.first_color + '    ██░░██    ')
            goto(x, y + 8)
            self.color.print(self.first_color + '  ████░░████  ')
            goto(x, y + 9)
            self.color.print(self.first_color + '  ██░░░░░░██  ')
            goto(x, y + 10)
            self.color.print(self.first_color + '  ██████████  ')

        if int(value) == 2:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 7)
            self.color.print(self.first_color + '██░░██        ')
            goto(x, y + 8)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 3:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 4:
            goto(x, y)
            self.color.print(self.first_color + '██████  ██████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '        ██████')

        if int(value) == 5:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██        ')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 6:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██        ')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██████████')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 7:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '        ██████')

        if int(value) == 8:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        if int(value) == 9:
            goto(x, y)
            self.color.print(self.first_color + '██████████████')
            goto(x, y + 1)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 2)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 3)
            self.color.print(self.first_color + '██░░██  ██░░██')
            goto(x, y + 4)
            self.color.print(self.first_color + '██░░██████░░██')
            goto(x, y + 5)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 6)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 7)
            self.color.print(self.first_color + '        ██░░██')
            goto(x, y + 8)
            self.color.print(self.first_color + '██████████░░██')
            goto(x, y + 9)
            self.color.print(self.first_color + '██░░░░░░░░░░██')
            goto(x, y + 10)
            self.color.print(self.first_color + '██████████████')

        # if self.width == 120 and self.height == 30:
        coordinates = (39, 79, 13, 17)
        # else:
        #     if self.width < 237 and self.height < 66:
        #         coordinates = (int(self.width // 2.75), int(self.width // 1.66),
        #                        int(self.height // 2.13), int(self.height // 1.80))
        #     else:
        #         coordinates = (int(self.width // 2.85), int(self.width // 1.69),
        #                        int(self.height // 2.35), int(self.height // 1.94))

        goto(coordinates[0], coordinates[2])
        self.color.print(self.first_color + '██')
        goto(coordinates[0], coordinates[3])
        self.color.print(self.first_color + '██')
        goto(coordinates[1], coordinates[2])
        self.color.print(self.first_color + '██')
        goto(coordinates[1], coordinates[3])
        self.color.print(self.first_color + '██')
