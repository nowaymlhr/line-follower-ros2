# Line Follower Robot - ROS2 and Gazebo

## Overview
A vision-based line follower robot simulated in Gazebo Harmonic using ROS2 Jazzy. The robot uses a downward-facing camera to detect a black track and follows it using a PID controller.

## Demo
![image](https://github.com/user-attachments/assets/7278011c-318e-4f30-82cf-b3616dc321b0)

## Dependencies
- ROS2 Jazzy
- Gazebo Harmonic
- ros_gz_sim
- cv_bridge
- OpenCV

## Package Structure

### line_follower_bot
Contains the URDF/Xacro files for the robot, structured modularly:
Example - 
- `base.xacro` — robot links and joints
- `properties.xacro` — dimensions, camera parameters and inertias
- 'camera_sensor.xacro' - camera-sensor (including gazebo code)
- 'base_gazebo.xacro' - gazebo code for the bot
- 'line_follower.urdf.xacro' - Includes all the files; main file

### my_robot_bringup
Contains the launch file, Gazebo bridge config and the simulation world.
Track used: [KroNton - Gazebo Fuel](https://app.gazebosim.org/KroNton/fuel/models/track1)

### line_follower_vision
Contains two nodes:
- `line_detection.py` — subscribes to `/image_raw`, converts to OpenCV format, applies grayscaling and thresholding, calculates centroid via moments, publishes error to `/track_detection`
- `line_guide.py` — subscribes to `/track_detection`, runs PID controller, publishes `linear.x` and `angular.z` to `/cmd_vel`

## How it Works
1. Camera captures image of the track below
2. Image is converted to grayscale and thresholded to isolate the black line
3. Centroid of the line is calculated using image moments
4. Error = centroid x position - image center (320px)
5. PID controller converts error into steering commands
6. Robot steers to minimize error and follow the line

## How to Run

```bash
# Clone into your workspace
cd ~/ros2_ws/src
git clone https://github.com/yourrepo/line-follower-ros2

# Build
cd ~/ros2_ws
colcon build
source install/setup.bash

# Launch simulation
ros2 launch my_robot_bringup line_follower.launch.xml

# Start the robot (in a second terminal)
ros2 param set /line_detection start True
```

## Future Improvements
- Recovery behavior when line is completely lost from camera frame
- Automatic speed reduction on sharp turns
- Dynamic threshold adjustment for varying lighting conditions
