#!/usr/bin/env python3
import json
import os
import subprocess
import sys

MQTT_HOST = os.environ.get("MQTT_HOST", "127.0.0.1")
MQTT_PORT = os.environ.get("MQTT_PORT", "1883")
MQTT_USER = os.environ.get("MQTT_USER", "")
MQTT_PASS = os.environ.get("MQTT_PASS")
if not MQTT_PASS:
    raise RuntimeError("MQTT_PASS is not set in the environment")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "truck/gps/state")

last_lat = None
last_lon = None
last_alt = None

def publish(payload: dict) -> None:
    msg = json.dumps(payload, separators=(",", ":"))
    subprocess.run(
        [
            "mosquitto_pub",
            "-h", MQTT_HOST,
            "-p", MQTT_PORT,
            "-u", MQTT_USER,
            "-P", MQTT_PASS,
            "-t", MQTT_TOPIC,
            "-r",
            "-m", msg,
        ],
        check=True,
    )

def main() -> None:
    global last_lat, last_lon, last_alt

    proc = subprocess.Popen(
        ["gpspipe", "-w"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )

    if proc.stdout is None:
        sys.exit("gpspipe stdout unavailable")

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue

        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        if obj.get("class") != "TPV":
            continue

        mode = int(obj.get("mode", 0) or 0)

        if "lat" in obj and "lon" in obj:
            last_lat = obj["lat"]
            last_lon = obj["lon"]

        if "alt" in obj:
            last_alt = obj["alt"]

        if last_lat is None or last_lon is None:
            continue

        payload = {
            "lat": last_lat,
            "lon": last_lon,
            "speed": obj.get("speed", 0),
            "alt": last_alt,
            "mode": mode,
        }

        publish(payload)

if __name__ == "__main__":
    main()
