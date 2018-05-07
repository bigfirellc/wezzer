from setuptools import setup

setup(
    name='wezzer',
    version='0.2',
    py_modules=['wezzer'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        wezzer=wezzer:cli
    ''',
)
