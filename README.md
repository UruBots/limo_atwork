# limo_atwork

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
### Run limo_atwork Node
```
ros2 launch limo_package limoatwork.launch.py
```
### Kill ROS2 Process
```
sudo chmod +x kill_ros2.sh
./kill_ros2.sh
```