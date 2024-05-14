from st7735 import TFT,TFTColor
from machine import SoftSPI,Pin
spi = SoftSPI(baudrate=600000000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(5), miso=Pin(13))#SCL,SDA，mosi无用，任意指定即可
tft = TFT(spi, 3, 4, 2)#DC,RES,CS
tft.initg()#按RGB中的g重置屏幕
tft.rgb(True)
tft.fill(TFT.BLACK)
tft.invertcolor(True)#反转屏幕颜色，负片，反色
f=open('a4.bmp', 'rb')
if f.read(2) == b'BM':  #header
    dummy = f.read(8) #file size(4), creator bytes(4)
    offset = int.from_bytes(f.read(4), 'little')
    hdrsize = int.from_bytes(f.read(4), 'little')
    width = int.from_bytes(f.read(4), 'little')
    height = int.from_bytes(f.read(4), 'little')
    if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
        depth = int.from_bytes(f.read(2), 'little')
        if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
            print("Image size:", width, "x", height)
            rowsize = (width * 3 + 3) & ~3
            if height < 0:
                height = -height
                flip = False
            else:
                flip = True
            w, h = width, height
            if w > 80: w = 80
            if h > 160: h = 160
            tft._setwindowloc((26,1),(w - 1 + 26,h - 1 + 1))#w方向移动26，h方向移动1
            for row in range(h):
                if flip:
                    pos = offset + (height - 1 - row) * rowsize
                else:
                    pos = offset + row * rowsize
                if f.tell() != pos:
                    dummy = f.seek(pos)
                for col in range(w):
                    bgr = f.read(3)
                    tft._pushcolor(TFTColor(bgr[0],bgr[1],bgr[2]))#bgr颜色顺序，红蓝反转
spi.deinit()

