import platform
from datetime import datetime

from configuration import (
    Configuration, os, error, init_pair, use_default_colors, color_pair,
    A_BOLD, COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
)


class Base(Configuration):
    """Класс общих методов и параметров программы."""

    __slots__ = (
        'error_emoji', 'logo_y', 'logo_x', 'name_y', 'name_x', 'info_y', 'info_x', 'temp_y', 'temp_x', 'version_y',
        'version_x', 'copy_right_y', 'copy_right_x', 'link_y', 'link_x', 'idct_y', 'idct_x', 'dgts_y', 'dgts_x'
    )

    def __init__(
            self, logo_y=0, logo_x=0, name_y=1, name_x=78, info_y=1, info_x=32, temp_y=2, temp_x=78, version_y=9,
            version_x=32, copy_right_y=10, copy_right_x=32, link_y=11, link_x=32, idct_y=11, idct_x=78, dgts_y=14,
            dgts_x=((0, 16, 33), (38, 54, 71), (76, 92, 71))
    ):
        super().__init__()
        self.error_emoji: str = '¯\\_(`-`)_/¯'

        self.logo_y: int = logo_y
        self.logo_x: int = logo_x

        self.name_y: int = name_y
        self.name_x: int = name_x

        self.info_y: int = info_y
        self.info_x: int = info_x

        self.temp_y: int = temp_y
        self.temp_x: int = temp_x

        self.version_y: int = version_y
        self.version_x: int = version_x

        self.copy_right_y: int = copy_right_y
        self.copy_right_x: int = copy_right_x

        self.link_y: int = link_y
        self.link_x: int = link_x

        self.idct_y: int = idct_y
        self.idct_x: int = idct_x

        self.dgts_y: int = dgts_y
        self.dgts_x: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] = dgts_x

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
        date: str = f'{day_and_month(day)}.{day_and_month(month)}.{year}'
        return date

    @staticmethod
    def verify_language(language: str) -> str:
        """
        Метод проверяет язык и возвращает 'ru', если язык не поддерживается.

        :param language: Язык для проверки.
        :return: Поддерживаемый язык ('ru' или 'en').
        """
        if language not in ['ru', 'en']:
            language: str = 'ru'
        return language

    @staticmethod
    def visualize_symbols(stdscr, height: int, y: int, x: int, symbol: list, color: object) -> None:
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

    @staticmethod
    def verify_color(color):
        """
        Метод проверяет настройку цвета из конфигурации.
        :return: COLOR_*: Цветовая константа, соответствующая цветовой конфигурации.
        """
        color_map: dict[str, object] = {
            'BLACK': COLOR_BLACK, 'BLUE': COLOR_BLUE, 'CYAN': COLOR_CYAN, 'GREEN': COLOR_GREEN,
            'MAGENTA': COLOR_MAGENTA, 'RED': COLOR_RED, 'WHITE': COLOR_WHITE, 'YELLOW': COLOR_YELLOW,
        }
        return color_map.get(color, COLOR_WHITE)

    def paint(self, color: str, a_bold: bool) -> object:
        """
        Метод раскрашивает текст или текстовое изображение.

        :param color: Цвет изображения.
        :param a_bold: A bold symbol true or false

        :return: Объект color_pair.
        :raises KeyError: Если указанный цвет не найден в словаре цветов.
        """
        colors_dict: dict[str, int] = {
            'MAGENTA': 1, 'BLUE': 2, 'CYAN': 3, 'GREEN': 4,
            'YELLOW': 5, 'RED': 6, 'WHITE': 7, 'BLACK': 8
        }
        if color not in colors_dict:
            raise KeyError(f'Цвет "{color}" не найден в доступных цветах.')
        for i, color_name in enumerate(colors_dict.keys()):
            use_default_colors()
            init_pair(1 + i, self.verify_color(color_name), -1)
        if a_bold:
            return color_pair(colors_dict[color]) | A_BOLD
        return color_pair(colors_dict[color])

    def get_info_list(self, function) -> list:
        """
        Метод получает список строковой информации на основе переданной функции.

        :param function: Функция, которая возвращает словарь с информацией для отображения.
        :return: Список строк, каждая из которых содержит ключ и значение из словаря.
        """
        return [f"{key}{value}" for key, value in function(self.language).items()]

    def verify_os(self) -> str:
        """
        Метод проверяет на какой ОС запускается программа.
        :return: Возвращает имя ОС.
        """
        if self.logo_name != '':
            return self.logo_name
        elif os.name == 'posix':
            if platform.system() == 'Linux':
                return 'Linux'
            elif platform.system() == 'Darwin':
                return 'macOS'
            return ''
        elif os.name == 'nt':
            return 'Windows'
        return ''
