#!/usr/bin/env python3

import logging
from argparse import ArgumentParser, FileType
from paho.mqtt.client import Client as MQTTClient
from PIL import Image

from .graphics import convert_to_raw_1bpp, convert_to_raw_4bpp, resize_to_inkplate10_size


def on_mqtt_connect(client, userdata, flags, rc):
    pass


def on_mqtt_message(client, userdata, msg):
    pass


def main():
    args_parser = ArgumentParser()
    args_parser.add_argument('input', type=FileType("r+b"), help='path to input file')
    args_parser.add_argument("--host" "-h", type=str, help="mqtt host to connect to", default="localhost")
    args_parser.add_argument("--port", "-p", type=int, help="network port to connect to", default=1883)
    args_parser.add_argument("--mode", choices=["1bpp", "4bpp"], default="1bpp", help="bit depth to convert to")

    panel_select_args = args_parser.add_mutually_exclusive_group(required=True)
    panel_select_args.add_argument("--topic", "-t", type=str, help="mqtt topic to publish to")
    panel_select_args.add_argument("--panel", type=str, help="panel id to send the graphics to")

    args = args_parser.parse_args()

    mqtt = MQTTClient()
    mqtt.on_connect = on_mqtt_connect
    mqtt.on_message = on_mqtt_message

    try:
        mqtt.connect("localhost", 1883)
        mqtt.loop_start()
    except Exception as err:
        logging.error("Failed to connect to MQTT broker")
        logging.error(err)
        exit(1)

    image = Image.open(args.input)
    image = resize_to_inkplate10_size(image)

    if args.mode == "1bpp":
        message_payload = convert_to_raw_1bpp(image)
        topic_payload_name = "raw_1bpp"
    else:
        message_payload = convert_to_raw_4bpp(image)
        topic_payload_name = "raw_4bpp"

    if args.topic:
        message_topic = args.topic
    else:
        message_topic = f"vsb-eink/{args.panel}/display/{topic_payload_name}/set"

    published_message = mqtt.publish(message_topic, payload=message_payload, qos=1)
    published_message.wait_for_publish()


if __name__ == "__main__":
    main()
