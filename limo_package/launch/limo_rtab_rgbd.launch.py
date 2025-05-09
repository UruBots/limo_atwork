# Requirements:
#   Install Turtlebot3 packages
#   Modify turtlebot3_waffle SDF:
#     1) Edit turtlebot3_gazebo/models/turtlebot3_waffle/model.sdf
#     2) Add
#          <joint name="camera_rgb_optical_joint" type="fixed">
#            <parent>camera_rgb_frame</parent>
#            <child>camera_rgb_optical_frame</child>
#            <pose>0 0 0 -1.57079632679 0 -1.57079632679</pose>
#            <axis>
#              <xyz>0 0 1</xyz>
#            </axis>
#          </joint> 
#     3) Rename <link name="camera_rgb_frame"> to <link name="camera_rgb_optical_frame">
#     4) Add <link name="camera_rgb_frame"/>
#     5) Change <sensor name="camera" type="camera"> to <sensor name="camera" type="depth">
#     6) Change image width/height from 1920x1080 to 640x480
#     7) Note that we can increase min scan range from 0.12 to 0.2 to avoid having scans 
#        hitting the robot itself
# Example:
#   $ export TURTLEBOT3_MODEL=waffle
#   $ ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
#
#   SLAM:
#   $ ros2 launch rtabmap_ros turtlebot3_rgbd.launch.py
#   OR
#   $ ros2 launch rtabmap_ros rtabmap.launch.py visual_odometry:=false frame_id:=base_footprint odom_topic:=/odom args:="-d" use_sim_time:=true rgb_topic:=/camera/image_raw depth_topic:=/camera/depth/image_raw camera_info_topic:=/camera/camera_info approx_sync:=true
#
#   Navigation (install nav2_bringup package):
#     $ ros2 launch nav2_bringup navigation_launch.py use_sim_time:=True
#     $ ros2 launch nav2_bringup rviz_launch.py
#
#   Teleop:
#     $ ros2 run turtlebot3_teleop teleop_keyboard

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    qos = LaunchConfiguration('qos')
    localization = LaunchConfiguration('localization')

    #     parameters={
    #       'frame_id':'base_link',
    #       'use_sim_time':False,
    #       'subscribe_depth':True,
    #       'subscribe_rgbd':False,
    #       'subscribe_rgb':True,
    #       'subscribe_scan':True,
    #       'use_action_for_goal':True,
    #       'wait_for_transform':0.2,
    #       'qos_image':qos,
    #       'qos_scan':qos,
    #       'qos_camera_info':qos,
    #       'approx_sync':True,
    #       'Reg/Force3DoF':'true',
    #       'Optimizer/GravitySigma':'0' # Disable imu constraints (we are already in 2D)
    # }

    rtabmap_parameters={
          'use_sim_time':False,
          'subscribe_rgbd':True,
          'subscribe_rgb':True,
          'subscribe_scan':True,
          'use_action_for_goal':True,
          'odom_sensor_sync': False,
          # RTAB-Map's parameters should be strings:
          'Mem/NotLinkedNodesKept':'false',
          'subscribe_depth': True,
          'subscribe_rgb': True,
          'wait_for_transform':0.2,
          'queue_size': 20,
          'approx_sync':True
    }

    # Shared parameters between different nodes
    shared_parameters={
          'frame_id':'base_link',
        #   'use_sim_time':use_sim_time,
          # RTAB-Map's parameters should be strings:
          'Reg/Strategy':'1',
          'Reg/Force3DoF':'true',
          'Mem/NotLinkedNodesKept':'false',
          'Icp/PointToPlaneMinComplexity':'0.04' # to be more robust to long corridors with low geometry
    }

    remappings=[
          ('odom','/odom'),
          ('scan','/scan'),
          ('rgb/image', '/camera/camera/color/image_raw'),
          ('rgb/camera_info', '/camera/camera/color/camera_info'),
          ('depth/image', '/camera/camera/depth/image_raw')
    ]

    base_link_to_camera_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_camera',
        arguments=['0.1','0','0.18','0','0','0','1','base_link','camera_link']
    )

    realsense_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='camera',
        output='screen',
        parameters=[{
            'frame_id': 'camera_link',
            'enable_rgbd': True,
            'enable_sync': True,
            'enable_depth': True,
            'enable_color': True,
            'align_depth.enable': True,
            'depth_module.depth_profile': '640x480x30',
            'rgb_camera.profile': '640x480x30',
            'color_depth_aligned': True,
            'enable_infra1': False,
            'enable_infra2': False,
        }]
    )

    rgbd_sync_node = Node(
        package='rtabmap_sync',
        executable='rgbd_sync',
        name='rgbd_sync',
        output='screen',
        parameters=[rtabmap_parameters, shared_parameters],
        remappings=remappings
    )
    return LaunchDescription([

        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        DeclareLaunchArgument(
            'qos', default_value='2',
            description='QoS used for input sensor topics'),
            
        DeclareLaunchArgument(
            'localization', default_value='false',
            description='Launch in localization mode.'),

        # Nodes to launch
        realsense_node,        
        # SLAM mode:
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[rtabmap_parameters, shared_parameters],
            remappings=remappings,
            arguments=['-d']), # This will delete the previous database (~/.ros/rtabmap.db)
            
        # Localization mode:
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[rtabmap_parameters, shared_parameters, {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),

        # # Nodes to launch
        # Node(
        #     package='rtabmap_sync', executable='rgbd_sync', output='screen',
        #     parameters=[rtabmap_parameters, shared_parameters],
        #     remappings=remappings),

        rgbd_sync_node,
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=[rtabmap_parameters, shared_parameters],
            remappings=remappings),
        base_link_to_camera_node
    ])
