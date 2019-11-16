import paho.mqtt.publish as publish
from picamera import PiCamera
from time import sleep
from gpiozero import MotionSensor
import socket
import datetime

#MQTT_SERVER = "192.168.0.19"
#MQTT_SERVER = "test.mosquitto.org"
MQTT_SERVER = "localhost"
MQTT_PATH = "test"

camera = PiCamera()
pir = MotionSensor(4)
#message = "Hello"

while True:
	print("Sensor resting")
	sleep(10)
	print("Done sleeping")
	message = "Motion Not Detected"
	#index = 0

	while True:
		sleep(1)
		print(pir.motion_detected)
		if pir.motion_detected == True:
			print("If Statement True")
			message = "Motion Detected"
			break;
		#index+=1


	print("Motion has been detected")

	publish.single(MQTT_PATH, message, hostname=MQTT_SERVER)
	print("Sent message: ", message)
	camera.resolution=(3280,2464)
	#camera.framerate=15
	camera.start_preview()
	#sleep(5)
	date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")
	filename = date+ '_camera1.jpg'
	#camera.capture('/home/pi/Desktop/' + date + '.jpg')
	path = '/home/pi/Desktop/cameraTrapPhotos/'
	#camera.capture('/home/pi/Desktop/cameraTrapPhotos/' + date + "_camera1" + '.jpg')
	camera.capture(path+filename)
	#camera.capture('/home/pi/Desktop/test.jpg')
	camera.stop_preview()
	print(datetime.datetime.now())
