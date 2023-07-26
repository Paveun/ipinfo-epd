
#!/usr/bin/python3
# -*- coding:utf-8 -*-

import epaper
import time
from PIL import Image,ImageDraw,ImageFont
import socket
import fcntl
import struct
import os
import urllib.request

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15].encode('utf-8')))[20:24])
    except:
        return 'N/A'

def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname[:15], 'utf-8')))
    return ''.join(['%02x:' % b for b in info[18:24]])[:-1]

def main():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    epd = epaper.epaper('epd2in7').EPD()
    epd.init()
    epd.Clear()
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
#    draw.rectangle((0, 0, 176, 264), fill=255)
    draw.text((10, 10), 'IP eth0: ' + get_ip_address('eth0'), font=font, fill=0)
    draw.text((10, 30), 'IP wlan0: ' + get_ip_address('wlan0'), font=font, fill=0)
    draw.text((10, 50), 'DNS: ' + os.popen('cat /etc/resolv.conf | grep nameserver | cut -d " " -f2').read(), font=font, fill=0)
    draw.text((10, 70), 'Gateway: ' + os.popen('ip route | grep default | cut -d " " -f3').read(), font=font, fill=0)
    draw.text((10, 90), 'Hostname: ' + os.popen('hostname').read(), font=font, fill=0)
    draw.text((10, 110), 'MAC eth0: ' + get_mac_address('eth0'), font=font, fill=0)
    draw.text((10, 130), 'MAC wlan0: ' + get_mac_address('wlan0'), font=font, fill=0)
    draw.text((10, 150), 'External IP: ' + urllib.request.urlopen('https://ident.me').read().decode('utf8'), font=font, fill=0)
    epd.display(epd.getbuffer(image))

if __name__ == '__main__':
    main()
