"""Philips Hue Sync Box integration."""

from homeassistant.helpers import config_validation
import voluptuous

from . import const
from. import services


PLATFORM_SCHEMA = config_validation.PLATFORM_SCHEMA.extend({
    voluptuous.Required(const.CONF_IP_ADDRESS): config_validation.string,
    voluptuous.Optional(const.CONF_NAME): config_validation.string,
})


async def async_setup(hass, config):
  hass.data[const.DOMAIN] = {}
  return True
