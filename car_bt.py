import serial
import time
import sys, select, termios, tty
banner = """
1. Reading from the keyboard  
2. Publishing to AckermannDriveStamped!
---------------------------
        w
   a    x    d
        s
anything else : stop
CTRL-C to quit
+shift speed up
"""

def getKey():
   tty.setraw(sys.stdin.fileno())
   select.select([sys.stdin], [], [], 0)
   key = sys.stdin.read(1)
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
   return key
def setto(control):
    bluetooth.flushInput()
    ret = bluetooth.write(str.encode(control))
    print("ret:", ret)
    time.sleep(0.1)
    
if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    bluetooth = serial.Serial("/dev/rfcomm1",115200)
    time.sleep(0.1)
    while(1):
       key = getKey()
       if key == 'w':
           setto("<+00+10>")
       elif key == 'W':
           setto("<+00+20>")
       elif key == 's':
           setto("<+00-10>")
       elif key == 'S':
           setto("<+00-20>")
       elif key == 'a':
           setto("<-45+10>")
       elif key == 'A':
           setto("<-45+20>")
       elif key == 'd':
           setto("<+45+10>")
       elif key == 'D':
           setto("<+45+20>")
       elif key == 'x':
           setto("<+00+00>")
           exit(0)
       print(key)
