from ast import literal_eval
from bext import hide, title
from rich.console import Console


class Configuration:
    hide()
    color = Console()
    title("Электроника 54")

    try:
        with open("settings.spec") as read_settings:
            first_color = literal_eval(read_settings.read())[0]
        with open("settings.spec") as read_settings:
            consistency = literal_eval(read_settings.read())[1]
    except (FileNotFoundError, NameError):
        with open("settings.spec", mode="w") as write_settings:
            write_settings.write("['[purple]', '3']")
        input("Перезапустите приложение!")
