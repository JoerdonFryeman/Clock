import psutil

from .visualisation import color_pair, Visualisation


class Temperature(Visualisation):
    """Класс получения и отображения информации о температуре."""

    def __init__(self):
        super().__init__()
        self.temperature = self.get_temperature_info()
        self.average_temperature = self.calculate_average_temperature()

    @staticmethod
    def verify_hardware(first: str, second: str) -> float | None:
        """
        Метод проверяет наличие датчиков температуры и возвращает текущую температуру.

        :param first: Имя первого датчика температуры.
        :param second: Имя второго датчика температуры.

        :return: Текущая температура в градусах Цельсия или None, если датчик не найден.
        """
        temperature: dict[str, list] = psutil.sensors_temperatures()
        try:
            if first in temperature:
                return temperature.get(first, [])[0].current
            elif second in temperature:
                return temperature.get(second, [])[0].current
            return temperature.get('acpitz', [])[0].current
        except (IndexError, TypeError):
            return None

    def get_temperature_info(self) -> tuple[float, float, float, float, float] | tuple[None, None, None, None, None]:
        """
        Метод получает информацию о температуре различных компонентов системы.
        :return: Кортеж с температурой процессора, видеокарты, оперативной памяти, накопителя и материнской платы.
        """
        try:
            cpu: float | None = self.verify_hardware('k10temp', 'coretemp')
            gpu: float | None = self.verify_hardware('amdgpu', 'nvidia')
            ram: float | None = self.verify_hardware('spd5118', '')
            storage: float | None = self.verify_hardware('nvme', '')
            motherboard: float | None = self.verify_hardware('acpitz', '')
            return cpu, gpu, ram, storage, motherboard
        except AttributeError:
            return None, None, None, None, None

    def create_temperature_info(self, language: str = 'ru') -> dict:
        """
        Метод создает словарь с информацией о температуре на заданном языке.

        :param language: Язык для отображения информации ('ru' или 'en').
        :return: Словарь с информацией о температуре на выбранном языке.
        """
        verify_temperature_info = lambda x: f'{x:.1f}°C' if x else self.error_emoji
        info: dict = {
            "ru": {
                "─": "─" * 26,
                "Температура ЦПУ: ": verify_temperature_info(self.temperature[0]),
                "Температура ГПУ: ": verify_temperature_info(self.temperature[1]),
                "Температура ОЗУ: ": verify_temperature_info(self.temperature[2]),
                "Тмп. накопителя: ": verify_temperature_info(self.temperature[3]),
                "Тмп. мат. платы: ": verify_temperature_info(self.temperature[4]),
                "Средняя тмп.   : ": verify_temperature_info(self.average_temperature)
            },
            "en": {
                "─": "─" * 26,
                "CPU temperature: ": verify_temperature_info(self.temperature[0]),
                "GPU temperature: ": verify_temperature_info(self.temperature[1]),
                "RAM temperature: ": verify_temperature_info(self.temperature[2]),
                "Storage t.     : ": verify_temperature_info(self.temperature[3]),
                "Motherboard t. : ": verify_temperature_info(self.temperature[4]),
                "Average tmp.   : ": verify_temperature_info(self.average_temperature)
            }
        }
        return info[self.verify_language(language)]

    def display_temperature_info(self, stdscr) -> None:
        """
        Метод отображает информацию о температуре на экране.
        :param stdscr: Объект стандартного экрана для отображения информации.
        """
        data: list[str] = self.get_info_list(self.create_temperature_info)
        self.display_symbols(stdscr, len(data), self.temp_y, self.temp_x, data, self.paint(self.info_color, False))

    def display_temperature_indicator(self, stdscr, indicators_value: int) -> None:
        """
        Метод отображает индикатор температуры на экране.

        :param stdscr: Объект стандартного экрана для отображения индикатора.
        :param indicators_value: Значение индикатора температуры.
        """
        for i in range(6):
            verify_item = lambda x: '█████' if i < indicators_value else '     '
            stdscr.addstr(self.idct_y, self.idct_x + i * 5, verify_item(i), color_pair(1 + i))

    def calculate_average_temperature(self) -> float | None:
        """
        Метод вычисляет среднюю температуру.
        :return: Средняя температура. Если допустимых значений нет, возвращает 0.
        """
        valid_temperatures: list = [i for i in self.temperature if isinstance(i, (int, float))]

        if not valid_temperatures:
            return None
        return sum(valid_temperatures) / len(valid_temperatures)

    def verify_temperature_indicator(self, stdscr) -> None:
        """
        Метод проверяет среднюю температуру и отображает соответствующий индикатор.
        :param stdscr: Объект стандартного экрана для отображения индикатора температуры.
        """
        thresholds: tuple = ((0, 40, 1), (40, 45, 2), (45, 50, 3), (50, 55, 4), (55, 60, 5), (60, 100, 6))
        try:
            for lower, upper, indicator in thresholds:
                if lower <= self.average_temperature < upper:
                    self.display_temperature_indicator(stdscr, indicator)
                    return None
            self.display_temperature_indicator(stdscr, 0)
            return None
        except TypeError:
            self.display_temperature_indicator(stdscr, 0)
            return None
