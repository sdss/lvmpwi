# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de
# @Date: 2021-07-06
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from contextlib import suppress

from clu.actor import AMQPActor

from lvmpwi import __version__
from lvmpwi.actor.commands import parser as pwi_command_parser
from lvmpwi.pwi import PWI4

from .commands.mount import statusTick

__all__ = ["lvmpwi"]


class lvmpwi(AMQPActor):
    """PWI actor.
    """

    parser = pwi_command_parser
    
    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        self.schema = {
                    "type": "object",
                    "properties": {
                       "is_connected": {"type": "boolean"},
                       "is_slewing": {"type": "boolean"},
                       "is_enabled": {"type": "boolean"},
                       "is_tracking": {"type": "boolean"},

                       "ra_j2000_hours" : {"type": "number"},
                       "dec_j2000_degs" : {"type": "number"},
                       
                       "ra_apparent_hours" : {"type": "number"},
                       "dec_apparent_degs" : {"type": "number"},

                       "altitude_degs" : {"type": "number"},
                       "azimuth_degs" : {"type": "number"},

                       "field_angle_at_target_degs" : {"type": "number"},
                       "field_angle_here_degs" : {"type": "number"},
                       "field_angle_rate_at_target_degs_per_sec" : {"type": "number"},

                       "axis0": {
                           "dist_to_target_arcsec" : {"type": "number"},
                           "is_enabled" : {"type": "boolean"},
                           "position_degs" : {"type": "number"},
                           "rms_error_arcsec" : {"type": "number"},
                           "servo_error_arcsec" : {"type": "number"},
                           "min_mech_position_degs" : {"type": "number"},
                           "max_mech_position_degs" : {"type": "number"},
                           "target_mech_position_degs" : {"type": "number"},
                           "max_velocity_degs_per_sec" : {"type": "number"},
                           "setpoint_velocity_degs_per_sec" : {"type": "number"},
                           "measured_velocity_degs_per_sec" : {"type": "number"},
                           "acceleration_degs_per_sec_sqr" : {"type": "number"},
                           "measured_current_amps" : {"type": "number"},
                        },
                       "axis1": {
                           "dist_to_target_arcsec" : {"type": "number"},
                           "is_enabled" : {"type": "boolean"},
                           "position_degs" : {"type": "number"},
                           "rms_error_arcsec" : {"type": "number"},
                           "servo_error_arcsec" : {"type": "number"},
                           "min_mech_position_degs" : {"type": "number"},
                           "max_mech_position_degs" : {"type": "number"},
                           "target_mech_position_degs" : {"type": "number"},
                           "max_velocity_degs_per_sec" : {"type": "number"},
                           "setpoint_velocity_degs_per_sec" : {"type": "number"},
                           "measured_velocity_degs_per_sec" : {"type": "number"},
                           "acceleration_degs_per_sec_sqr" : {"type": "number"},
                           "measured_current_amps" : {"type": "number"},
                        },
                       "model": {
                           "filename" : {"type": "string"},
                           "num_points_enabled" : {"type": "number"},
                           "position_degs" : {"type": "number"},
                           "num_points_total" : {"type": "number"},
                           "rms_error_arcsec" : {"type": "number"},
                        },
                       "geometry" : {"type": "number"},
                     },
                     "additionalProperties": False,
        }

        self.load_schema(self.schema, is_file=False)

    async def start(self):
        await super().start()

        assert len(self.parser_args) == 1
       
        self.log.debug(f"Start pwi ...")

        pwi = self.parser_args[0]
        self.log.debug(f"{type(self.parser_args)}")

        status = pwi.status()
        self.log.debug(f"is_connected {status.mount.is_connected}")


        self.statusLock = asyncio.Lock()
        self.statusTask = self.loop.create_task(statusTick(self, pwi, 1.0))

        self.log.debug("Start done")

    async def stop(self):
        return super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from a configuration file."""


        instance = super(lvmpwi, cls).from_config(config, *args, version=__version__,**kwargs)

        instance.log.info("Hello world")

        assert isinstance(instance, lvmpwi)
        assert isinstance(instance.config, dict)
        
        instance.log.debug(str(instance.config))

        pwi = PWI4()


        instance.log.debug(str(type(pwi)))
        
        instance.parser_args = [ pwi ]

        return instance
