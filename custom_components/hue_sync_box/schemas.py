"""Defines all services schemas."""

import voluptuous

from homeassistant.helpers import config_validation

from . import const

# Domain schemas.
_CUSTOM_REMOTE_SCHEMA = {
    voluptuous.Required(const.CONF_IP_ADDRESS): config_validation.string,
    voluptuous.Optional(const.CONF_NAME): config_validation.string,
}

REMOTE_SCHEMA = config_validation.PLATFORM_SCHEMA.extend(_CUSTOM_REMOTE_SCHEMA)

# Service schemas.
GET_ACCESS_TOKEN_SCHEMA = {}

SET_BRIGHTNESS_SCHEMA = {
    voluptuous.Required(const.ATTR_BRIGHTNESS): config_validation.positive_int,
}

SET_HDMI_INPUT_SCHEMA = {
    voluptuous.Required(const.ATTR_HDMI_INPUT): config_validation.string,
}

SET_INTENSITY_SCHEMA = {
    voluptuous.Required(const.ATTR_INTENSITY): config_validation.string,
    voluptuous.Optional(const.ATTR_SYNC_MODE): config_validation.string,
}

SET_SYNC_MODE_SCHEMA = {
    voluptuous.Required(const.ATTR_SYNC_MODE): config_validation.string,
}
