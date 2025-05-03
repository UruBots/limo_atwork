FROM ros:foxy

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# Install Gazebo 9 and required packages
RUN apt-get update && \
    apt-get install -y \
    gazebo9 \
    gazebo9-common \
    libgazebo9-dev \
    ros-foxy-gazebo-ros-pkgs \
    ros-foxy-gazebo-ros \
    ros-foxy-gazebo-dev \
    ros-foxy-gazebo-plugins \
    && apt-get clean

# Install ROS 2 packages
RUN apt-get update && apt-get install -y \
    cmake \
    git \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \    
    curl \	
    libusb-1.0-0 \
    udev \
    apt-transport-https \
    ca-certificates \
    curl \
    swig \
    software-properties-common \
    python3-pip \
    ros-foxy-dynamixel-workbench-toolbox \
    && rm -rf /var/lib/apt/lists/*


# create a workspace
RUN mkdir -p /root/limo_ws/src
WORKDIR /root/limo_ws
# Copy files
COPY . /root/limo_ws/src
# Build the workspace
RUN source /opt/ros/foxy/setup.sh && \
    rosdep install --from-paths src --ignore-src -r -y && \
    colcon build --symlink-install
# Source the workspace
RUN echo "source /root/limo_ws/install/setup.bash" >> ~/.bashrc
# Set the entrypoint
RUN source ~/.bashrc