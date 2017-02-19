#!/usr/bin/env python3

from setuptools import setup

setup(name='ResLight',
      version='0.1',
      description='A python app for estimating end use '
      'residential lighting electricity consumption, based on DOE data',
      author='Ken Weaver',
      author_email='kbweaver221@gmail.com',
      url='https://www.github.com/kenjones21/Residential-Lighting',
      packages=['res_light'],
      install_requires=['openpyxl', 'zipcode'],
      tests_require=['pytest']
     )
