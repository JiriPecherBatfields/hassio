import aiohttp
import asyncio
import async_timeout
import json
import logging
import datetime
import re

#import voluptuous as vol
from typing import Dict

#from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.helpers import aiohttp_client

_LOGGER = logging.getLogger(__name__)

_MONTH = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "maj": 5,
    "jun": 6, 
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "nov": 11,
    "dec": 12}

async def async_setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the computer switch platform."""
    entities = config.get('entities', {})
    devices = []

    session = aiohttp_client.async_get_clientsession(hass)

    for entity in entities:
        devices.append(SwedishRecyclingSensor(hass, session, entity,
                                              entities[entity]['station_id'],
                                              entities[entity]['use_as_state']))

    add_devices(devices, True)


class SwedishRecyclingSensor(Entity):
    def __init__(self, hass, session: aiohttp.ClientSession, name: str, station_id: str,
        use_as_state: str) -> None:
        """Initialize the ComputerSwitch entity."""
        # use wakeonlan package
        #import wakeonlan

        self._name = "swe_recycling_{}".format(name)
        self._station_id = station_id
        self._use_as_state = use_as_state
        self._session = session
        self._available = False
        self._attributes = {}
        _LOGGER.info("Init Swedish recycling {} with station_id {} and use state {}".format(
            self._name, self._station_id, self._use_as_state))

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def unique_id(self):
        """Return the unique ID of the device."""
        return self._name

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def icon(self):
        """Return the icon of the entity."""
        return 'mdi:trash-can-outline'

    @property
    def state(self):
        """Return the state of the switch."""

        for attr, value in self._attributes.items():
            if attr.lower() == self._use_as_state.lower():
                if value.date() == datetime.datetime.today().date():
                    return "on"
                else:
                    return "off"

        return "unavailable"
    
    @property
    def available(self):
        return self._available

    @property
    def device_state_attributes(self) -> Dict[str, str]:
        """Return the state attributes."""
        return self._attributes

    @Throttle(datetime.timedelta(minutes=60))
    async def async_update(self):
        """Update setting state."""
        try:
            with async_timeout.timeout(30, loop=self.hass.loop):
                self._attributes = await self.get_data()
               
                if len(self._attributes) > 0:
                    self._available = True
                else:
                    self._available = False
        except (asyncio.TimeoutError):
            self._available = False
            _LOGGER.error("Timeout fetching recycling data")

    async def get_data(self) -> Dict[str, str]:

        api_url = "https://webapp.ftiab.se/Code/Ajax/StationHandler.aspx/GetStationMaintenance"
        payload = '{"stationId": "'+ self._station_id + '"}'
        headers = {'Content-Type': 'application/json'}
        data_json = {}

        async with self._session.post(api_url, data=payload, headers=headers) as response:
            if response.status != 200:
                # Do some logging
                _LOGGER.warn("Fail to get Swedish recycle information {}, {}"
                             .format(self._name, self._station_id))
                return {}
            data = await response.text()
            response_json = json.loads(data)
            data_json = json.loads(response_json["d"])
            response_data = {}
            for attr, value in data_json.items():
                
                if 'kl' in value:
                    regular_expression = '([0-9]+)\s([a-z]{3})\skl\s([0-9]+):([0-9]+)'
                else:
                    regular_expression = '([0-9]+)\s([a-z]{3})'
                date_split = re.split(regular_expression, value)
                if len(date_split) >1:
                    year = datetime.datetime.now().year
                    month = _MONTH[date_split[2]]
                    if (month < datetime.datetime.now().month and attr.startswith('Next')):
                        year = year + 1
                    
                    if len(date_split) == 4:
                        response_data[attr] = datetime.datetime(year, month, int(date_split[1]))
                    else:
                        response_data[attr] = datetime.datetime(year, month, int(date_split[1]), \
                            int(date_split[3]), int(date_split[4]))
                else:
                    response_data[attr] = value

            return response_data
