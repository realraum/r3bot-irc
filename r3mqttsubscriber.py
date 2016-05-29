#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json


class r3mqttsubscriber():

    def __init__(self, subscriptions='#', on_message=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message if on_message is None else on_message

        self.client.connect('mqtt.realraum.at', 1883, 60)

        self.subscriptions = subscriptions

    def loop_forever(self):
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        content = json.loads(msg.payload)
        print(msg.topic + ": %s (%s)" % (content, type(content)))

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.subscriptions)
        # self.client.subscribe("$SYS/#")


if __name__ == '__main__':
    sub = r3mqttsubscriber(subscriptions='realraum/r3mqtt/demo')
    sub.loop_forever()
