#! /usr/bin/env python3
import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image
import pyapriltags
import threading # 【修复】导入线程库以安全地处理图像数据

# 【必要添加 1】: 导入要发布消息的类型 (Bool)
from std_msgs.msg import Bool

# --- 全局变量 ---
# 将这些耗时的对象创建移到全局范围，让它们只在程序启动时执行一次
bridge = cv_bridge.CvBridge()
detector = pyapriltags.Detector()

# 发布者对象
stop_publisher = None

# 使用帧数计数器来锁存停车状态
stop_frame_counter = 0
STOP_LATCH_FRAMES = 60

# 【修复】创建一个全局变量来存储从回调函数接收到的最新图像
latest_frame = None
# 【修复】创建一个锁，以确保在多线程环境下对latest_frame的访问是安全的
frame_lock = threading.Lock()
# --- 全局变量结束 ---


def image_callback(msg):
    """
    这个回调函数现在只做一件事：接收图像消息并将其存储到全局变量中。
    它必须尽可能快，不执行任何耗时的操作。
    """
    global latest_frame
    with frame_lock: # 使用锁来保证线程安全
        latest_frame = msg

def main_loop():
    """
    这是程序的主循环，所有耗时的处理、发布和显示都在这里完成。
    """
    global stop_publisher, stop_frame_counter, latest_frame

    # 设置循环频率 (例如 30Hz)
    rate = rospy.Rate(30)

    while not rospy.is_shutdown():
        # 检查是否有新的图像帧需要处理
        if latest_frame is None:
            rate.sleep()
            continue

        # 复制最新的图像帧以进行处理，并清空全局变量
        with frame_lock:
            # 将ROS消息格式转换为OpenCV格式
            try:
                current_frame = bridge.imgmsg_to_cv2(latest_frame, 'bgr8')
                latest_frame = None # 处理完后清空，等待下一帧
            except cv_bridge.CvBridgeError as e:
                rospy.logerr(e)
                rate.sleep()
                continue
        
        # --- 在主循环中执行所有处理逻辑 ---
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        tags = detector.detect(gray)

        if tags:
            stop_frame_counter = STOP_LATCH_FRAMES
            for tag in tags:
                cv2.circle(current_frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2)
                cv2.circle(current_frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2)
                cv2.circle(current_frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2)
                cv2.circle(current_frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2)
                print("tag id: ", tag.tag_id)

        should_stop = False
        if stop_frame_counter > 0:
            should_stop = True
            stop_frame_counter -= 1

        if stop_publisher:
            stop_publisher.publish(should_stop)
        
        # --- 显示图像 ---
        cv2.imshow("camera", current_frame)
        cv2.waitKey(1) # 这是保持GUI窗口响应的关键

        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node("apriltag_detector_node")

        # 创建发布者
        stop_publisher = rospy.Publisher('/car1/stop_command', Bool, queue_size=10)

        # 创建订阅者，注意回调函数现在是精简版的image_callback
        rospy.Subscriber("/car1/camera/zed_left/image_rect_color_left", Image, image_callback, queue_size=1, buff_size=2**24)
        
        rospy.loginfo("AprilTag detector node is running...")
        
        # 启动主循环，替代rospy.spin()
        main_loop()

    except rospy.ROSInterruptException:
        pass
    finally:
        # 确保程序退出时关闭所有OpenCV窗口
        cv2.destroyAllWindows()

