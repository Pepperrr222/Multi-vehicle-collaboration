gnome-terminal -t "raceworld_1car" -- bash -c 'source devel/setup.bash;roslaunch raceworld raceworld_1car.launch;bash'
sleep 4  
gnome-terminal -t "key_op" -- bash -c 'source devel/setup.bash;rosrun raceworld key_op.py;bash'
gnome-terminal -t "tag_detect" -- bash -c 'source devel/setup.bash;rosrun raceworld tag_detect.py;bash'
