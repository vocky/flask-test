# -*- encoding: utf-8 -*-

__author__ = 'laye'
__version__ = "1.0"
__copyright__ = ""
__licence__ = "The modified BSD license"

from setuptools import setup, find_packages

setup(
      name='timorest', 
      version='1.0',
      description='Code example about how to manage a JSON/xml request using Flask',
      author='Laye', 
      author_email='wuchunlei@pset.suntec.net',
      url='http://gitlab.pset.suntec.net/wuchunlei/timo/',
      include_package_data=True,
      zip_safe=False,
      packages=find_packages(),
      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['Flask>=0.10',
                        'protobuf>=2.6',
                        'dicttoxml>=1.6',
      ],
     )
