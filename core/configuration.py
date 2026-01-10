import os
from io import TextIOWrapper
from json import load, dump, JSONDecodeError

try:
    from curses import (
        wrapper, error, curs_set, baudrate, start_color, init_pair, use_default_colors, color_pair, A_BOLD,
        COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN, COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
    )
except ModuleNotFoundError:
    print('\nДля работы программы необходимо установить модуль curses!\n')

directories: tuple[str, str] = ('config_files', 'icons')
for directory in directories:
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass


class Configuration:
    """Класс Configuration используется для чтения и управления настройками конфигурации из JSON-файла."""

    clock_config: dict[str, str | bool] = {
        "digits_color": "MAGENTA",
        "system_info_color": "GREEN",
        "logo_color": "BLUE",
        "clock": True,
        "system_info": True,
        "language": "ru",
        "logo_name": ""
    }

    @staticmethod
    def write_json_data(config_name: str, json_data: dict) -> None:
        """
        Метод создает новый файл конфигурации по умолчанию, если указанный JSON-файл не существует.

        :param config_name: Имя файла конфигурации (без расширения .json).
        :param json_data: Записываемые в виде словаря данные.
        """
        try:
            with open(f'config_files/{config_name}.json', 'x', encoding='UTF-8') as write_file:
                assert isinstance(write_file, TextIOWrapper)
                dump(json_data, write_file, ensure_ascii=False, indent=4)
        except FileExistsError:
            pass
        except OSError as e:
            print(f'\nНе удалось создать файл «{config_name}.json» из-за {e}')

    @staticmethod
    def get_json_data(config_name: str) -> dict[str, str | bool]:
        """
        Метод считывает JSON-файл конфигурации.
        :param config_name: Имя файла конфигурации (без расширения .json).
        """
        with open(f'config_files/{config_name}.json', encoding='UTF-8') as read_file:
            data: dict[str, str | bool] = load(read_file)
        return data

    def get_config_data(self, config_name: str) -> dict[str, str | bool] | None:
        """
        Метод пробует прочитать файл конфигурации и, если это не удаётся, перезаписывает его.

        :param config_name: Имя файла конфигурации (без расширения .json).
        :return dict: Данные конфигурации, загруженные из файла JSON.
        """
        try:
            return self.get_json_data(config_name)
        except FileNotFoundError:
            self.write_json_data(config_name, self.clock_config)
            return self.clock_config
        except JSONDecodeError:
            print(f'\nJSONDecodeError! Файл «{config_name}.json» поврежден или не является корректным JSON!')
            return None
        except OSError as e:
            print(f'\nOSError! Не удалось прочитать файл «{config_name}.json» из-за {e}')
            return None

    __slots__ = (
        'variables', 'digits_color', 'info_color', 'logo_color', 'clock', 'system_info', 'language', 'logo_name'
    )

    def __init__(self):
        self.variables: dict[str, str | bool] = self.get_config_data('clock_config')
        try:
            self.digits_color: str = self.variables['digits_color']
            self.info_color: str = self.variables['system_info_color']
            self.logo_color: str = self.variables['logo_color']
            self.clock: bool = self.variables['clock']
            self.system_info: bool = self.variables['system_info']
            self.language: str = self.variables['language']
            self.logo_name: str = self.variables['logo_name']
        except TypeError:
            print('\nTypeError! Переменные не могут быть инициализированы!')
