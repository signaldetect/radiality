"""
radiality:radiality.base

The `radiality/base.py` is a part of `radiality`.
Apache 2.0 licensed.
"""

import json
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed

from radiality.reaction import Effector
from radiality import watch
from radiality import utils
from radiality import circuit


class Subsystem(watch.Loggable, circuit.Connectable):
    """
    Subsystem components container
    """
    logger_name = 'core.app'

    eventer = None  # default eventer, type: class
    effector = Effector  # default effector, type: class
    effectors = {}  # type: dict of str -> class

    _eventer_inst = None  # type: Eventer

    def __init__(self, logging_config, connection_config):
        """
        Initialization
        """
        self._logger = watch.Logger(
            config_path=logging_config, name=self.logger_name
        )
        self._connector = circuit.Connector(
            logger=self._logger,
            config_path=connection_config,
            wanted=self.effectors.keys()
        )

        if self.eventer:
            self._eventer_inst = self.eventer(
                logger=self._logger, connector=self._connector
            )
        else:
            raise Exception(
                'The `eventer` for the `{0}` subsystem '
                'is not specified'.format(self.sid)
            )

    def launch(self):
        """
        Launches the subsystem
        """
        event_loop = asyncio.get_event_loop()

        try:
            serving = websockets.serve(
                ws_handler=self._receiver,
                host=self.host,
                port=self.port,
                timeout=utils.MSG_TIMEOUT,
                max_size=utils.MSG_MAX_SIZE
            )
            event_loop.run_until_complete(serving)

            event_loop.run_until_complete(self.launched())

            event_loop.run_forever()
        finally:
            event_loop.close()

    # overridden from `circuit.Connectable`
    async def connect(self, sid, freq):
        effector_inst = Effector(
            logger=self._logger,
            connector=self._connector,
            eventer=self._eventer_inst,
            channel=None
        )
        channel = await effector_inst.connect(sid, freq)

        return channel

    async def launched(self):
        self.log('Serving on `{0}`'.format(self.freq))

    async def _receiver(self, channel, path):
        try:
            data = await channel.recv()
            data = json.loads(data)
        except ConnectionClosed:
            self.fail('Connection closed')
        except ValueError:
            self.fail('Invalid input -- could not decode data: %s', str(data))
        else:
            await self._parse(data, channel)

    async def _parse(self, data, channel):
        signal = data.get('*signal', None)
        sid = data.get('sid', None)

        if signal == 'connecting':
            freq = data.get('freq', None)
            channel = await self._eventer_inst.connect(sid, freq)
        elif signal == 'connected':
            self.log('Connected to `%s`', sid)
        elif signal == 'biconnected':
            self.log('Biconnected to `%s`', sid)
            self._eventer_inst.register_effector(sid, channel)
        elif signal is None:
            self.fail('Invalid input -- could not decode data: %s', str(data))
        else:
            self.warn('Unknown signal -- %s', str(signal))

        if sid in self.wanted:
            await self._receiving(sid, channel)

    async def _receiving(self, sid, channel):
        self.log('Receiving the `%s` subsystem', sid)

        effector_inst = self.effectors.get(sid, self.effector)(
            logger=self._logger,
            connector=self._connector,
            eventer=self._eventer_inst,
            channel=channel
        )

        receiving = True
        while receiving:
            try:
                receiving = await effector_inst.activate()
            except Exception as exc:
                self.log(exc, exc_info=True)
