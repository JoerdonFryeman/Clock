from time import sleep, time
from threading import Thread

from configuration import curs_set, wrapper, error
from clock import ClockModule
from info import InfoModule
from temperature import TemperatureModule


class RunProgram(TemperatureModule, InfoModule, ClockModule):
    """Класс запуска всех компонентов программы."""

    running: bool = True

    @staticmethod
    def safe_wrapper(function, func_arg, arg: bool) -> None:
        """Запускает метод в обёртке и игнорирует ошибки curses."""
        try:
            if arg:
                wrapper(function, func_arg)
            else:
                wrapper(function)
        except error:
            pass

    @classmethod
    def wait_for_enter(cls, stdscr) -> None:
        """Ожидает нажатия клавиши."""
        stdscr.nodelay(False)
        stdscr.getch()
        cls.running: bool = False
        stdscr.clear()

    @classmethod
    def run_all_modules(cls, stdscr, function) -> None:
        """
        Запускает все модули программы в цикле.

        :param stdscr: Объект стандартного экрана для отображения информации.
        :param function: Функция, которую необходимо выполнить в каждом цикле.
        """
        while cls.running:
            start_time: float = time()
            curs_set(False)
            function(stdscr)
            stdscr.refresh()
            elapsed_time: float = time() - start_time
            time_to_sleep: float = 0.25 - elapsed_time
            if time_to_sleep > 0:
                sleep(time_to_sleep)

    def get_info_modules(self, stdscr) -> None:
        """
        Обновляет и отображает информацию о системе, температуре и логотипе.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        self.display_logo(stdscr), self.display_info(stdscr), self.display_system_info(stdscr)
        self.display_temperature_info(stdscr), self.verify_temperature_indicator(stdscr), self.renew()

    def get_wrapped_threads(self, stdscr) -> None:
        """
        Запускает потоки для выполнения модулей в зависимости от наличия системной информации.

        Если системная информация доступна, запускает потоки для обновления информации и визуализации цифр.
        В противном случае выполняет визуализацию цифр в основном потоке.
        """
        Thread(target=self.safe_wrapper, args=(self.wait_for_enter, None, False)).start()
        if self.system_info:
            Thread(target=self.safe_wrapper, args=(self.run_all_modules, self.get_info_modules, True)).start()
        if self.clock:
            self.run_all_modules(stdscr, self.display_digits)
        else:
            message: dict[str, str] = {
                "ru": "\nМодули часов и информации деактивированы, что ещё ты хочешь здесь увидеть?\n",
                "en": "\nClock and info modules are disabled, what else do you want to see here?\n"
            }
            language = lambda: self.language if self.language == "ru" or self.language == "en" else "ru"
            print(message[self.verify_language(language())])


run = RunProgram()


def main() -> None:
    """Запускающая все процессы главная функция."""
    try:
        run.safe_wrapper(run.get_wrapped_threads, None, False)
    except Exception as e:
        print(f'Проверка выдала ошибку: {e}')


if __name__ == '__main__':
    main()
