#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
import math
from functools import reduce


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

        way_latitude = waypoint[0]
        way_longitude = waypoint[1]
        rotate_way_latitude = math.cos(-0.6060006599)*way_latitude - math.sin(-0.6060006599)*way_longitude
        rotate_way_longitude = math.sin(-0.6060006599)*way_latitude + math.cos(-0.6060006599)*way_longitude
        while True:
            data = ser.readline()
            result = collections.defaultdict()
            res = GPSparser(data) 
            print("I'm in GPS, ready to return del_lati, del_longi")
            if res == None:
                print("none")
                # print("I'm in Gps, and in res == None")
            else :
                   # res = str(res)
                print(res)
                lat = str (res[2])
                lon = str (res[4])
            # result['altitude'] = float(res[9])
                    
                if (res == "checksum error"):
                        print("")
            # print(result)
                print(lat)
                lat_h = float(lat[2:4])
                lon_h = float(lon[2:5])
                lat_m = float(lat[4:12])
                lon_m = float(lon[5:13])
                print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))

                latitude = lat_h + (lat_m/60)
                longitude = lon_h + (lon_m/60)
                
                print('latitude: %f longitude: %f' %(latitude,longitude))
                rotate_latitude = math.cos(-0.6060006599)*latitude - math.sin(-0.6060006599)*longitude
                rotate_longitude = math.sin(-0.6060006599)*latitude + math.cos(-0.6060006599)*longitude
                
                print('rotate_latitude: %f rotate_longitude: %f' %(rotate_latitude, rotate_longitude))
                del_lati = rotate_latitude - rotate_way_latitude    
                del_longi = rotate_longitude - rotate_way_longitude
                break

        return (del_lati, del_longi)
            #except:
            #    return (1 , 1)
            #    pass
if __name__ == '__main__':
    location(way)
