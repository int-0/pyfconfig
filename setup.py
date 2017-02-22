#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install import install

_PACKAGES_ = [
    'pyfconfig'
]

_PACKAGE_DIR_ = {
    'pyfconfig' :'src'
}

setup(
    name='pyfconfig',
    version='1.0',
    description='Python wrapper for ifconfig command',
    url='https://github.com/int-0/pyfconfig',
    author='Tobias Diaz',
    license='GPLv3',
    author_email='tobias.deb@gmail.com',
    packages=_PACKAGES_,
    package_dir=_PACKAGE_DIR_
)
