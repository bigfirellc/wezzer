# Wezzer

## Synopsis

Wezzer is a dead simple Python app to pull local weather information based on your geolocation and print it to your terminal with some okay formatting. 

It was born out of my frustration with most weather websites being full of ads, and just generally garbage to look at. 

For its forecast source, Wezzer uses NOAA's excellent [weather.gov API](https://www.weather.gov/documentation/services-web-api).

Wezzer is currently only compatible with Python 2.7.

## Installation

Clone the repository to your home directory

```bash
mkdir ~/GitHub/
cd ~/GitHub/
git clone https://github.com/nqnzp/wezzer.git
```

### virtualenv

It's recommended that you run Wezzer in a virtualenv, so make sure that you have a copy of virtualenv for your environment.

For example, on Ubuntu, just install it from apt:

```bash
sudo apt install python-virtualenv
```

Or on macOS, install [Homebrew](https://brew.sh/), then install virtualenv with `brew`:

```
brew install pyenv-virtualenv
```

Create a new virtualenv, for instance, inside of your home directory, and then activate it:

```bash
mkdir ~/venv
virtualenv ~/venv
. ~/venv/bin/activate
```

### Dependencies
Use the requirements.txt file to install dependencies, which are numerous.

```bash
cd ~/GitHub/wezzer/
pip install -r requirements.txt
```

Depending upon your environment, you may need to make wezzer.py executable before you run it.

```
chmod u+x ./wezzer.py
```

## Running Wezzer

Wezzer is easy to run once you've got it installed:

```bash
./wezzer.py
```

Wezzer will geolocate your computer by looking up your IP address, using [ipgetter](https://github.com/phoemur/ipgetter). It then looks up your latitude and longitude based on that IP, using [python-geoip](https://pythonhosted.org/python-geoip/), and uses those coordinates to query the NOAA's API for your local weather. By default, Wezzer displays 12 hours of short hourly forecasts, and 2 days worth of extended forecasts. 

### Commandline Options
Wezzer can be run with a handful of commandline options to adjust your experience. Use `-h` or `--help` for a full list of options.

 ```
 $ ./wezzer.py --help
 
 usage: wezzer.py [-h] [-c] [-d NUM_DAYS] [-t NUM_HOURS] [-w COLUMN_WIDTH]
                 [-z ZIP_CODE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --color           Enable terminal colors
  -d NUM_DAYS, --days NUM_DAYS
                        Number of days for Extended Forecast
  -t NUM_HOURS, --hours NUM_HOURS
                        Number of hours for Hourly Forecast
  -w COLUMN_WIDTH, --width COLUMN_WIDTH
                        Max width of the output (default 80 columns)
  -z ZIP_CODE, --zipcode ZIP_CODE
                        ZIP Code of desired weather location
```

### Sample Output
A typical run of Wezzer, with some options, will look something like this:

```
$ ./wezzer.py -z 07042

Wezzer 0.1.1
Weather for Glen Ridge, NJ (2018-05-06 01:16 PM)

12-Hour Forecast
01:00 PM - 02:00 PM ▪ 61F Slight Chance Rain Showers, wind 7 mph NE
02:00 PM - 03:00 PM ▲ 62F Rain Showers Likely, wind 7 mph NE
03:00 PM - 04:00 PM ▲ 63F Rain Showers Likely, wind 7 mph NE
04:00 PM - 05:00 PM ▼ 62F Rain Showers Likely, wind 7 mph NE
05:00 PM - 06:00 PM ▼ 61F Rain Showers Likely, wind 7 mph NE
06:00 PM - 07:00 PM ▼ 60F Rain Showers Likely, wind 7 mph NE
07:00 PM - 08:00 PM ▪ 60F Chance Rain Showers, wind 6 mph NE
08:00 PM - 09:00 PM ▼ 59F Chance Rain Showers, wind 5 mph NE
09:00 PM - 10:00 PM ▪ 59F Chance Rain Showers, wind 5 mph NE
10:00 PM - 11:00 PM ▼ 58F Chance Rain Showers, wind 3 mph NE
11:00 PM - 12:00 AM ▪ 58F Chance Rain Showers, wind 2 mph NE
12:00 AM - 01:00 AM ▼ 57F Chance Rain Showers, wind 2 mph NE

2-Day Extended Forecast
This Afternoon: ▼ 63F
    Rain showers likely. Cloudy. High near 63, with temperatures falling to
    around 60 in the afternoon. Northeast wind around 7 mph. Chance of
    precipitation is 60%. New rainfall amounts less than a tenth of an inch
    possible.
Tonight: ▪ 53F
    Rain showers likely. Cloudy, with a low around 53. Northeast wind 2 to 7
    mph. Chance of precipitation is 60%. New rainfall amounts between a tenth
    and quarter of an inch possible.
Monday: ▼ 67F
    A slight chance of rain showers. Partly sunny. High near 67, with
    temperatures falling to around 65 in the afternoon. Northeast wind 5 to 10
    mph. Chance of precipitation is 20%.
Monday Night: ▪ 49F
    A slight chance of rain showers before 9pm. Partly cloudy, with a low around
    49. East wind 3 to 9 mph. Chance of precipitation is 20%.
```

## Roadmap

You're looking at Wezzer 0.1. Future releases might look better or have more options. I'm toying with the idea of making a cross-platform GUI version called Gwezzer, but that's a bit further down the road. I'd also like to make it possible to create a ~/.wezzer_profile to store your default options in, like for example, if you always wanted to display wezzer with colors, or if you always wanted to override the IP lookup by specifying the ZIP Code for Beverly Hills 90210.

## Known Issues

* Wezzer is incompatible with Python 3.
* You can't paginate Wezzer with tools like `less` or `more` or `something in between`.
* Wezzer uses Unicode to print up and down arrows. Wezzer wants to print Unicode suns and clouds but hasn't figured out how to do that yet.
* Wezzer won't give you a backrub.