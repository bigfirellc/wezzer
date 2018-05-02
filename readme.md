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

For example, on Ubuntu:

```bash
sudo apt install python-virtualenv
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

And if you're really ambitious, you can copy Wezzer to a directory in your path, and rename it to remove the .py extension so you can run it from anywhere in your terminal:

```
sudo cp ./wezzer.py /usr/local/bin/wezzer
```

## Running Wezzer

Wezzer is easy to run once you've got it installed:

```bash
wezzer
```

Wezzer will geolocate your computer by looking up your IP address, using [ipgetter](https://github.com/phoemur/ipgetter). It then looks up your latitude and longitude based on that IP, using [python-geoip](https://pythonhosted.org/python-geoip/), and uses those coordinates to query the NOAA's API for your local weather. By default, Wezzer displays 12 hours of short hourly forecasts, and 2 days worth of extended forecasts. 

### Commandline Options
Wezzer can be run with a handful of commandline options to adjust your experience. Use `-h` or `--help` for a full list of options.

 ```
 $ wezzer --help
 
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
$ wezzer -z 90210 -d 2 -t 6

Wezzer 0.1: Weather for West Hollywood, CA (2018-05-01 09:34 PM)

6-hour forecast
06:00 PM - 07:00 PM ▲ 63F Chance Showers And Thunderstorms
07:00 PM - 08:00 PM ▼ 62F Chance Showers And Thunderstorms
08:00 PM - 09:00 PM ▼ 59F Chance Showers And Thunderstorms
09:00 PM - 10:00 PM ▼ 58F Chance Showers And Thunderstorms
10:00 PM - 11:00 PM ▼ 57F Chance Showers And Thunderstorms
11:00 PM - 12:00 AM ▼ 56F Chance Showers And Thunderstorms

2-Day Extended Forecast
Tonight: A chance of showers and thunderstorms. Mostly cloudy, with a low around 53.
South southeast wind 0 to 10 mph. Chance of precipitation is 40%.
Wednesday: A slight chance of rain showers before 11am. Partly sunny, with a high near 64.
South wind 0 to 10 mph. Chance of precipitation is 20%.
Wednesday Night: Partly cloudy, with a low around 52. West southwest wind 0 to 10 mph.
Thursday: Sunny, with a high near 71. West southwest wind 0 to 5 mph
```

## Roadmap

You're looking at Wezzer 0.1. Future releases might look better or have more options. I'm toying with the idea of making a cross-platform GUI version called Gwezzer, but that's a bit further down the road. I'd also like to make it possible to create a ~/.wezzer_profile to store your default options in, like for example, if you always wanted to display wezzer with colors, or if you always wanted to override the IP lookup by specifying the ZIP Code for Beverly Hills 90210.

## Known Issues

* Wezzer is incompatible with Python 3.
* You can't paginate Wezzer with tools like `less` or `more` or `something in between`.
* Wezzer uses Unicode to print up and down arrows. Wezzer wants to print Unicode suns and clouds but hasn't figured out how to do that yet.
* Wezzer won't give you a backrub.