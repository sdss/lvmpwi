# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: mount.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from __future__ import annotations

from math import nan

import click
import asyncio
from clu.command import Command

from lvmpwi.actor.exceptions import *
from lvmpwi.actor.commands import parser
from lvmpwi.pwi import PWI4


@parser.command("setConnected")
@click.argument("enable", type=bool)
async def setConnected(command: Command, pwi: PWI4, enable:bool):
    """set mount connected true/false """

    try:
        status = pwi.mount_connect() if enable else pwi.mount_disconnect()

        return command.finish(
            isconnected = status.mount.is_connected
        )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("setEnabled")
@click.argument("enable", type=bool)
@click.option("--axis0", type=bool, default=True)
@click.option("--axis1", type=bool, default=True)
async def setEnabled(command: Command, pwi: PWI4, enable:bool, axis0:bool, axis1:bool):
    """mount enable/disable axis"""

    try:
        if axis0:
            pwi.mount_enable(0) if enable else pwi.mount_disable(0)
        if axis1:
            pwi.mount_enable(1) if enable else pwi.mount_disable(1)
            
        await asyncio.sleep(0.1)

        status = pwi.status()
        return command.finish(
            is_enabled = status.mount.axis1.is_enabled & status.mount.axis0.is_enabled,
            axis0 = {
                'is_enabled': status.mount.axis0.is_enabled,
            },
            axis1 = {
                'is_enabled': status.mount.axis1.is_enabled,
            },
    )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("setTracking")
@click.argument("enable", type=bool)
async def setTracking(command: Command, pwi: PWI4, enable:bool):
    """mount enable/disable tracking"""

    try:
        status = pwi.mount_tracking_on() if enable else pwi.mount_tracking_off()

        await asyncio.sleep(0.1)

        status = pwi.status()
        return command.finish(
            is_tracking = status.mount.is_tracking,
        )
    
    except Exception as ex:
        return command.fail(error=ex)


@parser.command()
async def stop(command: Command, pwi: PWI4):
    """mount stop"""

    try:
        status = pwi.mount_stop()
    
        await asyncio.sleep(0.1)
        status = pwi.status()
        
        return command.finish(
            is_slewing=status.mount.is_slewing,
            is_tracking=status.mount.is_tracking,
            is_enabled = status.mount.axis0.is_enabled and status.mount.axis1.is_enabled,
            axis0 = {
                'is_enabled': status.mount.axis0.is_enabled,
            },
            axis1 = {
                'is_enabled': status.mount.axis1.is_enabled,
            },
        )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("setSlewTimeConstant")
@click.argument("TIME", type=int)
async def setSlewTimeConstant(command: Command, pwi: PWI4, time: int):
    """mount set_slew_time_constant"""

    try:
        status = pwi.mount_set_slew_time_constant()

        return command.finish(
            is_enabled = status.mount.axis0.is_enabled and status.mount.axis1.is_enabled,
            axis0 = {
                'is_enabled': status.mount.axis0.is_enabled,
            },
            axis1 = {
                'is_enabled': status.mount.axis1.is_enabled,
            },
        )
    
    except Exception as ex:
        return command.fail(error=ex)


def checkIfMountCanMove(status):
        if not status.mount.is_connected:
            raise PwiActorMountNotConnected()

        if not (status.mount.axis0.is_enabled & status.mount.axis1.is_enabled):
            raise PwiActorMountAxisNotEnabled()


async def waitUntilEndOfSlew(command: Command, pwi: PWI4):
    while(True):
        status = pwi.status()
        
        command.info(
            is_slewing=status.mount.is_slewing,
            
            ra_j2000_hours=status.mount.ra_j2000_hours,
            dec_j2000_degs=status.mount.dec_j2000_degs,
            
            ra_apparent_hours=status.mount.ra_apparent_hours,
            dec_apparent_degs=status.mount.dec_apparent_degs,
            
            altitude_degs=status.mount.altitude_degs,
            azimuth_degs=status.mount.azimuth_degs,
            
            field_angle_here_degs=status.mount.field_angle_here_degs,
            field_angle_rate_at_target_degs_per_sec=status.mount.field_angle_rate_at_target_degs_per_sec,
            field_angle_at_target_degs=status.mount.field_angle_at_target_degs,
            
            axis0 = {
                'dist_to_target_arcsec': status.mount.axis0.dist_to_target_arcsec,
                'position_degs': status.mount.axis0.position_degs,
                'rms_error_arcsec': status.mount.axis0.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis0.servo_error_arcsec,
            },
            
            axis1 = {
                'dist_to_target_arcsec': status.mount.axis1.dist_to_target_arcsec,
                'position_degs': status.mount.axis1.position_degs,
                'rms_error_arcsec': status.mount.axis1.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis1.servo_error_arcsec,
            },
        )
        for i in range(5):
            status = pwi.status()
            if not status.mount.is_slewing:
                return
            await asyncio.sleep(0.1)
            
        
@parser.command("gotoRaDecJ2000")
@click.argument("RA_H", type=float)
@click.argument("DEG_D", type=float)
async def gotoRaDecJ2000(command: Command, pwi: PWI4, ra_h: float, deg_d: float):
    """mount goto_ra_dec_j2000"""

    try:
        status = pwi.mount_goto_ra_dec_j2000(ra_h, deg_d)
        checkIfMountCanMove(status)
        
        await waitUntilEndOfSlew(command, pwi)
    
        status = pwi.status()
        return command.finish(
            ra_j2000_hours = status.mount.ra_j2000_hours,
            dec_j2000_degs = status.mount.dec_j2000_degs,
        )
    except Exception as ex:
        return command.fail(error=ex)


@parser.command("gotoRaDecApparent")
@click.argument("RA_H", type=float)
@click.argument("DEG_D", type=float)
async def gotoRaDecApparent(command: Command, pwi: PWI4, ra_h: float, deg_d: float):
    """mount goto_ra_dec_apparent """

    try:
        status = pwi.mount_goto_ra_dec_apparent(ra_h, deg_d)
        checkIfMountCanMove(status)

        await waitUntilEndOfSlew(command, pwi)
    
        status = pwi.status()
        return command.finish(
            ra_apparent_hours = status.mount.ra_apparent_hours,
            dec_apparent_degs = status.mount.dec_apparent_degs,
        )
    
    except Exception as ex:
        return command.fail(error=ex)


@parser.command("gotoAltAzJ2000")
@click.argument("ALT_D", type=float)
@click.argument("AZ_D", type=float)
async def gotoAltAzJ2000(command: Command, pwi: PWI4, alt_d: float, az_d: float):
    """mount goto_alt_az_j2000"""

    try:
        status = pwi.mount_goto_alt_az(alt_d, az_d)
        checkIfMountCanMove(status)

        await waitUntilEndOfSlew(command, pwi)
    
        status = pwi.status()
        return command.finish(
            altitude_degs = status.mount.altitude_degs,
            azimuth_degs = status.mount.azimuth_degs,
        )
    
    except Exception as ex:
        return command.fail(error=ex)


@parser.command("findHome")
async def findHome(command: Command, pwi: PWI4):
    """mount find_home"""

    try:
        status = pwi.mount_find_home()
        checkIfMountCanMove(status)
    
        await waitUntilEndOfSlew(command, pwi)

        status = pwi.status()
        return command.finish(
            dec_j2000_degs = status.mount.dec_j2000_degs,
            ra_j2000_hours = status.mount.ra_j2000_hours,
            axis0 = {
                'position_degs': status.mount.axis0.position_degs,
            },
            axis1 = {
                'position_degs': status.mount.axis1.position_degs,
            },
        )
    
    except Exception as ex:
        return command.fail(error=ex)


@parser.command()
async def park(command: Command, pwi: PWI4):
    """mount park"""

    try:
        status = pwi.mount_park()
        checkIfMountCanMove(status)

        await waitUntilEndOfSlew(command, pwi)

        status = pwi.status()
        return command.finish(
            dec_j2000_degs = status.mount.dec_j2000_degs,
            ra_j2000_hours = status.mount.ra_j2000_hours,
            axis0 = {
                'position_degs': status.mount.axis0.position_degs,
            },
            axis1 = {
                'position_degs': status.mount.axis1.position_degs,
            },
        )
    
    except Exception as ex:
        return command.fail(error=ex)



# pwi4 command: mount_set_park_here(self):

@parser.command("parkHere")
async def parkHere(command: Command, pwi: PWI4):
    """mount park"""

    try:
        status = pwi.mount_park_here()
        checkIfMountCanMove(status)

        await waitUntilEndOfSlew(command, pwi)

        status = pwi.status()
        return command.finish(
            dec_j2000_degs = status.mount.dec_j2000_degs,
            ra_j2000_hours = status.mount.ra_j2000_hours,
            axis0 = {
                'position_degs': status.mount.axis0.position_degs,
            },
            axis1 = {
                'position_degs': status.mount.axis1.position_degs,
            },
        )
    
    except Exception as ex:
        return command.fail(error=ex)


async def waitUntilAxisErrorIsBelowLimit(command: Command, pwi: PWI4, axis_error=0.2):
    while(True):
        for i in range(5):
            status = pwi.status()
            if status.mount.axis0.rms_error_arcsec < axis_error and status.mount.axis1.rms_error_arcsec < axis_error:
                return
            await asyncio.sleep(0.1)

        command.info(
            is_slewing=status.mount.is_slewing,
            
            ra_j2000_hours=status.mount.ra_j2000_hours,
            dec_j2000_degs=status.mount.dec_j2000_degs,
            
            ra_apparent_hours=status.mount.ra_apparent_hours,
            dec_apparent_degs=status.mount.dec_apparent_degs,
            
            altitude_degs=status.mount.altitude_degs,
            azimuth_degs=status.mount.azimuth_degs,
            
            field_angle_here_degs=status.mount.field_angle_here_degs,
            field_angle_rate_at_target_degs_per_sec=status.mount.field_angle_rate_at_target_degs_per_sec,
            field_angle_at_target_degs=status.mount.field_angle_at_target_degs,
            
            axis0 = {
                'dist_to_target_arcsec': status.mount.axis0.dist_to_target_arcsec,
                'position_degs': status.mount.axis0.position_degs,
                'rms_error_arcsec': status.mount.axis0.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis0.servo_error_arcsec,
            },
            
            axis1 = {
                'dist_to_target_arcsec': status.mount.axis1.dist_to_target_arcsec,
                'position_degs': status.mount.axis1.position_degs,
                'rms_error_arcsec': status.mount.axis1.rms_error_arcsec,
                'servo_error_arcsec': status.mount.axis1.servo_error_arcsec,
            },
        )
            
        

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
        checkIfMountCanMove(status)

        await waitUntilAxisErrorIsBelowLimit(command, pwi, axis_error=0.1)
        
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
            field_angle_at_target_degs=status.mount.field_angle_at_target_degs,
            field_angle_here_degs=status.mount.field_angle_here_degs,

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
        )


    except Exception as ex:
        return command.fail(error=ex)

    
