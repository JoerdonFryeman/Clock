from time import sleep, time
from threading import Thread

from .clock import Clock
from .info import Info
from .temperature import Temperature


class Additionally(Clock, Info, Temperature):
    message = {
        "ru": "\nМодули часов и информации деактивированы, что ещё ты хочешь здесь увидеть?",
        "en": "\nClock and info modules are disabled, what else do you want to see here?"
    }

    class NoThreadsError(Exception):

        def __init__(self, message: dict[str, str], key: str):
            super().__init__(message[key])

    def renew(self):
        """Обновляет необходимые атрибуты."""
        self.variables = self.get_config_data('clock_config')
        self.digits_color = self.variables['digits_color']
        self.info_color = self.variables['system_info_color']
        self.logo_color = self.variables['logo_color']
        self.clock = self.variables['clock']
        self.system_info = self.variables['system_info']
        self.language = self.variables['language']
        self.logo_name = self.variables['logo_name']
        self.info = self.get_system_info()
        self.temperature = self.get_temperature_info()
        self.average_temperature = self.calculate_average_temperature()

    def get_info_modules(self, stdscr) -> None:
        """Обновляет и отображает информацию о системе, температуре и логотипе."""
        self.display_logo(stdscr), self.display_info(stdscr), self.display_system_info(stdscr)
        self.display_temperature_info(stdscr), self.verify_temperature_indicator(stdscr), self.renew()


class RunProgram(Additionally):
    __slots__ = ('running', 'fps')

    def __init__(self):
        super().__init__()
        self.running = True
        self.fps = 10

    def build_app(self, stdscr, function) -> None:
        """Создаёт потоки для каждого уровня полосы."""
        start_time: float = time()
        function(stdscr)
        stdscr.refresh()
        elapsed_time: float = time() - start_time
        time_to_sleep: float = self.fps / 100 - elapsed_time
        if time_to_sleep > 0:
            sleep(time_to_sleep)

    def wait_for_enter(self, stdscr) -> None:
        """Ждёт нажатия клавиши и устанавливает флаг остановки."""
        stdscr.getch()
        self.running: bool = False

    def create_main_loop(self, stdscr, function) -> None:
        """Запускает все модули программы в цикле."""
        while self.running:
            self.build_app(stdscr, function)

    def create_wrapped_threads(self) -> None:
        """Запускает потоки для выполнения модулей в зависимости от наличия системной информации."""
        self.safe_wrapper(self.init_curses, None)
        Thread(target=self.safe_wrapper, args=(self.wait_for_enter, None)).start()
        if self.system_info:
            Thread(target=self.safe_wrapper, args=(self.create_main_loop, self.get_info_modules)).start()
        if self.clock:
            self.safe_wrapper(self.create_main_loop, self.display_digits)
        if not self.system_info and not self.clock:
            raise self.NoThreadsError(self.message, self.verify_language(self.language))
