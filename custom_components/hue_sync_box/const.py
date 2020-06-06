"""Constants and common variables for Philips Hue Sync Box."""

from homeassistant import const

# Set up.
DOMAIN = 'hue_sync_box'
PLATFORMS = ['remote']
TOKEN_FILE = 'hue-sync-box-token-cache-{}'

# Platform config.
CONF_ENTITY_ID = const.CONF_ENTITY_ID
CONF_IP_ADDRESS = const.CONF_IP_ADDRESS
CONF_NAME = const.CONF_NAME

# Services.
SERVICE_GET_ACCESS_TOKEN = 'get_access_token'
SERVICE_SET_BRIGHTNESS = 'set_brightness'
SERVICE_SET_HDMI_INPUT = 'set_hdmi_input'
SERVICE_SET_INTENSITY = 'set_intensity'
SERVICE_SET_SYNC_MODE = 'set_sync_mode'
SERVICE_TOGGLE = const.SERVICE_TOGGLE
SERVICE_TURN_OFF = const.SERVICE_TURN_OFF
SERVICE_TURN_ON = const.SERVICE_TURN_ON
SERVICE_UPDATE = 'update'

# Service attributes.
ATTR_BRIGHTNESS = const.CONF_BRIGHTNESS
ATTR_ENTITY_ID = const.ATTR_ENTITY_ID
ATTR_HDMI_INPUT = 'hdmi_input'
ATTR_INTENSITY = 'intensity'
ATTR_SYNC_MODE = 'sync_mode'

# Default values.
DEFAULT_STR_VALUE = 'undefined'
DEVICE_DEFAULT_NAME = 'Philips Hue Sync Box'

# Accepted API values.
INPUT_VALUES = ('1', '2', '3', '4')
ACTIVE_SYNC_MODES = ('video', 'music', 'game')
DEFAULT_SYNC_MODE = 'passthrough'
SYNC_MODE_VALUES = ('passthrough', 'powersave') + ACTIVE_SYNC_MODES
INTENSITY_VALUES = (
    'subtle', 'moderate', 'high', 'extreme', 'intense')  # Extreme = Intense.
