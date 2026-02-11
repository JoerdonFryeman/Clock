import os
import pwd
import socket
import getpass
import platform

from .visualisation import error, Visualisation


class Info(Visualisation):

    def __init__(self):
        super().__init__()
        self.info = self.get_system_info()

    @staticmethod
    def get_system_info() -> tuple[str, str, str, str, str, str, str, str, str]:
        """
        Метод получает информацию о системе.
        :return: Кортеж с информацией о пользователе, узле, системе, версии ОС, архитектуре, машине, процессоре и IP.
        """
        try:
            login = getpass.getuser()
        except Exception:
            try:
                login = pwd.getpwuid(os.geteuid()).pw_name
            except Exception:
                login = os.environ.get("USER")

        node: str = platform.node()
        system: str = platform.system()
        release: str = platform.release()
        architecture: str = platform.architecture()[0]
        machine: str = platform.machine()
        version_python: str = platform.python_version()
        processor: str = platform.processor()
        host_by_name = socket.gethostbyname(node)

        return login, node, system, release, architecture, machine, version_python, processor, host_by_name

    def display_logo(self, stdscr) -> None:
        """
        Метод получает и отображает логотип на экране.
        :param stdscr: Объект стандартного экрана для отображения логотипа.
        """
        logos: dict[str, str | bool] = self.get_json_data('config_files', 'logos')
        try:
            data: str | bool = logos[self.logo_name if self.logo_name != '' else self.verify_os()]
            self.display_symbols(
                stdscr, len(data), self.logo_y, self.logo_x, data, self.paint(self.logo_color, False)
            )
        except KeyError:
            try:
                stdscr.addstr(
                    self.logo_y + 6, self.logo_x + 11, self.error_emoji, self.paint(self.logo_color, False)
                )
            except error:
                pass

    def display_info(self, stdscr) -> None:
        """
        Метод отображает название проекта на экране.
        :param stdscr: Объект стандартного экрана для отображения названия и ссылки.
        """
        try:
            name: str = f'{self.format_date()} | ЭЛЕКТРОНИКА 54'
            version: str = 'Clock (version 1.0.7)'
            copy_right: str = 'MIT License, (c) 2026 Joerdon Fryeman'
            stdscr.addstr(self.name_y, self.name_x, name, self.paint(self.digits_color, False))
            stdscr.addstr(self.version_y, self.version_x, version, self.paint(self.info_color, False))
            stdscr.addstr(self.copy_right_y, self.copy_right_x, copy_right, self.paint(self.info_color, False))
        except error:
            pass

    def verify_info(self, info: str, max_length: int = 16) -> str:
        """
        Метод проверяет и обрезает информацию до заданной длины.

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

    def create_system_info(self, language: str = 'ru') -> dict:
        """
        Метод создает словарь с информацией о системе на заданном языке.

        :param language: Язык для отображения информации ('ru' или 'en').
        :return: Словарь с информацией о системе на выбранном языке.
        """
        login: str = self.verify_info(self.info[0])
        node: str = self.verify_info(self.info[1])
        info: dict = {
            "ru": {
                "": f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}',
                "─": "─" * (len(f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}') - 1),
                "ОС: ": self.verify_info(self.info[2]),
                "Версия ОС: ": self.verify_info(self.info[3]),
                "Архитектура: ": f"{self.verify_info(self.info[4])}, {self.verify_info(self.info[5])}",
                "Python: ": self.verify_info(self.info[6]),
                "Процессор: ": self.verify_info(self.info[7]),
                "IP-адрес: ": f"{self.verify_info(self.info[8])}{' ' * 9}"
            },
            "en": {
                "": f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}',
                "─": "─" * (len(f'{self.verify_info(f"{login}")}@{self.verify_info(f"{node}")}') - 1),
                "OS: ": self.verify_info(self.info[2]),
                "OS Version: ": self.verify_info(self.info[3]),
                "Architecture: ": f"{self.verify_info(self.info[4])}, {self.verify_info(self.info[5])}",
                "Python: ": self.verify_info(self.info[6]),
                "Processor: ": self.verify_info(self.info[7]),
                "IP address: ": f"{self.verify_info(self.info[8])}{' ' * 9}"
            }
        }
        return info[self.verify_language(language)]

    def display_system_info(self, stdscr) -> None:
        """
        Метод отображает информацию о системе на экране.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        data: list[str] = self.get_info_list(self.create_system_info)
        self.display_symbols(stdscr, len(data), self.info_y, self.info_x, data, self.paint(self.info_color, False))
