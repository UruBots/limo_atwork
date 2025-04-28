from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='limo_package',
            executable='limo_atwork_node',
            name='limo_atwork_node',
            output='screen'
        )
    ])