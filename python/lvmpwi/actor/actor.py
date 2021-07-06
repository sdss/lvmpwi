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

from lvmpwi.actor.commands import parser as pwi_command_parser
from lvmpwi.pwi import PWI4

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

    async def start(self):
        await super().start()

        assert len(self.parser_args) == 1
       
        try:
            self.log.debug(f"Start pwi ...")

            pwi = self.parser_args[0]
            self.log.debug(f"{type(self.parser_args)}")
            
            status = pwi.status()
            self.log.debug(f"is_connected {status.mount.is_connected}")


        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")

        self.log.debug("Start done")

    async def stop(self):
        return super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from a configuration file."""


        instance = super(lvmpwi, cls).from_config(config, *args, **kwargs)

        instance.log.info("Hello world")

        assert isinstance(instance, lvmpwi)
        assert isinstance(instance.config, dict)
        
        instance.log.debug(str(instance.config))

        pwi = PWI4()
         
        instance.log.debug(str(type(pwi)))
        
        instance.parser_args = [ pwi ]

        return instance
