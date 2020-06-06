"""Defines services that Hue Sync Box component supports."""

import logging
import voluptuous

from homeassistant.helpers import config_validation
from homeassistant.helpers import service

from . import const

_LOGGER = logging.getLogger(__name__)

GET_ACCESS_TOKEN_SCHEMA = config_validation.make_entity_service_schema({})

SET_BRIGHTNESS_SCHEMA = config_validation.make_entity_service_schema({
    voluptuous.Required(const.ATTR_BRIGHTNESS): config_validation.positive_int,
})

SET_HDMI_INPUT_SCHEMA = config_validation.make_entity_service_schema({
    voluptuous.Required(const.ATTR_HDMI_INPUT): config_validation.string,
})

SET_INTENSITY_SCHEMA = config_validation.make_entity_service_schema({
    voluptuous.Required(const.ATTR_INTENSITY): config_validation.string,
    voluptuous.Optional(const.ATTR_SYNC_MODE): config_validation.string,
})

SET_SYNC_MODE_SCHEMA = config_validation.make_entity_service_schema({
    voluptuous.Required(const.ATTR_SYNC_MODE): config_validation.string,
})


def register_services(hass):
  """Registers custom services for hue_sync_box."""
  _LOGGER.debug('Registering services for Hue Sync Box.')

  get_access_token_service = create_get_access_token_service(hass)
  hass.services.async_register(
      const.DOMAIN,
      const.SERVICE_GET_ACCESS_TOKEN,
      get_access_token_service,
      schema=GET_ACCESS_TOKEN_SCHEMA,
  )

  set_brightness_service = create_get_access_token_service(hass)
  hass.services.async_register(
      const.DOMAIN,
      const.SERVICE_SET_BRIGHTNESS,
      set_brightness_service,
      schema=SET_BRIGHTNESS_SCHEMA,
  )

  set_hdmi_input_service = create_set_hdmi_input_service(hass)
  hass.services.async_register(
      const.DOMAIN,
      const.SERVICE_SET_HDMI_INPUT,
      set_hdmi_input_service,
      schema=SET_HDMI_INPUT_SCHEMA,
  )

  set_intensity_service = create_set_intensity_service(hass)
  hass.services.async_register(
      const.DOMAIN,
      const.SERVICE_SET_INTENSITY,
      set_intensity_service,
      schema=SET_INTENSITY_SCHEMA,
  )

  sync_mode_service = create_set_sync_mode_service(hass)
  hass.services.async_register(
      const.DOMAIN,
      const.SERVICE_SET_SYNC_MODE,
      sync_mode_service,
      schema=SET_SYNC_MODE_SCHEMA,
  )


def unregister_services(hass):
  """Unregisters custom services from hue_sync_box."""
  hass.services.async_remove(const.DOMAIN, const.SERVICE_GET_ACCESS_TOKEN)
  hass.services.async_remove(const.DOMAIN, const.SERVICE_SET_BRIGHTNESS)
  hass.services.async_remove(const.DOMAIN, const.SERVICE_SET_HDMI_INPUT)
  hass.services.async_remove(const.DOMAIN, const.SERVICE_SET_INTENSITY)
  hass.services.async_remove(const.DOMAIN, const.SERVICE_SET_SYNC_MODE)


def create_get_access_token_service(hass):
  """Returns service for get_access_token."""
  async def async_get_access_token(call):
    _LOGGER.debug(
        f'hue_syc_box async_get_access_token handler called '
        f'with data: {call.data}.')

    entity_ids = call.data.get(const.ATTR_ENTITY_ID)

    for entity_id in entity_ids:
      entity = hass.data[const.DOMAIN].get(entity_id)
      if entity_id:
        await entity.async_get_access_token()

  return async_get_access_token


def create_set_brightness(hass):
  """Returns service for set_brightness."""
  async def async_set_brightness(call):
    _LOGGER.debug(
        f'hue_syc_box async_set_brightness handler called '
        f'with data: {call.data}.')

    entity_ids = call.data.get(const.ATTR_ENTITY_ID)
    brightness = call.data.get(const.ATTR_BRIGHTNESS)

    for entity_id in entity_ids:
      entity = hass.data[const.DOMAIN].get(entity_id)
      if entity_id:
        await entity.async_set_brightness(brightness)

  return async_set_brightness


def create_set_hdmi_input_service(hass):
  """Returns service for set_hdmi_input."""
  async def async_set_hdmi_input(call):
    _LOGGER.debug(
        f'hue_syc_box create_set_hdmi_input_service handler called '
        f'with data: {call.data}.')

    entity_ids = call.data.get(const.ATTR_ENTITY_ID)
    hdmi_input = call.data.get(const.ATTR_HDMI_INPUT)

    for entity_id in entity_ids:
      entity = hass.data[const.DOMAIN].get(entity_id)
      if entity_id:
        await entity.async_set_hdmi_input(hdmi_input)

  return async_set_hdmi_input


def create_set_intensity_service(hass):
  """Returns service for set_intensity."""
  async def async_set_intensity(call):
    _LOGGER.debug(
        f'hue_syc_box async_set_intensity handler called '
        f'with data: {call.data}.')

    entity_ids = call.data.get(const.ATTR_ENTITY_ID)
    intensity = call.data.get(const.ATTR_INTENSITY)
    sync_mode = call.data.get(const.ATTR_SYNC_MODE)

    for entity_id in entity_ids:
      entity = hass.data[const.DOMAIN].get(entity_id)
      if entity_id:
        await entity.async_set_intensity(intensity, sync_mode)

  return async_set_intensity


def create_set_sync_mode_service(hass):
  """Returns service for set_sync_mode."""
  async def async_set_sync_mode(call):
    _LOGGER.debug(
        f'hue_syc_box async_set_sync_mode handler called '
        f'with data: {call.data}.')

    entity_ids = call.data.get(const.ATTR_ENTITY_ID)
    sync_mode = call.data.get(const.ATTR_SYNC_MODE)

    for entity_id in entity_ids:
      entity = hass.data[const.DOMAIN].get(entity_id)
      if entity_id:
        await entity.async_set_sync_mode(sync_mode)

  return async_set_sync_mode
