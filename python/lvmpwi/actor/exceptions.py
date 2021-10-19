# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32


from __future__ import absolute_import, division, print_function


class PwiActorError(Exception):
    """A custom core PwiActor exception"""
    def __init__(self, message=None):
        message = "There has been an error" if not message else message
        super(PwiActorError, self).__init__(message)


class PwiActorMountNotConnected(PwiActorError):
    """Pwi Telescope is disconnected"""
    def __init__(self):
        super(PwiActorMountNotConnected, self).__init__("PWI mount is not connected")


class PwiActorMountAxisNotEnabled(PwiActorError):
    """Pwi Telescope is disconnected"""
    def __init__(self):
        super(PwiActorMountAxisNotEnabled, self).__init__("PWI mount axis is not enabled")

