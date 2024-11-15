from setuptools import setup
import sys

sys.setrecursionlimit(5000)
# Read requirements.txt to get a list of packages
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

APP = ['bazaar_scraper.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': required_packages,  # Include additional packages used by your script
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
