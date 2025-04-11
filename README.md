# ЭЛЕКТРОНИКА 54 (Clock)

A simple console retro clock with system and temperature information.

![Clock](https://github.com/user-attachments/assets/e7880e84-05c3-488f-bb46-a7f1453947e5)

## Project structure

- `main.py`: The main module to run the program.
- `clock.py`: Clock symbols and system info generation and animation module.
- `configuration.py`: Module for loading program configuration data.
- `clock_config.json`: Program settings and configuration file.
- `digits.json`: A set of images of digits.
- `logos.json`: A set of images of logos.

## Requirements

- Python 3
- psutil 7.0.0
- windows-curses 2.4.1a1 (for Windows)
- The application was developed for Arch Linux with the KDE Plasma desktop environment, but should work in other distributions as well as with limitations in Windows.

## Installation

Download the project

``` console
git clone https://github.com/JoerdonFryeman/Clock
cd Clock
```

Create a virtual environment and install the requirements

### For Linux

``` console
python -m venv venv && source venv/bin/activate
pip install --upgrade pip && pip install -r requirements_for_linux.txt
```

### For Windows

``` console
python -m venv venv && venv\Scripts\activate
python.exe -m pip install --upgrade pip && pip install -r requirements_for_windows.txt
```

## Startup

You can start the project in your console

``` console
python main.py
```

## Settings

Some program settings can be specified in the clock_config.json file.

- You can change the color of the clock, logo, or system info: BLACK, BLUE, CYAN, GREEN, MAGENTA, RED, WHITE, YELLOW.
- With true or false enable or disable system and temperature info (temperature info is only available on Linux).
- Change the system info language to Russian “ru” or English “en”.
- Create your own logo (13x31), add it to the logos.json file and enter its name in the clock_config.json file in the "logo_name" key.

The default settings can be restored by deleting the clock_config.json file and restarting the program.

### License

This project is being developed under the MIT license.

### Support with Bitcoin

bc1qewfgtrrg2gqgtvzl5d2pr9pte685pp5n3g6scy
