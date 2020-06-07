"""
Richard Cheng

Brief: This code is modified off of Adafruit's code bmp3xx_simpletest.py

This code requires Python 3 and BMP3xx series sensor from Adafruit.

Sensor is set to use I2C but if you need SPI, comment out I2C and uncomment SPI.

For more info see readme.
"""

import time
import board
import busio
import adafruit_bmp3xx

import requests

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# SPI setup
# from digitalio import DigitalInOut, Direction
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# cs = DigitalInOut(board.D5)
# bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)

def c_to_f(c_temp):
# convert temp from Celsius to Fahrenheit.
    return((c_temp * (9/5)) + 32)

def m_to_ft(meter):
# convert meter to feet.
    return(meter * 3.28084)

def get():
# send a get request to see if Smashing Dashboard is up.
    try:
        response = requests.get("http://localhost:3030")
    except requests.exceptions.ConnectionError as err:
        print('Connection error, Smashing Dashboard does not appear to be up!!!')
        return False
    return True

def post_data(url, data, connected):
# send a post request to Smashing Dashboard at the url with the json data.
    if connected:
        try:
            return requests.post(url, json = data)
        except requests.exceptions.Timeout:
            print('tbd')
        except requests.exceptions.RequestException as e:
            print('tbd')

#configuration stuff.
bmp.sea_level_pressure = 1010.1597 #set this for your area! This is in hPa, you can use data from Weather Underground but that requires conversion as they use inch of mercury.
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

refresh_rate_sec = 3

my_url = "http://localhost:3030/widgets/welcome"
hello_data = { "auth_token": "YOUR_AUTH_TOKEN", "text": "Hello Richard!"}

#temp_url = "http://localhost:3030/widgets/temp"
another_url = "http://localhost:3030/widgets/temp"

print('Verifying if Smashing Dashboard temp_dashboard is up..')
connected = get()

count = 0
while True:
    print("Time %s" % time.strftime("%H:%M:%S"))
    data = { "auth_token": "YOUR_AUTH_TOKEN", "text": "Time %s" % time.strftime("%H:%M:%S")}
    response = post_data(my_url, data, connected)
    f_temp = c_to_f(bmp.temperature)
    print("Pressure: %6.2f  Temperature: %5.2f F   %5.2f C" % (bmp.pressure, f_temp, bmp.temperature))
    tempData = {"auth_token": "YOUR_AUTH_TOKEN", "points": [{"x": time.strftime("%H:%M:%S"), "y": "%5.2f" % f_temp}]}
    tempData2 = {"auth_token": "YOUR_AUTH_TOKEN", "value": "%5.2f" % f_temp}

    #response = post_data(temp_url, tempData, connected)
    response = post_data(another_url, tempData2, connected)
    print("Altitude: %4.2f meters  %4.2f feet" % (bmp.altitude, m_to_ft(bmp.altitude)))
    time.sleep(refresh_rate_sec)

