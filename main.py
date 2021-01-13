import mazegenerator

import RPi.GPIO as GPIO

from shiftio import shiftOut

import time

import gpiozero



u=gpiozero.Button(5)

r=gpiozero.Button(6)

d=gpiozero.Button(13)

l=gpiozero.Button(19)





GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.OUT)#data

GPIO.setup(27,GPIO.OUT)#clock



while True:

    if u.is_pressed or d.is_pressed or r.is_pressed or l.is_pressed:



        mazegenerator.createMaze(8,4)

        mazegenerator.run(r,d,l,u)#Pass through the button objects



