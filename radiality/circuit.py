"""
radiality:radiality.circuit

The `radiality/circuit.py` is a part of `radiality`.
Apache 2.0 licensed.
"""

import os
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed

from radiality import watch
from radiality import utils


class Connector(watch.Loggable):
    """
    Connection
    """
    WAIT_TIME = 1  # 1 sec

    _sid = None  # type: str
    _host = None  # type: str
    _port = None  # type: int
    _freq = None  # type: str
    _wanted = None  # type: list of str

    def __init__(self, logger, config_path, wanted):
        """
        Setups the connection configuration
        """
        self._logger = logger

        if os.path.exists(config_path):
            config = utils.load_config(config_path)
        else:
            raise Exception()

        self._sid = config.get('sid', None)
        if self._sid is None:
            raise Exception()

        self._host = config.get('host', '127.0.0.1')
        try:
            self._port = int(config.get('port', 80))
        except ValueError:
            raise Exception()

        if self._host and self._port:
            self._freq = utils.subsystem_freq(host=self._host, port=self._port)
        else:
            raise Exception()

        self._wanted = wanted

    @property
    def sid(self):
        return self._sid

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def freq(self):
        return self._freq

    @property
    def wanted(self):
        return self._wanted

    async def connect(self, sid, freq):
        channel = None

        while True:
            try:
                channel = await websockets.connect(
                    freq,
                    timeout=utils.MSG_TIMEOUT,
                    max_size=utils.MSG_MAX_SIZE
                )
            except Exception as exc:
                self.warn('Connection failed: %s. Waiting...', str(exc))
                await asyncio.sleep(self.WAIT_TIME)
            else:
                break

        return channel

    async def disconnect(self, sid, channel):
        try:
            await channel.close()
        except ConnectionClosed:
            self.warn('Connection to `%s` already closed', sid)
        finally:
            del channel


class Connectable:
    """
    Mixin for the capability of being connected with other subsystem
    """
    _connector = None  # type: Connector

    @property
    def sid(self):
        return self._connector.sid

    @property
    def host(self):
        return self._connector.host

    @property
    def port(self):
        return self._connector.port

    @property
    def freq(self):
        return self._connector.freq

    @property
    def wanted(self):
        return self._connector.wanted

    async def connect(self, sid, freq):
        channel = await self._connector.connect(sid, freq)
        return channel

    async def disconnect(self, sid, channel):
        await self._connector.disconnect(sid, channel)
