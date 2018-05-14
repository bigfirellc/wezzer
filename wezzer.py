#!/usr/bin/env python

"""
wezzer.py
it's wezzer, for weather
github.com/nqnzp/wezzer
"""

from __future__ import print_function
import click
import configparser
import datetime
from dateutil.parser import parse
from geolite2 import geolite2
from geopy.geocoders import Nominatim
import ipgetter
import json
import os.path
import re
import requests
import sys
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

    return json.loads(r.content)


def get_forecast_data(forecast_url):

    try:
        r = requests.get(forecast_url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if r.status_code == 404:
            click.echo("[*] Invalid forecast URI provided.", err=True)
        if r.status_code != 200:
            click.echo("[*] Failed to get response from weather.gov API", err=True)
        sys.exit(1)

    return json.loads(r.content)


def ipaddr_forecast():

    ipaddr = str(ipgetter.myip())
    reader = geolite2.reader()
    loc = reader.get(ipaddr)
    geolite2.close()

    latlong = str(loc["location"]["latitude"]) + "," + str(loc["location"]["longitude"])
    ep = get_endpoint_data(latlong)
    return epdata_to_forecast(ep)

def load_rc_file(config):

    options = dict()

    file_name = homedir + "/.wezzerrc"
    try:
        config.read_file(open(file_name, 'r'))
    except IOError as e:
        click.echo(e)

    return options


def print_extended_forecast(forecast, days, width):
    
    ef = click.style("\n\n" + str(int(days / 2)) + "-Day Forecast", fg="cyan") + "\n"
    
    for i in range(1,width):
        ef += "="

    for period in forecast["extended"]["properties"]["periods"]:

        if period["number"] > days:
            break

        ef += "\n" + click.style(period["name"], fg="green") + " " + str(period["temperature"]) + period["temperatureUnit"]
        ef += "\n" + click.wrap_text(period["detailedForecast"], width=width, initial_indent="    ", subsequent_indent="    ")

    return ef


def print_hourly_forecast(forecast, hours, width):
    
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

        hf += "\n" + (click.style(start_time + "-" + end_time, fg="green") + " " + trend + " "
              + str(period["temperature"]) + period["temperatureUnit"] + " "
              + period["shortForecast"] + ", wind " + period["windSpeed"]
              + " " + period["windDirection"])

    return hf
    

def validate_days(ctx, param, value):

    if value < 0:
        raise click.BadParameter('days should be a positive number, and an integer.')
    value = value * 2

    return value


def validate_width(ctx, param, value):

    if value < 1:
        raise click.BadParameter('width should be a positive number, and an integer.')

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
@click.option('--address', help="Address or place for the forecast. Use quotes, eg. \"Bull Shoals, AR\". "
                                "Notable place names work too, like \"Griffith Park\" or \"Barton Springs Pool\"", type=str)
@click.option('--color/--no-color', default=True, help="Enable ANSI color")
@click.option('--days', default=3, callback=validate_days, help="# of days in the extended forecast, default is 3", type=int)
@click.option('--hours', default=6, help="# of hours in the hourly forecast, default is 6", type=int)
@click.option('--version', help="Show version information", is_flag=True, default=False)
@click.option('--width', default=80, callback=validate_width, help="Display width by # of columns, default is 80", type=int)
@click.option('--zip', default="", callback=validate_zip, help='ZIP code for the forecast', type=str)
def cli(address, color, days, hours, version, width, zip):

    versioninfo = click.style("wezzer 0.2.0\nhttps://github.com/nqnzp/wezzer\nIt's wezzer, for weather.", fg="green")

    if (version):
        click.echo(versioninfo, color=color)
        sys.exit(1)

    # Get things from the user's .wezzer file if they exist
    config = configparser.ConfigParser()
    try:
        config.read(os.path.expanduser('~/.wezzer'))
    except configparser.MissingSectionHeaderError as e:
        click.echo("Invalid .wezzer file: Missing [wezzer] header.")
        sys.exit(1)

    try: address = str(config["wezzer"]["address"])
    except (KeyError) as e: pass
    try: color = bool(config["wezzer"]["color"])
    except (KeyError) as e: pass
    try: days = int(config["wezzer"]["days"]) * 2
    except (KeyError) as e: pass
    try: hours = int(config["wezzer"]["hours"])
    except (KeyError) as e: pass
    try: width = int(config["wezzer"]["width"])
    except (KeyError) as e: pass
    try: days = str(config["wezzer"]["zip"])
    except (KeyError) as e: pass

    if (zip):
        forecast = geocode_forecast(zip)
    elif (address):
        forecast = geocode_forecast(address)
    else:
        forecast = ipaddr_forecast()

    nowtime = click.style(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"), fg="cyan")

    header = click.style("\nWeather forecast for %s, %s"
                         % (forecast["city"], forecast["state"]), fg="green")

    output = "\n" + nowtime + header

    if hours > 0:
        output += print_hourly_forecast(forecast, hours, width)
    if days > 0:
        output += print_extended_forecast(forecast, days, width)

    click.echo(output + "\n", color=color)

if __name__ == "__main__":
    cli()
