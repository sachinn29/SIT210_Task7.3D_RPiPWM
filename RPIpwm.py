import RPi.GPIO as GPIO
import time

# Set the GPIO mode to use Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the Trigger, Echo, and Buzzer
TRIGGER_PIN = 17
ECHO_PIN = 18
BUZZER_PIN = 2

# Set up the GPIO pins as inputs or outputs
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize the Buzzer PWM (Pulse Width Modulation) controller
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)  # Frequency = 1000 Hz
buzzer_pwm.start(0)  # Start with a 0% duty cycle

# Define a function to measure distance using the ultrasonic sensor
def measure_distance():
    # Trigger the HC-SR04 ultrasonic sensor
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    # Record the start time when the ultrasonic pulse is sent
    while GPIO.input(ECHO_PIN) == False:
        start_time = time.time()

    # Record the finish time when the echo is received
    while GPIO.input(ECHO_PIN) == True:
        finish_time = time.time()

    # Calculate the distance based on the time difference and the speed of sound
    total_time = finish_time - start_time
    distance = (total_time * 34300) / 2  # Speed of sound is approximately 34300 cm/s
    return distance

try:
    while True:
        # Get the distance measurement from the ultrasonic sensor
        distance = measure_distance()
        print(distance)  # Print the distance to the terminal for debugging
        
        # Limit the maximum distance reading to 30 cm
        if distance > 30:
            distance = 30
            
        if distance < 0:
            distance = 0

        # Convert the distance to a ratio between 0 and 100
        distance_ratio = (distance / 30) * 100
        
        # Adjust the PWM duty cycle for the buzzer based on the distance ratio
        buzzer_pwm.ChangeDutyCycle(distance_ratio)
        
        # Delay for a short time before taking the next distance reading
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up the GPIO settings when the program is interrupted by the user
    GPIO.cleanup()
