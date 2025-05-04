cmake_minimum_required(VERSION 3.5)
project(limo_package)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)

# Si tienes ejecutables en C++ (descomenta esto y ajusta)
# add_executable(my_node src/my_node.cpp)
# ament_target_dependencies(my_node rclcpp std_msgs)

# Install Python modules if using ROS2 Python nodes
#ament_python_install_package(${PROJECT_NAME})
ament_python_install_package(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Install launch and param files
install(
  DIRECTORY launch rviz
  DESTINATION share/${PROJECT_NAME}/
)

#install(
#  DIRECTORY param
#  DESTINATION share/${PROJECT_NAME}/
#)

# Install any resource files
#install(
#  DIRECTORY resource
#  DESTINATION share/${PROJECT_NAME}/
#)

# Install your package.xml
install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}/
)

# Si tienes ejecutables (descomenta)
# install(TARGETS
#   my_node
#   DESTINATION lib/${PROJECT_NAME}
# )

ament_package()