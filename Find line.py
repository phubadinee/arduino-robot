import sensor, image, time, lcd
import math
import utime

from machine import I2C
from fpioa_manager import fm
from Maix import GPIO
from machine import UART
i2c = I2C(I2C.I2C0, freq=100000, scl=27, sda=29)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 160 x 120 pixel
sensor.run(1)
sensor.skip_frames(30)

#def motorControl(speedMotor1,speedMotor2,speedMotor3,speedMotor4):
    #i2c.writeto(0x12,bytes(1))


while(True):

    img = sensor.snapshot()
    #lines = img.find_lines(
        #threshold=1300,
        #theta_margin=25,
        #rho_margin=25
    #)
    #for l in lines:
        #img.draw_line(l.line(),color=(255,0,0),thickness=4)

    i2c.writeto(0x12,bytes(1))
    time.sleep(1)
    lcd.display(img)
