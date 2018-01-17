#!/bin/bash


#LM_INSTALL_LOC="/home/ec2-user/environment/Log-Mapper"

. "/etc/os-release"
. "log-mapper.conf"

if [[ "$ID_LIKE" = "debian" ]]; then
	echo "Copying /var/log/auth.log"
	sudo cp /var/log/auth.log "$INSTALL_LOC/auth.log"
elif [[ "$ID_LIKE" = "rhel fedora" ]]; then
	echo "Copying /var/log/secure"
	sudo cp /var/log/secure "$INSTALL_LOC/auth.log"
fi

chmod 444 auth.log

cd $LM_INSTALL_LOC
sudo -u $LM_MAPPER_USER python "$INSTALL_LOC/stats_map.py"
sudo -u $LM_MAPPER_USER python "$INSTALL_LOC/draw_map.py"
sudo -u $LM_MAPPER_USER python3 "$INSTALL_LOC/get_stats.py"
