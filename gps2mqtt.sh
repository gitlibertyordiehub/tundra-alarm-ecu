#!/bin/bash
set -e

MQTT_HOST="192.168.68.22"
MQTT_TOPIC="truck/gps/raw"

gpspipe -w | mosquitto_pub -h "$MQTT_HOST" -t "$MQTT_TOPIC" -l
