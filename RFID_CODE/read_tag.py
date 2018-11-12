#!/usr/bin/env python3

#Import from AWS-IoT Library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

#To create delay
import time

#To get date and time
from datetime import date, datetime


import RPi.GPIO as GPIO
import MFRC522
import signal
import time
continue_reading = True

myclient = AWSIoTMQTTClient("harry")
myclient.configureEndpoint("abqtcn9goqnda-ats.iot.us-east-1.amazonaws.com", 8883)
myclient.configureCredentials("/home/pi/Desktop/final-project/aws-iot/AmazonRootCA1.pem", "/home/pi/Desktop/final-project/aws-iot/a270df8f44-private.pem.key", "/home/pi/Desktop/final-project/aws-iot/a270df8f44-certificate.pem.crt")
myclient.configureAutoReconnectBackoffTime(1, 32, 20)
myclient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myclient.configureDrainingFrequency(2)  # Draining: 2 Hz
myclient.configureConnectDisconnectTimeout(10)  # 10 sec
myclient.configureMQTTOperationTimeout(5)  # 5 sec

def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
TAGRead = MFRC522.MFRC522()

print("Automated Bike Docking Station")
print("Press Ctrl + C to End program")

myclient.connect()
while continue_reading:
    # Scan for cards   
    time.sleep(1)
    (status,TagType) = TAGRead.MFRC522_Request(TAGRead.PICC_REQIDL)

    # If a card is found
    if status == TAGRead.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = TAGRead.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == TAGRead.MI_OK:
        rfid_value = "Card read uid: " + str(uid[0])
        myclient.publish("harry_policy",rfid_value, 0)
        print("MQTT Client connection success!")
        # Print UID
        print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))

