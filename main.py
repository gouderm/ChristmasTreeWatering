import RPi.GPIO as GPIO
import time
import datetime


def init_gpio(GPIO_tree_sensor, GPIO_tree_ref, 
        GPIO_reservoir_sensor, GPIO_reservoir_ref,
        GPIO_alarm, GPIO_pump):

    GPIO.setup(GPIO_tree_sensor, GPIO.IN)
    GPIO.setup(GPIO_tree_ref, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(GPIO_reservoir_sensor, GPIO.IN)
    GPIO.setup(GPIO_reservoir_ref, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(GPIO_alarm, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GPIO_pump, GPIO.OUT, initial=GPIO.LOW)


def check_water_level(GPIO_sensor, GPIO_ref):
    # returns False if low water level is detected

    GPIO.output(GPIO_ref, GPIO.HIGH)
    time.sleep(0.1) # wait 100ms
    water_level = GPIO.input(GPIO_sensor)
    GPIO.output(GPIO_ref, GPIO.LOW)

    return water_level


def pump_water(GPIO_pump, duration_s):

    GPIO.output(GPIO_pump, GPIO.HIGH)
    time.sleep(duration_s)
    GPIO.output(GPIO_pump, GPIO.LOW)


def check_off_time():
    # return False if current time is in off_time.

    current_time = datetime.datetime.now().time()

    if current_time < datetime.time(07,0,0) 
        return False

    if current_time > datetime.time(21,30,0):
        return False

    return True


def alarm(GPIO_alarm, panic=False):

    if not panic:
        for _ in range(5):
            GPIO.output(GPIO_alarm, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(GPIO_alarm, GPIO.LOW)
            time.sleep(0.8)

    if panic:
        for _ in range(50):
            GPIO.output(GPIO_alarm, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(GPIO_alarm, GPIO.LOW)
            time.sleep(0.1)
            


def water_watchdog(
        GPIO_tree_sensor, GPIO_tree_ref,
        GPIO_reservoir_sensor, GPIO_reservoir_ref,
        GPIO_alarm, GPIO_pump,
        pump_duration=7):

    pump_ctr = 0

    while True:

        # check water level of reservoir
        while not check_water_level(GPIO_reservoir_sensor, GPIO_reservoir_ref):
            if check_off_time():
                alarm(GPIO_reservoir_sensor, GPIO_reservoir_ref, GPIO_alarm)
            time.sleep(10)

        # check water level of tree
        if not check_water_level(GPIO_tree_sensor, GPIO_tree_ref):
            pump_ctr += 1
            if pump_ctr < 3:
                pump_water(GPIO_pump, pump_duration)
            else: # don't activate pump more than 3 consecutive times
                alarm(GPIO_alarm, panic=True)
        else:
            pump_ctr = 0

        time.sleep(20)



if __name__ == "__main__":

    GPIO_tree_sensor = 
    GPIO_tree_ref = 
    GPIO_reservoir_sensor = 
    GPIO_reservoir_ref = 
    GPIO_alarm =
    GPIO_pump = 

    init_gpio(
            GPIO_tree_sensor,
            GPIO_tree_ref, 
            GPIO_reservoir_sensor,
            GPIO_reservoir_ref,
            GPIO_alarm,
            GPIO_pump
        )

    # startup beep
    for _ in range(2):
        GPIO.output(GPIO_alarm, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(GPIO_alarm, GPIO.LOW)
        time.sleep(0.1)

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



