# Installation Guide #

## General Information ##
This project contains the code to take part in the tool competition.
It is developed in Python and runs on Windows machines.

## Dependencies ##

### BeamNG simulator ###

This tool needs the BeamNG simulator to be installed on the machine where it is running. 
A free version of the BeamNG simulator for research purposes can be obtained by registering at [https://register.beamng.tech](https://register.beamng.tech) and following the instructions provided by BeamNG. Please fill the "Application Text" field of the registration form with the following text:

```
I would like to participate to the "Testing Self-Driving Car Software
Contest" of the SBST Tool Competition 2021 and for that I need to a
copy of BeamNG.research
```

> **Note**: as stated on the BeamNG registration page, **please use your university email address**. If you do not own a university email address, please contact the organizers of the tool competition. 

### Python ###

This code has been tested with **Python 3.7**. 

### Other Libraries ###

To easily install the other dependencies with rely on `pip`, we suggest to create a dedicated virtual environment (we tested [`venv`](https://docs.python.org/3.7/library/venv.html)), activate it, and run the following command:

```
pip install -r requirements-37.txt
```

Otherwise, you can manually install each required library listed in the ```requirements-37.txt``` file.

> **Note**: the version of Shapely should match your system (see below).

In case your test generator requires additional library, please store them into an additional requirement file to be submitted along with your code.

To create such a file you can run the following command from within your active virtual environment:

```
pip freeze > additional-requirements.txt
```

Otherwise, you can manually list the additional libraries your test generator need in the `additional-requirements.txt` file.

> **Note**: the format of this file must follow the usual convention where the library name is followed by the target version number


### Shapely ###

You can obtain Shapely from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely). 

You should download the wheel file matching you Python version, i.e. download the file with cp37 in the name if you use Python 3.7. The wheel file should also match the architecture of your machine, i.e., you should install the file with either `win32` or `win_amd64` in the name.

After downloading the wheel file, you can install Shapely by running (in an active virtual environment) the following command:

```
pip install [path to the shapely file]
```

## Recommended Requirements ##

[BeamNG](https://wiki.beamng.com/Requirements) recommends the following hardware requirements:

* OS: Windows 10 64-Bit
* CPU: AMD Ryzen 7 1700 3.0Ghz / Intel Core i7-6700 3.4Ghz (or better)
* RAM: 16 GB RAM
* GPU: AMD R9 290 / Nvidia GeForce GTX 970
* DirectX: Version 11
* Storage: 20 GB available space
* Additional Notes: Recommended spec based on 1080p resolution. Installing game mods will increase required storage space. Gamepad recommended.

>**Note**: BeamNG.research can run also on Mac Book provided you boot them on Windows. A porting to linux is expected in the near future, but we cannot guarantee it will be ready before the tool competition's deadline. You can track the following [issue on GitHub](https://github.com/BeamNG/BeamNGpy/issues/79) about Linux porting.
