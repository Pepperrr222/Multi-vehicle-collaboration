#! /usr/bin/env python3
import rospy
from std_msgs.msg import Bool
from ackermann_msgs.msg import AckermannDriveStamped

class Car1MainController:
    def __init__(self):
        # 初始化ROS节点
        rospy.init_node('car1_main_controller')
        
        # --- 状态变量 ---
        # pit_detected 用来记录是否检测到坑
        self.pit_detected = False
        # lane_vel_suggestion 用来存储来自巡线节点的最新建议速度
        self.lane_vel_suggestion = AckermannDriveStamped()

        # --- 订阅者 ---
        # 1. 订阅来自 tag_detect.py 的坑检测信号
        rospy.Subscriber('/car1/pit_detected', Bool, self.pit_callback)
        
        # 2. 订阅来自 lane.py 的巡线建议
        rospy.Subscriber('/car1/lane_vel_suggestion', AckermannDriveStamped, self.lane_callback)

        # --- 发布者 ---
        # 这个发布者将向小车发送最终的、经过决策的控制指令
        self.final_cmd_pub = rospy.Publisher('/car1/ackermann_cmd_mux/output', AckermannDriveStamped, queue_size=1)
        
        rospy.loginfo("Car1 Main Controller is running.")

    def pit_callback(self, msg):
        """当收到坑检测信号时，更新状态变量"""
        if msg.data:
            rospy.logwarn("PIT DETECTED! Stopping the car.")
        self.pit_detected = msg.data

    def lane_callback(self, msg):
        """当收到巡线建议时，存储它"""
        self.lane_vel_suggestion = msg

    def run_controller(self):
        """主循环，根据状态做出决策"""
        rate = rospy.Rate(20) # 20 Hz
        
        # 创建一个用于停车的指令（所有速度和角度都为0）
        stop_command = AckermannDriveStamped()
        stop_command.header.frame_id = "base_link" # 确保frame_id正确
        stop_command.drive.speed = 0.0
        stop_command.drive.steering_angle = 0.0

        while not rospy.is_shutdown():
            final_command = AckermannDriveStamped()
            
            # --- 核心决策逻辑 ---
            if self.pit_detected:
                # 如果检测到了坑，最终指令就是“停车”
                final_command = stop_command
            else:
                # 如果没有检测到坑，最终指令就采纳“巡线建议”
                final_command = self.lane_vel_suggestion
            
            # 无论做出何种决策，都更新时间戳并发布最终指令
            final_command.header.stamp = rospy.Time.now()
            self.final_cmd_pub.publish(final_command)
            
            rate.sleep()

if __name__ == '__main__':
    try:
        controller = Car1MainController()
        controller.run_controller()
    except rospy.ROSInterruptException:
        pass
