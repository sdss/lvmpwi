# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmpwi.actor.commands import parser
from lvmpwi.pwi import PWI4


def _model_status(status):
    """site status"""

    return {
            "filename": status.mount.model.filename,
            "num_points_enabled": status.mount.model.num_points_enabled,
            "num_points_total": status.mount.model.num_points_total,
            "rms_error_arcsec": status.mount.model.rms_error_arcsec,
        }


@parser.command("model")
async def model(command: Command, pwi: PWI4):
    """site status"""

    try:
        status = pwi.status()

        print (type(status.mount))
        print (status.mount)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("modelAddPoint")
@click.argument("ra_j2000_hours", type=float)
@click.argument("dec_j2000_degs", type=float)
async def modelAddPoint(command: Command, pwi: PWI4, ra_j2000_hours, dec_j2000_degs):
    """
    Add a calibration point to the pointing model, mapping the current pointing direction
    of the telescope to the secified J2000 Right Ascension and Declination values.

    This call might be performed after manually centering a bright star with a known
    RA and Dec, or the RA and Dec might be provided by a PlateSolve solution
    from an image taken at the current location.
    """

    try:
        status = pwi.mount_model_add_point(ra_j2000_hours, dec_j2000_degs)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)



@parser.command("modelDeletePoint")
@click.argument("POINTS", nargs=-1, type=int)
async def modelDeletePoint(command: Command, pwi: PWI4, points):
#async def mount_model_delete_point(self, *point_indexes_0_based):
    """
    Remove one or more calibration points from the pointing model.

    Points are specified by index, ranging from 0 to (number_of_points-1).

    Added in PWI 4.0.11 beta 9

    Examples:
        mount_model_delete_point(0)  # Delete the first point
        mount_model_delete_point(1, 3, 5)  # Delete the second, fourth, and sixth points
        mount_model_delete_point(*range(20)) # Delete the first 20 points
    """

    try:
        status = pwi.mount_model_delete_point(*points)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("modelEnablePoint")
@click.argument("POINTS", nargs=-1, type=int)
async def modelEnablePoint(command: Command, pwi: PWI4, points):
    """
    Flag one or more calibration points as "enabled", meaning that these points
    will contribute to the fit of the model.

    Points are specified by index, ranging from 0 to (number_of_points-1).

    Added in PWI 4.0.11 beta 9

    Examples:
        mount_model_enable_point(0)  # Enable the first point
        mount_model_enable_point(1, 3, 5)  # Enable the second, fourth, and sixth points
        mount_model_enable_point(*range(20)) # Enable the first 20 points
    """

    point_indexes_comma_separated = list_to_comma_separated_string(point_indexes_0_based)
    return self.request_with_status("/mount/model/enable_point", index=point_indexes_comma_separated)

    try:
        status = pwi.mount_model_enable_point(*points)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("modelDisablePoint")
@click.argument("POINTS", nargs=-1, type=int)
async def modelDisablePoint(command: Command, pwi: PWI4, points):
    """
    Flag one or more calibration points as "disabled", meaning that these calibration
    points will still be stored but will not contribute to the fit of the model.

    If a point is suspected to be an outlier, it can be disabled. This will cause the model
    to re-fit, and the point's deviation from the newly-fit model can be re-examined before
    being deleted entirely.

    Points are specified by index, ranging from 0 to (number_of_points-1).

    Added in PWI 4.0.11 beta 9

    Examples:
        modelDisablePoint(0)  # Disable the first point
        modelDisablePoint(1, 3, 5)  # Disable the second, fourth, and sixth points
        modelDisablePoint(*range(20)) # Disable the first 20 points
        modelDisablePoint(            # Disable all points
            *range(
                pwi4.status().mount.model.num_points_total
            ))
    """

    try:
        status = pwi.mount_model_disable_point(*points)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("modelClearPoints")
async def modelClearPoints(command: Command, pwi: PWI4):
    """
    Remove all calibration points from the pointing model.
    """

    try:
        status = pwi.mount_model_clear_points()

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


#async def mount_model_save_as_default(self):
        #"""
        #Save the active pointing model as the model that will be loaded
        #by default the next time the mount is connected.
        #"""

        #return self.request_with_status("/mount/model/save_as_default")

@parser.command("modelSave")
@click.argument("filename", type=str)
async def modelSave(command: Command, pwi: PWI4, filename: str):
#async def mount_model_save(self, filename):
    """
    Save the active pointing model to a file so that it can later be re-loaded
    by a call to mount_model_load().

    This may be useful when switching between models built for different instruments.
    For example, a system might have one model for the main telescope, and another
    model for a co-mounted telescope.
    """

    try:
        status = pwi.mount_model_save(filename)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


@parser.command("modelLoad")
@click.argument("filename", type=str)
async def modelLoad(command: Command, pwi: PWI4, filename: str):
    """
    Load a model from the specified file and make it the active model.

    This may be useful when switching between models built for different instruments.
    For example, a system might have one model for the main telescope, and another
    model for a co-mounted telescope.
    """

    try:
        status = pwi.mount_model_load(filename)

        return command.finish(model = _model_status(status) )

    except Exception as ex:
        return command.fail(error=ex)


