# ROS Support

Run the following in `car-ws` to download and build ROS packages.

```
wstool update

rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y -r

catkin_make

source devel/setup.sh
```
