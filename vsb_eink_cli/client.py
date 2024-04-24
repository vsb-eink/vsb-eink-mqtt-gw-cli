from dataclasses import dataclass, field, asdict
from urllib.parse import urlparse

from paho.mqtt.client import Client as MQTTClient

from .utils import to_json


class EInkColorMode:
    ONE_BIT = "1bpp"
    FOUR_BIT = "4bpp"


@dataclass
class EInkPanelConfig:
    @dataclass
    class PanelConfig:
        panel_id: str = field(default=None)
        waveform: int = field(default=None)

    @dataclass
    class WifiConfig:
        ssid: str
        password: str

    @dataclass
    class MQTTConfig:
        broker_url: str

    panel: PanelConfig = field(default=None)
    wifi: WifiConfig = field(default=None)
    mqtt: MQTTConfig = field(default=None)


@dataclass
class MQTTCredentials:
    username: str
    password: str


class EInkMQTTClient:
    def __init__(self, broker_url: str, topic_prefix: str = "vsb-eink"):
        parsed_url = urlparse(broker_url)
        self._host = parsed_url.hostname
        self._port = parsed_url.port
        self._topic_prefix = topic_prefix

        if parsed_url.username and parsed_url.password:
            self._credentials = MQTTCredentials(username=parsed_url.username, password=parsed_url.password)
        else:
            self._credentials = None

        self.mqtt_client = MQTTClient()

    def connect(self):
        if self._credentials:
            self.mqtt_client.username_pw_set(self._credentials.username, self._credentials.password)
        self.mqtt_client.connect(host=self._host, port=self._port)
        self.mqtt_client.loop_start()

    def display_image(self, panel_id: str, image: bytes, mode: EInkColorMode):
        topic = f"{self._topic_prefix}/{panel_id}/display/raw_{mode}/set"
        self.mqtt_client.publish(topic, payload=image).wait_for_publish()

    def update_config(self, panel_id: str, config: EInkPanelConfig):
        topic = f"{self._topic_prefix}/{panel_id}/config/set"
        self.mqtt_client.publish(topic, payload=to_json(config)).wait_for_publish()

    def reboot(self, panel_id: str):
        topic = f"{self._topic_prefix}/{panel_id}/reboot/set"
        self.mqtt_client.publish(topic).wait_for_publish()

    def ota_update(self, panel_id: str, ota_url: str):
        topic = f"{self._topic_prefix}/{panel_id}/firmware/update/set"
        self.mqtt_client.publish(topic, payload=ota_url).wait_for_publish()

    def request_display_data(self, panel_id: str):
        topic = f"{self._topic_prefix}/{panel_id}/display/get"
        self.mqtt_client.publish(topic).wait_for_publish()

