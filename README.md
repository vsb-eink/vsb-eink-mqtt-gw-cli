# VŠB-EInk - MQTT CLI

Trivial CLI wrapper around the VŠB E-Ink MQTT Panel API. It is intended to be used as a simple way to send messages to the E-Ink displays without having to craft MQTT messages by hand or without having to rely on the [vsb-eink-services](https://github.com/vsb-eink/vsb-eink-services).

## Installation

The easiest way to install the CLI is to install it via pipx:

```bash
pipx install git+https://github.com/vsb-eink/vsb-eink-mqtt-gw-cli.git
```

## Usage
The CLI tool is invoked with the command `vsb-eink-cli`. It supports several sub-commands, which are detailed below.

### Common Arguments
* `--help`: Show help message and exit.
* `--panel-id` (required): Identifier of the e-ink panel to operate on.
* `--mqtt-url`: URL of the MQTT broker. Defaults to the value of the `MQTT_URL` environment variable or mqtt://localhost:1883 if not set.

### Sub-commands

#### display
Display an image on an e-ink panel.

* `--mode`: Specifies the bit depth conversion (either "1bpp" or "4bpp"). Default is "1bpp".
* `image_path`: Path to the image file to display.

#### update-config
Update the configuration of an e-ink panel.

* `--new-wifi-ssid`: New WiFi SSID for the panel.
* `--new-wifi-password`: New WiFi password.
* `--new-broker-url`: New MQTT broker URL.
* `--new-panel-id`: New identifier for the panel.
* `--new-waveform`: New waveform setting for the panel.

#### reboot
Reboot the specified e-ink panel.

#### ota
Perform an OTA (Over-The-Air) update on the specified e-ink panel.

* `ota_url`: URL of the signed firmware binary to use for the update.

#### request-display
Request the current display data from the specified e-ink panel.

Examples
Here are some examples of how to use the CLI tool:

```bash
# Display an image on a panel
vsb-eink-cli --panel-id panel123 display --mode 4bpp /path/to/image.png

# Update the WiFi configuration of a panel
vsb-eink-cli --panel-id panel123 update-config --new-wifi-ssid MySSID --new-wifi-password MyPassword

# Reboot a panel
vsb-eink-cli --panel-id panel123 reboot

# Perform an OTA update
vsb-eink-cli --panel-id panel123 ota http://example.com/firmware.bin
```
