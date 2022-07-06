#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
import math
from functools import reduce
from motor import *
ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)    

def GPSparser(data):
	gps_data = data.split(b",")
	idx_rmc = data.find(b'GNGGA')
	if data[idx_rmc:idx_rmc+5] == b"GNGGA":
		data = data[idx_rmc:]    
		if checksum(data):
		   # print(data)
			parsed_data = data.split(b",")
			print(parsed_data)
			return parsed_data
		else :
			print ("checksum error")

def checksum(sentence):
	sentence = sentence.strip(b'\n')
	nmeadata, cksum = sentence.split(b'*',1)
	calc_cksum = reduce(operator.xor, (ord(chr(s)) for s in nmeadata), 0)
	print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location(waypoint):

    rotate_way_latitude = waypoint[0]
    rotate_way_longitude = waypoint[1]

    #rotate = atan2(revised[0], revised[1])
    #rotate = rotate * 180 / math.pi
    #print("rotate_angle: ", rotate)

    data = ser.readline()
    result = collections.defaultdict()
    res = GPSparser(data)
    if res == None:
        return(0,0)
    else:
        print(res)
        lat = str (res[2])
        lon = str (res[4])
        if (res == "checksum error"):
            print("")
            print(lat)
        else:
            lat_h = float(lat[2:4])
            lon_h = float(lon[2:5])
            lat_m = float(lat[4:12])
            lon_m = float(lon[5:13])
            print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))
            latitude = lat_h + (lat_m/60)
            longitude = lon_h + (lon_m/60)
            print('latitude: %f longitude: %f' %(latitude,longitude))
            del_lati = (latitude - waypoint[0] ) * 10000
            del_longi = (longitude - waypoint[1]) * 10000
            print('del_lati: %f del_longi: %f' %(del_lati, del_longi))
            print('this is gps and I m tell gps : %f' %(del_longi))
            return (del_lati, del_longi)
            #except:
            #    return (1 , 1)
            #    pass
if __name__ == '__main__':
    location(way)
