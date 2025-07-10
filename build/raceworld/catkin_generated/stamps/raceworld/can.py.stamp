#!/usr/bin/env python3                                                                                         
import rospy
import time
from ctypes import *
from math import *
from ackermann_msgs.msg import AckermannDriveStamped
ZCAN_DEVICE_TYPE  = c_uint32
ZCAN_DEVICE_INDEX = c_uint32
ZCAN_Reserved     = c_uint32
ZCAN_CHANNEL      = c_uint32
LEN               = c_uint32

USBCAN2       =   ZCAN_DEVICE_TYPE(4)
DEVICE_INDEX  =   ZCAN_DEVICE_INDEX(0)
Reserved      =   ZCAN_Reserved(0)
CHANNEL       =   ZCAN_CHANNEL(0)


class ZCAN_CAN_BOARD_INFO(Structure):
    _fields_ = [("hw_Version",c_ushort),
                ("fw_Version",c_ushort),
                ("dr_Version",c_ushort),
                ("in_Version",c_ushort),
                ("irq_Num",c_ushort),
                ("can_Num",c_ubyte),
                ("str_Serial_Num",c_ubyte*20),
                ("str_hw_Type",c_ubyte*40),
                ("Reserved",c_ubyte*4)]

    def __str__(self):
        return "Hardware Version:%s\nFirmware Version:%s\nDriver Version:%s\nInterface:%s\nInterrupt Number:%s\nCAN_number:%d"%(\
                self.hw_Version,  self.fw_Version,  self.dr_Version,  self.in_Version,  self.irq_Num,  self.can_Num)

    def serial(self):
        serial=''
        for c in self.str_Serial_Num:
            if c>0:
                serial +=chr(c)
            else:
                break
        return serial   
        
    def hw_Type(self):
        hw_Type=''
        for c in self.str_hw_Type:
            if c>0:
                hw_Type +=chr(c)
            else:
                break
        return hw_Type   



class ZCAN_CAN_INIT_CONFIG(Structure):
    _fields_ = [("AccCode",c_int),
                ("AccMask",c_int),
                ("Reserved",c_int),
                ("Filter",c_ubyte),
                ("Timing0",c_ubyte),
                ("Timing1",c_ubyte),
                ("Mode",c_ubyte)]

class ZCAN_CAN_OBJ(Structure):
    _fields_ = [("ID",c_uint32),
                ("TimeStamp",c_uint32),
                ("TimeFlag",c_uint8),
                ("SendType",c_byte),
                ("RemoteFlag",c_byte),
                ("ExternFlag",c_byte),
                ("DataLen",c_byte),
                ("Data",c_ubyte*8),
                ("Reserved",c_ubyte*3)]

def GetDeviceInf(DeviceType,DeviceIndex,lib):
    try:
        info = ZCAN_CAN_BOARD_INFO()
        ret  = lib.VCI_ReadBoardInfo(DeviceType,DeviceIndex,byref(info))
        return info if ret==1 else None
    except:
        print("Exception on readboardinfo")
        raise
                
def can_start(DEVCIE_TYPE,DEVICE_INDEX,CHANNEL,lib):
     init_config  = ZCAN_CAN_INIT_CONFIG()
     init_config.AccCode    = 0
     init_config.AccMask    = 0xFFFFFFFF
     init_config.Reserved   = 0
     init_config.Filter     = 1
     init_config.Timing0    = 0x00
     init_config.Timing1    = 0x14 #波特率1000k
     init_config.Mode       = 0
     ret=lib.VCI_InitCAN(DEVCIE_TYPE,DEVICE_INDEX,0,byref(init_config))   
     ret=lib.VCI_StartCAN(DEVCIE_TYPE,DEVICE_INDEX,CHANNEL)
     return ret
meanAngle = []
def talker(msg):
    global meanAngle                                                                                    
    #angle = min(int(abs(-msg.drive.steering_angle) * 50 / 0.3), 50) * [1, -1][msg.drive.steering_angle < 0]
    angle = int((-msg.drive.steering_angle + 6.28) * 180 / 3.14)
    if angle >= 180:
        angle -= 360
    #print(angle, -msg.drive.steering_angle)
    """if angle < 360:
        angle -= 360
    elif angle >= 360:
        angle %= 360"""
    if len(meanAngle) < 20:
        meanAngle.append(angle)
        return
    else:
        angle = int(sum(meanAngle) / len(meanAngle))
        #print(angle)
        meanAngle = meanAngle[1:]
    velocity = int(msg.drive.speed * 80)
    #print("\nCAN CAR angle:",angle," velocity:",velocity)
    Data = [abs(velocity),abs(velocity),[1,0][velocity >= 0],[0,1][velocity >= 0],[1,0][velocity >= 0],[0,1][velocity >= 0],max(0, 50 + angle * 2),7]
    for j in range(msgs.DataLen):
        msgs.Data[j] = Data[j] 
    lib.VCI_Transmit(4,0,0,byref(msgs),1) #important!
    lib.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL)
    print("Data:",Data)
    pass

if __name__ == '__main__':
    lib = cdll.LoadLibrary("libusbcan.so")
    lib.VCI_OpenDevice(USBCAN2,DEVICE_INDEX,Reserved)
   

    #info= GetDeviceInf(USBCAN2,DEVICE_INDEX,lib)
    #print("Devcie Infomation:\n%s"%(info))
    
    canstart = can_start(USBCAN2,DEVICE_INDEX,CHANNEL,lib)
    msgs=(ZCAN_CAN_OBJ)()
    msgs.ID = 0xFE
    msgs.TimeStamp = 0
    msgs.TimeFlag = 0
    msgs.SendType = 2 # self test  
    msgs.RemoteFlag = 0 # 0---Data frame , 1---remote frame
    msgs.ExternFlag = 0 # 0---Standard frame , 1---Extern frame
    msgs.DataLen = 8 # DLC,0~8
    rospy.init_node("can")
    rospy.Subscriber("/car1/ackermann_cmd_mux/output", AckermannDriveStamped, talker,queue_size=1)
    rospy.spin()
    if KeyboardInterrupt:
        Data = [0,0,0,1,0,1,50,7]
        for j in range(msgs.DataLen):
            msgs.Data[j] = Data[j]
        lib.VCI_Transmit(4,0,0,byref(msgs),1)
        lib.VCI_GetReceiveNum(USBCAN2,DEVICE_INDEX,CHANNEL)
        #print("Data:",Data)
        time.sleep(1)
        lib.VCI_ResetCAN(USBCAN2,DEVICE_INDEX,CHANNEL)
        lib.VCI_CloseDevice(USBCAN2,DEVICE_INDEX)
        del lib  
    pass
