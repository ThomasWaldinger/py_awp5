# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

from setuptools import setup, find_packages

setup(name='awp5',
      version='0.1.2',
      url='https://github.com/ThomasWaldinger/awp5',
      license='LICENSE.txt',
      author='Thomas Waldinger',
      author_email='info@thomaswaldinger.es',
      description='A python wrapper for the Archiware P5 CLI',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      python_requires='>=3',
      zip_safe=False)
