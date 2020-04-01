import paho.mqtt.publish as publish
from picamera import PiCamera
from time import sleep
from gpiozero import MotionSensor
import os
import shutil

path = "/home/pi/cameraTrapPhotos/" #photos directory
access_rights = 0o777

MQTT_SERVER = "localhost" #master Pi IP address
MQTT_PATH = "test" #topic name for MQTT

camera = PiCamera() #activate camera
pir = MotionSensor(4) #activate motion sensor
photoNum = 1

while True:
	print("Photo synchroniztion program: master device running")
	print("Resting the program for a few seconds...")
	sleep(30)
	print("Done resting")
	message = "Motion Not Detected"
	startdetection = False
    
    #Wait until motion is detected to start photo session
	while True:
		if pir.motion_detected == False and startdetection == False:
			startdetection = True
		sleep(1)
		print(pir.motion_detected)
		if startdetection== True:
			if pir.motion_detected == True:
				message = "Take Synced Photo " + str(photoNum)
				break;

	print("Motion has been detected. Taking camera 1 Photo" + str(photoNum))

	#MQTT, send message to all slaves in network to take a photo
	publish.single(MQTT_PATH, message, hostname=MQTT_SERVER)

	path = '/home/pi/cameraTrapPhotos/set' + str(photoNum) +  '/'

    #make a directory for the current session to store photos in 
	try:
		os.mkdir(path,access_rights)
	except OSError:
		print("creation of the directory %s failed" % path)
	else:
		print("successfully created the directory %s" % path)

    #set up photo and camera
	filename = 'set'+str(photoNum)+'_camera1.jpg'
	camera.resolution=(3280,2464)
	camera.shutter_speed = 30000

	#Take Photo
	camera.capture(path+filename)
    
	#End of Photo session
	print("Camera 1 photo number "+ str(photoNum) + " taken")
	photoNum = photoNum + 1
