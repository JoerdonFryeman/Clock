from clock import RunProgram

run_program = RunProgram()


def main() -> None:
    """Запускающая все процессы главная функция."""

    try:
        run_program.get_clock_wrapper()
    except Exception as error:
        print(f'Проверка выдала ошибку: {error}')


if __name__ == '__main__':
    main()
