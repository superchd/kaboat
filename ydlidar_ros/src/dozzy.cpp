#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include <vector>
#include <iostream>
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"
#define RAD2DEG(x) ((x)*180./M_PI)
#include <sstream>

float g_optimal;
std::vector<float> distances;
std::vector<float> real_distances;
std::vector< std::vector <float> > tmp;
int g_num;
int g_count;
float min;
float find_optimal_degree(const std::vector<float> distances);


float scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan)
{
    int count = scan->scan_time / scan->time_increment;
	g_count = count ;
    float min = 0;
    
	distances.clear();
	real_distances.clear();

	int a = 0;
	int b = 0;
	float dozzy = 0.4;
	for(int i = 0; i <= count /2 ; i++) 
    {
   
      	if (scan->ranges[i] > dozzy || scan->ranges[i] == 0) 
	  {
		  distances.push_back(1); 
		a++;
	  }                                  
      	else if (scan->ranges[i] < dozzy )
      {
		  distances.push_back(0);
		b++;
      }
//0.4~1.9?
//	printf("clear");

	if (a = count )
	{
	 distances[0] = 0;}
	else if (b = count)
	{
	 distances[0] = 1;}

      	//if (scan -> ranges[i] > 0.12)
	//{
		//real_distances.push_back(scan->ranges[i]);
	//}
     //min = *min_element(real_distances.begin(), real_distances.end());
    }
	//printf("min:%f\n",min);
//	for(int i = 0; i <= count /2 ; i++)

//	{	float z = i; 
//	std::cout << "distance[" << z << "]" << distances[i] << std::endl;}

    return (find_optimal_degree(distances));
}



std::vector <std::vector <float> > make_second_array(const std::vector<float> distances)
{
	std::vector <float> nums(2);

   std::vector <std::vector<float>> array;
	
   	g_num =0;
	int ranges = 0;
	int first_angle = 0;
	array.clear();
	tmp.clear();
	int i;

	for (i = 1; i <= g_count /2  ; i++) {
        	if ((distances[i - 1] == 1) && (distances[i] == 0) && (ranges > 10) && (first_angle != 0)) {
				nums[0] = ranges;
				nums[1] = first_angle;
				array.push_back(nums);
				g_num ++;

				first_angle = 0;
				ranges = 0;
      }
        	else if ((distances[i - 1] == 0) &&(distances[i] == 0)  ) {
				first_angle = i;
        }
		else if ((distances[i - 1] == 1) && (distances[i] == 1)) {
		ranges += 1;
        }
    }
	tmp = array;
	array.clear();
	return tmp;
}

float select_angle(std::vector< std::vector<float> > array)
{
   float ranges;
   float first_angle;
   int i;
        //배열크기,입력값,최소값,최대값
   ranges = array[0][0];

   first_angle = array[0][1];

      // 배열 첫번째 값을 최소 최대값으로 설정
	for(i=0; i < g_num-1 ;i++)
	{
		if(ranges < array[i][0])
	{
		ranges = array[i][0];
		first_angle = array[i][1];
		std::cout << "range is " << array[i][0] / g_count * 360 << " , first is " << array[i][1] / g_count * 360<< std::endl; 

	}
		else{
		std::cout << "range is " << array[i][0] / g_count * 360 << " , fisrt is " << array[i][1] / g_count * 360<< std::endl; 
}

	}
   	std::cout << "ranges: " << ranges/ g_count * 360 << " first angle: " << first_angle/ g_count * 360 << std::endl;

	ranges = ranges/ g_count * 360;
	first_angle = first_angle/ g_count * 360;

   return (first_angle + (ranges / 2));
}

float find_optimal_degree(const std::vector<float> distances)
{

	float optimal;

   optimal = select_angle(make_second_array(distances));
   printf("optimal: %f\n",  optimal);
  // msg = std::to_string(optimal);
	
   g_optimal = optimal;
   
	
   return (optimal);
}


float min_distance(const std::vector<float> real_distances)
{
	float min = *min_element(real_distances.begin(), real_distances.end());
	return min;
}







//main
int main(int argc, char **argv)
{
    ros::init(argc, argv, "seven");
    ros::NodeHandle n;
    ros::Subscriber sub = n.subscribe<sensor_msgs::LaserScan>("/scan", 1000, scanCallback);
	ros::Publisher angle_pub = n.advertise<std_msgs::Float64>("rotate_angle", 1000);
	ros::Publisher min_pub = n.advertise<std_msgs::Float64>("minimum_distance", 1000);
	ros::Rate loop_rate(1);
	while (ros::ok())
	{
		std_msgs::Float64 msg;
		std_msgs::Float64 mini;

        float g_o;
        g_o = g_optimal;
		//std::stringstream ss;
		//ss << g_optimal  ;
		msg.data = g_o;
		mini.data = min;

		ROS_INFO("%f", msg.data);
		ROS_INFO("%f", mini.data);

		angle_pub.publish(msg);
		min_pub.publish(mini);

		ros::spinOnce();

		loop_rate.sleep();
	}
    return 0;
}

