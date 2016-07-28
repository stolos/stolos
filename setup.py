# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='stolos-watchd',
    version='0.0.1',
    description='Watch Docker daemon for events and update ceryx routes',
    long_description=readme,
    author='Antonis Kalipetis',
    author_email='akalipetis@sourcelair.com',
    url='https://github.com/akalipetis/stolos-watchd',
    packages=find_packages(exclude=('tests', 'docs'))
)
