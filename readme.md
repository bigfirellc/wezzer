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

Finally, depending upon your environment, you may need to make wezzer.py executable before you run it.

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
A typical run of Wezzer will look something like this:

```
Wezzer 0.1: Weather for Upper Montclair, NJ (2018-05-01 09:25 PM)

12-hour forecast
09:00 PM - 10:00 PM ▲ 76F Mostly Clear
10:00 PM - 11:00 PM ▼ 72F Mostly Clear
11:00 PM - 12:00 AM ▼ 67F Mostly Clear
12:00 AM - 01:00 AM ▼ 65F Mostly Clear
01:00 AM - 02:00 AM ▼ 64F Mostly Clear
02:00 AM - 03:00 AM ▼ 62F Mostly Clear
03:00 AM - 04:00 AM ▼ 60F Mostly Clear
04:00 AM - 05:00 AM ▼ 59F Mostly Clear
05:00 AM - 06:00 AM ▼ 58F Mostly Clear
06:00 AM - 07:00 AM ▼ 57F Sunny
07:00 AM - 08:00 AM ▲ 58F Sunny
08:00 AM - 09:00 AM ▲ 59F Sunny

2-Day Extended Forecast
Tonight: Mostly clear. Low around 55, with temperatures rising to around 58 overnight. West wind 3 to 8 mph.
Wednesday: Sunny, with a high near 84. West wind 3 to 15 mph.
Wednesday Night: Partly cloudy. Low around 64, with temperatures rising to around 67 overnight. Southwest wind 3 to 15 mph.
Thursday: A slight chance of showers and thunderstorms after noon. Mostly sunny. High near 88, with temperatures falling to around
85 in the afternoon. Southwest wind 3 to 15 mph. Chance of precipitation is 20%.
```
  