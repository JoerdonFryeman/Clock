import os, socket, platform
from time import sleep, time
from datetime import datetime
from configuration import error, curs_set, init_pair, use_default_colors, color_pair, wrapper, Configuration


class Settings(Configuration):
    """Класс общих методов и параметров программы."""

    __slots__ = ('logo_y', 'logo_x', 'info_y', 'info_x', 'example_y', 'example_x', 'colors_dict')

    def __init__(self, logo_y=2, logo_x=2, info_y=2, info_x=26, example_y=12, example_x=26):
        super().__init__()
        self.logo_y: int = logo_y
        self.logo_x: int = logo_x
        self.info_y: int = info_y
        self.info_x: int = info_x
        self.example_y: int = example_y
        self.example_x: int = example_x

        self.colors_dict: dict[str, int] = {
            'WHITE': 1, 'YELLOW': 2, 'RED': 3, 'GREEN': 4, 'BLUE': 5, 'CYAN': 6, 'MAGENTA': 7, 'BLACK': 8
        }

    @staticmethod
    def visualize_symbol(stdscr, height: int, y: int, x: int, symbol: str, color: object) -> None:
        """
        Метод визуализирует символьное изображение.

        :param stdscr: Объект курсор окна.
        :param height: Высота символа.
        :param y: Координаты расположения по вертикали.
        :param x: Координаты расположения по горизонтали.
        :param symbol: Текстовое изображение.
        :param color: Цвет изображения.
        """
        for i in range(height):
            try:
                stdscr.addstr(i + y, x, symbol[i], color)
            except error:
                pass

    def paint(self, color: str) -> object:
        """
        Метод раскрашивает текст или текстовое изображение.

        :param color: Цвет изображения.
        :return: Объект color_pair.
        """
        for i in range(len(list(self.colors_dict.keys()))):
            init_pair(1 + i, self.verify_color(list(self.colors_dict.keys())[0 + i]), -1)
        return color_pair(self.colors_dict[color])


class Logo(Settings):
    """Класс визуализации текстового изображения логотипа."""

    def visualize_logo(self, stdscr) -> None:
        """
        Метод визуализирует текстовое изображение логотипа.

        :param stdscr: Объект курсор окна.
        """
        logos = self.get_json_data('logos')
        try:
            logo = logos[self.verify_os()]
            self.visualize_symbol(stdscr, len(logo), self.logo_y, self.logo_x, logo, self.paint(self.logo_color))
        except KeyError:
            try:
                stdscr.addstr(self.logo_y + 5, self.logo_x + 5, '¯\\_(`-`)_/¯', self.paint(self.logo_color))
            except error:
                pass


class Info(Settings):
    """Класс получения и отображения информации о системе."""

    @staticmethod
    def create_system_info(language='ru') -> dict[str]:
        """
        Метод получает информацию о системе на указанном языке.

        :param language: Язык отображения информации о системе.
        :return: Словарь с информацией о системе.
        """
        username_and_host = f"{os.getlogin()}@{platform.node()}"
        info = {
            "ru": {
                "Пользователь: ": username_and_host,
                "": '─' * (len(username_and_host) + 14),
                "ОС: ": platform.system(),
                "Версия ОС: ": platform.release(),
                "Архитектура: ": platform.architecture()[0],
                "Машина: ": platform.machine(),
                "Процессор: ": platform.processor(),
                "Версия Python: ": platform.python_version(),
                "IP-адрес: ": socket.gethostbyname(platform.node())
            },
            "us": {
                "User: ": username_and_host,
                "": '─' * (len(username_and_host) + 6),
                "OS: ": platform.system(),
                "OS Version: ": platform.release(),
                "Architecture: ": platform.architecture()[0],
                "Machine: ": platform.machine(),
                "Processor: ": platform.processor(),
                "Python Version: ": platform.python_version(),
                "IP address: ": socket.gethostbyname(platform.node())
            }
        }
        if language not in ['ru', 'us']:
            language = 'ru'
        return info[language]

    def visualize_system_info(self, stdscr) -> None:
        """
        Метод визуализирует информацию о системе.

        :param stdscr: Объект курсор окна.
        """
        system_info_data: dict[str] = self.create_system_info(self.language).items()
        system_info: list[str] = [f"{key}{value}" for key, value in system_info_data]
        for i in range(len(system_info_data)):
            try:
                stdscr.addstr(self.info_y + i, self.info_x, str(system_info[i]), self.paint(self.info_color))
            except error:
                pass

    def visualize_colors_example(self, stdscr) -> None:
        """
        Метод визуализирует поддерживаемые программой цвета.

        :param stdscr: Объект курсор окна.
        """
        for i in range(len(list(self.colors_dict.keys()))):
            init_pair(1 + i, self.verify_color(list(self.colors_dict.keys())[0 + i]), -1)
            try:
                stdscr.addstr(self.example_y, self.example_x + i * 2, '██', color_pair(1 + i))
            except error:
                pass


class Clock(Settings):
    """Класс визуализации текстовых изображений цифр."""

    def visualize_digits(self, stdscr) -> None:
        """
        Метод визуализирует текстовые изображения цифр.

        :param stdscr: Объект курсор окна.
        """
        color = self.paint(self.digits_color)
        digits_height_coordinates = lambda: 15 if self.system_info else 8
        y = digits_height_coordinates()
        x = (2, 18, 35), (40, 56, 73), (78, 94, 73)

        digits = self.get_json_data('digits')
        current_time = f'{datetime.now():%H}', f'{datetime.now():%M}', f'{datetime.now():%S}'

        for i in range(3):
            self.visualize_symbol(stdscr, len(digits), y, x[i - 1][0], digits[current_time[i - 1][0]], color)
            self.visualize_symbol(stdscr, len(digits), y, x[i - 1][1], digits[current_time[i - 1][1]], color)
            if i == 1 or i == 2:
                self.visualize_symbol(stdscr, len(digits), y, x[i - 1][2], digits['points'], color)


class RunProgram(Clock, Logo, Info):
    """Класс запуска всех компонентов программы."""

    def run_program(self, stdscr) -> None:
        """
        Метод запускает все компоненты программы.

        :param stdscr: Объект курсор окна.
        """
        for _ in range(1_000_000_000):
            start_time = time()
            curs_set(False), use_default_colors()

            if self.system_info:
                self.visualize_logo(stdscr)
                self.visualize_system_info(stdscr)
                self.visualize_colors_example(stdscr)
            self.visualize_digits(stdscr)

            stdscr.refresh()
            elapsed_time = time() - start_time
            time_to_sleep = 0.25 - elapsed_time

            if time_to_sleep > 0:
                sleep(time_to_sleep)

    def get_clock_wrapper(self) -> object:
        """
        Метод формирует обёртку экрана.

        :return: Возвращает обёртку экрана.
        """
        return wrapper(self.run_program)
