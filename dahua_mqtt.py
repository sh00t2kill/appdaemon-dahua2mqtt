import appdaemon.plugins.hass.hassapi as hass
import datetime
import requests
from requests.exceptions import ConnectionError

class DahuaMQTT(hass.Hass):

    def initialize(self):

        for camera in self.args["cameras"]:
            self.poll_camera(camera)

    def on_receive(self, data, camera):
        topic = camera["topic"]
        d = data.decode()
        for line in d.split("\r\n"):
            if line.startswith("Code="):
                event_data = line.split(";")
                for event in event_data:
                    chunk = event.split("=")
                    if chunk[0] == "Code":
                        event_name = chunk[1]
                    elif chunk[0] == "action":
                        action_name = chunk[1]
                    elif chunk[0] == "index":
                        camera_id = chunk[1]

                if camera_id:
                    mqtt_topic = f"{topic}{camera_id}/{event_name}"
                else:
                    mqtt_topic = f"{topic}{event_name}"
                self.log(f"Publishing {action_name} to {mqtt_topic}")
                self.call_service("mqtt/publish", topic=mqtt_topic, payload=action_name, retain=camera["retain"])

    def poll(self, url, camera):
        r = requests.get(url, stream=True, timeout=120)
        self.log("Connected to " + camera["host"])
        try:
            for event in r.iter_lines():
                self.on_receive(event, camera)
        except ConnectionError:
            self.log("Timeout reached connecting to " + camera["host"] + " :: Reconnecting")
            r.close()
            self.poll(url, camera)


    def poll_camera(self, camera):
        url = "http://{0}:{1}@{2}:{3}/cgi-bin/eventManager.cgi?action=attach&codes=[{4}]"
        url = url.format(camera["user"], camera["pass"], camera["host"], camera["port"], camera["events"])

        self.poll(url, camera)
