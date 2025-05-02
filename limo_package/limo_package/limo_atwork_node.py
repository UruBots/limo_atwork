#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from apriltag_msgs.msg import AprilTagDetectionArray

class LimoAtWorkNode(Node):
    def __init__(self):
        super().__init__('limo_atwork_node')
        self.initial_pub = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.arm_pub = self.create_publisher(JointTrajectory, '/goal_joint_trajectory', 10)
        self.tag_sub = self.create_subscription(
            AprilTagDetectionArray,
            '/tag_detections',
            self.read_april_tags,
            10
        )
        self.get_logger().info('Limo At Work node started.')
        self.publish_initialpose()

    # TODO: CHANGE COORDINATES
    def publish_initialpose(self):
        initialpose_msg = PoseWithCovarianceStamped()
        initialpose_msg.header.stamp = self.get_clock().now().to_msg()
        initialpose_msg.header.frame_id = 'map'
        initialpose_msg.pose.pose.position.x = 0.0
        initialpose_msg.pose.pose.position.y = 0.0
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

        for i in range(10):
            self.initial_pub.publish(initialpose_msg)
            self.get_logger().info(f'Published initialpose #{i+1}')
            time.sleep(0.2)
        # self.get_logger().info('Published initialpose once.')

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
                
        for i in range(10):
            self.goal_pub.publish(goal_msg)
            self.get_logger().info(f'Published goal_pose #{i+1}')
            time.sleep(0.2)

    def set_goal(self, x, y, z, orientation):
        self.publish_goal_pose(x, y, z, orientation)
        self.get_logger().info('Goal set to: x={}, y={}, z={}'.format(x, y, z))

    def mission_controller(self):
        orientation = PoseStamped().pose.orientation
        orientation.z = -0.7169632618807529
        orientation.w = 0.6970562528027344
        # Example of setting a goal
        self.set_goal(2.035064697265625, -1.3726273775100708, 0.0, orientation)
        self.get_logger().info('Mission controller running.')

    def move_arm(self, x, y, z):
        jt = JointTrajectory()
        jt.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        point = JointTrajectoryPoint()
        # Placeholder con valores dummy:
        point.positions = [0.0, -1.0, 1.0, 0.5]
        point.time_from_start.sec = 2
        jt.points.append(point)
        self.arm_pub.publish(jt)
        self.get_logger().info(f'Moving arm to x={x}, y={y}, z={z}')

    def open_manipulator(self):
        self.get_logger().info('Opening manipulator.')
        self.move_gripper(0.01)

    def close_manipulator(self):
        self.get_logger().info('Closing manipulator.')
        self.move_gripper(-0.01)

    def move_gripper(self, position):
        jt = JointTrajectory()
        jt.joint_names = ['gripper']
        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start.sec = 1
        jt.points.append(point)
        self.arm_pub.publish(jt)

    def read_april_tags(self, msg):
        # Placeholder for reading April tags logic
        self.get_logger().info('Reading April tags.')
        if not msg.detections:
            return
        tag = msg.detections[0]
        tag_id = tag.id[0]
        self.get_logger().info(f'Detected AprilTag ID: {tag_id}')

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