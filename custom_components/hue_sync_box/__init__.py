"""Philips Hue Sync Box integration."""

from homeassistant.helpers import config_validation

from . import const
from . import schemas


async def async_setup(hass, config):
  """Set up the Philips Hue Sync Box component."""
  hass.data.setdefault(const.DOMAIN, schemas.REMOTE_SCHEMA)
  return True
