#!/usr/bin/env python
import serial
import operator
import collections
import calcpoint
import rospy
import math
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray#,MultiArrayLayout,MultiArrayDimension

ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 38400, timeout = 0.1)	

class Globalpath:
    def __init__(self):
            self.GPS_x = 0.0
            self.GPS_y = 0.0
            self.psi = 0.0
            self.i = 0 #for 'Waypoints List' Index
            self.error_Distance = 30.0 # if error_distance = 0
            self.DirectionAngle = 0.0
            rospy.Subscriber("/change", Error_Distance, self.Error_Distance)
            rospy.Subscriber("/HeadingAngle_RealTime", HeadingAngle, self.HeadingAngle)

            self.direction_pub = rospy.Publisher("/Direction_Angle", DirectionAngle, queue_size = 10)
            self.thruster_pub = rospy.Publisher("/Error_Distance", Float32, queue_size = 10)


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


    def waypoint_step(self, waypoints, error_Distance, tolerance):
        if self.i + 1 != len(waypoints):
            if error_Distance > tolerance:
                waypoint = waypoints[self.i]
            elif error_Distance <= tolerance:
                waypoint = waypoints[self.i + 1]
                self.i = self.i + 1
       elif self.i + 1 == len(waypoints):
            waypoint = waypoints[self.i]
            return waypoint

    def location():

            pub = rospy.Publisher('gps_xy', Float64MultiArray, queue_size=10)
            rospy.init_node('gps', anonymous=True)
            rate = rospy.Rate(1) # 1hz

            #way_latitude = float(input("way_latitude: "))
            #way_longitude = float(input("way_longitude: "))
            
            #way_x, way_y = calcpoint.grid(way_latitude*100.0, way_longitude*100.0)
            #way_x_1 = float(input("way_x_1: "))
            #way_y_1 = float(input("way_y_1: "))
            #way_x_2 = float(input("way_x_2: "))
            #way_y_2 = float(input("way_y_2: "))
            #change = 0;

            while 1: 
                    data = ser.readline()
                    result = collections.defaultdict()
                    res = GPSparser(data)
                    if res == None:
                            continue
                        try:
                            way = waypoint_step(self, waypoints, error_Distance, tolerance)
                            way_latitude = way[0]
                            way_longitude = way[1]

                            lat = str (res[2])
                            lon = str (res[4])
                            result['altitude'] = float(res[9])
                            
                            #print(data)

                            if (res == "checksum error"):
                                    print("")
                            print(result)
                            #x, y = calcpoint.grid(result['latitude']*100.0,result['longitude']*100.0)
                            
                            
                            lat_h = float(lat[0:2])
                            lon_h = float(lon[0:3])
                            lat_m = float(lat[2:10])
                            lon_m = float(lon[3:11])
                            #print('lat_h: %f lon_h: %f lat_m: %f lon_m: %f' %(lat_h, lon_h, lat_m, lon_m))

                            latitude = lat_h + (lat_m/60)
                            longitude = lon_h + (lon_m/60)
                            
                            print('latitude: %f longitude: %f' %(latitude,longitude)) 
                            #x, y = calcpoint.grid(latitude ,longitude)
                            #print("x = %f y = %f" %(x,y))

                            value = Float64MultiArray()
                    
                            del_lati = (way_latitude - latitude)*100
                            del_longi = (way_longitude - longitude)*100
                            print("del_lati = %f del_longi = %f" %(del_lati,del_longi))
                            value.data = [del_lati,del_longi]
                            
                            #del_x_2 = way_x_2 - x
                            #del_y_2 = way_y_2 - y
                            #print("del_x_2 = %f del_y_2 = %f" %(del_x_2,del_y_2))

                            pub.publish(value)

                            rate.sleep()

                    except:
                            #print("not found data")

                            #if KeyboardInterrupt :
                            #	break
                            pass
                    

    if __name__ == '__main__':
            try:	
                    location()

            except rospy.ROSInterruptException:
                    pass

