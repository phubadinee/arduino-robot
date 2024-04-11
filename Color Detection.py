import sensor, image, lcd, time, math
from fpioa_manager import fm
from machine import UART

lcd.init()
lcd.rotation(2)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
#sensor.set_hmirror(1)
sensor.run(1)
sensor.skip_frames(30)

fm.register(30,fm.fpioa.UART1_TX)
fm.register(32,fm.fpioa.UART1_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)


Error = 0

#pos1
lineER = [64, 128, 192, 256]
zone_L4 = [ pos for pos in range(0,64) ]
zone_L2 = [ pos for pos in range(64,128) ]
zone_M0 = [ pos for pos in range(128,192) ]
zone_R2 = [ pos for pos in range(192,256) ]
zone_R4 = [ pos for pos in range(256,320) ]




yellow_threshold   = (100, 0, -128, 127, 19, 127)

while True:
    img = sensor.snapshot()
    blobs = img.find_blobs([yellow_threshold],area_threshold=40, pixels_threshold=20)

    #ERROR LINE
    for i in lineER:
        img.draw_line(i,0,i,320,color=(255,255,255),thickness=2)

    if blobs:
        for b in blobs:
            tmp = img.draw_rectangle(b[0:4],thickness=2,color=(255,0,0))
            tmp = img.draw_cross(b[5], b[6],thickness=4,color=(0,255,0),size=8)
            c = img.get_pixel(b[5], b[6])

            pos_x, pos_y = b[5], b[6]

            #Detect line Normal 1
            pos_middle = lcd.width()/2
            if pos_x < pos_middle:
                lane = 'left <=='
            elif pos_x > pos_middle:
                lane = 'right ==>'
            print("x:"+str(pos_x),", y:"+str(pos_y),lane)


            #Detect line PID 1
            if pos_x in zone_L4:
                Error = -4
            elif pos_x in zone_L2:
                Error = -2
            elif pos_x in zone_M0:
                Error = 0
            elif pos_x in zone_R2:
                Error = 2
            elif pos_x in zone_R4:
                Error = 4

            uart_A.write(str(Error))
            time.sleep(0.1)
            print("x:"+str(pos_x),", y:"+str(pos_y),lane,"Error:",Error)

    lcd.display(img)
