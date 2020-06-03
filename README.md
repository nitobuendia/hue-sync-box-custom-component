# Philips Hue HDMI Play Sync Box
# Custom Component for Home-Assistant
This project is a `Philips Hue Play HDMI Sync Box` custom component for
[Home-Assistant](https://home-assistant.io).


## Installation

### Via HACS

*Coming soon.*

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)


### Manually
1. Copy the files from the `custom_component/hue_sync_box/` folder into the
`custom_component/hue_sync_box/` of your Home-Assistant installation.

### Common Steps
1. Configure the remote following the instructions in `Configuration`.
1. Restart the Home-Assistant instance.

1. If the code was installed and configured properly, you will get a permanent
  notification. See `Notifications` section on the Home-Assistant menu.
1. Go to `Developer Tools` > `Services` and select `hue_sync_box.get_access_token`.
1. Add the detail for the entity id of the Hue Sync Box and call the service.
1. Go to your Philips Hue Play HDMI Sync Box and keep the off button pressed for
  3 seconds until the light blinks green.
1. Within 5 seconds, call again `hue_sync_box.get_access_token`.
    * The notification should confirm that the access token was captured correctly.
    * If not, kindly repeat the steps starting on `hue_sync_box.get_access_token`.

## Configuration

This component is set up as a remote and should be configured in your
`configuration.yaml` as a `remote`.

### Schema

```yaml
remote:
  - platform: hue_sync_box
    name:
    ip_address:
```

### Parameters
* `name`: Name of the remote (e.g. Hue Sync Box).
* `ip_address`: Local IP address of your Philips Hue Play HDMI Sync Box.
  The IP should be static for this solution work permanently.

### Example
```yaml
remote:
  - platform: hue_sync_box
    name: Hue Sync Box
    ip_address: 192.168.1.100
```

## Usage / Services

This component offers the following services:

* `remote.turn_on`: Turns on the Sync Box. Default sync mode is `passthrough`
  which means that it just allows the HDMI to work without syncing. This is
  equivalent to changing sync mode to `passthrough`. To start syncing, you will
  need to change the sync mode to `music`, `video` or `game`.

```yaml
  fields:
    entity_id:
      description: Name(s) of entities to turn on.
      example: "remote.living_room_tv"
```

* `remote.turn_off`: Turns off the Sync Box. This prevents HDMI from passing
  through. If you want HDMI to work but not sync, change sync mode to
  `passthrough` instead. This is equivalent to changing the sync mode to
  `powersave`.

```yaml
  fields:
    entity_id:
      description: Name(s) of entities to turn off.
      example: "remote.living_room_tv"
```

* `remote.toggle`: Turns on or off depending on current status.

```yaml
  fields:
    entity_id:
      description: Name(s) of entities to toggle.
      example: "remote.living_room_tv"
```

* `hue_sync_box.get_access_token`: Gets a new access token for the integration.
  This should only be used and called during the initial set up. See
  `Installation` section for more details.

```yaml
  fields:
    entity_id:
      description: "Name(s) of the entities whose access token to get"
      example: "remote.living_room_tv"
```

* `hue_sync_box.set_brightness`: Sets the brightness of the light during sync
  mode.

```yaml
  fields:
    entity_id:
      description: "Name(s) of the entities to set"
      example: "remote.living_room_tv"
    brightness:
      description: "Brightness (0-200)"
      example: "75"
```

* `hue_sync_box.set_hdmi_input`: Sets the HDMI input for the Sync Box. The
  current version has inputs 1 to 4.

```yaml
  fields:
    entity_id:
      description: "Name(s) of the entities to set"
      example: "remote.living_room_tv"
    hdmi_input:
      description: HDMI input number (1-4)
      example: "1"
```

* `hue_sync_box.set_intensity`: Sets the intensity of a particular sync mode.
  If no `sync_mode` is passed, it will use the current sync mode. However,
  intensity is only supported for active modes like `game`, `music` and `video`
  and not for others like `passthrough` or `powersave`. While intensity
  `Extreme` is the name used on the Hue Sync App, the API uses `Intense`
  instead. As such, both `Extreme` and `Intense` values are accepted and
  equivalent.

```yaml
  fields:
    entity_id:
      description: "Name(s) of the entities to set"
      example: "remote.living_room_tv"
    intensity:
      description: Intensity Level (Subtle, Moderate, High, Extreme)
      example: "Extreme"
    sync_mode:
      description: "Name of the sync mode (Video, Music, Game)"
      example: Game
```

* `hue_sync_box.set_sync_mode`: Sets the sync mode of the Sync box. Active
  syncing modes are `video`, `music` and `game`. The sync mode `passthrough`
  allows HDMI to be used without syncing; while `powersave` switches off the
  Sync Box and prevents HDMI to be used.

```yaml
  fields:
    entity_id:
      description: "Name(s) of the entities to set"
      example: "remote.living_room_tv"
    sync_mode:
      description: Name of the sync mode (Passthrough, Powersave, Video, Music, Game)
      example: "Video"
```

## What Data Can Be Retrieved

In addition to be able to control the Philips Hue Play HDMI Sync Box, the remote
also offers states and attributes useful for your scrips and automations.

### State and Attributes
The state of the remote will show the **hdmi active** state. In other word,
if the sync mode is `game`, `music`, `video` or `passthrough`, the HDMI would be
used and the state will be on. However, if the sync mode is `powersave` the
hdmi active state would be false and the state would be off.

### Attributes per Day
The attributes will contain details about the sync box. In particular:
* `brightness`: Brightness of the lights.
* `hdmi_active`: Whether HDMI input is active.
* `hdmi_source`: HDMI Input selected.
* `inputs`:
  * `input1`: Input 1 name.
  * `input2`: Input 2 name.
  * `input3`: Input 3 name.
  * `input4`: Input 4 name.
* `intensity`: Intensity of current mode.
* `name`: Name of the sync box.
* `sync_active`: Whether syncing is active.
* `sync_mode`: Syncing mode state.

## References
This component has been built using the following resources:
1. [Home-Assistant Community post for this integration](https://community.home-assistant.io/t/custom-component-philips-hue-hdmi-play-sync-box/201622)
1. [HDMI Sync Box API documentation](https://developers.meethue.com/develop/hue-entertainment/hue-hdmi-sync-box-api/)
1. [Hue Sync Box support issue on ebaauw/homebridge-hue](https://github.com/ebaauw/homebridge-hue/issues/552#issuecomment-572256796)
1. [Philips Hue Play HDMI sync post on the Home-Assistant community](https://community.home-assistant.io/t/philips-hue-play-hdmi-sync/137714)


## Sponsoring
If this is helpful, feel free to `Buy Me a Beer`; or check other options on the Github `❤️ Sponsor` link on the top of this page.


<a href="https://www.buymeacoffee.com/nitobuendia" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/arial-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>
