# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmpwi.actor.commands import parser
from lvmpwi.pwi import PWI4


# pwi4 command: mount_connect(self):

@parser.command()
async def connect(command: Command, pwi: PWI4):
    """mount connect"""

    try:

        status = pwi.mount_connect()
        command.info(
            isconnected = status.mount.is_connected
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_disconnect(self):

@parser.command()
async def disconnect(command: Command, pwi: PWI4):
    """mount disconnect"""

    try:

        status = pwi.mount_disconnect()
        command.info(
            isconnected = status.mount.is_connected
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


# pwi4 command: mount_enable(self, axisNum):

@parser.command()
async def enable(command: Command, pwi: PWI4, axis: int):
    """mount enable axis"""

    try:

        status = pwi.mount_enable(axis)
        command.info(
            isenabled = status.mount.axis1.is_enabled if axis else status.mount.axis0.is_enabled,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_disable(self, axisNum):

@parser.command()
@click.argument("AXIS", type=int)
async def disable(command: Command, pwi: PWI4, axis: int):
    """mount disable axis"""

    try:

        status = pwi.mount_disable(axis)
        command.info(
            isenabled = status.mount.axis1.is_enabled if axis else status.mount.axis0.is_enabled,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


# pwi4 command: mount_stop(self):

@parser.command()
async def stop(command: Command, pwi: PWI4):
    """mount stop"""

    try:

        status = pwi.mount_stop()
        command.info(
            isenabled = status.mount.is_enabled
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


# pwi4 command: mount_goto_ra_dec_apparent(self, ra_hours, dec_degs):

@parser.command()
@click.argument("RA_H", type=float)
@click.argument("DEG_D", type=float)
async def goto_ra_dec_apparent(command: Command, pwi: PWI4, ra_h: float, deg_d: float):
    """mount goto_ra_dec_apparent"""

    try:

        status = pwi.mount_goto_ra_dec_apparent(ra_h, deg_d)
        command.info(
            dec_apparent_degs = status.mount.dec_apparent_degs,
            ra_apparent_hours = status.mount.ra_apparent_hours,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


# pwi4 command: mount_goto_ra_dec_j2000(self, ra_hours, dec_degs):

@parser.command()
@click.argument("RA_H", type=float)
@click.argument("DEG_D", type=float)
async def goto_ra_dec_j2000(command: Command, pwi: PWI4, ra_h: float, deg_d: float):
    """mount goto_ra_dec_j2000"""

    try:

        status = pwi.mount_goto_ra_dec_j2000(ra_h, deg_d)
        command.info(
            dec_j2000_degs = status.mount.dec_j2000_degs,
            ra_j2000_hours = status.mount.ra_j2000_hours,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_goto_alt_az(self, alt_degs, az_degs):

@parser.command()
@click.argument("ALT_D", type=float)
@click.argument("AZ_D", type=float)
async def goto_ra_dec_j2000(command: Command, pwi: PWI4, alt_d: float, az_d: float):
    """mount goto_alt_az"""

    try:

        status = pwi.mount_goto_alt_az(alt_d, az_d)
        command.info(
            altitude_degs = status.mount.altitude_degs,
            azimuth_degs = status.mount.azimuth_degs,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_offset(self, **kwargs):

@parser.command()
async def goto_ra_dec_j2000(command: Command, pwi: PWI4):
     """mount mount_offset
     
        One or more of the following offsets can be specified as a keyword argument:
        AXIS_reset: Clear all position and rate offsets for this axis. Set this to any value to issue the command.
        AXIS_stop_rate: Set any active offset rate to zero. Set this to any value to issue the command.
        AXIS_add_arcsec: Increase the current position offset by the specified amount
        AXIS_set_rate_arcsec_per_sec: Continually increase the offset at the specified rate
        Where AXIS can be one of:
        ra: Offset the target Right Ascension coordinate
        dec: Offset the target Declination coordinate
        axis0: Offset the mount's primary axis position 
               (roughly Azimuth on an Alt-Az mount, or RA on In equatorial mount)
        axis1: Offset the mount's secondary axis position 
               (roughly Altitude on an Alt-Az mount, or Dec on an equatorial mount)
        path: Offset along the direction of travel for a moving target
        transverse: Offset perpendicular to the direction of travel for a moving target
        For example, to offset axis0 by -30 arcseconds and have it continually increase at 1
        arcsec/sec, and to also clear any existing offset in the transverse direction,
        you could call the method like this:
        mount_offset(axis0_add_arcsec=-30, axis0_set_rate_arcsec_per_sec=1, transverse_reset=0)
        """

    try:
        pass
#        status = pwi.mount_mount_offset(alt_d, az_d)
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


# pwi4 command: mount_park(self):

@parser.command()
async def park(command: Command, pwi: PWI4):
    """mount park"""

    try:

        status = pwi.mount_park()
        command.info(
            altitude_degs = status.mount.altitude_degs,
            azimuth_degs = status.mount.azimuth_degs,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_set_park_here(self):

@parser.command()
async def park_here(command: Command, pwi: PWI4):
    """mount park"""

    try:

        status = pwi.mount_park_here()
        command.info(
            altitude_degs = status.mount.altitude_degs,
            azimuth_degs = status.mount.azimuth_degs,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_tracking_on(self):

@parser.command()
async def tracking_on(command: Command, pwi: PWI4):
    """mount tracking_on"""

    try:

        status = pwi.mount_tracking_on()
        command.info(
            is_tracking = status.mount.is_tracking,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_tracking_off(self):

@parser.command()
async def tracking_off(command: Command, pwi: PWI4):
    """mount tracking_off"""

    try:

        status = pwi.mount_tracking_off()
        command.info(
            is_tracking = status.mount.is_tracking,
        )
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish("done")

# pwi4 command: mount_follow_tle(self, tle_line_1, tle_line_2, tle_line_3):

# pwi4 command: mount_model_add_point(self, ra_j2000_hours, dec_j2000_degs):

# pwi4 command: mount_model_clear_points(self):

# pwi4 command: mount_model_save_as_default(self):

# pwi4 command: mount_model_save(self, filename):

# pwi4 command: mount_model_load(self, filename):
