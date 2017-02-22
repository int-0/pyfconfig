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
import _ifconfig as _iface

def ifconfig(command):
    '''Common command wrapper'''
    if __IFCONFIG__ is None:
        raise IfconfigError('executable not defined')
    command = '%s %s' % (__IFCONFIG__, command)
    _DEB('Command: "%s"' % command)
    return subprocess.check_output(shlex.split(command),
                                   stderr=subprocess.STDOUT)
# Register common command wrapper
_iface.set_wrapper(ifconfig)


def set_ifconfig_executable(executable):
    global __IFCONFIG__
    if not os.path.isfile(executable):
        raise IfconfigError("%s not found!" % executable)
    _DEB('Set ifconfig executable to: %s' % executable)
    __IFCONFIG__ = executable
    _get_version_()


def _search_executable_():
    for path in ['/sbin', '/bin', '/usr/sbin', '/usr/bin']:
        executable = os.path.join(path, 'ifconfig')
        try:
            set_ifconfig_executable(executable)
            return
        except IfconfigError:
            pass


def _get_version_():
    global __VERSION__
    version=None
    try:
        version = _parse.ifconfig_version(ifconfig('--version'))
    except subprocess.CalledProcessError, e:
        version = _parse.ifconfig_version(e.output)
    _DEB('Detected version: %s' % version)
    __VERSION__ = version
    if int(version.split('.')[0]) >= 2:
        _parse.iface_to_dict = _parse.iface_to_dict_24
    else:
        _parse.iface_to_dict = _parse.iface_to_dict_16

def available_interfaces():
    all_iface_data = _iface.get_data()
    parsed_data = {}
    for iface_data in _parse.split_ifaces(all_iface_data):
        parsed_data.update(_parse.iface_to_dict(iface_data))
    print parsed_data
    return parsed_data.keys()


# Set a default ifconfig executable
_search_executable_()

class Interface(object):
    def __init__(self, name):
        if name not in available_interfaces():
            raise CommandError('interface "%s" not found on the system' % name)
        self.__name = name
        self.__mtu = None
        self.__flags = None
        self.__mac = None
        self.__ipv4 = None
        self.__mask4 = None
        self.__refresh_statistics__()

    def __refresh_statistics__(self):
        stats = _parse.iface_to_dict(_iface.get_data(self.__name))
        stats = stats[self.__name]
        self.__mtu = stats.get('mtu', None)
        self.__flags = stats.get('flags', None)
        self.__mac = stats.get('mac', None)
        self.__ipv4 = stats.get('ipv4', None)
        self.__mask4 = stats.get('mask4', None)

    @property
    def name(self):
        return self.__name

    @property
    def mac(self):
        return self.__mac

    @property
    def ipv4(self):
        return self.__ipv4

    @property
    def mask4(self):
        return self.__mask4

    @property
    def flags(self):
        return self.__flags

    @property
    def mtu(self):
        return self.__mtu

    @mtu.setter
    def mtu(self, new_mtu):
        _iface.set_mtu(new_mtu)
        self.__refresh_statistics__()
