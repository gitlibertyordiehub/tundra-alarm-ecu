#!/bin/bash
set -e

: "${MQTT_HOST:?Missing MQTT_HOST}"
: "${MQTT_PORT:?Missing MQTT_PORT}"
: "${MQTT_USER:?Missing MQTT_USER}"
: "${MQTT_PASS:?Missing MQTT_PASS}"
: "${MQTT_TOPIC:?Missing MQTT_TOPIC}"

gpspipe -w | mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" -u "$MQTT_USER" -P "$MQTT_PASS" -t "$MQTT_TOPIC" -l
