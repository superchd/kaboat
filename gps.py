#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
import math

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	

def GPSparser(data):
	gps_data = data.split(b",")
	idx_rmc = data.find(b'GNGGA')
	if data[idx_rmc:idx_rmc+5] == b"GNGGA":
		data = data[idx_rmc:]	
		print (data)
		if checksum(data):
			parsed_data = data.split(b",")
			return parsed_data
		else :
			print (b"checksum error")

def checksum(sentence):
	sentence = sentence.strip(b'\n')
	nmeadata, cksum = sentence.split(b'*',1)
	calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
	print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location():

	way_latitude = float(input("way_latitude: "))
	way_longitude = float(input("way_longitude: "))
        rotate_way_latitude = math.cos(-0.629645)*way_latitude - math.sin(-0.629645)*way_longitude
        rotate_way_longitude = math.sin(-0.629645)*way_latitude + math.cos(-0.629645)*way_longitude

        while 1:
	        data = ser.readline()
		result = collections.defaultdict()
		res = GPSparser(data)
		if res == None:
			continue
		try:
			lat = str (res[2])
			lon = str (res[4])
			result['altitude'] = float(res[9])
			
			if (res == "checksum error"):
				print("")
			print(result)
			
			lat_h = float(lat[0:2])
			lon_h = float(lon[0:3])
			lat_m = float(lat[2:10])
			lon_m = float(lon[3:11])
			print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))

			latitude = lat_h + (lat_m/60)
			longitude = lon_h + (lon_m/60)
			
			print('latitude: %f longitude: %f' %(latitude,longitude))
            		rotate_latitude = math.cos(-0.629645)*latitude - math.sin(-0.629645)*longitude
            		rotate_longitude = math.sin(-0.629645)*latitude + math.cos(-0.629645)*longitude
            
			print('rotate_latitude: %f rotate_longitude: %f' %(rotate_latitude, rotate_longitude))
            		del_lati = rotate_latitude - rotate_way_latitude	
			del_longi = rotate_longitude - rotate_way_longitude

			print('del_lati: %f del_longi: %f' %(del_lati,del_longi))
		except:
                    pass
if __name__ == '__main__':
	
		location()

