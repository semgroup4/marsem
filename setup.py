#!/usr/bin/env python

import os
from setuptools import setup, find_packages, Command

class CleanCommand(Command):
    """ Cleans the dist directory and other dist related files """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


setup(name='MarsemServer',
      version='0.1',
      description='Marsem Server Application',
      author='Group 4',
      url='https://github.com/semgroup4/marsem',
      packages=find_packages(exclude=["arduino","microphones"]),
      cmdclass={
          'clean': CleanCommand,
      }
)
 
