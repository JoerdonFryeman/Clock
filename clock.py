from base import Base, datetime


class ClockModule(Base):
    """Класс визуализации текстовых изображений цифр."""

    def visualize_digits(self, stdscr) -> None:
        """
        Метод отображает текстовые изображения цифр текущего времени на экране.
        :param stdscr: Объект стандартного экрана для отображения цифр.
        """
        color: object = self.paint(self.digits_color, False)
        digits_height = lambda: self.dgts_y if self.system_info else self.dgts_y - 6
        y: int = digits_height()
        x: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] = self.dgts_x

        data: dict[str, list[str]] = self.get_json_data('digits')
        current_time: tuple = f'{datetime.now():%H}', f'{datetime.now():%M}', f'{datetime.now():%S}'

        for i in range(3):
            self.visualize_symbols(stdscr, len(data), y, x[i - 1][0], data[current_time[i - 1][0]], color)
            self.visualize_symbols(stdscr, len(data), y, x[i - 1][1], data[current_time[i - 1][1]], color)
            if i == 1 or i == 2:
                self.visualize_symbols(stdscr, len(data), y, x[i - 1][2], data['points'], color)
