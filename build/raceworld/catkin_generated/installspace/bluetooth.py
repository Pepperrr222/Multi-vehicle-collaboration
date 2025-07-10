#! /usr/bin/env python3
import rospy
import serial
import time
import random
from ackermann_msgs.msg import AckermannDriveStamped

def setto(control):
    bluetooth.flushInput()
    bluetooth.write(str.encode(control))
    time.sleep(0.01)
meanAngle = []
def talker(msg):
    global meanAngle                                                                                    
    angle = min(int(abs(-msg.drive.steering_angle) * 45 / 0.1), 45) * [-1, 1][msg.drive.steering_angle < 0]
    if len(meanAngle) < 20:
        meanAngle.append(angle)
        return
    else:
        angle = int(sum(meanAngle) / len(meanAngle))
        meanAngle = meanAngle[1:]
    velocity = int(msg.drive.speed * 80)
    a = ["-","+"][angle >= 0]+["","0"][len(str(abs(angle)))==1]+str(abs(angle))
    v = ["-","+"][velocity >= 0]+["","0"][len(str(abs(velocity)))==1]+str(abs(velocity))
    control = "<" + a + v + ">\n"
    print("\n蓝牙指令:",control)

    setto(control)
    pass
if __name__=="__main__":
    bluetooth = serial.Serial("/dev/rfcomm1",115200)
    
    rospy.init_node("bluetooth")
    rospy.Subscriber("/car1/ackermann_cmd_mux/output", AckermannDriveStamped, talker,queue_size=1)
    rospy.spin()
    if KeyboardInterrupt:
        setto("<+00+00>")
        time.sleep(2)
        bluetooth.close()
    pass
