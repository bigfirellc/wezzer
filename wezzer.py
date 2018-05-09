#!/usr/bin/env python

"""
wezzer.py
it's wezzer, for weather
github.com/nqnzp/wezzer
"""

from __future__ import print_function

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
from typing import Dict, Any
import win_inet_pton


def epdata_to_forecast(ep):
    forecast = dict()
    forecast["city"] = ep["properties"]["relativeLocation"]["properties"]["city"]
    forecast["state"] = ep["properties"]["relativeLocation"]["properties"]["state"]
    forecast["extended_url"] = ep["properties"]["forecast"]
    forecast["hourly_url"] = ep["properties"]["forecastHourly"]
    forecast["extended"] = get_forecast_data(forecast["extended_url"])
    forecast["hourly"] = get_forecast_data(forecast["hourly_url"])
    return forecast

def geocode_forecast(addr):
    geo = Nominatim()
    loc = geo.geocode(addr)
    latlong = str(loc.latitude) + "," + str(loc.longitude)
    ep = get_endpoint_data(latlong)
    return epdata_to_forecast(ep)

def get_endpoint_data(geolocation):
    try:
        r = requests.get("https://api.weather.gov/points/%s" % geolocation)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if r.status_code == 404:
            click.echo("[*] Invalid address, city, or zip code provided.", err=True)
        if r.status_code != 200:
            click.echo("[*] Failed to get response from weather.gov API", err=True)
        sys.exit(1)

    endpoint_data = json.loads(r.content)

    return endpoint_data  # returns a json object


def get_forecast_data(forecast_url):
    response = requests.get(forecast_url)

    if response.status_code == 200:
        forecast_data = json.loads(response.content)
    else:
        click.echo("[*] Failed to get response from API", err=True)

    return forecast_data  # returns a json object


def ipaddr_forecast():
    ipaddr = str(ipgetter.myip())
    click.echo("[+] Your IP address is %s" % ipaddr)
    geoip = geolite2.lookup(ipaddr)
    location = geoip.location
    latlong = str(location[0]) + "," + str(location[1])
    ep = get_endpoint_data(latlong)
    return epdata_to_forecast(ep)  # type: Dict[str, Any]

def print_extended_forecast(forecast, days, color, width):
    
    ef = click.style("\n\n" + str(days / 2) + "-Day Forecast", fg="cyan") + "\n"
    
    for i in range(1,width):
        ef += "="

    for period in forecast["extended"]["properties"]["periods"]:

        if period["number"] > days:
            break

        ef += "\n" + period["name"] + " " + str(period["temperature"]) + period["temperatureUnit"] 
        ef += "\n" + click.wrap_text(period["detailedForecast"], initial_indent="    ", subsequent_indent="    ")

    return ef
    
def print_hourly_forecast(forecast, hours, color, width):
    
    hf = click.style("\n\n" + str(hours) + "-Hour Forecast", fg="cyan") + "\n"
    
    for i in range(1,width):
        hf += "="

    last_temp = int()

    for period in forecast["hourly"]["properties"]["periods"]:
        if period["number"] > hours:
            break

        if last_temp == 0:
            trend = " "
        elif last_temp < period["temperature"]:
            trend = "+"
        elif last_temp > period["temperature"]:
            trend = "-"
        else:
            trend = "="

        last_temp = period["temperature"]

        # Convert the formatted time to a datetime object, and only print time
        start_time = parse(period["startTime"]).strftime("%I:%M%p")
        end_time = parse(period["endTime"]).strftime("%I:%M%p")

        hf += "\n" + (start_time + "-" + end_time + " " + trend + " "
              + str(period["temperature"]) + period["temperatureUnit"] + " "
              + period["shortForecast"] + ", wind " + period["windSpeed"]
              + " " + period["windDirection"])

    return hf
    

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


"""
========= MAIN ========
"""

@click.command()
@click.option('--address', help="Address for the forecast", type=str)
@click.option('--color/--no-color', default=True, help="Enable ANSI color")
@click.option('--days', default=3, callback=validate_days, help="Number of days for the extended forecast", type=int)
@click.option('--hours', default=6, help="Number of hours for the hourly forecast", type=int)
@click.option('--width', default=80, help="Display width", type=int)
@click.option('--zip', default="", callback=validate_zip, help='ZIP code for the forecast', type=str)
def cli(address, color, days, hours, width, zip):

    click.clear()

    if color:
        version = click.style("Wezzer 0.2.0", fg="yellow")
        nowtime = click.style(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"), fg="yellow")
    else:
        version = "\nWezzer 0.2.0"
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")


    if (zip):
        forecast = geocode_forecast(zip)
    elif (address):
        forecast = geocode_forecast(address)
    else:
        forecast = ipaddr_forecast()

    header = "\nWeather for %s, %s" % (forecast["city"], forecast["state"])
    output = version + "\n" + nowtime + header
    
    if hours > 0:
        output += print_hourly_forecast(forecast, hours, color, width)
    if days > 0:
        output += print_extended_forecast(forecast, days, color, width)

    if color:
        click.echo(output + "\n")
    else:
        click.echo(output + "\n", color=False)

if __name__ == "__main__":
    cli()
