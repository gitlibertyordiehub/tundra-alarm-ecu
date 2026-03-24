#!/usr/bin/env python3

import os
import time
import signal
import logging
import RPi.GPIO as GPIO

LOG_DIR = "/home/pizero2w/tundra-alarm-ecu/logs"
LOG_FILE = os.path.join(LOG_DIR, "alarm_core.log")
PLAY_PIN = 17

running = True


def handle_signal(signum, frame):
    global running
    running = False


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logging.info("alarm_core starting")


def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PLAY_PIN, GPIO.OUT, initial=GPIO.HIGH)


def cleanup():
    try:
        GPIO.cleanup()
    except Exception:
        pass
    logging.info("alarm_core stopped cleanly")


def main():
    global running

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    setup_logging()
    setup_gpio()

    logging.info("alarm_core heartbeat loop started")

    while running:
        logging.info("alarm_core alive")
        time.sleep(30)

    cleanup()


if __name__ == "__main__":
    main()
