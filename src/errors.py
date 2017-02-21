#!/usr/bin/env python
# -*- mode=python; coding: utf-8 -*-
#


class IfconfigError(Exception):
    def __init__(self, executable='unknown'):
        self.__exec = executable
    def __str__(self):
        return 'Error with ifconfig executable: "%s"'


class CannotParse(Exception):
    def __init__(self, raw_string=None):
        self.__raw = raw_string
    def __str__(self):
        raw = (' (%s)' % self.__raw) if self.__raw is not None else ''
        return 'Error parsing data%s' % raw
