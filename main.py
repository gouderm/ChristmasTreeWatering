#! /usr/bin/python3

import RPi.GPIO as GPIO
import time
import datetime
import sys
import os
import logging
import telepot
import urllib2

log_format = '%(asctime)s | %(message)s'
TOKEN = "SECRET TELEGRAM TOKEN"

log_file_path = os.path.dirname(os.path.realpath(__file__)) + "/log.txt"
logging.basicConfig(filename=log_file_path, format=log_format, filemode='a')

# logging.basicConfig(stream=sys.stdout, format=log_format)
  
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://google.de',timeout=1)
            return
        except urllib2.URLError:
            pass

def broadcast(msg, bot=bot, chat_ids=ids):
    for id in chat_ids:
        try:
            bot.sendMessage(id, msg)
        except:
            logger.error(f"failed to broadcast")

def init_gpio(GPIO_tree_sensor, GPIO_tree_ref, 
        GPIO_reservoir_sensor, GPIO_reservoir_ref,
        GPIO_alarm, GPIO_pump) -> None:

    logger.debug("initializing GPIO")

    GPIO.setup(GPIO_tree_sensor, GPIO.IN)
    GPIO.setup(GPIO_tree_ref, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(GPIO_reservoir_sensor, GPIO.IN)
    GPIO.setup(GPIO_reservoir_ref, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(GPIO_alarm, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GPIO_pump, GPIO.OUT, initial=GPIO.LOW)


def check_water_level(GPIO_sensor, GPIO_ref) -> bool:
    # returns False if low water level is detected
    logger.debug("check water level: Sensor-Pin {}".format(GPIO_sensor))

    GPIO.output(GPIO_ref, GPIO.HIGH)
    time.sleep(0.1) # wait 100ms
    water_level = GPIO.input(GPIO_sensor)
    GPIO.output(GPIO_ref, GPIO.LOW)

    logger.debug("water level high" if water_level else "water level low")

    return water_level


def pump_water(GPIO_pump, duration_s) -> None:
    logger.debug("pump water")

    GPIO.output(GPIO_pump, GPIO.HIGH)
    time.sleep(duration_s)
    GPIO.output(GPIO_pump, GPIO.LOW)


def check_off_time() -> bool:
    # return False if current time is in off_time.

    current_time = datetime.datetime.now().time()

    if current_time < datetime.time(7,0,0):
        return False

    if current_time > datetime.time(21,30,0):
        return False

    return True


def alarm(GPIO_alarm, panic=False):

    if not panic:
        logger.debug("alarm (no panic)")
        for _ in range(5):
            GPIO.output(GPIO_alarm, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(GPIO_alarm, GPIO.HIGH)
            time.sleep(0.8)

    if panic:
        logger.debug("alarm (panic)")
        for _ in range(50):
            GPIO.output(GPIO_alarm, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(GPIO_alarm, GPIO.HIGH)
            time.sleep(0.1)
            


def water_watchdog(
        GPIO_tree_sensor, GPIO_tree_ref,
        GPIO_reservoir_sensor, GPIO_reservoir_ref,
        GPIO_alarm, GPIO_pump,
        pump_duration=7):

    logger.debug("start water watchdog")

    pump_ctr = 0

    while True:

        # check water level of reservoir
        if not check_water_level(GPIO_reservoir_sensor, GPIO_reservoir_ref):
            broadcast("Waterlevel in Reservoir low!")
            if check_off_time():
                alarm(GPIO_alarm)
            else:
                logger.debug("silent alarm")
            time.sleep(5)

        # check water level of tree
        if not check_water_level(GPIO_tree_sensor, GPIO_tree_ref):
            pump_ctr += 1
            if pump_ctr < 3:
                pump_water(GPIO_pump, pump_duration)
            else: # don't activate pump more than 3 consecutive times
                broadcast("Water in Tree-pot does not change! Tried to pump 3-times.")
                alarm(GPIO_alarm, panic=True)
        else:
            pump_ctr = 0

        time.sleep(20)



if __name__ == "__main__":

    logger.info("waiting for internet connection")
    wait_for_internet_connection()
    logger.info("connected to internet")

    broadcast("ChristmasTree Up and Running!")



    bot = telepot.Bot(TOKEN)
    ids = []

    for msg in bot.getUpdates():
        if (_id := msg.get("message",{}).get("chat",{}).get("id", None)) != None:
            if _id not in ids:
                ids.append(_id)

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO_tree_sensor = 2
        GPIO_tree_ref = 4
        GPIO_reservoir_sensor = 27
        GPIO_reservoir_ref = 17
        GPIO_alarm = 3
        GPIO_pump = 22

        init_gpio(
                GPIO_tree_sensor,
                GPIO_tree_ref, 
                GPIO_reservoir_sensor,
                GPIO_reservoir_ref,
                GPIO_alarm,
                GPIO_pump
            )

        # startup beep
        logger.debug("Startup Beep")
        for _ in range(5):
            GPIO.output(GPIO_alarm, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(GPIO_alarm, GPIO.HIGH)
            time.sleep(0.05)

        time.sleep(2)

        water_watchdog(
                GPIO_tree_sensor,
                GPIO_tree_ref,
                GPIO_reservoir_sensor,
                GPIO_reservoir_ref,
                GPIO_alarm,
                GPIO_pump,
                pump_duration = 7
            )


    finally:

        logger.debug("Terminating")
        GPIO.cleanup()
