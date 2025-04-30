#!/bin/bash

echo "[INFO] Searching for ROS 2 related processes to kill..."

# Kill ros2 CLI commands
pkill -f "^ros2 "

# Kill Python-based ROS 2 nodes (rclpy)
pkill -f "python.*rclpy"

# Kill C++ ROS 2 nodes (rclcpp)
pkill -f "rclcpp"

# Kill RViz2
pkill -f "rviz2"

# Kill Gazebo Classic or Ignition
pkill -f "gzserver"
pkill -f "gzclient"
pkill -f "gazebo"

echo "[DONE] ROS 2 and simulation processes terminated."
