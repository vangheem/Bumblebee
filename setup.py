from setuptools import setup, find_packages
import os

version = '1.0a2'


setup(name='Bumblebee',
      version=version,
      description="deliverance-like implementation that only works on html output(no theme file)",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[],
      keywords='transform deliverance diazo lxml',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://github.com/vangheem/Bumblebee',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'repoze.xmliter'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
