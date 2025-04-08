import os, socket, platform, psutil
from datetime import datetime
from configuration import error, init_pair, use_default_colors, color_pair, Configuration


class Base(Configuration):
    """Класс общих методов и параметров программы."""

    __slots__ = (
        'error_emoji', 'logo_y', 'logo_x', 'name_y', 'name_x', 'info_y', 'info_x', 'temp_y',
        'temp_x', 'link_y', 'link_x', 'idct_y', 'idct_x', 'dgts_y', 'dgts_x', 'colors_dict'
    )

    def __init__(
            self, logo_y=0, logo_x=0, name_y=1, name_x=77, info_y=1, info_x=32, temp_y=2, temp_x=77, link_y=10,
            link_x=32, idct_y=10, idct_x=77, dgts_y=14, dgts_x=((0, 16, 33), (38, 54, 71), (76, 92, 71))
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
        """
        Метод обновляет параметры класса.
        :return: Вызывает инициализацию заново.
        """
        return self.__init__()

    @staticmethod
    def get_date() -> str:
        """
        Метод получает текущую дату в формате 'DD.MM.YYYY'.
        :return: Текущая дата в строковом формате.
        """
        now = datetime.now()
        day, month, year = now.day, now.month, now.year
        day_and_month = lambda x: x if x > 9 else f'0{x}'
        date = f'{day_and_month(day)}.{day_and_month(month)}.{year}'
        return date

    @staticmethod
    def verify_language(language: str) -> str:
        """
        Метод проверяет язык и возвращает 'ru', если язык не поддерживается.

        :param language: Язык для проверки.
        :return: Поддерживаемый язык ('ru' или 'en').
        """
        if language not in ['ru', 'en']:
            language = 'ru'
        return language

    @staticmethod
    def visualize_symbols(stdscr, height: int, y: int, x: int, symbol: dict[str: dict[str]], color: object) -> None:
        """
        Метод отображает символы на экране.

        :param stdscr: Объект стандартного экрана для отображения символов.
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

        :raises KeyError: Если указанный цвет не найден в словаре цветов.
        """
        for i, color_name in enumerate(self.colors_dict.keys()):
            use_default_colors()
            init_pair(1 + i, self.verify_color(color_name), -1)
        if color not in self.colors_dict:
            raise KeyError(f'Цвет "{color}" не найден в доступных цветах!')
        return color_pair(self.colors_dict[color])

    def get_info_list(self, function) -> list[str]:
        """
        Метод получает список строковой информации на основе переданной функции.

        :param function: Функция, которая возвращает словарь с информацией для отображения.
        :return: Список строк, каждая из которых содержит ключ и значение из словаря.
        """
        return [f"{key}{value}" for key, value in function(self.language).items()]


class LogoModule(Base):
    """Класс визуализации текстового изображения логотипа."""

    def get_logo(self, stdscr) -> None:
        """
        Метод получает и отображает логотип на экране.
        :param stdscr: Объект стандартного экрана для отображения логотипа.
        """
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
        """
        Метод отображает название и ссылку на проект на экране.
        :param stdscr: Объект стандартного экрана для отображения названия и ссылки.
        """
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
        """
        Получает информацию о системе.
        :return: Кортеж с информацией о пользователе, узле, системе, версии ОС, архитектуре, машине, процессоре и IP.
        """
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
        """
        Проверяет и обрезает информацию до заданной длины.

        :param info: Информация для проверки.
        :param max_length: Максимальная длина строки.

        :return: Проверенная и обрезанная информация или символ ошибки.
        """
        if info:
            if isinstance(info, str):
                if len(info) <= max_length:
                    return info
                return f'{info[:max_length + 9]}...'
            return self.error_emoji
        return self.error_emoji

    def create_system_info(self, language: str = 'ru') -> dict[str]:
        """
        Создает словарь с информацией о системе на заданном языке.

        :param language: Язык для отображения информации ('ru' или 'en').
        :return: Словарь с информацией о системе на выбранном языке.
        """
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
                "IP-адрес: ": f"{self.verify_info(self.info[7])}{' ' * 9}"
            },
            "en": {
                "": f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}',
                "─": "─" * (len(f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}') - 1),
                "OS: ": self.verify_info(self.info[2]),
                "OS Version: ": self.verify_info(self.info[3]),
                "Architecture: ": self.verify_info(self.info[4]),
                "Machine: ": self.verify_info(self.info[5]),
                "Processor: ": self.verify_info(self.info[6]),
                "IP address: ": f"{self.verify_info(self.info[7])}{' ' * 9}"
            }
        }
        return info[self.verify_language(language)]

    def visualize_system_info(self, stdscr) -> None:
        """
        Отображает информацию о системе на экране.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        data = self.get_info_list(self.create_system_info)
        self.visualize_symbols(stdscr, len(data), self.info_y, self.info_x, data, self.paint(self.info_color))


class TemperatureModule(Base):
    """Класс получения и отображения информации о температуре."""

    def __init__(self):
        super().__init__()
        self.temperature = self.get_temperature_info()

    @staticmethod
    def verify_hardware(first: str, second: str) -> float | None:
        """
        Проверяет наличие датчиков температуры и возвращает текущую температуру.

        :param first: Имя первого датчика температуры.
        :param second: Имя второго датчика температуры.

        :return: Текущая температура в градусах Цельсия или None, если датчик не найден.
        """
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
        """
        Получает информацию о температуре различных компонентов системы.
        :return: Кортеж с температурой процессора, видеокарты, оперативной памяти, накопителя и материнской платы.
        """
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
        """
        Создает словарь с информацией о температуре на заданном языке.

        :param language: Язык для отображения информации ('ru' или 'en').
        :return: Словарь с информацией о температуре на выбранном языке.
        """
        verify_temperature_info = lambda x: f'{x:.1f}°C' if x else self.error_emoji
        info = {
            "ru": {
                "─": "─" * 26,
                "Температура ЦПУ: ": verify_temperature_info(self.temperature[0]),
                "Температура ГПУ: ": verify_temperature_info(self.temperature[1]),
                "Температура ОЗУ: ": verify_temperature_info(self.temperature[2]),
                "Тмп. накопителя: ": verify_temperature_info(self.temperature[3]),
                "Тмп. мат. платы: ": verify_temperature_info(self.temperature[4])
            },
            "en": {
                "─": "─" * 26,
                "CPU temperature: ": verify_temperature_info(self.temperature[0]),
                "GPU temperature: ": verify_temperature_info(self.temperature[1]),
                "RAM temperature: ": verify_temperature_info(self.temperature[2]),
                "Storage t.     : ": verify_temperature_info(self.temperature[3]),
                "Motherboard t. : ": verify_temperature_info(self.temperature[4])
            }
        }
        return info[self.verify_language(language)]

    def visualize_temperature_info(self, stdscr) -> None:
        """
        Отображает информацию о температуре на экране.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        data = self.get_info_list(self.create_temperature_info)
        self.visualize_symbols(stdscr, len(data), self.temp_y, self.temp_x, data, self.paint(self.info_color))

    def visualize_temperature_indicator(self, stdscr, indicators_value: int) -> None:
        """
        Отображает индикатор температуры на экране.

        :param stdscr: Объект стандартного экрана для отображения индикатора.
        :param indicators_value: Значение индикатора температуры.
        """
        for i in range(6):
            try:
                verify_item = lambda x: '█████' if i < indicators_value else '     '
                stdscr.addstr(self.idct_y, self.idct_x + i * 5, verify_item(i), color_pair(1 + i))
            except error:
                pass

    def calculate_average_temperature(self) -> int | float | None:
        """
        Вычисляет среднюю температуру.
        :return: Средняя температура. Если допустимых значений нет, возвращает 0.
        """
        valid_temperatures = [i for i in self.temperature if isinstance(i, (int, float))]

        if not valid_temperatures:
            return None
        return sum(valid_temperatures) / len(valid_temperatures)

    def verify_temperature_indicator(self, stdscr) -> None:
        """
        Проверяет среднюю температуру и отображает соответствующий индикатор.
        :param stdscr: Объект стандартного экрана для отображения индикатора температуры.
        """
        average_temperature = self.calculate_average_temperature()
        thresholds = ((0, 40, 1), (40, 45, 2), (45, 50, 3), (50, 55, 4), (55, 60, 5), (60, 100, 6))
        try:
            for lower, upper, indicator in thresholds:
                if lower <= average_temperature < upper:
                    self.visualize_temperature_indicator(stdscr, indicator)
                    return
            self.visualize_temperature_indicator(stdscr, 0)
        except TypeError:
            self.visualize_temperature_indicator(stdscr, 0)


class ClockModule(Base):
    """Класс визуализации текстовых изображений цифр."""

    def visualize_digits(self, stdscr) -> None:
        """
        Отображает текстовые изображения цифр текущего времени на экране.
        :param stdscr: Объект стандартного экрана для отображения цифр.
        """
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
