import RPi.GPIO as GPIO
import time

def PIRSensor():
    pir=17
    sound=20
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(sound,GPIO.OUT)
    while(True):
        temp=GPIO.input(pir)
        if(temp):
            print("No motion detected")
            GPIO.output(sound,GPIO.LOW)
        else:
            print("Motion detected")
            GPIO.output(sound,GPIO.HIGH)
    GPIO.cleanup()
    
PIRSensor()