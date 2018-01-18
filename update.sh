#!/bin/bash

. "/etc/os-release"
. "logmapper.conf"

#LM_CONF

if [[ "$ID_LIKE" = "debian" ]]; then
	echo "Copying /var/log/auth.log"
	sudo cp /var/log/auth.log "$LM_INSTALL_LOC/auth.log"
elif [[ "$ID_LIKE" = "rhel fedora" ]]; then
	echo "Copying /var/log/secure"
	sudo cp /var/log/secure "$LM_INSTALL_LOC/auth.log"
fi

chmod 444 auth.log

cd $LM_INSTALL_LOC
sudo -u $LM_MAPPER_USER python "$LM_INSTALL_LOC/stats_map.py"
sudo -u $LM_MAPPER_USER python "$LM_INSTALL_LOC/draw_map.py"
sudo -u $LM_MAPPER_USER python3 "$LM_INSTALL_LOC/get_stats.py"
