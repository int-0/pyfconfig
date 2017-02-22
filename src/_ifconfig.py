#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#

from errors import CommandError

__IFCONFIG__ = None


def set_wrapper(method):
    global __IFCONFIG__
    __IFCONFIG__ = method


def _ifconfig_(cmd):
    try:
        return __IFCONFIG__(cmd)
    except Exception, e:
        raise CommandError('command "ifconfig %s" gets: %s' % (cmd, str(e)))

def set_mtu(iface, new_value):
    return _ifconfig_('%s mtu %s up' % (iface, new_value))

def set_mac(iface, new_mac):
    set_interface_down(iface)
    result = _ifconfig_('%s hw ether %s' % (iface, new_mac))
    set_interface_up(iface)
    return result

def set_down(iface):
    return _ifconfig_('%s down' % iface)

def set_up(iface):
    return _ifconfig_('%s up' % iface)

def set_ip(iface, ipv4, mask4):
    set_interface_down(iface)
    return _ifconfig_('%s %s netmask %s up' % (iface, ipv4, mask4))

def get_data(iface=None):
    if iface is None:
        iface = '-a'
    return _ifconfig_(iface)
