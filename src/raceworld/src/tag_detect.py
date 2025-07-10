#! /usr/bin/env python3
import rospy, cv2, cv_bridge
from sensor_msgs.msg import Image
import pyapriltags

#1. 导入标准消息类型 Bool
from std_msgs.msg import Bool
#2. 在全局创建一个发布者变量
# 我们将在主函数中初始化它
pit_detected_pub = None


def image_callback(msg):
    global pit_detected_pub

    detector = pyapriltags.Detector()
    bridge = cv_bridge.CvBridge()
    frame = bridge.imgmsg_to_cv2(msg, 'bgr8')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.namedWindow("gray image",0)
    #cv2.imshow('gray image', gray)
    if detector.detect(gray):
        tags = detector.detect(gray)
    # if not tags:
        for tag in tags:
            cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
            cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
            cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
            cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
            print("tag id: ", tag.tag_id)
    cv2.namedWindow("camera",0)
    cv2.imshow('camera', frame)
    cv2.waitKey(1)
    
    #4. 只要发布者存在，就发布消息
    # 无论是否检测到，都会发布一个布尔值 (True 或 False)
    if pit_detected_pub is not None:
        pit_detected_pub.publish(detection_msg)

def get_camera():
    rospy.Subscriber("/car1/camera/zed_left/image_rect_color_left", Image, image_callback)

if __name__ == '__main__':
    rospy.init_node("tag_detector")
    
    # 在启动订阅者之前，初始化全局发布者
    # 发布到 /car1/pit_detected 话题
    pit_detected_pub = rospy.Publisher('/car1/pit_detected', Bool, queue_size=1)
    get_camera()
    rospy.spin()
