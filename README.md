### 如果apriltag报错，安装pyapriltags,代码中改为import pyapriltags
pip install pyapriltags

### CAN驱动安装
在/usbcan_ii_linux/usbcan_libusb_x64_2020_07_01/test目录下找到libusbcan.so文件，右键选择属性，点击Permissions，在Access选项中选择Read and write。输入命令sudo mv libusbcan.so /usr/lib，将libusbcan.so文件移动到/usr/lib文件夹下。
### CAN
运行仿真程序后
sudo -s
source devel/setup.bash
rosrun raceworld can.py

### Bluetooth
运行仿真程序后
1. 
./connect_bluetooth.sh

2. 
source devel/setup.bash
rosrun raceworld bluetooth.py
