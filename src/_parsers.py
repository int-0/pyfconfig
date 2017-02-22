#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#
# THIS MODULE IS QUICK'N'DIRTY (sorry)
#

import re

from errors import CannotParse

def iface_to_dict_16(raw):
    '''Convert raw data into a dict (ifconfig -2.4 version)'''
    def int_value(variable_name):
        '''Return a value next to a variable'''
        try:
            match = re.search('%s:\d+' % variable_name, raw).group(0)
            return int(match.split(':')[1])
        except AttributeError:
            raise CannotParse(repr(raw))
        except IndexError:
            raise CannotParse(match)
        
    def mac_value():
        '''Search "HWaddr XX:XX:XX:XX:XX:XX" pattern and return MAC'''
        try:
            match = re.search('HWaddr .*\n', raw).group(0)
            return match.split()[1]
        except AttributeError:
            raise CannotParse(repr(raw))
        except IndexError:
            raise CannotParse(match)

    def ipv4_value(variable_name):
        '''Search a XXX.XXX.XXX.XXX pattern next to a variable_name'''
        try:
            match = re.search(
                '%s:\d+\.\d+\.\d+\.\d+' % variable_name,
                raw).group(0)
            return match.split(':')[1]
        except AttributeError:
            raise CannotParse(repr(raw))
        except IndexError:
            raise CannotParse(match)

    def iface_name():
        '''Search interface name'''
        try:
            return re.search('^.*Link', raw).group(0)[:-4].strip()
        except AttributeError:
            raise CannotParse(repr(raw))

    iface = iface_name()
    result = {
        iface: {
            'mtu': int_value('MTU'),
            'txqueuelen': int_value('txqueuelen'),
            'packets_received': int_value('RX packets'),
            'packets_sent': int_value('TX packets')
        }
    }
    try:
        result[iface].update({'mac': mac_value()})
    except CannotParse, e:
        pass
    try:
        result[iface].update({'ipv4': ipv4_value('inet addr')})
    except CannotParse:
        pass
    try:
        result[iface].update({'netmask4': ipv4_value('Mask')})
    except CannotParse:
        pass
    return result


def iface_to_dict_24(raw):
    '''Convert raw data into a dict (ifconfig +2.4 version)'''
    def int_value(variable_name):
        '''Return a value next to a variable'''
        try:
            match = re.search('%s\s*\d+' % variable_name, raw).group(0)
            var_len = len(variable_name.split())
            return int(match.split()[var_len])
        except AttributeError:
            raise CannotParse(repr(raw))
        except IndexError:
            raise CannotParse(match)
        
    def mac_value():
        '''Search "ether XX:XX:XX:XX:XX:XX" pattern and return MAC'''
        try:
            match = re.search(
                'ether (([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4})', raw).group(0)
            return match.split()[1]
        except AttributeError:
            raise CannotParse(repr(raw))
        except IndexError:
            raise CannotParse(match)

    def ipv4_value(variable_name):
        '''Search a XXX.XXX.XXX.XXX pattern next to a variable_name'''
        try:
            return re.search(
                '%s ^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$' % variable_name,
                raw).group(1)
        except AttributeError:
            raise CannotParse(repr(raw))

    def iface_name():
        '''Search interface name'''
        try:
            return re.search('^.*\:', raw).group(0)[:-1]
        except AttributeError:
            raise CannotParse(repr(raw))

    iface = iface_name()
    result = {
        iface: {
            'mtu': int_value('mtu'),
            'txqueuelen': int_value('txqueuelen'),
            'packets_received': int_value('RX packets'),
            'packets_sent': int_value('TX packets'),
            'reception_errors': int_value('RX errors'),
            'transmission_errors': int_value('TX errors'),
        }
    }
    try:
        result[iface].update({'mac': mac_value()})
    except CannotParse, e:
        pass
    try:
        result[iface].update({'ipv4': ipv4_value('inet')})
    except CannotParse:
        pass
    try:
        result[iface].update({'netmask4': ipv4_value('netmask')})
    except CannotParse:
        pass
    return result


# By default use old parsers
iface_to_dict = iface_to_dict_16


def split_ifaces(raw):
    '''Split a list of data into subsets of data'''
    splitted = []
    current = None
    for line in raw.splitlines():
        # This indicate new interface data
        if not line.startswith(' '):
            if (current is not None) and (current != '\n'):
                splitted.append(current)
            current = '%s\n' % line
        else:
            current += '%s\n' % line
    if (current is not None) and (current != '\n'):
        splitted.append(current)
    return splitted


def ifconfig_version(raw):
    '''Parse version'''
    line = raw.strip()
    try:
        return line.split()[1]
    except:
        raise CannotParse(line)
