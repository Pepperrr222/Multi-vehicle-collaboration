sudo -S killall rfcomm << EOF
richouu
EOF
#sudo rfcomm connect /dev/rfcomm1 98:DA:F0:00:43:31 1 &
sudo rfcomm connect /dev/rfcomm1 98:DA:F0:00:12:34 1 &
sleep 6
sudo -S sudo chmod 777 /dev/rfcomm1 << EOF
richouu
EOF
sudo -S sudo minicom -D /dev/rfcomm1 << EOF
richouu
EOF
