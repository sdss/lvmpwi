# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from clu.command import Command

from lvmpwi.actor.commands import parser
from lvmpwi.pwi import PWI4


@parser.command()
async def status(command: Command, pwi: PWI4):
    """mount status"""

    try:
        status = pwi.status()

        return command.finish(
            is_tracking=status.mount.is_tracking,
            is_connected=status.mount.is_connected,
            is_slewing=status.mount.is_slewing,
            is_enabled=status.mount.axis0.is_enabled & status.mount.axis1.is_enabled,

            ra_j2000_hours=status.mount.ra_j2000_hours,
            dec_j2000_degs=status.mount.dec_j2000_degs,

            ra_apparent_hours=status.mount.ra_apparent_hours,
            dec_apparent_degs=status.mount.dec_apparent_degs,

            altitude_degs=status.mount.altitude_degs,
            azimuth_degs=status.mount.azimuth_degs,

            field_angle_rate_at_target_degs_per_sec=status.mount.field_angle_rate_at_target_degs_per_sec,
            field_angle_here_degs=status.mount.field_angle_here_degs,
            field_angle_at_target_degs=status.mount.field_angle_at_target_degs,

            axis0 = {
                'dist_to_target_arcsec': status.mount.axis0.dist_to_target_arcsec,
                'is_enabled': status.mount.axis0.is_enabled,
                'position_degs': status.mount.axis0.position_degs,
                'rms_error_arcsec': status.mount.axis0.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis0.servo_error_arcsec,
                'position_timestamp': status.mount.axis0.position_timestamp_str,
            },

            axis1 = {
                'dist_to_target_arcsec': status.mount.axis1.dist_to_target_arcsec,
                'is_enabled': status.mount.axis1.is_enabled,
                'position_degs': status.mount.axis1.position_degs,
                'rms_error_arcsec': status.mount.axis1.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis1.servo_error_arcsec,
                'position_timestamp': status.mount.axis1.position_timestamp_str,
            },
            model = {
                'filename': status.mount.model.filename,
                'num_points_enabled': status.mount.model.num_points_enabled,
                'num_points_total': status.mount.model.num_points_total,
                'rms_error_arcsec': status.mount.model.rms_error_arcsec,
            },

            geometry=status.mount.geometry,
        )

    except Exception as ex:
        return command.fail(error=ex)
