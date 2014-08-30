#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import Adafruit_DHT
import os
import glob
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--key', help="private key of sparkfun data stream", action="store")
args = parser.parse_args()
key = args.key

url = 'http://data.sparkfun.com/input/LQQobq79V0HGGAZNGMVl?private_key={}\&humidity={:+.2f}\&indoortemp={:+.2f}\&outdoortemp={:+.2f}'

# DS18B20 parameters and helper functions
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r') 
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0 
        return temp_c

# DHT11 parameters
sensor = Adafruit_DHT.DHT11
pin = '17'

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, indoortemp = Adafruit_DHT.read_retry(sensor, pin)
outdoortemp = read_temp()

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
if humidity is not None and indoortemp is not None and outdoortemp is not None:
	print("curl "+url.format(key, humidity, indoortemp, outdoortemp))
	#print 'curl http://data.sparkfun.com/input/NJJ67Z6K8xCZJ9VKlAyv?private_key=5ddRwJRo2EIK2MA4E0jX\&humidity={:.2f}\&temp={:+.2f}'.format(humidity,temperature)
	#print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
else:
	print 'echo "AMPELBO ERROR: Failed to get reading."'



