import sensor, image, time,lcd,math
from fpioa_manager import fm
from machine import UART
from Maix import GPIO

print("start script")

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 160 x 120 pixel
sensor.run(1)
sensor.skip_frames(30)
fm.register(28,fm.fpioa.UART1_TX)
fm.register(30,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)


fm.register(13,fm.fpioa.GPIOHS3,force = True)
fm.register(20,fm.fpioa.GPIOHS1,force = True)
fm.register(18,fm.fpioa.GPIOHS2,force = True)
led_1 = GPIO(GPIO.GPIOHS1, GPIO.OUT)
led_2 = GPIO(GPIO.GPIOHS2, GPIO.OUT)
led_3 = GPIO(GPIO.GPIOHS3, GPIO.OUT)





print("start loop...")

Apriltaglist = []

while True:
    img=sensor.snapshot()
    tags = img.find_apriltags() # defaults to TAG36H11 without

    if len(tags) > 0:
        for tag in img.find_apriltags(): # defaults to TAG36H11 without
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

            apriltag = tag.id()

            if apriltag not in Apriltaglist:
                Apriltaglist.append(apriltag)


                for i in range(5):

                    led_1.value(1)
                    time.sleep(0.1)
                    led_1.value(0)
                    time.sleep(0.1)


            print(Apriltaglist)
            img.draw_string(2,2,str(apriltag) , color=(255,255,255), scale=2)
            degress = 180 * tag.rotation() / math.pi

    if len(Apriltaglist) == 5:
        img.draw_string(2,60,'apriltag full!' , color=(255,255,0), scale=1)
        print('Apriltag FUll')
        led_2.value(1)
        time.sleep(2)
        led_2.value(0)


        break
    lcd.display(img)

time.sleep(2)

for i in range(5):
    led_1.value(1)
    led_2.value(1)
    time.sleep(0.1)
    led_1.value(0)
    led_2.value(0)
    time.sleep(0.1)



while True:

    img=sensor.snapshot()
    tags = img.find_apriltags() # defaults to TAG36H11 without
    img.draw_string(2,50,str(Apriltaglist) , color=(255,255,255), scale=1)
    if len(tags) > 0:
        for tag in img.find_apriltags(): # defaults to TAG36H11 without
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

            apriltag = tag.id()


            if apriltag in Apriltaglist:
                index = Apriltaglist.index(apriltag)
                uart_A.write(str(index+1))

                Apriltaglist.remove(apriltag)
                Apriltaglist.insert(index,0)

    else:
        uart_A.write('0')
    lcd.display(img)
