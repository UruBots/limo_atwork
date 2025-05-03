import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource, AnyLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.conditions import IfCondition

def generate_launch_description():
    limo_bringup_dir = get_package_share_directory('limo_bringup')
    astra_camera_dir = get_package_share_directory('astra_camera')
    apriltag_ros_dir = get_package_share_directory('apriltag_ros')
    manipulator_dir = get_package_share_directory('open_manipulator_x_controller')
    yolo_ros_dir = get_package_share_directory('yolo_ros')

    is_work = DeclareLaunchArgument(
        'is_work',
        default_value='true',
        description='Whether to launch Working mode or not'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(limo_bringup_dir, 'launch', 'limo_start.launch.py')
            )
        ),
        # Lanzar astra.launch.xml
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                os.path.join(astra_camera_dir, 'launch', 'astra.launch.xml')
            )
        ),
        # Lanzar AprilTag con Astra como fuente de imagen
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(apriltag_ros_dir, 'launch', 'tag_realsense.launch.py')
            ),
            launch_arguments={
                'camera_name': '/camera/color',
                'image_topic': '/camera/image_raw'
            }.items()
        ),
        # Lanzar el manipulador
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(manipulator_dir, 'launch', 'open_manipulator_x_controller.launch.py')
            )
        ),

        # Launch YOLO detection
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(yolo_ros_dir, 'launch', 'yolo.launch.py')
            ),
            launch_arguments={
                'model_path': os.path.join(yolo_ros_dir, 'models', 'yolov8n.pt'),
                'image_topic': '/camera/color/image_raw',  # or your topic from astra_camera
                'visualize': 'true'
            }.items(),
            condition=IfCondition(is_work)
        )
    ])