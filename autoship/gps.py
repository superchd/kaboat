#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import operator
import collections
import calcpoint
import math

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	

def GPSparser(data):
	gps_data = data.split(",")
	idx_rmc = data.find('GNGGA')
	if data[idx_rmc:idx_rmc+5] == "GNGGA":
		data = data[idx_rmc:]	
		print (data)
		if checksum(data):
			parsed_data = data.split(",")
			return parsed_data
		else :
			print ("checksum error")

def checksum(sentence):
	sentence = sentence.strip('\n')
	nmeadata, cksum = sentence.split('*',1)
	calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
	print(int(cksum,16), calc_cksum)
	if int(cksum,16) == calc_cksum:
		return True 
	else:
		return False 

def location():

	way_latitude = float(input("way_latitude: "))
	way_longitude = float(input("way_longitude: "))

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
                        a = (way_longitude - longitude) / (way_latitude - latitude)
                        
			way_radi  = math.atan(a)
                        way_degree = way_radi*(180/math.pi)

			print(way_degree)
		except:
                    pass
		


if __name__ == '__main__':
#	try:	
		location()

#	except rospy.ROSInterruptException:
		#pass
