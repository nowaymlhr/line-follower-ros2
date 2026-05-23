#!/usr/bin/env python3
import rclpy
from sensor_msgs.msg import Image #For subscribing to the camera topic
from std_msgs.msg import Float64 #For publishing the track detection results, if needed
import cv2
from cv_bridge import CvBridge #For converting ROS images to OpenCV format
from rclpy.node import Node


class LineDetectionNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("line_detection") # MODIFY NAME

        self.declare_parameter('start', False) # Declare a parameter for the image width

        self.subscriber_ = self.create_subscription(Image, '/image_raw', self.image_callback, 10) #For getting the cam data for track detection
        self.publisher_ = self.create_publisher(Float64, '/track_detection', 10) #For publishing the track detection results
        self.bridge = CvBridge() #For converting ROS images to OpenCV format
        self.start = self.get_parameter('start').value
        self.image_width = 640
        self.last_error = 0.0

        self.add_post_set_parameters_callback(self.parameter_update_callback)


    def image_callback(self, msg):

        if self.start:
            #1 - convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            #2 - Convert it into grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            #3 - Using threshold to isolate black line
            _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

            #4 - Calculate the moments of the binary image to find the centroid of the line
            moments = cv2.moments(binary)

            #m[00] = all the white pixels
            #m[10] = sum of x coordinates of all the white pixels
            #m[01] = sum of y coordinates of all the white pixels

            error_msg = Float64()

            #5 - Calculate the error (deviation from the center of the image)
            if moments['m00'] > 0: # If the track exists in the image
                cx = int(moments['m10'] / moments['m00'])
                error = cx - (self.image_width / 2)
                self.last_error = error
                error_msg.data = float(error)
            else: # If the track does not exist in the image, we can set the error
                error_msg.data = self.last_error
                self.get_logger().warn("Track not detected in the image.")

            #6 - Publish the error
            self.publisher_.publish(error_msg)

    def parameter_update_callback(self, params):
        for param in params:
            if param.name == 'start' and param.type_ == rclpy.Parameter.Type.BOOL:
                self.start = param.value
                self.get_logger().info(f"Parameter 'start' updated to: {self.start}")
        





def main(args=None):
    rclpy.init(args=args)
    node = LineDetectionNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
