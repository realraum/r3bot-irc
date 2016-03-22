#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time


class r3mqttpublisher():

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect("mqtt.realraum.at", 1883, 60)

    def send(self, structname, datadict):
        self.client.publish(structname, json.dumps(datadict))


if __name__ == '__main__':
    pub = r3mqttpublisher()
    pub.send("realraum/r3mqtt/demo",
             {"Ts": int(time.time()),
              "aBool": bool(True),
              "aInt": float(42),
              "aFloat": float(2904.0),
              "aString": str("hello world")
              })
