#!/usr/bin/env python
import sys
from twython import Twython
import os
import pygame
import pygame.camera
from pygame.locals import *

# Initializing API keys
CONSUMER_KEY = 'VSCpiXrN57ENtRBBNNVdhH6AM'
CONSUMER_SECRET = 'ycLCXoeQYZ7r1cRNwVAVOR6lAnUBAR5G49ZMRtJCKbsfklcwCM'
ACCESS_KEY = '1397494044196970499-dXq1e7hVBTPF0Wll0SgBxry4qcQCjk'
ACCESS_SECRET = 'JJcxr4EyzHMgCGPpnNJ9bMMcbfu8yasXig2JPB8AXioGm'
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

# Last.fm integration
import re
import webbrowser
import urllib

last_fm_source = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=swishe&api_key=97f2ecff84ac3401c14d220b48c52791&format=json'
last_fm_page = urllib.urlopen(last_fm_source)
last_fm_bytes = last_fm_page.read()
last_fm_data = last_fm_bytes.decode('UTF-8')

playing_artist = re.findall('artist.*?text":"(.*?)"', last_fm_data)

try:
    playing_track = re.findall('nowplaying.*?name":"(.*?)"', last_fm_data)
    playing_album = re.findall('nowplaying.*?text":"(.*?)"', last_fm_data)
    playing = ('Ryan is currently playing: ' + playing_track[0] + ' by ' + playing_artist[0] + ' from ' + playing_album[0] + ' #RyanTweetbot')

except:
    playing_track = re.findall('name":"(.*?)"', last_fm_data)
    playing_album = re.findall('album.*?text":"(.*?)"', last_fm_data)
    playing = ('Ryan\'s last played track: ' + playing_track[0] + ' by ' + playing_artist[0] + ' from ' + playing_album[0] + ' #RyanTweetbot')

# Initializing webcam picture tweet
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1920,1080))
cam.start()
image = cam.get_image()
pygame.image.save(image,'webcam.jpg')
photo = open('webcam.jpg','rb')
response = api.upload_media(media=photo)
api.update_status(status=playing, media_ids=[response['media_id']])


import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

TERMS = 'music'

# GPIO pin number of LED
LED = 25

# Twitter application authentication
CONSUMER_KEY = 'VSCpiXrN57ENtRBBNNVdhH6AM'
CONSUMER_SECRET = 'ycLCXoeQYZ7r1cRNwVAVOR6lAnUBAR5G49ZMRtJCKbsfklcwCM'
ACCESS_KEY = '1397494044196970499-dXq1e7hVBTPF0Wll0SgBxry4qcQCjk'
ACCESS_SECRET = 'JJcxr4EyzHMgCGPpnNJ9bMMcbfu8yasXig2JPB8AXioGm'

class MyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        GPIO.output(LED, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(LED, GPIO.LOW)

        def on_error(self, err, data):
                print err, data

# Setup GPIO as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
stream.statuses.filter(track=TERMS)




# Obtaining CPU temp and tweeting it
cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]
#api.update_status(status='My current CPU temperature is '+temp+' C')