#Coding By ARIS KKU ==> P'nest, P'oil

import sensor, image, time, lcd
import math
import utime

from machine import I2C
from fpioa_manager import fm
from Maix import GPIO
from machine import UART
fm.register(13,fm.fpioa.GPIOHS3,force = True)
led = GPIO(GPIO.GPIOHS3, GPIO.OUT)
i2c = I2C(I2C.I2C0, freq=100000, scl=27, sda=29)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

COLOR_THRESHOLDS =[(92, 98, -25, -11, 30, 87)] # Yellow(93, 100, -25, 0, 20, 56)
COLOR_HIGH_LIGHT_THRESHOLDS = [(50, 100, -10, 7, -7, 19)] #Cut Hi-Light

##COLOR_HIGH_LIGHT_THRESHOLDS = [(70, 100, -10, 7, -8, 8)] #Cut Hi-Light
##COLOR_CONE = [(15, 53, 25, 56, 11, 44)] # Red
##COLOR_THRESHOLDS =[(98, 75, -27, -6, 10, 76)] # Yellow
##COLOR_THRESHOLDS =[(95, 99, -27, -12, 69, 91)] # Yellow
##COLOR_HIGH_LIGHT_THRESHOLDS = [(82, 100, -2, 6, 25, -1)] #Cut Hi-Light
##COLOR_CONE = [(15, 71, 17, 52, 27, 50)] # Red
COLOR_CONE = [(17, 84, -1, 36, 23, 62)] #rad

FRAME_SIZE = sensor.QQVGA # Frame size.
FRAME_REGION = 0.75 # Percentage of the image from the bottom (0 - 1.0).
FRAME_WIDE = 1.0 # Percentage of the frame width.

AREA_THRESHOLD = 0 # Raise to filter out false detections.
PIXELS_THRESHOLD = 40 # Raise to filter out false detections.
MAG_THRESHOLD = 4 # Raise to filter out false detections.
MIXING_RATE = 0.9 # Percentage of a new line detection to mix into current steering.
THROTTLE_CUT_OFF_ANGLE = 1.0 # Maximum angular distance from 90 before we cut speed [0.0-90.0).
THROTTLE_CUT_OFF_RATE = 0.5 # How much to cut our speed boost (below) once the above is passed (0.0-1.0].

OPENMV = True
last_error = 0
pidValue = 0
leftSpeed = 0
rightSpeed = 0

lcd.init()
lcd.rotation(1)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_auto_gain(False,200)
sensor.skip_frames(40)
green_threshold = [(86, 94, -22, -13, -11, 5)]
old_cx_normal = None
img = {}
img2 = {}
img3 = {}
line = {}
errors = 0


def laneValue(line, img):
    global old_cx_normal
    cy = img.height() / 2
    cx = (line.rho() - (cy * math.sin(math.radians(line.theta())))) / math.cos(math.radians(line.theta()))
    cx_middle = cx - (img.width() / 2)
    cx_normal = cx_middle / (img.width() / 2)
    if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
    else: old_cx_normal = cx_normal
    return old_cx_normal

def readCam():
    global img
    global img2
    global img3
    img = sensor.snapshot().rotation_corr(0,0,-180)
    img2 = img.copy()
    img3 = img.copy()

def readLane():
    global img
    global line
    readCam()
    img.binary(COLOR_HIGH_LIGHT_THRESHOLDS , zero = True)
    img.histeq()
    line = img.get_regression((COLOR_THRESHOLDS), area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, robust = True)
    lcd.display(img)

def motorControl(speedMotor1,speedMotor2,speedMotor3,speedMotor4):

    i2c.writeto(0x12,bytes([int(speedMotor1+127),int(speedMotor2+127),int(speedMotor3+127),int(speedMotor4+127)]))



Kp = 15
Kd = 3
baseSpeed = 15
timer = 0
counter = 0
r = 1
while True:

    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)
    readCam()
    cone = img2.find_blobs(COLOR_CONE,area_threshold=150,pixels_threshold=150)
    cone2 = img2.find_blobs(green_threshold,area_threshold=300,pixels_threshold=300)
    if cone :
        dist = cone[0].cx() - 40
        if dist == 0 :
            dist = 1
        if dist >= 0 :
            timer = (40-dist)*30
            motorControl(-20,20,20,-20)
            time.sleep_ms(1300)
            motorControl(18,15,15,15)
            time.sleep_ms(3200)
            motorControl(20,-20,-20,20)
            time.sleep_ms(1500)
        else :
            timer = (40+dist)*30
            motorControl(20,-20,-20,20)
            time.sleep_ms(1300)
            motorControl(18,15,15,15)
            time.sleep_ms(3200)
            motorControl(-20,20,20,-20)
            time.sleep_ms(1500)
        img.draw_rectangle(cone[0].x(),cone[0].y(),cone[0].w(),cone[0].h(),thickness=2)
        motorControl(0,0,0,0)

    if cone2 :
        time.sleep_ms(1000)
        x = 1
        if x == 1 and r == 1 :
            counter += 1
            r = 0
        print(counter)
        if counter == 2:
            motorControl(-20,20,20,-20)
            time.sleep_ms(11000)


    else :
      r = 1
      readLane()
      if line and (line.magnitude() >= MAG_THRESHOLD):
        img.draw_line(line.line(), thickness=2,color = (127, 127, 255))
        errors = laneValue(line, img)
        pidValue = (Kp * errors) + (Kd * (errors - last_error))
        last_error = errors
        if pidValue <= (-baseSpeed) : pidValue = (-baseSpeed)
        if pidValue >= baseSpeed : pidValue = baseSpeed
        leftSpeed = (int(baseSpeed + pidValue))
        rightSpeed = (int(baseSpeed - pidValue))
        motorControl(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
      else :
        motorControl(0,0,0,0)



