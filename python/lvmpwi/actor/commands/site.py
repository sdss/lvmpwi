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
async def site(command: Command, pwi: PWI4):
    """site status"""

    try:
        status = pwi.status()

        return command.finish(
            height_meters=status.site.height_meters,
            latitude_degs=status.site.latitude_degs,
            lmst_hours=status.site.lmst_hours,
            longitude_degs=status.site.longitude_degs,
        )

    except Exception as ex:
        return command.fail(error=ex)

