import os, socket, platform, psutil
from datetime import datetime
from configuration import error, init_pair, color_pair, Configuration


class Base(Configuration):
    """Класс общих методов и параметров программы."""

    __slots__ = (
        'error_emoji', 'logo_y', 'logo_x', 'name_y', 'name_x', 'info_y', 'info_x', 'temp_y',
        'temp_x', 'link_y', 'link_x', 'idct_y', 'idct_x', 'dgts_y', 'dgts_x', 'colors_dict'
    )

    def __init__(
            self, logo_y=1, logo_x=5, name_y=1, name_x=77, info_y=1, info_x=31, temp_y=2, temp_x=77, link_y=10,
            link_x=31, idct_y=10, idct_x=77, dgts_y=14, dgts_x=((1, 17, 34), (39, 55, 72), (77, 93, 72))
    ):
        super().__init__()
        self.error_emoji = '¯\\_(`-`)_/¯'

        self.logo_y: int = logo_y
        self.logo_x: int = logo_x

        self.name_y: int = name_y
        self.name_x: int = name_x

        self.info_y: int = info_y
        self.info_x: int = info_x

        self.temp_y: int = temp_y
        self.temp_x: int = temp_x

        self.link_y: int = link_y
        self.link_x: int = link_x

        self.idct_y: int = idct_y
        self.idct_x: int = idct_x

        self.dgts_y: int = dgts_y
        self.dgts_x: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] = dgts_x

        self.colors_dict: dict[str, int] = {
            'MAGENTA': 1, 'BLUE': 2, 'CYAN': 3, 'GREEN': 4, 'YELLOW': 5, 'RED': 6, 'WHITE': 7, 'BLACK': 8
        }

    def renew(self):
        return self.__init__()

    @staticmethod
    def get_date() -> str:
        now = datetime.now()
        day, month, year = now.day, now.month, now.year
        day_and_month = lambda x: x if x > 9 else f'0{x}'
        date = f'{day_and_month(day)}.{day_and_month(month)}.{year}'
        return date

    @staticmethod
    def verify_language(language: str) -> str:
        if language not in ['ru', 'us']:
            language = 'ru'
        return language

    @staticmethod
    def visualize_symbols(stdscr, height: int, y: int, x: int, symbol: dict[str: dict[str]], color: object) -> None:
        for i in range(height):
            try:
                stdscr.addstr(i + y, x, symbol[i], color)
            except error:
                pass

    def paint(self, color: str) -> object:
        for i in range(len(list(self.colors_dict.keys()))):
            init_pair(1 + i, self.verify_color(list(self.colors_dict.keys())[0 + i]), -1)
        return color_pair(self.colors_dict[color])

    def get_info_list(self, function) -> list[str]:
        return [f"{key}{value}" for key, value in function(self.language).items()]


class LogoModule(Base):
    """Класс визуализации текстового изображения логотипа."""

    def get_logo(self, stdscr) -> None:
        logos = self.get_json_data('logos')
        try:
            data = logos[self.verify_os()]
            self.visualize_symbols(stdscr, len(data), self.logo_y, self.logo_x, data, self.paint(self.logo_color))
        except KeyError:
            try:
                stdscr.addstr(self.logo_y + 5, self.logo_x + 5, self.error_emoji, self.paint(self.logo_color))
            except error:
                pass

    def get_name_and_link(self, stdscr) -> None:
        try:
            name = f'{self.get_date()} | ЭЛЕКТРОНИКА 54'
            link = 'https://github.com/JoerdonFryeman/Clock'
            stdscr.addstr(self.name_y, self.name_x, name, self.paint(self.digits_color))
            stdscr.addstr(self.link_y, self.link_x, link, self.paint(self.info_color))
        except error:
            pass


class InfoModule(Base):
    """Класс получения и отображения информации о системе."""

    def __init__(self):
        super().__init__()
        self.info = self.get_system_info()

    @staticmethod
    def get_system_info() -> tuple:
        login = os.getlogin()
        node = platform.node()
        system = platform.system()
        release = platform.release()
        architecture = platform.architecture()[0]
        machine = platform.machine()
        processor = platform.processor()
        host_by_name = socket.gethostbyname(platform.node())
        return login, node, system, release, architecture, machine, processor, host_by_name

    def verify_info(self, info: str, max_length: int = 16) -> str:
        if info:
            if isinstance(info, str):
                if len(info) <= max_length:
                    return info
                return f'{info[:max_length + 9]}...'
            return self.error_emoji
        return self.error_emoji

    def create_system_info(self, language: str = 'ru') -> dict[str]:
        login, node = self.verify_info(self.info[0]), self.verify_info(self.info[1])
        info = {
            "ru": {
                "": f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}',
                "─": "─" * (len(f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}') - 1),
                "ОС: ": self.verify_info(self.info[2]),
                "Версия ОС: ": self.verify_info(self.info[3]),
                "Архитектура: ": self.verify_info(self.info[4]),
                "Машина: ": self.verify_info(self.info[5]),
                "Процессор: ": self.verify_info(self.info[6]),
                "IP-адрес: ": self.verify_info(self.info[7])
            },
            "us": {
                "": f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}',
                "─": "─" * (len(f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}') - 1),
                "OS: ": self.verify_info(self.info[2]),
                "OS Version: ": self.verify_info(self.info[3]),
                "Architecture: ": self.verify_info(self.info[4]),
                "Machine: ": self.verify_info(self.info[5]),
                "Processor: ": self.verify_info(self.info[6]),
                "IP address: ": self.verify_info(self.info[7])
            }
        }
        return info[self.verify_language(language)]

    def visualize_system_info(self, stdscr) -> None:
        data = self.get_info_list(self.create_system_info)
        self.visualize_symbols(stdscr, len(data), self.info_y, self.info_x, data, self.paint(self.info_color))


class TemperatureModule(Base):
    """Класс получения и отображения информации о температуре."""

    def __init__(self):
        super().__init__()
        self.temperature = self.get_temperature_info()

    @staticmethod
    def verify_hardware(first: str, second: str) -> float | None:
        temperature = psutil.sensors_temperatures()
        try:
            if first in temperature:
                return temperature.get(first, [])[0].current
            elif second in temperature:
                return temperature.get(second, [])[0].current
            return temperature.get('acpitz', [])[0].current
        except (IndexError, TypeError):
            pass

    def get_temperature_info(self) -> tuple[float, float, float, float, float] | tuple[None, None, None, None, None]:
        try:
            cpu = self.verify_hardware('k10temp', 'coretemp')
            gpu = self.verify_hardware('amdgpu', 'nvidia')
            ram = self.verify_hardware('spd5118', '')
            storage = self.verify_hardware('nvme', '')
            motherboard = self.verify_hardware('acpitz', '')
            return cpu, gpu, ram, storage, motherboard
        except AttributeError:
            return None, None, None, None, None

    def create_temperature_info(self, language: str = 'ru') -> dict[str]:
        verify_temperature_info = lambda x: f'{x:.1f}°C' if x else self.error_emoji
        info = {
            "ru": {
                "─": "─" * 26,
                "Темп-ра процессора: ": verify_temperature_info(self.temperature[0]),
                "Темп-ра видеокарты: ": verify_temperature_info(self.temperature[1]),
                "Темп-ра оп. памяти: ": verify_temperature_info(self.temperature[2]),
                "Темп-ра накопителя: ": verify_temperature_info(self.temperature[3]),
                "Темп-ра мат. платы: ": verify_temperature_info(self.temperature[4])
            },
            "us": {
                "─": "─" * 26,
                "CPU temperature: ": verify_temperature_info(self.temperature[0]),
                "GPU temperature: ": verify_temperature_info(self.temperature[1]),
                "RAM temperature: ": verify_temperature_info(self.temperature[2]),
                "Storage temper.: ": verify_temperature_info(self.temperature[3]),
                "Mot. b. temper.: ": verify_temperature_info(self.temperature[4])
            }
        }
        return info[self.verify_language(language)]

    def visualize_temperature_info(self, stdscr) -> None:
        data = self.get_info_list(self.create_temperature_info)
        self.visualize_symbols(stdscr, len(data), self.temp_y, self.temp_x, data, self.paint(self.info_color))

    def visualize_temperature_indicator(self, stdscr, indicators_value: int) -> None:
        for i in range(6):
            try:
                verify_item = lambda x: '█████' if i < indicators_value else '     '
                stdscr.addstr(self.idct_y, self.idct_x + i * 5, verify_item(i), color_pair(1 + i))
            except error:
                pass

    def verify_temperature_indicator(self, stdscr) -> None:
        if 0 < self.temperature[0] < 40:
            self.visualize_temperature_indicator(stdscr, 1)
        elif 40 <= self.temperature[0] < 45:
            self.visualize_temperature_indicator(stdscr, 2)
        elif 45 <= self.temperature[0] < 50:
            self.visualize_temperature_indicator(stdscr, 3)
        elif 50 <= self.temperature[0] < 55:
            self.visualize_temperature_indicator(stdscr, 4)
        elif 55 <= self.temperature[0] < 60:
            self.visualize_temperature_indicator(stdscr, 5)
        elif 60 <= self.temperature[0] < 100:
            self.visualize_temperature_indicator(stdscr, 6)
        else:
            self.visualize_temperature_indicator(stdscr, 0)


class ClockModule(Base):
    """Класс визуализации текстовых изображений цифр."""

    def visualize_digits(self, stdscr) -> None:
        color = self.paint(self.digits_color)
        digits_height = lambda: self.dgts_y if self.system_info else self.dgts_y - 6
        y, x = digits_height(), self.dgts_x

        data = self.get_json_data('digits')
        current_time = f'{datetime.now():%H}', f'{datetime.now():%M}', f'{datetime.now():%S}'

        for i in range(3):
            self.visualize_symbols(stdscr, len(data), y, x[i - 1][0], data[current_time[i - 1][0]], color)
            self.visualize_symbols(stdscr, len(data), y, x[i - 1][1], data[current_time[i - 1][1]], color)
            if i == 1 or i == 2:
                self.visualize_symbols(stdscr, len(data), y, x[i - 1][2], data['points'], color)
