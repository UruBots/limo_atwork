from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='limo_package',
            executable='limo_atrescue_node',
            name='limo_atrescue_node',
            output='screen'
        )
    ])