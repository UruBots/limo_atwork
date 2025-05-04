# limo_atwork

### Clone repository
```
git clone --recurse-submodules -b ros2-foxy https://github.com/UruBots/limo_atwork.git
```
### Install
```
wget https://raw.githubusercontent.com/ROBOTIS-GIT/open_manipulator/foxy-devel/open_manipulator_x.repos
vcs import src < open_manipulator_x.repos
source /opt/ros/foxy/setup.sh && rosdep install --from-paths src --ignore-src -r -y
```
### Filter packages
```
colcon build --symlink-install --packages-select limo_ros2 limo_package
```
### Build packages with gcc 9
```
colcon build --cmake-force-configure \
  --cmake-args -DCMAKE_C_COMPILER=/usr/bin/gcc-10 -DCMAKE_CXX_COMPILER=/usr/bin/g++-10
```
#### Create 2d map
```
sudo apt-get install ros-foxy-rtabmap-ros
ros2 launch limo_bringup limo_start.launch.py
ros2 launch limo_bringup cartographer.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard

ros2 run nav2_map_server map_saver_cli -f map
```

### Create 3d map
```
ros2 launch limo_bringup limo_start.launch.py
ros2 launch orbbec_camera dabai.launch.py 
ros2 launch limo_package limo_rtab_rgbd.launch.py 
ros2 run teleop_twist_keyboard teleop_twist_keyboard 
```
### Start
```
ros2 launch limo_package start.launch.py
```
### Run limo_atwork Node
```
ros2 launch limo_package limoatwork.launch.py
```
### Run limo_atrescue Node
```
ros2 launch limo_package limoatrescue.launch.py
```
### Kill ROS2 Process
```
sudo chmod +x kill_ros2.sh
./kill_ros2.sh
```