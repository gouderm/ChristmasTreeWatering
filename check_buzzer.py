from main import alarm, init_gpio
import constants as c
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)

        init_gpio(
                c.GPIO_tree_sensor,
                c.GPIO_tree_ref, 
                c.GPIO_reservoir_sensor,
                c.GPIO_reservoir_ref,
                c.GPIO_alarm,
                c.GPIO_pump
            )

        while True:
            alarm(c.GPIO_alarm)
            time.sleep(1)
            alarm(c.GPIO_alarm, True)
            time.sleep(1)

    finally:
        GPIO.cleanup()
