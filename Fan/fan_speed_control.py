from gpiozero import PWMLED
from time import sleep

# Configuration
FAN_PIN = 14		# BCM pin used to drive PWM fan
WAIT_TIME = 2		# [s] Time to wait between each refresh
PWM_FREQ = 25		# [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 42 		# under this temp value fan is switched to the FAN_OFF speed
MAX_TEMP = 68 		# over this temp value fan is switched to the FAN_MAX speed
FAN_LOW = 11 		# lower side of the fan speed range during cooling
FAN_HIGH = 99 		# higher side of the fan speed range during cooling
FAN_OFF = 10 		# fan speed to set if the detected temp is below MIN_TEMP 
FAN_MAX = 100 		# fan speed to set if the detected temp is above MAX_TEMP 

# Function to get the CPU temperature
def getCPUTemp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        return float(file.read()) / 1000

def setFanSpeed(speed):
		fan.value = speed/100  # divide by 100 to get values from 0 to 1
		return()

# Calculate and set the fan speed
def calcFanSpeed():
	temp = float(getCPUTemp())
	# print("cpu temp: {}".format(temp)) # Uncomment for testing
      
	# Turn off the fan if temperature is below MIN_TEMP
	if temp < MIN_TEMP:
		setFanSpeed(FAN_OFF)
		# print("Fan OFF") # Uncomment for testing
	# Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
	elif temp > MAX_TEMP:
		setFanSpeed(FAN_MAX)
		# print("Fan MAX") # Uncomment for testing
	# Caculate dynamic fan speed
	else:
		step = (FAN_HIGH - FAN_LOW)/(MAX_TEMP - MIN_TEMP)
		temp -= MIN_TEMP
		setFanSpeed(FAN_LOW + ( round(temp) * step ))
		# print(FAN_LOW + ( round(temp) * step )) # Uncomment for testing
	return ()

try:
    fan = PWMLED(pin=FAN_PIN, frequency=PWM_FREQ) # Create a PWMLED object for the fan
    setFanSpeed(FAN_OFF) # initially set fan speed to the FAN_OFF value
    while True:
        calcFanSpeed() # Call the function that calculates the target fan speed
        sleep(WAIT_TIME) # wait for WAIT_TIME seconds before recalculate

except KeyboardInterrupt:
    # When Ctrl+C is caught, set fan speed to high
    setFanSpeed(FAN_HIGH)

finally:
    fan.off() # Ensure the fan is turned off when exiting the program
