import os, socket, platform, psutil
from time import sleep, time
from datetime import datetime
from configuration import error, curs_set, init_pair, use_default_colors, color_pair, wrapper, Configuration


class Settings(Configuration):
    """Класс общих методов и параметров программы."""

    __slots__ = (
        'logo_y', 'logo_x', 'name_y', 'name_x', 'info_y', 'info_x', 'info_temp_y', 'info_temp_x',
        'git_y', 'git_x', 'example_y', 'example_x', 'digits_y', 'digits_x', 'colors_dict'
    )

    def __init__(
            self, logo_y=1, logo_x=6, name_y=1, name_x=77, info_y=1, info_x=31, info_temp_y=2, info_temp_x=77, git_y=10,
            git_x=31, example_y=10, example_x=77, digits_y=13, digits_x=((1, 17, 34), (39, 55, 72), (77, 93, 72))
    ):
        super().__init__()
        self.logo_y: int = logo_y
        self.logo_x: int = logo_x

        self.name_y: int = name_y
        self.name_x: int = name_x

        self.info_y: int = info_y
        self.info_x: int = info_x

        self.info_temp_y: int = info_temp_y
        self.info_temp_x: int = info_temp_x

        self.git_y: int = git_y
        self.git_x: int = git_x

        self.example_y: int = example_y
        self.example_x: int = example_x

        self.digits_y: int = digits_y
        self.digits_x: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] = digits_x

        self.colors_dict: dict[str, int] = {
            'MAGENTA': 1, 'BLUE': 2, 'CYAN': 3, 'GREEN': 4, 'YELLOW': 5, 'RED': 6, 'WHITE': 7, 'BLACK': 8
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

    now = datetime.now()
    date = f'{now.day}.{now.month}.{now.year}'

    @staticmethod
    def verify_system_info(system_info) -> str:
        if system_info:
            return system_info
        return '¯\\_(`-`)_/¯'

    def create_system_info(self, language='ru') -> dict[str]:
        """
        Метод получает информацию о системе на указанном языке.

        :param language: Язык отображения информации о системе.
        :return: Словарь с информацией о системе.
        """
        get_login = os.getlogin()
        platform_node = platform.node()
        platform_system = platform.system()
        platform_release = platform.release()
        platform_architecture = platform.architecture()[0]
        platform_machine = platform.machine()
        platform_processor = platform.processor()
        socket_gethostbyname = socket.gethostbyname(platform.node())

        verify_login = lambda: get_login if len(get_login) < 15 else 'user'
        verify_platform = lambda: platform_node if len(platform_node) < 15 else 'computer'
        info = {
            "ru": {
                "": self.verify_system_info(f"{verify_login()}@{verify_platform()}"),
                "─": "─" * (len(self.verify_system_info(f"{verify_login()}@{verify_platform()}")) - 1),
                "ОС: ": self.verify_system_info(platform_system),
                "Версия ОС: ": self.verify_system_info(platform_release),
                "Архитектура: ": self.verify_system_info(platform_architecture),
                "Машина: ": self.verify_system_info(platform_machine),
                "Процессор: ": self.verify_system_info(platform_processor),
                "IP-адрес: ": self.verify_system_info(socket_gethostbyname)
            },
            "en": {
                "": self.verify_system_info(f"{verify_login()}@{verify_platform()}"),
                "─": "─" * (len(self.verify_system_info(f"{verify_login()}@{verify_platform()}")) - 1),
                "OS: ": self.verify_system_info(platform_system),
                "OS Version: ": self.verify_system_info(platform_release),
                "Architecture: ": self.verify_system_info(platform_architecture),
                "Machine: ": self.verify_system_info(platform_machine),
                "Processor: ": self.verify_system_info(platform_processor),
                "IP address: ": self.verify_system_info(socket_gethostbyname)
            }
        }
        if language not in ['ru', 'en']:
            language = 'ru'
        return info[language]

    @staticmethod
    def verify_hardware(temperature, hw_first: str, hw_second: str) -> str:
        if hw_first in temperature:
            return hw_first
        elif hw_second in temperature:
            return hw_second
        raise error

    def get_temperature_info(self):
        temperature = psutil.sensors_temperatures()
        cpu = temperature.get(self.verify_hardware(temperature, 'k10temp', 'coretemp'), [])[0].current
        gpu = temperature.get(self.verify_hardware(temperature, 'amdgpu', 'nvidia'), [])[0].current
        ram = temperature.get('spd5118', [])[0].current
        storage = temperature.get(self.verify_hardware(temperature, 'nvme', 'sd'), [])[0].current
        motherboard = temperature.get('acpitz', [])[0].current
        return cpu, gpu, ram, storage, motherboard

    def create_temperature_info(self, language='ru') -> dict[str]:
        temperature = self.get_temperature_info()
        info = {
            "ru": {
                "─": "─" * (len(self.date) + 16),
                "Темп. процессора: ": f"{self.verify_system_info(temperature[0]):.1f}°C",
                "Темп. видеокарты: ": f"{self.verify_system_info(temperature[1]):.1f}°C",
                "Темп. оп. памяти: ": f"{self.verify_system_info(temperature[2]):.1f}°C",
                "Темп. накопителя: ": f"{self.verify_system_info(temperature[3]):.1f}°C",
                "Темп. мат. платы: ": f"{self.verify_system_info(temperature[4]):.1f}°C"
            },
            "us": {
                "─": "─" * (len(self.date) + 16),
                "CPU temperature: ": f"{self.verify_system_info(temperature[0]):.1f}°C",
                "GPU temperature: ": f"{self.verify_system_info(temperature[1]):.1f}°C",
                "RAM temperature: ": f"{self.verify_system_info(temperature[2]):.1f}°C",
                "Storage temper.: ": f"{self.verify_system_info(temperature[3]):.1f}°C",
                "Mot. b. temper.: ": f"{self.verify_system_info(temperature[4]):.1f}°C"
            }
        }
        if language not in ['ru', 'us']:
            language = 'ru'
        return info[language]

    def verify_name_length(self) -> int:
        length = len(self.date)
        if 7 < length < 12:
            return {11: lambda: 79, 10: lambda: 80, 9: lambda: 81, 8: lambda: 82}[length]()
        raise KeyError(f'Ошибка текущей даты: "{self.date}"!')

    def visualize_info(self, stdscr) -> None:
        """
        Метод визуализирует информацию о системе.

        :param stdscr: Объект курсор окна.
        """
        system_info_data: dict[str] = self.create_system_info(self.language).items()
        system_info: list[str] = [f"{key}{value}" for key, value in system_info_data]
        stdscr.addstr(self.git_y, self.git_x, 'https://github.com/JoerdonFryeman/Clock', self.paint(self.info_color))
        if self.temperature_info:
            temperature_info_data: dict[str] = self.create_temperature_info(self.language).items()
            temperature_info: list[str] = [f"{key}{value}" for key, value in temperature_info_data]
            for i in range(len(temperature_info_data)):
                try:
                    stdscr.addstr(
                        self.info_temp_y + i, self.info_temp_x, str(temperature_info[i]),
                        self.paint(self.info_color)
                    )
                except error:
                    pass
        try:
            name_x = lambda: self.name_x if self.temperature_info else self.verify_name_length()
            stdscr.addstr(self.name_y, name_x(), f'{self.date} | ЭЛЕКТРОНИКА 54', self.paint(self.digits_color))
        except error:
            pass
        for i in range(len(system_info_data)):
            try:
                stdscr.addstr(
                    self.info_y + i, self.info_x, str(system_info[i]), self.paint(self.info_color)
                )
            except error:
                pass

    def visualize_colors_example(self, stdscr) -> None:
        """
        Метод визуализирует поддерживаемые программой цвета.

        :param stdscr: Объект курсор окна.
        """
        for i in range(6):
            init_pair(1 + i, self.verify_color(list(self.colors_dict.keys())[0 + i]), -1)
            try:
                stdscr.addstr(self.example_y, self.example_x + i * 4, '████', color_pair(1 + i))
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
        digits_height = lambda: self.digits_y if self.system_info else self.digits_y - 6
        y, x = digits_height(), self.digits_x
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
                self.visualize_info(stdscr)
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
