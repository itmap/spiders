# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'itspider',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = itspider.settings']},
    zip_safe = False,
)
