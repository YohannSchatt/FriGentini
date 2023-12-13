import RPi.GPIO as GPIO

from pn532 import *


def ReadCard () : 
    try : 
        print("Beginning of reading")
        #Init of the sensor
        pn532 = PN532_I2C(debug=False, reset=20, req=16)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        lecture = False
        while not lecture:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            #print('Found card with UID:', [hex(i) for i in uid])
            lecture = True
    except Exception as e: 
        print("Exception")
    finally : 
        print("fin")
        GPIO.cleanup()
        return uid