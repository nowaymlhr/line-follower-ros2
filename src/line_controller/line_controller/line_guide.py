#!/usr/bin/env python3
import rclpy
from std_msgs.msg import Float64 #For subscribing to the track detection results
from geometry_msgs.msg import Twist #For publishing the velocity commands to the robot
from rclpy.node import Node


class LineGuideNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("line_guide") # MODIFY NAME

        self.subscriber_ = self.create_subscription(Float64, '/track_detection', self.track_detection_callback, 10) #For subscribing to the track detection results
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) #For publishing the velocity commands to the robot
        self.last_error = 0.0

    def track_detection_callback(self, msg):
        # Implement your line following logic here
        error = msg.data
        sum_errors = error + self.last_error

        #Using a simple proportional controller (for turning)
        Kp = 0.02
        Ki = 0.0
        Kd = 0.01

        twist = Twist()
        twist.linear.x = max(0.5, 1.0 - 0.1 *abs(error)) # Constant forward speed
        twist.angular.z = -(Kp * error + Ki * sum_errors + Kd * (error - self.last_error)) # Turn based on the error (negative sign to turn in the correct direction)
        self.last_error = error # Update the last error for the next iteration
        self.publisher_.publish(twist)



def main(args=None):
    rclpy.init(args=args)
    node = LineGuideNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
