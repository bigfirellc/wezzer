# wezzer

<img src="https://user-images.githubusercontent.com/20565648/39849784-0373a2b8-53dc-11e8-9b0a-6f1715d441f8.png" width="450"/>

## Synopsis

wezzer is a simple Python command line interface that pulls local weather information based on your geolocation,
zip code, or address and prints it to your console with some decent formatting. 

It was born out of my frustration with most weather websites being full of ads, and generally garbage to look at. 

For its forecast source, wezzer uses NOAA's excellent [weather.gov API](https://www.weather.gov/documentation/services-web-api).

wezzer is compatible with Python 2.7 and Python 3.6

wezzer has been tested to run nicely on Ubuntu, Windows, and macOS.

It's wezzer, for weather.


## Installation

Download the zip file from the releases page and unzip it, or clone the repository to 
somewhere memorable in your home directory, like a GitHub directory:

```commandline
mkdir ~/GitHub/
cd ~/GitHub/
git clone https://github.com/nqnzp/wezzer.git
```

### virtualenv

It's recommended that you run wezzer in a virtualenv, so make sure that you have a copy of virtualenv for your environment.

For example, on Ubuntu, just install it from apt:

```commandline
sudo apt install python-virtualenv
```

On Windows, it's helpful to use [Chocolatey](https://chocolatey.org) to set up your Python environment.
Install Chocolatey, then use it to install python and then use python to install virtualenv

```commandline
choco install python
easy_install virtualenv
```

For macOS, install [Homebrew](https://brew.sh/), then install python and virtualenv with `brew`:

```commandline
brew install python
brew install pyenv-virtualenv
```

Change directories into the `wezzer` dir, create a new virtualenv and then activate it. 
On Linux and macOS:

```commandline
cd wezzer
virtualenv venv
. venv/bin/activate
```

On Windows:

```commandline
cd wezzer
virtualenv venv
venv/Scripts/activate
```

### Dependencies
Use `pip` and the `requirements.txt` file to install dependencies:

```commandLine
pip install -r requirements.txt
```

Depending upon your environment, you may need to make wezzer.py executable before you run it.

```commandline
chmod u+x ./wezzer.py
```

## Running wezzer

wezzer is easy to run once you've got it installed:

```commandline
./wezzer.py
```

By default, wezzer will locate your computer by looking up your IP address. It coverts the address to latitude and longitude, and uses those coordinates to query the NOAA's API for a weather endpoint. Finally, it queries that endpoint for your local weather forecast. Run without any options, wezzer will display 6 hours of hourly forecasts, and 3 days worth of extended forecasts. 

### Commandline Options
wezzer can be run with a handful of commandline options to adjust your experience. Use `--help` for a full list of options.

 ```commandline
 ./wezzer.py --help
Usage: wezzer.py [OPTIONS]

Options:
  --address TEXT        Address or place for the forecast. Use quotes, eg.
                        "Bull Shoals, AR". Notable place names work too, like
                        "Griffith Park" or "Barton Springs Pool"
  --color / --no-color  Enable ANSI color
  --days INTEGER        # of days in the extended forecast, default is 3
  --hours INTEGER       # of hours in the hourly forecast, default is 6
  --width INTEGER       Display width by # of columns, default is 80
  --zip TEXT            ZIP code for the forecast
  --help                Show this message and exit.
```

### Sample Output
A run of wezzer with some options will look something like this:

```commandline
$ ./wezzer.py --address "Citi Field" --days 2 --hours 4

2018-05-09 07:48 PM
Weather forecast for Harbor Hills, NY

4-Hour Forecast
===============================================================================
07:00PM-08:00PM   68F Mostly Clear, wind 8 mph S
08:00PM-09:00PM - 66F Mostly Clear, wind 8 mph S
09:00PM-10:00PM - 64F Mostly Clear, wind 7 mph S
10:00PM-11:00PM - 61F Mostly Clear, wind 2 to 6 mph S

2-Day Forecast
===============================================================================
Tonight 54F
    Partly cloudy, with a low around 54. Southeast wind 0 to 8 mph.
Thursday 71F
    A slight chance of showers and thunderstorms after 2pm. Partly sunny. High
    near 71, with temperatures falling to around 68 in the afternoon. South wind
    1 to 13 mph. Chance of precipitation is 20%.
Thursday Night 58F
    A slight chance of showers and thunderstorms before 1am. Mostly cloudy, with
    a low around 58. West wind 6 to 13 mph. Chance of precipitation is 20%.
Friday 72F
    Sunny. High near 72, with temperatures falling to around 70 in the
    afternoon. West wind 7 to 10 mph.

```

## Changelog

**0.1** - very crude, did not support Windows or Python 3

**0.2** - switched to Click for all CLI logic, adds support for Windows,
 switched to maxminddb-geolite2 for Python 3 compatibility

## Roadmap

**0.3** - produce pre-built binaries for Linux, Windows, macOS with setuptools

**0.4** - allow wezzer to daemonize, display a web front end on a local port, using Flask

## Known Issues

See the **Issues** tab for known bugs, or to submit a feature request.

## Acknowledgements

wezzer heavily relies on the work of others much smarter and probably nicer than me, and makes use of the following projects

* [click](https://github.com/pallets/click)
* [geopy](https://github.com/geopy/geopy)
* [ipgetter](https://github.com/phoemur/ipgetter)

