"""Creates class to interact with Sync Box API.

API Documentation: https://developers.meethue.com/develop/hue-entertainment/hue-hdmi-sync-box-api/
"""

import enum
import json
import logging
import requests

from . import const


_LOGGER = logging.getLogger(__name__)


class SyncBoxEndpoints(enum.Enum):
  """Philips Hue Sync Box API endpoints."""
  REGISTRATIONS = 'api/v1/registrations'
  DEVICE_DETAILS = 'api/v1'
  EXECUTION = 'api/v1/execution'


class HueSyncBoxApi(object):
  """Class to interact with Philips Hye Sync Box API.

  Public Methods:
    get_device_details: Gets device details.
    request_access_token: Requests access token from API.
    set_access_token: Sets access token after requesting it.
    set_brightness: Sets brightness of the lights during sync.
    set_hdmi_input: Sets HDMI input.
    set_intensity: Sets intensity of the sync.
    set_sync_mode: Sets the Sync mode.
  """

  def __init__(self, ip_address, access_token=None):
    """Initializes API service.

    Args:
      ip_address: IP of the Sync Box.
      access_token: Access token to interact with API.
    """
    self._ip_address = ip_address
    self._access_token = access_token
    _LOGGER.debug(f'Philips Hue Sync Box API for IP {ip_address} initialized.')

  # Public methods.
  def get_device_details(self):
    """Gets device details.

    Returns:
      Dictionary containing device information.
    """
    response = self._call_api_endpoint(SyncBoxEndpoints.DEVICE_DETAILS)
    return response.json()

  def request_access_token(self, instance_name):
    """Gets access token from API.

    Args:
      instance_name: Name of the instance for which to generate token.

    Returns:
      Access token. None if not found.
    """
    _LOGGER.debug(
        f'Requested Philips Hue Sync Box access token for {instance_name}.')

    payload = {
        'appName': 'hass',
        'instanceName': instance_name,
    }
    response = self._call_api_endpoint(SyncBoxEndpoints.REGISTRATIONS, payload)
    response_json = response.json()

    if response_json.get('code') is not None:
      error_code = response_json.get('code')
      error_message = response_json.get('message')
      _LOGGER.debug(
          f'Unable to retrieve access token. '
          f'Error {error_code}: {error_message}.')
      return None

    access_token = response_json.get('accessToken')
    if access_token:
      _LOGGER.debug(f'Access token found from API.')
      self.set_access_token(access_token)

    return access_token

  def set_access_token(self, access_token):
    """Sets internal access token.

    Args:
      access_token: Access token to interact with API.
    """
    self._access_token = access_token

  def set_brightness(self, brightness):
    """Sets HDMI Sync Box to a certain brightness.

    Args:
      brightness: Brightness of the light during sync.
    """
    brightness = int(brightness)
    if not 0 <= brightness <= 200:
      raise ValueError(
          'Invalid Brightness {}. Expected integer between 0-200.'.format(
              brightness))

    payload = {'brightness': brightness}
    response = self._call_api_endpoint(SyncBoxEndpoints.EXECUTION, payload)
    _LOGGER.debug(f'Response {response.status_code}: {response.text}')

  def set_hdmi_input(self, hdmi_input):
    """Sets HDMI Sync box to a certain HDMI input.

    Args:
      hdmi_input: HDMI input number.
    """
    hdmi_input = str(hdmi_input).lower()
    if hdmi_input not in const.INPUT_VALUES:
      raise ValueError('Invalid HDMI input {}. Expected: {}.'.format(
          hdmi_input, const.INPUT_VALUES))

    payload = {'hdmiSource': f'input{hdmi_input}'}
    response = self._call_api_endpoint(SyncBoxEndpoints.EXECUTION, payload)
    _LOGGER.debug(f'Response {response.status_code}: {response.text}')

  def set_intensity(self, intensity, sync_mode):
    """Sets HDMI Sync Box to a certain intensity mode

    Args:
      sync_mode: Mode of which to set up intensity.
      intensity: Intensity level.
    """
    sync_mode = str(sync_mode).lower()
    if sync_mode not in const.ACTIVE_SYNC_MODES:
      raise ValueError(
          f'Sync mode {sync_mode} does not support intensity. '
          'Change mode first to one that supports intensity: '
          f'{const.ACTIVE_SYNC_MODES}.')

    intensity = str(intensity).lower()
    if intensity == 'extreme':
      intensity = 'intense'
    if intensity not in const.INTENSITY_VALUES:
      raise ValueError('Invalid Intensity {}. Expected: {}.'.format(
          intensity, const.INTENSITY_VALUES))

    payload = {sync_mode: {'intensity': intensity}}
    response = self._call_api_endpoint(SyncBoxEndpoints.EXECUTION, payload)
    _LOGGER.debug(f'Response {response.status_code}: {response.text}')

  def set_sync_mode(self, sync_mode):
    """Sets HDMI Sync Box to a certain sync mode.

    Args:
      sync_mode: Sync mode to which to set up Sync box.
    """
    sync_mode = str(sync_mode).lower()
    if sync_mode not in const.SYNC_MODE_VALUES:
      raise ValueError('Invalid Sync Mode {}. Expected: {}.'.format(
          sync_mode, const.SYNC_MODE_VALUES))

    payload = {'mode': sync_mode}
    response = self._call_api_endpoint(SyncBoxEndpoints.EXECUTION, payload)
    _LOGGER.debug(f'Response {response.status_code}: {response.text}')

  # Helpers.
  def _get_authorization_headers(self):
    """Gets the authorization headers to make API requests.

    Returns:
      Authorization headers to make API request.
    """
    if not self._access_token:
      raise ValueError('Access token has not been enabled.')
    return {'Authorization': 'Bearer ' + self._access_token}

  def _get_api_url(self, api_endpoint):
    """Gets URL for a given endpoint and JSON payload.

    Args:
      api_endpoint: SyncBoxEndpoints to call.

    Returns:
      API URL.
    """
    return 'https://{ip}/{endpoint}'.format(
        ip=self._ip_address,
        endpoint=api_endpoint.value,
    )

  def _call_api_endpoint(self, api_endpoint, payload=None):
    """Makes a call to the Sync Box API endpoint.

    Args:
      api_endpoint: SyncBoxEndpoints to call.
      payload: Payload to send to API call.

    Returns:
      API response in dict format.
    """
    api_url = self._get_api_url(api_endpoint)
    api_headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    if api_endpoint == SyncBoxEndpoints.REGISTRATIONS:
      response = requests.post(api_url, data=json.dumps(payload), verify=False)
    elif api_endpoint == SyncBoxEndpoints.DEVICE_DETAILS:
      api_headers.update(self._get_authorization_headers())
      response = requests.get(api_url, headers=api_headers, verify=False)
    elif api_endpoint == SyncBoxEndpoints.EXECUTION:
      api_headers.update(self._get_authorization_headers())
      response = requests.put(
          api_url, data=json.dumps(payload), headers=api_headers, verify=False)
    else:
      raise NotImplementedError('Unknown API endpoint.')

    _LOGGER.debug(
        f'Made {response.request.method} request to {response.request.url} '
        f'with body: {response.request.body}')

    return response
