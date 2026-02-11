from core.run import RunProgram

run = RunProgram()


def main() -> None:
    """Запускающая все процессы главная функция."""
    try:
        run.create_directories()
        run.get_logging_data()
        run.safe_wrapper(run.create_wrapped_threads, None)
    except Exception as e:
        run.logger.error(f'Проверка выдала ошибку: {e}\nНажми Enter для завершения.')


if __name__ == '__main__':
    main()
