# ЭЛЕКТРОНИКА 54 (Clock)

A simple console retro clock with system and temperature information.

![Clock](https://github.com/user-attachments/assets/3dd15196-6276-46f2-82f5-7b5a6a9c6652)

## Startup
Download [latest release](https://github.com/JoerdonFryeman/Clock/releases/tag/Clock_v1.0.8).

In Linux, run ```Clock_v1.0.8``` in the terminal with the command:
```console
cd /home/your_directories.../Clock_v1.0.8/Linux/ && ./Clock_v1.0.8
```
In Windows, run ```Clock_v1.0.8.exe```

## Docker

Image [latest release](https://hub.docker.com/r/joerdonfryeman/clock).

Run with attached standard streams (interactive terminal):

```console
docker run -it joerdonfryeman/clock:1.0.8
```

Same with automatic container removal after exit:

```console
docker run --rm -it joerdonfryeman/clock:1.0.8
```

## Requirements

- Python: >= 3.14
- psutil: >= 7.2.2
- windows-curses: >= 2.4.1a1 (for Windows)
- The application was developed for Arch Linux with the KDE Plasma desktop environment, but should work in other distributions as well as with limitations in Windows.

## Installation

Download the project

``` console
git clone https://github.com/JoerdonFryeman/Clock
cd Clock
```

### For Linux

Create and activate a virtual environment:

``` console
python -m venv venv && source venv/bin/activate
```

Install the requirements and run the script in your console:

``` console
pip install --upgrade pip && pip install -r requirements.txt
python main.py
```

### For Windows

Create and activate a virtual environment:

``` console
python -m venv venv && venv\Scripts\activate
```

Install the requirements and run the script in your console:

``` console
python.exe -m pip install --upgrade pip && pip install -r requirements_for_windows.txt
python main.py
```

## Stop

Just press Enter or try any other key.

## Settings

Some program settings can be specified in the clock_config.json file.

- You can change the color of the clock, logo, or system info: BLACK, BLUE, CYAN, GREEN, MAGENTA, RED, WHITE, YELLOW.
- With true or false enable or disable clock or system and temperature info (temperature info is only available on Linux).
- Set the system info language to Russian "ru" or English "en".
- Create your own logo (13x31), add it to the logos.json file and enter its name in the clock_config.json file in the "logo_name" key.

The default settings can be restored by deleting the clock_config.json file and restarting the program.

## License

This project is being developed under the MIT license.

## Support with Bitcoin

bc1qewfgtrrg2gqgtvzl5d2pr9pte685pp5n3g6scy
