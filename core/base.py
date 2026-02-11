import os
import platform
from logging import config, getLogger
from json import load, dump, JSONDecodeError


class Base:
    __slots__ = (
        'logger', 'clock_config', 'variables', 'digits_color', 'info_color',
        'logo_color', 'clock', 'system_info', 'language', 'logo_name'
    )

    def __init__(self):
        self.logger = getLogger()
        self.clock_config = {
            "digits_color": "MAGENTA",
            "system_info_color": "GREEN",
            "logo_color": "BLUE",
            "clock": True,
            "system_info": True,
            "language": "ru",
            "logo_name": ""
        }
        self.variables = self.get_config_data('clock_config')
        try:
            self.digits_color = self.variables['digits_color']
            self.info_color = self.variables['system_info_color']
            self.logo_color = self.variables['logo_color']
            self.clock = self.variables['clock']
            self.system_info = self.variables['system_info']
            self.language = self.variables['language']
            self.logo_name = self.variables['logo_name']
        except TypeError:
            print('\nTypeError! Переменные не могут быть инициализированы!')

    @staticmethod
    def create_directories() -> None:
        """Создаёт каталоги, игнорируя уже существующие."""
        directories: tuple[str, str, str] = ('config_files', 'config_files/logs', 'icons')
        for directory in directories:
            try:
                os.mkdir(directory)
            except FileExistsError:
                pass

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
    def verify_os() -> str | None:
        """Метод проверяет на какой ОС запускается программа."""
        system: str = platform.system()
        if system == 'Linux':
            return 'Linux'
        if system == 'Darwin':
            return 'macOS'
        if system == 'Windows':
            return 'Windows'
        return None

    @staticmethod
    def get_json_data(directory: str, name: str) -> dict:
        """Возвращает данные в формате json из указанного файла."""
        file_path: str = os.path.join(directory, f'{name}.json')
        try:
            with open(file_path, encoding='UTF-8') as json_file:
                data: dict = load(json_file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f'Файл не найден: {file_path}')
        except JSONDecodeError:
            raise ValueError(f'Ошибка декодирования JSON в файле: {file_path}')
        except PermissionError:
            raise PermissionError(f'Нет доступа к файлу: {file_path}')
        except Exception as e:
            raise Exception(f'Произошла ошибка: {str(e)}')

    @staticmethod
    def save_json_data(directory: str, name: str, data: list | dict) -> None:
        """Сохраняет файл json."""
        file_path: str = os.path.join(directory, f'{name}.json')
        try:
            with open(file_path, 'w', encoding='UTF-8') as json_file:
                dump(data, json_file, ensure_ascii=False, indent=4)
        except PermissionError:
            raise PermissionError(f'Нет доступа для записи в файл: {file_path}')
        except IOError as e:
            raise IOError(f'Ошибка записи в файл: {file_path}. Причина: {str(e)}')
        except Exception as e:
            raise Exception(f'Произошла ошибка: {str(e)}')

    def get_config_data(self, config_name: str):
        """Метод пробует прочитать файл конфигурации и, если это не удаётся, перезаписывает его."""
        try:
            return self.get_json_data('config_files', config_name)
        except FileNotFoundError:
            self.save_json_data('config_files', config_name, self.clock_config)
            return self.clock_config
        except JSONDecodeError:
            print(f'\nJSONDecodeError! Файл «{config_name}.json» поврежден или не является корректным JSON!')
            return None
        except OSError as e:
            print(f'\nOSError! Не удалось прочитать файл «{config_name}.json» из-за {e}')
            return None

    def get_logging_data(self) -> None:
        """Загружает и применяет конфигурацию логирования из JSON-файла."""
        config.dictConfig(self.get_json_data('config_files/logs', 'logging'))
