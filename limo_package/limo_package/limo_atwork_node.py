#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped

class LimoAtWorkNode(Node):
    def __init__(self):
        super().__init__('limo_atwork_node')
        self.initial_pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.get_logger().info('Limo At Work node started.')
        self.publish_initialpose()

    # TODO: CHANGE COORDINATES
    def publish_initialpose(self):
        initialpose_msg = PoseWithCovarianceStamped()
        initialpose_msg.header.stamp = self.get_clock().now().to_msg()
        initialpose_msg.header.frame_id = 'map'
        initialpose_msg.pose.pose.position.x = 1.0
        initialpose_msg.pose.pose.position.y = 2.0
        initialpose_msg.pose.pose.position.z = 0.0
        initialpose_msg.pose.pose.orientation.x = 0.0
        initialpose_msg.pose.pose.orientation.y = 0.0
        initialpose_msg.pose.pose.orientation.z = 0.0
        initialpose_msg.pose.pose.orientation.w = 1.0
        initialpose_msg.pose.covariance = [
            0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942
        ]

        self.initial_pub.publish(initialpose_msg)
        self.get_logger().info('Published initialpose once.')

    def publish_goal_pose(self, x, y, z, orientation):
        goal_msg = PoseStamped()
        goal_msg.header.stamp = self.get_clock().now().to_msg()
        goal_msg.header.frame_id = 'map'
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.position.z = z
        goal_msg.pose.orientation.x = orientation.x
        goal_msg.pose.orientation.y = orientation.y
        goal_msg.pose.orientation.z = orientation.z
        goal_msg.pose.orientation.w = orientation.w
        self.goal_pub.publish(goal_msg)
        self.get_logger().info('Published goal_pose.')

    def set_goal(self, x, y, z, orientation):
        self.publish_goal_pose(x, y, z, orientation)
        self.get_logger().info('Goal set to: x={}, y={}, z={}'.format(x, y, z))

    def mission_controller(self):
        # Example of setting a goal
        self.set_goal(5.0, 5.0, 0.0, PoseStamped().pose.orientation)
        self.get_logger().info('Mission controller running.')

    def move_arm(self, x, y, z):
        # Placeholder for arm movement logic
        self.get_logger().info('Moving arm to x={}, y={}, z={}'.format(x, y, z))

    def open_manipulator(self):
        # Placeholder for opening manipulator logic
        self.get_logger().info('Opening manipulator.')

    def close_manipulator(self):
        # Placeholder for closing manipulator logic
        self.get_logger().info('Closing manipulator.')

    def read_april_tags(self):
        # Placeholder for reading April tags logic
        self.get_logger().info('Reading April tags.')

    def read_robot_and_move(self):
        # Placeholder for reading robot and moving logic
        self.get_logger().info('Reading robot and moving.')

def main(args=None):
    rclpy.init(args=args)
    try:
        node = LimoAtWorkNode()
        node.mission_controller()
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Limo At Work node stopped.')
    finally:
        node.destroy_node()

if __name__ == '__main__':
    main()