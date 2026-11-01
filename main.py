import framebuf
import utime
import network
import requests
import random
import images
from display import EPD_2in13_V3


### globals ###
epd = EPD_2in13_V3(landscape=True)
wlan = network.WLAN(network.STA_IF)


def draw_image(imgdata: list[int], x, y, w, h):
    fb = framebuf.FrameBuffer(bytearray(imgdata), w, h, framebuf.MONO_HLSB)
    epd.blit(fb, x, y)


def display_line(text: str, size: int = 3):
    print('Display: %s' % text)
    epd.fill(0xff)
    epd.large_text(text, 20, 20, size, 0x00)
    epd.display(epd.buffer)


def connect() -> str:
    ssid = 'Gunby-Modem'
    password = 'bowiedog'
    if wlan.isconnected():
        return wlan.ifconfig()[0]

    display_line("Wifi...")

    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        utime.sleep(1)
    try:
        print('Trying HTTP request')
        requests.get('http://crafty.local:8080/alive.txt', timeout=0.5)
        ip = wlan.ifconfig()[0]
    except Exception as e:
        display_line('Err: %s' % str(e))
        return None

    display_line(ip)
    return ip


def get_sensor_state(sensor: str) -> str:
    tok = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyNWRkZDgzMzd" +
           "lYzA0M2ZhODdiZDE3ODViN2JmMTdjMiIsImlhdCI6MTc5MzM3NjE1MiwiZXh" +
           "wIjoyMTA4NzM2MTUyfQ.iwV142R2HtLuV5914JzMH3Dg4Ey7x0-vSbqe9gqsZr0")
    req = requests.get('http://homeassistant.local/api/states/%s' % sensor,
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer %s' % tok
                        })
    data = req.json()
    return data['state']


def get_solar_power() -> float:
    state = get_sensor_state('sensor.solar_power')
    print('solar: %d' % float(state))
    return float(state)


def sun_above_horizon() -> bool:
    return get_sensor_state('sun.sun') == 'above_horizon'


def show_power(power: int):
    try:
        epd.fill(0xff)
        draw_image(images.sun, 0, 18, images.sun_w, images.sun_h)

        left_margin = 100
        top = 25
        left = left_margin
        for digit in list(str(power)):
            draw_image(images.digits[int(digit)], left, top, images.digits_w, images.digits_h)
            left += images.digits_w

        top += images.digits_h
        left = left_margin
        draw_image(images.watts, left + 3, top, images.watts_w, images.watts_h)

        epd.display(epd.buffer)
    except Exception as e:
        print("Exception", e)
        display_line("Err: %s" % str(e))


def show_night():
    epd.fill(0xff)
    left = 0 + random.randint(0, 153)
    draw_image(images.moon, left, 18, images.moon_w, images.moon_h)
    epd.display(epd.buffer)


if __name__=='__main__':

    epd.init()
    display_line("Init")
    night_display = False

    while True:
        try:
            connect()
            if sun_above_horizon():
                if night_display:
                    epd.init()
                    night_display = False
                power = int(get_solar_power())
                if power is None:
                    continue

                show_power(power)

                epd.sleep()
                epd.delay_ms(300 * 1000)
                epd.init()
            else:
                if not night_display:
                    night_display = True
                    show_night()
                    epd.sleep()
                epd.delay_ms(300 * 1000)

        except Exception as e:
            print("Exception", e)
            epd.init()
            display_line("Err: %s" % str(e))
