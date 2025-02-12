#!/usr/bin/env python3

import rospy

from std_msgs.msg import *
from open_manipulator_msgs.msg import *
from move_base_msgs.msg import *
from geometry_msgs.msg import *
from open_manipulator_msgs.srv import SetKinematicsPose, SetKinematicsPoseRequest, SetKinematicsPoseResponse
import time
from sensor_msgs.msg import LaserScan
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from apriltag_ros.msg import AprilTagDetectionArray

laser_scan = LaserScan()
tags = AprilTagDetectionArray()

def call_goal_task_space_service(end_effector_name, position, orientation, time):
	rospy.wait_for_service('/goal_task_space_path')
	try:
		set_kinematics_pose = rospy.ServiceProxy('/goal_task_space_path', SetKinematicsPose)

		request = SetKinematicsPoseRequest()
		request.end_effector_name = end_effector_name
		request.kinematics_pose.pose.position.x = position[0]
		request.kinematics_pose.pose.position.y = position[1]
		request.kinematics_pose.pose.position.z = position[2]
		request.kinematics_pose.pose.orientation.x = orientation[0]
		request.kinematics_pose.pose.orientation.y = orientation[1]
		request.kinematics_pose.pose.orientation.z = orientation[2]
		request.kinematics_pose.pose.orientation.w = orientation[3]
		request.path_time = time

		response = set_kinematics_pose(request)
		return response
	except rospy.ServiceException as e:
		rospy.logerr("Service call failed: %s" % e)
		return None

def call_tool_control_service(grip_state):
	rospy.wait_for_service('/goal_tool_control')
	try:
		set_joint_position = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)
       
		request = SetJointPositionRequest()
		request.joint_position.joint_name = ["gripper"]
		request.joint_position.position = [0.01 if grip_state == "open" else -0.01]  # Adjust values as needed
		request.path_time = 1.0  # Time to complete movement

		response = set_joint_position(request)
		return response
	except rospy.ServiceException as e:
		rospy.logerr("Service call failed: %s" % e)
		return None

def open_gripper():
	rospy.loginfo("Opening gripper...")
	response = call_tool_control_service("open")
	if response:
		rospy.loginfo("Gripper opened successfully: %s" % response.is_planned)

	rospy.sleep(2)  # Wait before closing	

def close_gripper():
	rospy.loginfo("Closing gripper...")
	response = call_tool_control_service("close")
	if response:
		rospy.loginfo("Gripper closed successfully: %s" % response.is_planned)

	rospy.sleep(2)  # Wait before closing

def move_arm(pos, ori):
	end_effector = "gripper"
	position = pos  # Example position (x, y, z)
	orientation = ori  # Example quaternion (x, y, z, w)
	path_time = 1.5  # Example path time in seconds

	response = call_goal_task_space_service(end_effector, position, orientation, path_time)
   
	if response:
		rospy.loginfo("Service response: %s" % response.is_planned)
	else:
		rospy.logwarn("Failed to receive a response from the service.")

def move_robot(x,y,wx,wy,wz,ww):
	pub = rospy.Publisher("/move_base/goal", MoveBaseActionGoal, queue_size=10)

	global_target_position = MoveBaseActionGoal()

	global_target_position.goal.target_pose.header.frame_id = 'map'
	global_target_position.goal.target_pose.pose.position.x = x
	global_target_position.goal.target_pose.pose.position.y = y

	global_target_position.goal.target_pose.pose.orientation.x = wx
	global_target_position.goal.target_pose.pose.orientation.y = wy
	global_target_position.goal.target_pose.pose.orientation.z = wz
	global_target_position.goal.target_pose.pose.orientation.w = ww

	rate = rospy.Rate(10)
	flag = 0
	while not rospy.is_shutdown():
		pub.publish(global_target_position)
		rate.sleep()
		if flag == 10:
			break
		else: 
			flag+=1

def machine_state_arm_grab(x,y,z):
	global tags

	rospy.loginfo(str(x)+", "+str(y)+", "+str(z))

	rospy.loginfo("Moving to home")

	position = [0.0, 0.08, 0.10]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to home1")

	position = [0.0, 0.12, 0.05]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving over the object")
	
	position = [0.0, 0.13-y, -0.0]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	open_gripper()

	time.sleep(2)

	rospy.loginfo("Moving to object")

	position = [0.0, 0.13-y, 0.31-z]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	close_gripper()

	time.sleep(2)

	rospy.loginfo("Moving over the object")
	
	position = [0.0, 0.13-y, -0.0]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to home")

	position = [0.0, 0.13, 0.08]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to home")

	position = [0.0, 0.13, 0.10]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to Store")

	position = [0.15, 0.0, 0.11]  # Example position (x, y, z)
	orientation = [0.0, 0.7, 0.0, 0.7]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(3)

	rospy.loginfo("Moving to Store Down")

	position = [0.15, 0.0, 0.06]  # Example position (x, y, z)
	orientation = [0.0, 0.7, 0.0, 0.7]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(5)


def machine_state_arm_release(x,y,z):

	rospy.loginfo("Moving to home")

	position = [0.0, 0.13, 0.10]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving over the object")
	
	position = [0.0, 0.13-y, -0.0]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)	

	time.sleep(2)

	rospy.loginfo("Moving to object")

	position = [0.0, 0.13-y, 0.31-z]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	open_gripper()

	time.sleep(2)

	rospy.loginfo("Moving over the object")
	
	position = [0.0, 0.13-y, -0.0]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to home")

	position = [0.0, 0.13, 0.08]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to home")

	position = [0.0, 0.13, 0.10]  # Example position (x, y, z)
	orientation = [0.51, -0.48, -0.51, -0.48]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(2)

	rospy.loginfo("Moving to Store")

	position = [0.15, 0.0, 0.11]  # Example position (x, y, z)
	orientation = [0.0, 0.7, 0.0, 0.7]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(3)

	rospy.loginfo("Moving to Store Down")

	position = [0.15, 0.0, 0.06]  # Example position (x, y, z)
	orientation = [0.0, 0.7, 0.0, 0.7]  # Example quaternion (x, y, z, w)

	move_arm(position, orientation)

	time.sleep(5)	

def laser_callback(data):
	global laser_scan
	laser_scan = data

def dock_robot():
	global laser_scan

	cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

	vel_msg = Twist()

	while not rospy.is_shutdown():
		try:
			if (sum(laser_scan.ranges[210:230])/len(laser_scan.ranges[210:230]) < 0.095):
				vel_msg = Twist()
				rospy.loginfo("Arrived in front of the base")
				break
				
			else:
				vel_msg.linear.x = 0.1
		except:
			pass		

		cmd_vel_pub.publish(vel_msg)

	rospy.loginfo("Rotating to dock")
	vel_msg.linear.x = 0.0
	vel_msg.angular.z = -0.5
	timeout = time.time() + 2.5
	while True:
		if (time.time() < timeout):
			cmd_vel_pub.publish(vel_msg)
			#rospy.loginfo(str(sum(laser_scan.ranges[350:370])/len(laser_scan.ranges[350:370])))
		else:
			break

def undock_robot():	

	cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

	vel_msg = Twist()

	rospy.loginfo("Rotating to dock")
	vel_msg.linear.x = 0.0
	vel_msg.angular.z = -0.5
	timeout = time.time() + 2.25
	while True:
		if (time.time() < timeout):
			cmd_vel_pub.publish(vel_msg)			
		else:
			break

	vel_msg.linear.x = 0.1
	vel_msg.angular.z = 0.0
	timeout = time.time() + 2.25
	while True:
		if (time.time() < timeout):
			cmd_vel_pub.publish(vel_msg)			
		else:
			break

def tag_callback(data):
	global tags
	tags = data	

def find_object_and_move(object_id):
	global tags
	rospy.loginfo("Finding Object")

	FLAG_OBJECT_FOUND = False

	cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
	vel_msg = Twist()
	
	while not rospy.is_shutdown():
		try:
			for i in range (0, len(tags.detections)):
				#rospy.loginfo(str(tags.detections[i].id))
				cmd_vel_pub.publish(Twist())
				if tags.detections[i].id[0] == object_id:
					#rospy.loginfo("Id Object found "+str(object_id))
					x = tags.detections[i].pose.pose.pose.position.x
					rospy.loginfo(str(x))				
					
					if (x < 0.01 and x > 0.0):
						cmd_vel_pub.publish(Twist())
						FLAG_OBJECT_FOUND = True
						break
					else:
						if (x < -0.0):
							vel_msg.linear.x = -0.05
						else:
							vel_msg.linear.x = 0.05
						cmd_vel_pub.publish(vel_msg)
					
				#else:	
				#	break
			if (FLAG_OBJECT_FOUND): 
				return tags.detections[i].pose.pose.pose.position.x, tags.detections[i].pose.pose.pose.position.y, tags.detections[i].pose.pose.pose.position.z
			else:
				vel_msg.linear.x = 0.03	
				cmd_vel_pub.publish(vel_msg)
		except:
			pass			
			#rospy.loginfo("Object not found")

if __name__ == "__main__":
	rospy.init_node("limo_at_work_node")

	rospy.Subscriber("/scan", LaserScan, laser_callback)

	rospy.Subscriber('/tag_detections', AprilTagDetectionArray, tag_callback)

	#machine_state_arm()	

	#dock_robot()
	
	#rospy.spin()		

	

	#rospy.loginfo("Moving to Position 1")
	
	open_gripper()

	move_robot(3.3, -2.06, 0, 0, 0.0, 1.0)

	time.sleep(20)

	dock_robot()

	time.sleep(2)

	x,y,z = find_object_and_move(object_id=4)

	machine_state_arm_grab(x,y,z)
	
	time.sleep(2)

	undock_robot()

	move_robot(0.37, -2.51, 0, 0, -0.70, 0.7)

	time.sleep(15)

	dock_robot()

	time.sleep(2)

	machine_state_arm_release(x,y,z)

	
	
	



	
	
	


