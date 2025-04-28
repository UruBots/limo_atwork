# limo_atwork

### Install
```
source /opt/ros/foxy/setup.sh && rosdep install --from-paths src --ignore-src -r -y
```
Filter packages
```
colcon build --symlink-install --packages-select limo_ros2 limo_package
```