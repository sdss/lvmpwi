# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from clu.command import Command

from lvmpwi.actor.commands import parser
from lvmpwi.pwi import PWI4


@parser.command()
async def isconnected(command: Command, pwi: PWI4):
    """mount is connected"""

    try:
        status = pwi.status()
    
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish(
        isconnected=pwi.status().mount.is_connected
    )


@parser.command()
async def status(command: Command, pwi: PWI4):
    """mount status"""

    try:
        status = pwi.status()

    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish(
        is_tracking=status.mount.is_tracking,
        is_connected=status.mount.is_connected,
        is_slewing=status.mount.is_slewing,
        is_enabled=status.mount.axis0.is_enabled & status.mount.axis1.is_enabled,
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



@parser.command()
async def site(command: Command, pwi: PWI4):
    """site status"""

    try:
        status = pwi.status()
    except Exception as ex:
        return command.fail(error=str(ex))

    return command.finish(
        height_meters=status.site.height_meters,
        latitude_degs=status.site.latitude_degs,
        lmst_hours=status.site.lmst_hours,
        longitude_degs=status.site.longitude_degs,
    )

