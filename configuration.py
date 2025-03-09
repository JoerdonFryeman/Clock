import os
import platform
from io import TextIOWrapper
from json import load, dump
from typing import Dict

try:
    from curses import (
        wrapper, error, curs_set, baudrate, start_color, init_pair, use_default_colors, color_pair, A_BOLD,
        COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
    )
except ModuleNotFoundError:
    print('\nДля Windows необходимо установить файл requirements_for_windows.txt!\n')

try:
    directories: tuple[str, str] = ('config_files', 'icons')
    for i in range(len(directories)):
        os.mkdir(directories[i])
        i += 1
except FileExistsError:
    pass


class Configuration:
    """Класс Configuration используется для чтения и управления настройками конфигурации из JSON-файла."""

    json_data = {
        "digits_color": "MAGENTA",
        "system_info_color": "GREEN",
        "logo_color": "BLUE",
        "system_info": True,
        "language": "ru",
        "logo_name": ""
    }

    @classmethod
    def get_json_data(cls, config_name: str) -> Dict:
        """
        Метод считывает конфигурационный файл JSON.
        Если указанный JSON-файл не существует, он создает новый файл с конфигурациями по умолчанию.

        :param config_name: Имя файла конфигурации (без расширения .json).
        :return Dict: Данные конфигурации, загруженные из файла JSON.
        """
        try:
            with open(f'config_files/{config_name}.json', encoding='UTF-8') as read_file:
                data = load(read_file)
            return data
        except FileNotFoundError:
            print(f'\nFileNotFoundError! File "{config_name}.json" not found!')
            try:
                if config_name == 'clock_config':
                    with open(f'config_files/{config_name}.json', 'w', encoding='UTF-8') as write_file:
                        if isinstance(write_file, TextIOWrapper):
                            dump(cls.json_data, write_file, ensure_ascii=False, indent=4)
                        else:
                            raise TypeError("Expected TextIOWrapper for the file type")
                else:
                    raise TypeError(f'Файл "{config_name}.json" не найден!')
            except OSError as e:
                print(f'\nFailed to create file "{config_name}.json" due to {e}')
            return cls.json_data

    __slots__ = (
        'variables', 'digits_color', 'info_color', 'logo_color', 'system_info', 'language', 'logo_name'
    )

    def __init__(self):
        self.variables = self.get_json_data('clock_config')
        try:
            self.digits_color = self.variables['digits_color']
            self.info_color = self.variables['system_info_color']
            self.logo_color = self.variables['logo_color']
            self.system_info = self.variables['system_info']
            self.language = self.variables['language']
            self.logo_name = self.variables['logo_name']
        except TypeError:
            print('\nTypeError! Variables can\'t be initialized!')

    @staticmethod
    def verify_color(color):
        """
        Метод проверяет настройку цвета из конфигурации.
        :return: COLOR_*: Цветовая константа, соответствующая цветовой конфигурации.
        """
        dictionary = {
            'BLACK': lambda: COLOR_BLACK, 'BLUE': lambda: COLOR_BLUE,
            'CYAN': lambda: COLOR_CYAN, 'GREEN': lambda: COLOR_GREEN,
            'MAGENTA': lambda: COLOR_MAGENTA, 'RED': lambda: COLOR_RED,
            'WHITE': lambda: COLOR_WHITE, 'YELLOW': lambda: COLOR_YELLOW,
        }[color]
        return dictionary()

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
