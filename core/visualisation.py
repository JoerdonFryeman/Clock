from datetime import datetime

try:
    from curses import (
        wrapper, error, curs_set, baudrate, start_color, init_pair, use_default_colors, has_colors, color_pair,
        A_BOLD, COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
    )
except ModuleNotFoundError:
    print('\nДля работы программы необходимо установить модуль curses!\n')

from .base import Base


class Visualisation(Base):
    __slots__ = (
        'error_emoji', 'logo_y', 'logo_x', 'name_y', 'name_x', 'info_y', 'info_x', 'temp_y', 'temp_x',
        'version_y', 'version_x', 'copy_right_y', 'copy_right_x', 'idct_y', 'idct_x', 'dgts_y', 'dgts_x'
    )

    def __init__(
            self, logo_y=0, logo_x=0, name_y=1, name_x=78, info_y=1, info_x=32, temp_y=2, temp_x=78,
            version_y=10, version_x=32, copy_right_y=11, copy_right_x=32, idct_y=11, idct_x=78, dgts_y=14,
            dgts_x=((0, 16, 33), (38, 54, 71), (76, 92, 71))
    ):
        super().__init__()
        self.error_emoji = '¯\\_(`-`)_/¯'
        self.logo_y = logo_y
        self.logo_x = logo_x
        self.name_y = name_y
        self.name_x = name_x
        self.info_y = info_y
        self.info_x = info_x
        self.temp_y = temp_y
        self.temp_x = temp_x
        self.version_y = version_y
        self.version_x = version_x
        self.copy_right_y = copy_right_y
        self.copy_right_x = copy_right_x
        self.idct_y = idct_y
        self.idct_x = idct_x
        self.dgts_y = dgts_y
        self.dgts_x = dgts_x

    @staticmethod
    def safe_wrapper(function, *args) -> None:
        """Оборачивает вызов wrapper в try/except и подавляет исключения curses.error."""
        try:
            if any(args):
                wrapper(function, *args)
            else:
                wrapper(function)
        except error:
            pass

    @staticmethod
    def format_date() -> str:
        """Возвращает текущую дату в формате 'DD.MM.YYYY'."""
        now = datetime.now()
        return now.strftime("%d.%m.%Y")

    @staticmethod
    def display_symbols(
            stdscr, height: int, y: int, x: int, symbol: str | bool | list[str] | dict[str, str | bool], color: object
    ) -> None:
        """Метод отображает символы на экране."""
        for i in range(height):
            try:
                stdscr.addstr(i + y, x, symbol[i], color)
            except error:
                pass

    @staticmethod
    def verify_color(color) -> object | int:
        """Метод проверяет настройку цвета из конфигурации."""
        color_map: dict[str, int] = {
            'BLACK': COLOR_BLACK, 'BLUE': COLOR_BLUE, 'CYAN': COLOR_CYAN, 'GREEN': COLOR_GREEN,
            'MAGENTA': COLOR_MAGENTA, 'RED': COLOR_RED, 'WHITE': COLOR_WHITE, 'YELLOW': COLOR_YELLOW,
        }
        return color_map.get(color, COLOR_WHITE)

    @staticmethod
    def init_curses(stdscr) -> None:
        """Инициализирует экран curses"""
        stdscr.clear()
        stdscr.refresh()
        curs_set(False)
        if has_colors():
            use_default_colors()
            start_color()

    def paint(self, color: str, a_bold: bool) -> int:
        """Метод раскрашивает текст или текстовое изображение."""
        colors_dict: dict[str, int] = {
            'MAGENTA': 1, 'BLUE': 2, 'CYAN': 3, 'GREEN': 4,
            'YELLOW': 5, 'RED': 6, 'WHITE': 7, 'BLACK': 8
        }
        if color not in colors_dict:
            error_message = f'Цвет "{color}" не найден в доступных цветах.'
            self.logger.error('%s (доступные: %s)', error_message, ', '.join(colors_dict.keys()))
            raise KeyError(error_message)
        for i, color_name in enumerate(colors_dict.keys()):
            init_pair(1 + i, self.verify_color(color_name), -1)
        if a_bold:
            return color_pair(colors_dict[color]) | A_BOLD
        return color_pair(colors_dict[color])

    def get_info_list(self, function) -> list[str]:
        """Метод получает список строковой информации на основе переданной функции."""
        return [f"{key}{value}" for key, value in function(self.language).items()]
