# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from __future__ import annotations

from math import nan

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
@click.argument("AXIS", type=int)
async def enable(command: Command, pwi: PWI4, axis: int):
    """mount enable axis"""

    try:
        # we do ignore the false status returned
        pwi.mount_enable(axis)
        status = pwi.status()
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
        # we do ignore the false status returned
        pwi.mount_disable(axis)
        status = pwi.status()
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
            isenabled = status.mount.axis0.is_enabled and status.mount.axis1.is_enabled
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
async def goto_alt_az_j2000(command: Command, pwi: PWI4, alt_d: float, az_d: float):
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
# AXIS_reset
@click.option("--ra_reset", type=float, default=nan)
@click.option("--dec_reset", type=float, default=nan)
@click.option("--axis0_reset", type=float, default=nan)
@click.option("--axis1_reset", type=float, default=nan)
@click.option("--path_reset", type=float, default=nan)
@click.option("--transverse_reset", type=float, default=nan)
# AXIS_stop_rate
@click.option("--ra_stop_rate", type=float, default=nan)
@click.option("--dec_stop_rate", type=float, default=nan)
@click.option("--axis0_stop_rate", type=float, default=nan)
@click.option("--axis1_stop_rate", type=float, default=nan)
@click.option("--path_stop_rate", type=float, default=nan)
@click.option("--transverse_stop_rate", type=float, default=nan)
# AXIS_add_arcsec
@click.option("--ra_add_arcsec", type=float, default=nan)
@click.option("--dec_add_arcsec", type=float, default=nan)
@click.option("--axis0_add_arcsec", type=float, default=nan)
@click.option("--axis1_add_arcsec", type=float, default=nan)
@click.option("--path_add_arcsec", type=float, default=nan)
@click.option("--transverse_add_arcsec", type=float, default=nan)
# AXIS_set_rate_arcsec_per_sec
@click.option("--ra_set_rate_arcsec_per_sec", type=float, default=nan)
@click.option("--dec_set_rate_arcsec_per_sec", type=float, default=nan)
@click.option("--axis0_set_rate_arcsec_per_sec", type=float, default=nan)
@click.option("--axis1_set_rate_arcsec_per_sec", type=float, default=nan)
@click.option("--path_set_rate_arcsec_per_sec", type=float, default=nan)
@click.option("--transverse_set_rate_arcsec_per_sec", type=float, default=nan)
async def offset(command: Command, pwi: PWI4, **kwargs):
    """mount offset
     
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
        status = pwi.mount_offset(**{key: value for key, value in kwargs.items() if value is not nan})
        
        command.info(
            is_tracking=status.mount.is_tracking,
            is_connected=status.mount.is_connected,
            is_slewing=status.mount.is_slewing,
            altitude_degs=status.mount.altitude_degs,
            dec_apparent_degs=status.mount.dec_apparent_degs,
            field_angle_rate_at_target_degs_per_sec=status.mount.field_angle_rate_at_target_degs_per_sec,
            axis0 = {
                'dist_to_target_arcsec': status.mount.axis0.dist_to_target_arcsec,
                'is_enabled': status.mount.axis0.is_enabled,
                'position_degs': status.mount.axis0.position_degs,
                'rms_error_arcsec': status.mount.axis0.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis0.servo_error_arcsec,
            },
            axis1 = {
                'dist_to_target_arcsec': status.mount.axis1.dist_to_target_arcsec,
                'is_enabled': status.mount.axis1.is_enabled,
                'position_degs': status.mount.axis1.position_degs,
                'rms_error_arcsec': status.mount.axis1.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis1.servo_error_arcsec,
            },
            dec_j2000_degs=status.mount.dec_j2000_degs,
            geometry=status.mount.geometry,
            model = {
                'filename': status.mount.model.filename,
                'num_points_enabled': status.mount.model.num_points_enabled,
                'num_points_total': status.mount.model.num_points_total,
              
              'rms_error_arcsec': status.mount.model.rms_error_arcsec,
            },
            field_angle_at_target_degs=status.mount.field_angle_at_target_degs,
            ra_apparent_hours=status.mount.ra_apparent_hours,
            azimuth_degs=status.mount.azimuth_degs,
            field_angle_here_degs=status.mount.field_angle_here_degs,
            ra_j2000_hours=status.mount.ra_j2000_hours
        )

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
