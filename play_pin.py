#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO

PLAY_PIN = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PLAY_PIN, GPIO.OUT, initial=GPIO.HIGH)

try:
    GPIO.output(PLAY_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(PLAY_PIN, GPIO.HIGH)
finally:
    GPIO.cleanup()
