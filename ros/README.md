# ROS Support

Run `build.sh`, or use the following commands in `car-ws` to download and build ROS packages.

```
wstool update

rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y -r

catkin_make
```

Then either source the development packages directly:

```
source devel/setup.sh
```

or install the packages and source from their installation directory:

```
catkin_make install
source install/setup.sh
```
