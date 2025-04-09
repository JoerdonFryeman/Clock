from clock import LogoModule, InfoModule, TemperatureModule, ClockModule
from time import sleep, time
from configuration import curs_set, use_default_colors, wrapper
from threading import Thread


class RunProgram(ClockModule, TemperatureModule, InfoModule, LogoModule):
    """Класс запуска всех компонентов программы."""

    @staticmethod
    def run_all_modules(stdscr, function) -> None:
        """
        Запускает все модули программы в цикле.

        :param stdscr: Объект стандартного экрана для отображения информации.
        :param function: Функция, которую необходимо выполнить в каждом цикле.
        """
        while True:
            start_time = time()
            curs_set(False), use_default_colors()
            function(stdscr)
            stdscr.refresh()
            elapsed_time = time() - start_time
            time_to_sleep = 0.25 - elapsed_time
            if time_to_sleep > 0:
                sleep(time_to_sleep)

    def get_info_modules(self, stdscr):
        """
        Обновляет и отображает информацию о системе, температуре и логотипе.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        self.renew()
        self.get_logo(stdscr), self.get_name_and_link(stdscr), self.visualize_system_info(stdscr)
        self.visualize_temperature_info(stdscr), self.verify_temperature_indicator(stdscr)

    def get_wrapped_threads(self) -> None:
        """
        Запускает потоки для выполнения модулей в зависимости от наличия системной информации.

        Если системная информация доступна, запускает потоки для обновления информации и визуализации цифр.
        В противном случае выполняет визуализацию цифр в основном потоке.
        """
        if self.system_info:
            Thread(target=wrapper, args=(self.run_all_modules, self.get_info_modules)).start()
            Thread(target=wrapper, args=(self.run_all_modules, self.visualize_digits)).start()
        else:
            wrapper(self.run_all_modules, self.visualize_digits)


run = RunProgram()


def main() -> None:
    """Запускающая все процессы главная функция."""

    try:
        run.get_wrapped_threads()
    except Exception as error:
        print(f'Проверка выдала ошибку: {error}')


if __name__ == '__main__':
    main()
