from setuptools import setup, find_packages

setup(
    name         = 'facebook_ads',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = facebook_ads.settings']},
)
