from clock import LogoModule, InfoModule, TemperatureModule, ClockModule
from time import sleep, time
from configuration import curs_set, use_default_colors, wrapper
from threading import Thread


class RunProgram(ClockModule, TemperatureModule, InfoModule, LogoModule):
    """Класс запуска всех компонентов программы."""

    @staticmethod
    def run_all_modules(stdscr, function) -> None:
        for _ in range(1_000_000_000):
            start_time = time()
            curs_set(False), use_default_colors(), function(stdscr), stdscr.refresh()
            elapsed_time = time() - start_time
            time_to_sleep = 0.25 - elapsed_time
            if time_to_sleep > 0:
                sleep(time_to_sleep)

    def get_info_modules(self, stdscr):
        self.renew()
        self.get_logo(stdscr), self.get_name_and_link(stdscr), self.visualize_system_info(stdscr)
        self.visualize_temperature_info(stdscr), self.verify_temperature_indicator(stdscr)

    def get_wrapped_threads(self) -> None:
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
