from main import check_water_level, init_gpio
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
            if check_water_level(c.GPIO_tree_sensor, c.GPIO_tree_ref):
                GPIO.output(c.GPIO_alarm, GPIO.LOW)
            else:
                GPIO.output(c.GPIO_alarm, GPIO.HIGH)
            time.sleep(0.1)

    finally:
        GPIO.cleanup()
