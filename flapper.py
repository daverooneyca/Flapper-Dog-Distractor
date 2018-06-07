import RPi.GPIO as GPIO
from ServoPi import Servo
import time

GPIO.setmode(GPIO.BOARD)

# Set up the GPIO pins to be pull-down so that they are triggered when 
# current from the corresponding RF receiver goes through
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

flap_toggling = False

def button_pressed(something):
    if flap_toggling:
        return

    toggle_flap()

def toggle_flap():
    flap_toggling = True
    
    servo = Servo(0x40)

    # set the servo minimum and maximum limits in milliseconds
    # the limits for a servo are typically between 1ms and 2ms.

    servo.set_low_limit(1.0)
    servo.set_high_limit(2.0)

    # Enable the outputs
    servo.output_enable()

    servo.move(1, 250)
    time.sleep(0.15)
    servo.move(1, 0)

    flap_toggling = False

if __name__ == "__main__":
    # Add event detection to GPIO pins
    GPIO.add_event_detect(16, GPIO.RISING, button_pressed, bouncetime=100)

    try:
        print "Press <Control-C> to quit"

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print "Done!"

    finally:
        GPIO.cleanup()
