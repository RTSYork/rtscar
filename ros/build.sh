#!/bin/sh

cd car-ws
wstool update
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y -r
catkin_make
