#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import requests
import threading


class mThread(threading.Thread):

    def __init__(self,selec):
        super(mThread, self).__init__()
        self._stop_event = threading.Event()
	self.selec = selec

    def run(self):
	while not self._stop_event.isSet():
	    try:
		if self.selec == 1:
		    print "Trigger Relay 1"
		    GPIO.output(5,1)
		    time.sleep(18)
		    GPIO.output(5,0)
		    print "Done Trigger Relay 1"
		    run1 = False
		elif self.selec == 2:
		    print "Trigger Relay 2"
		    GPIO.output(6,1)
		    time.sleep(18)
		    GPIO.output(6,0)
		    print "Done Trigger Relay 2"
		    run2 = False
		elif self.selec == 3:
		    print "Trigger Relay 3"
		    GPIO.output(13,1)
		    time.sleep(18)
		    GPIO.output(13,0)
		    print "Done Trigger Relay 3"
		    run3 = False
		elif self.selec == 4:
		    print "Trigger Relay 4"
		    GPIO.output(19,1)
		    time.sleep(18)
		    GPIO.output(19,0)
		    print "Done Trigger Relay 4"
		    run4 = False
		self._stop_event.set()

	    except:
		print "error inside"
		time.sleep(1.8)
		#GPIO.output(21,0)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


continue_reading = True
# the uid of the last recognized card
lastcarduid = None
# the time a card uid was last seen
lastcardtime = 0.0

# this long after a card has been noticed, it can be noticed again
# This works because the reader generates repeated notifications of the card
# as it is held agains the reader - faster than this interval.
# The timer is restarted every time the reader generates a uid.
# If you sometimes get repeated new card IDs when holding a card against the
# reader, increase this a little bit.
CARDTIMEOUT = 1.0

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

## Welcome message
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)

def gettypename( typecode ):
    typecode &= 0x7F;
    if typecode == 0x00:
        return "MIFARE Ultralight or Ultralight C"
    elif typecode == 0x01:
        return "MIFARE TNP3XXX"
    elif typecode == 0x04:
        return "SAK indicates UID is not complete"
    elif typecode == 0x08:
        return "MIFARE 1KB"
    elif typecode == 0x09:    
        return "MIFARE Mini, 320 bytes"
    elif typecode == 0x10 or typecode == 0x11:
        return "MIFARE Plus"
    elif typecode == 0x18:
        return "MIFARE 4KB"
    elif typecode == 0x20:
        return "PICC compliant with ISO/IEC 14443-4"
    elif typecode == 0x40:
        return "PICC compliant with ISO/IEC 18092 (NFC)"
    return "Unknown type";

#thread1 = threading.Thread(target=relay1)
#thread1.daemon = True

run1 = False
run2 = False
run3 = False
run4 = False

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,rawuid) = MIFAREReader.MFRC522_Anticoll()

    # If we have a good read of the UID, process it
    if status == MIFAREReader.MI_OK:
	uid = "{0[0]:02x}{0[1]:02x}{0[2]:02x}{0[3]:02x}".format(rawuid)
	UID = str(rawuid[0])+str(rawuid[1])+str(rawuid[2])+str(rawuid[3])
	# Print UID
	print UID
	print "Card read UID: "+uid
	newcard = False
	if lastcarduid:
	    if lastcarduid != uid or (lastcardtime and time.clock() - lastcardtime >= CARDTIMEOUT):
		newcard = True
	    else:
		newcard = True
	
	if newcard:
    #            print "New Card read UID: "+uid
	    # String payload = "{\"d\":{\"cardUID\":\"";
	    #  payload += UID_HEX;
	    #  payload += "\",\"cardtype\":\"";
	    #  payload += mfrc522.PICC_GetTypeName(piccType);
	    #  payload += "\"}}"; 
	    rawcardtype = MIFAREReader.MFRC522_SelectTag(rawuid)
	    cardtypename = gettypename( rawcardtype )
	    #print '{ "cardUID": "'+ UID +'","cardtype":"'+cardtypename+'" }'
	    GPIO.output(21,1)
	    GPIO.output(5,0)
	    GPIO.output(6,0)
	    GPIO.output(13,0)
	    GPIO.output(19,0)

	    try:
		time.sleep(0.1)
		GPIO.output(21,0)
		#requests.post('http://pointofsale.ml/api/customer/dine', data = {"uid": UID})
		#r = requests.post('http://pointofsale.ml/api/customer/dine', data = {"uid": UID})
		# print r.text
		if uid == "14548926":
			if run1 == False:
				run1 = True
				t1 = mThread(1)
				t1.start()
			else:
				if t1.isAlive() == False:
					t1 = mThread(1)
					t1.start()
				else:
					print "1 is running"
		elif uid == "64028a26":
			if run2 == False:
				run2 = True
				t2 = mThread(2)
				t2.start()
			else:
				if t2.isAlive() == False:
					t2 = mThread(2)
					t2.start()
				else:
					print "2 is running"
		elif uid == "f675b608":
			if run3 == False:
				run3 = True
				t3 = mThread(3)
				t3.start()
			else:
				if t3.isAlive() == False:
					t3 = mThread(3)
					t3.start()
				else:
					print "3 is running"
		else:
			print "Invalid Card Detected"

	    except RuntimeError:
		print RuntimeError.message
		time.sleep(1.8)
		#GPIO.output(21,0)
		
	# remember the last card uid recognized
	lastcarduid = uid
	# remember when it was seen
	lastcardtime = time.clock()



