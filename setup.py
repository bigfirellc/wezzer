## Don't use this yet

from setuptools import setup

setup(
    name='wezzer',
    version='0.2.0',
    py_modules=['wezzer'],
    install_requires=[
        'Click',
        'colorama',
        'geopy',
        'ipgetter',
        'python-dateutil',
        'python-geoip',
        'maxminddb-geolite2',
        'requests',
        'typing',
        'win-inet-pton'
    ],
    entry_points='''
        [console_scripts]
        wezzer=wezzer:cli
    ''',
)
