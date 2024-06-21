import RPi.GPIO as GPIO
import time 

# BCM Number of LED indicators
leds = [5, 6, 13, 19]
pwms = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for l in leds:
    GPIO.setup(l, GPIO.OUT)
    pwms.append(GPIO.PWM(l, 50))

for p in pwms:
    p.start(0)

try:
    while True:
        for dc in range(0, 101, 5):
            for p in pwms:
                p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            for p in pwms:
                p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass

for p in pwms:
    p.stop()
GPIO.cleanup()
print("BYE")

