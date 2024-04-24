import os
from argparse import ArgumentParser

from PIL import Image

from .client import EInkMQTTClient, MQTTCredentials, EInkPanelConfig
from .graphics import resize_to_inkplate10_size, convert_to_raw_1bpp, convert_to_raw_4bpp


def display_image(args):
    client = EInkMQTTClient(broker_url=args.mqtt_url)
    client.connect()

    image = Image.open(args.image_path)
    image = resize_to_inkplate10_size(image)
    payload = convert_to_raw_1bpp(image) if args.mode == "1bpp" else convert_to_raw_4bpp(image)

    client.display_image(panel_id=args.panel_id, image=payload, mode=args.mode)


def update_config(args):
    client = EInkMQTTClient(broker_url=args.mqtt_url)
    client.connect()

    if not any([args.new_wifi_ssid, args.new_wifi_password, args.new_broker_url, args.new_panel_id, args.new_waveform]):
        print("No new configuration options provided, nothing to update.")
        exit(1)

    config = EInkPanelConfig()
    if args.new_wifi_ssid or args.new_wifi_password:
        if not args.new_wifi_ssid or not args.new_wifi_password:
            print("Both --new-wifi-ssid and --new-wifi-password must be provided to update WiFi configuration.")
            exit(1)

        config.wifi = EInkPanelConfig.WifiConfig(ssid=args.new_wifi_ssid, password=args.new_wifi_password)

    if args.new_broker_url:
        config.mqtt = EInkPanelConfig.MQTTConfig(broker_url=args.new_broker_url)

    if args.new_panel_id or args.new_waveform:
        config.panel = EInkPanelConfig.PanelConfig()
        if args.new_panel_id:
            config.panel.panel_id = args.new_panel_id
        if args.new_waveform:
            config.panel.waveform = args.new_waveform

    client.update_config(panel_id=args.panel_id, config=config)


def reboot(args):
    client = EInkMQTTClient(broker_url=args.mqtt_url)
    client.connect()
    client.reboot(panel_id=args.panel_id)


def ota_update(args):
    client = EInkMQTTClient(broker_url=args.mqtt_url)
    client.connect()
    client.ota_update(panel_id=args.panel_id, ota_url=args.ota_url)


def request_display_data(args):
    client = EInkMQTTClient(broker_url=args.mqtt_url)
    client.connect()
    client.request_display_data(panel_id=args.panel_id)


def main():
    main_parser = ArgumentParser(prog="vsb-eink-cli")
    main_parser.add_argument("--panel-id", type=str, required=True)
    main_parser.add_argument("--mqtt-url",
                             type=str,
                             default=os.environ.get("MQTT_URL", "mqtt://localhost:1883"),
                             help="MQTT broker URL, defaults to MQTT_URL environment variable or mqtt://localhost:1883")

    command_subparser = main_parser.add_subparsers(dest="command")
    command_subparser.required = True

    display_image_parser = command_subparser.add_parser("display")
    display_image_parser.add_argument("--mode", choices=["1bpp", "4bpp"], default="1bpp",
                                      help="bit depth to convert to")
    display_image_parser.add_argument("image_path", type=str, help="path to an image file")
    display_image_parser.set_defaults(func=display_image)

    update_config_parser = command_subparser.add_parser("update-config")
    update_config_parser.add_argument("--new-wifi-ssid", type=str)
    update_config_parser.add_argument("--new-wifi-password", type=str)
    update_config_parser.add_argument("--new-broker-url", type=str)
    update_config_parser.add_argument("--new-panel-id", type=str)
    update_config_parser.add_argument("--new-waveform", type=int)
    update_config_parser.set_defaults(func=update_config)

    reboot_parser = command_subparser.add_parser("reboot")
    reboot_parser.set_defaults(func=reboot)

    ota_update_parser = command_subparser.add_parser("ota")
    ota_update_parser.add_argument("ota_url", type=str, help="URL of a signed firmware binary")
    ota_update_parser.set_defaults(func=ota_update)

    request_display_data_parser = command_subparser.add_parser("request-display")
    request_display_data_parser.set_defaults(func=request_display_data)

    args = main_parser.parse_args()

    args.func(args)
