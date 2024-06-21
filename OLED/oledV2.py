import time
import board
import busio
import subprocess
import adafruit_ssd1306 as ssd1306
from PIL import Image, ImageDraw, ImageFont

I2C = busio.I2C(board.SCL, board.SDA)
ADDR = 0x3C
RST = None
oled = ssd1306.SSD1306_I2C(128, 32, I2C, addr=ADDR, reset=RST)

# Clear display
oled.fill(0)
oled.show()

width = oled.width
height = oled.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.load_default()

padding = -2 
top = padding
bottom = height - padding
x = 0

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    cmd = "hostname -I | cut -d\' \' -f1" 
    ip = subprocess.check_output(cmd, shell=True)

    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %s%%\", $(NF-2)*100}'"
    cpu = subprocess.check_output(cmd, shell=True)

    cmd = "free -m | awk 'NR==2{printf \"Mem: %.2f/%.2fGB %.2f%%\", $3/1024, $2/1024, $3*100/$2 }'"
    mem = subprocess.check_output(cmd, shell=True)

    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3, $2, $5}'"
    disk = subprocess.check_output(cmd, shell=True)

    cmd = "vcgencmd measure_temp"
    temp = subprocess.check_output(cmd, shell=True)

    draw.text((x, top), "IP: {}".format(ip.decode('utf-8')), font=font, fill=255)
    draw.text((x, top+8), "{}".format(cpu.decode('utf-8')), font=font, fill=255)
    draw.text((x, top+16), "{}".format(mem.decode('utf-8')), font=font, fill=255)
    draw.text((x, top+24), "{}".format(temp.decode('utf-8')), font=font, fill=255)

    oled.image(image)
    #oled.display()
    oled.show()
    time.sleep(3)
























