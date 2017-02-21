#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

__version__ = '1.0.0'
__author__ = 'tobias.diaz'
__author_email__ = 'tobias.deb@gmail.com'
__description__ = 'ifconfig python wrapper'

__IFCONFIG__ = None
__VERSION__ = None

import shlex
import os.path
import subprocess

import logging
_DEB = logging.debug
logging.basicConfig(level=logging.DEBUG)

from errors import *
import _parsers as _parse


def ifconfig(command):
    if __IFCONFIG__ is None:
        raise IfconfigNotFound('executable not defined')
    command = '%s %s' % (__IFCONFIG__, command)
    _DEB('Command: "%s"' % command)
    return subprocess.check_output(shlex.split(command),
                                   stderr=subprocess.STDOUT)


def set_ifconfig_executable(executable):
    global __IFCONFIG__
    if not os.path.isfile(executable):
        raise IfconfigNotFound("%s not found!" % executable)
    _DEB('Set ifconfig executable to: %s' % executable)
    __IFCONFIG__ = executable
    _get_version_()


def _search_executable_():
    for path in ['/sbin', '/bin', '/usr/sbin', '/usr/bin']:
        executable = os.path.join(path, 'ifconfig')
        try:
            set_ifconfig_executable(executable)
            return
        except IfconfigNotFound:
            pass


def _get_version_():
    global __VERSION__
    version = _parse.ifconfig_version(ifconfig('--version'))
    _DEB('Detected version: %s' % version)
    __VERSION__ = version


# Set a default ifconfig executable
_search_executable_()
