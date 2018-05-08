#!/usr/bin/env python

"""
wezzer.py
it's wezzer, for weather
github.com/nqnzp/wezzer
"""

from __future__ import print_function

import argparse
import click
import datetime
from dateutil.parser import parse
from geoip import geolite2
from geopy.geocoders import Nominatim
import ipgetter
import json
import re
import requests
import sys
from termcolor import colored, cprint
import textwrap

def get_localhost_ip():
    myip = ipgetter.myip()
    return str(myip)     # returns a string of format "0.0.0.0"


def get_geoip(ip_addr):
    match = geolite2.lookup(ip_addr)
    return (match)  # returns a geoip object


def get_geopy_zip(zip):
    geo = Nominatim()
    loc = geo.geocode(zip)
    return (loc)  # returns a geopy object

def get_geopy_city(city):
    geo = Nominatim()
    loc = geo.geocode(city)
    return (loc)  # returns a geopy object


def get_endpoint_data(geolocation):
    try:
        r = requests.get("https://api.weather.gov/points/%s" % geolocation)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if r.status_code == 404:
            print ("Error: Invalid address, city, or zip code provided.")
        sys.exit(1)

    if r.status_code == 200:
        endpoint_data = json.loads(r.content)
    else:
        print("Error: Failed to get response from weather.gov API")

    return endpoint_data  # returns a json object


def get_forecast_data(forecast_url):
    response = requests.get(forecast_url)

    if response.status_code == 200:
        forecast_data = json.loads(response.content)
    else:
        print("[*] Failed to get response from API")

    return forecast_data  # returns a json object

def get_extended_forecast(endpoint_data):
    pass

def get_hourly_forecast(endpoint_data):
    pass

def validate_days(ctx, param, value):
    if value < 0:
        raise click.BadParameter('Days should be a positive integer.')
    value = value * 2
    return value

def validate_zip(ctx, param, value):
    zipCode = re.compile(r"(\s*)?(\d){5}(\s*)?")
    if not (zipCode.match(value) or value == ""):
        raise click.BadParameter('Invalid zip code format.')
    return value

def zip_forecast(zip):
    click.echo("[*] Getting forecast for zip code %s" % zip)
    gp = get_geopy_zip(zip)
    latlong = str(gp.latitude) + "," + str(gp.longitude)
    ep = get_endpoint_data(latlong)


"""
========= MAIN ========
"""

@click.command()
@click.option('--address', help="Address for the forecast", type=str)
@click.option('--color', default=True, help="Enable ANSI color", type=bool)
@click.option('--days', default=5, callback=validate_days, help="Number of days for the extended forecast", type=int)
@click.option('--hours', default=5, help="Number of hours for the hourly forecast", type=int)
@click.option('--width', default=80, help="Display width", type=int)
@click.option('--zip', default="", callback=validate_zip, help='ZIP code for the forecast', type=str)
def cli(address, color, days, hours, width, zip):
    if (zip):
        zip_forecast(zip)
    elif (address):
        address_forecast(address)
    else:
        ip_forecast()

    pass

def main():

    # The most important variable declaration
    version = "Wezzer 0.2.0"

    # Setting up the textwrapper object
    indstr = "    "
    wrapper = textwrap.TextWrapper()
    wrapper.width = results.column_width
    wrapper.initial_indent = indstr
    wrapper.subsequent_indent = indstr


    # Make a datetime object for right now's time
    d = datetime.datetime.now()
    nowtime = d.strftime("%Y-%m-%d %I:%M %p")

    # If the user provides a zip code, look up the lat/long for
    # that, otherwise use their IP address
    if zip_code:
        geopy = get_geopy_zip(zip_code)
        latlong_str = str(geopy.latitude) + "," + str(geopy.longitude)

    else:
        # Determine the IP address of the host running the script
        ip_addr = get_localhost_ip()

        # Determine the latitude and longitude of the IP address
        geoip = get_geoip(ip_addr)
        location = geoip.location

        # Convert the geoip tuple to a string to use it
        # in the API request
        latlong_str = str(location[0]) + "," + str(location[1])

    # Send API request to weather.gov to get the
    # endpoint location data

    epdata = get_endpoint_data(latlong_str)

    # Derive the URLs from the returned endpoint data
    forecast_url = epdata["properties"]["forecast"]
    hourly_url = epdata["properties"]["forecastHourly"]

    # Use the forecast and hourly forecast URLs to get
    # forecast and hourly data
    forecast_data = get_forecast_data(forecast_url)
    hourly_data = get_forecast_data(hourly_url)

    # Find the city and state from the returned endpoint data
    city = epdata["properties"]["relativeLocation"]["properties"]["city"]
    state = epdata["properties"]["relativeLocation"]["properties"]["state"]

    # Setup variable for temperature trend monitoring
    last_temp = 0

    # The color handling logic is not the greatest
    if color_on:
        version = colored(version, 'yellow')
        nowtime = colored(nowtime, 'yellow')
        hourly_default_str = colored(hourly_default_str + "-Hour Forecast", 'yellow')
    else:
        hourly_default_str = hourly_default_str + "-Hour Forecast"

    print("\n" + version)
    print("Weather for %s, %s (%s)" % (city, state, nowtime))
    print("\n" + hourly_default_str)

    # Iterate through the hourly JSON, print
    # the time, temp, and forecast

    for period in hourly_data["properties"]["periods"]:

        # pprint(period)

        # Limit the output to what was set on
        # command line or default
        if period["number"] > hourly_default:
            break

        # Convert the formatted time to a datetime object
        start_d = parse(period["startTime"])
        end_d = parse(period["endTime"])

        # Output just the hour and minute
        start_time = start_d.strftime("%I:%M %p")
        end_time = end_d.strftime("%I:%M %p")

        # Get trend information on the temperature
        this_temp = int(period["temperature"])
        temperature = str(period["temperature"])

        if color_on:
            if last_temp == 0:
                trend = colored(u'\u25aa')
            elif last_temp < this_temp:
                trend = colored(u'\u25b2', 'red')
            elif last_temp > this_temp:
                trend = colored(u'\u25bc', 'blue')
            else:
                trend = colored(u'\u25aa', 'yellow')

            start_time = colored(start_time, 'cyan')
            end_time = colored(end_time, 'cyan')
            temperature = colored(temperature, attrs=['bold'])
        else:
            if last_temp == 0:
                trend = u'\u25aa'
            elif last_temp < this_temp:
                trend = u'\u25b2'
            elif last_temp > this_temp:
                trend = u'\u25bc'
            else:
                trend = u'\u25aa'

        last_temp = this_temp

        # Print some output of the time, temperature and short forecast
        print (start_time + ' - ' + end_time + ' ', end='')
        print (trend + " ", end='')
        print (temperature, end='')
        print (period["temperatureUnit"] + " ", end='')
        print (period["shortForecast"], end='')
        print (", wind " + period["windSpeed"] + " " + period["windDirection"])

    # Print a nice message about the x-Day forecast
    if color_on:
        cprint("\n" + str(results.num_days) +
               "-Day Extended Forecast", 'yellow')
    else:
        print("\n" + str(results.num_days) + "-Day Extended Forecast")

    # Iterate through the forecast JSON and print
    # the name and forecast
    for period in forecast_data["properties"]["periods"]:

        if period["number"] > extended_default:
            break

        #pprint(period)

        unit = period["temperatureUnit"]

        if color_on:
            name = colored(period["name"] + ": ", 'cyan')
            if period["temperatureTrend"] == "falling":
                trend = colored(u'\u25bc', 'blue')
            elif period["temperatureTrend"] == "rising":
                trend = colored(u'\u25b2', 'red')
            else:
                trend = colored(u'\u25aa')
            temp = colored(str(period["temperature"]), attrs=['bold'])
        else:
            name = period["name"] + ": "
            temp = str(period["temperature"])
            if period["temperatureTrend"] == "falling":
                trend = u'\u25bc'
            elif period["temperatureTrend"] == "rising":
                trend = u'\u25b2'
            else:
                trend = u'\u25aa'

        print(name + trend + " " + temp + unit)

        # Use text wrap to limit the output to x characters wide
        print(wrapper.fill(period["detailedForecast"]))


if __name__ == "__main__":
    cli()
